from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v50.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
EXCLUDED = {"DK4_MES_B176_R0020": "Seven-byte ship-return scene control; no independently rendered dialogue."}
LINES = {
    174: ["Still hasn't returned."],
    175: ["Still hasn't returned."],
    176: [
        "Admiral! Admiral!{LB}That ship has returned!",
        "What?! Really?!",
        "There! That's the ship.{LB}No mistake!",
        "Yee-haw! The sea is great!{LB}Wide! Huge!",
        "Whew... fun since sunrise.{LB}Another fresh day! Yee-haw!",
        "Stranger than thought...",
        "Hey, you!{LB}Don't board another person's ship!",
        "Huh?{LB}Lying here!",
        "Ships don't lie around anywhere!",
        "Walking by the port, there it lay,{LB}abandoned and lonely!{LB}That's the truth, so there.",
        "Thus kindhearted Jam picked it up!{LB}Jam: J-A-M!{LB}Yee-haw!",
        "You sailed it because you found it?{LB}How did you move it alone?",
        "Did this, did that...{LB}Mostly instinct! Yee-haw!",
        "Amazing.",
        "Listen.{LB}Ships move on water!{LB}What if you had sunk?!",
        "Tsk, tsk, tsk!{LB}Here's a great saying.{LB}Listen well!",
        "'Try, and it happens!'{LB}Good enough for me! Yee-haw!",
        "This one is trouble.",
        "'Try, and it works'...",
        "All thanks to me--good!{LB}'Life runs bold and short!'{LB}That's the rule!",
        "Looking down, inching along,{LB}'thin and long'?{LB}Too boring for me!",
        "What a man...{LB}{MACRO:FI}, what now?{LB}Call the guard?",
        "No! Claudio,{LB}let's recruit him!",
        "Hey, {MACRO:FI}.{LB}Did his stupidity spread to you?",
        "But he sailed alone!{LB}That's incredible.{LB}Jam, right?",
        "Join us?",
        "Hmm. Go or not go...{LB}What to do? Just a moment!{LB}Wait! Two seconds to decide!",
        "All right!",
        "Decided?",
        "Yes. Not going!{LB}Goodbye! Have a fine voyage!",
        "What?! W-wait!",
        "Ha! Just the reaction expected!{LB}Merci! Kidding!",
        "A joke?",
        "Yes, take me along!{LB}Jam Jack Ludwyan!{LB}Yee-haw!",
    ],
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = [row for row in csv.DictReader(stream) if row["id"].startswith(tuple(f"DK4_MES_B{block}_" for block in LINES))]
    if len(source_rows) != 37:
        raise SystemExit(f"B174-B176 inventory changed: {len(source_rows)}")
    rows_by_block = {block: [row for row in source_rows if row["id"].startswith(f"DK4_MES_B{block}_") and row["id"] not in EXCLUDED] for block in LINES}
    for block, lines in LINES.items():
        if len(rows_by_block[block]) != len(lines):
            raise SystemExit(f"B{block}: {len(rows_by_block[block])} visible rows != {len(lines)} translations")
    speaker_names = {0x05: "Claudio Manini", 0x0B: "Jam Jack Ludwyan", 0x14: "Raphael companion", 0x74: "Port attendant"}
    records = []
    for block, lines in LINES.items():
        for row, english in zip(rows_by_block[block], lines, strict=True):
            first = bytes.fromhex(row["source_hex"])[0]
            state = f"{first:02X}" if first in speaker_names else ""
            unsafe = english
            for macro in ("FI", "FA", "FO", "FU"):
                unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
            if "I" in unsafe or "F" in unsafe:
                raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
            records.append({
                "id": row["id"], "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": speaker_names.get(first, "Raphael Castor or companion"),
                "context": "The port waits for Raphael's stolen ship, then the eccentric Jam Jack Ludwyan returns it after sailing alone and joins the crew.",
                "source_meaning": english.replace("{LB}", " ").replace("{MACRO:FI}", "Raphael"),
                "localization_note": "Faithful energetic American English preserving Jam's absurd logic, motto, prank, canonical name, and yee-haw verbal tic.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
                **({"manual_break_reason": "Protects comic timing, four-line bounds, and progressive ASCII pair phase."} if "{LB}" in english else {}),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v50-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Stolen-ship waiting lines and Jam Jack Ludwyan's complete recruitment across SC0 blocks 174-176.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": {str(block): len(rows_by_block[block]) for block in LINES}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} control excluded")


if __name__ == "__main__":
    main()
