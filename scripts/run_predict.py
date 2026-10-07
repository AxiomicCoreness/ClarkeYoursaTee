#!/usr/bin/env python3
"""Run lane20 twice and keep the record only if both JSON results match."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "ledger" / "predictions.jsonl"


def once() -> dict:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "predict_lane.py")],
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
        "codename": "lane20",
        "same": first == second,
        "chain_ok": first.get("chain_ok") is True,
        "kubectl": first.get("kubectl") is True,
        "tail": first.get("tail"),
    }
    LOG.write_text(json.dumps(record, sort_keys=True) + "\n")
    print(json.dumps(record, sort_keys=True))
    return 0 if record["same"] and record["chain_ok"] and not record["kubectl"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
