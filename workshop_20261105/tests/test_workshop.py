import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from workshop.catalog import seed, find_products, read_product
from workshop.flows import (basic_report, retrieve, research, ledger, detect, snapshot,
                            approval, digest, new_product)


class ClassroomAcceptance(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def count(self, filename):
        path=self.path/filename
        if not path.exists():
            return 0
        with sqlite3.connect(path) as db:
            return db.execute('SELECT COUNT(*) FROM operations').fetchone()[0]

    def event(self):
        return detect(snapshot(40000,source_id='SIM-W1',date='2026-10-26'),snapshot())

    def decision(self, state, action, **extra):
        return dict(action=action,hash=digest(state['draft']),**extra)

    def test_configuration_and_missing_warranty(self):
        result=basic_report()
        self.assertEqual([r['id'] for r in result['comparison']],['DEMO-TW-016','DEMO-TW-032'])
        self.assertEqual(result['comparison'][1]['warranty'],'待確認')

    def test_sqlite_tools_reject_injection_and_unknown_id(self):
        db=seed(self.path/'catalog.sqlite')
        self.assertEqual(len(find_products(db,'DemoBook A','TW')),2)
        self.assertEqual(find_products(db,"' OR 1=1 --",'TW'),[])
        self.assertEqual(read_product(db,'unknown')['status'],'not_found')

    def test_metadata_filter_excludes_old_and_other_market(self):
        rows=retrieve(k=10)
        self.assertTrue(rows)
        self.assertTrue(all(r['current'] and r['market']=='TW' for r in rows))
        self.assertIn('P-TW#2',[r['id'] for r in rows])

    def test_bounded_research_preserves_service_gap(self):
        result=research(max_rounds=2)
        self.assertEqual(result['round'],3)  # 初查一次＋補查最多兩次
        self.assertEqual(result['matrix'][0]['status'],'符合')
        self.assertEqual(result['matrix'][1]['status'],'待確認')
        self.assertIn('上限',result['stop_reason'])

    def test_recovery_across_processes(self):
        args=[sys.executable,'-m','workshop.cli']
        crashed=subprocess.run(args+['recover-start','--out',str(self.path)],capture_output=True,text=True)
        self.assertNotEqual(crashed.returncode,0)
        self.assertIn('DEMO_CRASH_AFTER_ASUS_WRITE',crashed.stderr)
        state=json.loads((self.path/'state.json').read_text())
        self.assertEqual(set(state['values']['results']),{'Dell','Lenovo'})
        self.assertEqual(state['next'],['ASUS'])
        done=subprocess.run(args+['recover-resume','--out',str(self.path)],capture_output=True,text=True)
        self.assertEqual(done.returncode,0,done.stderr)
        nodes=[json.loads(line)['node'] for line in (self.path/'execution.jsonl').read_text().splitlines()]
        self.assertEqual(nodes,['Dell','Lenovo','ASUS','ASUS'])
        self.assertEqual(self.count('operations.sqlite'),3)
        self.assertTrue((self.path/'report.md').exists())

    def test_mcp_protocol_discovery_and_tool_calls(self):
        from workshop.mcp_client import run
        result=run(seed(self.path/'catalog.sqlite'))
        self.assertEqual(set(result['tools']),{'find_products_by_model','read_product_by_id'})
        self.assertEqual(len(result['results'][0]['products']),2)
        self.assertIsNone(result['results'][1]['product']['warranty_years'])

    def test_same_operation_different_payload_is_rejected(self):
        ledger(self.path/'ops.sqlite','x',{'value':1})
        with self.assertRaises(ValueError):
            ledger(self.path/'ops.sqlite','x',{'value':2})

    def test_no_change_is_not_data_error(self):
        self.assertEqual(detect(snapshot(),snapshot())['status'],'no_major_change')
        self.assertEqual(detect(snapshot(),snapshot(None))['status'],'data_error')
        with self.assertRaises(ValueError):
            approval(self.path,detect(snapshot(),snapshot(None)))

    def test_sku_currency_tax_alignment(self):
        for update in [dict(sku='OTHER'),dict(currency='USD'),dict(tax='excluded'),dict(market='US')]:
            self.assertEqual(detect(snapshot(),snapshot(**update))['status'],'not_comparable')

    def test_price_change_boundary(self):
        self.assertEqual(detect(snapshot(40000),snapshot(36000))['status'],'pending_review')
        self.assertEqual(detect(snapshot(40000),snapshot(36001))['status'],'no_major_change')
        self.assertAlmostEqual(self.event()['percent'],-15)

    def test_new_product_requires_release_evidence(self):
        self.assertEqual(new_product({'sku':'NEW'})['status'],'data_error')
        self.assertEqual(new_product(dict(sku='NEW',market='TW',source_id='SIM-RELEASE',release_date='2026-11-02'))['status'],'pending_review')

    def test_new_product_approval_and_delivery(self):
        event=new_product(dict(sku='NEW',market='TW',source_id='SIM-RELEASE',release_date='2026-11-02'))
        s=approval(self.path,event)
        self.assertEqual(self.count('outbox.sqlite'),0)
        s=approval(self.path,event,self.decision(s,'approve'))
        self.assertEqual(self.count('outbox.sqlite'),1)
        self.assertIn('新品',s['delivery']['receipt']['text'])

    def test_same_event_in_new_thread_reuses_delivery(self):
        s=approval(self.path,self.event())
        approval(self.path,self.event(),self.decision(s,'approve'))
        s=approval(self.path,self.event(),thread='retrigger')
        s=approval(self.path,self.event(),self.decision(s,'approve'),thread='retrigger')
        self.assertTrue(s['delivery']['reused'])
        self.assertEqual(self.count('outbox.sqlite'),1)

    def test_approve_once_and_duplicate_decision(self):
        s=approval(self.path,self.event())
        self.assertEqual(self.count('outbox.sqlite'),0)
        d=self.decision(s,'approve')
        s=approval(self.path,self.event(),d)
        self.assertEqual(self.count('outbox.sqlite'),1)
        with self.assertRaises(ValueError):
            approval(self.path,self.event(),d)
        self.assertEqual(self.count('outbox.sqlite'),1)

    def test_revise_requires_new_approval(self):
        s=approval(self.path,self.event())
        stale=self.decision(s,'approve')
        s=approval(self.path,self.event(),self.decision(s,'revise',text='v2：保留促銷條件待確認'))
        self.assertEqual(s['draft']['version'],2)
        self.assertEqual(self.count('outbox.sqlite'),0)
        with self.assertRaises(ValueError):
            approval(self.path,self.event(),stale)
        s=approval(self.path,self.event(),self.decision(s,'approve'))
        self.assertEqual(s['delivery']['receipt']['version'],2)

    def test_reject_does_not_send(self):
        s=approval(self.path,self.event())
        approval(self.path,self.event(),self.decision(s,'reject'))
        self.assertEqual(self.count('outbox.sqlite'),0)

    def test_crash_before_and_after_delivery(self):
        for position in ['before','after']:
            with self.subTest(position=position):
                p=self.path/position
                s=approval(p,self.event())
                with self.assertRaises(RuntimeError):
                    approval(p,self.event(),self.decision(s,'approve'),crash=position)
                s=approval(p,self.event())
                with sqlite3.connect(p/'outbox.sqlite') as db:
                    self.assertEqual(db.execute('SELECT COUNT(*) FROM operations').fetchone()[0],1)
                self.assertEqual(s['delivery']['reused'],position=='after')


if __name__=='__main__':
    unittest.main()
