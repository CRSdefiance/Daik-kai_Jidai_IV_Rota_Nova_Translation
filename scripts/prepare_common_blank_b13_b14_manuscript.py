"""Restore complete native tavern and diplomatic-message groups in B13/B14."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

PROSE = {
    1063: ("Even if you grew up in a cultured country, you're a barbarian if you settle things by force. I hate people like that.", "Even someone born and raised in a culturally advanced country is a barbarian if they try to solve matters by force. The speaker strongly dislikes such people."),
    1064: ("Hehe... I'll get scolded for drinking too much again... But I'll have another drink anyway!", "A playful laugh, anticipation of being scolded again for drinking too much, then a decision to drink anyway."),
    1065: ("They say I go for looks, but I just love a romantic mood. If someone's not my type, though, where's the romance?", "The speaker is often called someone who judges romantic partners by looks, but says they are really susceptible to the mood. Then asks how there could be any mood if the person's face is not to their taste. No partner gender is specified."),
    1123: ("Don't worry. I'll see that it gets delivered.", "An informal reassurance that the speaker will deliver the letter properly."),
    1124: ("Admiral, there's no faction in these waters we can send a diplomatic letter to.", "A polite crew report that this sea region has no faction to which negotiation documents can be delivered."),
    1128: ("Come to think of it, there's no one in these waters we can send a diplomatic letter to.", "An informal voice recalls there is no recipient in this sea region to whom a negotiation letter can be sent."),
    1129: ("Well now, there are no factions in these waters we can deliver diplomatic letters to.", "An older, formal voice realizes there is no faction in this sea region to which negotiation documents can be delivered."),
    1130: ("Sorry, all the couriers are out right now. Give us five or six days.", "An informal apology: couriers are currently all out on deliveries; asks the player to wait five or six days."),
    1131: ("There's no faction for us to oppose together.", "There is no faction that can be opposed jointly; the source describes an absence of a common target, not an absence of an ally."),
    1132: ("We have no enemy to oppose together.", "A formal voice states there is no enemy to oppose jointly."),
    1136: ("There's nobody we can team up against.", "An informal voice states there is no opponent to defeat by cooperating."),
    1137: ("There is no enemy for us to face together.", "An older, polite voice states there is no enemy to oppose jointly."),
}


REVISIONS = {
    1064: "Hehe... Too much drinking again... They'll scold me, but I'll drink!",
    1128: "Right, nobody in these waters can receive a diplomatic letter.",
    1129: "Well now, no faction in these waters can receive diplomatic letters.",
    1130: "Sorry, the couriers are all out now. Please wait five or six days.",
    1136: "We have no common enemy to beat.",
}


def main() -> None:
    clean = NdsImage.open("work/clean.nds")
    entries = common_message_entries(clean.read_file("/COMMON/MESFILE.DK4"), clean.read_file("/__arm9__.bin"))
    pending = json.loads(Path("work/analysis/common_blank_remaining_v110_source_entries.json").read_text(encoding="utf-8"))
    required = {row["message_id"] for row in pending if row["block"] in {13, 14}}
    if required != PROSE.keys():
        raise ValueError("Cover every native neighbor of every missing B13/B14 group")
    records = []
    for message_id, (english, gloss) in PROSE.items():
        english = REVISIONS.get(message_id, english)
        source = entries[message_id]
        records.append({
            "id": f"COMMON_MESSAGE_{message_id:04d}", "message_id": message_id,
            "block": source.block, "record": source.record_index,
            "source_hex": source.text.hex().upper(), "japanese": source.text.decode("cp932"),
            "english": english.replace("I", "Ｉ").replace("F", "Ｆ") + "{PAD}",
            "source_meaning": gloss, "speaker": "Tavern contact or diplomatic crew voice",
            "context": f"Independent native message {message_id}, COMMON B{source.block} R{source.record_index}; tavern small talk, courier or diplomatic warning. Packed neighbors are separate messages and voice variants.",
            "previous_japanese": entries[message_id - 1].text.decode("cp932"),
            "next_japanese": entries[message_id + 1].text.decode("cp932"),
            "localization_note": "Fresh clean-source English retains condemnation, playful drinking, romantic self-contradiction, reassurance, geographic scope, faction/recipient roles and the five-or-six-day wait. Joint-opposition warnings describe absence of a common enemy rather than absence of an ally. No gender or kinship is invented. Songlike emphasis is conveyed through prose tone. Reserved I/F use existing full-width Latin glyphs; native repack and every exact-font preview require review.",
            "review": {"source": True, "context": True, "localization": True,
                       "naturalness": True, "formatting": False},
        })
    Path("translations/common_blank_b13_b14_manuscript_v1.json").write_text(json.dumps({
        "format": "dk4-common-entry-manuscript-v1", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "encoder": "dialogue-fixed-v1",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "status": "draft-awaiting-native-repack-and-formatting-review", "records": records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(records)} source-reviewed B13/B14 entries; formatting pending")


if __name__ == "__main__":
    main()
