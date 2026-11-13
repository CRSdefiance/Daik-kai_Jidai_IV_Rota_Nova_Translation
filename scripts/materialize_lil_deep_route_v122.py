from __future__ import annotations

import csv
import json

from scripts.materialize_lil_deep_route_v107 import ROOT, SC2_SHA256

LINES = {
    (325, 12): "Please get a map to the ruins first.",
    (325, 32): "Hard to believe an ancient city stood out here...",
    (325, 34): "An ancient city stood out here...",
    (325, 35): "An ancient city stood here, huh?",
    (325, 36): "An ancient city stood here...",
    (325, 37): "An ancient city in a place like this...",
    (325, 38): "Hard to believe an ancient city stood out here...",
    (325, 40): "There was a city out here long ago, huh?",
    (325, 41): "An ancient city in a place like this...",
    (325, 44): "The map says the ruins aren't on this island...",
    (325, 48): "What? What do you mean!?",
    (325, 54): "We must cross the sea.",
    (325, 59): "Then shouldn't we go back to port?",
    (325, 62): "No, a small boat is ready. We'll use it to go on.",
    (325, 65): "Only you are worthy. Please keep the sailors from learning where the ruins are.",
    (325, 74): "One day passed.",
    (325, 78): "We've arrived. Now let's go on by land.",
    (325, 81): "Oh! There they are!",
    (325, 94): "Admiral, the ruins!",
    (325, 96): "Admiral, the ruins!",
    (325, 98): "Admiral, ruins!",
    (325, 100): "Admiral, we've found ruins.",
    (325, 102): "Admiral, we've found ruins.",
    (325, 104): "Admiral! Those are the ruins!",
    (325, 106): "Admiral, we're at the ruins.",
    (325, 110): "Coming over!",
    (326, 5): "Oh, welcome!",
    (326, 9): "Been to the village far north in the New World?",
    (326, 13): "A guest said a revered local monk once sailed to the northern continent to preach.",
    (326, 17): "He went missing after finding that village, they say. What happened?",
    (326, 21): "Who knows?",
    (326, 25): "They say he was virtuous. May his new flock love him.",
    (326, 28): "Should you head north, ask what became of that monk.",
    (327, 5): "Hey, {MACRO:FI}! Got just the job for you!",
    (327, 8): "Make tomatoes, a New World crop, popular in Mediterranean Genoa.",
    (327, 12): "Tomatoes... in Genoa? Why?",
    (327, 15): "New World cocoa, tobacco and silver are famous. But tomatoes are worth a look, too.",
    (327, 19): "Yet in parts of Europe, many won't even try tomatoes. They find the blood-red color revolting.",
    (327, 22): "The fastest way to tell people how good they taste is a rumor that they're all the rage in some town, right?",
    (327, 25): "They're quite popular on the peninsula around Genoa, they say. As a major city there, it seems ideal.",
    (327, 28): "Ah, makes sense. All right, let's do it.",
    (327, 31): "A ship's chapel, a missionary, then free goods in the square, right?",
    (327, 35): "Genoa's guild knows about it, too. Collect your reward there.",
    (328, 19): "Hurry and make tomatoes popular here!",
    (328, 24): "Make tomatoes popular here. You can do it! We'll wait patiently.",
    (328, 40): "Hey, {MACRO:FA}! Almost there! At this rate, tomatoes will be a hit in two or three days!",
    (328, 45): "Amazing! Look at the town!",
    (329, 5): "Amazing! Such a success! Who knew tomatoes could be so popular!",
    (329, 8): "Here, take your reward.",
    (329, 12): "Received 24,000 gold.",
    (329, 38): "Havana's share rose a little!",
    (329, 49): "Oh, right! Drop by Havana's guild again.",
    (329, 53): "Why?",
    (329, 57): "Seems someone came by with a job for you.",
}
STATES = {0x02, 0x93, 0xB3, 0xCE, 0xD0, 0xFE}
EXCLUDED = {
    "DK4_MES_B325_R0023": "Packed ruins event 05 60 40 46 94 80 3F 63; identical SC0B334R0023/SC1B318R0023/SC3B293R0022. Preserve unchanged.",
    "DK4_MES_B325_R0069": "Packed sea-crossing event 46 95 80; identical SC0B334R0072/SC1B318R0070/SC3B293R0069. Preserve unchanged.",
    "DK4_MES_B325_R0079": "Packed arrival event 2B 63 22 46 93 80; identical SC0B334R0082/SC1B318R0134/SC3B293R0079. Preserve unchanged.",
}


def main() -> None:
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = {r["id"]: r for r in csv.DictReader(stream)}
    expected = {i for i in source if 325 <= int(i.split("_B")[1].split("_")[0]) <= 329}
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
        records.append({"id": row_id, "english": (f"{{SPEAKER:{raw[0]:02X}}}" if state else "") + text + "{PAD}", "speaker": "Lil" if raw[0] == 2 else "Guide, companion, hostess, guild or system", "context": "Ruins sea crossing and sailor secrecy, northern New World missing missionary rumor, Genoa tomato boom quest, chapel/missionary/free goods, 24,000 gold and Havana share reward.", "source_meaning": text, "source_japanese": raw[int(state):].decode("shift_jis", errors="replace"), "localization_note": "Natural English retains island crossing, worthy visitors, secrecy, one-day delay, northern village and missing monk, tomato prejudice and publicity, Genoa/Havana distinction, two/three days and 24,000 gold. Genoa's surrounding peninsula identifies the Italian location without unsafe literal I. FI/FA and native states preserved.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
    batch = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-v122-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "Complete B325-B329 sea crossing, missionary rumor and Genoa tomato quest.", "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {str(b): sum(bb == b for bb, _ in LINES) for b in range(325, 330)}}, "excluded_records": EXCLUDED, "records": records}
    (ROOT / "translations/lil_deep_route_v122.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote Lil V122: {len(records)} records")


if __name__ == "__main__":
    main()
