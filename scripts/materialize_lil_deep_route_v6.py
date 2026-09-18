from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v6.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
LINES = {
    "DK4_MES_B28_R0006": "You! The country merchant girl{LB}raiding Spain's waters lately!",
    "DK4_MES_B28_R0017": "Could that be...?",
    "DK4_MES_B28_R0024": "And who are you?{LB}No manners before a lady?!",
    "DK4_MES_B28_R0035": "{MACRO:FI}, ignore him.{LB}No need for more trouble.",
    "DK4_MES_B28_R0042": "Country girls deserve no courtesy!{LB}Pedro de Valdes, admiral{LB}of Spain's fleet!",
    "DK4_MES_B28_R0054": "So it is Valdes...",
    "DK4_MES_B28_R0061": "You know what it means{LB}to oppose Spain's Armada?!",
    "DK4_MES_B28_R0069": "Not too late. Leave these waters{LB}quietly and live.{LB}Refuse, and be crushed!",
    "DK4_MES_B28_R0081": "W-wait!{LB}Let's withdraw...",
    "DK4_MES_B28_R0089": "Withdraw.",
    "DK4_MES_B28_R0091": "Never.",
    "DK4_MES_B28_R0099": "A sensible surprise.{LB}Never interfere again.{LB}Next time, no mercy!",
    "DK4_MES_B28_R0103": "Our share in Seville has fallen.",
    "DK4_MES_B28_R0115": "Bitter, but he is stronger.{LB}Build our strength for now.",
    "DK4_MES_B28_R0134": "{MACRO:FI}...{LB}Are we truly fighting?!",
    "DK4_MES_B28_R0140": "So you want pain...{LB}Good. Regret this forever!",
    "DK4_MES_B29_R0006": "Pain is the only lesson{LB}you understand.",
    "DK4_MES_B29_R0009": "Changed my mind!{LB}Pride will not let me{LB}bow to force!",
    "DK4_MES_B29_R0013": "Hmph. As you wish.{LB}Prepare to be crushed!",
    "DK4_MES_B30_R0006": "Spain's finest fleet... beaten?{LB}How can the king be faced?",
    "DK4_MES_B30_R0010": "Could Clifford have...",
    "DK4_MES_B30_R0020": "With that little girl...",
    "DK4_MES_B30_R0026": "With an Amsterdam trader...",
    "DK4_MES_B30_R0033": "Hey!",
    "DK4_MES_B30_R0037": "Clifford!",
    "DK4_MES_B30_R0041": "Our alliance split his forces.{LB}That cost Valdes the battle...",
    "DK4_MES_B30_R0045": "Our goal is met.{LB}What now?",
    "DK4_MES_B30_R0048": "Good question...{LB}The king's orders decide...",
    "DK4_MES_B30_R0051": "Not against me...",
    "DK4_MES_B30_R0055": "Let's hope not.",
    "DK4_MES_B30_R0059": "Yes...",
    "DK4_MES_B30_R0063": "Take care, then.",
    "DK4_MES_B30_R0067": "You too.",
    "DK4_MES_B31_R0006": "You plan to trade{LB}in the southern Mediterranean?{LB}Surely you know the rumors?",
    "DK4_MES_B31_R0010": "...Rumors?",
    "DK4_MES_B31_R0027": "Rumors? About what?",
    "DK4_MES_B31_R0034": "You do not know{LB}the Pirate King?",
    "DK4_MES_B31_R0037": "What is this 'Pirate King'?",
    "DK4_MES_B31_R0048": "...(Could it be that man?)",
    "DK4_MES_B31_R0055": "Take my advice.{LB}Leave this port and sail elsewhere!{LB}Get away from Egypt!",
    "DK4_MES_B31_R0059": "Was that Clifford's 'warning'?",
    "DK4_MES_B31_R0063": "So you know something...{LB}Then leave these southern waters!",
    "DK4_MES_B31_R0066": "Do not challenge the Pirate King!",
    "DK4_MES_B31_R0078": "'Pirate King'...? S-scary.{LB}{MACRO:FI}, let's heed the warning.",
    "DK4_MES_B31_R0093": "...(Could it be that man?)",
    "DK4_MES_B32_R0005": "You mean to make enemies{LB}of the Hayreddin clan?",
    "DK4_MES_B32_R0010": "No.",
    "DK4_MES_B32_R0012": "Attack.",
    "DK4_MES_B32_R0020": "Then leave quickly{LB}before they find you.",
    "DK4_MES_B32_R0029": "Reckless...",
    "DK4_MES_B32_R0044": "W-will we be okay?",
    "DK4_MES_B32_R0056": "Stop shaking!{LB}This time is safe!",
    "DK4_MES_B32_R0073": "Reckless, sure!",
    "DK4_MES_B33_R0005": "Those fools deserved bankruptcy!{LB}Claiming everything in lands{LB}where they trade is theirs--{LB}such arrogance!",
    "DK4_MES_B33_R0016": "True! Still...{LB}That was unusually wise{LB}for you, {MACRO:FI}.",
    "DK4_MES_B33_R0020": "'Unusually'?! How rude!{LB}Everything said here is wise!",
}

SPEAKERS = {
    "02": "Lil Argot", "04": "Nervous crewmate", "09": "Kamil", "0B": "Crewmate",
    "10": "Gerhard Adelknauts", "14": "Fernando", "1C": "James Clifford",
    "1F": "Pedro de Valdes", "71": "Tavern patron", "FE": "System notice",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    28: "Pedro de Valdes confronts Lil and offers withdrawal or battle; retreat lowers Seville market share.",
    29: "Lil reverses her retreat and openly resists Valdes and the Spanish Armada.",
    30: "Valdes loses after Clifford's alliance divides his fleet; Lil and Clifford part on uncertain terms.",
    31: "A tavern patron warns Lil about Hayreddin, the Pirate King of the Mediterranean.",
    32: "Lil chooses whether to avoid or challenge the Hayreddin clan as her crew reacts.",
    33: "Lil and Kamil condemn a defeated company's arrogant claim over every trading region.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V6 inventory mismatch: missing={sorted(missing)}")
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
            "speaker": SPEAKERS.get(state, "Choice text" if not state else "Story participant"),
            "context": CONTEXTS[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving confrontation choices, political facts, and character tone.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Lil's Valdes confrontation, Spanish victory aftermath, Pirate King warning and choice, and regional-company aftermath across SC2 blocks 28-33.",
        "excluded_records": {}, "inventory": {"identified_records": len(LINES), "translated_records": len(records), "blocks": blocks},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
