#!/usr/bin/env python3
"""Fail if a proposed public release contains excluded input or credential files."""
from pathlib import Path
import argparse, json

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root', type=Path)
    args = ap.parse_args()
    excluded = []
    for p in args.root.rglob('*'):
        if not p.is_file(): continue
        name = p.name.lower()
        if name.endswith('.csv') or any(x in name for x in ('token', 'cookie', 'credential', 'secret')):
            excluded.append(str(p.relative_to(args.root)))
    result = {'status': 'PASS' if not excluded else 'FAIL', 'excluded_files_found': excluded}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not excluded else 1

if __name__ == '__main__': raise SystemExit(main())
