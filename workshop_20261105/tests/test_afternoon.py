"""驗證比較條件、失敗基準保護及反覆操作的實際SQLite結果。"""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'day2'))
import afternoon as lab

class AfternoonTests(unittest.TestCase):
    def test_routes_and_comparability(self):
        weeks=lab.teaching_weeks()
        self.assertEqual([r['route'] for r in weeks['comparisons']],
            ['重大變化待審','無重大變化','不可直接比較','資料不足'])
        self.assertEqual(weeks['comparisons'][0]['change_pct'],-15)
        old=weeks['first']
        for field,value in [('market','US'),('currency','USD'),('tax','未稅'),('configuration','16GB'),('simulation',False)]:
            self.assertEqual(lab.compare_quotes(old,dict(old,**{field:value}))['route'],'不可直接比較')
        self.assertEqual(lab.teaching_weeks(39000)['comparisons'][0]['route'],'無重大變化')
        self.assertEqual(lab.teaching_weeks(36000)['comparisons'][0]['route'],'重大變化待審')

    def test_invalid_prices_and_threshold(self):
        old=lab.teaching_weeks()['first']
        for value in (None,True,0,-1,float('nan'),float('inf'),'34000'):
            self.assertEqual(lab.compare_quotes(old,dict(old,price=value))['route'],'資料不足')
        for value in (0,True,-10,float('nan'),float('inf')):
            with self.assertRaises(ValueError): lab.teaching_weeks(threshold=value)

    def test_snapshot_failure_and_change_keep_baseline(self):
        with tempfile.TemporaryDirectory() as out:
            good=dict(status='ok',source_id='LEN-PSREF',url='https://example.invalid/spec.pdf',sha256='old',fetched_at='first')
            self.assertEqual(lab.monitor_once(out,lambda:good)['status'],'baseline_created')
            baseline=Path(out,'baseline.json').read_bytes()
            self.assertEqual(lab.monitor_once(out,lambda:dict(good,status='data_error'))['status'],'data_error')
            self.assertEqual(Path(out,'baseline.json').read_bytes(),baseline)
            self.assertEqual(lab.monitor_once(out,lambda:dict(good,sha256='new'))['status'],'content_changed_needs_review')
            self.assertEqual(Path(out,'baseline.json').read_bytes(),baseline)
            self.assertEqual(len(Path(out,'history.jsonl').read_text().splitlines()),3)

    def test_review_repeat_wait_revise_and_branches(self):
        with tempfile.TemporaryDirectory() as out:
            draft={'recipient':'supplier@example.invalid','subject':'詢價','body':'原稿','comparison_attachment':lab.teaching_weeks()}
            state=lab.case.approval(out,draft=draft)
            self.assertTrue(lab.decide_once(out,'wait','')['pending'])
            with self.assertRaises(ValueError): lab.decide_once(out,'approve',' ')
            revised=lab.revise_once(out,'請附交期')
            self.assertNotEqual(state['hash'],revised['hash'])
            self.assertEqual(lab.revise_once(out,'請附交期')['hash'],revised['hash'])
            with self.assertRaisesRegex(ValueError,'草稿已更動'):
                lab.case.approval(out,decision={'action':'approve','hash':state['hash']})
            approved=lab.decide_once(out,'approve','核對完成')
            self.assertEqual(approved['outbox_count'],1)
            self.assertEqual(lab.decide_once(out,'reject','不能改既有決定')['outbox_count'],1)
            self.assertEqual(lab.revise_once(out,'已結束不覆寫')['hash'],approved['hash'])
            self.assertEqual(json.loads(Path(out,'decision.json').read_text())['action'],'approve')
            for _ in range(2):
                rows=lab.exercise_branches(Path(out)/'branches',draft)
                self.assertEqual([r['outbox_count'] for r in rows],[1,1,0])
            self.assertEqual(lab.case.approval(out)['hash'],approved['hash'])
            changed=copy.deepcopy(draft); changed['comparison_attachment']['second']['price']=35000
            self.assertNotEqual(lab.case.digest(draft),lab.case.digest(changed))
