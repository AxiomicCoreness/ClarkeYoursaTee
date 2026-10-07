#!/usr/bin/env python3
"""Run the ClarkeYoursaTee engine twice. Stdlib only. No kubectl."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "scripts" / "clarke_engine.py"
LOG = ROOT / "ledger" / "engine_run.jsonl"


def once() -> dict:
    proc = subprocess.run(
        [sys.executable, str(ENGINE)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr or proc.stdout)
    return json.loads(proc.stdout)


def main() -> int:
    first = once()
    second = once()
    record = {
        "runner": "scripts/run_engine.py",
        "same": first == second,
        "chain_ok": first.get("chain_ok") is True,
        "kubectl": first.get("kubectl") is True,
        "packet_hash": first.get("packet_hash"),
    }
    LOG.parent.mkdir(exist_ok=True)
    LOG.write_text(json.dumps(record, sort_keys=True) + "\n")
    print(json.dumps(record, sort_keys=True))
    return 0 if record["same"] and record["chain_ok"] and not record["kubectl"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
