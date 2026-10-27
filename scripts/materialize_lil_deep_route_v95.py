from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v95.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("A seller says the mast rope is worn.", "That mast rope's badly worn."),
    8: ("Lil thinks the rope is still usable.", "Really? Looks fine to me."),
    11: ("The seller offers a replacement rope said to have strange powers.",
         "Oh, it is. Why not try this rope? They say it has mysterious powers."),
    14: ("Lil asks whether the seller will replace it for free.",
         "Oh? You'll do it for free?"),
    18: ("The seller denies a free exchange and asks 300,000 coins.",
         "What? Of course not! A discount, sure. Say 300,000 coins."),
    21: ("Carlo warns the admiral against paying that price.",
         "Admiral, don't pay that!"),
    24: ("Carlo argues that even special rope is worth at most 30,000 coins.",
         "Special or not, 300,000? Rope's worth 30,000 tops."),
    27: ("The seller calls it unique and lowers the price to 200,000 coins.",
         "Wait! This is one of a kind. How about 200,000 coins?"),
    34: ("The seller reluctantly asks for 150,000 coins.",
         "150,000 coins. Please!"),
    37: ("Carlo counters with 75,000 coins.", "75,000."),
    41: ("The seller's final offer is 100,000 coins.",
         "100,000 coins. No lower!"),
    45: ("Carlo thinks the price is fair and asks the admiral to decide.",
         "Hm. That sounds fair. What do you say, Admiral?"),
    50: ("Choose to buy the rope.", "Buy"),
    52: ("Choose not to buy the rope.", "Pass"),
    59: ("Carlo says he will handle the purchase.", "Leave the rest to me."),
    62: ("Lil entrusts the purchase to Carlo.", "Sure. Go ahead."),
    69: ("Carlo tells the seller to bring the rope to the deck.",
         "Take the rope to the deck."),
    73: ("The seller thanks them for buying.", "Thank you for your business."),
    77: ("The system raises the named admiral's charm by one.", "{MACRO:FI}: Charm +1!"),
    80: ("The system raises Carlo's wit by one.", "Carlo's wit rose by 1!"),
    86: ("Lil decides the old rope still works and replacement can wait.",
         "Old rope still works. Let's keep it."),
    90: ("Carlo says he will decline the sale.", "All right. We'll pass."),
    94: ("The seller complains that they wasted his time.",
         "Not buying? Don't waste my time!"),
    97: ("Carlo apologizes to the seller.",
         "Sorry for the trouble. Please forgive us."),
    100: ("The system raises the named admiral's spirit by one.", "{MACRO:FI}: Spirit +1!"),
}
SPEAKERS = {0x69: "Rope seller", 0x02: "Lil", 0x13: "Carlo Sinato", 0xFE: "System notice"}
CHOICES = {50, 52}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B201_")}
    authored = {f"DK4_MES_B201_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B201 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B201_R{number:04d}"
        raw = bytes.fromhex(source_rows[row_id]["source_hex"])
        lead = raw[0]
        if number in CHOICES:
            if lead != 0x94:
                raise ValueError(f"{row_id}: unexpected Shift-JIS choice lead {lead:02X}")
            prefix, speaker = "", "Purchase choice"
        else:
            if lead not in SPEAKERS:
                raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
            prefix, speaker = f"{{SPEAKER:{lead:02X}}}", SPEAKERS[lead]
        prose = english.replace("{MACRO:FI}", "")
        if "I" in prose or "F" in prose:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        if raw.count(b"FI") != english.count("{MACRO:FI}"):
            raise ValueError(f"{row_id}: name macro count changed")
        records.append({
            "id": row_id,
            "english": f"{prefix}{english}{{PAD}}",
            "speaker": speaker,
            "context": "Lil and Carlo bargain over a supposedly enchanted mast rope.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B201 Japanese and parallel event context. "
                "Preserve 69/02/13/FE states and both FI reward macros. "
                "Choice-leading 94 is Shift-JIS text; literal uppercase I/F are unsafe."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v94-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 25 B201 rope bargaining, Buy/Pass choice, and reward records.",
        "inventory": {"identified_records": 25, "translated_records": 25, "blocks": {"201": 25}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
