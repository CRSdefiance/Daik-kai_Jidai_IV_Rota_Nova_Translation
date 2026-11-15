from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v101.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
BLOCKS = range(207, 215)
LINES = {
    (207, 5): "Admiral! Got my eye on a weapon!",
    (207, 8): "Eh?",
    (207, 12): "Wanna get stronger, so a weapon would help!",
    (207, 15): "You mean a weapon, not a snack? Kidding! What's its name?",
    (207, 19): "The Minotaur's Axe!",
    (207, 23): "What a name! Must be huge. You may be the only one who could use it. Where is it?",
    (207, 26): "A Minotaur lived here long ago. That's all the rumor says.",
    (207, 30): "Hmm. Maybe we'll look sometime.",
    (207, 33): "Hooray!",
    (207, 37): "Maybe, remember?",
    (207, 41): "Still, hooray!",
    (207, 45): "And it may not be yours to keep.",
    (207, 48): "Aw.",
    (208, 5): "You there! Got a moment?",
    (208, 9): "Me?",
    (208, 13): "Yes, you.",
    (208, 17): "What?",
    (208, 21): "You remind me of a fierce woman pirate from long ago.",
    (208, 25): "Do we look alike? Our faces?",
    (208, 28): "Not your face. Your manner... You both look strong.",
    (208, 32): "So you think so? Time to get stronger, just like her!",
    (208, 36): "Want strength? Seek the treasure sword that pirate used.",
    (208, 40): "Her sword?",
    (208, 44): "Yes, the sword she used. Can't say how much it's worth, though.",
    (208, 48): "Sounds interesting. Where is it?",
    (208, 51): "Caribbean.",
    (208, 55): "Caribbean",
    (208, 59): "She lost it during a great naval battle in the Caribbean.",
    (208, 62): "And?",
    (208, 66): "That's all.",
    (208, 70): "That's all? So how do we find it?",
    (208, 73): "No clue. You might just find it.",
    (208, 76): "Well, good to know.",
    (208, 79): "You'll find it. Good luck!",
    (208, 82): "Thanks!",
    (208, 86): "(A pirate's lost Caribbean sword... Worth a look.)",
    (208, 90): "Cristina: Charm +1!",
    (209, 14): "Admiral, a letter from Yukihisa.",
    (209, 15): "Admiral, a letter from Yukihisa.",
    (209, 16): "Admiral, a letter from Yukihisa.",
    (209, 17): "Admiral, a letter from Yukihisa.",
    (209, 18): "Admiral, a letter from Yukihisa.",
    (209, 19): "Admiral, a letter from Yukihisa.",
    (209, 20): "Admiral! A letter from Yukihisa!",
    (209, 27): "Muramasa is a legendary cursed sword. Tokugawa, ruler of Japan, fears the blades and seeks their destruction.",
    (209, 30): "A clan bearing a grudge against Tokugawa has hidden one somewhere in East Asia. This letter brings you that news.",
    (209, 33): "My long-sought treasure, beyond doubt. -- Yukihisa Genjo Shiraki",
    (209, 53): "Hard to read. That's Yukihisa.",
    (209, 54): "Hard to read. That's Yukihisa.",
    (209, 55): "Hard to read. That's Yukihisa.",
    (209, 56): "Hard to read. That's Yukihisa.",
    (209, 57): "What a wordy letter. Typical Yukihisa.",
    (209, 58): "Hard to read. That's Yukihisa.",
    (209, 59): "Too hard! What's it even saying?",
    (209, 60): "Hard to read. That's Yukihisa.",
    (209, 65): "What a wordy letter. Typical Yukihisa.",
    (209, 71): "Hmm. Sounds fun. Let's look for it.",
    (210, 5): "Admiral, listen! Got a good lead!",
    (210, 8): "A local lord has a sword sharp enough to cut anything.",
    (210, 11): "Hmm.",
    (210, 15): "The faintly red blade looks steeped in its victims' blood.",
    (210, 19): "A reddish blade...",
    (210, 23): "The lord found it creepy and locked it away unused. What a coward!",
    (210, 26): "Creepy, sure... But what a waste.",
    (210, 29): "What a fool! Why buy a sword?",
    (210, 33): "Why not sell it? Any word on its hiding place?",
    (210, 36): "No word on the location. Let's search when we can.",
    (211, 5): "Lovely square... Hm? What's that down in the pond?",
    (211, 9): "Honk!",
    (211, 13): "Two swans! Even here! Are you traveling together?",
    (211, 17): "Honk! Cluck... cluck... honk!",
    (211, 21): "Hehe. So close. Lucky you.",
    (211, 24): "flap, flap!",
    (211, 28): "Oh! Where to? They're carrying something!",
    (211, 32): "That way...",
    (211, 36): "Cristina! What are you doing?",
    (211, 39): "Oh, {MACRO:FI}! There were two swans here.",
    (211, 42): "Really? Wish we'd seen them!",
    (211, 45): "They carried a long, shiny thing toward Amsterdam. Let's go look.",
    (212, 5): "Hello! Know Romance of the Three Kingdoms?",
    (212, 10): "Yes",
    (212, 12): "No",
    (212, 22): "Try reading it sometime. Great fun!",
    (212, 32): "Oh, good! Glad to hear it. Who's your favorite warrior?",
    (212, 39): "Zhao",
    (212, 41): "Guan",
    (212, 43): "Zhuge",
    (212, 51): "Same as me! We'll get along!",
    (212, 54): "He rides through Cao Cao's army, baby Adou in his arms!",
    (212, 58): "Rumor says a legendary spear Zhao Yun used is somewhere on the nearby peninsula.",
    (212, 62): "My search took ages, with no luck. Maybe you could succeed where my search failed.",
    (212, 78): "Zhuge Liang... Yes, his memorial on the expedition moves me to tears. My second favorite!",
    (213, 5): "Excuse me.",
    (213, 9): "Me?",
    (213, 13): "Could you let me see that?",
    (213, 16): "At what?",
    (213, 20): "That.",
    (213, 24): "Just as the tale says. No doubt.",
    (213, 31): "Emperor Kublai Khan ruled this continent over 300 years ago.",
    (213, 35): "But even he had to face death...",
    (213, 38): "'A sea conqueror shall come in 200 years,' he told his servant.",
    (213, 42): "'He rules many foreigners and bears a gold seal from a land beyond my rule. To that hero, give my sword.'",
    (213, 45): "We are his heirs. Our clan awaited the sea king.",
    (213, 48): "And today, at last, you have come. Conqueror of the seas, we have awaited you.",
    (213, 52): "Please! Just a merchant, that's all.",
    (213, 63): "Exactly! {MACRO:FI}, a conqueror foretold 300 years ago?",
    (213, 69): "No, my eyes do not deceive me. You are the sea king.",
    (213, 72): "South of Shandong Peninsula you'll find his great sword.",
    (213, 75): "The great sword is yours. Goodbye.",
    (214, 14): "Admiral, a letter from Janus.",
    (214, 16): "Admiral, a letter from Janus.",
    (214, 18): "Admiral, a letter from Janus.",
    (214, 20): "A letter from Janus.",
    (214, 22): "Admiral, a letter from Janus.",
    (214, 24): "Admiral, a letter from Janus.",
    (214, 26): "Admiral! A letter from Janus!",
    (214, 34): "This letter comes from a road leading into Rome.",
    (214, 38): "This road is rich in tales of early missionaries who braved persecution to spread their faith.",
    (214, 41): "Religion holds no appeal. One tale, though, caught my ear.",
    (214, 44): "Judas, one of Jesus' twelve disciples, had a sword. They say it lies in a place linked to him.",
    (214, 48): "Judas betrayed Jesus. His sword's history frightens people away.",
    (214, 51): "Yet it is said to be a splendid sword with a keen edge. The blade itself is blameless. Surely it's worth a search.",
    (214, 62): "Manuel is devout. This tale might upset him.",
    (214, 68): "Should more news reach me, another letter will follow. -- Janus Pasha",
    (214, 75): "Judas' sword... Janus cares about the blade, not its owner's betrayal. Typical!",
    (214, 87): "No firm objection here. Judas repented in the end, so the choice is yours, Admiral.",
}
EXCLUDED = {"DK4_MES_B213_R0022": "Packed item payload 21 48 96 A8; identical to Maria SC3 B186 R0021's verified nontext sword-legend payload; unchanged."}
BARE = {(209, n) for n in (15, 16, 17, 18, 19, 20, 54, 55, 56, 57, 58, 59, 60)} | {
    (212, 10), (212, 12), (212, 39), (212, 41), (212, 43),
    (214, 16), (214, 18), (214, 20), (214, 22), (214, 24), (214, 26),
}
SPEAKERS = {0x02: "Lil", 0x04: "Janus's letter", 0x07: "Cristina", 0x09: "Kamil", 0x0B: "Jam", 0x0C: "Yukihisa's letter", 0x0E: "Emilio", 0x11: "Al", 0x17: "Manuel", 0x95: "Book enthusiast", 0xAA: "Old man", 0xD0: "Companion report", 0xFE: "Sound effect or stat notice"}
CONTEXT = {
    207: "Emilio asks Lil to seek the Minotaur's Axe.",
    208: "Cristina hears about a woman pirate's lost Caribbean treasure sword.",
    209: "Yukihisa's Muramasa letter, all companion delivery and reaction variants, and Lil's response.",
    210: "Al tells Lil about a local lord's blood-red sword.",
    211: "Cristina watches swans carry a shining object toward Amsterdam.",
    212: "Three Kingdoms enthusiast, every choice, and Zhao Yun's spear rumor.",
    213: "Kublai Khan's prophecy and the Sea King's sword south of Shandong.",
    214: "Janus's Judas-sword letter, every delivery variant, and Manuel's response.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {i for i in source_rows if int(i.split("_B")[1].split("_")[0]) in BLOCKS}
    authored = {f"DK4_MES_B{b}_R{n:04d}" for b, n in LINES}
    if authored | EXCLUDED.keys() != expected or authored & EXCLUDED.keys():
        raise ValueError(f"Coverage mismatch: {expected - authored - EXCLUDED.keys()}")
    if source_rows["DK4_MES_B213_R0022"]["source_hex"] != "214896A8":
        raise ValueError("Sword payload changed")
    records = []
    for (block, number), english in LINES.items():
        row_id = f"DK4_MES_B{block}_R{number:04d}"
        raw = bytes.fromhex(source_rows[row_id]["source_hex"])
        state = None if (block, number) in BARE else raw[0]
        if state is not None and state not in SPEAKERS:
            raise ValueError(f"{row_id}: unmapped state {state:02X}")
        prose = english.replace("{MACRO:FI}", "")
        if "I" in prose or "F" in prose:
            raise ValueError(f"{row_id}: unsafe uppercase renderer byte")
        if raw.count(b"FI") != english.count("{MACRO:FI}"):
            raise ValueError(f"{row_id}: macro mismatch")
        prefix = "" if state is None else f"{{SPEAKER:{state:02X}}}"
        records.append({
            "id": row_id, "english": f"{prefix}{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Bare choice or companion variant"),
            "context": CONTEXT[block],
            "source_meaning": english.replace("{MACRO:FI}", "the admiral's name"),
            "source_japanese": raw[int(state is not None):].decode("shift_jis", errors="replace"),
            "localization_note": "Clean Japanese reviewed in full scene context. Preserve speakers, bare entry starts, choices, name macros, treasure names, prices and locations; fit natural English to the fixed byte slot.",
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v101-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete B207-B214 optional weapon, swan and letter events.",
        "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {str(b): sum(block == b for block, _ in LINES) for b in BLOCKS}},
        "excluded_records": EXCLUDED, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
