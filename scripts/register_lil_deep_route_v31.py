from __future__ import annotations

import json
from pathlib import Path

STACK = Path("translations/release_stack.json")


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    batches = list(profiles["lil-deep-route-v30"]["batches"])
    batch = "translations/lil_deep_route_v31.json"
    if batch not in batches:
        batches.append(batch)
    profiles["lil-deep-route-v31"] = {
        "status": "experimental",
        "batches": batches,
        "note": (
            "Extends Lil V30 with all 30 B112 sandbar-rescue dialogue records. "
            "The seven-byte scene fragment remains unchanged as an explicit "
            "exclusion. Rescuer, child, and grandfather states are source mapped; "
            "runtime confirmation remains pending."
        ),
    }
    STACK.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered lil-deep-route-v31: {len(batches)} experimental batches")


if __name__ == "__main__":
    main()
