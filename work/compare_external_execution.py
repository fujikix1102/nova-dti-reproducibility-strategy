#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path

def sha256(path):
    if not path.is_file(): return None
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''): h.update(block)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('manifest', type=Path)
    ap.add_argument('--external-dir', type=Path, required=True)
    ap.add_argument('--external-log', type=Path, required=True)
    ap.add_argument('--external-manifest', type=Path)
    ap.add_argument('--report', type=Path)
    a = ap.parse_args()
    frozen = json.loads(a.manifest.read_text())
    result = {'status': 'FAIL', 'formal_pass': False, 'checks': {}, 'notes': []}
    inputs = {
        'jma': a.external_dir / 'independent_events_jma_expanded/jma_independent_events_12station_daily_v2.csv',
        'gpm': a.external_dir / 'independent_events_gpm_station_extract_expanded/gpm_independent_events_11station_30min_complete.csv',
    }
    for name, path in inputs.items():
        actual = sha256(path); expected = frozen['input_sha256'][name]
        result['checks']['input:' + name] = {'expected': expected, 'actual': actual, 'pass': actual == expected}
    out = a.external_dir / 'independent_events_comparison_expanded/jma_gpm_daily_v2_event_bootstrap.json'
    actual = sha256(out); expected = frozen['determinism_check']['bootstrap_output_sha256_run_1']
    result['checks']['output:bootstrap'] = {'expected': expected, 'actual': actual, 'pass': actual == expected}
    try:
        log = json.loads(a.external_log.read_text())
        result['checks']['log:completed'] = {'pass': log.get('status', '').startswith('COMPLETED_WITH_')}
        result['checks']['log:formal_pass_false'] = {'pass': log.get('formal_pass_expected') is False}
        result['environment'] = {k: log.get(k) for k in ('python', 'platform', 'code_dir', 'base_dir')}
    except (OSError, json.JSONDecodeError):
        result['checks']['log:completed'] = {'pass': False}
    if a.external_manifest:
        try:
            ext = json.loads(a.external_manifest.read_text())
            result['checks']['external_manifest_case_id'] = {'pass': ext.get('case_id') == frozen.get('case_id')}
        except (OSError, json.JSONDecodeError):
            result['checks']['external_manifest_case_id'] = {'pass': False}
    else:
        result['notes'].append('No external manifest supplied; independent reproduction is not established.')
    result['status'] = 'PASS' if all(v.get('pass', False) for v in result['checks'].values()) else 'FAIL'
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'; print(text, end='')
    if a.report: a.report.write_text(text)
    return 0 if result['status'] == 'PASS' else 1

if __name__ == '__main__': raise SystemExit(main())
