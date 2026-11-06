"""深度研究的真實圖路由、補查、讀取失敗與付費呼叫邊界。"""
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import httpx
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'day2'))
import deep_research as research


def fake_request(self,role,prompt,rows=(),schema=None,search=False):
    self.log.append({'role':role,'web_search_calls':int(search),'used_cache':False})
    if role=='Planner':
        follow='Critic：' in prompt
        return {'questions':[{'question':'補查台灣服務' if follow else '比較硬體','query':'Taiwan service' if follow else 'hardware official','purpose':'核對證據'}]}
    if search:
        return [{'url':'https://www.hp.com/'+('service' if role.endswith('02') else 'hardware'),'title':'Official'}]
    if role.startswith('Reader'):
        live=[r for r in rows if r['origin']=='live'];id_=(live or rows)[0]['id']
        return {'answer':'仍需確認 ['+id_+']','evidence_ids':[id_],'public_gaps':['台灣服務條件'],'supplier_questions':['正式報價']}
    if role=='Critic':
        return {'is_sufficient':False,'score':6,'critique':'需要補查','public_gaps':['台灣服務條件'],'supplier_questions':['正式報價'],'conflicts':[]}
    return '研究結果 [HP-01]；仍需正式報價。'


def original(url):
    return {'url':url,'checked_on':'2026-11-06','status':'read_ok','kind':'HTML','sha256':url.rsplit('/',1)[-1],
            'pieces':[{'page':0,'text':url+' Official hardware and service conditions. '*8}]}


class ResearchGraph(unittest.TestCase):
    @patch.object(research.ResearchModel,'request',fake_request)
    @patch.object(research,'fetch_original',original)
    def test_pause_replan_accumulate_and_finish_once(self):
        with tempfile.TemporaryDirectory() as out:
            session=research.ResearchSession('120台台灣採購','qa-secret',out=out)
            first=session.advance()
            self.assertEqual([r['role'] for r in session.llm.log],['Planner'])
            self.assertEqual(session.app.get_state(session.config).next,('searcher',))
            first=session.advance()
            self.assertEqual(len(first['history']),1)
            self.assertEqual(first['round_added'],1)
            self.assertEqual(session.app.get_state(session.config).next,('planner',))
            plan=session.advance()
            self.assertEqual(plan['current_questions'][0]['id'],'Q02')
            self.assertEqual(len(plan['history']),1)
            final=session.finish()
            self.assertEqual(final['round'],2)
            self.assertEqual([r['new_evidence'] for r in final['history']],[1,1])
            self.assertEqual(len(final['readings']),2)
            self.assertEqual(final['stop_reason'],'max_rounds')
            self.assertEqual(final['validation']['status'],'ids_valid')
            calls=len(session.llm.log)
            self.assertEqual(session.finish(),final)
            self.assertEqual(session.advance(),final)
            self.assertEqual(len(session.llm.log),calls)
            trace=Path(out,'trace.json').read_text()
            self.assertNotIn('qa-secret',trace)
            self.assertEqual(json.loads(trace)['next_nodes'],[])

    @patch.object(research.ResearchModel,'request',fake_request)
    @patch.object(research,'fetch_original',lambda url:dict(original(url),status='http_403',pieces=[]))
    def test_failed_pages_never_become_evidence(self):
        with tempfile.TemporaryDirectory() as out:
            s=research.ResearchSession('比較','qa',out=out).finish()
            self.assertFalse(any(r['origin']=='live' for r in s['evidence']))
            self.assertTrue(all(g['pages'][0]['status']=='http_403' for g in s['searches']))
            self.assertFalse(list(Path(out,'pages').glob('*.json')))

    @patch.object(research.ResearchModel,'request',fake_request)
    def test_snapshot_no_native_search_or_get(self):
        with tempfile.TemporaryDirectory() as out,patch.object(research,'fetch_original') as fetch:
            session=research.ResearchSession('比較','qa',max_rounds=1,mode='snapshot',out=out)
            s=session.finish()
            fetch.assert_not_called()
            self.assertEqual(sum(r['web_search_calls'] for r in session.llm.log),0)
            self.assertEqual(s['round'],1)
            self.assertTrue(s['report'])

    def test_supplier_only_stops_after_first_cycle(self):
        def request(model,role,*args,**kwargs):
            value=fake_request(model,role,*args,**kwargs)
            if role=='Critic':value['public_gaps']=[]
            return value
        with tempfile.TemporaryDirectory() as out,patch.object(research.ResearchModel,'request',request):
            session=research.ResearchSession('比較','qa',mode='snapshot',out=out)
            final=session.finish()
            self.assertEqual(final['round'],1)
            self.assertEqual(final['stop_reason'],'supplier_confirmation')
            self.assertEqual(sum(r['role']=='Planner' for r in session.llm.log),1)

    def test_stop_rules_distinguish_supplier_and_public_gaps(self):
        base={'round':1,'max_rounds':3,'round_added':0,'critique':{'is_sufficient':True,'public_gaps':[]}}
        self.assertEqual(research.next_action(base),'sufficient')
        base['critique']={'is_sufficient':False,'public_gaps':[]}
        self.assertEqual(research.next_action(base),'supplier_confirmation')
        base['critique']['public_gaps']=['公開資料'];self.assertEqual(research.next_action(base),'planner')
        base['round']=2;self.assertEqual(research.next_action(base),'no_new_evidence')

    @patch.object(research.ResearchModel,'request',lambda *a,**k:{'questions':[]})
    def test_initial_empty_plan_is_error(self):
        with tempfile.TemporaryDirectory() as out:
            with self.assertRaisesRegex(ValueError,'有效研究問題'):
                research.ResearchSession('比較','qa',out=out).advance()


class OfficialReading(unittest.TestCase):
    def test_redirect_to_unapproved_host_blocked(self):
        requests=[]
        def handle(req):
            requests.append(str(req.url));return httpx.Response(302,headers={'location':'https://outside.invalid/a'})
        real_client=httpx.Client
        with patch.object(research.httpx,'Client',lambda **kw:real_client(transport=httpx.MockTransport(handle),**kw)):
            result=research.fetch_original('https://www.hp.com/a')
        self.assertEqual(result['status'],'read_failed');self.assertEqual(len(requests),1)

    def test_html_extract_and_block_page(self):
        real_client=httpx.Client
        for body,status in [('<html><script>HIDDEN_SECRET</script><main>'+('Hardware memory 32GB. '*12)+'</main></html>','read_ok'),('<html>Access denied</html>','blocked_page')]:
            with patch.object(research.httpx,'Client',lambda **kw:real_client(transport=httpx.MockTransport(lambda req:httpx.Response(200,text=body,headers={'content-type':'text/html'})),**kw)):
                value=research.fetch_original('https://www.hp.com/a')
            self.assertEqual(value['status'],status)
            self.assertNotIn('HIDDEN_SECRET',json.dumps(value['pieces']))

    def test_unknown_citations_and_official_domain(self):
        self.assertEqual(research.citation_check('[WEB-0002]',[{'id':'WEB-0001'}])['unknown_ids'],['WEB-0002'])
        for url in ['https://hp.com.evil.invalid/x','http://hp.com/a','https://user@hp.com/a']:
            with self.assertRaises(ValueError):research.canonical_url(url)


class NativeSearch(unittest.TestCase):
    def test_structured_reply_prose_normalized_but_invalid_rejected(self):
        valid={'questions':[{'question':'規格','query':'hardware','purpose':'核對'}]}
        value,normalized=research.parse_structured('說明\n```json\n'+json.dumps(valid)+'\n```',research.Plan)
        self.assertEqual(value,valid);self.assertTrue(normalized)
        with self.assertRaisesRegex(RuntimeError,'結構驗證'):
            research.parse_structured('沒有物件',research.Plan)
        with self.assertRaisesRegex(RuntimeError,'結構驗證'):
            research.parse_structured(json.dumps({'questions':'wrong type'}),research.Plan)

    def test_reader_unknown_id_not_cached_as_success(self):
        with tempfile.TemporaryDirectory() as out,patch.object(research,'OpenAI') as sdk:
            sdk.return_value.responses.create.return_value=SimpleNamespace(status='completed',output_text=json.dumps({'answer':'錯誤 [WEB-9999]','evidence_ids':['WEB-9999'],'public_gaps':[],'supplier_questions':[]}))
            model=research.ResearchModel('qa','gpt-6-luna',out)
            with self.assertRaisesRegex(ValueError,'未保存'):
                model.request('Reader Q01','讀取',schema=research.Reading)
            self.assertFalse(list(Path(out).rglob('*.json')))

    def test_requires_tool_sources_logs_queries_and_caches(self):
        class Response:
            status='completed';output_text='搜尋結果';id='test-response';usage=None
            def model_dump(self,**kw):
                return {'output':[{'type':'web_search_call','id':'call1','action':{'queries':['hardware official'],'sources':None}},{'type':'message','content':[{'annotations':[{'type':'url_citation','url':'https://www.hp.com/a','title':'HP'},{'type':'url_citation','url':'https://outside.invalid/a'}]}]}]}
        with tempfile.TemporaryDirectory() as out,patch.object(research,'OpenAI') as sdk:
            sdk.return_value.responses.create.return_value=Response()
            model=research.ResearchModel('qa','gpt-6-luna',out)
            first=model.request('Searcher Q01','hardware',search=True)
            self.assertEqual(first,[{'url':'https://www.hp.com/a','title':'HP'}])
            self.assertEqual(model.log[0]['actual_queries'],['hardware official'])
            self.assertEqual(model.request('Searcher Q01','hardware',search=True),first)
            self.assertEqual(sdk.return_value.responses.create.call_count,1)
            self.assertTrue(model.log[-1]['used_cache'])
            self.assertEqual(sdk.return_value.responses.create.call_args.kwargs['include'],['web_search_call.action.sources'])
            model.request('Searcher Q01','changed query',search=True)
            self.assertEqual(sdk.return_value.responses.create.call_count,2)


if __name__=='__main__':unittest.main()
