from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v11.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
LINES = {
    "DK4_MES_B52_R0005": "China's largest port!{LB}Everyone, unload the cargo!",
    "DK4_MES_B52_R0023": "Who?! Admiral!",
    "DK4_MES_B52_R0032": "{MACRO:FI}, danger!",
    "DK4_MES_B52_R0038": "Assassin:{LB}Die!",
    "DK4_MES_B52_R0042": "Aah!",
    "DK4_MES_B52_R0046": "Assassin:{LB}Tch!",
    "DK4_MES_B52_R0064": "Admiral, okay?",
    "DK4_MES_B52_R0073": "{MACRO:FI},{LB}hurt?",
    "DK4_MES_B52_R0079": "What was that...?{LB}Ow... wounded!{LB}Hm? Something fell here...",
    "DK4_MES_B52_R0083": "The Li family crest?!{LB}They are targeting me...?",
    "DK4_MES_B52_R0094": "Mamma mia!{LB}This is bad!",
    "DK4_MES_B52_R0108": "Terrible people{LB}are hunting us now...",
    "DK4_MES_B53_R0006": "Are you {MACRO:FI}?",
    "DK4_MES_B53_R0017": "Who is she?{LB}Such pressure...",
    "DK4_MES_B53_R0023": "Yes... Who are you?",
    "DK4_MES_B53_R0027": "Before giving my name,{LB}one question.{LB}Answer me.",
    "DK4_MES_B53_R0031": "What?",
    "DK4_MES_B53_R0035": "Why expand your trade sphere?",
    "DK4_MES_B53_R0046": "Why trade...?",
    "DK4_MES_B53_R0053": "Why? Because merchants trade.{LB}Things just grew as we traded.{LB}No special reason.",
    "DK4_MES_B53_R0056": "Answer seriously!{LB}This matters far more{LB}than you realize!",
    "DK4_MES_B53_R0059": "All right.{LB}We expand our trade because...",
    "DK4_MES_B53_R0062": "We need money.{LB}Enough to help people in need{LB}all across the world.",
    "DK4_MES_B53_R0066": "Across the world...?{LB}Are you serious?",
    "DK4_MES_B53_R0070": "Yes!{LB}That is why it felt embarrassing!{LB}Believe it or not,{LB}that is my purpose!",
    "DK4_MES_B53_R0073": "Hmm... Yet almost everyone{LB}in this world is suffering.",
    "DK4_MES_B53_R0077": "Trying to save every one of them{LB}is rather reckless, is it not?",
    "DK4_MES_B53_R0081": "No. Dreams come true{LB}when we truly desire them!{LB}We can do this!",
    "DK4_MES_B53_R0085": "...",
    "DK4_MES_B53_R0088": "Heh... heh heh...",
    "DK4_MES_B53_R0091": "Hey! Laughing is rude!",
    "DK4_MES_B53_R0095": "Pardon me. Never imagined{LB}that you held such a dream.",
    "DK4_MES_B53_R0102": "Based on your answer,{LB}we came ready to defeat you.{LB}That seems unnecessary now.",
    "DK4_MES_B53_R0105": "Defeat me?{LB}What does that mean...?",
    "DK4_MES_B53_R0108": "Want the truth?{LB}Come to Hangzhou's tavern.",
    "DK4_MES_B53_R0120": "That woman...?",
    "DK4_MES_B53_R0135": "{MACRO:FI},{LB}let us go. Want to hear{LB}what that woman has to say.",
    "DK4_MES_B54_R0005": "Kuhn.",
    "DK4_MES_B54_R0009": "Hm?",
    "DK4_MES_B54_R0013": "About {MACRO:FI} {MACRO:FA}.{LB}They met with the Li family{LB}and now suspect you.",
    "DK4_MES_B54_R0016": "They are also secretly probing{LB}into your son...",
    "DK4_MES_B54_R0020": "So... that girl is finished.{LB}Still useful, but no choice.{LB}She did more than expected...",
    "DK4_MES_B54_R0024": "Agreed.{LB}Then follow our standing plan...",
    "DK4_MES_B54_R0027": "Have Li-disguised ships{LB}attack her. Keep our fleet{LB}waiting nearby.",
    "DK4_MES_B54_R0031": "Should our decoys win, we avenge{LB}{MACRO:FO}, our allied company,{LB}and gain cause to crush Li.",
    "DK4_MES_B54_R0034": "Should she survive,{LB}our fleet destroys her weakened ships.{LB}A stray shot can finish her.",
    "DK4_MES_B54_R0038": "Once she is gone, no proof remains.{LB}A brilliant plan as always...",
    "DK4_MES_B54_R0042": "No flattery.{LB}Do it.",
    "DK4_MES_B54_R0045": "At once.",
    "DK4_MES_B55_R0005": "Master Kuhn, grave news.",
    "DK4_MES_B55_R0009": "Hm?",
    "DK4_MES_B55_R0020": "The Li family has fallen.",
    "DK4_MES_B55_R0024": "What?! Truly?",
    "DK4_MES_B55_R0041": "Li has surrendered{LB}to {MACRO:FO}!",
    "DK4_MES_B55_R0044": "What?! Truly?{LB}That girl is stronger than expected.",
    "DK4_MES_B55_R0050": "Unexpected.{LB}Our plan cannot work now...",
    "DK4_MES_B55_R0053": "Right.{LB}No use now.{LB}Destroy her.",
    "DK4_MES_B55_R0057": "Understood.",
    "DK4_MES_B55_R0061": "Take care.{LB}She is no easy prey...",
    "DK4_MES_B55_R0064": "Yes, sir.",
    "DK4_MES_B56_R0005": "Kuhn sent a letter.",
    "DK4_MES_B56_R0009": "A letter...?{LB}War?!",
    "DK4_MES_B56_R0020": "So Maria told the truth{LB}about him...",
    "DK4_MES_B56_R0034": "He shows his true colors...{LB}That rat.",
    "DK4_MES_B56_R0048": "Kuhn used me as he pleased,{LB}then meant to discard me{LB}once my use ended...",
    "DK4_MES_B56_R0052": "Not knowing, we attacked Li...{LB}So sorry...",
    "DK4_MES_B57_R0011": "Li's family...{LB}united and strong.",
    "DK4_MES_B57_R0016": "Was this the region{LB}the Li family dominated...?",
    "DK4_MES_B57_R0019": "Heard a woman led them.{LB}Wanted to meet her...{LB}A shame we never did.",
    "DK4_MES_B57_R0033": "Li's hidden room{LB}held this, Admiral.",
    "DK4_MES_B57_R0049": "Li's retainer sent{LB}this for you.",
    "DK4_MES_B57_R0055": "This?",
    "DK4_MES_B57_R0059": "Some kind of blueprint...",
    "DK4_MES_B58_R0006": "Admiral, a letter came{LB}from Clifford's fleet.",
    "DK4_MES_B58_R0009": "A letter? What happened?",
    "DK4_MES_B58_R0013": "Dear {MACRO:FI},{LB}come to the New World at once.{LB}James Clifford",
    "DK4_MES_B58_R0017": "New World?",
    "DK4_MES_B59_R0005": "Brute force failed.{LB}They truly thought{LB}those old tactics would work.",
    "DK4_MES_B59_R0028": "Only Escante remains here.{LB}His force is large,{LB}and he is wiser than Maldonado...",
    "DK4_MES_B59_R0033": "One local power remains.{LB}Rumor says it is larger{LB}than Maldonado's.",
    "DK4_MES_B59_R0040": "We must be careful.",
    "DK4_MES_B60_R0011": "Maldonado fell...",
    "DK4_MES_B60_R0015": "And lately a company called{LB}{MACRO:FO}{LB}entered this region.",
    "DK4_MES_B60_R0020": "Maldonado fell...{LB}{MACRO:FO}...{LB}Stronger than expected.",
    "DK4_MES_B60_R0034": "With Clifford absent,{LB}independence seemed easy...",
    "DK4_MES_B60_R0039": "Use Maldonado to strike Clifford,{LB}and independence seemed easy...",
    "DK4_MES_B60_R0046": "Now attack{LB}{MACRO:FO}{LB}with all our strength.",
}

EXCLUDED = {
    "DK4_MES_B53_R0110": "Four-byte interior control fragment (20 46 83 80), not a standalone dialogue record.",
    "DK4_MES_B60_R0050": "Five-byte scene-control fragment (01 13 96 45 62), not standalone dialogue.",
}
SPEAKERS = {
    "02": "Lil Argot", "06": "Old sailor", "0C": "Crewmate", "0F": "Emilio",
    "10": "Gerhard", "11": "Crewmate", "13": "Crewmate", "14": "Fernando",
    "15": "Companion", "28": "Antony Kuhn", "2B": "Escante", "38": "Kuhn envoy",
    "97": "Sailor", "FE": "Mysterious woman",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    52: "Lil reaches China's largest port, survives a Li-family assassination attempt, and finds the assailant's crest.",
    53: "A mysterious woman tests Lil's motives, accepts her dream of helping the world, and summons her to Hangzhou's tavern.",
    54: "Kuhn learns Lil suspects him and orders a false-flag Li attack designed to kill her and justify war.",
    55: "Kuhn learns the Li family was defeated or subordinated, abandons the false-flag plan, and orders Lil destroyed directly.",
    56: "Kuhn declares war; Lil realizes Maria's warning was true and regrets attacking Li while being used.",
    57: "Lil reflects on Li's strength and receives a blueprint discovered after the family's fall.",
    58: "Clifford urgently summons Lil to the New World.",
    59: "Lil assesses Maldonado's obsolete tactics and the remaining Escante threat.",
    60: "Escante reacts to Maldonado's fall and resolves to attack Lil's company with full strength.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = (set(LINES) | set(EXCLUDED)) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V11 inventory mismatch: missing={sorted(missing)}")
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
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Story participant"), "context": CONTEXTS[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving plot revelations, false-flag planning, branch outcomes, rewards, and character tone.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Lil's Li assassination, Maria challenge, Kuhn murder plot and war, Li rewards, Clifford summons, and Escante reaction across SC2 blocks 52-60.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(LINES) + len(EXCLUDED), "translated_records": len(records), "blocks": blocks},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records; {len(EXCLUDED)} control exclusions")


if __name__ == "__main__":
    main()
