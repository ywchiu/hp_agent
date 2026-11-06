"""實際PDF抽文、向量排序、索引身分與問答圖的回歸檢查。"""
import importlib.util
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from pypdf import PdfWriter
from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject

spec = importlib.util.spec_from_file_location('pdf_rag', Path(__file__).resolve().parents[1]/'day2/pdf_rag.py')
rag = importlib.util.module_from_spec(spec); spec.loader.exec_module(rag)


def make_pdf(path, text='Memory module replacement. Only authorized service providers may replace the SSD. '):
    writer = PdfWriter()
    for content in [text*20, 'Battery and USB Type-C connectors. '*20]:
        page = writer.add_blank_page(width=600, height=800)
        font = DictionaryObject({NameObject('/Type'): NameObject('/Font'),
                                 NameObject('/Subtype'): NameObject('/Type1'),
                                 NameObject('/BaseFont'): NameObject('/Helvetica')})
        page[NameObject('/Resources')] = DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/F1'):font})})
        stream = DecodedStreamObject()
        stream.set_data(('BT /F1 10 Tf 10 700 Td ('+content+') Tj ET').encode())
        page[NameObject('/Contents')] = writer._add_object(stream)
    writer.write(path)


def embedding_response(**kwargs):
    return SimpleNamespace(data=[SimpleNamespace(index=i, embedding=[1., float(i+1)]) for i,_ in enumerate(kwargs['input'])], usage=None)


class PDFRag(unittest.TestCase):
    def test_real_pdf_pages_chunk_overlap_and_no_text(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'manual.pdf'; make_pdf(path)
            doc=rag.extract_pdf(path, chunk_size=400, overlap=60)
            self.assertEqual(doc['pages'],2)
            self.assertEqual({r['page'] for r in doc['rows']},{1,2})
            self.assertEqual(doc['rows'][0]['text'][-60:], doc['rows'][1]['text'][:60])
            self.assertTrue(all(len(r['text'])<=400 for r in doc['rows']))
            writer=PdfWriter();writer.add_blank_page(width=100,height=100);writer.write(path)
            with self.assertRaisesRegex(ValueError,'OCR'):rag.extract_pdf(path)
            path.write_text('fake PDF')
            with self.assertRaisesRegex(ValueError,'內容不是PDF'):rag.extract_pdf(path)

    def test_semantic_ranking_is_vector_based(self):
        # 中文問題沒有任何與英文段落共同的詞，仍按向量取回第一段。
        index={'identity':{'embedding_model':rag.EMBEDDING_MODEL},'dimensions':2,
               'rows':[{'id':'PDF-0001','text':'replaceable RAM'}, {'id':'PDF-0002','text':'battery'}],
               'vectors':[[1.,0.],[0.,1.]]}
        client=SimpleNamespace(embeddings=SimpleNamespace(create=lambda **kw:SimpleNamespace(
            data=[SimpleNamespace(index=0,embedding=[1.,0.])],usage=None)))
        rows,_=rag.search(index,'記憶體能升級嗎',client,k=1)
        self.assertEqual(rows[0]['id'],'PDF-0001')
        self.assertAlmostEqual(rows[0]['score'],1.)
        with self.assertRaises(ValueError):rag.search(index,'',client)
        with self.assertRaises(ValueError):rag.search(index,'問題',client,k=13)

    @patch.object(rag,'OpenAI')
    def test_cache_identity_changes_with_pdf_settings_and_model(self,sdk):
        sdk.return_value.embeddings.create.side_effect=embedding_response
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'manual.pdf';make_pdf(path)
            first=rag.build_index(path,'qa',out=d)
            repeated=rag.build_index(path,'qa',out=d)
            self.assertFalse(first['reused']);self.assertTrue(repeated['reused'])
            self.assertEqual(sdk.return_value.embeddings.create.call_count,1)
            self.assertEqual(repeated['embedding_calls_this_run'],[])
            rag.build_index(path,'qa',out=d,chunk_size=800)
            rag.build_index(path,'qa',out=d,model='other-model')
            make_pdf(path,'New memory configuration and different computer. ')
            changed=rag.build_index(path,'qa',out=d)
            self.assertFalse(changed['reused'])
            self.assertEqual(len(list(Path(d,'indexes').glob('*.json'))),4)

    def test_embedding_incomplete_or_invalid_vectors_refused(self):
        client=SimpleNamespace(embeddings=SimpleNamespace(create=lambda **kw:SimpleNamespace(data=[],usage=None)))
        with self.assertRaisesRegex(ValueError,'不完整'):rag.embed(client,['x'],rag.EMBEDDING_MODEL)
        for vector in ([0.,0.],[float('nan'),1.],[]):
            with self.assertRaises(ValueError):rag.normalize(vector)

    @patch.object(rag,'OpenAI')
    def test_graph_calls_query_embedding_then_answer_and_retains_pages(self,sdk):
        sdk.return_value.embeddings.create.side_effect=embedding_response
        sdk.return_value.responses.create.return_value=SimpleNamespace(output_text='manual.pdf PDF第7頁 [PDF-0001]；台灣報價待確認。',status='completed',id='qa-response',usage=None)
        index={'identity':{'embedding_model':rag.EMBEDDING_MODEL},'document':{'file':'manual.pdf','sha256':'qa'},
               'dimensions':2,'vectors':[rag.normalize([1.,1.])],
               'rows':[{'id':'PDF-0001','file':'manual.pdf','page':7,'text':'Memory is replaceable.'}]}
        with tempfile.TemporaryDirectory() as d:
            result=rag.run_pdf_rag('台灣價格?',index,'qa',out=d)
            self.assertEqual(result['validation']['status'],'ids_valid')
            self.assertEqual(result['validation']['pages'][0]['pdf_page'],7)
            self.assertEqual(sdk.return_value.embeddings.create.call_count,1)
            self.assertEqual(sdk.return_value.responses.create.call_count,1)
            request=sdk.return_value.responses.create.call_args.kwargs
            self.assertEqual(request['model'],'gpt-6-luna')
            self.assertIn('文件資料',request['instructions'])
            self.assertIn('PDF第7頁',request['input'])
            self.assertNotIn('qa-response',Path(d,'report.md').read_text())
            self.assertEqual(json.loads(Path(d,'trace.json').read_text())['embedding_model'],rag.EMBEDDING_MODEL)

    def test_citations_must_exist_in_retrieved_pages(self):
        rows=[{'id':'PDF-0001','file':'m.pdf','page':5}]
        self.assertEqual(rag.check_citations('[PDF-9999]',rows)['unknown_ids'],['PDF-9999'])
        self.assertEqual(rag.check_citations('沒有引用',rows)['status'],'needs_review')

    @patch.object(rag,'OpenAI')
    def test_competitor_documents_keep_unique_ids_and_each_gets_evidence(self,sdk):
        sdk.return_value.embeddings.create.side_effect=embedding_response
        with tempfile.TemporaryDirectory() as d:
            paths=[]
            for name in ('hp','lenovo','dell'):
                p=Path(d)/(name+'.pdf');make_pdf(p,name+' Memory module and SSD specifications. ');paths.append(p)
            index=rag.build_index(paths,'qa',out=d)
            self.assertEqual(len(index['document']),3)
            self.assertEqual(len({r['id'] for r in index['rows']}),len(index['rows']))
            rows,_=rag.search(index,'比較三品牌記憶體',sdk.return_value,k=1)
            self.assertEqual({r['file'] for r in rows},{'hp.pdf','lenovo.pdf','dell.pdf'})
            self.assertEqual(len(rows),3)
            with self.assertRaisesRegex(ValueError,'相同內容|檔名重複'):
                rag.build_index([paths[0],paths[0]],'qa',out=d)


if __name__=='__main__':unittest.main()
