"""Isolated recovery tests; fixtures only, no model APIs or real research."""
import contextlib, io, os, sys, time, unittest
from pathlib import Path
from unittest.mock import patch
ROOT = Path(__file__).resolve().parent
SKILL = Path(os.environ.get('AUTORESEARCH_SKILL_ROOT', str(ROOT.parent)))
sys.path.insert(0, str(SKILL/'scripts'))
import manager
from common import read, write, object_digest
from test_recovery_regressions import ForwardTests

class AdversarialTests(ForwardTests):
    def resume(self):
        with patch.object(sys,'argv',['manager.py','resume','--run-dir',str(self.run_dir)]), patch.object(manager,'detach'), contextlib.redirect_stdout(io.StringIO()):
            manager.main()
        return read(self.run_dir/'state.json')

    def slow_lane(self, receipt_status='RETRY'):
        self.set_phase('dual')
        plan=read(self.run_dir/'plan.json')
        plan['drivers']['dual_b'][-1]='0.6'
        write(self.run_dir/'plan.json',plan)
        state=read(self.run_dir/'state.json')
        state['plan_sha256']=object_digest(plan)
        manager.save(self.run_dir,state)
        state=manager.tick(self.run_dir)
        a=Path(state['jobs']['dual_a']['directory'])
        end=time.monotonic()+5
        while not (a/'exit.json').exists():
            if time.monotonic()>end: self.fail('fixture did not exit')
            time.sleep(.01)
        r=read(a/'receipt.json');r['status']=receipt_status;write(a/'receipt.json',r)
        self.assertFalse((Path(state['jobs']['dual_b']['directory'])/'exit.json').exists())
        return state

    def test_inflight_peer_is_not_orphaned_by_input(self):
        old=self.slow_lane('NEEDS_INPUT')
        state=manager.tick(self.run_dir)
        self.assertEqual(state['status'],'RUNNING')
        self.assertEqual(state['jobs'],old['jobs'])
        self.wait_exits(state)
        state=manager.tick(self.run_dir)
        self.assertEqual(state['status'],'NEEDS_INPUT')
        self.assertEqual(state['completed']['dual_b']['job_directory'],old['jobs']['dual_b']['directory'])
        state=self.resume()
        state=manager.tick(self.run_dir)
        self.wait_exits(state)
        self.assertNotIn('dual_b',state['jobs'])
        self.assertIn('dual_b',state['completed'])

    def test_task_change_waits_for_running_peer_before_repair(self):
        old=self.slow_lane('PASS')
        (self.task/'task.txt').write_text('changed frozen task')
        state=manager.tick(self.run_dir)
        self.assertEqual(state['jobs'],old['jobs'])
        self.assertEqual(state['phase'],'dual')
        self.wait_exits(state)
        state=manager.tick(self.run_dir)
        self.assertEqual(state['phase'],'repair')
        self.assertTrue(all((Path(j['directory'])/'exit.json').exists() for j in old['jobs'].values()))

    def test_retained_evidence_change_waits_for_running_retry(self):
        old,state=self.make_one_retry('dual','RETRY')
        time.sleep(.02)
        state=manager.tick(self.run_dir)
        b=state['jobs']['dual_b']
        entry=state['completed']['dual_a']
        (Path(entry['job_directory'])/'duration.json').write_text('{"changed":true}')
        if not (Path(b['directory'])/'exit.json').exists():
            fresh=manager.tick(self.run_dir)
            self.assertEqual(fresh['jobs']['dual_b']['id'],b['id'])
        self.wait_exits(state)
        state=manager.tick(self.run_dir)
        self.assertEqual(state['phase'],'repair')
        self.assertEqual(state['failures'][-1]['error_type'],'PriorEvidenceChanged')

    def test_failure_precedes_retry_in_either_lane(self):
        for phase in ('dual','qa'):
            for failed in ('a','b'):
                with self.subTest(phase=phase,failed=failed):
                    # each combination gets its own independent temporary run
                    self.setUp()
                    self.set_phase(phase)
                    state=manager.tick(self.run_dir);self.wait_exits(state)
                    for lane in ('a','b'):
                        p=Path(state['jobs'][phase+'_'+lane]['directory'])/'receipt.json'
                        r=read(p);r['status']='FAIL' if lane==failed else 'RETRY';write(p,r)
                    state=manager.tick(self.run_dir)
                    self.assertEqual(state['phase'],'repair')
                    self.assertEqual(state['failures'][-1]['stage'],phase+'_'+failed)

    def test_restored_frozen_plan_reuses_finished_jobs(self):
        self.set_phase('dual')
        state=manager.tick(self.run_dir);self.wait_exits(state)
        original=read(self.run_dir/'plan.json')
        changed=dict(original, goal='accidental edit while jobs were running')
        write(self.run_dir/'plan.json',changed)
        blocked=manager.tick(self.run_dir)
        self.assertEqual(blocked['status'],'NEEDS_INPUT')
        write(self.run_dir/'plan.json',original)
        resumed=self.resume()
        final=manager.tick(self.run_dir)
        self.wait_exits(final)  # let any incorrectly restarted fixtures exit before cleanup
        self.assertEqual(len(list((self.run_dir/'jobs').iterdir())),2, 'Restoring a frozen plan dispatched completed lanes again')
        self.assertEqual(final['phase'],'finalize')
        for stage in ('dual_a','dual_b'):
            self.assertEqual(final['completed'][stage]['job_directory'],state['jobs'][stage]['directory'])

if __name__=='__main__':
    suite=unittest.TestSuite(AdversarialTests(n) for n in AdversarialTests.__dict__ if n.startswith('test_'))
    r=unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not r.wasSuccessful())
