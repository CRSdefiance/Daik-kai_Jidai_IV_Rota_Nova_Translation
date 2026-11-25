"""Restore missing native town rumors and recommendation-letter explanations."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

PROSE = {
    713: ("They say Admiral Albuquerque's ancestor won great renown commanding Portuguese fleets in the Indian Ocean long ago.", "Admiral Albuquerque's ancestor is said to have commanded Portuguese fleets in the Indian Ocean long ago and performed outstandingly."),
    714: ("Admiral Valdes's Spanish navy is called the Invincible Armada for its formidable array of ships.", "The Spanish navy led by Admiral Valdes is called the Invincible Armada because of its substantial, formidable force composition."),
    716: ("Athens still has plenty of profitable trade goods, as always.", "Athens continues, as usual, to be blessed with profitable trading commodities."),
    717: ("The Ottoman Empire controls the eastern Mediterranean.", "The Ottoman Turkish Empire holds control of the eastern Mediterranean."),
    722: ("Nagalpur can sit back and let the money roll in. I can't help envying him!", "Nagalpur occupies a position where money flows in while he lives comfortably and idly; the speaker is intensely envious. No rank or relationship is added for danna."),
    723: ("Admiral Pereira is a tough, fiercely patriotic man, but utterly ruthless toward anyone outside his own circle.", "Admiral Pereira is a stern/tough man overflowing with patriotism, but thoroughly merciless to everyone except his own companions."),
    725: ("They say an empress would ruin China. I disagree. I wish the female admiral who routs Japanese pirates were our emperor...", "In China it is said that a female emperor would ruin the country, but the speaker does not believe it. Wishes that the female admiral who drives off the wako were this country's emperor."),
    726: ("Hideyoshi or Kurushima, it makes no difference. I'll drive them off every time they come!", "Whether it is Hideyoshi or Kurushima, the speaker will drive them off no matter how many times they come."),
    727: ("They say Kurushima became obsessed with the power of ironclad ships after Nobunaga defeated him.", "Since his defeat by Nobunaga, Kurushima is said to have become fascinated and captivated by the strength of iron-armored ships. No invented rank from oyabun."),
    728: ("Maldonado can't resist gold or anything that glitters.", "Maldonado has a weakness for gold and shiny valuables; the familiar oyabun does not establish a family relationship or formal rank."),
    730: ("One of the goods in %s is sure to become popular soon.", "The speaker predicts confidently that one of the items within the substituted category/list will become fashionable from now on."),
    731: ("I think %s will sell well.", "The speaker thinks the substituted commodity will sell."),
    734: ("I'd better make plenty of money before this fad fades. Oh, there's so much to do!", "The speaker must earn well before the trend dies out and exclaims at being busy."),
    735: ("Thanks to you, everyone will recover from their illness!", "Because of the player, everyone's illness will be cured; this is prospective, not an already completed recovery."),
    742: ("Hey, could you give me that? With that %s, I think %s could become a local specialty here. What do you say?", "Asks the player to give over the item. With the first substituted item, the speaker believes the second substituted product can become this city's specialty. Ends with a question."),
    743: ("Really? You're a good person. You're the best!", "An enthusiastic reaction: really? The player is a good person and the best."),
    777: ("Oh, you have a letter of introduction! I'll add a few words to turn it into a letter of recommendation.", "Notices the player has an introduction letter and offers to add writing to make it a recommendation letter."),
    778: ("I know! To thank you for selling us so many trendy goods, I'll write you a letter of recommendation.", "The speaker has an idea: write a recommendation letter as thanks for the large amount of fashionable goods sold."),
    779: ("Take it to a palace or governor's office in a small town. They should grant you some market share.", "Taking that letter to the palace or governor's office of a small town should result in an allocation of market share."),
    780: ("Take it to a palace or governor's office in any town. They should grant you some market share.", "Taking that letter to a palace or governor's office should obtain an allocation of market share regardless of town size."),
}


REVISIONS = {
    713: "They say Admiral Albuquerque's ancestor distinguished himself long ago commanding Portuguese fleets across the Indian Ocean.",
    714: "Admiral Valdes's Spanish navy has such formidable ships that it's called the Invincible Armada.",
    716: "Athens is still rich in profitable trade goods, as always.",
    717: "The Ottoman Empire rules the eastern Mediterranean.",
    722: "Nagalpur can sit back as money rolls in. I can't help envying him!",
    723: "Admiral Pereira is tough and fiercely patriotic, but merciless to anyone outside his circle.",
    725: "They say an empress would ruin China. I disagree. If only that female admiral who routs Japanese pirates were our emperor...",
    730: "One of the goods in %s will surely become popular soon.",
    742: "Hey, would you give me that %s? I think it could make %s a local specialty here. What do you say?",
    777: "You have a letter of introduction! With a few words of mine, it can become a letter of recommendation.",
}


def main() -> None:
    clean = NdsImage.open("work/clean.nds")
    entries = common_message_entries(clean.read_file("/COMMON/MESFILE.DK4"), clean.read_file("/__arm9__.bin"))
    pending = json.loads(Path("work/analysis/common_blank_remaining_v108_source_entries.json").read_text(encoding="utf-8"))
    required = {row["message_id"] for row in pending if row["block"] in {9, 10}}
    if required != PROSE.keys():
        raise ValueError("Cover every native neighbor of every missing B9/B10 group")
    records = []
    for message_id, (english, gloss) in PROSE.items():
        english = REVISIONS.get(message_id, english)
        source = entries[message_id]
        records.append({
            "id": f"COMMON_MESSAGE_{message_id:04d}", "message_id": message_id,
            "block": source.block, "record": source.record_index,
            "source_hex": source.text.hex().upper(), "japanese": source.text.decode("cp932"),
            "english": english.replace("I", "Ｉ").replace("F", "Ｆ") + "{PAD}",
            "source_meaning": gloss, "speaker": "Townsperson or trading contact",
            "context": f"Independent native town message {message_id}, COMMON B{source.block} R{source.record_index}; political or commodity rumor, gift reaction or letter explanation. Packed neighbors are separate messages.",
            "previous_japanese": entries[message_id - 1].text.decode("cp932"),
            "next_japanese": entries[message_id + 1].text.decode("cp932"),
            "localization_note": "Fresh clean-source English preserves hearsay, conjecture, continuing conditions, enemies, empathy, future cure, gratitude and item argument order. Introduction and recommendation letters remain distinct, as do small-town and all-town benefits. Character names follow existing route spellings. Familiar danna/oyabun address does not invent kinship or rank. Reserved I/F use existing full-width Latin glyphs; complete repack and exact-font review required.",
            "review": {"source": True, "context": True, "localization": True,
                       "naturalness": True, "formatting": False},
        })
    Path("translations/common_blank_b9_b10_manuscript_v1.json").write_text(json.dumps({
        "format": "dk4-common-entry-manuscript-v1", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "encoder": "dialogue-fixed-v1",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "status": "draft-awaiting-native-repack-and-formatting-review", "records": records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(records)} source-reviewed B9/B10 entries; formatting pending")


if __name__ == "__main__":
    main()
