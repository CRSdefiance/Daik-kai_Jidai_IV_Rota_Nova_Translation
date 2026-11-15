from __future__ import annotations

import csv
import json

from scripts.materialize_lil_deep_route_v107 import ROOT, SC2_SHA256

LINES = {
    (316, 19): "Admiral, no map means getting lost.",
    (316, 20): "Admiral, no map? We'll be lost.",
    (316, 21): "Admiral, no map means getting lost!",
    (316, 22): "Admiral, we'll get lost without a map.",
    (316, 23): "Admiral, we'll get lost without a map!",
    (316, 24): "Admiral, no map means getting lost.",
    (316, 25): "Admiral, we'll get lost without a map!",
    (316, 26): "Admiral, no map? We'll be lost.",
    (316, 53): "Really hot here.",
    (316, 55): "So very hot!",
    (316, 57): "So very hot!",
    (316, 59): "So hot.",
    (316, 61): "Ugh, so hot!",
    (316, 65): "A desert! Of course it's hot. Let's go!",
    (316, 69): "W-whoa!!",
    (316, 85): "A-Admiral! Scorpions!",
    (316, 86): "Whoa! Scorpions!",
    (316, 87): "Eek! S-scorpions!!",
    (316, 88): "A-Admiral! So many scorpions!",
    (316, 89): "A-Admiral! Scorpions!",
    (316, 90): "Whoa! Scorpions!",
    (316, 93): "E-everyone, calm down!",
    (316, 97): "B-but... What do we do?",
    (316, 104): "Kill",
    (316, 106): "Shoo",
    (316, 108): "Run",
    (316, 116): "L-let me handle this... Take that!",
    (316, 130): "They fled! Well done, Admiral! You're so reliable!",
    (316, 131): "They fled! Great job, Admiral!",
    (316, 132): "They fled! Well done, Admiral! So reliable!",
    (316, 133): "They fled! Well done, Admiral! So reliable!",
    (316, 134): "They fled! Well done, Admiral! So reliable!",
    (316, 135): "They fled! Admiral, you're amazing!",
    (316, 136): "They fled! Well done, Admiral! So reliable!",
    (316, 139): "Ouch!!",
    (316, 156): "Admiral! Are you okay?!",
    (316, 158): "Admiral! You okay?!",
    (316, 160): "Admiral! You okay?!",
    (316, 162): "Whoa! Admiral!",
    (316, 166): "G-got stung!",
    (316, 180): "Treat it at once!",
    (316, 182): "Treat it quickly!",
    (316, 184): "Oh no! Treat it quickly!",
    (316, 185): "Treat it quickly!",
    (316, 187): "Treat it at once!",
    (316, 189): "Treat it at once!",
    (316, 205): "{MACRO:FI} was injured. One day's treatment.",
    (316, 213): "Thanks! What a shock! Hate bugs!",
    (316, 218): "L-let me handle this... Go away! Shoo, shoo!",
    (316, 231): "They fled! Well done, Admiral! You're so reliable!",
    (316, 232): "They fled! Great job, Admiral!",
    (316, 233): "They fled! Well done, Admiral! So reliable!",
    (316, 234): "They fled! Well done, Admiral! So reliable!",
    (316, 235): "They fled! Well done, Admiral! So reliable!",
    (316, 236): "They fled! Admiral, you're amazing!",
    (316, 237): "They fled! Well done, Admiral! So reliable!",
    (316, 241): "Ouch!!",
    (316, 258): "Admiral! Are you okay?!",
    (316, 260): "Admiral! You okay?!",
    (316, 262): "Admiral! You okay?!",
    (316, 264): "Admiral!",
    (316, 268): "G-got stung!",
    (316, 278): "...You're fine. Just a cactus spine.",
    (316, 279): "You're fine. Just a cactus spine stuck in you.",
    (316, 281): "Let me see... Ah, you're fine. Just a cactus spine.",
    (316, 282): "...Ah, you're fine. Just a cactus spine stuck in you.",
    (316, 284): "You're fine. Just a cactus spine stuck in you. Such a fuss!",
    (316, 285): "Let's see... Ah, you're fine. Just a cactus spine.",
    (316, 286): "Let me see... Oh, a cactus spine!",
    (316, 287): "You're fine. Just a cactus spine.",
    (316, 291): "Oh! What a shock! Really hate bugs!",
    (316, 296): "Shh! We'll slip away. Don't provoke them!",
    (316, 310): "Everyone, let's go. Slowly, quietly...",
    (316, 311): "Everyone, let's go. Slowly, quietly...",
    (316, 312): "Everyone, let's go. Very quietly...",
    (316, 313): "Everyone, let's go. Slowly, quietly...",
    (316, 314): "Everyone, let's go. Slowly, quietly...",
    (316, 315): "Everyone, let's go. Very quietly...",
    (316, 330): "Thud!",
    (316, 334): "Oops! Dropped my luggage!",
    (316, 348): "Oh no!",
    (316, 350): "Ah!",
    (316, 352): "Oh no!",
    (316, 354): "Damn!",
    (316, 358): "Waaah!",
    (316, 371): "Y-you okay?! Stay with us!",
    (316, 372): "You okay?! Stay with us!",
    (316, 374): "Y-you okay? Stay with us!",
    (316, 376): "Hey, you okay? Stay with us!",
    (316, 378): "Y-you okay? Stay with us!",
    (316, 380): "You okay? Stay with us!",
    (316, 384): "Everyone, run!",
    (316, 391): "Sailors were injured.",
    (316, 410): "Oh, we've arrived!",
}
STATES = {0x02, 0x97, 0xD0, 0xD3, 0xD6, 0xDA, 0xFE}


def main() -> None:
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = {r["id"]: r for r in csv.DictReader(stream)}
    expected = {i for i in source if i.startswith("DK4_MES_B316_")}
    assert expected == {f"DK4_MES_B{b}_R{n:04d}" for b, n in LINES}
    records = []
    for (b, n), text in LINES.items():
        row_id = f"DK4_MES_B{b}_R{n:04d}"
        raw = bytes.fromhex(source[row_id]["source_hex"])
        assert raw.count(b"FI") == text.count("{MACRO:FI}"), row_id
        safe = text.replace("{MACRO:FI}", "")
        assert "I" not in safe and "F" not in safe, row_id
        state = raw[0] in STATES
        records.append({"id": row_id, "english": (f"{{SPEAKER:{raw[0]:02X}}}" if state else "") + text + "{PAD}", "speaker": "Lil" if raw[0] == 2 else "Companion or system", "context": "Complete desert scorpion Kill/Shoo/Run branches; true sting, cactus spine, dropped luggage and escape.", "source_meaning": text, "source_japanese": raw[int(state):].decode("shift_jis", errors="replace"), "localization_note": "Natural English retains all companion responses, heat and map warnings, scorpion swarms, real sting and day of treatment, harmless cactus branch, stealth warning, dropped luggage, sailor injuries and arrival. Real state 97 preserved; Japanese 81/8B/8C/8E/8F/91/92/93/96 heads are bare prose.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
    batch = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-v118-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "Complete B316 desert scorpion encounter.", "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {"316": len(records)}}, "excluded_records": {}, "records": records}
    (ROOT / "translations/lil_deep_route_v118.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote Lil V118: {len(records)} records")


if __name__ == "__main__":
    main()
