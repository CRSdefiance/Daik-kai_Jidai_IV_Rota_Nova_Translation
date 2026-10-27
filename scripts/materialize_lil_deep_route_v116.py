from __future__ import annotations

import csv
import json

from scripts.materialize_lil_deep_route_v107 import ROOT, SC2_SHA256

LINES = {
    (312, 20): "Admiral, no map? We'll be lost.",
    (312, 21): "No map? We'll get lost!",
    (312, 22): "Admiral, no map? Seems risky.",
    (312, 23): "Admiral, no map? We'll be lost.",
    (312, 24): "Admiral, no map? Bad idea!",
    (312, 25): "Admiral, no map means getting lost.",
    (312, 26): "Admiral, we need a map!",
    (312, 27): "Admiral, no map? We'll be lost.",
    (312, 52): "Let's go, then.",
    (312, 54): "Let's go!",
    (312, 56): "Let's go.",
    (312, 58): "Shall we go?",
    (312, 71): "A-Admiral! Wolves!",
    (312, 73): "Hmm! Wolves!",
    (312, 75): "A-Admiral! Wolves!",
    (312, 77): "Eek! Wolves!!",
    (312, 79): "Whoa! Wolves appeared!",
    (312, 81): "A-Admiral! Wolves!",
    (312, 83): "Whoa! Wolves!",
    (312, 85): "A-Admiral! Wolves here!",
    (312, 89): "Eek! Eeek!!",
    (312, 94): "E-everyone, calm down!",
    (312, 98): "W-what will you do?",
    (312, 105): "Shoo",
    (312, 107): "Hit",
    (312, 109): "Run",
    (312, 117): "L-let me handle this... Go away! Shoo, shoo!",
    (312, 131): "Admiral! Watch out!",
    (312, 132): "Admiral! Watch out!",
    (312, 133): "Admiral! Watch out!",
    (312, 134): "Watch out!!",
    (312, 136): "Admiral! Watch out!",
    (312, 137): "Admiral! Watch out!",
    (312, 140): "Eek! That hurts!",
    (312, 157): "Are you okay?!",
    (312, 159): "You okay?",
    (312, 161): "You okay?!",
    (312, 163): "You okay?",
    (312, 167): "Ouch... But yes, seems okay.",
    (312, 175): "{MACRO:FI} was injured.",
    (312, 179): "We'll beat these things! Charge!!",
    (312, 196): "Watch out!",
    (312, 198): "Watch out!",
    (312, 200): "Watch out!",
    (312, 217): "Argh!",
    (312, 219): "Aaaah!!",
    (312, 221): "Yah!",
    (312, 223): "Waaah!!",
    (312, 227): "You okay?!",
    (312, 242): "Ugh! J-just fine.",
    (312, 243): "Ugh! Ouch...",
    (312, 244): "Ugh! Hurts...",
    (312, 245): "Ugh! N-nothing serious!",
    (312, 246): "Ugh! Q-quite fine.",
    (312, 247): "Waaah! Not okay!",
    (312, 250): "Sorry... Could've fought better... This is my fault...",
    (312, 260): "Treat it soon; we'll be fine. The wolves fled.",
    (312, 261): "Admiral, don't worry. Treat it soon; we'll be fine. The wolves fled.",
    (312, 263): "Don't worry! Treat it soon. The wolves left, too.",
    (312, 265): "Just treat it soon. Glad the wolves are gone, too.",
    (312, 266): "Don't worry! Treat it soon; we'll be fine. The wolves left, too.",
    (312, 268): "Don't worry. Treat it soon to avoid serious harm. The wolves left; that's settled.",
    (312, 270): "Quick treatment will help! Glad the wolves fled, too!",
    (312, 271): "You'll be fine. Treat this small wound soon. The wolves fled, too.",
    (312, 275): "Phew!",
    (312, 282): "The sailors seem tired.",
    (312, 287): "Hey, you're lucky! Normally we'd beat you, but today we'll let you go!",
    (312, 299): "Just admit you're afraid of wolves...",
    (312, 302): "What was that, Kamil?!",
    (312, 306): "N-no, nothing! (Amazing how well she hears things like that.)",
    (312, 330): "Nearly out of the forest...",
    (312, 331): "The forest should end soon?",
    (312, 332): "Nearly out of the forest...",
    (312, 333): "Nearly out of the forest...",
    (312, 334): "The forest's ending, right?",
    (312, 349): "Admiral, there it is!",
    (312, 351): "See, Admiral?",
    (312, 353): "Admiral, it's there!",
    (312, 355): "Admiral, it's there!",
    (312, 357): "There, Admiral!",
    (313, 6): "Welcome, {MACRO:FI}!",
    (313, 9): "Want to know where the gate is?",
    (313, 13): "Not really allowed to tell foreigners, though...",
    (313, 16): "Outside pressure has made this country's isolation meaningless. All right, let me tell you in secret.",
}
STATES = {0x02, 0x09, 0x97, 0xC9, 0xD0, 0xD3, 0xD6, 0xD7, 0xDA, 0xFE}
EXCLUDED = {
    "DK4_MES_B312_R0038": "Packed forest event 05 60 41 46 89 80 3E 63; identical SC0B325R0038, SC1B309R0038 and SC3B281R0037. Preserve unchanged.",
    "DK4_MES_B312_R0316": "Packed wolf event 46 8A 80 81 43; identical SC0B325R0313, SC1B309R0316 and SC3B281R0316. Preserve unchanged.",
}


def main() -> None:
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = {r["id"]: r for r in csv.DictReader(stream)}
    expected = {i for i in source if 312 <= int(i.split("_B")[1].split("_")[0]) <= 313}
    assert expected == {f"DK4_MES_B{b}_R{n:04d}" for b, n in LINES} | set(EXCLUDED)
    records = []
    for (b, n), text in LINES.items():
        row_id = f"DK4_MES_B{b}_R{n:04d}"
        raw = bytes.fromhex(source[row_id]["source_hex"])
        assert raw.count(b"FI") == text.count("{MACRO:FI}"), row_id
        safe = text.replace("{MACRO:FI}", "")
        assert "I" not in safe and "F" not in safe, row_id
        state = raw[0] in STATES
        records.append({"id": row_id, "english": (f"{{SPEAKER:{raw[0]:02X}}}" if state else "") + text + "{PAD}", "speaker": "Lil" if raw[0] == 2 else "Kamil, companion or hostess", "context": "Complete wolf Shoo/Hit/Run branches, injuries and companion treatment advice; Japanese city gate clue.", "source_meaning": text, "source_japanese": raw[int(state):].decode("shift_jis", errors="replace"), "localization_note": "Natural English retains all wolf encounter choices and branches, injuries, Lil's remorse and bluster, Kamil's aside, sailor fatigue, forest exit and gate secrecy. Speaker states, bare variants and FI substitutions retained.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
    batch = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-v116-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "Complete B312-B313 wolf encounter and city gate clue.", "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {str(b): sum(bb == b for bb, _ in LINES) for b in (312, 313)}}, "excluded_records": EXCLUDED, "records": records}
    (ROOT / "translations/lil_deep_route_v116.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote Lil V116: {len(records)} records")


if __name__ == "__main__":
    main()
