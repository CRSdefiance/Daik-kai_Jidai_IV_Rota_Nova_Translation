from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v100.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("A merchant offers something good for sale.", "Want to buy something nice?"),
    9: ("Cristina asks what he has.", "Like what?"),
    13: ("The merchant shows the item.", "Here."),
    17: ("Lil recognizes the earrings.", "Oh, what's that? Earrings!"),
    20: ("The merchant identifies ceramic earrings.", "That's right. Ceramic earrings."),
    24: ("Cristina does not see anything rare about them.", "They don't look that rare to me."),
    28: ("The merchant insists the earrings are special.",
         "Heh, these aren't ordinary earrings."),
    32: ("Lil does not see what is unusual about them.",
         "Really? Nothing special about them."),
    36: ("The merchant tells the dancer legend.",
         "The world's best dancer wore these. Dance in them, and any man will fall for you."),
    39: ("Lil declines to dance and asks Cristina.",
         "Dance? No thanks. How about you?"),
    42: ("Cristina has no man she wants to win over that badly.",
         "Maybe if they made me dance better. No man's worth that much effort."),
    46: ("The merchant suggests giving the earrings to a tavern woman.",
         "Give a tavern woman these earrings. She'll warm right up to you. You needn't wear them yourself."),
    49: ("Cristina asks why they would want to befriend her.",
         "And why would we want that?"),
    53: ("The merchant says tavern women know plenty of useful information.",
         "Befriend her and she'll share news. Tavern women know plenty."),
    59: ("First response choice acknowledges the value of tavern information.", "Got it"),
    61: ("Second response choice dismisses the pitch.", "So?"),
    68: ("The merchant responds to the interested choice.",
         "See? You get it now, don't you?"),
    71: ("Lil asks the price.", "How much?"),
    75: ("The merchant names a firm price of 9,000 coins.",
         "That'll be 9,000 coins. A bargain, and not a coin less."),
    80: ("Choice to buy the earrings.", "Buy"),
    82: ("Choice to reject the steep price.", "Pass"),
    90: ("The merchant hands over the ceramic earrings.",
         "Good eye. Here are your ceramic earrings."),
    97: ("The merchant refuses to sell after being dismissed.",
         "...Wrong about you. Get lost. Not for sale."),
    100: ("Cristina protests the merchant's rudeness.",
          "Hey, how rude! You called us over!"),
    103: ("The merchant calls them stingy and sends them away.",
          "Hmph. Cheapskates. Get lost."),
    106: ("Cristina rejects the merchant in return.",
          "Good! You can keep them!"),
    117: ("The merchant refuses a different branch after his explanation.",
          "Don't get it? Get lost. No deal."),
    120: ("Cristina is confused and disgusted by the merchant's attitude.",
          "Huh? What was that? How rude!"),
}
EXCLUDED = {
    "DK4_MES_B206_R0015": (
        "Four-byte 35 48 8A A8 packed item/scene payload, identical to the "
        "verified nontext payload in Hodram SC1 B210; leave unchanged."
    ),
}
SPEAKERS = {0xAD: "Merchant", 0x02: "Lil", 0x07: "Cristina"}
CHOICES = {59, 61, 80, 82}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B206_")}
    authored = {f"DK4_MES_B206_R{number:04d}" for number in LINES}
    if authored | EXCLUDED.keys() != expected or authored & EXCLUDED.keys():
        raise ValueError(f"B206 coverage mismatch: missing {expected - authored - EXCLUDED.keys()}")
    if source_rows["DK4_MES_B206_R0015"]["source_hex"].upper() != "35488AA8":
        raise ValueError("B206 packed item payload changed")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B206_R{number:04d}"
        raw = bytes.fromhex(source_rows[row_id]["source_hex"])
        lead = raw[0]
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        if number in CHOICES:
            if lead not in {0x82, 0x94, 0x8D}:
                raise ValueError(f"{row_id}: unexpected choice lead {lead:02X}")
            rendered = f"{english}{{PAD}}"
            speaker = "Choice"
        else:
            if lead not in SPEAKERS:
                raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
            rendered = f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}"
            speaker = SPEAKERS[lead]
        records.append({
            "id": row_id,
            "english": rendered,
            "speaker": speaker,
            "context": "Lil and Cristina consider a merchant's legendary ceramic earrings.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B206 Japanese and matching Hodram B210 event. "
                "Preserve AD/02/07 presentation states, four bare choice leads, and "
                "the unchanged packed item payload. Literal uppercase I/F are unsafe."
            ),
            **({"manual_break_reason": "Keeps dialogue at the source's dramatic pauses and safe glyph-pair boundaries."} if "{LB}" in english else {}),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v100-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "28 B206 ceramic-earrings text records; one packed event excluded unchanged.",
        "inventory": {"identified_records": 29, "translated_records": 28, "blocks": {"206": 28}},
        "excluded_records": EXCLUDED, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records; {len(EXCLUDED)} exclusion")


if __name__ == "__main__":
    main()
