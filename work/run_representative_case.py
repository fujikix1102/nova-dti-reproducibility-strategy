#!/usr/bin/env python3
"""Run the frozen JMA–GPM v2 reproduction in the recorded order.

This wrapper does not modify the archived source files.  The legacy scripts
currently use the original /Volumes/1tbinside/NOVA/... paths, so the wrapper
fails early if that source tree is unavailable instead of silently substituting
different data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_CODE = Path("/Users/fujikijunichi/Documents/Codex/2026-09-27/new-chat")
DEFAULT_BASE = Path("/Volumes/1tbinside/NOVA/external_data/real_events")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--code-dir", type=Path, default=DEFAULT_CODE)
    ap.add_argument("--base-dir", type=Path, default=DEFAULT_BASE)
    ap.add_argument("--log", type=Path, default=Path("run_log.json"))
    args = ap.parse_args()

    required = {
        "jma": args.base_dir / "independent_events_jma_expanded/jma_independent_events_12station_daily_v2.csv",
        "gpm": args.base_dir / "independent_events_gpm_station_extract_expanded/gpm_independent_events_11station_30min_complete.csv",
    }
    scripts = ["recompute_jma_gpm_v2.py", "bootstrap_v2.py", "downstream_v2.py"]
    record = {
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "code_dir": str(args.code_dir),
        "base_dir": str(args.base_dir),
        "formal_pass_expected": False,
        "source_files": {k: {"path": str(v), "exists": v.exists()} for k, v in required.items()},
        "scripts": scripts,
        "steps": [],
    }

    missing = [str(p) for p in required.values() if not p.is_file()]
    missing += [str(args.code_dir / s) for s in scripts if not (args.code_dir / s).is_file()]
    if missing:
        record["status"] = "BLOCKED_MISSING_INPUT_OR_CODE"
        record["missing"] = missing
        args.log.parent.mkdir(parents=True, exist_ok=True)
        args.log.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(record, ensure_ascii=False, indent=2))
        return 2

    record["source_sha256"] = {k: sha256(v) for k, v in required.items()}
    for script in scripts:
        path = args.code_dir / script
        step = {"script": str(path), "sha256": sha256(path)}
        proc = subprocess.run([sys.executable, str(path)], text=True, capture_output=True)
        step.update({"returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr})
        record["steps"].append(step)
        if proc.returncode != 0:
            record["status"] = "FAILED"
            args.log.parent.mkdir(parents=True, exist_ok=True)
            args.log.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
            print(json.dumps(record, ensure_ascii=False, indent=2))
            return proc.returncode or 1

    record["status"] = "COMPLETED_WITH_FORMAL_PASS_FALSE_BOUNDARY"
    args.log.parent.mkdir(parents=True, exist_ok=True)
    args.log.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
