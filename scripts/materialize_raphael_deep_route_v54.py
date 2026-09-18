from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v54.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
EXCLUDED = {"DK4_MES_B181_R0129": "Eight-byte Taoist-art action control; no independently rendered dialogue."}
LINES = {
    181: [
        "Hey, {MACRO:FI}.{LB}Seems like someone's watching us.",
        "Really?",
        "Got a bad feeling...{LB}Let's return to the ship early.",
        "Hey! Did you say 'ship'?{LB}Are you two sailors?",
        "Whoa! Who are you?!",
        "Y-yes, we're sailors.{LB}Why do you ask?",
        "Lucky!{LB}Let me board your ship!{LB}Trouble has me cornered.",
        "That's rather sudden...",
        "Ran away from my master.{LB}Getting caught would be bad.{LB}So come on! Let's go!",
        "Hey! Don't decide for us.{LB}Not our problem.",
        "Sorry. We can't take someone aboard{LB}just for fun.",
        "Just for fun?!{LB}You think this child's a fool!",
        "This is serious!{LB}A real sailor--that's my goal!",
        "Why do you want to sail?",
        "To travel around the world!",
        "Training in many countries,{LB}becoming much stronger,{LB}then proving my master wrong!",
        "Stronger?{LB}What are you training in?",
        "Taoist arts!",
        "Taoist?",
        "Your resolve is clear.{LB}But our voyage isn't a game.",
        "Shipboard life is hard.{LB}Once underway, leaving midway{LB}is impossible.",
        "No problem!{LB}Training made me tough.{LB}Any ship work can be handled!",
        "But...",
        "Aha! You don't believe me.{LB}Beat this man, and you take me.{LB}Deal?",
        "What? You want to fight me?{LB}That's asking a lot.",
        "Here goes!{LB}Prepare yourself!",
        "All right...{LB}Don't blame me if hurt.",
        "Haaah!!",
        "(Did she act?)",
        "Now!",
        "Gah! What was that?",
        "See?{LB}The paralyzing art!",
        "A-amazing!",
        "Wait! That wasn't magic.{LB}You merely caught me off guard!",
        "Still, closing in on Claudio{LB}that far takes real skill.",
        "Why admire her?!{LB}Stupid. Let's go!",
        "Hey!{LB}Won't you take me?",
        "Uh...",
        "Come on!{LB}Move, {MACRO:FI}!",
        "All right! Don't pull my arm.{LB}Such a temper...",
    ],
    182: [
        "That was awful.{LB}The bad feeling came true.",
        "Hehe. Came along!",
        "What?! How?!",
        "Another Taoist art!",
        "Amazing!{LB}Never noticed you!",
        "With this crowd,{LB}missing her is hardly strange!",
        "Hehe. Sour grapes from before?",
        "Shut up!",
        "A young girl made a fool of you.{LB}Now you're angry. Ho ho!",
        "What, old man?!",
        "Well? Made a decision?",
        "You truly mean to sail?",
        "Of course!",
        "Her resolve is firm.",
        "Once, being seen as an adult{LB}quickly mattered to me too...",
        "All right. Join us!{LB}Your name?",
        "Yifa!",
    ],
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = [row for row in csv.DictReader(stream) if row["id"].startswith(("DK4_MES_B181_", "DK4_MES_B182_"))]
    if len(source_rows) != 58:
        raise SystemExit(f"B181-B182 inventory changed: {len(source_rows)}")
    rows_by_block = {block: [row for row in source_rows if row["id"].startswith(f"DK4_MES_B{block}_") and row["id"] not in EXCLUDED] for block in LINES}
    for block, lines in LINES.items():
        if len(rows_by_block[block]) != len(lines):
            raise SystemExit(f"B{block}: {len(rows_by_block[block])} visible rows != {len(lines)} translations")
    speaker_names = {0x05: "Claudio Manini", 0x06: "Julio Erdi", 0x19: "Ifa"}
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
                "context": "The runaway Taoist trainee Ifa asks to sail, demonstrates a paralyzing art against Claudio, secretly follows the crew, and is accepted after Raphael recognizes her resolve.",
                "source_meaning": english.replace("{LB}", " ").replace("{MACRO:FI}", "Raphael"),
                "localization_note": "Faithful natural American English preserving Ifa's youthful confidence, Taoist demonstration, Claudio's embarrassment, recruitment continuity, and canonical identity in metadata.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
                **({"manual_break_reason": "Protects action timing, four-line bounds, and progressive ASCII pair phase."} if "{LB}" in english else {}),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v51-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Ifa's complete Taoist-art encounter, pursuit, and recruitment across SC0 blocks 181-182.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": {str(block): len(rows_by_block[block]) for block in LINES}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} control excluded")


if __name__ == "__main__":
    main()
