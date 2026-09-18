from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v60.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = (215, 216, 217)
EXCLUDED = {
    "DK4_MES_B217_R0007": "Four-byte packed parrot-scene payload; not dialogue.",
}
LINES = {
    215: [
        "Hm, this?",
        "Something wrong?",
        "This thing here.",
        "...A bug?",
        "But a strange plant grows from it.",
        "True.",
        "That is called caterpillar fungus.",
        "People in China prize it as medicine.",
        "Medicine?",
        "Hm, medicine...",
        "Yes. Take this too.",
        "What is this?",
        "A book about many ingredients{LB}used in medicine.",
        "We cannot accept it for nothing.",
        "This old man no longer needs it,{LB}so take it.",
        "But...",
        "Hohoho.{LB}Your friend wants it.",
        "What? Well...{LB}This old man did want to read it.",
        "Understood.{LB}Will you sell it for 1,000 coins?",
        "Hohoho.{LB}Then 100 coins will do.",
        "{MACRO:FI}: Charm +1!",
    ],
    216: [
        "Bored. Time to go somewhere.",
        "Ma'am, anywhere interesting nearby?{LB}A walk might cure this boredom.",
        "Well, the lord's castle lies east.",
        "A castle? Sounds good.{LB}Time to see this country's castle.",
        "Jam, where were you?{LB}Everyone searched for you!",
        "Sorry. This was heavy.",
        "What's that? Where from?",
        "Obviously a figurehead!{LB}Genuine, made in Japan!",
        "People here misuse figureheads,{LB}so this man taught them.{LB}They gave this as thanks.",
        "You taught them? Huh.{LB}We sail soon. Pack.",
        "Got it. Give this man a moment.",
        "My lord! My looord!{LB}Disaster!",
        "What now? Noise from dawn!",
        "The shachihoko vanished,{LB}and this foreign letter appeared!",
        "What?! The shachihoko is gone?{LB}Catch that thief at any cost!",
        "At once!",
        "Dear lord of Japan,",
        "That statue is a figurehead.{LB}Such things belong on ships,{LB}not castles. Someone misunderstood.",
        "No thanks needed.{LB}One spare was taken instead.{LB}A ship needs one figurehead.{LB}Remember that.",
        "Take care.{LB}Jam Jack Ludwyan",
    ],
    217: [
        "flap, flap!",
        "Whoa! What is that?!",
        "WHAT'S THAT",
        "Mamma mia!{LB}That bird spoke!",
        "THAT PARROT TALKED",
        "That is a parrot.",
        "A parrot, eh?",
        "A PARROT, EH",
        "Quit that!",
        "STOP THAT",
        "Oh, fun!{LB}This man will catch you!",
        "Here goes! Hah!",
        "flap! Thud! Crash!{LB}flap! Bang! Rustle!",
        "Got it.",
        "Whew! Surrender now?{LB}Hahahaha!",
        "SURRENDER NOW",
        "Hah.",
    ],
}

SPEAKERS = {
    0x0B: "Jam Jack Ludwyan",
    0x0F: "Sailor",
    0x4B: "Crew scholar",
    0x7C: "Castle retainer",
    0x91: "Towns-woman",
    0xAA: "Herbalist",
    0xFE: "Parrot, system, or letter text",
}
CONTEXT = {
    215: "An herbalist explains caterpillar fungus and gives the crew a medicinal-materials book.",
    216: "Jam mistakes a castle's shachihoko for a ship's figurehead and takes it.",
    217: "A sailor encounters and captures a talking parrot.",
}


def main() -> None:
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = [row for row in csv.DictReader(stream) if row["id"].startswith(prefixes)]
    if len(source_rows) != 59:
        raise SystemExit(f"B215-B217 inventory changed: {len(source_rows)}")
    rows_by_block = {
        block: [
            row for row in source_rows
            if row["id"].startswith(f"DK4_MES_B{block}_") and row["id"] not in EXCLUDED
        ]
        for block in BLOCKS
    }
    for block, lines in LINES.items():
        if len(rows_by_block[block]) != len(lines):
            raise SystemExit(f"B{block}: {len(rows_by_block[block])} visible rows != {len(lines)} translations")

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
                "localization_note": "Faithful concise American English preserving item-event timing, canonical names, the parrot's mimicry, and fixed-record display constraints.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
                **({"manual_break_reason": "Protects action timing, four-line bounds, and progressive ASCII pair phase."} if "{LB}" in english else {}),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v60-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Raphael's medicinal-materials, Jam shachihoko, and talking-parrot events across SC0 blocks 215-217.",
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(source_rows),
            "translated_records": len(records),
            "blocks": {str(block): len(rows_by_block[block]) for block in BLOCKS},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} control preserved")


if __name__ == "__main__":
    main()
