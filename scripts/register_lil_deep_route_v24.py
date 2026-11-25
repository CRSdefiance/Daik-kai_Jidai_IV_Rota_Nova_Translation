from __future__ import annotations

import json
from pathlib import Path

STACK = Path("translations/release_stack.json")


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    batches = list(profiles["lil-deep-route-v23"]["batches"])
    batch = "translations/lil_deep_route_v24.json"
    if batch not in batches:
        batches.append(batch)
    profiles["lil-deep-route-v24"] = {
        "status": "experimental",
        "batches": batches,
        "note": (
            "Extends Lil V23 with 51 source-reviewed SC2 records: Yukihisa's "
            "Muramasa viewing in B99, the townwide tomato boom in B119, and "
            "Julio Erneco's recruitment in B165."
        ),
    }
    STACK.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered lil-deep-route-v24: {len(batches)} experimental batches")


if __name__ == "__main__":
    main()
