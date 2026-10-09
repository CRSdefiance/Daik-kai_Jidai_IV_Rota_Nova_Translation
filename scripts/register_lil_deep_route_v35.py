from __future__ import annotations

import json
from pathlib import Path

STACK = Path("translations/release_stack.json")


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    batches = list(profiles["lil-deep-route-v34"]["batches"])
    batch = "translations/lil_deep_route_v35.json"
    if batch not in batches:
        batches.append(batch)
    profiles["lil-deep-route-v35"] = {
        "status": "experimental",
        "batches": batches,
        "note": (
            "Extends Lil V34 with the 28 remaining B120 sailing-tutorial records. "
            "Preserves two FI macros, 02/09/FE states, and the inherited V21 R0012. "
            "Directions, sails, stylus automation, and flagship stop instructions "
            "are source reviewed. Runtime confirmation remains pending."
        ),
    }
    STACK.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered lil-deep-route-v35: {len(batches)} experimental batches")


if __name__ == "__main__":
    main()
