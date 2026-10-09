from __future__ import annotations

import json
from pathlib import Path

STACK = Path("translations/release_stack.json")
BATCH = "translations/lil_deep_route_v40.json"


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    lil = list(profiles["lil-deep-route-v39"]["batches"])
    if BATCH not in lil:
        lil.append(BATCH)
    profiles["lil-deep-route-v40"] = {
        "status": "experimental", "batches": lil,
        "note": (
            "Extends Lil V39 with all 15 B126 Bruges trading-post tutorial "
            "records, preserving both choices, FI and 02/09 presentation states. "
            "Runtime confirmation pending."
        ),
    }
    unified = list(profiles["all-routes-unified-v5"]["batches"])
    if BATCH not in unified:
        unified.append(BATCH)
    profiles["all-routes-unified-v6"] = {
        "status": "experimental", "require_screen_entry_layout": True,
        "batches": unified,
        "note": (
            "Four-route review build: complete unified V5 stack with Raphael V93, "
            "Hodram V32, Maria V111, shared repairs and Lil V40. Runtime confirmation pending."
        ),
    }
    STACK.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered Lil V40 ({len(lil)} batches) and unified V6 ({len(unified)} batches)")


if __name__ == "__main__":
    main()
