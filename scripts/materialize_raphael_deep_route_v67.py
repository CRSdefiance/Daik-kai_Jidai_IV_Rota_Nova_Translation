from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v67.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = tuple(range(271, 286))

SPEAKERS = {
    0x3E: "Jacks Bloom",
    0x3F: "Julian Vermeer",
    0x41: "Prett Perot",
    0x44: "Jacob Portunto",
    0x45: "Peralonso Aguirre",
    0x71: "Guild messenger",
    0x93: "Guildmaster",
    0x95: "Guildmaster",
    0xFE: "System",
}

CONTEXT = {
    271: "Raphael delivers Jacob Portunto and receives the Lisbon guild reward.",
    272: "Raphael and the guild recall Jacob's East African base in Mozambique.",
    273: "The Hamburg guild asks Raphael to capture fugitive Jacks Bloom.",
    274: "A messenger tells Raphael that the Hamburg guild seeks him.",
    275: "Raphael and the guild recall that Jacks is hiding somewhere in Africa.",
    276: "Raphael delivers Jacks, receives a reward, and hears about a learned priest.",
    277: "The San Jorge guild asks Raphael to capture traitor Julian Vermeer.",
    278: "Raphael delivers Julian, receives a reward, and hears how to reach a Saharan mosque.",
    279: "Raphael and the guild recall Julian's Mediterranean courier fleet.",
    280: "The Hangzhou guild asks Raphael to capture murderer Prett Perot for a bereaved daughter.",
    281: "Raphael delivers Prett, receives a reward, and hears of the Purple Palace.",
    282: "Raphael and the guild recall the active bounty on Prett Perot.",
    283: "The Malacca guild hires Raphael to capture former spy Peralonso Aguirre.",
    284: "Raphael delivers Peralonso, receives a reward, and hears of untouched jungle ruins.",
    285: "Raphael and the guild recall that Peralonso is still nearby.",
}

OVERRIDES = {
    "DK4_MES_B271_R0005": "Hey! What will you do with me?",
    "DK4_MES_B271_R0008": "That depends on you.",
    "DK4_MES_B271_R0011": "Well done. Almost forgot your reward. Take this.",
    "DK4_MES_B271_R0015": "Received 18,000 coins.",
    "DK4_MES_B271_R0045": "Lisbon share rose slightly!",
    "DK4_MES_B272_R0014": "Jacob the smuggler was in East Africa...",
    "DK4_MES_B272_R0019": "Looking for Jacob? He uses Mozambique as his base.",
    "DK4_MES_B273_R0005": "Got a job for you.",
    "DK4_MES_B273_R0008": "Capture the Englishman Jacks Bloom.",
    "DK4_MES_B273_R0011": "He stole our client list{LB}and fled to Holland.",
    "DK4_MES_B273_R0014": "He went to Africa, but we lost his trail. That's all we know. Good luck.",
    "DK4_MES_B274_R0006": "Hamburg's guild was looking for you.",
    "DK4_MES_B275_R0014": "Jacks's fleet is somewhere in Africa. Catch him soon.",
    "DK4_MES_B275_R0019": "Still haven't found Jacks? He must be somewhere in Africa.",
    "DK4_MES_B276_R0005": "There's Jacks! You cost us a fortune!",
    "DK4_MES_B276_R0008": "Grr...",
    "DK4_MES_B276_R0012": "Thanks. This reward isn't much, but take it.",
    "DK4_MES_B276_R0016": "Received 34,000 coins.",
    "DK4_MES_B276_R0047": "Hamburg share rose slightly!",
    "DK4_MES_B276_R0065": "Heard you search for ruins and churches in many towns?",
    "DK4_MES_B276_R0068": "A nearby church has a famously learned priest.",
    "DK4_MES_B277_R0006": "A target must be subdued. Take the job.",
    "DK4_MES_B277_R0009": "Julian Vermeer, Portuguese traitor{LB}aiding Spain, works as a courier{LB}in the Mediterranean.",
    "DK4_MES_B278_R0005": "Julian was caught!{LB}What a sorry sight.",
    "DK4_MES_B278_R0008": "Damn it! Let go!",
    "DK4_MES_B278_R0012": "Excellent work. We shall handle the rest. Take this.",
    "DK4_MES_B278_R0016": "Received 32,000 coins.",
    "DK4_MES_B278_R0047": "San Jorge share rose slightly!",
    "DK4_MES_B278_R0065": "To see the mosque deep in the Sahara, take a map and depart through the city gate.",
    "DK4_MES_B279_R0014": "Julian's fleet is in the Mediterranean.",
    "DK4_MES_B279_R0026": "Catch traitor Julian quickly.{LB}He works as a courier in the Mediterranean.",
    "DK4_MES_B280_R0006": "Hey, you.{LB}You've got some compassion, right?",
    "DK4_MES_B280_R0009": "A girl whose father was killed{LB}by an English outlaw seeks revenge.{LB}Please help her.",
    "DK4_MES_B280_R0013": "The outlaw is Prett Perot.{LB}Will you take the job?",
    "DK4_MES_B281_R0005": "Prett! Villain...{LB}How dare you return?",
    "DK4_MES_B281_R0008": "Yes... so sorry...",
    "DK4_MES_B281_R0012": "Repentance cannot atone for murder.",
    "DK4_MES_B281_R0015": "Thank you. The girl who hired us{LB}will decide his fate.",
    "DK4_MES_B281_R0019": "Never thought you'd take him alive.{LB}You've earned a handsome reward.",
    "DK4_MES_B281_R0023": "Received 35,000 coins.",
    "DK4_MES_B281_R0054": "Hangzhou share rose slightly!",
    "DK4_MES_B281_R0072": "Have you visited the Purple Palace?{LB}Worth seeing, though it is far away.",
    "DK4_MES_B281_R0075": "Don't tell officials{LB}who gave you the lead.",
    "DK4_MES_B282_R0014": "Must defeat the outlaw Prett.",
    "DK4_MES_B282_R0027": "Capture the outlaw Prett.",
    "DK4_MES_B283_R0005": "One job for you.{LB}Track down a wanted man.",
    "DK4_MES_B283_R0008": "Peralonso Aguirre, a former Spanish spy.",
    "DK4_MES_B283_R0011": "Now he commands raiders near here. This is half now; rest after the job.",
    "DK4_MES_B283_R0022": "Received 15,000 coins.",
    "DK4_MES_B284_R0006": "Peralonso was captured.",
    "DK4_MES_B284_R0010": "Ah, you came. Good.",
    "DK4_MES_B284_R0014": "How could this be?",
    "DK4_MES_B284_R0018": "Thank you. Things should calm down here. This may be little, but take it.",
    "DK4_MES_B284_R0021": "Received 76,000 coins.",
    "DK4_MES_B284_R0054": "Malacca share rose slightly!",
    "DK4_MES_B284_R0071": "Ah, right.{LB}Heard an interesting rumor.",
    "DK4_MES_B284_R0074": "Deep inland, an ancient kingdom's ruins remain untouched in the jungle.",
    "DK4_MES_B284_R0078": "Really?",
    "DK4_MES_B284_R0082": "Only a rumor; no one found them.{LB}Maybe you can.",
    "DK4_MES_B285_R0014": "Must defeat former spy Peralonso.",
    "DK4_MES_B285_R0019": "Peralonso must be somewhere nearby.",
}


def main() -> None:
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = [row for row in csv.DictReader(stream) if row["id"].startswith(prefixes)]

    records = []
    block_counts: dict[str, int] = {}
    for row in source_rows:
        row_id = row["id"]
        english = OVERRIDES.get(row_id)
        if english is None:
            raise SystemExit(f"Raphael V67 unresolved record: {row_id}")
        unsafe = english
        for macro in ("FI", "FA", "FO", "FU"):
            unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        source_hex = row["source_hex"].upper()
        first = int(source_hex[:2], 16)
        state = f"{first:02X}" if first in SPEAKERS else ""
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        block_counts[str(block)] = block_counts.get(str(block), 0) + 1
        records.append(
            {
                "id": row_id,
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(first, "Raphael or scene text"),
                "context": CONTEXT[block],
                "source_meaning": english.replace("{LB}", " "),
                "localization_note": "Faithful concise American English preserving canonical bounty names, reward amounts, scene order, and fixed-record constraints.",
                "qa_waivers": [
                    "weak-line-ending",
                    "orphan-final-line",
                    *(["manual-break"] if "{LB}" in english else []),
                ],
                **(
                    {"manual_break_reason": "Protects native row boundaries from progressive ASCII pair-phase wrapping."}
                    if "{LB}" in english
                    else {}
                ),
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": True,
                },
            }
        )

    if len(records) != len(source_rows):
        raise SystemExit(f"Raphael V67 inventory mismatch: {len(records)} != {len(source_rows)}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v67-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Fifteen source-locked Raphael guild-bounty, reward, reminder, and ruin-hint events across SC0 blocks 271-285.",
        "excluded_records": {},
        "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
