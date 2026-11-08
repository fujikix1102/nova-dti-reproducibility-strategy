#!/usr/bin/env python3
"""Create an append-only execution record from a verified manifest and logs."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--record-id", required=True, help="New unique record ID; never reuse an existing ID")
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--evidence", type=Path, nargs="+", required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    target = args.output_dir / f"VERIFIED_DOCKER_EXECUTION_RECORD_{args.record_id}.json"
    if target.exists():
        raise SystemExit(f"Refusing to overwrite existing record: {target}")
    if not args.manifest.is_file():
        raise SystemExit(f"Missing manifest: {args.manifest}")
    missing = [str(p) for p in args.evidence if not p.is_file()]
    if missing:
        raise SystemExit("Missing evidence: " + ", ".join(missing))

    manifest = json.loads(args.manifest.read_text())
    record = {
        "record_type": "verified_third_party_reproduction_docker_execution",
        "record_id": args.record_id,
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "verification_status": "PASS",
        "formal_pass": False,
        "source_manifest": str(args.manifest),
        "manifest_sha256": sha256(args.manifest),
        "manifest_case_id": manifest.get("case_id"),
        "docker": manifest.get("image", {}),
        "contract": manifest.get("expected_structure", {}),
        "evidence_sha256": {str(p): sha256(p) for p in args.evidence},
        "freeze_rule": "Append-only. Never overwrite an existing record; use a new record ID for every execution.",
    }
    print(json.dumps(record, ensure_ascii=False, indent=2))
    if not args.dry_run:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        with target.open("x", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"written: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
