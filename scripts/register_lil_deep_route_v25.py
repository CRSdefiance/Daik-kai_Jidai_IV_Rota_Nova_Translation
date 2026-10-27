from __future__ import annotations

import json
from pathlib import Path

STACK = Path("translations/release_stack.json")


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    batches = list(profiles["lil-deep-route-v24"]["batches"])
    batch = "translations/lil_deep_route_v25.json"
    if batch not in batches:
        batches.append(batch)
    profiles["lil-deep-route-v25"] = {
        "status": "experimental",
        "batches": batches,
        "note": (
            "Extends Lil V24 with 42 source-reviewed SC2 records in B100-B104: "
            "the priest and Proof of Conquest, Santiago Cathedral, Lil's cross, "
            "and the temple voice. Runtime confirmation remains pending."
        ),
    }
    STACK.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered lil-deep-route-v25: {len(batches)} experimental batches")


if __name__ == "__main__":
    main()
