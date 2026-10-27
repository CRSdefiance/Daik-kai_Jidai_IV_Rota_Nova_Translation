from __future__ import annotations

import csv
import json

from scripts.materialize_lil_deep_route_v107 import ROOT, SC2_SHA256

LINES = {
    (314, 18): "Admiral, we can't go on without a map.",
    (314, 19): "Admiral, going on without a map is rash.",
    (314, 20): "Admiral, no map? We won't know where to go.",
    (314, 21): "Admiral, no map? How can we go on?",
    (314, 22): "Admiral, no map? We can't go on.",
    (314, 23): "Admiral, no map? We won't know where to go.",
    (314, 24): "Admiral, no map? We won't know where to go.",
    (314, 25): "Admiral, no map? Going on is impossible.",
    (314, 47): "This forest's quite dark.",
    (314, 49): "Dense forest...",
    (314, 51): "So dark, even in daytime!",
    (314, 53): "So dark in the forest!",
    (314, 55): "Quite a dark wood.",
    (314, 57): "Dense forest...",
    (314, 59): "So dark it's like night!",
    (314, 61): "Dense forest...",
    (314, 69): "...Oh, dear.",
    (314, 75): "Climb down",
    (314, 77): "Detour",
    (314, 95): "Watch your step.",
    (314, 97): "Watch your step.",
    (314, 99): "Watch your step!",
    (314, 101): "Watch your step, now.",
    (314, 103): "Watch your step!",
    (314, 105): "Please watch your step.",
    (314, 109): "Caving in!",
    (314, 113): "Ouch...",
    (314, 121): "Some people are injured.",
    (314, 145): "One day passed.",
    (314, 165): "Almost there. Come on!",
    (314, 184): "Admiral! Look there!",
    (314, 186): "Admiral! Look there!",
    (314, 188): "Admiral! Look there!",
    (314, 190): "Admiral! Look there!",
    (315, 6): "Oh, {MACRO:FI}! Meant to tell you something, but forgot!",
    (315, 10): "An ancient pictorial map was found recently. Seems an old kingdom's ruins lie near this city.",
    (315, 13): "Wow, a pictorial map? Who's got it?",
    (315, 16): "Sorry, don't know that. But if you're interested, why not look for it?",
}
STATES = {0x02, 0x97, 0xCD, 0xD0, 0xD3, 0xD6, 0xFE}
EXCLUDED = {
    "DK4_MES_B314_R0036": "Packed forest event 05 60 61 46 9A 80 3F 63; identical SC0B327R0036, SC1B311R0036 and SC3B283R0035. Preserve unchanged.",
    "DK4_MES_B314_R0063": "Packed descent event 75 46 9B 80; native operation/state bytes without prose. Preserve unchanged.",
}


def main() -> None:
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = {r["id"]: r for r in csv.DictReader(stream)}
    expected = {i for i in source if 314 <= int(i.split("_B")[1].split("_")[0]) <= 315}
    assert expected == {f"DK4_MES_B{b}_R{n:04d}" for b, n in LINES} | set(EXCLUDED)
    records = []
    for (b, n), text in LINES.items():
        row_id = f"DK4_MES_B{b}_R{n:04d}"
        raw = bytes.fromhex(source[row_id]["source_hex"])
        assert raw.count(b"FI") == text.count("{MACRO:FI}"), row_id
        safe = text.replace("{MACRO:FI}", "")
        assert "I" not in safe and "F" not in safe, row_id
        state = raw[0] in STATES
        records.append({"id": row_id, "english": (f"{{SPEAKER:{raw[0]:02X}}}" if state else "") + text + "{PAD}", "speaker": "Lil" if raw[0] == 2 else "Companion or hostess", "context": "Dark forest, Climb down/Detour branches, crumbling slope, injuries and one-day detour; ancient pictorial-map rumor.", "source_meaning": text, "source_japanese": raw[int(state):].decode("shift_jis", errors="replace"), "localization_note": "Natural English retains map requirement, dark dense forest, descent and detour choices, all footing warnings, injuries, one-day delay and ruins/map rumor. Bare Japanese 8949/9F54 retained as prose; real speaker 97 preserved.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
    batch = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-v117-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "Complete B314-B315 dark forest branches and pictorial-map rumor.", "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {str(b): sum(bb == b for bb, _ in LINES) for b in (314, 315)}}, "excluded_records": EXCLUDED, "records": records}
    (ROOT / "translations/lil_deep_route_v117.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote Lil V117: {len(records)} records")


if __name__ == "__main__":
    main()
