"""第二天的重要邊界：引用、跨程序資料身分、去重、人工審核、監測失敗。"""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('procurement',Path(__file__).resolve().parents[1]/'day2/procurement.py')
case=importlib.util.module_from_spec(spec);spec.loader.exec_module(case)


def answer(self,role,prompt,rows):
    self.log.append({'role':role,'evidence_ids':[r['id'] for r in rows]})
    return f"{role}：待確認台灣 SKU、報價與到府權益。 [{rows[0]['id']}]"


class Day2(unittest.TestCase):
    def test_corpus_scope_and_citation(self):
        self.assertEqual(len(case.corpus()),29)
        self.assertEqual(sum(case.eligible(r) for r in case.corpus()),27)
        self.assertEqual(len(case.coverage()),27)
        rows=case.retrieve('Lenovo 台灣到府三年',10,brand='Lenovo')
        self.assertTrue(all(case.eligible(r,'Lenovo') for r in rows))
        self.assertNotIn('desktop_only',[r['scope'] for r in rows])
        self.assertEqual(case.citation_check('[LEN-99]',rows)['status'],'needs_review')
        self.assertEqual(case.citation_check('沒有引用',rows)['status'],'needs_review')

    @patch.object(case.Model,'ask',answer)
    def test_real_graph_routes_and_bounded_revision(self):
        with tempfile.TemporaryDirectory() as d:
            result=case.run_team('120台台灣詢價','qa',max_revisions=1,out=d)
            log=json.loads(Path(d,'trace.json').read_text())['model_calls']
            self.assertEqual([r['role'] for r in log],['Planner','Researcher-HP','Researcher-Lenovo','Researcher-Dell','Writer','Reviewer','Writer','Reviewer'])
            self.assertEqual(result['revisions'],1)
            self.assertEqual(len(result['coverage']),27)

    @patch.object(case.Model,'ask',answer)
    def test_checkpoint_effect_gap_and_identity(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(RuntimeError,'LESSON_PAUSE'):
                case.run_batch(d,'qa')
            paused=case.inspect_batch(d)
            self.assertEqual(paused['completed_brands'],['HP'])
            self.assertEqual(paused['next'],['Lenovo'])
            self.assertEqual(paused['effects'],{'HP':1,'Lenovo':1})
            with self.assertRaisesRegex(ValueError,'無法恢復'):
                case.run_batch(d,'qa',model='other',resume=True,crash=False)
            resumed=case.run_batch(d,'qa',resume=True,crash=False)
            self.assertEqual(resumed['next'],[])
            self.assertEqual([e['brand'] for e in resumed['execution']],['HP','Lenovo','Lenovo','Dell'])
            self.assertTrue(resumed['execution'][2]['reused'])
            self.assertEqual(sum(resumed['effects'].values()),3)
            # 完成後再次 resume 不新增節點或效果。
            self.assertEqual(case.run_batch(d,'qa',resume=True,crash=False)['execution'],resumed['execution'])

    def test_revision_stale_hash_approval_and_duplicate(self):
        with tempfile.TemporaryDirectory() as d:
            draft={'recipient':'test@example.invalid','body':'草稿','action':'archive_local_draft','case_hash':'a'}
            first=case.approval(d,draft)
            self.assertTrue(first['pending']);self.assertEqual(first['outbox_count'],0)
            newer=case.approval(d,decision={'action':'revise','hash':first['hash'],'text':'保留未知與來源的新草稿'})
            with self.assertRaisesRegex(ValueError,'舊 hash'):
                case.approval(d,decision={'action':'approve','hash':first['hash']})
            approved=case.approval(d,decision={'action':'approve','hash':newer['hash']})
            self.assertFalse(approved['pending']);self.assertEqual(approved['outbox_count'],1)
            self.assertEqual(approved['sent_count'],0)
            with self.assertRaises(ValueError):case.approval(d,decision={'action':'approve','hash':newer['hash']})
            self.assertEqual(case.approval(d)['outbox_count'],1)

    def test_reject_and_content_change_are_separate(self):
        with tempfile.TemporaryDirectory() as d:
            state=case.approval(d,{'body':'草稿','recipient':'test@example.invalid'})
            result=case.approval(d,decision={'action':'reject','hash':state['hash']})
            self.assertEqual(result['outbox_count'],0)
            self.assertFalse(result['pending'])
        old={'status':'ok','source_id':'LEN-PSREF','url':'https://example.invalid/spec.pdf','sha256':'a'}
        self.assertEqual(case.compare_snapshots(old,dict(old)),'unchanged')
        self.assertEqual(case.compare_snapshots(old,dict(old,sha256='b')),'content_changed_needs_review')
        self.assertEqual(case.compare_snapshots(old,dict(old,status='data_error')),'data_error')
        self.assertEqual(case.compare_snapshots(old,dict(old,source_id='another')),'not_comparable')

class Restore(unittest.TestCase):
    @patch.object(case.Model,'ask',answer)
    def test_restore_paused_zip_in_new_directory(self):
        import shutil
        with tempfile.TemporaryDirectory() as d:
            original=Path(d)/'original'
            with self.assertRaisesRegex(RuntimeError,'LESSON_PAUSE'):
                case.run_batch(original,'qa')
            archive=shutil.make_archive(str(Path(d)/'paused'),'zip',original)
            restored=Path(d)/'restored'
            case.restore_archive(archive,restored)
            result=case.run_batch(restored,'qa',resume=True,crash=False)
            self.assertEqual(result['effects'],{'HP':1,'Lenovo':1,'Dell':1})
            self.assertTrue(result['execution'][2]['reused'])
            with self.assertRaisesRegex(ValueError,'已有資料'):
                case.restore_archive(archive,restored)

class ModelCache(unittest.TestCase):
    def test_cache_reuses_only_identical_role_prompt_model_and_evidence(self):
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory() as d, patch.object(case,'OpenAI') as sdk:
            sdk.return_value.responses.create.return_value=SimpleNamespace(output_text='待確認 [LEN-01]',status='completed',id='qa-response',usage=None)
            llm=case.Model('qa',cache_dir=d)
            rows=case.retrieve('Lenovo',1,brand='Lenovo')
            llm.ask('Researcher','同一任務',rows)
            llm.ask('Researcher','同一任務',rows)
            self.assertEqual(sdk.return_value.responses.create.call_count,1)
            self.assertTrue(llm.log[-1]['used_cache'])
            changed=[dict(rows[0],text='來源已更新，需重新判讀')]
            llm.ask('Researcher','同一任務',changed)
            self.assertEqual(sdk.return_value.responses.create.call_count,2)
            self.assertFalse(llm.log[-1]['used_cache'])


if __name__=='__main__':unittest.main()
