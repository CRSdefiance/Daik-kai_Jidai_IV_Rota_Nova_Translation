from __future__ import annotations

import json
from pathlib import Path

STACK = Path("translations/release_stack.json")


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    batches = list(profiles["lil-deep-route-v35"]["batches"])
    batch = "translations/lil_deep_route_v36.json"
    if batch not in batches:
        batches.append(batch)
    profiles["lil-deep-route-v36"] = {
        "status": "experimental",
        "batches": batches,
        "note": (
            "Extends Lil V35 with all 109 B121 ambush, rescue, reconciliation, "
            "family-history and farewell records. Preserves both rescue branches, "
            "ten FI macros, fourteen presentation states and bare combat choices. "
            "Runtime confirmation remains pending."
        ),
    }
    STACK.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered lil-deep-route-v36: {len(batches)} experimental batches")


if __name__ == "__main__":
    main()
