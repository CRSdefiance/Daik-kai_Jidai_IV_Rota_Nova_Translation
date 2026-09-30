from __future__ import annotations

import csv
import json

from scripts.materialize_lil_deep_route_v107 import ROOT, SC2_SHA256

LINES = {
    (295, 5): "We'd like you to find an item.",
    (295, 8): "His Majesty will host a vassal king soon. He plans to show his collection to the honored guest.",
    (295, 11): "Collection?",
    (295, 15): "His Majesty collects rarities from around the world. There's one item he wants before the unveiling.",
    (295, 18): "What's that?",
    (295, 22): "The Heavenly Wristband. Said to grant its bearer exceptional leadership.",
    (295, 26): "Hmm.",
    (295, 30): "Probably to show off the Ottoman Empire's majesty.",
    (295, 33): "Majesty... Kings everywhere are so vain, aren't they?",
    (295, 37): "Heard he'll even postpone the ceremony until it's found.",
    (295, 40): "Seriously?! Like a child...",
    (295, 43): "Don't say that. Please find it and bring it here. We only need to borrow it for one day!",
    (295, 46): "Rumor puts it in the New World. Counting on you!",
    (296, 18): "Where's the Heavenly Wristband? The New World's a big place...",
    (296, 23): "This Heavenly Wristband must reach Constantinople's guild soon.",
    (296, 39): "Still no Heavenly Wristband?",
    (297, 5): "Oh, you found it! Thank you. Please wait just one day.",
    (297, 13): "His Majesty was delighted! You made me look good, too! Here's a generous reward!",
    (297, 16): "Received 25,000 gold coins.",
    (297, 40): "Share in Constantinople rose a little!",
    (297, 51): "Anything you want to know about this town? Just ask.",
    (297, 54): "Ruins? A real gem here. Let me guide you!",
    (298, 6): "Constantinople's guild is looking for you.",
}
SPEAKERS = {2: "Lil", 0x5F: "Sailor", 0x94: "Guild master", 0xFE: "System"}


def main() -> None:
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {i for i in source if 295 <= int(i.split("_B")[1].split("_")[0]) <= 298}
    assert expected == {f"DK4_MES_B{b}_R{n:04d}" for b, n in LINES}
    records = []
    for (b, n), text in LINES.items():
        row_id = f"DK4_MES_B{b}_R{n:04d}"
        raw = bytes.fromhex(source[row_id]["source_hex"])
        assert raw[0] in SPEAKERS and "I" not in text and "F" not in text, row_id
        records.append({"id": row_id, "english": f"{{SPEAKER:{raw[0]:02X}}}" + text + "{PAD}", "speaker": SPEAKERS[raw[0]], "context": "Complete Ottoman emperor collection quest, Heavenly Wristband loan for one day, 25,000 gold, Constantinople share and ruins guide.", "source_meaning": text, "source_japanese": raw[1:].decode("shift_jis", errors="replace"), "localization_note": "Natural English retains the emperor's ceremony, vassal king, leadership item, one-day loan and wait, full reward, share and guide. Uses established Heavenly Wristband item name and Constantinople city alias to avoid capital I macro byte.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
    batch = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-v111-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "Complete B295-B298 Heavenly Wristband guild quest.", "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {str(b): sum(bb == b for bb, _ in LINES) for b in range(295, 299)}}, "excluded_records": {}, "records": records}
    (ROOT / "translations/lil_deep_route_v111.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote Lil V111: {len(records)} records")


if __name__ == "__main__":
    main()
