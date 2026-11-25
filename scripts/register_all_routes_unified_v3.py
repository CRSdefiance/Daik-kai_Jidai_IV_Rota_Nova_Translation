from __future__ import annotations

import json
from pathlib import Path

STACK = Path("translations/release_stack.json")


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    lil = list(profiles["lil-deep-route-v36"]["batches"])
    batch = "translations/lil_deep_route_v37.json"
    if batch not in lil:
        lil.append(batch)
    profiles["lil-deep-route-v37"] = {
        "status": "experimental", "batches": lil,
        "note": "Extends V36 with all 30 B122 Clifford farewell records, preserving three FI macros and 02/09/97/FE states. Runtime confirmation pending.",
    }
    unified = list(profiles["all-routes-unified-v2"]["batches"])
    for batch in lil:
        if batch not in unified:
            unified.append(batch)
    profiles["all-routes-unified-v3"] = {
        "status": "experimental", "require_screen_entry_layout": True,
        "batches": unified,
        "note": (
            "Cumulative four-route candidate: preserves the complete unified V2 stack "
            "(Raphael V93, Hodram V32, Maria V111, shared UI/layout/COMMON repairs) "
            "and adds Lil V24-V37. No baseline promotion; cold-boot acceptance pending."
        ),
    }
    STACK.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered all-routes-unified-v3: {len(unified)} experimental batches")


if __name__ == "__main__":
    main()
