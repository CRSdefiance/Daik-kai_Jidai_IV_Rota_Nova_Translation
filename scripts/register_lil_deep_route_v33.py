from __future__ import annotations

import json
from pathlib import Path

STACK = Path("translations/release_stack.json")


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    batches = list(profiles["lil-deep-route-v32"]["batches"])
    batch = "translations/lil_deep_route_v33.json"
    if batch not in batches:
        batches.append(batch)
    profiles["lil-deep-route-v33"] = {
        "status": "experimental",
        "batches": batches,
        "note": (
            "Extends Lil V32 with all 37 B115 tablet and shared Maria raider-recruitment "
            "records. Preserves the 03/04/B4 states and FO macro; the opening LF in "
            "R0089 is staging, not a speaker selector. Runtime review remains pending."
        ),
    }
    STACK.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered lil-deep-route-v33: {len(batches)} experimental batches")


if __name__ == "__main__":
    main()
