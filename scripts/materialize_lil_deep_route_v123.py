from __future__ import annotations

import csv
import json

from scripts.materialize_lil_deep_route_v107 import ROOT, SC2_SHA256

LINES = {
    (330, 5): "Hello...",
    (330, 9): "You have a job for me?",
    (330, 12): "Actually... We're searching for ruins. We thought you might be able to help us...",
    (330, 16): "What job?",
    (330, 20): "They say our ancestors built the ruins to honor warriors.",
    (330, 23): "Legend says only those worthy of being the mightiest warrior can find them.",
    (330, 27): "Huh?",
    (330, 31): "Hey! A delicate maiden like me, the mightiest warrior? Really?",
    (330, 35): "O-of course, we don't mean you look like some muscle-bound warrior.",
    (330, 39): "The mightiest has strength, a good heart and wisdom.",
    (330, 42): "You made tomatoes popular for the guild. Surely you have that heart and wisdom...",
    (330, 46): "A righteous heart and wisdom... Honest and clever? That's me, all right!",
    (330, 58): "Really?",
    (330, 65): "To be honest, even we feel this search is like chasing clouds.",
    (330, 68): "We ask everyone who seems to meet the conditions, just as we're asking you.",
    (330, 72): "Sorry if that offends you. No one has ever succeeded, so even if you fail, it won't be a problem.",
    (330, 75): "What?! So anyone will do? Don't make a fool of me!",
    (330, 79): "Please, won't you help?",
    (330, 83): "...We thought {MACRO:FA} would help people who needed it. Disappointing...",
    (330, 87): "D-disappointed?",
    (330, 91): "We'll pay part up front. Even if you don't find the ruins, we won't ask for the money back.",
    (330, 95): "Could you...?",
    (330, 99): "A-all right! To help people? Let's do it!",
    (330, 102): "Really! Thank you so much!",
    (330, 106): "Received 5,000 gold.",
    (330, 112): "You'll need a map first. Get the Ancient City Ruins Map, then let me know. We'll search together.",
    (330, 115): "Meet me at this city's gate, then.",
    (331, 5): "Unfamiliar faces. Where are you from?",
    (331, 8): "Holland.",
    (331, 12): "Holland? Maybe we've heard of it... But you've come a long way, it seems.",
    (331, 16): "Ah, now we see! You have that handy thing called a sextant, don't you?",
    (331, 20): "Huh?",
    (331, 24): "We've heard it tells you where you are even at sea, with no landmarks in sight.",
    (331, 28): "How about giving us that sextant? We'll give you something good in exchange.",
    (331, 31): "Something?",
    (331, 35): "Bring it, and you'll find out.",
    (332, 6): "Oh, you brought it? Here, take this in exchange.",
    (332, 14): "Gave the sextant.",
    (333, 15): "Let's land the team.",
    (333, 17): "Landing the team.",
    (333, 19): "Landing the team.",
    (333, 21): "Land the team.",
    (333, 23): "Landing the team!",
    (333, 25): "Let's land the team.",
    (333, 71): "Gave all our gold as initial funds.",
    (333, 76): "Gave 1,000 gold as initial funds.",
    (333, 83): "We'll start the survey now. Please report to Sofala's guild.",
    (334, 6): "You came for this, yes?",
    (334, 10): "At long last, this day has come...",
    (334, 13): "We'll put our faith in you. Please accept this.",
    (335, 5): "Oh! You know of that good monk!?",
    (335, 9): "Know him?",
    (335, 13): "He couldn't bear our suffering from the plague. His devoted care saved our village from extinction.",
    (335, 16): "His medicine eased the illness at once. A true miracle!",
    (335, 20): "Wow, a monk who works like a doctor.",
    (335, 23): "No, he called it alchemy. He said it removed toxic minerals from our water...",
    (335, 27): "Look, he wrote this book.",
    (335, 38): "!! Could this be...!?",
    (335, 57): "The book Charles mentioned! At last, it's ours!",
    (335, 64): "The Alchemy Book!? Never thought we'd find it here!!",
    (335, 76): "H-hey! What's got into you, Charles!?",
    (335, 79): "My journey to the New World began with rumors of a newly discovered material for experiments!!",
    (335, 82): "My research showed that the Alchemy Book was needed to obtain that material, but...",
    (335, 86): "This must be a clue to some precious metal!! Now, how to use it... *mutter*",
    (335, 89): "N-no need! Sounds long...",
    (335, 94): "At last, it's ours!",
    (335, 103): "At last, it's ours!",
    (335, 113): "Hey, where is he now?",
    (335, 125): "He drank our village's water and fell ill, just like us...",
    (335, 128): "Yet he hid his illness and gave all the medicine he made to the villagers!",
    (335, 132): "And at last, he passed away... He was truly God's messenger...",
    (335, 139): "...May we entrust this book to you?",
    (335, 142): "To us?",
    (335, 146): "The book tells of an ore no one has ever seen before.",
    (335, 149): "That ore must lie buried somewhere in the world.",
    (335, 152): "We seek someone to carry on the monk's research. Will you find that ore for us?",
    (335, 156): "Yes, let's try! We'll find it, whatever it takes!",
}
STATES = {0x02, 0x09, 0x12, 0x97, 0xA1, 0xB3, 0xCF, 0xD0, 0xFE}
EXCLUDED = {
    "DK4_MES_B22_R0077": "Packed companion operation 2C 63 20 46 E6 80 between Kamil and Fernando dialogue. Native operation bytes and terminal 46/state/80 event family, no Japanese prose. Preserve unchanged.",
    "DK4_MES_B22_R0088": "Packed companion event 20 46 E8 80 between Fernando and Emilio dialogue; same 20/46/state/80 family as cross-route-confirmed B323R0106. No Japanese prose. Preserve unchanged.",
    "DK4_MES_B22_R0124": "Packed companion event 21 46 E5 80 between Fernando and Kamil dialogue; same 21/46/state/80 family as cross-route-confirmed B323R0066. No Japanese prose. Preserve unchanged.",
}


def main() -> None:
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = {r["id"]: r for r in csv.DictReader(stream)}
    expected = {i for i in source if 330 <= int(i.split("_B")[1].split("_")[0]) <= 335}
    expected |= set(EXCLUDED)
    assert expected == {f"DK4_MES_B{b}_R{n:04d}" for b, n in LINES} | set(EXCLUDED)
    records = []
    for (b, n), text in LINES.items():
        row_id = f"DK4_MES_B{b}_R{n:04d}"
        raw = bytes.fromhex(source[row_id]["source_hex"])
        safe = text
        for macro in ("FI", "FA", "FO"):
            assert raw.count(macro.encode()) == text.count(f"{{MACRO:{macro}}}"), row_id
            safe = safe.replace(f"{{MACRO:{macro}}}", "")
        assert "I" not in safe and "F" not in safe, row_id
        state = raw[0] in STATES
        records.append({"id": row_id, "english": (f"{{SPEAKER:{raw[0]:02X}}}" if state else "") + text + "{PAD}", "speaker": {2: "Lil", 9: "Kamil", 0x12: "Charles"}.get(raw[0], "Guide, elder, companion or system"), "context": "Mightiest warrior ruins commission, 5,000-gold advance, sextant exchange, Sofala survey funding, item handoff, deceased monk's selfless medicine and Alchemy Book ore search.", "source_meaning": text, "source_japanese": raw[int(state):].decode("shift_jis", errors="replace"), "localization_note": "Natural English retains virtue/wisdom joke, non-refundable advance, map and city-gate meeting, sextant navigation/exchange, all-gold/1,000-gold alternatives, Sofala, Charles's experimental material, toxic minerals in water, monk's sacrifice and ore lead. Native states, bare team variants and FA preserved.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
    batch = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-v123-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "Complete B330-B335 final ruins commissions, survey, sextant and Alchemy Book scenes; classify three B22 companion controls.", "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {str(b): sum(bb == b for bb, _ in LINES) for b in range(330, 336)}}, "excluded_records": EXCLUDED, "records": records}
    (ROOT / "translations/lil_deep_route_v123.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote Lil V123: {len(records)} records")


if __name__ == "__main__":
    main()
