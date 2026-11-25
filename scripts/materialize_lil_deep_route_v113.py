from __future__ import annotations

import csv
import json

from scripts.materialize_lil_deep_route_v107 import ROOT, SC2_SHA256

LINES = {
    (301, 19): "Admiral, no map means getting lost...",
    (301, 20): "Admiral, we need a map.",
    (301, 22): "Admiral, we can't go on without a map!",
    (301, 23): "Admiral, let's get a map first so we don't get lost.",
    (301, 24): "Admiral, no map? Going on is risky.",
    (301, 25): "Admiral, no map means getting lost.",
    (301, 27): "Admiral, we'll get lost without a map!",
    (301, 28): "Admiral, no map? We'll get lost.",
    (301, 53): "Quite hot here.",
    (301, 55): "Hot...",
    (301, 57): "Phew, so hot!",
    (301, 59): "So hot here!",
    (301, 61): "So hot!",
    (301, 63): "Very hot here.",
    (301, 65): "Phew, so hot!",
    (301, 67): "My, it's hot here.",
    (301, 71): "A long way to go. Don't drink all your water, folks!",
    (301, 74): "Storm?!",
    (301, 78): "Ptoo! Sand in my mouth!",
    (301, 91): "Can't see ahead!",
    (301, 93): "Can't see...",
    (301, 95): "Can't see!",
    (301, 97): "Can't see!",
    (301, 99): "Damn, can't see ahead!",
    (301, 101): "Can't see!",
    (301, 103): "Can't see a thing!",
    (301, 105): "Can't see ahead.",
    (301, 109): "An oasis!",
    (301, 113): "Everyone looks tired. Shall we rest?",
    (301, 118): "Rest briefly",
    (301, 120): "Long rest",
    (301, 128): "Aw, leaving already?",
    (301, 132): "No complaints!",
    (301, 136): "Yeah...",
    (301, 145): "Ah, much better!",
    (301, 152): "One day passed. The sailors rested.",
    (301, 167): "The desert should end soon...",
    (301, 168): "Should be out of the desert...",
    (301, 169): "The desert should end soon...",
    (301, 170): "Shouldn't the desert end soon...?",
    (301, 171): "Should be out of the desert soon...",
    (301, 172): "The desert should end soon...",
    (301, 173): "Thought the desert would end soon...",
    (301, 174): "We should leave the desert soon...",
    (301, 187): "Admiral! Look over there!",
    (301, 188): "Admiral! Look!",
    (301, 189): "Admiral! Look there!",
    (301, 190): "Admiral! Look!",
    (301, 191): "Admiral! Look there!",
    (301, 192): "Admiral! Look!",
    (302, 6): "Oh, {MACRO:FI}! Welcome!",
    (302, 9): "Thanks to you, my dancing has really improved!",
    (302, 12): "Here's a tip to thank you.",
    (302, 16): "There's a mosque far inland honoring an ancient king. They say it holds a wonderful treasure.",
    (302, 20): "Only someone the king accepts can claim the treasure, they say. Why not try?",
    (303, 6): "Basra's guild is looking for you.",
    (304, 5): "Sorry to call you in. We have a big job for you.",
    (304, 8): "Merchants from around the ocean will gather for a spice exhibition. We'll hold a small sale there, too.",
    (304, 11): "As you know, this city doesn't trade in spices, so we must bring them in from other cities.",
    (304, 15): "Preparing the venue has kept us busy. We barely have enough for display; we'll be short of stock to sell.",
    (304, 18): "You know the world's goods. That's why we'd like you to procure the stock.",
    (304, 22): "Leave it all to me!",
    (304, 26): "We need one hold of each kind of spice.",
    (304, 29): "Nine kinds: pepper, cloves, cinnamon, nutmeg, pimento, tamarind, saffron, vanilla and chilies.",
    (304, 32): "Bring all of them together.",
    (304, 36): "Huh? Can't we bring them one at a time?",
    (304, 39): "We need them at the venue together. We're busy, as we said! There's no storage space here.",
    (304, 43): "Ugh, what a bother!",
    (304, 47): "Oh, don't say that.",
    (304, 51): "The New World and Southeast Asia are major sources. Unsure? Check market information. Thanks!",
    (305, 13): "Where's the pepper? Hurry, please.",
    (305, 33): "No cloves yet? Please hurry.",
    (305, 53): "Not enough nutmeg. Please get more.",
    (305, 73): "No cinnamon. Please get some soon.",
    (305, 93): "Where's the pimento? Bring all the spices together.",
    (305, 113): "No chilies. Bring all the spices together.",
    (305, 133): "No vanilla. Bring the whole set together.",
    (305, 153): "Where's the saffron? Hurry!",
    (305, 173): "No tamarind. Please hurry.",
    (305, 185): "You've got them all! Thanks! Here's your payment and reward.",
    (305, 198): "Received 40,000 gold coins.",
    (305, 221): "Share in Basra rose a little!",
    (305, 232): "We'd like to give you more, but we have expenses, too... Oh, that's right!",
    (305, 236): "Someone brought us an item. Apparently it's valuable, but we can't work out a price for it.",
    (305, 239): "Would you take it as a token of our thanks?",
}
STATES = {0x02, 0x5F, 0x94, 0x97, 0xC5, 0xD0, 0xD3, 0xD6, 0xFE}


def main() -> None:
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = {r["id"]: r for r in csv.DictReader(stream)}
    expected = {i for i in source if 301 <= int(i.split("_B")[1].split("_")[0]) <= 305}
    assert expected == {f"DK4_MES_B{b}_R{n:04d}" for b, n in LINES}
    records = []
    for (b, n), text in LINES.items():
        row_id = f"DK4_MES_B{b}_R{n:04d}"
        raw = bytes.fromhex(source[row_id]["source_hex"])
        safe = text.replace("{MACRO:FI}", "")
        assert "I" not in safe and "F" not in safe, row_id
        state = raw[0] in STATES
        prefix = f"{{SPEAKER:{raw[0]:02X}}}" if state else ""
        records.append({"id": row_id, "english": prefix + text + "{PAD}", "speaker": "Lil" if raw[0] == 2 else "Source state or companion variant", "context": "Desert heat, sandstorm, oasis rest choices; mosque clue and Basra's nine-spice exhibition quest.", "source_meaning": text, "source_japanese": raw[int(state):].decode("shift_jis", errors="replace"), "localization_note": "Natural English retains branch actions, one-day rest, one hold of each spice, all-at-once delivery, 40,000 gold and gift follow-up. Bare companion variants and real state 97 preserved.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
    batch = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-v113-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "Complete B301-B305 desert encounter, mosque tip and spice quest.", "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {str(b): sum(bb == b for bb, _ in LINES) for b in range(301, 306)}}, "excluded_records": {}, "records": records}
    (ROOT / "translations/lil_deep_route_v113.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote Lil V113: {len(records)} records")


if __name__ == "__main__":
    main()
