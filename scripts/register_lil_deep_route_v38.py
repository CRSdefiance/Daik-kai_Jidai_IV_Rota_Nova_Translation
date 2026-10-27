from __future__ import annotations

import json
from pathlib import Path

STACK = Path("translations/release_stack.json")
BATCH = "translations/lil_deep_route_v38.json"


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    lil = list(profiles["lil-deep-route-v37"]["batches"])
    if BATCH not in lil:
        lil.append(BATCH)
    profiles["lil-deep-route-v38"] = {
        "status": "experimental", "batches": lil,
        "note": (
            "Extends Lil V37 with all seven B123 Christina-invitation and fifteen "
            "B124 Julian tavern-advice records. Runtime confirmation pending."
        ),
    }
    unified = list(profiles["all-routes-unified-v3"]["batches"])
    if BATCH not in unified:
        unified.append(BATCH)
    profiles["all-routes-unified-v4"] = {
        "status": "experimental", "require_screen_entry_layout": True,
        "batches": unified,
        "note": (
            "Four-route review build: complete unified V3 stack with Raphael V93, "
            "Hodram V32, Maria V111 and shared repairs, extended through Lil V38. "
            "Runtime confirmation pending."
        ),
    }
    STACK.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered Lil V38 ({len(lil)} batches) and unified V4 ({len(unified)} batches)")


if __name__ == "__main__":
    main()
