from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v74.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    (173, 6): ("Lil seeks someone who knows the Golden Crown of Silla.", "Anyone here know about the Golden Crown of Silla?"),
    (173, 9): ("A Seoul tavernkeeper welcomes Lil.", "Welcome!"),
    (173, 13): ("Lil asks the tavernkeeper about the crown.", "Say, ever heard of the Golden Crown of Silla?"),
    (173, 17): ("The tavernkeeper has heard of it and asks why.", "Yes, a little. Why do you ask?"),
    (173, 20): ("Lil wants to find the beautiful crown.", "That's the one! Heard it's beautiful."),
    (173, 24): ("The tavernkeeper says a man just asked the same question.", "Yes, it's lovely. Odd... A man just asked about it too."),
    (173, 28): ("Lil suspects the man was Julian.", "What?! Was his name Julian?"),
    (173, 32): ("The tavernkeeper recalls a smooth talker going to King Muryeong's Tomb.", "Smooth talker. Name escapes me. Off to King Muryeong's Tomb."),
    (173, 36): ("Lil repeats the tomb's name.", "That tomb?"),
    (173, 40): ("The tavernkeeper says the crown is rumored to lie in the nearby ruins.", "The crown lies in some nearby ruins."),
    (173, 44): ("Lil resolves to beat Julian to the tomb.", "Julian's ahead! Gotta beat him!"),
    (174, 6): ("Julian thanks Lil for helping him obtain the crown.", "Ah, you! Thanks again."),
    (174, 10): ("Mihwa asks whether Julian knows Lil.", "You know her?"),
    (174, 14): ("Julian says Lil found the crown first and yielded it to him.", "She found the crown first, Mihwa, then gave it to me."),
    (174, 18): ("Mihwa admires the crown's dignified beauty.", "What lovely gold... So elegant!"),
    (174, 22): ("Julian presents the crown as promised.", "As promised, it's yours!"),
    (174, 26): ("Mihwa promises to treasure the crown.", "Lovely! A lifelong treasure!"),
    (174, 30): ("Lil is glad for Mihwa.", "Good for you."),
    (174, 34): ("Julian asks how Lil reached the tomb so quickly.", "Thanks to you. How did you reach King Muryeong's Tomb so fast?"),
    (174, 38): ("Lil boasts about her adventuring experience.", "More experience, that's all."),
    (174, 42): ("Julian praises Lil as charming and reliable.", "An adventurer? Charming and dependable too!"),
    (174, 46): ("Lil explains she sails and trades rather than adventuring.", "Not adventurers. We sail and trade."),
    (174, 50): ("Julian realizes Lil sailed to Seoul.", "Ah! You sailed here. Of course!"),
    (174, 54): ("Julian says he ran to Seoul, collapsed, and was overtaken.", "Ran all the way to Seoul. After hearing the lead, collapsed! You passed me while resting..."),
    (174, 57): ("Lil doubts Julian ran all the way.", "You ran to Seoul? Seriously?!"),
    (174, 69): ("Emilio imagines running that far and getting hungry.", "All that running makes me hungry..."),
    (174, 75): ("Julian sees fate in his trip and meeting Lil.", "Seoul was destiny! Meeting someone as wonderful as you proves it!"),
    (174, 78): ("Lil thinks Julian has started flirting again.", "(There he goes again...)"),
    (174, 81): ("Julian asks Lil to take him along on her voyage.", "Take me along! Show me the world!"),
    (174, 84): ("Lil asks what Julian hopes to do abroad.", "Really? What would you do out there?"),
    (174, 87): ("Julian wants to see the world like his sailor grandfather.", "Grandpa sailed the world. Been dreaming of that since childhood!"),
    (174, 91): ("Julian wants to become an adventurer like his grandfather.", "To be an adventurer like Grandpa!"),
    (174, 94): ("Lil asks whether Julian learned navigation from his grandfather.", "So Grandpa sailed. You know navigation, then?"),
    (174, 98): ("Julian assures Lil he will be useful.", "Sure! You can count on me."),
    (174, 102): ("Lil lets Julian join the crew.", "All right. Come along."),
    (174, 106): ("Julian celebrates sailing with charming Lil.", "To sail beside someone so lovely... what luck!"),
    (174, 110): ("Lil threatens to toss Julian overboard if he keeps flirting.", "Say one more word and you're overboard!"),
    (174, 113): ("Mihwa asks Julian what will happen to her.", "Julian? What about me?"),
    (174, 116): ("Julian realizes Mihwa heard him.", "Mihwa..."),
    (174, 120): ("Mihwa rebukes Julian for flirting with another woman before her.", "You hit on her in front of me? Go see the world!"),
    (174, 124): ("Julian says Lil is only his new employer and asks Mihwa not to sulk.", "Mihwa, don't be jealous! She's my new captain. Come on, smile."),
    (174, 128): ("Julian promises to return with a better gift and asks for a date.", "When we find a finer gift, we'll come back for a date!"),
    (174, 132): ("Mihwa agrees to wait for Julian's return.", "Promise? You'll have me waiting!"),
    (174, 135): ("Lil privately wonders whether Julian has hidden potential.", "(He could be special...)"),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x0E: "Emilio", 0x1A: "Julian",
    0xC9: "Mihwa", 0xCA: "Seoul tavernkeeper",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {
        row_id for row_id in source_rows
        if row_id.startswith(("DK4_MES_B173_", "DK4_MES_B174_"))
    }
    authored = {f"DK4_MES_B{block}_R{number:04d}" for block, number in LINES}
    if authored != expected:
        raise ValueError(f"B173-B174 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for (block, number), (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B{block}_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": (
                "Lil follows the Golden Crown of Silla lead to King Muryeong's Tomb, "
                "then helps Julian give the crown to Mihwa before he joins her crew."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B173-B174 Japanese. Source "
                "presentation leads retain their control behavior. Literal "
                "uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v74-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 44 B173-B174 Golden Crown search and Julian recruitment records.",
        "inventory": {"identified_records": 44, "translated_records": 44, "blocks": {"173": 11, "174": 33}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
