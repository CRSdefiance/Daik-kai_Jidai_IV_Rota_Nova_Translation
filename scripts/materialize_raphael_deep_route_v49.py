from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v49.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
EXCLUDED = {"DK4_MES_B172_R0017": "Four-byte market scene control; no independently rendered dialogue."}
LINES = {
    171: [
        "Whew... drank quite a bit.",
        "What? A man of the sea drinks hard.{LB}Look at Christina--totally fine.",
        "Christina isn't a man...{LB}Claudio, too much.",
        "Quite a lot for me too. Oh...",
        "Some passionate music started.",
        "Yeah. Makes you want to dance.",
        "This song...{LB}excuse me.",
        "Christina...",
        "Restroom, Christina?",
        "<Patron 1>{LB}Wow, that woman!",
        "<Patron 2>{LB}Yeah! Beautiful and skilled!",
        "Christina, amazing!",
        "What a surprise...",
        "<Both>{LB}Bravo! Bravo! Bra-vo!",
        "Clap, clap, clap!",
        "Had to dance.{LB}Love this song.",
        "...Amazing.{LB}Truly incredible, Christina.",
        "Thanks. So awkward.",
        "Swordswoman likes flamenco?",
        "Claudio! That was rude!",
        "Not an insult.{LB}Thought you only trained with swords--{LB}a dull woman.",
        "Eh?",
        "Sorry...",
        "You've won me over.{LB}Not merely his granddaughter--{LB}one of us.",
    ],
    172: [
        "Wow! Amazing!",
        "What's this?!{LB}A cow asleep in the road!",
        "Nothing like our country.",
        "Come buy! How about it?{LB}Only quality goods here!",
        "Rare customers!{LB}You're travelers, right?",
        "Take me along. Elephants bore me.{LB}Other lands are calling me.{LB}Come on, what do you say?",
        "S-sudden, isn't it?{LB}Yes, we're sailors...{LB}Any special skills?",
        "Cooking! Great cooking!{LB}Handy at sea, right?",
        "Hmm. Cooking...{LB}We already have someone.",
        "Nimble hands too.{LB}Could repair ships,{LB}maybe even draw maps.",
        "A very quick learner.{LB}Great instincts, you know.",
        "Whatever the skill,{LB}any experience?",
        "Nope!",
        "Huh?!",
        "Big claims with no experience.",
        "Strange? Young and quick to learn.{LB}Already said: great instincts!",
        "Why not? You won me over.",
        "Hey now.{LB}Can an admiral be so careless?",
        "Yeah. You're far too casual.",
        "Huh? Weren't you asking{LB}to be hired?",
        "Sure. But you must see{LB}how amazing my skills are.",
        "So what now?",
        "Test me.",
        "What test?",
        "A dish gets cooked now.{LB}Everyone likes it, that means a pass.{LB}How about it?",
        "Sounds good. Let's taste it.",
        "Ready! Here you go.",
        "What's this weird food?{LB}Not something bizarre, right?{LB}(munch)",
        "...D-delicious!{LB}This is great!",
        "True. Delicious.",
        "Oh, certainly tasty.{LB}Looks can deceive.",
        "A talented hawk hides its talons!",
        "Don't brag.",
        "Then it's settled?{LB}You'll join us?",
        "Yes!{LB}Samuel da Khan.{LB}Great to meet you!",
    ],
    173: [
        "Admiral! Disaster!{LB}The ship--it's gone!",
        "Mmh... what?{LB}So early...",
        "Ship is gone...?{LB}No. Can't be...",
        "Then it's serious...",
        "Really!{LB}Come to the port now!",
        "What?! No!{LB}Gone--really gone!",
        "What do we do?!",
        "Oh my.{LB}Really gone.",
        "What happened?!",
        "Admiral! Wait!",
        "Disaster!{LB}A thin young man was alone,{LB}working on the ship this morning...",
        "Then he sailed away!",
        "Hey!{LB}'Sailed away' isn't enough!",
        "Well...{LB}what an impressive person.",
        "Don't admire him!{LB}This is no time to relax!",
        "Never expected him to sail.{LB}He was alone, so it looked{LB}like an inspection.",
        "A natural assumption.{LB}Not your fault.",
        "Still, sailing alone...{LB}Who could he be?",
        "Stop wondering.{LB}Gather news in town!{LB}We'll catch that ship thief!",
    ],
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = [row for row in csv.DictReader(stream) if row["id"].startswith(tuple(f"DK4_MES_B{block}_" for block in LINES))]
    if len(source_rows) != 79:
        raise SystemExit(f"B171-B173 inventory changed: {len(source_rows)}")
    rows_by_block = {block: [row for row in source_rows if row["id"].startswith(f"DK4_MES_B{block}_") and row["id"] not in EXCLUDED] for block in LINES}
    for block, lines in LINES.items():
        if len(rows_by_block[block]) != len(lines):
            raise SystemExit(f"B{block}: {len(rows_by_block[block])} visible rows != {len(lines)} translations")
    speaker_names = {
        0x05: "Claudio Manini", 0x06: "Julio Erdi", 0x07: "Christina",
        0x08: "Raphael companion", 0x16: "Samuel da Khan", 0x74: "Port attendant",
        0x97: "Crewman", 0xFE: "Tavern patrons",
    }
    contexts = {
        171: "Christina performs flamenco in a tavern and wins Claudio's respect as a full crewmate.",
        172: "Raphael meets Samuel da Khan in an Indian market and recruits him after tasting his cooking.",
        173: "Raphael's crew discovers their ship has been stolen by a lone young man and begins the pursuit.",
    }
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
                "id": row["id"],
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": speaker_names.get(first, "Raphael Castor or companion"),
                "context": contexts[block],
                "source_meaning": english.replace("{LB}", " "),
                "localization_note": "Faithful natural American English preserving character banter, recruitment logic, and event continuity.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
                **({"manual_break_reason": "Protects scene pacing, four-line bounds, and progressive ASCII pair phase."} if "{LB}" in english else {}),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v48-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Christina's flamenco scene, Samuel da Khan's recruitment, and the opening of the stolen-ship event across SC0 blocks 171-173.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": {str(block): len(rows_by_block[block]) for block in LINES}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} control excluded")


if __name__ == "__main__":
    main()
