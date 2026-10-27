from __future__ import annotations

import json
from pathlib import Path

STACK = Path("translations/release_stack.json")
BATCH = "translations/lil_deep_route_v39.json"


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    lil = list(profiles["lil-deep-route-v38"]["batches"])
    if BATCH not in lil:
        lil.append(BATCH)
    profiles["lil-deep-route-v39"] = {
        "status": "experimental", "batches": lil,
        "note": (
            "Extends Lil V38 with all 44 B125 moral-doubt, two-choice, "
            "Guiding Staff and spirit-reward records. Runtime confirmation pending."
        ),
    }
    unified = list(profiles["all-routes-unified-v4"]["batches"])
    if BATCH not in unified:
        unified.append(BATCH)
    profiles["all-routes-unified-v5"] = {
        "status": "experimental", "require_screen_entry_layout": True,
        "batches": unified,
        "note": (
            "Four-route review build: complete unified V4 stack with Raphael V93, "
            "Hodram V32, Maria V111, shared repairs and Lil V39. Runtime confirmation pending."
        ),
    }
    STACK.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered Lil V39 ({len(lil)} batches) and unified V5 ({len(unified)} batches)")


if __name__ == "__main__":
    main()
