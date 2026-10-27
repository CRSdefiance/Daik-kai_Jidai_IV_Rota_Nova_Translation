from __future__ import annotations

import json
from pathlib import Path

STACK = Path("translations/release_stack.json")


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    batches = list(profiles["lil-deep-route-v31"]["batches"])
    batch = "translations/lil_deep_route_v32.json"
    if batch not in batches:
        batches.append(batch)
    profiles["lil-deep-route-v32"] = {
        "status": "experimental",
        "batches": batches,
        "note": (
            "Extends Lil V31 with 19 B113-B114 jade-discovery and cacao-follow-up "
            "dialogue records. The two non-prose B113 fragments remain unchanged "
            "as explicit exclusions. Townsman's 68 state is source mapped; "
            "runtime confirmation remains pending."
        ),
    }
    STACK.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered lil-deep-route-v32: {len(batches)} experimental batches")


if __name__ == "__main__":
    main()
