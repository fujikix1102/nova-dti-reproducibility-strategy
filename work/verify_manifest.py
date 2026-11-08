#!/usr/bin/env python3
"""Verify a JMA–GPM seeded reproduction against its frozen manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def check_file(result: dict, label: str, path: Path, expected: str) -> None:
    actual = digest(path) if path.is_file() else None
    result["checks"][label] = {"path": str(path), "expected": expected, "actual": actual, "pass": actual == expected}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--code-dir", type=Path, required=True)
    ap.add_argument("--base-dir", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--log", type=Path, action="append", default=[])
    args = ap.parse_args()
    m = json.loads(args.manifest.read_text())
    result = {"case_id": m["case_id"], "checks": {}, "formal_pass": False}

    code_names = {
        "recompute_jma_gpm_v2.py": "recompute_jma_gpm_v2.py",
        "bootstrap_v2_seeded.py": "bootstrap_v2.py",
        "downstream_v2.py": "downstream_v2.py",
    }
    for manifest_name, actual_name in code_names.items():
        check_file(result, f"code:{manifest_name}", args.code_dir / actual_name, m["code_sha256"][manifest_name])

    inputs = {
        "jma": args.base_dir / "independent_events_jma_expanded/jma_independent_events_12station_daily_v2.csv",
        "gpm": args.base_dir / "independent_events_gpm_station_extract_expanded/gpm_independent_events_11station_30min_complete.csv",
    }
    for name, path in inputs.items():
        check_file(result, f"input:{name}", path, m["input_sha256"][name])

    expected_bootstrap = m["determinism_check"]["bootstrap_output_sha256_run_1"]
    check_file(result, "output:bootstrap", args.output_dir / "jma_gpm_daily_v2_event_bootstrap.json", expected_bootstrap)

    audit_path = args.output_dir / "jma_gpm_daily_v2_audit.json"
    downstream_path = args.output_dir / "jma_gpm_daily_v2_downstream_audit.json"
    csv_path = args.output_dir / "jma_gpm_daily_jst_aligned_v2.csv"
    structural = {}
    try:
        rows = list(__import__("csv").DictReader(csv_path.open(newline="")))
        audit = json.loads(audit_path.read_text())
        downstream = json.loads(downstream_path.read_text())
        bootstrap = json.loads((args.output_dir / "jma_gpm_daily_v2_event_bootstrap.json").read_text())
        structural = {
            "matched_daily_records": len(rows) == 81,
            "event_station_groups": len({(r["event"], r["station"]) for r in rows}) == 27,
            "events": len({r["event"] for r in rows}) == 3,
            "stations": len({r["station"] for r in rows}) == 9,
            "bootstrap_replicates": bootstrap.get("replicates") == 2000,
            "seed": bootstrap.get("seed") == m["random_seed"],
            "audit_formal_pass_false": audit.get("formal_pass") is False,
            "downstream_formal_pass_false": downstream.get("formal_pass") is False,
        }
    except (OSError, KeyError, json.JSONDecodeError, TypeError):
        structural = {"output_files_readable": False}
    result["structural_checks"] = structural

    for log in args.log:
        try:
            payload = json.loads(log.read_text())
            result["checks"][f"log:{log.name}"] = {"pass": payload.get("status", "").startswith("COMPLETED_WITH_")}
        except (OSError, json.JSONDecodeError):
            result["checks"][f"log:{log.name}"] = {"pass": False}

    result["status"] = "PASS" if all(v.get("pass", False) for v in result["checks"].values()) and all(structural.values()) else "FAIL"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
