from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v78.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    7: ("A neighbor says homemade bread is best.", "Nothing beats baking your own bread!"),
    10: ("A second neighbor says her husband loved her bread.", "True. My husband loved ours!"),
    13: ("A third neighbor asks whether homemade bread is that good.", "Homemade bread tastes that good?"),
    17: ("The first neighbor says it is the best.", "The best! Right?"),
    21: ("The second neighbor says it beats the corner bakery.", "Yes! Better than the corner bakery."),
    24: ("The third neighbor considers baking her own bread.", "Might try baking some myself."),
    28: ("The first neighbor encourages her.", "You should!"),
    32: ("The second neighbor offers to teach her.", "We'll teach."),
    36: ("The third neighbor is delighted by the offer.", "Really? How lovely!"),
    40: ("The first neighbor suggests buying ingredients at once.", "Let's buy ingredients right away!"),
    43: ("The second neighbor asks what ingredients they need.", "What do we need?"),
    47: ("The third neighbor says wheat is essential.", "Wheat, of course!"),
    51: ("The market notice says wheat may boom in Amsterdam.", "Wheat may catch on in Amsterdam."),
}
SPEAKERS = {0xA6: "Amsterdam neighbor", 0xA7: "Amsterdam neighbor", 0xA8: "Amsterdam neighbor", 0xFE: "Market notice"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B178_")}
    authored = {f"DK4_MES_B178_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B178 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B178_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "Three Amsterdam neighbors plan to bake bread, prompting a wheat boom.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B178 Japanese. Source presentation "
                "leads are preserved. Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v78-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 13 B178 Amsterdam wheat-boom dialogue records.",
        "inventory": {"identified_records": 13, "translated_records": 13, "blocks": {"178": 13}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
