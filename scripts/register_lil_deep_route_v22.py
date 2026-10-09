from __future__ import annotations

import json
from pathlib import Path


STACK = Path("translations/release_stack.json")


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    batches = list(profiles["lil-deep-route-v21"]["batches"])
    batch = "translations/lil_deep_route_v22.json"
    if batch not in batches:
        batches.append(batch)
    profiles["lil-deep-route-v22"] = {
        "status": "experimental",
        "batches": batches,
        "note": (
            "Extends Lil V21 with 144 records from SC2 B81-B88 and B164: "
            "character and treasure scenes, Cesare Tohni's recruitment, and his "
            "ship-selection, cargo-hold, refit, and combat-readiness tutorial."
        ),
    }
    STACK.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered lil-deep-route-v22: {len(batches)} batches")


if __name__ == "__main__":
    main()
