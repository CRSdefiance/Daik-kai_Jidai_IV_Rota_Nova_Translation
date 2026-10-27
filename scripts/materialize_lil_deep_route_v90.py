from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v90.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("A strange seller says the admiral looks wealthy and laughs.", "You look rich... hee hee."),
    12: ("She offers an item for 200,000 coins and laughs.", "Got something to sell. 200,000 coins? Hee hee!"),
    24: ("A crewman challenges her inflated opening price.", "Hold on. You're not overcharging us?"),
    32: ("Buy the item at the offered price.", "Buy"),
    34: ("Decline and keep bargaining.", "Pass"),
    42: ("The seller praises the buyer and says the item will be useful.", "Generous! This will come in handy."),
    45: ("A system notice raises the named admiral's charm by one.", "{MACRO:FI}: Charm +1!"),
    62: ("The seller drops her asking price to 100,000 coins.", "100,000 coins, then? Hee hee!"),
    74: ("A companion notes the instant halving exposes the inflated price and advises two more bargains.",
         "(Half already? She overcharged. Haggle twice more.)"),
    82: ("Buy the item at the offered price.", "Buy"),
    84: ("Decline and keep bargaining.", "Pass"),
    92: ("The seller laughs, praises the bargain, and says the item will help.", "Hee hee! Sharp eye. This will come in handy."),
    107: ("The seller drops her asking price to 70,000 coins.", "Then 70,000 coins? Hee hee!"),
    118: ("A crewman privately recommends bargaining once more.", "(One more bargain might work.)"),
    126: ("Buy the item at the offered price.", "Buy"),
    128: ("Decline and keep bargaining.", "Pass"),
    136: ("The seller hands over the useful item and laughs.", "Here. Should come in handy. Hee hee!"),
    152: ("The seller calls the admiral greedy and lowers the price to 50,000 coins.",
          "Greedy, eh? 50,000 coins? Heh!"),
    170: ("An older crew member would hold out once more.", "(Try to hold out once more.)"),
    178: ("A younger crew member urges another price cut.", "(Make her lower it more!)"),
    187: ("Buy the item at the offered price.", "Buy"),
    189: ("Decline and keep bargaining.", "Pass"),
    197: ("The seller praises the admiral's bargaining and hands over the item.",
          "Sharp bargainer! Here's the item."),
    212: ("The seller reluctantly names a price of 40,000 coins.", "40,000 coins... heh."),
    223: ("A companion thinks this is the right time to buy.", "(Now's a good time to buy.)"),
    232: ("Buy the item at the offered price.", "Buy"),
    234: ("Decline and keep bargaining.", "Pass"),
    242: ("The seller thought the admiral would not buy and gives over the item.",
          "Thought you'd never buy. Here."),
    257: ("The seller pleads for a sale at 30,000 coins.", "Please buy it! Just 30,000 coins."),
    268: ("An older crew member says the price will not fall further.", "(This is as low as she'll go.)"),
    277: ("Buy the item at the offered price.", "Buy"),
    279: ("Decline the item at its lowest price.", "Pass"),
    287: ("The seller complains about the low sale price and asks the buyer to care for it.",
          "Tch, sold it far too cheap. Take good care of it."),
    302: ("The seller insults the admiral's judgment if the sale fails.", "Hmph. No eye for value!"),
    306: ("The seller says she will sell the item to somebody else.", "Then someone else can have it!"),
}
SPEAKERS = {
    0xAD: "Suspicious seller", 0x14: "Crewman", 0x13: "Adviser",
    0x06: "Older crew member", 0x19: "Younger crew member",
    0xFE: "System notice",
}
CHOICES = {32, 34, 82, 84, 126, 128, 187, 189, 232, 234, 277, 279}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B196_")}
    authored = {f"DK4_MES_B196_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B196 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B196_R{number:04d}"
        raw = bytes.fromhex(source_rows[row_id]["source_hex"])
        lead = raw[0]
        if number in CHOICES:
            if lead != 0x94:
                raise ValueError(f"{row_id}: choice has unexpected Shift-JIS lead {lead:02X}")
            prefix, speaker = "", "Purchase choice"
        else:
            if lead not in SPEAKERS:
                raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
            prefix, speaker = f"{{SPEAKER:{lead:02X}}}", SPEAKERS[lead]
        if english.count("{MACRO:FI}") != raw.count(b"FI"):
            raise ValueError(f"{row_id}: FI name-macro count mismatch")
        prose = english.replace("{MACRO:FI}", "")
        if "I" in prose or "F" in prose:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{prefix}{english}{{PAD}}",
            "speaker": speaker,
            "context": "Six-stage haggling for a charm-enhancing item, from 200,000 to 30,000 coins.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B196 Japanese. Choice-leading 94 is Shift-JIS "
                "text, not a speaker state; other source states and the FI macro "
                "are preserved. Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v90-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 35 B196 seller, six Buy/Pass choices, companion advice, outcomes and reward records.",
        "inventory": {"identified_records": 35, "translated_records": 35, "blocks": {"196": 35}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
