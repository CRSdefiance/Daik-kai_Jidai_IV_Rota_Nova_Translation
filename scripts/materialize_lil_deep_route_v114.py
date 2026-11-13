from __future__ import annotations

import csv
import json

from scripts.materialize_lil_deep_route_v107 import ROOT, SC2_SHA256

LINES = {
    (306, 12): "Got a map?",
    (306, 16): "Oh, forgot!",
    (306, 30): "We'll part here. Travel safely!",
    (306, 35): "Yes, thanks!",
    (306, 49): "Let's go, then.",
    (306, 51): "Let's go!",
    (306, 53): "Shall we go?",
    (306, 55): "Let's go.",
    (306, 57): "Shall we go?",
    (306, 59): "Off we go!",
    (306, 61): "Let's go, then.",
    (306, 65): "Huh? There should be a bridge...",
    (306, 78): "Perhaps a flood washed it away.",
    (306, 79): "Perhaps a flood washed it away.",
    (306, 80): "A flood must have washed it away.",
    (306, 83): "Did a flood wash it away?",
    (306, 84): "Perhaps a flood washed it away.",
    (306, 85): "Maybe a flood washed it away?",
    (306, 86): "Perhaps a flood washed it away.",
    (306, 89): "Whoa... Such a fast river! What now?",
    (306, 95): "Bridge",
    (306, 97): "Wade",
    (306, 114): "Admiral, look at the map. A log bridge lies upstream, quite far away.",
    (306, 116): "Admiral, the map shows a log bridge upstream, quite far away.",
    (306, 118): "Hey, the map shows a log bridge upstream! Looks a bit far, though...",
    (306, 120): "Hey, the map shows a log bridge far upstream!",
    (306, 121): "Admiral, look at this map! Seems there's a log bridge upstream! A bit far, though...",
    (306, 123): "The map shows a log bridge upstream. A bit far, though...",
    (306, 125): "Hey, look at the map! There's a bridge upstream, but it's very far away!",
    (306, 127): "The map shows a log bridge upstream. Quite a distance away, though...",
    (306, 133): "The map shows a log bridge upstream. A bit far, but shall we try it?",
    (306, 140): "Better than turning back! Let's head upstream!",
    (306, 149): "One day passed. The sailors seem tired.",
    (306, 155): "Bah, this river's nothing! We'll wade across!",
    (306, 159): "Okay... Huh? Admiral, a ferry!",
    (306, 162): "Oh, how handy! Everyone, take turns crossing on it!",
    (306, 166): "Paid 100 gold coins for the ferry.",
    (306, 174): "All across?",
    (306, 179): "A-Admiral! There!",
}
STATES = {0x02, 0x09, 0x97, 0xCB, 0xD0, 0xFE}
EXCLUDED = {
    "DK4_MES_B306_R0028": "Packed event 05 60 60 46 89 80 3E 63; identical SC0B320R0029, SC1B304R0028 and SC3B274R0027. Preserve unchanged.",
    "DK4_MES_B306_R0063": "Packed river event 1E 63 94 46 8F 80 contains native operation/state bytes and no prose. Preserve unchanged.",
}
PENDING = {"DK4_MES_B306_R0081"}


def main() -> None:
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = {r["id"]: r for r in csv.DictReader(stream)}
    expected = {i for i in source if i.startswith("DK4_MES_B306_")}
    assert expected == {f"DK4_MES_B{b}_R{n:04d}" for b, n in LINES} | set(EXCLUDED) | PENDING
    records = []
    for (b, n), text in LINES.items():
        row_id = f"DK4_MES_B{b}_R{n:04d}"
        raw = bytes.fromhex(source[row_id]["source_hex"])
        assert "I" not in text and "F" not in text, row_id
        state = raw[0] in STATES
        records.append({"id": row_id, "english": (f"{{SPEAKER:{raw[0]:02X}}}" if state else "") + text + "{PAD}", "speaker": "Lil" if raw[0] == 2 else "Companion or guide", "context": "Missing bridge; all companion variants, upstream bridge and wading/ferry branches.", "source_meaning": text, "source_japanese": raw[int(state):].decode("shift_jis", errors="replace"), "localization_note": "Natural English retains map, upstream log bridge, detour day and fatigue, wading alternative, ferry fare of 100 gold and all-crossed check. Bare Japanese 97AC record R0081 is translated separately in V115 to avoid confusion with real state 97 on R0159.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
    batch = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-v114-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "B306 river encounter, except one bare 97AC variant handled in V115.", "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {"306": len(records)}, "pending_records": sorted(PENDING)}, "excluded_records": EXCLUDED, "records": records}
    (ROOT / "translations/lil_deep_route_v114.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote Lil V114: {len(records)} records")


if __name__ == "__main__":
    main()
