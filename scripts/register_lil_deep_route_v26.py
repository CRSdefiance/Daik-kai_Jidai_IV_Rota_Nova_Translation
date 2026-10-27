from __future__ import annotations

import json
from pathlib import Path

STACK = Path("translations/release_stack.json")


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    batches = list(profiles["lil-deep-route-v25"]["batches"])
    batch = "translations/lil_deep_route_v26.json"
    if batch not in batches:
        batches.append(batch)
    profiles["lil-deep-route-v26"] = {
        "status": "experimental",
        "batches": batches,
        "note": (
            "Extends Lil V25 with all 36 source-reviewed SC2 B105 Sphinx-riddle "
            "records, including both riddles, choice text, failure reactions, and "
            "the reward. Runtime confirmation remains pending."
        ),
    }
    STACK.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered lil-deep-route-v26: {len(batches)} experimental batches")


if __name__ == "__main__":
    main()
