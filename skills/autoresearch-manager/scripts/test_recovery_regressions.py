"""Independent behavioral expectations; simulated drivers only, no API or training."""
import contextlib
import io
import json
import os
import sys
import time
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
SKILL = Path(os.environ.get('AUTORESEARCH_SKILL_ROOT', str(ROOT.parent))).resolve()
sys.path.insert(0, str(SKILL / 'scripts'))
import manager
from common import digest, read, write
from test_manager import ManagerTests

class ForwardTests(ManagerTests):
    def wait_exits(self, state):
        paths = [Path(j['directory']) / 'exit.json' for j in state['jobs'].values()]
        end = time.monotonic() + 5
        while not all(p.exists() for p in paths):
            if time.monotonic() > end:
                self.fail('simulated drivers did not exit')
            time.sleep(0.02)

    def set_phase(self, phase):
        self.make_run()
        state = read(self.run_dir / 'state.json')
        state['phase'] = phase
        if phase == 'qa':
            state['revision'] = 2  # fixture QA reports both PASS on this revision
            artifact = self.root / 'simulated.zip'
            import zipfile
            with zipfile.ZipFile(artifact, 'w') as z:
                z.writestr('SIMULATION.txt', 'NOT RESEARCH EVIDENCE')
            state['artifact'] = {'path': str(artifact), 'sha256': digest(artifact), 'revision': 2}
        manager.save(self.run_dir, state)

    def make_one_retry(self, phase, receipt_status):
        self.set_phase(phase)
        state = manager.tick(self.run_dir)
        self.wait_exits(state)
        bad = phase + '_b'
        receipt = Path(state['jobs'][bad]['directory']) / 'receipt.json'
        data = read(receipt)
        data['status'] = receipt_status
        write(receipt, data)
        return state, manager.tick(self.run_dir)

    def assert_retry_preserves_peer(self, phase):
        old, state = self.make_one_retry(phase, 'RETRY')
        good = phase + '_a'
        time.sleep(0.02)
        state = manager.tick(self.run_dir)
        self.wait_exits(state)
        self.assertIn(good, state['completed'], 'Successful concurrent lane was discarded on peer RETRY')
        self.assertNotIn(good, state['jobs'], 'Successful concurrent lane was dispatched again')
        self.assertEqual(state['completed'][good]['job_directory'], old['jobs'][good]['directory'])

    def test_dual_retry_preserves_successful_lane(self):
        self.assert_retry_preserves_peer('dual')

    def test_qa_retry_preserves_successful_lane(self):
        self.assert_retry_preserves_peer('qa')

    def assert_resume_preserves_peer(self, phase):
        old, state = self.make_one_retry(phase, 'NEEDS_INPUT')
        good = phase + '_a'
        self.assertEqual(state['status'], 'NEEDS_INPUT')
        with patch.object(sys, 'argv', ['manager.py', 'resume', '--run-dir', str(self.run_dir)]), patch.object(manager, 'detach'), contextlib.redirect_stdout(io.StringIO()):
            manager.main()
        state = manager.tick(self.run_dir)
        self.wait_exits(state)
        self.assertIn(good, state['completed'], 'Successful concurrent lane was discarded on resume')
        self.assertNotIn(good, state['jobs'], 'Successful concurrent lane was dispatched again after peer input')
        self.assertEqual(state['completed'][good]['job_directory'], old['jobs'][good]['directory'])

    def test_dual_resume_input_preserves_successful_lane(self):
        self.assert_resume_preserves_peer('dual')

    def test_qa_resume_input_preserves_successful_lane(self):
        self.assert_resume_preserves_peer('qa')

    def test_doctor_rejects_missing_python_driver_script(self):
        plan = self.plan()
        plan['drivers']['dual_b'] = [sys.executable, str(self.root / 'missing_driver.py')]
        with self.assertRaisesRegex(ValueError, 'driver'):
            manager.validate_plan(plan, self.run_dir)

    def test_preflight_rejects_same_model_disguised_with_version(self):
        plan = self.plan()
        plan['reviewers'][1] = dict(plan['reviewers'][0], version='other-alias')
        with self.assertRaisesRegex(ValueError, 'reviewer|model'):
            manager.validate_plan(plan, self.run_dir)

    def test_retry_does_not_hide_peer_failure(self):
        self.set_phase('dual')
        state = manager.tick(self.run_dir)
        self.wait_exits(state)
        for key, status in [('dual_a', 'RETRY'), ('dual_b', 'FAIL')]:
            path = Path(state['jobs'][key]['directory']) / 'receipt.json'
            row = read(path)
            row['status'] = status
            write(path, row)
        state = manager.tick(self.run_dir)
        self.assertEqual(state['phase'], 'repair')
        self.assertEqual(state['failures'][-1]['stage'], 'dual_b')

    def test_retained_peer_tampering_prevents_new_dispatch(self):
        _, state = self.make_one_retry('dual', 'RETRY')
        entry = state['completed']['dual_a']
        relative = next(iter(entry['evidence_sha256s']))
        (Path(entry['job_directory']) / relative).write_text('modified after success')
        before = len(list((self.run_dir / 'jobs').iterdir()))
        time.sleep(0.02)
        state = manager.tick(self.run_dir)
        self.assertEqual(state['phase'], 'repair')
        self.assertEqual(len(list((self.run_dir / 'jobs').iterdir())), before)

    def test_retained_qa_peer_completes_consensus_without_rerun(self):
        old, state = self.make_one_retry('qa', 'RETRY')
        final = self.until(lambda s: s['status'] == 'DONE')
        self.assertEqual(final['completed']['qa_a']['job_directory'], old['jobs']['qa_a']['directory'])
        requests = [read(p) for p in (self.run_dir / 'jobs').glob('*/request.json')]
        self.assertEqual(sum(r['stage'] == 'qa_a' for r in requests), 1)
        self.assertEqual(sum(r['stage'] == 'qa_b' for r in requests), 2)

    def test_retained_peer_from_other_revision_is_rejected(self):
        _, state = self.make_one_retry('dual', 'RETRY')
        state['completed']['dual_a']['revision'] -= 1
        manager.save(self.run_dir, state)
        time.sleep(0.02)
        self.assertEqual(manager.tick(self.run_dir)['phase'], 'repair')

if __name__ == '__main__':
    # Only run new tests; inherited suite is run separately.
    names = [n for n in ForwardTests.__dict__ if n.startswith('test_')]
    suite = unittest.TestSuite(ForwardTests(n) for n in names)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())
