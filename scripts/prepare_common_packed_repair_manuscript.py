"""Prepare clean-source prose for four packed defects and three B33 messages."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

PROSE = {
    889: ("Admiral, we're short on funds...", "The speaker tells the admiral there is insufficient money, trailing off politely."),
    890: ("We'll recruit sailors for %s coins.", "Sailors will be recruited for the substituted number of gold coins."),
    1845: ("Ｉ feel fantastic right now!", "The speaker is in exceptionally high spirits right now; the musical note conveys a cheerful tone."),
    1846: ("Ｉ just can't get motivated...", "The speaker cannot find the motivation to do anything, trailing off."),
    1982: ("An afterimage!", "An emphatic exclamation identifying an afterimage."),
    1983: ("White Tree Sword Style: The Twin Shadow Array!", "The speaker calls out the White Tree school of swordsmanship's Twin Shadow Formation technique."),
    2508: ("They don't seem to need it right now, though...", "It seems they do not need the item now, but the speaker leaves the thought open."),
    2509: ("We gave the sailors %s.", "The sailors were given the substituted item or quantity."),
    3034: ("Ｉ think it would grow well around the Mediterranean.", "The speaker thinks the crop would grow successfully if introduced around the Mediterranean."),
    3036: ("Honey from Mediterranean flowers must taste good too.", "The speaker expects honey made from flowers blooming in the Mediterranean to taste good as well."),
    3037: ("Ｉ hear they eat shark fins in China and shark eggs around the Black Sea, beyond the Mediterranean.", "The speaker has heard that shark fins are eaten in China and shark eggs around the Black Sea, beyond the Mediterranean."),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", type=int, choices=(1, 2), default=1)
    args = parser.parse_args()
    clean = NdsImage.open("work/clean.nds")
    entries = common_message_entries(clean.read_file("/COMMON/MESFILE.DK4"), clean.read_file("/__arm9__.bin"))
    records = []
    prose = dict(PROSE)
    if args.version == 2:
        prose.update({
            905: ("Ｉ hear %s has been going through quite a %s lately.", "The speaker has heard that the substituted city has recently been experiencing a major instance of the substituted condition."),
            906: ("Word is, %s's been having one heck of a %s lately.", "An informal speaker reports that the substituted city has lately been experiencing quite an extreme instance of the substituted condition."),
            907: ("Whoa!", "A short surprised exclamation."),
            908: ("Disrupting the enemy will cost about 1,000 coins. What kind of scheme do you have in mind?", "Disrupting the enemy costs approximately one thousand gold coins; the speaker asks what plan the player wants to carry out."),
        })
    for message_id, (english, gloss) in sorted(prose.items()):
        source = entries[message_id]
        records.append({
            "id": f"COMMON_MESSAGE_{message_id:04d}", "message_id": message_id,
            "block": source.block, "record": source.record_index,
            "source_hex": source.text.hex().upper(), "japanese": source.text.decode("cp932"),
            "english": english + "{PAD}", "source_meaning": gloss,
            "speaker": "Shared response speaker" if message_id < 3034 else "Item appraiser",
            "context": f"COMMON B{source.block} R{source.record_index}; independently selected native message {message_id}. Adjacent entries are distinct messages, not one paragraph.",
            "previous_japanese": entries[message_id - 1].text.decode("cp932"),
            "next_japanese": entries[message_id + 1].text.decode("cp932"),
            "localization_note": "Fresh clean-source localization retains facts, uncertainty, tone and substitutions. Existing merged English is rejected. The musical note is expressed through cheerful wording. Full-width Latin I prevents an executable ASCII I command. Formatting awaits a complete pointer-aware repack and preview review.",
            "review": {"source": True, "context": True, "localization": True,
                       "naturalness": True, "formatting": False},
        })
    payload = {"format": "dk4-common-entry-manuscript-v1", "translation_policy": "natural-dialogue-v2",
               "target_locale": "en-US", "encoder": "dialogue-fixed-v1",
               "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
               "status": "draft-awaiting-native-repack-and-formatting-review", "records": records}
    path = Path(f"translations/common_packed_native_repair_manuscript_v{args.version}.json")
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(records)} clean-source entries; formatting gate remains pending")


if __name__ == "__main__":
    main()
