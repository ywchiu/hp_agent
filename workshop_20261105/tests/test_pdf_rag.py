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


def stored_fixture(directory, rows, vectors):
    client=rag.chromadb.PersistentClient(path=str(Path(directory)/'chroma'), settings=rag.Settings(anonymized_telemetry=False))
    collection=client.create_collection('fixture', embedding_function=None,
        configuration={'hnsw':{'space':'cosine','num_threads':2}})
    collection.upsert(ids=[r['id'] for r in rows],embeddings=vectors,
        documents=[r['text'] for r in rows],metadatas=[{'file':r['file'],'page':r['page']} for r in rows])
    files=list(dict.fromkeys(r['file'] for r in rows))
    return {'identity':{'embedding_model':rag.EMBEDDING_MODEL},'dimensions':len(vectors[0]),
            'db_path':str(Path(directory)/'chroma'),'collection_name':'fixture','row_count':len(rows),
            'document':[{'file':name,'chunks':sum(r['file']==name for r in rows)} for name in files]}


class PDFRag(unittest.TestCase):
    def test_official_download_validates_and_reuses_complete_pdf(self):
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/'source.pdf';make_pdf(source)
            calls=[]
            def handle(request):
                calls.append(str(request.url))
                return rag.httpx.Response(200,content=source.read_bytes())
            client=rag.httpx.Client(transport=rag.httpx.MockTransport(handle))
            with patch.object(rag,'PDF_SOURCES',{'hp_manual.pdf':'https://example.test/hp.pdf'}), patch.object(rag.httpx,'Client',return_value=client):
                result=rag.download_pdfs(Path(d)/'downloads')
                self.assertEqual(result[0]['status'],'downloaded')
                self.assertEqual(rag.download_pdfs(Path(d)/'downloads')[0]['status'],'reused')
            self.assertEqual(len(calls),1)
            self.assertEqual((Path(d)/'downloads/hp_manual.pdf').read_bytes(),source.read_bytes())
            self.assertFalse(list((Path(d)/'downloads').glob('*.part')))

    def test_failed_or_html_download_never_becomes_pdf(self):
        for status,body in [(403,b'blocked'),(200,b'<html>denied</html>'),(200,b'%PDF-1.7 truncated')]:
            with self.subTest(status=status,body=body),tempfile.TemporaryDirectory() as d:
                client=rag.httpx.Client(transport=rag.httpx.MockTransport(lambda req:rag.httpx.Response(status,content=body)))
                with patch.object(rag,'PDF_SOURCES',{'hp_manual.pdf':'https://example.test/hp.pdf'}),patch.object(rag.httpx,'Client',return_value=client):
                    with self.assertRaisesRegex(ValueError,'AUTO_DOWNLOAD'):rag.download_pdfs(d)
                self.assertFalse((Path(d)/'hp_manual.pdf').exists())
                self.assertFalse(list(Path(d).glob('*.part')))

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
        with tempfile.TemporaryDirectory() as d:
            index=stored_fixture(d,[{'id':'PDF-0001','file':'hp.pdf','page':1,'text':'replaceable RAM'},
                                    {'id':'PDF-0002','file':'hp.pdf','page':2,'text':'battery'}],[[1.,0.],[0.,1.]])
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

    @patch.object(rag,'OpenAI')
    def test_chroma_persistence_manifest_and_missing_collection_rebuild(self,sdk):
        sdk.return_value.embeddings.create.side_effect=embedding_response
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'manual.pdf';make_pdf(path)
            index=rag.build_index(path,'qa',out=d)
            manifest=json.loads(next(Path(d,'indexes').glob('*.json')).read_text())
            self.assertNotIn('vectors',manifest)
            self.assertNotIn('rows',manifest)
            self.assertTrue((Path(index['db_path'])/'chroma.sqlite3').exists())
            reopened=rag.inspect_index(manifest)
            self.assertEqual(reopened['count'],index['row_count'])
            self.assertEqual(reopened['sample'][0]['page'],1)
            client=rag.chromadb.PersistentClient(path=index['db_path'],settings=rag.Settings(anonymized_telemetry=False))
            client.delete_collection(index['collection_name'])
            with self.assertRaises(Exception):rag.collection_for(index)
            rebuilt=rag.build_index(path,'qa',out=d)
            self.assertFalse(rebuilt['reused'])
            self.assertEqual(rag.inspect_index(rebuilt)['count'],index['row_count'])
            self.assertEqual(sdk.return_value.embeddings.create.call_count,2)

    def test_embedding_incomplete_or_invalid_vectors_refused(self):
        client=SimpleNamespace(embeddings=SimpleNamespace(create=lambda **kw:SimpleNamespace(data=[],usage=None)))
        with self.assertRaisesRegex(ValueError,'不完整'):rag.embed(client,['x'],rag.EMBEDDING_MODEL)
        for vector in ([0.,0.],[float('nan'),1.],[]):
            with self.assertRaises(ValueError):rag.normalize(vector)

    @patch.object(rag,'OpenAI')
    def test_graph_calls_query_embedding_then_answer_and_retains_pages(self,sdk):
        sdk.return_value.embeddings.create.side_effect=embedding_response
        sdk.return_value.responses.create.return_value=SimpleNamespace(output_text='manual.pdf PDF第7頁 [PDF-0001]；台灣報價待確認。',status='completed',id='qa-response',usage=None)
        with tempfile.TemporaryDirectory() as d:
            index=stored_fixture(d,[{'id':'PDF-0001','file':'manual.pdf','page':7,'text':'Memory is replaceable.'}],
                                  [rag.normalize([1.,1.])])
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
    def test_preview_and_answer_use_exact_same_retrieval_without_second_embedding(self,sdk):
        sdk.return_value.embeddings.create.side_effect=embedding_response
        sdk.return_value.responses.create.return_value=SimpleNamespace(output_text='證據 [PDF-0001]',status='completed',id='qa',usage=None)
        with tempfile.TemporaryDirectory() as d:
            index=stored_fixture(d,[{'id':'PDF-0001','file':'hp.pdf','page':7,'text':'<script>bad</script> Memory module.'}],
                                  [rag.normalize([1.,1.])])
            preview=rag.retrieve_pdf('記憶體?',index,'qa',k=1)
            self.assertEqual(sdk.return_value.responses.create.call_count,0)
            html=rag.retrieval_html(preview)
            self.assertIn('&lt;script&gt;',html)
            self.assertNotIn('<script>',html)
            self.assertIn('展開完整片段',html)
            result=rag.run_pdf_rag('記憶體?',index,'qa',k=1,out=d,retrieval=preview)
            self.assertEqual(result['rows'],preview['rows'])
            self.assertEqual(sdk.return_value.embeddings.create.call_count,1)
            self.assertEqual(sdk.return_value.responses.create.call_count,1)
            for question,k in [('新問題',1),('記憶體?',2)]:
                with self.assertRaisesRegex(ValueError,'先重跑搜尋'):
                    rag.run_pdf_rag(question,index,'qa',k=k,out=d,retrieval=preview)

    @patch.object(rag,'OpenAI')
    def test_competitor_documents_keep_unique_ids_and_each_gets_evidence(self,sdk):
        sdk.return_value.embeddings.create.side_effect=embedding_response
        with tempfile.TemporaryDirectory() as d:
            paths=[]
            for name in ('hp','lenovo','dell'):
                p=Path(d)/(name+'.pdf');make_pdf(p,name+' Memory module and SSD specifications. ');paths.append(p)
            index=rag.build_index(paths,'qa',out=d)
            self.assertEqual(len(index['document']),3)
            stored=rag.collection_for(index).get(include=['metadatas','documents','embeddings'])
            self.assertEqual(len(set(stored['ids'])),index['row_count'])
            self.assertEqual(len(stored['embeddings']),index['row_count'])
            self.assertNotIn('vectors',index)
            self.assertNotIn('rows',index)
            rows,_=rag.search(index,'比較三品牌記憶體',sdk.return_value,k=1)
            self.assertEqual({r['file'] for r in rows},{'hp.pdf','lenovo.pdf','dell.pdf'})
            self.assertEqual(len(rows),3)
            with self.assertRaisesRegex(ValueError,'相同內容|檔名重複'):
                rag.build_index([paths[0],paths[0]],'qa',out=d)


if __name__=='__main__':unittest.main()
