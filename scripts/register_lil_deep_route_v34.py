from __future__ import annotations

import json
from pathlib import Path

STACK = Path("translations/release_stack.json")


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    batches = list(profiles["lil-deep-route-v33"]["batches"])
    batch = "translations/lil_deep_route_v34.json"
    if batch not in batches:
        batches.append(batch)
    profiles["lil-deep-route-v34"] = {
        "status": "experimental",
        "batches": batches,
        "note": (
            "Extends Lil V33 with 30 B116-B118 India-tip, figurehead-discovery, "
            "and tribal knife-reward records. C6/D1/DC/B3 states are source "
            "mapped; two non-prose staging fragments remain unchanged. "
            "Runtime confirmation remains pending."
        ),
    }
    STACK.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered lil-deep-route-v34: {len(batches)} experimental batches")


if __name__ == "__main__":
    main()
