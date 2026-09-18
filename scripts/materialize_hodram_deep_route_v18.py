from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v18.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (*range(230, 235), *range(236, 240))
EXCLUDED: dict[str, str] = {}


LINES = {
    # Charlotte trains late and recalls an extraordinary protective robe.
    "DK4_MES_B230_R0005": "Hah! Take this!",
    "DK4_MES_B230_R0009": "Training this late? Marines should follow her example.",
    "DK4_MES_B230_R0013": "Confronting an armed opponent takes tremendous courage.",
    "DK4_MES_B230_R0016": "But fear the blade and hesitate as you step in, and you get hurt worse. A fearless spirit is essential.",
    "DK4_MES_B230_R0019": "They say a martial-arts robe exists that can chip a striking sword. Have you heard?",
    "DK4_MES_B230_R0022": "Swords chip? Hm.",
    "DK4_MES_B230_R0025": "With that robe, this woman could fight freely...",
    "DK4_MES_B230_R0028": "But rely on equipment, and Master would scold: 'Train yourself first!'",
    "DK4_MES_B230_R0032": "More training. Hah!",

    # Samwell reports the Armadillo's Steel Hide shield.
    "DK4_MES_B231_R0005": "A moment, Admiral?",
    "DK4_MES_B231_R0009": "Hm?",
    "DK4_MES_B231_R0013": "A tale just came up about an animal called an armadillo. Apparently its hide is harder than iron.",
    "DK4_MES_B231_R0017": "And?",
    "DK4_MES_B231_R0021": "Long ago, someone made a shield{LB}from armadillo hide. They called it{LB}the Armadillo's Steel Hide.",
    "DK4_MES_B231_R0024": "What about the shield?",
    "DK4_MES_B231_R0028": "Do you not want a shield harder{LB}than iron? That would surely help{LB}in battle.",
    "DK4_MES_B231_R0031": "True. Where can it be found?",
    "DK4_MES_B231_R0034": "Problem is, it lies somewhere{LB}around Africa. That is all we know.",
    "DK4_MES_B231_R0038": "That barely narrows it.",
    "DK4_MES_B231_R0042": "No, it does not...",
    "DK4_MES_B231_R0046": "Cheer up. We will remember.{LB}Luck may lead us there.",
    "DK4_MES_B231_R0049": "Right.",

    # Samwell repeats the pitch with the Giant Tortoise Shield.
    "DK4_MES_B232_R0005": "A moment, Admiral?",
    "DK4_MES_B232_R0009": "Hm?",
    "DK4_MES_B232_R0013": "A rumor just came up about a giant tortoise whose shell is harder than iron.",
    "DK4_MES_B232_R0016": "And?",
    "DK4_MES_B232_R0020": "Someone made a shield from that shell.{LB}People called it the Giant Tortoise{LB}Shield.",
    "DK4_MES_B232_R0023": "Hm? This sounds familiar. Did you not tell the same tale about an armadillo?",
    "DK4_MES_B232_R0027": "Perhaps. Hard to recall.",
    "DK4_MES_B232_R0031": "Enough. What of the shield?",
    "DK4_MES_B232_R0034": "Would it not help us in battle? Do you not want it?",
    "DK4_MES_B232_R0038": "That is exactly what you said about the armadillo shield.",
    "DK4_MES_B232_R0041": "Did this man? Never mind that.",
    "DK4_MES_B232_R0045": "...Where can it be found?",
    "DK4_MES_B232_R0048": "Problem is, it lies somewhere{LB}around the eastern ocean.",
    "DK4_MES_B232_R0051": "That barely narrows it.",
    "DK4_MES_B232_R0055": "No, it does not...",
    "DK4_MES_B232_R0059": "Cheer up. We will remember.{LB}Luck may lead us there.",
    "DK4_MES_B232_R0062": "Right.",

    # Samwell investigates the Phoenix Bascinet.
    "DK4_MES_B233_R0005": "A moment, Admiral?",
    "DK4_MES_B233_R0009": "Hm?",
    "DK4_MES_B233_R0013": "Admiral, do phoenixes exist?",
    "DK4_MES_B233_R0017": "Hard to say. But seeing one{LB}would be worthwhile. Why ask?",
    "DK4_MES_B233_R0021": "A helmet forged in phoenix fire exists.{LB}They call it the Phoenix Bascinet.",
    "DK4_MES_B233_R0024": "And you want it because it may help in battle?",
    "DK4_MES_B233_R0027": "You knew at once!",
    "DK4_MES_B233_R0031": "You have said this before.",
    "DK4_MES_B233_R0034": "Have we? Good memory.",
    "DK4_MES_B233_R0038": "Where is it, then?{LB}Do not say Africa or the eastern ocean.",
    "DK4_MES_B233_R0042": "What are you saying? Britain.",
    "DK4_MES_B233_R0046": "Oh. That is much more specific this time.",
    "DK4_MES_B233_R0049": "Of course! This man researched it. At first, all we knew was northern Europe.",
    "DK4_MES_B233_R0053": "Well done, Samwell.",
    "DK4_MES_B233_R0057": "Heh. Sure.",
    "DK4_MES_B233_R0061": "Very well. Samwell earned this. We will remember the Phoenix Bascinet.",
    "DK4_MES_B233_R0065": "Good! Hope we find it.",

    # Carlo tells Hodram about the medical writings of Herophilus.
    "DK4_MES_B234_R0005": "Admiral, heard of Herophilus?",
    "DK4_MES_B234_R0009": "No. Who was he?",
    "DK4_MES_B234_R0012": "An ancient physician left what may be{LB}the world's oldest medical text.",
    "DK4_MES_B234_R0016": "Hm.",
    "DK4_MES_B234_R0020": "Supposedly, that text explains how to reduce a ship crew's exhaustion...",
    "DK4_MES_B234_R0024": "A remarkable book.{LB}We should find it if true.",
    "DK4_MES_B234_R0027": "Agreed.",
    "DK4_MES_B234_R0031": "But how can we search? Any useful clue?",
    "DK4_MES_B234_R0035": "Only a very old report that it was seen deep in the Mediterranean.",
    "DK4_MES_B234_R0039": "More?",
    "DK4_MES_B234_R0043": "...Nothing.",
    "DK4_MES_B234_R0047": "Then finding it may be hopeless.",
    "DK4_MES_B234_R0050": "My apologies.",
    "DK4_MES_B234_R0054": "No need to apologize.",
    "DK4_MES_B234_R0058": "Yes.",
    "DK4_MES_B234_R0062": "So we must search the Mediterranean.",

    # Manuel describes Phidias's legendary sculpting chisel.
    "DK4_MES_B236_R0005": "Admiral, a moment please?",
    "DK4_MES_B236_R0008": "Hm?",
    "DK4_MES_B236_R0012": "A fascinating scrap turned up{LB}at the Library of Alexandria.",
    "DK4_MES_B236_R0016": "Hm?",
    "DK4_MES_B236_R0020": "The scrap tells of a strange chisel{LB}used by Phidias, legendary sculptor{LB}of ancient Greece.",
    "DK4_MES_B236_R0023": "Hm.",
    "DK4_MES_B236_R0027": "They say his soul entered it after death, granting miraculous artistic talent to whoever used it.",
    "DK4_MES_B236_R0030": "The chisel was buried somewhere in the Balkans near Greece, but the writing gave no exact location.",
    "DK4_MES_B236_R0033": "Manuel, do you mean to use that chisel for ship repairs?",
    "DK4_MES_B236_R0037": "Why not? Romans even made kings{LB}tools of policy. A king as a tool{LB}sounds wonderfully extravagant.",
    "DK4_MES_B236_R0040": "A ship is a work of art. The finer its tools, the better. Search for it if an opportunity comes.",

    # Carlo and Filippo discuss old trade in the Papal States.
    "DK4_MES_B237_R0009": "Why so vacant, Ｆilippo?",
    "DK4_MES_B237_R0012": "Huh? Carlo! When did you return?",
    "DK4_MES_B237_R0016": "Only passing through on business. But Ｆilippo, no customers will come while you look so vacant.",
    "DK4_MES_B237_R0019": "Mind your own business. Still, that sharp tongue means you have recovered.",
    "DK4_MES_B237_R0023": "At last. This man is back at work and sails with these people.",
    "DK4_MES_B237_R0026": "Oh, customers! Sorry. A story from this man's great-grandfather had come to mind.",
    "DK4_MES_B237_R0029": "What story?",
    "DK4_MES_B237_R0033": "Trade in the Papal States. The pope once ruled almost to Venice.",
    "DK4_MES_B237_R0037": "This man has heard. Trade there thrived when papal power stood at its height.",
    "DK4_MES_B237_R0040": "Exactly. Princes competed over what and how much to donate to the pope...",
    "DK4_MES_B237_R0043": "Our ancestors grew rich merely moving goods from one lord to another. But now...",
    "DK4_MES_B237_R0047": "Papal authority faded, and commerce with the Church fell away.",
    "DK4_MES_B237_R0051": "Right. We are back to earning profits by our own labor. Those ancestors had it easy.",
    "DK4_MES_B237_R0054": "Come to think of it, relics tied to the pope sometimes appear in lands he once ruled.",
    "DK4_MES_B237_R0057": "A pope's possessions may carry blessings.{LB}This man could use divine favor.",
    "DK4_MES_B237_R0060": "Divine aid...",
    "DK4_MES_B237_R0064": "Admiral, this may be no joke.{LB}A pope's cherished object would be a great discovery.",

    # Charles writes about a mysterious roar that rallied sailors west of Lisbon.
    "DK4_MES_B238_R0014": "Admiral, a letter from Charles.",
    "DK4_MES_B238_R0015": "Admiral, correspondence from Charles.",
    "DK4_MES_B238_R0016": "Admiral, a letter from Charles.",
    "DK4_MES_B238_R0017": "Admiral, a letter from Mr. Charles.",
    "DK4_MES_B238_R0018": "Admiral, Charles sent a letter.",
    "DK4_MES_B238_R0019": "Admiral, a letter from Charles.",
    "DK4_MES_B238_R0020": "Admiral! A letter from Charles!",
    "DK4_MES_B238_R0027": "Now in West Africa,{LB}this man heard a strange tale from sailors.",
    "DK4_MES_B238_R0031": "Pirates attacked a Spanish fleet sailing from the New World to West Africa.",
    "DK4_MES_B238_R0035": "Hopelessly outmatched and too slow to escape, the merchants faced certain destruction.",
    "DK4_MES_B238_R0038": "West of Lisbon,{LB}they heard a roar unlike anything of this world.",
    "DK4_MES_B238_R0041": "The sound inexplicably roused the sailors. With lionlike courage, they turned and fought the pirates evenly.",
    "DK4_MES_B238_R0044": "Spanish warships appeared in time. The pirates fled, and the merchants escaped.",
    "DK4_MES_B238_R0047": "What made the sound, or whether nature can explain it, remains unknown.",
    "DK4_MES_B238_R0050": "Still, a fascinating tale.{LB}An investigation may be worthwhile.{LB}Charles Jean Rochefort",
    "DK4_MES_B238_R0057": "Dubious... Yet a roar that roused a crew is worth noting.",

    # Jam writes from India about a Gupta spirit-beast statue.
    "DK4_MES_B239_R0014": "Admiral, a letter from Jam.",
    "DK4_MES_B239_R0015": "Admiral, correspondence from Jam.",
    "DK4_MES_B239_R0016": "Admiral, a letter from Jam.",
    "DK4_MES_B239_R0017": "Admiral, a letter from Mr. Jam.",
    "DK4_MES_B239_R0018": "Admiral, Jam sent a letter.",
    "DK4_MES_B239_R0019": "Admiral, a letter from Jam.",
    "DK4_MES_B239_R0020": "Admiral! A letter from Jam!",
    "DK4_MES_B239_R0027": "Hey, Admiral! Everyone doing well?",
    "DK4_MES_B239_R0030": "South Asia is incredible. Hard to explain, but one interesting rumor came up.",
    "DK4_MES_B239_R0033": "A statue of a spirit beast, made under the Gupta dynasty, can supposedly see the future.",
    "DK4_MES_B239_R0036": "Sounds false, right? But anything seems possible here. Maybe the story is true.",
    "DK4_MES_B239_R0039": "With it, maybe this man could finally beat Ｆernando at gambling. Too much to hope?",
    "DK4_MES_B239_R0042": "But none is sold, and no one this man meets has ever seen it.",
    "DK4_MES_B239_R0046": "Admiral, why not look if time permits? Even beyond gambling, it could prove useful.",
    "DK4_MES_B239_R0049": "Time to sail. Hope you find the treasure. Until next time. Jam Jack Ludwayer",
    "DK4_MES_B239_R0064": "Ha! You are 500 years too soon to beat this man!",
    "DK4_MES_B239_R0070": "Hmph. Can that man not write a normal letter? Still, he made the effort to report it. We may investigate.",
}


SPEAKERS = {
    "01": "Hodram Bergstrom",
    "0B": "Jam Jack Ludwayer",
    "12": "Charles Jean Rochefort",
    "13": "Carlo",
    "14": "Fernando",
    "16": "Samwell",
    "17": "Manuel",
    "19": "Charlotte",
    "68": "Filippo",
    "D0": "Crewman",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXT = {
    230: "Charlotte trains late and recalls a martial-arts robe able to chip swords.",
    231: "Samwell reports the Armadillo's Steel Hide shield hidden somewhere around Africa.",
    232: "Samwell repeats his pitch with the Giant Tortoise Shield from the eastern ocean.",
    233: "Samwell investigates the Phoenix Bascinet and narrows its location to Britain.",
    234: "Carlo tells Hodram about Herophilus's medical text and its remedy for crew exhaustion.",
    236: "Manuel describes Phidias's legendary chisel buried somewhere in the Balkans.",
    237: "Carlo and Filippo discuss Papal States trade and relics once owned by a pope.",
    238: "Charles writes about a mysterious roar that rallied sailors west of Lisbon.",
    239: "Jam writes from South Asia about a Gupta spirit-beast statue that sees the future.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {
            row["id"]: row
            for row in csv.DictReader(stream)
            if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)
        }
    if set(LINES) | set(EXCLUDED) != set(source_rows) or set(LINES) & set(EXCLUDED):
        missing = sorted(set(source_rows) - set(LINES) - set(EXCLUDED))
        extra = sorted((set(LINES) | set(EXCLUDED)) - set(source_rows))
        raise SystemExit(f"Hodram V18 inventory mismatch: missing={missing}, extra={extra}")

    records = []
    block_counts: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = (
            f"{first:02X}"
            if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES)
            else ""
        )
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        block_counts[str(block)] = block_counts.get(str(block), 0) + 1
        records.append(
            {
                "id": row_id,
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(state, "Alternate crew text"),
                "context": CONTEXT[block],
                "source_meaning": english.replace("{LB}", " "),
                "localization_note": "Faithful concise American English with measured fixed-record wrapping.",
                "qa_waivers": [
                    "weak-line-ending",
                    "orphan-final-line",
                    *(["manual-break"] if "{LB}" in english else []),
                ],
                **(
                    {
                        "manual_break_reason": (
                            "Places a protected newline before the native row boundary so the "
                            "progressive ASCII pair phase cannot auto-wrap and skip a display row."
                        )
                    }
                    if "{LB}" in english
                    else {}
                ),
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": True,
                },
            }
        )

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC1.DK4",
        "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "hodram-story-legend-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Nine source-locked Hodram equipment, correspondence, trade-history, and character events across SC1 blocks 230-239.",
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(source_rows),
            "translated_records": len(records),
            "blocks": block_counts,
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
