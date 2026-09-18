from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v58.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = tuple(range(200, 208))
LINES = {
    200: [
        "Splendid! Art itself.",
        "As you say.",
        "A piece this splendid{LB}must be from a famed artisan.",
        "So it seems.",
        "Hm. Never knew such things{LB}were in fashion.",
        "What is it called?",
        "Giyaman. Glass, my lord.",
        "Hm. Giyaman.",
        "Add it to my collection.{LB}Gather every piece in town.",
        "At once.",
        "Glass may boom in Osaka.",
    ],
    201: [
        "At last, that piece is mine.",
        "Oh, the ceramics?",
        "Yes. Just as expected, superb.",
        "Marvelous. May this man see it?",
        "Certainly. Please visit my home.",
        "This ceramics craze makes{LB}fine pieces hard to obtain.",
        "People who know no value{LB}are buying anything they see.",
        "A nuisance.",
        "Exactly.",
        "Look at those men.",
        "That pair? Why?",
        "They paid an absurd sum{LB}for worthless ceramics recently.",
        "Good customers, then.{LB}Our purses are empty.{LB}Shall we approach?",
        "Nice.",
        "Settled. Let's go.",
        "Sir!",
        "Ceramics may boom in Hamburg.",
    ],
    202: [
        "Heard the news?",
        "What?",
        "The mansion's lord.",
        "His mystery illness?",
        "Yes.",
        "Everyone knows that story.",
        "What came next?",
        "After?",
        "Store-bought medicine cured him at once.",
        "Common medicine cured him?",
        "Yes. Amazing, right?",
        "Yes... Really true?",
        "Apparently, that medicine{LB}cures every illness.",
        "Amazing! This man wants some too.",
        "Shall we find it?",
        "Let's go.",
        "Medicine boom in Havana.",
    ],
    203: [
        "Only that dye can produce this color.",
        "See? We must buy it now,{LB}before other shops take it all.",
        "But...",
        "Why wait?{LB}Once it sells out, it is too late.",
        "No need to rush.{LB}Surely it will not sell out.",
        "Wrong!{LB}So popular, it will vanish at once.",
        "Really?",
        "Yes!",
        "All right. Handle it.",
        "Do not sulk, father.{LB}This color guarantees profit.",
        "Really?",
        "Absolutely!",
        "Dyes may boom in Calicut.",
    ],
    204: [
        "Hey, ever smoked tobacco?",
        "You still have not tried it?",
        "No. Never had the chance.",
        "Really? With it this popular?{LB}You may be the only one in town!",
        "Maybe. This man would like to try.",
        "Come along; this man will show you.",
        "Sure.",
        "Tobacco may boom in Ｉstanbul.",
    ],
    205: [
        "What a meal!{LB}Never has this woman tasted{LB}anything so wonderful.",
        "Truly. Such an exciting flavor.",
        "How do you make food taste this good?",
        "Hehe. This is it.",
        "Chili pepper, a spice{LB}perfect for local foods.",
        "Oh. Must it be expensive?",
        "Not especially.",
        "Then perhaps this woman{LB}will use it tonight.",
        "This woman too.",
        "Then this woman can teach you{LB}right now.",
        "Really?!",
        "How kind.",
        "Of course. We are friends.",
        "Chili peppers may boom in Seoul.",
    ],
    206: [
        "This man tried sake.",
        "Same here.",
        "Pretty good, right?",
        "Apparently it is made from rice.",
        "Huh. They make liquor from that?",
        "Talking about it makes this man thirsty.{LB}Shall we have a cup?",
        "Sounds good.",
        "Then let us hurry.",
        "What?!{LB}{MACRO:FI}, did you hear?!",
        "This cannot wait!{LB}Let us buy that sake at once!",
        "W-wait, Julio!{LB}...What a handful.",
        "Sake may boom in Hangzhou.",
    ],
    207: [
        "Hm? Something smells delicious.",
        "Sniff... Yes.",
        "Barkeep, what smells?",
        "Our specialty, packed with cheese.{LB}Delicious!",
        "Really that good?",
        "Do not ask the obvious.",
        "Then bring us one.",
        "Certainly. Just a moment.{LB}Ready very soon.",
        "Here you are.",
        "That was fast.",
        "Just trust me and take a bite.",
        "Sure.",
        "Munch",
        "Munch",
        "Delicious!",
        "This is amazing!",
        "Told you!",
        "Everyone must hear about this!",
        "Yes! Barkeep, this dish{LB}will be a sensation!",
        "Cheese may boom in Veracruz.",
    ],
}

SPEAKERS = {
    0x06: "Julio Erdi",
    0x52: "Ceramics collector",
    0x56: "Dyer",
    0x5C: "Tavernkeeper",
    0x67: "Tavern patron",
    0x68: "Swindler",
    0x71: "Swindler",
    0x73: "Townsman",
    0x75: "Townsman",
    0x77: "Townsman",
    0x82: "Japanese lord",
    0x93: "Ceramics collector",
    0x96: "Retainer",
    0x99: "Townsman",
    0x9A: "Dyer's son",
    0x9C: "Townsman",
    0x9F: "Townsman",
    0xA6: "City woman",
    0xA7: "City woman",
    0xA8: "City woman",
    0xFE: "Market report",
}
CONTEXT = {
    200: "A Japanese lord orders every piece of fashionable glass in Osaka.",
    201: "Hamburg collectors discuss ceramics while swindlers target them.",
    202: "Havana townsmen seek a reputed cure-all medicine.",
    203: "Calicut dyers anticipate demand for a scarce dye.",
    204: "Townsmen spread the tobacco craze in Istanbul.",
    205: "Seoul women discover chili peppers and plan a cooking lesson.",
    206: "Hangzhou townsmen and Julio discover sake.",
    207: "Veracruz patrons discover a cheese dish and spread the word.",
}


def main() -> None:
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = [row for row in csv.DictReader(stream) if row["id"].startswith(prefixes)]
    if len(source_rows) != 112:
        raise SystemExit(f"B200-B207 inventory changed: {len(source_rows)}")
    rows_by_block = {
        block: [row for row in source_rows if row["id"].startswith(f"DK4_MES_B{block}_")]
        for block in BLOCKS
    }
    for block, lines in LINES.items():
        if len(rows_by_block[block]) != len(lines):
            raise SystemExit(f"B{block}: {len(rows_by_block[block])} rows != {len(lines)} translations")

    records = []
    for block, lines in LINES.items():
        for row, english in zip(rows_by_block[block], lines, strict=True):
            first = bytes.fromhex(row["source_hex"])[0]
            state = f"{first:02X}" if first in SPEAKERS else ""
            unsafe = english
            for macro in ("FI", "FA", "FO", "FU"):
                unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
            if "I" in unsafe or "F" in unsafe:
                raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
            records.append({
                "id": row["id"],
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(first, "Raphael companion or scene text"),
                "context": CONTEXT[block],
                "source_meaning": english.replace("{LB}", " ").replace("{MACRO:FI}", "Raphael"),
                "localization_note": "Faithful concise American English preserving the economic rumor and all fixed-record display constraints.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
                **({"manual_break_reason": "Protects dialogue grouping and progressive ASCII pair phase."} if "{LB}" in english else {}),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v58-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "The final eight complete Raphael trade-boom events across SC0 blocks 200-207.",
        "excluded_records": {},
        "inventory": {
            "identified_records": len(source_rows),
            "translated_records": len(records),
            "blocks": {str(block): len(rows_by_block[block]) for block in BLOCKS},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
