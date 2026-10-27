from __future__ import annotations

import csv
import json

from scripts.materialize_lil_deep_route_v107 import ROOT, SC2_SHA256

LINES = {
    (289, 6): "Oh, {MACRO:FI}! Welcome.",
    (289, 9): "Ruins? Never heard of any near this town.",
    (289, 12): "You seek the ancient kingdom's temple?",
    (289, 15): "Huh? Who are you?",
    (289, 19): "Oh, {MACRO:FI}! He's the local elder!",
    (289, 30): "S-sorry! {MACRO:FI}, apologize too!",
    (289, 36): "Ho ho ho! No harm done.",
    (289, 39): "You should be able to find it. But...",
    (289, 43): "But?",
    (289, 47): "Oh, never mind. Ho ho ho!",
    (289, 50): "How odd.",
    (290, 5): "Ugh, no good! No idea! What's Angkor's riddle supposed to mean?!",
    (290, 9): "'Adorn me in a new star's pure glow'... Right? What does that mean?",
    (290, 13): "At the start... He said he had gold like the sun and silver like the moon, right?",
    (290, 17): "Yes. Then he said, 'Yet a star's light remains unknown to me.'",
    (290, 21): "So not gold or silver... Does 'star' mean a metal more precious than those?",
    (290, 30): "Admiral, the Alchemy Book reportedly describes an element no one's ever seen.",
    (290, 34): "Really?!",
    (290, 38): "Heard the alchemist who wrote it sailed to the New World.",
    (290, 42): "No one knows it? A clue! That must be it!",
    (290, 46): "Sun for gold, moon for silver... The star may be platinum! My long search could be over...",
    (290, 50): "Platinum?! No idea what that is, but it must be it!!",
    (290, 54): "You know, from that Alchemy Book...",
    (290, 57): "Oh, that! Let's take platinum aboard!",
    (290, 61): "Yes. Should be mined in southern Africa.",
    (291, 5): "Ugh! Angkor's riddle has me stumped!",
    (291, 8): "'Adorn me in a new star's pure glow'... Meaning?",
    (291, 11): "Sun for gold, moon for silver?",
    (291, 14): "Yes, that's what he said.",
    (291, 18): "Then the star?",
    (291, 22): "That's the puzzle. Solve that, and we have our answer...",
    (291, 25): "He has gold and silver, yet no star's light. A very rare precious metal, then?",
    (291, 28): "Could that be platinum?",
    (291, 37): "Platinum? What is it?",
    (291, 40): "A precious metal mined nearby. But you need a certain book first.",
    (291, 44): "What book?",
    (291, 48): "A book about alchemy. By a man who sailed to the New World over a decade ago, they say.",
    (291, 52): "New World",
    (291, 58): "Platinum?! Oh, from the alchemy book!! That must be it!",
    (291, 62): "Then we need to take platinum aboard!",
    (291, 65): "Platinum's mined here in Africa. Be sure to buy some!",
    (292, 13): "Adorn me in a new star's pure glow.",
    (292, 17): "A new star's light... What should we bring?",
    (292, 31): "Heave, ho!",
    (292, 35): "Brought platinum... Will this do?",
    (292, 46): "Sage, bearing a new star's pure glow!",
    (292, 50): "Stir a storm at sea with thy wisdom! Then grant me peaceful sleep!",
    (292, 56): "This coin's really old...",
    (292, 68): "What did those words mean?",
    (292, 72): "Who knows? That voice did sound pleased, though.",
    (292, 76): "Yes. This coin's sure to come in handy someday.",
}
STATES = {0x02, 0x09, 0x12, 0x68, 0x97, 0xAA, 0xC7, 0xFE}
EXCLUDED = {
    "DK4_MES_B292_R0003": "Packed Angkor event 20 46 94 80; identical SC3 B263 R0002; preserve unchanged.",
    "DK4_MES_B292_R0047": "Packed Angkor reward event 20 46 94 80 15 62; same event prefix as R0003 with trailing operation payload; no Japanese prose; preserve unchanged.",
}


def main() -> None:
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {i for i in source if 289 <= int(i.split("_B")[1].split("_")[0]) <= 292}
    assert expected == {f"DK4_MES_B{b}_R{n:04d}" for b, n in LINES} | set(EXCLUDED)
    records = []
    for (b, n), text in LINES.items():
        row_id = f"DK4_MES_B{b}_R{n:04d}"
        raw = bytes.fromhex(source[row_id]["source_hex"])
        assert raw[0] in STATES, row_id
        prose = text
        for macro in ("FI", "FA", "FO"):
            assert raw.count(macro.encode()) == text.count(f"{{MACRO:{macro}}}"), row_id
            prose = prose.replace(f"{{MACRO:{macro}}}", "")
        assert "I" not in prose and "F" not in prose, row_id
        records.append({"id": row_id, "english": f"{{SPEAKER:{raw[0]:02X}}}" + text + "{PAD}", "speaker": {2: "Lil", 9: "Kamil", 0x12: "Companion", 0x68: "Market keeper", 0x97: "Companion", 0xAA: "Village elder", 0xC7: "Tavern hostess", 0xFE: "Temple voice"}[raw[0]], "context": "Complete Angkor temple platinum riddle, both explanation branches, Alchemy Book and New World lead, platinum offering and ancient coin reward.", "source_meaning": text, "source_japanese": raw[1:].decode("shift_jis", errors="replace"), "localization_note": "Natural source-reviewed English keeps the star clue identical across branches, gold/sun and silver/moon pairing, platinum and book requirement, southern Africa and New World directions, and exact macros.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
    batch = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-v109-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "Complete B289-B292 Angkor temple riddle.", "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {str(b): sum(bb == b for bb, _ in LINES) for b in range(289, 293)}}, "excluded_records": EXCLUDED, "records": records}
    (ROOT / "translations/lil_deep_route_v109.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote Lil V109: {len(records)} records")


if __name__ == "__main__":
    main()
