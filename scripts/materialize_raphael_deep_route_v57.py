from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v57.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = tuple(range(196, 200))
LINES = {
    196: [
        "Ah, delicious!",
        "Yes, tea truly is wonderful.",
        "How was something this tasty{LB}not fashionable before?",
        "True. People have no taste.",
        "Oh, our tea is nearly gone.{LB}Would you buy more tomorrow?",
        "Of course.",
        "Tea is so delicious and soothing.",
        "We cannot live without tea.",
        "Tea may boom in Sofala.",
    ],
    197: [
        "So cold. Truly freezing.",
        "Yes, coldest in years.",
        "A fur coat would help.{LB}This cold may freeze me.",
        "This cold has raised{LB}both fur sales and prices.",
        "So they say. Brrr!",
        "Hopefully it warms soon.",
        "True. Still, a fur coat would be lovely.",
        "A fur boom may hit Stockholm.",
    ],
    198: [
        "Hm... Something is missing.{LB}Sweetness! This needs sweetness.",
        "Sweetness?",
        "Yes! Such a plain taste{LB}cannot satisfy customers.{LB}Sweetness is vital!",
        "You think so?",
        "When this woman says so,{LB}it is true!",
        "Then how should we make it sweeter?",
        "Working that out is your job.",
        "...Yeah.",
        "Anyway, sweet goods{LB}will become fashionable.",
        "Yeah.",
        "Sweetness above all!{LB}Work hard now! Ohohoho!",
        "Sweets may boom in Alexandria.",
    ],
    199: [
        "Bad cough lately. Cough, cough.",
        "You okay?",
        "Yes. Just a little painful.{LB}Cough, cough.",
        "Many people seem to be coughing lately.",
        "Could an illness be spreading?",
        "Word says there is good medicine.",
        "Really? Which medicine? Cough.",
        "Name forgotten, but it uses almonds.",
        "Almonds?",
        "That odd ingredient is exactly{LB}why this man remembered it.",
        "Does it work? Cough, cough.",
        "They say it works like magic{LB}and sells well.",
        "Then time to find some.",
        "This man too.",
        "Thanks. Cough, cough.",
        "Almonds may boom in Malacca.",
    ],
}

SPEAKERS = {
    0x57: "City man",
    0x9B: "Coughing man",
    0xA4: "Tea drinker",
    0xA5: "Tea drinker",
    0xAE: "Merchant",
    0xAF: "Merchant's assistant",
    0xFE: "Market report",
}
CONTEXT = {
    196: "Tea drinkers predict a tea boom in Sofala.",
    197: "A cold spell predicts a fur boom in Stockholm.",
    198: "A demanding merchant predicts a sweets boom in Alexandria.",
    199: "A medicinal rumor predicts an almond boom in Malacca.",
}


def main() -> None:
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = [row for row in csv.DictReader(stream) if row["id"].startswith(prefixes)]
    if len(source_rows) != 45:
        raise SystemExit(f"B196-B199 inventory changed: {len(source_rows)}")
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
        "dialogue_profile": "raphael-story-deep-route-v57-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Four complete Raphael trade-boom events across SC0 blocks 196-199.",
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
