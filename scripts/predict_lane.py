#!/usr/bin/env python3
"""lane20: parallel prediction lane. SQLite and stdlib only. No kubectl.

Codename lane20. Scores are local rule outputs, not product claims.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "engine.db"
MODELS = ("rule-cadence", "rule-parity", "rule-bound")


def sha3(value: str) -> str:
    return hashlib.sha3_256(value.encode("utf-8")).hexdigest()


def task_id(model_id: str, payload: str) -> str:
    return sha3(f"{model_id}|{payload}|bucket-0")


def score(model_id: str, payload: str) -> dict:
    digest = sha3(payload)
    if model_id == "rule-cadence":
        value = int(digest[:2], 16) / 255
    elif model_id == "rule-parity":
        value = digest.count("a") / 64
    else:
        value = int(digest[-2:], 16) / 255
    return {"model_id": model_id, "value": round(value, 6), "input_hash": digest}


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS predictions (
            prediction_id TEXT PRIMARY KEY,
            model_id TEXT NOT NULL,
            input_hash TEXT NOT NULL,
            prediction_json TEXT NOT NULL,
            confidence REAL NOT NULL,
            prev_hash TEXT NOT NULL,
            hash TEXT NOT NULL
        )
        """
    )
    return conn


def run(payload: str = "lane20") -> dict:
    with ThreadPoolExecutor(max_workers=len(MODELS)) as pool:
        rows = list(pool.map(lambda model: score(model, payload), MODELS))
    conn = connect()
    prev = ""
    stored = []
    for row in rows:
        body = json.dumps(row, sort_keys=True)
        digest = sha3(f"{body}|{prev}")
        pid = task_id(row["model_id"], payload)
        conn.execute(
            """
            INSERT INTO predictions
                (prediction_id, model_id, input_hash, prediction_json, confidence, prev_hash, hash)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(prediction_id) DO UPDATE SET
                prediction_json=excluded.prediction_json,
                confidence=excluded.confidence,
                prev_hash=excluded.prev_hash,
                hash=excluded.hash
            WHERE predictions.hash != excluded.hash
            """,
            (pid, row["model_id"], row["input_hash"], body, row["value"], prev, digest),
        )
        stored.append({"prediction_id": pid, "model_id": row["model_id"], "hash": digest})
        prev = digest
    conn.commit()
    chain = conn.execute(
        "SELECT prev_hash, hash FROM predictions ORDER BY rowid"
    ).fetchall()
    walking = ""
    intact = True
    for previous, digest in chain:
        if previous != walking:
            intact = False
        walking = digest
    conn.close()
    return {
        "codename": "lane20",
        "rows": len(stored),
        "chain_ok": intact and len(chain) == len(MODELS),
        "kubectl": False,
        "tail": stored[-1]["hash"],
    }


def main() -> int:
    print(json.dumps(run(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
