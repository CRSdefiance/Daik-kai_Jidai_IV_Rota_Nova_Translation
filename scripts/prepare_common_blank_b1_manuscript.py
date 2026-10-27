"""Restore every native neighbor of B1's blank save/status/commodity messages."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

PROSE = {
    108: ("Game saves need four free blocks. You can't save right now. Start playing anyway?", "Game data needs four free blocks. Saving is currently impossible, and the player is asked whether to begin anyway."),
    109: ("One free block is required to save system data. You can't save right now. Start the game anyway?", "System data needs one free block. Saving is currently impossible, and the player is asked whether to begin anyway."),
    110: ("Saving requires five free blocks. You can't save right now. Start playing anyway?", "Saving data needs five free blocks. Saving is currently impossible, and the player is asked whether to begin anyway."),
    111: ("There's no game data to load.", "There is no game data, so it cannot be loaded."),
    115: ("There aren't enough free blocks. Saving requires five.", "There is insufficient free storage; saving needs five free blocks."),
    116: ("Checking the memory card. Please don't insert or remove the memory card or controller.", "While the memory card is being checked, the player must not insert or remove the memory card or controller."),
    124: ("You can format the memory card when you save. Start the game?", "Memory card initialization can be performed when saving; the player is asked whether to start the game."),
    125: ("Thanks to substantial commercial investment, %s's economy has recovered.", "Large commercial investment has caused the substituted city's economic conditions to recover."),
    126: ("Substantial commercial investment has brought an economic boom to %s.", "Large commercial investment has caused the substituted city to enjoy a thriving economy."),
    140: ("A New World vegetable with edible underground stem tubers. It tastes mild and is prepared in many ways. Some regions use it as a staple.", "This vegetable has edible underground stem tubers, originates in the New World, tastes mild, supports many cooking methods and also serves as a staple in some regions."),
    141: ("Soybeans used to make tofu, miso and other foods. They're said to have come from northern China.", "Soybean seeds are ingredients for tofu, miso and similar foods; their origin is said to be northern China."),
    150: ("A seasoning essential to the body. It draws out moisture and helps prevent spoilage.", "This seasoning is physiologically indispensable to the human body and has dehydrating and preservative effects."),
    151: ("Oil from olives common on Mediterranean coasts. Used to pack anchovies in oil, it oxidizes easily and isn't suited to frying.", "Oil from olives common on the Mediterranean coast; frequently used for anchovies preserved in oil, easily oxidized, and unsuitable for fried foods according to the source."),
    152: ("Oil pressed from coconut flesh, known as coconut oil. Used in food and industry.", "Oil extracted from the coconut fruit's endosperm, also called coconut oil, used as edible and industrial fats/oils."),
    153: ("Native to southern China, this fruit has white, jellylike flesh and is used in Chinese desserts.", "The fruit is white and jellylike, originates in southern China, and is used in Chinese-cuisine desserts."),
}


def main() -> None:
    clean = NdsImage.open("work/clean.nds")
    entries = common_message_entries(clean.read_file("/COMMON/MESFILE.DK4"), clean.read_file("/__arm9__.bin"))
    inventory = json.loads(Path("work/analysis/common_native_v103.json").read_text(encoding="utf-8"))
    owners = {(entry["block"], entry["record"]) for entry in inventory["blank_native_messages"] if entry["block"] == 1}
    required = {entry.message_id for entry in entries if (entry.block, entry.record_index) in owners}
    if required != PROSE.keys():
        raise ValueError("B1 manuscript must cover every native neighbor of every blank record")
    records = []
    for message_id, (english, gloss) in PROSE.items():
        source = entries[message_id]
        records.append({
            "id": f"COMMON_MESSAGE_{message_id:04d}", "message_id": message_id,
            "block": source.block, "record": source.record_index,
            "source_hex": source.text.hex().upper(), "japanese": source.text.decode("cp932"),
            "english": english.replace("I", "Ｉ").replace("F", "Ｆ") + "{PAD}",
            "source_meaning": gloss, "speaker": "System prompt or commodity description narrator",
            "context": f"Independent native message {message_id}, COMMON B1 R{source.record_index}; source save-system wording, investment status or commodity description. Packed neighbors are separate messages.",
            "previous_japanese": entries[message_id - 1].text.decode("cp932"),
            "next_japanese": entries[message_id + 1].text.decode("cp932"),
            "localization_note": "Fresh clean-source English retains block counts, device names, yes/no prompts, commercial investment, uncertainty, origins, food preparation and industrial uses. Coconut flesh expresses endosperm naturally. Historical source claims are translated faithfully; inherited platform wording is not silently changed. Reserved capital I/F use existing full-width Latin glyphs. Full native repack and preview review are required.",
            "review": {"source": True, "context": True, "localization": True,
                       "naturalness": True, "formatting": False},
        })
    path = Path("translations/common_blank_b1_manuscript_v1.json")
    path.write_text(json.dumps({
        "format": "dk4-common-entry-manuscript-v1", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "encoder": "dialogue-fixed-v1",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "status": "draft-awaiting-native-repack-and-formatting-review", "records": records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(records)} source-reviewed B1 entries; formatting remains pending")


if __name__ == "__main__":
    main()
