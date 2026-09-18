from __future__ import annotations

import json
from pathlib import Path


STACK = Path("translations/release_stack.json")
PROFILE = "all-routes-unified-v1"


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    raphael = list(profiles["raphael-deep-route-v93"]["batches"])
    lil = list(profiles["lil-deep-route-v21"]["batches"])
    hodram = list(profiles["hodram-deep-route-v32"]["batches"])

    # The ten shared interface/layout batches are identical in all three route
    # profiles.  Apply them once, then combine the disjoint SC0/SC1/SC2 route
    # layers and the now-source-verified Lil opening.
    original_infrastructure = raphael[:10]
    if lil[:10] != original_infrastructure or hodram[:10] != original_infrastructure:
        raise SystemExit("latest route profiles no longer share one infrastructure prefix")

    replaced_common = {
        "translations/common_shipyard_layout_v2.json",
        "translations/guild_item_descriptions_layout_v3.json",
        "translations/common_mystery_items_v1.json",
        "translations/common_runtime_layout_v4.json",
        "translations/common_global_layout_v1.json",
    }
    infrastructure = [
        batch for batch in original_infrastructure if batch not in replaced_common
    ]

    batches = [
        *infrastructure,
        "translations/common_mesfile_spacing_v4.json",
        "translations/supply_ratio_label_arm9_v1.json",
        "translations/help_literal_percent_safety_v1.json",
        "translations/raphael_literal_percent_safety_v1.json",
        *raphael[10:],
        *lil[10:],
        *hodram[10:],
    ]
    if len(batches) != len(set(batches)):
        raise SystemExit("unified profile contains a duplicate batch")

    profiles[PROFILE] = {
        "status": "experimental",
        "require_screen_entry_layout": True,
        "batches": batches,
        "note": (
            "Unified route candidate: Raphael V93, Lil V21 plus her source-locked "
            "Amsterdam opening, Hodram V32, shared interface layers, and the global "
            "COMMON MESFILE spacing/packed-entry repair."
        ),
    }
    STACK.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"registered {PROFILE}: {len(batches)} batches")


if __name__ == "__main__":
    main()
