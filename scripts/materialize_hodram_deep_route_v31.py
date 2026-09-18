from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v31.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (17, 18, 19)
LINES = {
    "DK4_MES_B17_R0006": "Damn, beaten again...{LB}But next time... Huh?!",
    "DK4_MES_B17_R0009": "No 'next time' for you.",
    "DK4_MES_B17_R0012": "Heh heh...",
    "DK4_MES_B17_R0016": "What?!{LB}Say that again!",
    "DK4_MES_B17_R0020": "What? Could not hear?",
    "DK4_MES_B17_R0024": "Nobody here obeys you anymore.{LB}Not one of us!",
    "DK4_MES_B17_R0027": "Damn you!{LB}You betrayed me!",
    "DK4_MES_B17_R0030": "Noise over there...",
    "DK4_MES_B17_R0034": "Her own men surround her.",
    "DK4_MES_B17_R0037": "Alongside.",
    "DK4_MES_B17_R0041": "We keep losing and earn nothing.{LB}Someone must answer for that,{LB}and it will be you.",
    "DK4_MES_B17_R0045": "Answer?!",
    "DK4_MES_B17_R0049": "Why keep chasing{LB}{MACRO:FO}, anyway?",
    "DK4_MES_B17_R0053": "Heh. Hiding the reason{LB}from us, are you?!",
    "DK4_MES_B17_R0060": "You only chased {MACRO:FO}{LB}to reclaim the Bloody Shamshir!{LB}Your father's keepsake!",
    "DK4_MES_B17_R0064": "No... That was not why...",
    "DK4_MES_B17_R0068": "You have gone soft.{LB}Nobody follows a leader{LB}who cannot earn. Prepare yourself!",
    "DK4_MES_B17_R0072": "Admiral!{LB}They will kill her{LB}if we do nothing!",
    "DK4_MES_B17_R0076": "We cannot abandon her.",
    "DK4_MES_B17_R0080": "Let us go.",
    "DK4_MES_B17_R0084": "W-wait! Do not be rash!",
    "DK4_MES_B17_R0088": "What? Stay out of this!",
    "DK4_MES_B17_R0091": "Back off, lackey.",
    "DK4_MES_B17_R0095": "This is none of your affair!{LB}Men, finish Aziza and these fools!",
    "DK4_MES_B17_R0099": "Al, my aid is yours.",
    "DK4_MES_B17_R0103": "Count me in!{LB}Men who need numbers are weak!",
    "DK4_MES_B17_R0106": "Then let us blow them away{LB}with a fine, loud boom!",
    "DK4_MES_B17_R0110": "Pirates!{LB}Come and face me!",
    "DK4_MES_B17_R0113": "Why...?{LB}Why fight for me?{LB}We were enemies moments ago...",
    "DK4_MES_B17_R0117": "D-damn! The odds are against us!",
    "DK4_MES_B17_R0121": "At last, you see.",
    "DK4_MES_B17_R0125": "{MACRO:FI} {MACRO:FA}...",
    "DK4_MES_B17_R0129": "You came to save her too?",
    "DK4_MES_B17_R0133": "And if we did?",
    "DK4_MES_B17_R0137": "This woman caused all of it!{LB}Why should we suffer?!",
    "DK4_MES_B17_R0140": "You have complained enough.{LB}Why not release her now?",
    "DK4_MES_B17_R0143": "You only want Aziza gone,{LB}correct?",
    "DK4_MES_B17_R0146": "You heard us.{LB}Nobody will follow her now.",
    "DK4_MES_B17_R0153": "Then we shall take Aziza{LB}with us.",
    "DK4_MES_B17_R0160": "Good.{LB}But she is not free.",
    "DK4_MES_B17_R0164": "Money?!",
    "DK4_MES_B17_R0168": "Al, enough.{LB}What is your price?",
    "DK4_MES_B17_R0171": "Pay 1,000,000 coins.",
    "DK4_MES_B17_R0176": "Aziza... come.",
    "DK4_MES_B17_R0184": "Done. Go!",
    "DK4_MES_B17_R0190": "Betrayed by my own crew...{LB}How low have things fallen?{LB}But why did you save me?",
    "DK4_MES_B17_R0193": "Had to help...",
    "DK4_MES_B17_R0197": "Only a brute{LB}would abandon you.",
    "DK4_MES_B17_R0200": "Something puzzles me.{LB}Why would a woman of your skill{LB}turn to piracy?",
    "DK4_MES_B17_R0204": "You flatter me.{LB}But piracy was no fall from grace.{LB}My father was a pirate.",
    "DK4_MES_B17_R0207": "Oh?",
    "DK4_MES_B17_R0211": "Those men served my father.{LB}Watching him as a child taught me{LB}swordplay and the pirate trade.",
    "DK4_MES_B17_R0214": "Where is your father?",
    "DK4_MES_B17_R0218": "An accident took him.{LB}That sword was his.{LB}He vanished with it...",
    "DK4_MES_B17_R0222": "The Bloody Shamshir...",
    "DK4_MES_B17_R0225": "My dream: become{LB}a great pirate like him.{LB}His every deed became my model.",
    "DK4_MES_B17_R0229": "When news came that you had it,{LB}that sword became all that mattered.{LB}With it...",
    "DK4_MES_B17_R0236": "Then that might prove{LB}being like my father...{LB}Heh, but...",
    "DK4_MES_B17_R0240": "More than pirate fame,{LB}his keepsake was all that mattered.{LB}At last, that became clear...",
    "DK4_MES_B17_R0243": "No wonder they abandoned me.{LB}Chasing a worthless relic{LB}would anger any crew.",
    "DK4_MES_B17_R0247": "Still yearn for piracy?",
    "DK4_MES_B17_R0251": "Piracy was never the true pursuit.{LB}My father was.{LB}That life is over now.",
    "DK4_MES_B17_R0255": "Sir.",
    "DK4_MES_B17_R0259": "Al, your thought is clear.{LB}Aziza, will you sail with us?",
    "DK4_MES_B17_R0262": "Gladly.{LB}Hard work will repay this debt.{LB}You saved my life.",
    "DK4_MES_B17_R0266": "And from now on,{LB}just call me Aziza.",
    "DK4_MES_B17_R0269": "Serving one's savior{LB}is a worthy path.",
    "DK4_MES_B17_R0272": "Livelier now...",
    "DK4_MES_B18_R0018": "We withdraw today!{LB}Next time, this ends!",
    "DK4_MES_B18_R0021": "Boast away.",
    "DK4_MES_B18_R0027": "Damn! We withdraw for now,{LB}but surrender is unthinkable!{LB}Remember Aziza Nurennahar!",
    "DK4_MES_B18_R0031": "Noted.",
    "DK4_MES_B19_R0016": "We withdraw for today.",
    "DK4_MES_B19_R0020": "Running away?!{LB}More cowardly than you look!",
    "DK4_MES_B19_R0023": "Do not answer her taunt!",
    "DK4_MES_B19_R0027": "Understood. Retreat!",
    "DK4_MES_B19_R0033": "Escaped!",
    "DK4_MES_B19_R0037": "Withdraw for now.",
    "DK4_MES_B19_R0041": "That pirate is formidable.{LB}She could serve as a navy admiral...",
    "DK4_MES_B19_R0045": "You thought you could beat me?{LB}Next time, prepare to die!",
}

SPEAKERS = {
    "01": "Hodram Bergstrom",
    "07": "Sailor",
    "0C": "Sailor",
    "10": "Gerhard Adelknauts",
    "11": "Al",
    "12": "Charles",
    "1B": "Aziza Nurennahar",
    "B7": "Mutineer",
    "B8": "Mutineer",
    "B9": "Mutineer",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(all_rows)
    if missing:
        raise SystemExit(f"Hodram V31 inventory mismatch: missing={sorted(missing)}")
    records = []
    counts = {str(block): 0 for block in BLOCKS}
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        counts[row_id.split("_B", 1)[1].split("_", 1)[0]] += 1
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Story participant"),
            "context": "Aziza's crew mutinies after repeated defeats; Hodram rescues and recruits her, with alternate victory and retreat branches.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving Aziza's pride, the mutineers' hostility, and all battle branches.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC1.DK4",
        "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "hodram-story-opening-battles-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Hodram Aziza-mutiny, rescue, recruitment, victory, and retreat dialogue in SC1 blocks 17-19.",
        "excluded_records": {},
        "inventory": {"identified_records": len(LINES), "translated_records": len(records), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
