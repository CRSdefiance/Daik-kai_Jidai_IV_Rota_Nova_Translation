from __future__ import annotations

import json
from pathlib import Path

STACK = Path("translations/release_stack.json")


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    batches = list(profiles["lil-deep-route-v29"]["batches"])
    batch = "translations/lil_deep_route_v30.json"
    if batch not in batches:
        batches.append(batch)
    profiles["lil-deep-route-v30"] = {
        "status": "experimental",
        "batches": batches,
        "note": (
            "Extends Lil V29 with 33 B111 gold-temple monk dialogue records. "
            "Two language-neutral three-byte monk ellipses remain unchanged as "
            "explicit exclusions. The monk's 89 presentation state is batch "
            "scoped; runtime confirmation remains pending."
        ),
    }
    STACK.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered lil-deep-route-v30: {len(batches)} experimental batches")


if __name__ == "__main__":
    main()
