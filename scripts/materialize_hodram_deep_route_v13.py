from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v13.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = tuple(range(174, 180))
EXCLUDED = {
    "DK4_MES_B174_R0095": "Packed martial-arts scene-control payload; not dialogue.",
    "DK4_MES_B179_R0008": "Packed pirate encounter scene-control payload; not dialogue.",
}


LINES = {
    "DK4_MES_B174_R0007": "...Hey, handsome!",
    "DK4_MES_B174_R0014": "Hey, handsome!",
    "DK4_MES_B174_R0018": "Me...?",
    "DK4_MES_B174_R0022": "Girl, why hide there?",
    "DK4_MES_B174_R0025": "Shh! Quiet. There's a story here.",
    "DK4_MES_B174_R0028": "You're sailors, right?{LB}Let me aboard your ship!",
    "DK4_MES_B174_R0032": "What an abrupt girl.",
    "DK4_MES_B174_R0036": "What story? Why board a ship?",
    "DK4_MES_B174_R0039": "Ran away from my master.{LB}Being found means getting dragged back!",
    "DK4_MES_B174_R0043": "Running away is serious.{LB}What do you study?",
    "DK4_MES_B174_R0046": "Taoist arts!",
    "DK4_MES_B174_R0050": "Studying isn't bad, but sometimes it's a drag, right?",
    "DK4_MES_B174_R0054": "My master caught me skipping and went wild. So rigid!",
    "DK4_MES_B174_R0057": "So training around the world will prove my worth. Admirable, right?",
    "DK4_MES_B174_R0060": "Young women today...",
    "DK4_MES_B174_R0064": "Good resolve, but how skilled are you in these 'arts'?",
    "DK4_MES_B174_R0068": "Then watch. Old man, draw your sword.",
    "DK4_MES_B174_R0072": "O-old man? You mean me?",
    "DK4_MES_B174_R0075": "Right! Here goes!",
    "DK4_MES_B174_R0078": "Hm",
    "DK4_MES_B174_R0082": "Haaaah!",
    "DK4_MES_B174_R0090": "Hm? (Nothing happened...)",
    "DK4_MES_B174_R0093": "Got you!",
    "DK4_MES_B174_R0098": "Whoa!",
    "DK4_MES_B174_R0102": "Nice dodge! See? The paralyzing art!",
    "DK4_MES_B174_R0106": "Paralyzing art? Hard to see how...",
    "DK4_MES_B174_R0109": "Taoist arts are mysterious, huh?",
    "DK4_MES_B174_R0113": "That wasn't the point...",
    "DK4_MES_B174_R0117": "Closing on Gerhard that fast is rare. Your sense of distance is keen.",
    "DK4_MES_B174_R0120": "Clearly, you have trained.",
    "DK4_MES_B174_R0123": "My master told me to sail. That shaped the man here now.",
    "DK4_MES_B174_R0127": "Running off was wrong, but your resolve seems real. Girl, your name?",
    "DK4_MES_B174_R0131": "Ｉfa!",
    "DK4_MES_B174_R0135": "Ｉfa, this is a navy ship. Still want aboard?",
    "DK4_MES_B174_R0138": "So your ship is strict too?{LB}Bring it on!",

    "DK4_MES_B175_R0010": "...Sir",
    "DK4_MES_B175_R0018": "{MACRO:FI}...",
    "DK4_MES_B175_R0022": "...Hm?",
    "DK4_MES_B175_R0026": "Pardon the intrusion. No threat is meant.",
    "DK4_MES_B175_R0029": "We meet at last. Sanghyeon, her senior pupil.",
    "DK4_MES_B175_R0033": "Word came that you took her in.{LB}This man came to offer one request.",
    "DK4_MES_B175_R0037": "Her...?",
    "DK4_MES_B175_R0041": "Her wild nature reflects this man's poor guidance. The shame is mine.",
    "DK4_MES_B175_R0044": "She fled training without leave and crossed the border. Such acts are unforgivable.",
    "DK4_MES_B175_R0048": "Unknown to her, our people are forbidden from leaving the nation.",
    "DK4_MES_B175_R0052": "You mean to take her back?",
    "DK4_MES_B175_R0056": "Her crime was grave.{LB}The school has expelled her.",
    "DK4_MES_B175_R0059": "Our bond is already severed...",
    "DK4_MES_B175_R0062": "We grew together from childhood,{LB}as true siblings.",
    "DK4_MES_B175_R0065": "She remains immature.{LB}Worry persists that she may offend others.",
    "DK4_MES_B175_R0069": "A selfish request, but please guide her so she never strays from the proper path.",
    "DK4_MES_B175_R0072": "And if possible, ensure she trains and obeys our master's teachings.",
    "DK4_MES_B175_R0075": "Please take good care of her.",
    "DK4_MES_B175_R0078": "A dream...?",
    "DK4_MES_B175_R0082": "So vivid, though...",
    "DK4_MES_B175_R0086": "Gooood morning! Let's depart...",
    "DK4_MES_B175_R0093": "What?",
    "DK4_MES_B175_R0097": "My senior...!",
    "DK4_MES_B175_R0101": "Could it be... Was his name Sanghyeon?",
    "DK4_MES_B175_R0105": "What?! How do you know?",
    "DK4_MES_B175_R0109": "So he truly was your senior...{LB}A man in my dream gave that name{LB}and entrusted you to me.",
    "DK4_MES_B175_R0113": "Brother Sanghyeon...",
    "DK4_MES_B175_R0117": "He came through his art...",
    "DK4_MES_B175_R0121": "Arts? (Again...)",
    "DK4_MES_B175_R0124": "He said to obey your master's teachings, even away from home.",
    "DK4_MES_B175_R0128": "Brother... he worries too much. Heh.",
    "DK4_MES_B175_R0132": "...What?",
    "DK4_MES_B175_R0135": "Training starts now! Can't disappoint Brother Sanghyeon!",
    "DK4_MES_B175_R0139": "Hah. Don't neglect ship duties for training. No leniency for being a woman.",
    "DK4_MES_B175_R0142": "Got it!",

    "DK4_MES_B176_R0007": "Mihwa, this man lives for your radiant smile.",
    "DK4_MES_B176_R0011": "Oh, Julian...",
    "DK4_MES_B176_R0015": "So syrupy.",
    "DK4_MES_B176_R0019": "Huh? You usually smile now. Do you hate me?",
    "DK4_MES_B176_R0023": "No... Usually your words cheer me, but...",
    "DK4_MES_B176_R0027": "There's something needed so badly that it fills every waking dream...",
    "DK4_MES_B176_R0031": "Mihwa, that face doesn't suit you. What do you want so badly?",
    "DK4_MES_B176_R0035": "The Golden Crown of Silla. A mystical name, yes? Very rare, too.",
    "DK4_MES_B176_R0039": "Sounds costly... Can this man pay?{LB}Where is it sold?",
    "DK4_MES_B176_R0042": "No shop sells it. Word says it's in Seoul.",
    "DK4_MES_B176_R0045": "Not sold? ...Ah! Of course. That place!",
    "DK4_MES_B176_R0048": "You know where?",
    "DK4_MES_B176_R0052": "Leave it to me! The crown will be yours, and your smile will return!",
    "DK4_MES_B176_R0056": "Your smile gives me life! Once it's found, you'll date me, right?",
    "DK4_MES_B176_R0059": "Not even found yet. How eager. Very well, perhaps.",
    "DK4_MES_B176_R0063": "Yes! Don't forget that promise! Off to Seoul!",
    "DK4_MES_B176_R0066": "Good luck... He's gone already.",
    "DK4_MES_B176_R0073": "Oh, sorry. Welcome.",
    "DK4_MES_B176_R0076": "About it...",
    "DK4_MES_B176_R0080": "You heard?",
    "DK4_MES_B176_R0084": "That Golden Crown?",
    "DK4_MES_B176_R0088": "Sorry, not much is known. Only that it's gorgeous.",
    "DK4_MES_B176_R0091": "Ah...",
    "DK4_MES_B176_R0095": "A soldier interested in such things?",
    "DK4_MES_B176_R0098": "You said it's in Seoul?",
    "DK4_MES_B176_R0102": "Yes, but nothing more is known.",
    "DK4_MES_B176_R0105": "Enough. The rest awaits there.",
    "DK4_MES_B176_R0108": "Would you give it to me?",
    "DK4_MES_B176_R0112": "We'll see...",

    "DK4_MES_B177_R0006": "Someone here may know of the Golden Crown of Silla.",
    "DK4_MES_B177_R0009": "Welcome. A drink?",
    "DK4_MES_B177_R0013": "A drink. And news of the Golden Crown of Silla?",
    "DK4_MES_B177_R0017": "Need to know?",
    "DK4_MES_B177_R0021": "Where is it? Any idea?",
    "DK4_MES_B177_R0024": "Seems it's in King Muryeong's Tomb, but no idea how to get it.",
    "DK4_MES_B177_R0028": "Muryeong's Tomb...",
    "DK4_MES_B177_R0032": "Odd. Someone asked the same thing earlier.",
    "DK4_MES_B177_R0035": "Same? Was that man named Julian?",
    "DK4_MES_B177_R0039": "Can't recall. He entered saying,{LB}'Your lips are rose petals.'{LB}A practiced flirt.",
    "DK4_MES_B177_R0046": "Then he's already gone to the tomb?",
    "DK4_MES_B177_R0049": "Probably...",
    "DK4_MES_B177_R0053": "Understood. Time to go.",

    "DK4_MES_B178_R0006": "You... Thanks for earlier.",
    "DK4_MES_B178_R0010": "You two know each other?",
    "DK4_MES_B178_R0014": "Anyway, as promised, the Golden Crown of Silla is yours!",
    "DK4_MES_B178_R0018": "So this is it... Beautiful. Thank you! Treasured forever!",
    "DK4_MES_B178_R0022": "Seems it went well...",
    "DK4_MES_B178_R0026": "So it seems.",
    "DK4_MES_B178_R0030": "Then we should leave...",
    "DK4_MES_B178_R0034": "Wait!",
    "DK4_MES_B178_R0042": "Mihwa, {MACRO:FI} actually found the crown.",
    "DK4_MES_B178_R0046": "What?! Really?",
    "DK4_MES_B178_R0050": "Then this man asked for it.",
    "DK4_MES_B178_R0053": "Thought that needn't be said...",
    "DK4_MES_B178_R0056": "No. Proper thanks will come later.",
    "DK4_MES_B178_R0059": "Julian...",
    "DK4_MES_B178_R0063": "No need. But your adventurous honor intrigues me.",
    "DK4_MES_B178_R0067": "Then let me sail aboard your ship, {MACRO:FI}! Hard work is promised!",
    "DK4_MES_B178_R0070": "An interesting offer.",
    "DK4_MES_B178_R0074": "My grandfather sailed the world.{LB}His stories made adventure call.",
    "DK4_MES_B178_R0078": "An adventurer like him!",
    "DK4_MES_B178_R0082": "Like him...",
    "DK4_MES_B178_R0086": "This isn't an adventure ship.{LB}But it does sail the whole world.",
    "DK4_MES_B178_R0090": "Work as promised, and you may board.",
    "DK4_MES_B178_R0093": "Yes! Then it's settled!",

    "DK4_MES_B179_R0006": "Her...?",
    "DK4_MES_B179_R0010": "You... from {MACRO:FO}. Never expected to meet here.",
    "DK4_MES_B179_R0013": "Why stalk our fleet?!",
    "DK4_MES_B179_R0017": "My, starting so bluntly?{LB}What a dull old man.",
    "DK4_MES_B179_R0021": "A pleasant time together was the plan.",
    "DK4_MES_B179_R0024": "What a woman...",
    "DK4_MES_B179_R0028": "Heh. Such a stiff soldier. Can't even take a joke.",
    "DK4_MES_B179_R0032": "You waited here to ambush and kill us!",
    "DK4_MES_B179_R0039": "Count them! Two of you, dozens of us!",
    "DK4_MES_B179_R0043": "Coward",
    "DK4_MES_B179_R0047": "Angel, since when did you outrank me?",
    "DK4_MES_B179_R0051": "Uh, n-no... This man...",
    "DK4_MES_B179_R0055": "No interruptions. Get back!",
    "DK4_MES_B179_R0058": "Y-yes!",
    "DK4_MES_B179_R0062": "Hmph. Don't misunderstand.",
    "DK4_MES_B179_R0065": "Killing you here would insult my pride!",
    "DK4_MES_B179_R0068": "Pirates have pride?",
    "DK4_MES_B179_R0072": "Pirates have their own honor. As a seaman, you know. Our reckoning comes at sea!",
    "DK4_MES_B179_R0076": "Challenge accepted.",
    "DK4_MES_B179_R0080": "Then wash your neck and wait! ...Hah!",
    "DK4_MES_B179_R0083": "What now?",
    "DK4_MES_B179_R0087": "A fine sword.",
    "DK4_MES_B179_R0091": "So you had it... Heh. Someday that sword will be mine.",
    "DK4_MES_B179_R0095": "Your meaning escapes me.",
    "DK4_MES_B179_R0099": "Someday you'll know. Men, withdraw!",
    "DK4_MES_B179_R0102": "Aye!",
    "DK4_MES_B179_R0106": "Strange, but her command earns praise.",
    "DK4_MES_B179_R0109": "She could easily command a fleet or two.",
    "DK4_MES_B179_R0113": "Pirate pride...",
}


SPEAKERS = {
    "01": "Hodram Bergstrom",
    "10": "Gerhard Adelknauts",
    "19": "Ifa",
    "1A": "Julian",
    "51": "Sanghyeon",
    "99": "Pirate crew",
    "B7": "Angel",
    "C9": "Mihwa",
    "CA": "Tavernkeeper",
    "FE": "Pirate captain",
}
EXTENDED_STATES = {0x10, 0x19, 0x1A, 0x51, 0x99, 0xB7, 0xC9, 0xCA, 0xFE}
CONTEXT = {
    174: "Ifa demonstrates her Taoist training and asks to join Hodram's navy ship.",
    175: "Sanghyeon appears in Hodram's dream, entrusts Ifa to him, and inspires her to continue training.",
    176: "Julian promises Mihwa the Golden Crown of Silla, and Hodram learns that it may be found in Seoul.",
    177: "A Seoul tavernkeeper points Hodram and Julian toward King Muryeong's Tomb.",
    178: "Julian gives Mihwa the Golden Crown, credits Hodram, and joins the fleet as an aspiring adventurer.",
    179: "A pirate captain confronts Hodram ashore, rejects an ambush, and vows to settle their rivalry at sea.",
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
        raise SystemExit(f"Hodram V13 inventory mismatch: missing={missing}, extra={extra}")

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
                "speaker": SPEAKERS.get(state, "Choice or scene text"),
                "context": CONTEXT[block],
                "source_meaning": english
                .replace("{LB}", " ")
                .replace("{MACRO:FI}", "Hodram")
                .replace("{MACRO:FA}", "Bergstrom")
                .replace("{MACRO:FO}", "Bergstrom Fleet"),
                "localization_note": "Faithful concise American English with measured fixed-record wrapping.",
                "qa_waivers": [
                    "weak-line-ending",
                    "orphan-final-line",
                    *(["manual-break"] if "{LB}" in english else []),
                ],
                **(
                    {
                        "manual_break_reason": (
                            "Places the protected newline before the native row boundary so the "
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
        "dialogue_profile": "hodram-story-ifa-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Hodram optional Ifa and Julian recruitment, Golden Crown, and pirate encounter events across SC1 blocks 174-179.",
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
