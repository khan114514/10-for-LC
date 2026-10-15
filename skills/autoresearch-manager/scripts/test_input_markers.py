"""Final input-marker checks; isolated fixtures, no model APIs or live systems."""
import os, sys, unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parent
SKILL=Path(os.environ.get('AUTORESEARCH_SKILL_ROOT',str(ROOT.parent)))
sys.path.insert(0,str(SKILL/'scripts'))
import manager
from common import read, write
from test_adversarial_recovery import AdversarialTests

class InputMarkerTests(AdversarialTests):
    def count_stage(self,stage):
        return sum(read(p)['stage']==stage for p in (self.run_dir/'jobs').glob('*/request.json'))

    def test_legacy_input_state_reuses_successful_peer(self):
        old,state=self.make_one_retry('dual','NEEDS_INPUT')
        state.pop('input_jobs',None)
        manager.save(self.run_dir,state)
        self.resume()
        state=manager.tick(self.run_dir);self.wait_exits(state)
        state=manager.tick(self.run_dir)
        self.assertEqual(state['phase'],'finalize')
        self.assertEqual(self.count_stage('dual_a'),1)
        self.assertEqual(self.count_stage('dual_b'),2)
        self.assertEqual(state['completed']['dual_a']['job_directory'],old['jobs']['dual_a']['directory'])

    def test_both_input_jobs_get_exactly_one_new_attempt(self):
        self.set_phase('dual')
        state=manager.tick(self.run_dir);self.wait_exits(state)
        for stage in ('dual_a','dual_b'):
            p=Path(state['jobs'][stage]['directory'])/'receipt.json'
            r=read(p);r['status']='NEEDS_INPUT';write(p,r)
        state=manager.tick(self.run_dir)
        self.assertEqual(set(state['input_jobs']),{'dual_a','dual_b'})
        resumed=self.resume()
        self.assertNotIn('input_jobs',resumed)
        state=manager.tick(self.run_dir);self.wait_exits(state)
        state=manager.tick(self.run_dir)
        self.assertEqual(state['phase'],'finalize')
        self.assertEqual(self.count_stage('dual_a'),2)
        self.assertEqual(self.count_stage('dual_b'),2)

    def test_restored_qa_assets_collect_finished_jobs(self):
        self.set_phase('dual')
        old=manager.tick(self.run_dir);self.wait_exits(old)
        with patch.object(manager,'verify_assets',side_effect=ValueError('SIMULATED MISSING ASSET')):
            state=manager.tick(self.run_dir)
        self.assertEqual(state['status'],'NEEDS_INPUT')
        self.resume()
        state=manager.tick(self.run_dir)
        self.assertEqual(state['phase'],'finalize')
        self.assertEqual(self.count_stage('dual_a'),1)
        self.assertEqual(self.count_stage('dual_b'),1)
        for stage in ('dual_a','dual_b'):
            self.assertEqual(state['completed'][stage]['job_directory'],old['jobs'][stage]['directory'])

    def test_input_and_retry_recover_without_stale_marker(self):
        self.set_phase('dual')
        state=manager.tick(self.run_dir);self.wait_exits(state)
        for stage,status in (('dual_a','NEEDS_INPUT'),('dual_b','RETRY')):
            p=Path(state['jobs'][stage]['directory'])/'receipt.json'
            r=read(p);r['status']=status;write(p,r)
        state=manager.tick(self.run_dir)
        self.assertEqual(state['input_jobs'],['dual_a'])
        resumed=self.resume()
        self.assertNotIn('input_jobs',resumed)
        state=manager.tick(self.run_dir);self.wait_exits(state)
        state=manager.tick(self.run_dir)
        self.assertEqual(state['phase'],'finalize')
        self.assertEqual(self.count_stage('dual_a'),2)
        self.assertEqual(self.count_stage('dual_b'),2)

if __name__=='__main__':
    suite=unittest.TestSuite(InputMarkerTests(n) for n in InputMarkerTests.__dict__ if n.startswith('test_'))
    r=unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not r.wasSuccessful())
