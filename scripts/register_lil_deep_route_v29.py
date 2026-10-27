from __future__ import annotations

import json
from pathlib import Path

STACK = Path("translations/release_stack.json")


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    batches = list(profiles["lil-deep-route-v28"]["batches"])
    batch = "translations/lil_deep_route_v29.json"
    if batch not in batches:
        batches.append(batch)
    profiles["lil-deep-route-v29"] = {
        "status": "experimental",
        "batches": batches,
        "note": (
            "Extends Lil V28 with all 73 B109-B110 Colosseum riddle and urn-puzzle "
            "dialogue records. The six-byte B109 event fragment remains unchanged "
            "as an explicit exclusion. Portraits, choices, first glyphs, and "
            "transitions await cold-boot review."
        ),
    }
    STACK.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered lil-deep-route-v29: {len(batches)} experimental batches")


if __name__ == "__main__":
    main()
