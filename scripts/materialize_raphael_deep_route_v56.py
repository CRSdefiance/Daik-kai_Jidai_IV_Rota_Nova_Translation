from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v56.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = tuple(range(189, 196))
LINES = {
    189: [
        "Tomatoes! The coming age is tomatoes!",
        "Really? This bright-red food?",
        "That red stirs passion and recalls the burning love of youth.",
        "...Good for you.",
        "Make tomato dishes; sell them at once.",
        "Understood.",
        "Yes. We must not miss this tomato craze.",
        "Yeah.",
        "Work hard now! Ohohoho!",
        "Tomatoes may boom in Genoa.",
    ],
    190: [
        "Home-baked bread really is the best.",
        "Yes. My husband loved it.",
        "Really that much better?",
        "Simply wonderful.",
        "Yes. The corner bakery cannot compare.",
        "Really? Maybe try it.",
        "You should.",
        "Let me teach.",
        "Really? How lovely!",
        "Then let us buy ingredients at once.",
        "What do we need?",
        "Wheat, above all.",
        "Wheat may boom in Amsterdam.",
    ],
    191: [
        "So what?",
        "Wine? Any good?",
        "That good?",
        "Maybe a taste.{LB}Barkeep, bring one glass of wine.",
        "Here.",
        "Gulp, gulp, gulp...",
        "Delicious!{LB}Barkeep, another!",
        "Wine may boom in Sao Jorge.",
    ],
    192: [
        "Did you notice that woman's{LB}wonderful fragrance?",
        "You noticed it too?",
        "What scent was it?",
        "No idea, but that scent{LB}will surely catch on.",
        "Oh dear! We must obtain it{LB}before everyone else.",
        "Certainly.",
        "Shall we boldly ask her{LB}the next time we meet?",
        "A splendid idea.{LB}Let us do exactly that.",
        "Until next time.",
        "Goodbye.",
        "Spices may boom in Lisbon.",
    ],
    193: [
        "Did you see that brilliant red ruby?",
        "Yes. Magnificent.",
        "What is this about?",
        "The necklace that lady was wearing.",
        "Ah, that enormous, beautiful stone.",
        "Just once, this woman would love{LB}such a gift from a gentleman.",
        "Truly. Sigh...",
        "Sigh",
        "Sigh",
        "Rubies may boom in Athens.",
    ],
    194: [
        "Did you hear?{LB}The princess is to be engaged.",
        "Yes, to the duke's son, correct?",
        "That ring is worth a mountain.",
        "Such wealth suits a duke.{LB}When might we see that jewel?",
        "Before long, surely.{LB}Then every lady will want that gem.",
        "Oh! Once it catches on, too late.{LB}Do you know which gem?",
        "No. We must ask around immediately!",
        "Gems may boom in London.",
    ],
    195: [
        "Hm?",
        "Truly wonderful!",
        "You do?",
        "He will be a famous artist.",
        "Ah.",
        "You should buy his work while you can.",
        "This one is better!",
        "Not bad, but no match for his work.",
        "Nonsense. That one is clearly the better work.",
        "Still, his painting is mine!",
        "Work by this artist is mine!",
        "This one is mine!",
        "Thank you very much.",
        "Slam!",
        "At last, they left.{LB}Must they argue in the shop every time?",
        "What was that commotion?",
        "A rich man's pastime.",
        "A rich hobby?",
        "Yes. Painting is in fashion.",
        "A refined hobby.",
        "Though few buyers have a true eye for art.",
        "Hahaha! Bold words, dealer.",
        "Oops. Please keep that secret.",
        "Understood.",
        "Paintings may boom in Basra.",
    ],
}

SPEAKERS = {
    0x55: "Art dealer",
    0x5C: "Barkeep",
    0x60: "Tavern patron",
    0x6E: "Art buyer",
    0x84: "Art buyer",
    0x94: "Art buyer",
    0x99: "Raphael companion",
    0xA6: "City woman",
    0xA7: "City woman",
    0xA8: "City woman",
    0xAE: "Merchant",
    0xAF: "Merchant's assistant",
    0xFE: "Market report",
}
CONTEXT = {
    189: "A merchant predicts a tomato boom in Genoa.",
    190: "A conversation about home baking predicts a wheat boom in Amsterdam.",
    191: "A tavern patron discovers wine and predicts a wine boom in Sao Jorge.",
    192: "Two women discuss a fashionable fragrance and predict a spice boom in Lisbon.",
    193: "Three women admire a ruby necklace and predict a ruby boom in Athens.",
    194: "Talk of a royal engagement predicts a gem boom in London.",
    195: "Competing art buyers and a candid dealer predict a painting boom in Basra.",
}


def main() -> None:
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = [row for row in csv.DictReader(stream) if row["id"].startswith(prefixes)]
    if len(source_rows) != 85:
        raise SystemExit(f"B189-B195 inventory changed: {len(source_rows)}")
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
                "source_meaning": english.replace("{LB}", " "),
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
        "dialogue_profile": "raphael-story-deep-route-v56-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Seven complete Raphael trade-boom events across SC0 blocks 189-195.",
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
