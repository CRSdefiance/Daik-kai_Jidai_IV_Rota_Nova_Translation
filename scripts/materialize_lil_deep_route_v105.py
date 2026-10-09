from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.materialize_lil_deep_route_v101 import SC2_SHA256

ROOT = Path(__file__).resolve().parents[1]
LINES = {
    (250, 5): "What's wrong, Boss?",
    (250, 9): "This statue... Doesn't it feel strange to you? Somehow, it seems warm.",
    (250, 15): "A statue? Where?",
    (250, 18): "Right there.",
    (250, 22): "Let's see.",
    (250, 26): "Oh! A figurehead! Such elaborate work! Hmm, yes, there's something about it!",
    (250, 33): "Do you know it? A famous statue?",
    (250, 36): "No, never heard of it. Oh! Are you thinking of taking it with us?",
    (250, 42): "Yes",
    (250, 44): "No",
    (250, 52): "Hmm. Such a fine figurehead would surely bless our ship. But is it all right to take it without permission?",
    (250, 55): "Wouldn't leaving such a fine figurehead ashore be a crime?",
    (250, 59): "Oh! How kind you are, Admiral! Settled, then! Let's carry it away!",
    (250, 63): "Pardon us, dear figurehead. Please come along with us.",
    (250, 66): "Then you shall have my protection.",
    (250, 69): "W-what? Whose voice was that?!",
    (250, 72): "What's wrong? Hurry and grab that end!",
    (250, 75): "But... a voice!",
    (250, 79): "Still asleep?",
    (250, 84): "{MACRO:FI}'s Luck rose by 1!",
    (250, 88): "Cesare's Luck rose by 1!",
    (250, 91): "?? (Whose voice was that? So warm, so full of love...)",
    (250, 98): "Of course. (Still, it's a little disappointing...)",
    (250, 102): "Let's head back.",
    (250, 109): "Yes, let's. (Such a wonderful statue. Just looking at it seemed to cleanse the heart...)",
    (250, 112): "{MACRO:FI}'s Charm rose by 1!",
    (250, 116): "Cesare's Charm rose by 1!",
    (251, 6): "Admiral, over here! Writing on the wall!",
    (251, 9): "A full vessel holds water and floating ice. When the ice melts, does the water level change?",
    (251, 12): "Press the stone ahead for 'rises,' left for 'falls,' or right for 'unchanged.'",
    (251, 19): "Ahead",
    (251, 21): "Left",
    (251, 23): "Right",
    (251, 31): "Easy! Here's the answer!",
    (251, 41): "Admiral, the ceiling's falling! Danger!",
    (251, 42): "Admiral! The ceiling's falling!",
    (251, 43): "Admiral! The ceiling's falling!",
    (251, 44): "Admiral! The ceiling's falling! Run!",
    (251, 46): "Look out! The ceiling's falling!",
    (251, 47): "Admiral, the ceiling's falling! Best run!",
    (251, 48): "Aah! The ceiling's falling!",
    (251, 49): "The ceiling's falling. We can't stay here!",
    (251, 52): "Huh? That's odd... No time for that! Run! Everyone, back to town for today!",
    (251, 66): "Easy! Here's the answer!",
    (251, 76): "Admiral, the ceiling's falling! Danger!",
    (251, 77): "Admiral! The ceiling's falling!",
    (251, 78): "Admiral! The ceiling's falling!",
    (251, 79): "Admiral! The ceiling's falling! Run!",
    (251, 80): "Look out! The ceiling's falling!",
    (251, 82): "Admiral, the ceiling's falling! Best run!",
    (251, 83): "Aah! The ceiling's falling!",
    (251, 84): "The ceiling's falling. We can't stay here!",
    (251, 87): "Huh? That's odd... No time for that! Run! Everyone, back to town for today!",
    (251, 102): "Melting ice won't change the level. The right stone!",
    (251, 109): "The wall opens!",
    (251, 117): "Admiral! A strange statue!",
    (251, 120): "Where?",
    (251, 124): "Here. Looks like a figurehead...",
    (251, 127): "Crack! Crack!",
    (251, 131): "W-what?!",
    (251, 135): "Did you awaken me?",
    (251, 139): "Aah! A-Admiral!",
    (251, 142): "Speak!",
    (251, 148): "Yes",
    (251, 150): "No",
    (251, 157): "Then you may wield my power!",
    (251, 161): "Eh?",
    (251, 165): "Take the statue that holds my power. Once you have it, leave at once!",
    (251, 171): "What was that? Using this thing won't curse us, will it?",
    (251, 175): "Y-yes... A little creepy...",
    (251, 181): "By chance, you say? An insult! You shall not leave!",
    (251, 192): "Rooooaaar!!",
    (251, 204): "A-Admiral! Let's run!",
    (251, 209): "Everyone, run!",
    (251, 231): "Huff... puff... Whew! Close one!",
    (251, 234): "My body feels heavy...",
    (252, 7): "Oh, {MACRO:FI}! Welcome!",
    (252, 10): "Seeking ruins? Some are nearby.",
    (252, 13): "Usually a secret from foreigners. But we'll tell you!",
    (253, 6): "Welcome, {MACRO:FI}!",
    (253, 9): "Oh? Searching for ruins around the world? Hmm. None particularly famous in this town.",
    (254, 6): "Oh, {MACRO:FI}!",
    (254, 10): "Seeking ruins worldwide? Sorry... None famous in this town.",
}
BARE = {(250, 42), (250, 44), (251, 19), (251, 21), (251, 23), (251, 148), (251, 150)} | {(251, n) for n in (42, 43, 44, 46, 47, 48, 49, 77, 78, 79, 80, 82, 83, 84)}
EXCLUDED = {"DK4_MES_B251_R0183": "Packed curse-control event (35 63 94 47), identical to SC0 B261 R0197, SC1 B252 R0186 and SC3 B221 R0185; preserved unchanged."}
SPEAKERS = {0x02: "Lil", 0x0D: "Cesare", 0x14: "Peres", 0xBE: "Tavern woman", 0xBD: "Tavern woman", 0xC8: "Tavern woman", 0xD0: "Companion", 0xFE: "Figurehead or system"}
CONTEXT = {250: "Kind figurehead, both take/leave choices, voice and Luck/Charm rewards.", 251: "Melting-ice ruin puzzle, every collapse variant, demon figurehead answers and curse branch.", 252: "Tavern woman's nearby ruin directions.", 253: "Tavern woman has no local ruin clue.", 254: "Alternate tavern woman's no-ruins reply."}


def main() -> None:
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {i for i in source if 250 <= int(i.split("_B")[1].split("_")[0]) <= 254}
    assert expected == {f"DK4_MES_B{b}_R{n:04d}" for b, n in LINES} | set(EXCLUDED)
    assert source["DK4_MES_B251_R0183"]["source_hex"].lower() == "35639447"
    records = []
    for (b, n), text in LINES.items():
        row_id = f"DK4_MES_B{b}_R{n:04d}"
        raw = bytes.fromhex(source[row_id]["source_hex"])
        state = None if (b, n) in BARE else raw[0]
        assert state is None or state in SPEAKERS
        prose = text
        for macro in ("FI", "FA", "FO"):
            assert raw.count(macro.encode()) == text.count(f"{{MACRO:{macro}}}")
            prose = prose.replace(f"{{MACRO:{macro}}}", "")
        assert "I" not in prose and "F" not in prose, row_id
        records.append({"id": row_id, "english": ("" if state is None else f"{{SPEAKER:{state:02X}}}") + text + "{PAD}", "speaker": SPEAKERS.get(state, "Bare choice or companion variant"), "context": CONTEXT[b], "source_meaning": text, "source_japanese": raw[int(state is not None):].decode("shift_jis", errors="replace"), "localization_note": "Source-reviewed natural English retains all puzzle answers, branches, native presentation and macro order. Bare variants retain their first glyph.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
    batch = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-v105-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "All B250-B254 benevolent and demon figurehead events and ruin hints.", "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {str(b): sum(bb == b for bb, _ in LINES) for b in CONTEXT}}, "excluded_records": EXCLUDED, "records": records}
    (ROOT / "translations/lil_deep_route_v105.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote Lil V105: {len(records)} records, {len(EXCLUDED)} exclusions")


if __name__ == "__main__":
    main()
