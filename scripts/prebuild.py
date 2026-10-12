#!/usr/bin/env python3
"""prebuild.py — existence gate over scripts/render_status.LAYERS.

Contract (first definition, accepted):

    Existence gate only: Path.exists() against the per-layer anchor.
    No compile, no lint, no format, no hash, no network.
    pres is not correct; both come from render_status.get_state().
    LAYERS single source of truth: imported from render_status.py,
    not redeclared here.
    pinned layer -> "---" in report, never fails.

    Exit codes:
        0  all landed anchors present (--strict: and no claimed/draft MISS)
        1  a landed anchor is missing (MISS) in either mode
        2  --strict only: a claimed or draft MISS that default mode
           would display without failing
        3  import/usage error (sibling modules missing, bad flags)
"""

import argparse
import sys
from pathlib import Path


def _load_state():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from render_status import get_state  # may raise ImportError
    return get_state()


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="prebuild.py",
        description="Existence gate over render_status.LAYERS.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="claimed/draft MISS also fail (exit 2).",
    )
    args = parser.parse_args(argv)

    try:
        state = _load_state()
    except Exception as exc:  # import/usage error -> exit 3
        print(f"prebuild: error: {exc}", file=sys.stderr)
        return 3

    declared = state["declared"]
    pres = state["pres"]
    anchors = state["anchors"]

    print(f"prebuild: layers={state['counts']['layers']} "
          f"components={state['counts']['components']}")
    print(f"prebuild: root={state['root']}")

    landed_missing = []
    claim_missing = []
    locked = []

    for layer in declared:
        status = declared[layer]
        present = pres[layer]
        mark = "OK" if present else "MISS"
        if status == "pinned":
            locked.append(layer)
            print(f"  {layer:16s} pinned  ---")
            continue
        print(f"  {layer:16s} {status:8s} {mark:4s} -> {anchors[layer]}")
        if not present:
            if status == "landed":
                landed_missing.append(layer)
            elif status in ("claimed", "draft"):
                claim_missing.append(layer)

    for layer in locked:
        print(f"  {layer:16s} --- (pinned, not evaluated)")

    if landed_missing:
        print(f"prebuild: landed MISS: {', '.join(landed_missing)}")
        return 1
    if args.strict and claim_missing:
        print(f"prebuild: --strict claim/draft MISS: {', '.join(claim_missing)}")
        return 2
    if claim_missing:
        print(f"prebuild: claim/draft MISS (display only): "
              f"{', '.join(claim_missing)}")
    print("prebuild: all landed anchors present")
    return 0


if __name__ == "__main__":
    sys.exit(main())