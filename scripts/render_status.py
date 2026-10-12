"""render_status.py — state table for the eight symplectic layers.

Single source of truth: LAYERS is imported from render_box.py (via
COMPONENTS/ANCHORS); it is never redeclared here.

States:
    landed  — the anchor file is committed to the tree and expected present.
    claimed — asserted by a claim, not yet verified against the tree.
    draft   — in design, may legitimately be absent.
    pinned  — sealed; reported as "---" and never fails any gate.

pres is the filesystem-observed existence of each anchor, refreshed on every
call.  pres is NOT "correct": the two disagree whenever the tree has drifted
from the declared state — that disagreement is precisely what prebuild
reports.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_box import ANCHORS, LAYERS, COMPONENT_COUNT  # noqa: E402

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent

# Default declared state: every layer landed. Flip individual entries to
# "claimed"/"draft" to exercise the --strict paths; "pinned" to freeze one.
STATUS = {layer: "landed" for layer in LAYERS}


def _pres_state():
    return {layer: (Path(_PROJECT_ROOT) / ANCHORS[layer]).exists() for layer in LAYERS}


def get_state():
    return {
        "counts": {"layers": len(LAYERS), "components": COMPONENT_COUNT},
        "declared": dict(STATUS),
        "pres": _pres_state(),
        "anchors": dict(ANCHORS),
        "root": str(_PROJECT_ROOT),
    }