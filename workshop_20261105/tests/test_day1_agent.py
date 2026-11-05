import json
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from day1_fakes import FakeClient, response, tool

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'day1'))
from research_agent import run_research, local_tool


class Day1Tests(unittest.IsolatedAsyncioTestCase):
    async def test_mcp_with_notebook_stderr_without_fileno(self):
        from mcp.client.stdio import stdio_client
        notebook_stderr=io.StringIO()
        with self.assertRaises(io.UnsupportedOperation):
            notebook_stderr.fileno()
        # MCP 的預設 errlog 在 import 時綁定；模擬 Colab 的無 fileno 串流。
        with patch.object(stdio_client.__wrapped__, '__defaults__', (notebook_stderr,)):
            with tempfile.TemporaryDirectory() as folder:
                result=await run_research(client=FakeClient(),data_path=ROOT/'data/products.json',
                    mcp_server=ROOT/'day1/company_database.py',output_dir=folder)
                self.assertEqual(result['tool_log'][0]['transport'],'mcp')
                self.assertEqual(result['tool_log'][0]['result']['status'],'ok')
                self.assertTrue((Path(folder)/'mcp_server.log').exists())

    async def test_real_openai_sdk_with_mock_http_tool_round_trip(self):
        import httpx
        from openai import AsyncOpenAI
        fake=FakeClient()
        async def handler(request):
            body=json.loads(request.content)
            generated=await fake.create(**body)
            return httpx.Response(200,json={'id':'resp_test', 'object':'response', 'created_at':0,
                'status':'completed', 'model':body['model'], 'output':[i.model_dump() for i in generated.output],
                'parallel_tool_calls':True,'tool_choice':'auto','tools':body['tools']})
        async with AsyncOpenAI(api_key='qa-only-not-a-key',http_client=httpx.AsyncClient(
                transport=httpx.MockTransport(handler))) as client:
            with tempfile.TemporaryDirectory() as folder:
                result=await run_research(client=client,data_path=ROOT/'data/products.json',output_dir=folder)
                self.assertEqual(result['model_calls'],3)
                self.assertIn('待確認',result['report'])
                self.assertFalse(fake.requests[0]['store'])

    async def test_model_selects_tools_and_receives_actual_rows(self):
        client=FakeClient()
        with tempfile.TemporaryDirectory() as folder:
            result=await run_research(api_key='qa-only-not-a-key', client=client,
                data_path=ROOT/'data/products.json', output_dir=folder)
            self.assertEqual(result['model_calls'],3)
            self.assertEqual(len(result['tool_log']),3)
            self.assertIsNone(result['tool_log'][2]['result']['product']['warranty_years'])
            self.assertEqual(result['tool_log'][0]['transport'],'local')
            self.assertNotIn('qa-only-not-a-key', ''.join(p.read_text() for p in Path(folder).iterdir()))
            returned=client.requests[1]['input'][-1]
            self.assertEqual(returned['type'],'function_call_output')
            self.assertEqual(len(json.loads(returned['output'])['products']),2)

    async def test_plain_skill_is_sent_on_every_model_call(self):
        skill='請用三句話向採購主管說明差異；未知保留待確認。'
        client=FakeClient()
        with tempfile.TemporaryDirectory() as folder:
            await run_research(skill=skill, client=client, data_path=ROOT/'data/products.json', output_dir=folder)
            self.assertTrue(all(r['instructions'].endswith(skill) for r in client.requests))
            self.assertEqual(json.loads((Path(folder)/'research_log.json').read_text())['skill'],skill)

    async def test_true_mcp_discovery_sqlite_and_missing_id(self):
        client=FakeClient()
        with tempfile.TemporaryDirectory() as folder:
            result=await run_research('請讀 DEMO-TW-999',client=client, data_path=ROOT/'data/products.json',
                mcp_server=ROOT/'day1/company_database.py',output_dir=folder)
            self.assertEqual(result['tool_log'][0]['transport'],'mcp')
            self.assertEqual(result['tool_log'][0]['result']['status'],'not_found')
            self.assertEqual({t['name'] for t in client.requests[0]['tools']}, {'find_products_by_model','read_product_by_id'})
            self.assertTrue((Path(folder)/'products.sqlite').exists())

    async def test_true_mcp_preserves_null_and_market(self):
        with tempfile.TemporaryDirectory() as folder:
            result=await run_research(client=FakeClient(),data_path=ROOT/'data/products.json',
                mcp_server=ROOT/'day1/company_database.py',output_dir=folder)
            rows=result['tool_log'][0]['result']['products']
            self.assertEqual({p['market'] for p in rows},{'TW'})
            self.assertIsNone(result['tool_log'][2]['result']['product']['warranty_years'])

    async def test_six_model_calls_stop_incomplete_loop(self):
        client=FakeClient([response([tool('find_products_by_model',{'model':'DemoBook A','market':'TW'},n)]) for n in range(6)])
        with tempfile.TemporaryDirectory() as folder:
            result=await run_research(client=client,data_path=ROOT/'data/products.json',output_dir=folder)
            self.assertEqual(result['model_calls'],6)
            self.assertEqual(len(result['tool_log']),5)
            self.assertIn('尚未完成',result['report'])

    async def test_unknown_tool_is_error_instead_of_missing_data(self):
        client=FakeClient([response([tool('does_not_exist',{})]),response(text='工具不可用')])
        with tempfile.TemporaryDirectory() as folder:
            result=await run_research(client=client,data_path=ROOT/'data/products.json',output_dir=folder)
            self.assertEqual(result['tool_log'][0]['result']['status'],'error')

    def test_missing_product_and_market_are_not_substituted(self):
        products=json.loads((ROOT/'data/products.json').read_text())
        self.assertEqual(local_tool('read_product_by_id',{'product_id':'missing'},products)['status'],'not_found')
        self.assertEqual(local_tool('find_products_by_model',{'model':'Other','market':'TW'},products)['products'],[])


if __name__=='__main__':
    unittest.main()
