"""Restore all B4 native groups containing missing descriptions or prompts."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

PROSE = {
    248: ("Black or green pearls from black-lipped oysters, prized for their mysterious colors and deep luster.", "Black or green pearls taken from black-lipped pearl oysters; their mysterious colors and deep luster are considered attractive."),
    249: ("Caviar from sturgeon in Lake Baikal, not far from the upper reaches of the Yenisei River.", "Caviar from sturgeon living in Lake Baikal, relatively near the upper Yenisei River."),
    254: ("Small tomatoes with a distinctive taste and flavor. They fetch high prices in their native Andes region.", "A small-fruited tomato variety with distinctive taste and flavor. Traded at high prices in the Andes, its place of origin."),
    255: ("Salted salmon dried in smoke from burning oak chips and similar woods. It has a distinctive smoky flavor.", "Salted salmon is dried while smoked over chips of deciduous or evergreen oak and similar woods; it has a distinctive aroma and flavor."),
    259: ("Fire opal, a gem as red as flames. It is thought to be volcanic in origin.", "Fire opal is a gemstone with a flame-red color and is believed to be a volcanic opal."),
    260: ("New Zealand honey with strong antibacterial properties, long prized as a remedy for burns, wounds and sore throats.", "Honey unique to New Zealand; strong antibacterial properties have made it valued as an effective remedy for burns, wounds and sore throats."),
    269: ("Choose the ship whose captain you want to change.", "Select the ship for which the captain will be changed."),
    270: ("Assign a subordinate as captain.", "Entrust the captain's position to a subordinate."),
    271: ("Choose a crew member to serve as captain.", "Select the crew member to appoint as captain."),
    272: ("Changing your flagship may remove crew members from their assigned rooms.", "Changing the flagship can result in room assignees being dismissed from those duties."),
    291: ("%s and the others gained valuable firsthand experience of a new culture.", "The named character and companions had the valuable experience of encountering a new culture firsthand."),
    292: ("This discovery seems to be the talk of the trend-conscious people of %s.", "This discovery appears to be a topic of conversation among people attentive to trends in the named city."),
    294: ("After enduring hunger, %s and the others glimpsed a new state of awareness.", "After enduring hunger, the named character and companions were able to glimpse a new realm or state of understanding. Nearby discovery messages concern spiritual experiences."),
    295: ("%s and the others got a strenuous workout on land for the first time in a while.", "The named character and companions performed strenuous exercise on land for the first time in a long while."),
    296: ("Is %s all right?", "Confirmation asking whether the substituted selection is acceptable."),
    297: ("Discovered %s.", "The substituted discovery has been found."),
    298: ("Stop automatic movement?", "Asks whether to cancel automatic movement."),
    299: ("You can't place it here.", "The selected object or assignee cannot be placed here; the source does not identify a specific type."),
    314: ("You obtained a young shark!", "The player obtained a juvenile shark."),
    315: ("You can't reassign sailors during battle!", "Sailor allocation cannot be changed during combat."),
    316: ("Save the ending data?", "Asks whether to save ending data."),
    317: ("You can't change figureheads while at sea.", "Figureheads cannot be changed at sea."),
    318: ("This is exhibition data. If you quit the game, the data will be lost. Proceed?", "This is fair/exhibition data; interrupting the game will cause it to be lost. Asks whether this is acceptable. Actual DS use is unclassified."),
    326: ("You don't have any items.", "No items are possessed."),
    327: ("%s equipped %s.", "The first substituted person has equipped the second substituted item."),
    332: ("Vibration is currently %s. Change it to %s?", "States the current vibration setting, then asks whether to change it to the second substituted setting."),
    333: ("Quick Guide automatic display is %s. Change it to %s?", "States the current Quick Guide automatic-display setting, then asks whether to switch to the second setting."),
    334: ("%s is under attack by %s's fleet!", "The first substituted city is being attacked by the fleet belonging to the second substituted name."),
    335: ("%s leveled up!!", "The named person has gained a level, with emphatic double exclamation."),
    336: ("%s increased by %s!", "The first substituted attribute increased by the second substituted amount."),
}


REVISIONS = {
    248: "Pearls from black-lipped oysters. Black or green, their mysterious hues and deep luster are prized.",
    249: "Caviar from sturgeon in Lake Baikal, near the upper Yenisei River.",
    254: "Small tomatoes with a unique taste and flavor. They fetch high prices in their native Andes.",
    255: "Salted salmon with a unique aroma and flavor, smoked and dried over oak chips or similar wood.",
    259: "Fire opal, a flame-red gem thought to have volcanic origins.",
    271: "Choose a crew member as captain.",
    272: "Changing your flagship may cancel the crew's room assignments.",
    291: "%s and companions gained valuable experience by encountering a new culture firsthand.",
    292: "This discovery seems to have people who follow trends in %s talking.",
    294: "Enduring hunger gave %s and companions a glimpse of a new state of awareness.",
    315: "You can't change sailor assignments during battle!",
    317: "At sea, you can't change figureheads.",
    332: "Vibration is %s. Change it to %s?",
}


def main() -> None:
    clean = NdsImage.open("work/clean.nds")
    entries = common_message_entries(clean.read_file("/COMMON/MESFILE.DK4"), clean.read_file("/__arm9__.bin"))
    pending = json.loads(Path("work/analysis/common_blank_remaining_v106_source_entries.json").read_text(encoding="utf-8"))
    required = {row["message_id"] for row in pending if row["block"] == 4}
    if required != PROSE.keys():
        raise ValueError("Cover every native neighbor of every missing B4 group")
    records = []
    for message_id, (english, gloss) in PROSE.items():
        english = REVISIONS.get(message_id, english)
        source = entries[message_id]
        records.append({
            "id": f"COMMON_MESSAGE_{message_id:04d}", "message_id": message_id,
            "block": source.block, "record": source.record_index,
            "source_hex": source.text.hex().upper(), "japanese": source.text.decode("cp932"),
            "english": english.replace("I", "Ｉ").replace("F", "Ｆ") + "{PAD}",
            "source_meaning": gloss, "speaker": "System or discovery narrator",
            "context": f"Independent native message {message_id}, COMMON B4 R{source.record_index}; commodity, ship assignment, discovery or system prompt. Packed neighbors are separate messages.",
            "previous_japanese": entries[message_id - 1].text.decode("cp932"),
            "next_japanese": entries[message_id + 1].text.decode("cp932"),
            "localization_note": "Fresh clean-source prose retains properties, origins, uncertainty, firsthand experience, timing and questions. All printf arguments retain source order. No object type or ownership is invented where the source is generic. Nara/kashi become oak naturally; fair data becomes exhibition data, retaining inherited platform terminology for later visibility classification. Reserved I/F use existing full-width Latin glyphs. Complete repack and exact-font review are required.",
            "review": {"source": True, "context": True, "localization": True,
                       "naturalness": True, "formatting": False},
        })
    Path("translations/common_blank_b4_manuscript_v1.json").write_text(json.dumps({
        "format": "dk4-common-entry-manuscript-v1", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "encoder": "dialogue-fixed-v1",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "status": "draft-awaiting-native-repack-and-formatting-review", "records": records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(records)} source-reviewed B4 entries; formatting pending")


if __name__ == "__main__":
    main()
