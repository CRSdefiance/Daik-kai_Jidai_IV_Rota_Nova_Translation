from __future__ import annotations

import csv
import json

from scripts.materialize_lil_deep_route_v107 import ROOT, SC2_SHA256

LINES = {
    (306, 81): "Was it washed away?",
    (307, 6): "Oh, {MACRO:FI}!",
    (307, 10): "Visiting the temple today. Want to come?",
    (307, 13): "A temple... Anything worth seeing?",
    (307, 16): "Hmm... Well, it'll be a nice break.",
    (307, 19): "Oh, right!",
    (307, 23): "The gold temple on this map... Nearby?",
    (307, 26): "Gold? Oh, that temple! Not nearby, though...",
    (307, 30): "Let's go partway together. Then follow your map to the temple.",
    (308, 6): "Oh, right. We need to buy rice?",
    (309, 7): "Bought it! Ah, so tired...",
    (309, 15): "Huh?! What is it now?",
    (309, 22): "...What is it now?!",
    (309, 29): "Another offering? Do we pay for this, too?",
    (309, 36): "Why make me do all this? Not even a Buddhist!",
    (309, 43): "Yes, yes, tea and sugar! Just buy them, right?!",
    (310, 13): "We need tea and sugar.",
    (310, 35): "We need tea and sugar.",
    (310, 52): "Bought them!",
    (310, 56): "Well done. Next...",
    (310, 59): "Yes, what now?! (Oh, whatever...)",
    (310, 62): "Hmm. Not sincere yet, but you've learned some humility and courtesy at last. Very well.",
    (310, 65): "Huh?",
    (310, 69): "Now, listen closely.",
    (310, 77): "China's far NE...?",
    (310, 81): "Big peninsula base: east coast, high peak's foot.",
    (310, 84): "So far away that ordinary ships may not reach it. Without firm resolve, you'll lose your lives.",
    (310, 91): "Never give the Proof to anyone with evil intent.",
    (310, 94): "Stay humble and courteous. Don't give in to wicked desires.",
    (310, 97): "Y-yes.",
    (310, 101): "Repayment for purchases, plus a tip.",
    (310, 106): "Received 20,000 gold coins.",
    (310, 110): "Huh?! We can keep it? ...May we?",
    (310, 114): "Don't waste it.",
    (310, 118): "Don't treat me like a child!",
    (310, 122): "Ho ho! Do your best, then.",
    (311, 9): "Admiral, meet the Proof map's keepers? A village far northeast of China, right?",
    (311, 11): "Admiral, let's meet the Proof map's guardians soon. Their village is far northeast of China.",
    (311, 12): "Admiral, what are the Proof map's guardians like? A village far northeast of China, right? Let's go!",
    (311, 13): "Admiral, let's visit the Proof map's keepers before we forget! They're far northeast of China?",
    (311, 14): "Admiral, let's visit the Proof map's keepers soon! A village far northeast of China?",
    (311, 16): "Admiral, as for the Proof... Let's meet its map's guardians soon, at their village far northeast of China.",
    (311, 17): "Admiral, curious about the Proof map's guardians? Let's visit that village far northeast of China!",
    (311, 18): "Admiral, curious about the Proof map? Let's visit its guardians, in a village far northeast of China, yes?",
}
STATES = {0x02, 0x89, 0xCB, 0xD0, 0xFE}


def main() -> None:
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = {r["id"]: r for r in csv.DictReader(stream)}
    expected = {i for i in source if 307 <= int(i.split("_B")[1].split("_")[0]) <= 311} | {"DK4_MES_B306_R0081"}
    assert expected == {f"DK4_MES_B{b}_R{n:04d}" for b, n in LINES}
    records = []
    for (b, n), text in LINES.items():
        row_id = f"DK4_MES_B{b}_R{n:04d}"
        raw = bytes.fromhex(source[row_id]["source_hex"])
        assert raw.count(b"FI") == text.count("{MACRO:FI}"), row_id
        safe = text.replace("{MACRO:FI}", "")
        assert "I" not in safe and "F" not in safe, row_id
        state = raw[0] in STATES
        records.append({"id": row_id, "english": (f"{{SPEAKER:{raw[0]:02X}}}" if state else "") + text + "{PAD}", "speaker": "Lil" if raw[0] == 2 else "Monk, hostess or companion", "context": "Gold temple errands, monk's humility lesson, Proof map directions and northeastern clan; last river variant.", "source_meaning": text, "source_japanese": raw[int(state):].decode("shift_jis", errors="replace"), "localization_note": "Natural English retains rice, tea and sugar offerings, Lil's frustration, humility/courtesy, dangerous voyage, Proof warning, 20,000 gold repayment, huge peninsula base and eastern peak directions. B306R0081 starts with Japanese 97AC (flow), not a speaker state.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
    batch = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-v115-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "Complete B307-B311 temple and Proof clue, plus B306R0081 bare river variant.", "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {str(b): sum(bb == b for bb, _ in LINES) for b in range(306, 312)}}, "excluded_records": {}, "records": records}
    (ROOT / "translations/lil_deep_route_v115.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote Lil V115: {len(records)} records")


if __name__ == "__main__":
    main()
