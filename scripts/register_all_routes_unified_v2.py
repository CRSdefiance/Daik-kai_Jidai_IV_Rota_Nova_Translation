import json
from pathlib import Path

STACK = Path("translations/release_stack.json")


def main() -> None:
    payload = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    unified = list(profiles["all-routes-unified-v1"]["batches"])
    spacing = "translations/common_mesfile_spacing_v4.json"
    spacing_base = "translations/common_mesfile_spacing_v4_unified_base.json"
    unified[unified.index(spacing)] = spacing_base
    encounter_directions = "translations/common_encounter_directions_arm9_v1.json"
    if encounter_directions not in unified:
        supply_ratio = "translations/supply_ratio_label_arm9_v1.json"
        unified.insert(unified.index(supply_ratio) + 1, encounter_directions)
    for batch in profiles["lil-deep-route-v23"]["batches"]:
        if batch not in unified:
            unified.append(batch)
    for batch in profiles["maria-deep-route-v111"]["batches"]:
        if batch not in unified:
            unified.append(batch)
    profiles["all-routes-unified-v2"] = {
        "status": "experimental",
        "require_screen_entry_layout": True,
        "batches": unified,
        "note": (
            "True unified release: Raphael V93, Hodram V32, Lil V23, Maria V111, "
            "and the newest shared interface, layout, encounter-direction, and COMMON layers. The legacy "
            "COMMON spacing layer is filtered where newer accepted layout records supersede it."
        ),
    }
    STACK.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered all-routes-unified-v2: {len(unified)} batches")


if __name__ == "__main__":
    main()
