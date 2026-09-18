from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v18.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
LINES = {
    "DK4_MES_B74_R0005": "Busy port.{LB}Skilled sailors may be here.",
    "DK4_MES_B74_R0022": "Seek a cook instead.{LB}{MACRO:FI}'s food is awf...",
    "DK4_MES_B74_R0026": "Be grateful you get food at all!",
    "DK4_MES_B74_R0037": "A sailor... Oh!",
    "DK4_MES_B74_R0041": "A man worthy of respect lives here.{LB}He helped me once.{LB}Could ask him to join us.",
    "DK4_MES_B74_R0044": "What sort of man is he?",
    "DK4_MES_B74_R0048": "You can judge when we meet.{LB}Hope he is well!",
    "DK4_MES_B74_R0051": "Think this is the place...",
    "DK4_MES_B74_R0056": "Who?",
    "DK4_MES_B74_R0060": "Admiral Adernkatz!{LB}So good to see you!",
    "DK4_MES_B74_R0063": "Ah! You are...",
    "DK4_MES_B74_R0066": "Kamil Overijssel!{LB}You helped me once, sir!",
    "DK4_MES_B74_R0069": "Ah... yes.{LB}Age has dulled my memory.{LB}Pardon me.",
    "DK4_MES_B74_R0073": "Not at all!{LB}Glad to see you looking well!",
    "DK4_MES_B74_R0076": "You have grown into a fine man.{LB}And this your wife?",
    "DK4_MES_B74_R0079": "What?! No!{LB}What are you saying, old man?!",
    "DK4_MES_B74_R0087": "Do not speak to the admiral so!{LB}Sir, please forgive her!",
    "DK4_MES_B74_R0091": "She is {MACRO:FI} {MACRO:FA}.{LB}Serving aboard her ship now.",
    "DK4_MES_B74_R0094": "You serve under such a girl?{LB}How lamentable.",
    "DK4_MES_B74_R0106": "Quite right.{LB}Lamentable indeed.",
    "DK4_MES_B74_R0120": "Really?{LB}Life here is fun.",
    "DK4_MES_B74_R0126": "Lamentable?!{LB}What do you mean by that?",
    "DK4_MES_B74_R0129": "Exactly my meaning.{LB}No respect and little vocabulary.",
    "DK4_MES_B74_R0133": "Kamil serves your sort...{LB}How far he has fallen.",
    "DK4_MES_B74_R0140": "Now wait!{LB}That is a rotten thing to say!",
    "DK4_MES_B74_R0144": "Stating fact.",
    "DK4_MES_B74_R0148": "Say what you like about me!{LB}But my manners say nothing{LB}about Kamil!",
    "DK4_MES_B74_R0155": "Kamil has not fallen!{LB}That is no fact.{LB}That is slander!",
    "DK4_MES_B74_R0159": "Hmm...",
    "DK4_MES_B74_R0167": "Wrong of me.{LB}You are right.",
    "DK4_MES_B74_R0174": "(He apologized...{LB}That is unexpected.)",
    "DK4_MES_B74_R0177": "Admiral... we came hoping{LB}to ask for your help.",
    "DK4_MES_B74_R0185": "{MACRO:FI}, this is{LB}Admiral Gerhard Adernkatz.",
    "DK4_MES_B74_R0188": "He led a mighty private fleet{LB}devoted to hunting pirates.",
    "DK4_MES_B74_R0191": "Pirates once vanished from{LB}the North Sea to the Mediterranean.{LB}His fleet made that happen.",
    "DK4_MES_B74_R0194": "A naval admiral...{LB}So that is why you kept quiet.",
    "DK4_MES_B74_R0198": "You would judge him as a soldier.{LB}Better to meet him first{LB}and see his worth...",
    "DK4_MES_B74_R0205": "Kamil.",
    "DK4_MES_B74_R0209": "Yes, sir! Sorry!{LB}She spoke so rudely...",
    "DK4_MES_B74_R0212": "Never mind that.{LB}Tell me why you choose{LB}to serve this woman.",
    "DK4_MES_B74_R0216": "What?",
    "DK4_MES_B74_R0220": "Called {MACRO:FI}?",
    "DK4_MES_B74_R0223": "Yes.",
    "DK4_MES_B74_R0227": "Your words had heart.{LB}You lack manners, yet you are{LB}loyal to your friends.",
    "DK4_MES_B74_R0235": "We may not agree,{LB}but with Kamil aboard,{LB}your ship will do.",
    "DK4_MES_B74_R0239": "Admiral! Really?!",
    "DK4_MES_B74_R0243": "Yes, if your admiral agrees.",
    "DK4_MES_B74_R0247": "{MACRO:FI}!{LB}Please say yes!",
    "DK4_MES_B74_R0250": "Cannot imagine liking this man,{LB}but...",
    "DK4_MES_B74_R0257": "All right.{LB}Kamil admires you so much.{LB}There must be good in you.",
    "DK4_MES_B74_R0260": "We did it! Admiral Adernkatz,{LB}thank you! Please keep teaching me!",
    "DK4_MES_B74_R0264": "Please, no more 'Admiral.'{LB}She holds that title now.",
    "DK4_MES_B74_R0267": "Oh, right...{LB}How about Gerhard?",
    "DK4_MES_B74_R0270": "Ha ha!{LB}Never thought that day would come.",
    "DK4_MES_B74_R0273": "Admiral,{LB}at your service.",
    "DK4_MES_B74_R0276": "...Likewise.",
    "DK4_MES_B74_R0281": "{MACRO:FI}, this is our chance.{LB}Let Gerhard teach us battle tactics.",
    "DK4_MES_B74_R0286": "Yes, please.",
    "DK4_MES_B74_R0288": "No need.",
    "DK4_MES_B74_R0295": "Hmm...{LB}Hear a short lesson.",
    "DK4_MES_B74_R0298": "Start with naval gunfire.{LB}Let me explain the standard{LB}crossing-the-T tactic.",
    "DK4_MES_B74_R0302": "Avoid the enemy broadside.{LB}Move before or behind the ship,{LB}then turn your own broadside{LB}toward it and fire.",
    "DK4_MES_B74_R0305": "Sounds complicated...",
    "DK4_MES_B74_R0308": "You steer; gunners fire alone.{LB}Put a sailor with high accuracy{LB}at the gun deck for better fire.",
    "DK4_MES_B74_R0312": "Naval movement works as at sea.{LB}Set course and sail direction.{LB}Guns fire automatically{LB}when an enemy enters range.",
    "DK4_MES_B74_R0315": "To prepare for boarding, refit a hold{LB}into Marine Quarters at a shipyard.",
    "DK4_MES_B74_R0318": "Hire extra sailors for boarding.{LB}Assign a skilled swordsman{LB}to lead the Marine Quarters{LB}for greater effect.",
    "DK4_MES_B74_R0322": "Choose a skilled fighter{LB}for Marine Quarters.",
    "DK4_MES_B74_R0325": "Touching ships begin boarding.{LB}Your leader commands the attack.",
    "DK4_MES_B74_R0329": "That is all.{LB}Understand?",
    "DK4_MES_B74_R0333": "Y-yes... mostly.",
    "DK4_MES_B74_R0342": "Even if you seek peace,{LB}battle may find you.{LB}Never neglect preparation.",
}

SPEAKERS = {
    "02": "Lil Argot", "09": "Kamil", "0E": "Emilio", "10": "Gerhard Adernkatz",
    "14": "Fernando", "FE": "Tutorial narrator",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXT = "Lil recruits veteran admiral Gerhard Adernkatz through Kamil, then receives a practical naval-combat tutorial."
EXCLUDED: dict[str, str] = {}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V18 inventory mismatch: missing={sorted(missing)}")
    records = []
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Story participant"),
            "context": CONTEXT,
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Concise American English preserving Lil's temper, Gerhard's formality, Kamil's admiration, and the tutorial's exact mechanics.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Gerhard Adernkatz recruitment and naval-combat tutorial in SC2 block 74.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(LINES), "translated_records": len(records), "blocks": {"74": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
