#!/usr/bin/env python3
"""Fetch a pinned official repository into a new author-only directory; never execute it."""
import argparse
import json
import re
import subprocess
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    rows = json.loads((root / 'manifests/sources.json').read_text())['sources']
    by_id = {row['id']: row for row in rows}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('task_id', choices=sorted(by_id))
    parser.add_argument('--dest', required=True, type=Path)
    args = parser.parse_args()
    dest = args.dest
    if not dest.is_absolute() or dest.is_symlink():
        parser.error('--dest must be an absolute, non-symlink directory')
    if dest.exists() and (not dest.is_dir() or any(dest.iterdir())):
        parser.error('--dest must be new or empty; existing work will not be overwritten')
    row = by_id[args.task_id]
    if not re.fullmatch(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', row['repo']):
        parser.error('unsupported source URL')
    if not re.fullmatch(r'[0-9a-f]{40}', row['commit']):
        parser.error('invalid pinned commit')
    dest.mkdir(parents=True, exist_ok=True)
    # All arguments remain separate argv values. Disable checkout hooks explicitly.
    def git(*argv):
        return subprocess.check_output(['git', '-c', 'core.hooksPath=/dev/null', *argv], cwd=dest, text=True).strip()
    git('init')
    git('config', 'core.hooksPath', '/dev/null')
    git('remote', 'add', 'origin', row['repo'] + '.git')
    git('fetch', '--depth=1', 'origin', row['commit'])
    git('checkout', '--detach', row['commit'])
    actual = git('rev-parse', 'HEAD')
    if actual != row['commit']:
        raise RuntimeError('checkout does not match pinned commit')
    print(json.dumps({'id': args.task_id, 'commit': actual,
                      'source_checkout': 'VERIFIED', 'training': 'NOT_RUN',
                      'datasets': 'NOT_VALIDATED', 'license_status': row['license_status']},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
