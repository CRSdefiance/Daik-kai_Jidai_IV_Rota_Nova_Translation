from __future__ import annotations

import json
from pathlib import Path


STACK = Path("translations/release_stack.json")


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    batches = list(profiles["lil-deep-route-v20"]["batches"])
    batches.append("translations/lil_deep_route_v21.json")
    profiles["lil-deep-route-v21"] = {
        "status": "experimental",
        "batches": batches,
        "note": (
            "Extends Lil V20 with runtime fixes for choice centering, a literal-percent "
            "format-string failure, and untranslated B120 dialogue."
        ),
    }
    STACK.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"registered lil-deep-route-v21: {len(batches)} batches")


if __name__ == "__main__":
    main()
