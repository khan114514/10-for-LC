#!/usr/bin/env python3
"""Check release inventory, hashes, task records and the unchanged pinned QA release."""
import hashlib
import json
import re
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'manifests/files.json'


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def visible_files():
    return {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
            if p.is_file() and not ({'.git', '__pycache__'} & set(p.relative_to(ROOT).parts))
            and p.name != '.DS_Store' and p.suffix not in ('.pyc', '.pyo')}


def safe(relative):
    path = PurePosixPath(relative)
    if path.is_absolute() or '..' in path.parts or not path.parts:
        raise ValueError('invalid manifest path')
    target = ROOT / relative
    if any(p.is_symlink() for p in [target, *target.parents] if p != ROOT.parent):
        raise ValueError('symlink is not a release file')
    return target


def main():
    manifest = json.loads((ROOT / MANIFEST).read_text())
    failures = []
    for relative, expected in manifest['files'].items():
        try:
            path = safe(relative)
            if not path.is_file() or sha256(path) != expected['sha256'] or path.stat().st_size != expected['bytes']:
                failures.append({'path': relative, 'reason': 'missing or content mismatch'})
        except (ValueError, OSError):
            failures.append({'path': relative, 'reason': 'unsafe or unreadable path'})
    actual = visible_files() - {MANIFEST}
    if actual != set(manifest['files']):
        failures.append({'reason': 'inventory mismatch', 'unexpected': sorted(actual - set(manifest['files'])),
                         'missing': sorted(set(manifest['files']) - actual)})
    manager = ROOT / 'skills/autoresearch-manager'
    release = json.loads((manager / 'assets/qa-release.json').read_text())
    for relative, expected in release['files'].items():
        path = manager / 'assets/qa-skills' / relative
        if not path.is_file() or sha256(path) != expected:
            failures.append({'path': 'skills/autoresearch-manager/assets/qa-skills/' + relative,
                             'reason': 'original QA source mismatch'})
    tasks = json.loads((ROOT / 'manifests/tasks.json').read_text())['tasks']
    ids = {t['id'] for t in tasks}
    if len(tasks) != 10 or len(ids) != 10:
        failures.append({'reason': 'expected ten distinct task IDs'})
    dedup = {r['id']: r for r in json.loads((ROOT / 'reports/selection/dedup.json').read_text())['rows']}
    sources = {r['id']: r for r in json.loads((ROOT / 'manifests/sources.json').read_text())['sources']}
    for task in tasks:
        key = task['id']
        if (task['status'] != 'PREPARATION_ONLY' or task['gpu_reproduction_verified']
                or not re.fullmatch(r'[0-9a-f]{40}', task['commit'])
                or not safe(task['card']).is_file()
                or sources.get(key, {}).get('commit') != task['commit']
                or dedup.get(key, {}).get('dedup') != 'pass'):
            failures.append({'id': key, 'reason': 'task handoff consistency failure'})
        report = json.loads(safe(task['difficulty_evidence']).read_text())
        if report['final_level'] != '困难' or report['status'] != 'PROVISIONAL_NOT_GPU_VALIDATED':
            failures.append({'id': key, 'reason': 'missing provisional hard rating'})
    print(json.dumps({'status': 'FAIL' if failures else 'PASS', 'handoff_files': len(manifest['files']),
                      'tasks': len(tasks), 'qa_files': len(release['files']),
                      'qa_version': release['release']['version'], 'failures': failures},
                     ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
