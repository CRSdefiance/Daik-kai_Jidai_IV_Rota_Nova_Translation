from __future__ import annotations

import csv
import json

from scripts.materialize_lil_deep_route_v107 import ROOT, SC2_SHA256

LINES = {
    (299, 20): "We'll get lost without a map.",
    (299, 21): "We'll get lost without a map.",
    (299, 22): "We can't go on without a map!",
    (299, 23): "We'll get lost without a map!",
    (299, 24): "No map? We'll get lost, Admiral!",
    (299, 25): "Admiral, no map means getting lost.",
    (299, 26): "Admiral, we need a map to go on!",
    (299, 27): "We'll get lost without a map.",
    (299, 40): "Ugh. Why come here? Looks full of bugs and snakes...",
    (299, 51): "We'll be fine... Probably.",
    (299, 57): "Admiral! Look!",
    (299, 61): "Eek! A g-giant snake!!",
    (299, 78): "W-what now?",
    (299, 80): "Hmm... What now, Admiral?",
    (299, 81): "Whoa! A-Admiral, what now?",
    (299, 82): "Eek! A-Admiral, what now?",
    (299, 83): "What now, Admiral?",
    (299, 85): "What now, Admiral?",
    (299, 87): "Whoa, scary! What do we do?!",
    (299, 88): "Hmm... What now, Admiral?",
    (299, 93): "No time to freeze up! What now?",
    (299, 101): "Hit",
    (299, 103): "Run",
    (299, 110): "But don't make me fight it! You all kill it! Snakes really scare me!",
    (299, 114): "Got it!",
    (299, 122): "Did you kill it?",
    (299, 139): "Safe now. The snake fled into the forest.",
    (299, 140): "Safe; it fled into the forest.",
    (299, 141): "Yes, it fled into the forest.",
    (299, 142): "Safe now; it fled deep into the forest!",
    (299, 143): "Yeah, it fled that way.",
    (299, 145): "Deep in the forest now. No worries.",
    (299, 146): "Yep, it ran off somewhere!",
    (299, 147): "Seems it fled into the forest. No worries.",
    (299, 152): "Yes, it fled deep into the forest.",
    (299, 161): "Some sailors were injured.",
    (299, 166): "Of course! We're running!",
    (299, 175): "Admiral, wait for us!",
    (299, 181): "Wait, {MACRO:FI}! Everyone, we're leaving! Stay close to me!",
    (299, 189): "Phew, safe... Oh! Everyone all right?",
    (299, 204): "Cruel, Admiral. Warn us before running!",
    (299, 205): "Cruel, Admiral! Running off like that...",
    (299, 206): "How cruel! You ran without warning! We had a hard time!",
    (299, 208): "Cruel, Admiral! Warn us before running!",
    (299, 209): "Hey, Admiral! Warn us before running off!",
    (299, 210): "You bolted! We had a hard time, Admiral! What were you thinking...?",
    (299, 212): "How cruel, Admiral! You ran without warning! So awful!",
    (299, 214): "Cruel, Admiral! You must warn us before running!",
    (299, 220): "T-that's cruel, {MACRO:FI}! You just ran off!",
    (299, 226): "Oh, sorry, sorry! Just can't stand snakes!",
    (299, 229): "Glad everyone's safe. Let's set off again!",
    (299, 235): "H-huh? Oh no! Can't get out! Help!",
    (299, 250): "Stay still! Might be a bottomless bog! We'll save you!",
    (299, 252): "We'll save you! Might be a bottomless bog!",
    (299, 253): "Admiral, all right?! Stay still! We'll help!",
    (299, 254): "Could be a bottomless bog! Don't move!",
    (299, 255): "Admiral, could be a bottomless bog! Hold on! We'll help!",
    (299, 256): "Could be a bottomless bog! Hang on, Admiral!",
    (299, 257): "Whoa, Admiral!",
    (299, 259): "Maybe a bottomless bog! This is bad!",
    (299, 264): "{MACRO:FI}!! Don't move! Might be a bottomless bog! We'll save you!",
    (299, 290): "Hang on! Are you all right?!",
    (299, 291): "Admiral, stay awake!",
    (299, 292): "Admiral, you're safe!",
    (299, 294): "Admiral! You're saved! Safe now!",
    (299, 295): "Are you all right?",
    (299, 297): "Admiral, all right?",
    (299, 299): "Admiral, stay with us!",
    (299, 301): "Admiral, hang on! You're safe!",
    (299, 306): "{MACRO:FI}, {MACRO:FI}! Stay with us!",
    (299, 312): "U-ugh... Huh... Safe now...?",
    (299, 330): "That was close...",
    (299, 332): "That was close...",
    (299, 334): "That was pretty close, really!",
    (299, 335): "Safe now, but it was close.",
    (299, 336): "A close call!",
    (299, 338): "A close call.",
    (299, 340): "That was close!",
    (299, 342): "Thank goodness! That was very close.",
    (299, 347): "Yes, barely.",
    (299, 375): "Admiral, all right?",
    (299, 377): "Okay?",
    (299, 379): "You okay?",
    (299, 381): "Admiral, okay?!",
    (299, 383): "All right?",
    (299, 385): "Admiral, all right? Hurt anywhere?",
    (299, 386): "How do you feel?",
    (299, 392): "{MACRO:FI}, okay? Glad you're safe.",
    (299, 399): "Ugh! Had enough! Covered in mud!",
    (299, 405): "The sailors seem fatigued.",
    (299, 422): "Look ahead...!",
    (299, 424): "Look ahead!!",
    (299, 426): "L-look there...",
    (299, 428): "Look there!",
    (299, 430): "Admiral, look!",
    (299, 432): "Admiral, there!",
    (299, 434): "Oh...!",
    (300, 6): "Oh, {MACRO:FI}! Good timing.",
    (300, 9): "Do you know the Colosseum?",
    (300, 13): "Colosseum?",
    (300, 17): "Roman ruins. Heard you seek ruins, so thought you'd like to know.",
    (300, 21): "Really? Thanks! Yes, let's visit!",
    (300, 24): "Take care. Don't forget to buy a map.",
}
STATES = {0x02, 0x09, 0x97, 0xC0, 0xCF, 0xD0, 0xD3, 0xFE}
EXCLUDED = {"DK4_MES_B299_R0038": "Packed jungle event 05 60 60 46 8B 80 3E 63, identical SC0 B310 R0038, SC1 B300 R0038 and SC3 B267 R0037; preserve unchanged."}


def main() -> None:
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {i for i in source if 299 <= int(i.split("_B")[1].split("_")[0]) <= 300}
    assert expected == {f"DK4_MES_B{b}_R{n:04d}" for b, n in LINES} | set(EXCLUDED)
    records = []
    for (b, n), text in LINES.items():
        row_id = f"DK4_MES_B{b}_R{n:04d}"
        raw = bytes.fromhex(source[row_id]["source_hex"])
        has_state = raw[0] in STATES
        prose = text
        for macro in ("FI", "FA", "FO"):
            assert raw.count(macro.encode()) == text.count(f"{{MACRO:{macro}}}"), row_id
            prose = prose.replace(f"{{MACRO:{macro}}}", "")
        assert "I" not in prose and "F" not in prose, row_id
        records.append({"id": row_id, "english": (f"{{SPEAKER:{raw[0]:02X}}}" if has_state else "") + text + "{PAD}", "speaker": {2: "Lil", 9: "Kamil", 0xC0: "Tavern hostess", 0xCF: "Companion", 0xFE: "System"}.get(raw[0], "Companion variant"), "context": "Complete giant-snake fight/flee encounter, bottomless-bog rescue and Colosseum map lead; all companion variants.", "source_meaning": text, "source_japanese": raw[1 if has_state else 0:].decode("shift_jis", errors="replace"), "localization_note": "Natural source-reviewed English retains fight/run choices, snake's forest retreat, injuries, Lil's fear and premature flight, every rescue/check-in response, sailor fatigue and map hint. Bare text retains first glyph; state 97 retained.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
    batch = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-v112-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "Complete B299-B300 snake and bog encounter.", "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {str(b): sum(bb == b for bb, _ in LINES) for b in (299, 300)}}, "excluded_records": EXCLUDED, "records": records}
    (ROOT / "translations/lil_deep_route_v112.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote Lil V112: {len(records)} records")


if __name__ == "__main__":
    main()
