from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v89.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    6: ("A patron notices an appetizing smell.", "Hey, smell something good?"),
    9: ("His friend sniffs and agrees.", "Sniff... Yeah."),
    13: ("The patron asks the barkeep what is cooking.", "Hey, what's cooking?"),
    17: ("The barkeep says it is his delicious cheese-rich house specialty.", "Our specialty. Cheesy and delicious!"),
    20: ("The friend asks whether it truly tastes good.", "Really that good?"),
    24: ("The barkeep insists that of course it does.", "Why ask? Of course it is!"),
    28: ("The patron orders one serving for them.", "Then one for us, please."),
    32: ("The barkeep asks them to wait a moment while he brings it.", "Coming up. Won't be long."),
    35: ("The barkeep serves the food.", "Here you go."),
    39: ("The patron is impressed by the quick service.", "That was fast!"),
    43: ("The barkeep urges them to taste it.", "Go on. Give it a try."),
    46: ("The patron agrees.", "Right."),
    50: ("The patron chews.", "Munch."),
    54: ("His friend chews.", "Munch."),
    58: ("The patron finds the dish delicious.", "Delicious!"),
    62: ("His friend is equally impressed.", "Wow, so good!"),
    65: ("The barkeep says he told them so.", "Told you!"),
    69: ("The patron wants to tell everyone about the dish.", "Everyone should know about this!"),
    73: ("His friend predicts the barkeep's dish will become very popular.", "Yeah! Barkeep, this will be a hit!"),
    77: ("The market notice predicts cheese will become popular in Veracruz.", "Cheese may catch on in Veracruz."),
}
SPEAKERS = {0x77: "Patron", 0x67: "Friend", 0x5C: "Barkeep", 0xFE: "Market notice"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B195_")}
    authored = {f"DK4_MES_B195_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B195 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B195_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "Veracruz barkeep serves a cheese-rich dish to two patrons.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B195 Japanese. Source presentation "
                "leads are preserved. Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v89-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 20 B195 Veracruz cheese-dish market records.",
        "inventory": {"identified_records": 20, "translated_records": 20, "blocks": {"195": 20}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
