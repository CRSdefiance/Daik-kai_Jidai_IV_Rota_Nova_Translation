from __future__ import annotations

import json
from pathlib import Path


STACK = Path("translations/release_stack.json")


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    batches = list(profiles["maria-deep-route-v55"]["batches"])
    batches.append("translations/maria_deep_route_v56.json")
    profiles["maria-deep-route-v56"] = {
        "status": "experimental",
        "require_screen_entry_layout": True,
        "batches": batches,
        "note": (
            "Extends Maria V55 with all 51 dialogue records in SC3 blocks 46-47: "
            "the English colonial challenge, Espinosa's capture by his victims, "
            "the African regional-treasure lead, and Maria's public acclaim."
        ),
    }
    STACK.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"registered maria-deep-route-v56: {len(batches)} batches")


if __name__ == "__main__":
    main()
