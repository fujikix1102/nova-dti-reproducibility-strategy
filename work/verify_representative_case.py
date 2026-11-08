#!/usr/bin/env python3
"""Verify the structural contract of the JMA–GPM v2 outputs."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("comparison_dir", type=Path)
    args = ap.parse_args()
    d = args.comparison_dir
    csv_path = d / "jma_gpm_daily_jst_aligned_v2.csv"
    audit_path = d / "jma_gpm_daily_v2_audit.json"
    boot_path = d / "jma_gpm_daily_v2_event_bootstrap.json"
    downstream_path = d / "jma_gpm_daily_v2_downstream_audit.json"
    required = [csv_path, audit_path, boot_path, downstream_path]
    missing = [str(p) for p in required if not p.is_file()]
    result = {"expected_formal_pass": False, "missing": missing, "checks": {}}
    if missing:
        result["status"] = "FAIL_MISSING_OUTPUT"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    with csv_path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    audit = json.loads(audit_path.read_text())
    boot = json.loads(boot_path.read_text())
    downstream = json.loads(downstream_path.read_text())
    checks = {
        "matched_rows_81": len(rows) == 81,
        "event_station_groups_27": len({(r["event"], r["station"]) for r in rows}) == 27,
        "events_3": len({r["event"] for r in rows}) == 3,
        "stations_9": len({r["station"] for r in rows}) == 9,
        "bootstrap_replicates_2000": boot.get("replicates") == 2000,
        "audit_formal_pass_false": audit.get("formal_pass") is False,
        "downstream_formal_pass_false": downstream.get("formal_pass") is False,
    }
    result["checks"] = checks
    result["status"] = "PASS" if all(checks.values()) else "FAIL_CONTRACT_MISMATCH"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
