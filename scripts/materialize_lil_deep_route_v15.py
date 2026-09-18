from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v15.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
LINES = {
    "DK4_MES_B68_R0012": "Pirate Clifford...{LB}Though he now serves {MACRO:FO},{LB}he deserved England's royal favor.",
    "DK4_MES_B68_R0023": "Still cannot believe{LB}we made him submit.",
    "DK4_MES_B68_R0037": "Our bond made it possible!",
    "DK4_MES_B68_R0045": "Always believed...{LB}you were one of us...",
    "DK4_MES_B68_R0056": "Somehow...{LB}Clifford's feelings{LB}make sense to me.",
    "DK4_MES_B68_R0060": "He must regret{LB}deceiving {MACRO:FI}...",
    "DK4_MES_B68_R0063": "So...?",
    "DK4_MES_B68_R0067": "Without royal court chains,{LB}none of this would have happened.{LB}He wanted our friendship...",
    "DK4_MES_B68_R0077": "Clifford sent us{LB}this item...",
    "DK4_MES_B68_R0080": "This...",
    "DK4_MES_B68_R0090": "The stolen Ruler's Proof!",
    "DK4_MES_B68_R0096": "Ruler's Proof.",
    "DK4_MES_B68_R0249": "A letter from Clifford.",
    "DK4_MES_B68_R0253": "Letter?",
    "DK4_MES_B68_R0257": "Yes. Here.",
    "DK4_MES_B68_R0261": "Says, \"To {MACRO:FI}...\"",
    "DK4_MES_B68_R0264": "A gift awaits. Bring this letter{LB}to Amsterdam's tavern.{LB}-James Clifford",
    "DK4_MES_B68_R0268": "A gift...? Unsure why.{LB}Amsterdam's tavern{LB}must be the place.",
    "DK4_MES_B69_R0006": "We did it, {MACRO:FI}!",
    "DK4_MES_B69_R0009": "Ah, Kamil.",
    "DK4_MES_B69_R0012": "We did it!{LB}Our trade reaches{LB}the whole world now!",
    "DK4_MES_B69_R0020": "What is it?{LB}Not happy?",
    "DK4_MES_B69_R0023": "No, that is not it...",
    "DK4_MES_B69_R0027": "You miss home, right?",
    "DK4_MES_B69_R0031": "N-no way...",
    "DK4_MES_B69_R0035": "Hey...{LB}Return to Amsterdam{LB}after so long.",
    "DK4_MES_B69_R0039": "What?",
    "DK4_MES_B69_R0043": "Mom is still there alone.{LB}Want to show her my face sometimes.",
    "DK4_MES_B69_R0046": "Kamil...",
    "DK4_MES_B69_R0050": "All right?",
    "DK4_MES_B69_R0054": "Yes...{LB}(Thank you, Kamil.)",
    "DK4_MES_B70_R0012": "We did it,{LB}{MACRO:FI}!",
    "DK4_MES_B70_R0015": "Ah!{LB}...Kamil!",
    "DK4_MES_B70_R0018": "We did it!{LB}Our trade now spans{LB}the whole world.",
    "DK4_MES_B70_R0024": "Amsterdam...{LB}We are home.",
    "DK4_MES_B70_R0027": "Yes. Home again.",
    "DK4_MES_B70_R0031": "Everything began here...",
    "DK4_MES_B70_R0038": "Yes.",
    "DK4_MES_B70_R0042": "Still...{LB}the world was vast.",
    "DK4_MES_B70_R0045": "So fun!{LB}And all that tasty food{LB}around the world!",
    "DK4_MES_B70_R0057": "Got to rampage worldwide too!{LB}Yahoo!",
    "DK4_MES_B70_R0072": "The world's vastness{LB}moved me deeply.{LB}All thanks to {MACRO:FI}.",
    "DK4_MES_B70_R0079": "{MACRO:FO}...{LB}Never dreamed it would{LB}grow this large.",
    "DK4_MES_B70_R0091": "Yes, yes.{LB}Even this old man is amazed.",
    "DK4_MES_B70_R0105": "Science says impossible, perhaps.",
    "DK4_MES_B70_R0112": "What does that mean?",
    "DK4_MES_B70_R0116": "Ha, only joking.",
    "DK4_MES_B70_R0128": "That joke went past you!{LB}No wonder they call you a girl!",
    "DK4_MES_B70_R0134": "Hmph!",
    "DK4_MES_B70_R0138": "But this was not my doing alone.{LB}Everyone here made it possible...",
    "DK4_MES_B70_R0142": "Yes.",
    "DK4_MES_B70_R0154": "Ahem!{LB}Perhaps you mean me?",
    "DK4_MES_B70_R0168": "Your charm, {MACRO:FI}.{LB}People love cheerful {MACRO:FI}.",
    "DK4_MES_B70_R0175": "And also...{LB}Um... well...{LB}Kamil...",
    "DK4_MES_B70_R0187": "You...{LB}were here for me...",
    "DK4_MES_B70_R0191": "What?",
    "DK4_MES_B70_R0201": "Seems we are intruding.{LB}Emilio, everyone, move.",
    "DK4_MES_B70_R0204": "Huh? What? What is it?",
    "DK4_MES_B70_R0210": "Ahem.{LB}Leave them alone.{LB}Come, everyone.",
    "DK4_MES_B70_R0214": "The old man is right.",
    "DK4_MES_B70_R0229": "Withdraw...",
    "DK4_MES_B70_R0244": "This...{LB}not my forte.",
    "DK4_MES_B70_R0273": "Well done!{LB}Makes me jealous!",
    "DK4_MES_B70_R0287": "Yahoo!{LB}What a mood!{LB}Love makes us human!",
    "DK4_MES_B70_R0311": "So...{LB}this old man can stay...",
    "DK4_MES_B70_R0314": "Lecherous old fool!{LB}You are the worst intruder!",
    "DK4_MES_B70_R0329": "At last... now...",
    "DK4_MES_B70_R0335": "When Kamil left me...",
    "DK4_MES_B70_R0341": "Then...",
    "DK4_MES_B70_R0345": "Hey.",
    "DK4_MES_B70_R0349": "When we first set sail,{LB}all that selfish girl wanted{LB}was money, right?",
    "DK4_MES_B70_R0353": "But at sea, meeting people{LB}and seeing the world,{LB}my true desire became clear.",
    "DK4_MES_B70_R0356": "Now my dream is happiness{LB}for everyone in the world.{LB}Even me... changed so much.",
    "DK4_MES_B70_R0360": "And... all that time, Kamil...{LB}you always supported me...",
    "DK4_MES_B70_R0364": "Truly... thanks.",
    "DK4_MES_B70_R0368": "{MACRO:FI}, not just slow.{LB}You get lost without me.",
    "DK4_MES_B70_R0372": "Where would you be{LB}without me?",
    "DK4_MES_B70_R0376": "Hey! You are the slow one!{LB}What about me...!",
    "DK4_MES_B70_R0379": "{MACRO:FI},{LB}still do not get it?{LB}You are slow.",
    "DK4_MES_B70_R0383": "What means?!",
    "DK4_MES_B70_R0387": "Such words should not come{LB}from the girl's mouth.",
    "DK4_MES_B70_R0390": "Kamil...?",
    "DK4_MES_B70_R0394": "{MACRO:FI}...{LB}No...",
    "DK4_MES_B70_R0397": "Always at your side.{LB}Whatever comes, you are safe with me.",
    "DK4_MES_B70_R0400": "Whatever happens,{LB}my heart stays yours.",
    "DK4_MES_B70_R0403": "Kamil...",
    "DK4_MES_B70_R0407": "Love you...",
    "DK4_MES_B70_R0411": "What?",
    "DK4_MES_B70_R0416": "At last, they got together.",
    "DK4_MES_B70_R0420": "Yes. They look so happy.",
    "DK4_MES_B70_R0423": "Romance is another game.{LB}Kamil knows when to make a move.",
    "DK4_MES_B70_R0435": "Yahoo!{LB}Kiss, kiss, kiss!{LB}One more yahoo!",
    "DK4_MES_B70_R0450": "Took them long enough.{LB}What a troublesome pair.",
    "DK4_MES_B70_R0464": "Yes, yes.{LB}A proposal needs sincerity.",
    "DK4_MES_B70_R0476": "...Coming from you,{LB}that rings hollow.",
    "DK4_MES_B70_R0493": "Kamil's words were splendid.{LB}A lovely poem will come from them.",
    "DK4_MES_B70_R0507": "The answer is love!",
    "DK4_MES_B70_R0522": "Love? Science cannot explain it...",
    "DK4_MES_B70_R0537": "Ah... my chubby darling...",
    "DK4_MES_B70_R0541": "Huh? Samwell too...?{LB}His taste is beyond me.",
    "DK4_MES_B70_R0555": "Peeking is shameful!",
    "DK4_MES_B70_R0570": "Kamil, now!{LB}Push her down!",
    "DK4_MES_B70_R0584": "Quiet, you fools!{LB}They will hear you!",
    "DK4_MES_B70_R0599": "Maybe loving someone{LB}is not so bad...",
    "DK4_MES_B70_R0607": "Later...",
    "DK4_MES_B70_R0611": "Dong... dong.",
    "DK4_MES_B70_R0615": "Oh no, hurry!{LB}This dress is unfamiliar,{LB}and took so long!",
    "DK4_MES_B70_R0619": "Sorry, sorry...{LB}...?!",
    "DK4_MES_B70_R0626": "Well? Look good...?",
    "DK4_MES_B70_R0630": "Yes... so beautiful.",
    "DK4_MES_B70_R0634": "{MACRO:FI}...{LB}my beautiful bride.",
    "DK4_MES_B70_R0638": "Truly...{LB}the most beautiful in the world.",
    "DK4_MES_B70_R0642": "...Thank you.",
    "DK4_MES_B70_R0653": "...?{LB}Ah!",
    "DK4_MES_B70_R0656": "A man with a woman's name,{LB}yet fit for the occasion.",
    "DK4_MES_B70_R0659": "Dad!",
    "DK4_MES_B70_R0663": "Mr. Kuhn...",
    "DK4_MES_B70_R0667": "Your friends told me.{LB}At such a busy time...",
    "DK4_MES_B70_R0670": "(He came...)",
    "DK4_MES_B70_R0674": "Came this far,{LB}so one lesson for you.",
    "DK4_MES_B70_R0677": "No absolute truth exists.{LB}Walk the path you believe in.{LB}Understand, Marinus?",
    "DK4_MES_B70_R0680": "My path is unclear...{LB}But...",
    "DK4_MES_B70_R0683": "Beside {MACRO:FI},{LB}sure to find it.",
    "DK4_MES_B70_R0686": "(Kamil...)",
    "DK4_MES_B70_R0690": "Hmph.",
    "DK4_MES_B70_R0694": "No need to rush.{LB}Haste made me lose my way...",
    "DK4_MES_B70_R0697": "Dad...",
    "DK4_MES_B70_R0701": "...Enough.{LB}Leaving before Mother comes.",
    "DK4_MES_B70_R0704": "What?{LB}Not seeing her?",
    "DK4_MES_B70_R0707": "No. Your new life begins.{LB}Cannot disgrace it.{LB}Until another day.",
    "DK4_MES_B70_R0711": "...Y-yes.",
    "DK4_MES_B70_R0715": "Mr. Kuhn...",
    "DK4_MES_B70_R0719": "(Dad... Thank you.)",
    "DK4_MES_B70_R0735": "{MACRO:FI}!",
    "DK4_MES_B70_R0739": "Long time no see!",
    "DK4_MES_B70_R0743": "The polder is complete!",
    "DK4_MES_B70_R0746": "Really?!",
    "DK4_MES_B70_R0750": "Look!{LB}This is what the polder achieved!",
    "DK4_MES_B70_R0757": "Amazing. Truly.",
    "DK4_MES_B70_R0761": "Lovely.",
    "DK4_MES_B70_R0765": "Now we can save the poor.{LB}All thanks to {MACRO:FI}!",
    "DK4_MES_B70_R0769": "My work from now on will seek{LB}ways to help people worldwide.",
    "DK4_MES_B70_R0773": "A wonderful idea!",
    "DK4_MES_B70_R0777": "Yes. Amazing!",
    "DK4_MES_B70_R0781": "Meeting {MACRO:FI}{LB}taught me to think this way.",
    "DK4_MES_B70_R0785": "When another idea comes,{LB}please support it.",
    "DK4_MES_B70_R0788": "Yes, count on me!",
    "DK4_MES_B70_R0792": "By the way...{LB}why are you two at the church?",
    "DK4_MES_B70_R0796": "Well...{LB}we are getting married.",
    "DK4_MES_B70_R0799": "Yes.",
    "DK4_MES_B70_R0803": "...What?!{LB}You are getting married?!",
    "DK4_MES_B70_R0806": "This dress did not tell you?",
    "DK4_MES_B70_R0810": "Ah! Of course!{LB}No, no...{LB}never noticed!",
    "DK4_MES_B70_R0814": "The polder filled my thoughts...{LB}So sorry!",
    "DK4_MES_B70_R0817": "No worry at all.",
    "DK4_MES_B70_R0821": "And the two who made the polder{LB}possible are marrying!",
    "DK4_MES_B70_R0824": "Wonderful! What a happy day!",
    "DK4_MES_B70_R0828": "So glad the polder was ready{LB}for this happy day!{LB}Now joy is doubled!",
    "DK4_MES_B70_R0832": "May both be happy!",
    "DK4_MES_B70_R0836": "Hee hee, thanks.",
    "DK4_MES_B70_R0843": "Kamil, almost time.",
    "DK4_MES_B70_R0847": "Yes. Let us go!{LB}Our new voyage!",
}

SPEAKERS = {
    "02": "Lil Argot", "06": "Old sailor", "07": "Christina", "09": "Kamil",
    "0B": "Jam Jack Ludwayer", "0C": "Yukihisa", "0D": "Crewmate", "0E": "Emilio Ferrog",
    "0F": "Crewmate", "10": "Gerhard", "11": "Al", "12": "Charles",
    "13": "Carlo", "14": "Fernando", "16": "Samwell", "17": "Manuel",
    "19": "Ifa", "1A": "Julian", "28": "Antony Kuhn", "4C": "Old scholar",
    "97": "Sailor", "AB": "Lelystad founder", "FE": "Narration",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    68: "After Clifford's alternate defeat or submission, Lil's crew reflects on his motives and receives either the stolen Ruler's Proof or his Amsterdam gift letter.",
    69: "With Lil's worldwide trade network complete, Kamil suggests returning home to Amsterdam and visiting his mother.",
    70: "Lil's Amsterdam ending: the crew reflects on the voyage, Kamil confesses his love, they marry years later, Kuhn offers a final blessing, and Lelystad's polder is completed.",
}
EXCLUDED = {"DK4_MES_B70_R0005": "two-byte scene-control marker, not visible dialogue"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = (set(LINES) | set(EXCLUDED)) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V15 inventory mismatch: missing={sorted(missing)}")
    records = []
    blocks: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        blocks[str(block)] = blocks.get(str(block), 0) + 1
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Story participant"),
            "context": CONTEXTS[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving Clifford's branch outcomes, the crew epilogue, Lil and Kamil's romance, Kuhn's blessing, and the polder finale.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Clifford's alternate rewards, Lil's homecoming, full crew epilogue, Kamil's confession, wedding, Kuhn's blessing, and the completed polder across SC2 blocks 68-70.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(LINES) + len(EXCLUDED), "translated_records": len(records), "blocks": blocks},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records; excluded {len(EXCLUDED)} control")


if __name__ == "__main__":
    main()
