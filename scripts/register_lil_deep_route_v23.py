from __future__ import annotations

import json
from pathlib import Path


STACK = Path("translations/release_stack.json")


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    batches = list(profiles["lil-deep-route-v22"]["batches"])
    batch = "translations/lil_deep_route_v23.json"
    if batch not in batches:
        batches.append(batch)
    profiles["lil-deep-route-v23"] = {
        "status": "experimental",
        "batches": batches,
        "note": (
            "Extends Lil V22 with 157 records from SC2 B91-B96 and B166-B167: "
            "six treasure and companion scenes, Manuel Almeida's recruitment and "
            "ship-room tutorial, and the complete sail and wind-angle lesson."
        ),
    }
    STACK.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered lil-deep-route-v23: {len(batches)} batches")


if __name__ == "__main__":
    main()
