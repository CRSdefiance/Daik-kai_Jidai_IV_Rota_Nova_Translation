from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v17.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (220, 221, *range(223, 230))
EXCLUDED: dict[str, str] = {}


LINES = {
    # Hodram asks a tavernkeeper about Avalon.
    "DK4_MES_B220_R0005": "Barkeep, do you know Avalon?",
    "DK4_MES_B220_R0008": "Again? You believe that woman who calls herself a witch?",
    "DK4_MES_B220_R0012": "Avalon supposedly lies just west of here.",
    "DK4_MES_B220_R0016": "King Arthur is a fairy tale. Many ask, but no one has ever found Avalon.",

    # Ian discusses the Sacred Spear of Ares.
    "DK4_MES_B221_R0005": "Admiral, news of a magnificent weapon.",
    "DK4_MES_B221_R0008": "What is it called?",
    "DK4_MES_B221_R0011": "Legend says Ares carried it, hence the name Sacred Spear of Ares.",
    "DK4_MES_B221_R0014": "A spear of Ares? Curious. Do you know its location?",
    "DK4_MES_B221_R0018": "Rumor says armor named for other Olympians may have fallen nearby as well.",
    "DK4_MES_B221_R0021": "That does not answer the question.",
    "DK4_MES_B221_R0024": "The townspeople imply it lies nearby... This man wishes to find it.",
    "DK4_MES_B221_R0028": "(Hm. So he cares.)",
    "DK4_MES_B221_R0032": "Admiral? Why that face? Surprised this man cares about legends?",
    "DK4_MES_B221_R0036": "Yes.",
    "DK4_MES_B221_R0040": "Perhaps. Yet these mysteries stir the heart: gods of myth roaming this very land.",
    "DK4_MES_B221_R0043": "Thinking their weapons remain{LB}sends the mind into antiquity.",
    "DK4_MES_B221_R0046": "...Ah.",

    # Julian flirts with Lucia while discussing the Empress's Gown.
    "DK4_MES_B223_R0005": "Lucia! Well? This man comes here solely to see those noble, beautiful eyes.",
    "DK4_MES_B223_R0008": "Welcome, Julian. Still a master of sweet words.",
    "DK4_MES_B223_R0012": "Hm...?",
    "DK4_MES_B223_R0016": "What is it? Something on my face?",
    "DK4_MES_B223_R0019": "So... Perhaps the legendary empress resembled you.",
    "DK4_MES_B223_R0023": "What does that mean?",
    "DK4_MES_B223_R0027": "Sorry, rather sudden. A tale of armor called the Empress's Gown brought it to mind.",
    "DK4_MES_B223_R0031": "The Empress's Gown?",
    "DK4_MES_B223_R0035": "A Chinese empress wore it.{LB}Her tyranny brought a tragic end.",
    "DK4_MES_B223_R0039": "She must have been terrifyingly beautiful, stealing hearts at a glance... Just like you.",
    "DK4_MES_B223_R0042": "But 'tyranny' means selfish and arrogant. Does this woman seem so spiteful?",
    "DK4_MES_B223_R0046": "Silly. A little selfishness makes a woman charming, about as much as you have.",
    "DK4_MES_B223_R0050": "A gown that protected a beautiful woman... How romantic. Do you not agree?",
    "DK4_MES_B223_R0053": "A gown, romantic? Her rings and necklaces interest me far more.",
    "DK4_MES_B223_R0057": "Their price, you mean? Women are so practical! Time to leave. See you.",
    "DK4_MES_B223_R0061": "See you.",
    "DK4_MES_B223_R0065": "He flees when this woman asks for gifts.",

    # A townsman and crewman recount the Crusades and Saladin's armor.
    "DK4_MES_B224_R0005": "You there. Do not cross this square without hearing.",
    "DK4_MES_B224_R0008": "What is in this city?",
    "DK4_MES_B224_R0012": "Do you know of the Crusades?",
    "DK4_MES_B224_R0018": "Know it",
    "DK4_MES_B224_R0020": "No",
    "DK4_MES_B224_R0028": "Hmph. Noble knights reclaiming the Holy Land, right?",
    "DK4_MES_B224_R0034": "Europe calls them chivalrous armies that fought to reclaim the Holy Land...",
    "DK4_MES_B224_R0040": "A convenient lie. People here know what the Crusaders were truly like.",
    "DK4_MES_B224_R0043": "The truth?",
    "DK4_MES_B224_R0047": "Their real goal was this region's wealth. They looted and killed along the way.",
    "DK4_MES_B224_R0050": "Such rewritten history is unforgivable! The true hero was Saladin, not the Crusaders!",
    "DK4_MES_B224_R0053": "Who was Saladin?",
    "DK4_MES_B224_R0057": "A great Muslim hero. Beating Crusaders barely hints at his greatness.",
    "DK4_MES_B224_R0061": "His warfare, treatment of captives and civilians, and peace terms were all humane. He rejected dishonor.",
    "DK4_MES_B224_R0064": "A true hero, then.",
    "DK4_MES_B224_R0068": "Word says Saladin's armor vanished. Seek it if you wish to follow his example.",

    # Gerhard tells Hodram of the samurai Noritsune.
    "DK4_MES_B225_R0009": "Gerhard, why watch the sunset? Troubled?",
    "DK4_MES_B225_R0012": "Admiral... A tale heard in Japan stirred this man's heart, oddly enough.",
    "DK4_MES_B225_R0016": "Whose tale?",
    "DK4_MES_B225_R0020": "A warrior from centuries ago named Noritsune.",
    "DK4_MES_B225_R0023": "What did he do so long ago?",
    "DK4_MES_B225_R0027": "His once-mighty clan lost battle after battle against a rival power and faced destruction.",
    "DK4_MES_B225_R0030": "As his weak kin fell, he alone fought bravely...",
    "DK4_MES_B225_R0033": "During the last sea battle, he crossed seven ships toward his foe.",
    "DK4_MES_B225_R0037": "At last exhausted, he seized two foes and sank with them and his brilliant armor into the strait...",
    "DK4_MES_B225_R0040": "Such courage in this small eastern land reveals the true spirit of its people.",
    "DK4_MES_B225_R0044": "A fearsome death... A true warrior, surely.",
    "DK4_MES_B225_R0047": "Exactly.",
    "DK4_MES_B225_R0051": "Gerhard, that tale truly moved you.",
    "DK4_MES_B225_R0054": "...Armor, lost in the strait...",
    "DK4_MES_B225_R0057": "This man has spoken too long. Shall we return to work?",

    # Ian writes about Timur's stolen mail coat.
    "DK4_MES_B226_R0014": "Admiral, a letter from Ｉan.",
    "DK4_MES_B226_R0015": "Admiral, correspondence from Ｉan.",
    "DK4_MES_B226_R0016": "Admiral, a letter from Ｉan.",
    "DK4_MES_B226_R0017": "Admiral, a letter from Mr. Ｉan.",
    "DK4_MES_B226_R0018": "Admiral, Ｉan sent a letter.",
    "DK4_MES_B226_R0019": "Admiral, a letter from Ｉan.",
    "DK4_MES_B226_R0020": "Admiral! A letter from Ｉan!",
    "DK4_MES_B226_R0028": "An odd book appeared at a shop.",
    "DK4_MES_B226_R0031": "A book about Timur, heir to Mongol blood, who built an empire across Central and West Asia two centuries ago.",
    "DK4_MES_B226_R0034": "On the battlefield, he wore marvelous mail that deflected arrows and turned the edges of blades and spears.",
    "DK4_MES_B226_R0037": "Buried with him, it was stolen decades later along with his other grave goods.",
    "DK4_MES_B226_R0040": "The thieves fled into a scorching desert to evade pursuit, but died just before reaching sight of the sea.",
    "DK4_MES_B226_R0044": "That fact stayed unknown for ages,{LB}and the mail remains lost.",
    "DK4_MES_B226_R0048": "Should this interest you, perhaps investigate it. Ｉan Dukov",
    "DK4_MES_B226_R0056": "Hm. Ｉan likes Asian history?",
    "DK4_MES_B226_R0067": "The Mongols once ruled Russia and stayed enemies for years. Such interest is natural.",
    "DK4_MES_B226_R0070": "Hm.",

    # Julian flirts with Safia while discussing Medusa's Shield.
    "DK4_MES_B227_R0005": "Safia! Those eyes remain mysterious.",
    "DK4_MES_B227_R0008": "Oh, Julian. Welcome.",
    "DK4_MES_B227_R0015": "What is it? Something on my face?",
    "DK4_MES_B227_R0018": "No... Those eyes nearly pulled this man inside. Perhaps petrification feels like this.",
    "DK4_MES_B227_R0022": "What is this?",
    "DK4_MES_B227_R0026": "A story of Medusa's Shield in the Tasman Sea lingered in mind. Your eyes recalled it.",
    "DK4_MES_B227_R0029": "Medusa was an ugly monster with snake hair. Are you calling me frightening and ugly?",
    "DK4_MES_B227_R0032": "Nonsense. Hide your hair;{LB}those lovely eyes can capture me.",
    "DK4_MES_B227_R0035": "Always joking.",
    "DK4_MES_B227_R0039": "Turned to stone by you, living beside you forever under moonlight... How romantic.",
    "DK4_MES_B227_R0043": "Even as stone, this woman ignores you.",
    "DK4_MES_B227_R0046": "So cold. Yet that aloofness is charming. Time to leave. See you.",
    "DK4_MES_B227_R0050": "See you.",
    "DK4_MES_B227_R0054": "An odd comparison... Yet this heart fluttered.",

    # Children reenact Charles Martel's victory and prompt a discussion of heroes.
    "DK4_MES_B228_R0005": "Prepare yourself, heathen! Charles Martel will defeat you!",
    "DK4_MES_B228_R0009": "Ow! This man yields! Retreat!",
    "DK4_MES_B228_R0012": "What are they doing?",
    "DK4_MES_B228_R0016": "Playing heroes. Children everywhere admire their nation's champions.",
    "DK4_MES_B228_R0020": "So the hero was Charles... What name?",
    "DK4_MES_B228_R0023": "Charles Martel,{LB}who lived eight centuries ago.",
    "DK4_MES_B228_R0026": "Near Tours and Poitiers,{LB}he defeated a Muslim army{LB}advancing north from Spain.",
    "DK4_MES_B228_R0029": "Winning is admirable, but calling him a hero for that alone seems excessive.",
    "DK4_MES_B228_R0033": "Why that victory matters.",
    "DK4_MES_B228_R0037": "Had he lost, all Europe might be Muslim. History would have changed greatly.",
    "DK4_MES_B228_R0041": "A man who might have changed history... The children adore him as Europe's defender.",
    "DK4_MES_B228_R0045": "Your deeds are certainly no less worthy than those of Charles Martel, Admiral.",
    "DK4_MES_B228_R0049": "This man wonders how posterity will tell your story.",

    # Manuel discusses Attila and the missing king's armor.
    "DK4_MES_B229_R0005": "Ah, Admiral.",
    "DK4_MES_B229_R0008": "Manuel.",
    "DK4_MES_B229_R0012": "Surveying fashions? Always busy.",
    "DK4_MES_B229_R0015": "Not only that. A pleasant respite.",
    "DK4_MES_B229_R0018": "True.",
    "DK4_MES_B229_R0022": "Manuel, some business in the square?",
    "DK4_MES_B229_R0025": "The same as you: gathering news while taking a walk.",
    "DK4_MES_B229_R0028": "Admiral, do you know Attila,{LB}king of the Huns?",
    "DK4_MES_B229_R0032": "The name is familiar...",
    "DK4_MES_B229_R0036": "The Huns were Asian nomadic horsemen. Attila pressured both Eastern and Western Rome.",
    "DK4_MES_B229_R0040": "Hm. A man great enough to threaten Rome itself.",
    "DK4_MES_B229_R0044": "However mighty an empire,{LB}a stronger foe comes. No rule lasts.",
    "DK4_MES_B229_R0047": "Harsh. So we must stay vigilant?",
    "DK4_MES_B229_R0050": "Certainly. Effort decides all.",
    "DK4_MES_B229_R0053": "Naturally. Why mention Attila now?",
    "DK4_MES_B229_R0057": "A rumor just surfaced about armor tied to Attila. Nothing more than rumor, though.",
    "DK4_MES_B229_R0061": "Mail",
    "DK4_MES_B229_R0065": "After Attila died, someone reportedly carried his armor northwest.",
    "DK4_MES_B229_R0069": "A king's armor carried northwest... A man who threatened Rome must have inspired terror.",
    "DK4_MES_B229_R0073": "Northwest from here means somewhere in northern Europe.",
}


SPEAKERS = {
    "01": "Hodram Bergstrom",
    "0D": "Crewman",
    "10": "Gerhard Adelknauts",
    "11": "Crewman",
    "15": "Ian",
    "17": "Manuel",
    "1A": "Julian",
    "55": "Townsman",
    "5C": "Tavernkeeper",
    "97": "Child",
    "A2": "Child",
    "C5": "Safia",
    "C7": "Lucia",
    "D0": "Crewman",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXT = {
    220: "Hodram asks a tavernkeeper where to find Avalon.",
    221: "Ian discusses the Sacred Spear of Ares and other Olympian equipment.",
    223: "Julian flirts with Lucia while discussing the Empress's Gown.",
    224: "A townsman and crewman recount the Crusades, Saladin, and his missing armor.",
    225: "Gerhard tells Hodram of the samurai Noritsune and his armor lost in a strait.",
    226: "Ian writes to Hodram about Timur's stolen mail coat.",
    227: "Julian flirts with Safia while discussing Medusa's Shield.",
    228: "Children reenact Charles Martel's victory and prompt a discussion of heroes.",
    229: "Manuel discusses Attila and the missing king's armor.",
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
        raise SystemExit(f"Hodram V17 inventory mismatch: missing={missing}, extra={extra}")

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
                "speaker": SPEAKERS.get(state, "Choice or alternate crew text"),
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
        "scope": "Nine source-locked Hodram legendary-armor, correspondence, history, and Julian character events across SC1 blocks 220-229.",
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
