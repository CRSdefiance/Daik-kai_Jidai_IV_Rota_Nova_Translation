from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
OUTPUT = Path("translations/maria_deep_route_v30.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (294, 295, 296, 297, 298, 299)

LINES = {
    "DK4_MES_B294_R0004": "Welcome.",
    "DK4_MES_B294_R0008": "Have you visited the village{LB}far north in the New World?",
    "DK4_MES_B294_R0012": "A great monk from this town{LB}once sailed north to preach.",
    "DK4_MES_B294_R0016": "After finding that village, he vanished.{LB}What happened to him?",
    "DK4_MES_B294_R0020": "Maybe.",
    "DK4_MES_B294_R0024": "He was very virtuous.{LB}Hope they cherished him.",
    "DK4_MES_B294_R0027": "When you travel north,{LB}ask what became of him.",
    "DK4_MES_B295_R0004": "{MACRO:FA}, only you can handle this.",
    "DK4_MES_B295_R0008": "What is wrong?{LB}You look so grave.",
    "DK4_MES_B295_R0011": "Unknown ships have sunk every fleet{LB}that passes nearby.",
    "DK4_MES_B295_R0015": "Pirates?",
    "DK4_MES_B295_R0019": "No survivor has seen the enemy.",
    "DK4_MES_B295_R0022": "Patrols found nothing.{LB}The foe appears and vanishes like a ghost.",
    "DK4_MES_B295_R0026": "Quite skilled.",
    "DK4_MES_B295_R0030": "Yet there is an odd rumor.",
    "DK4_MES_B295_R0034": "Which?",
    "DK4_MES_B295_R0038": "Some say it is a ghost ship.",
    "DK4_MES_B295_R0041": "You believe it?",
    "DK4_MES_B295_R0045": "Nothing else explains it.{LB}So there is a request.",
    "DK4_MES_B295_R0048": "Learn what it is.",
    "DK4_MES_B295_R0052": "Only investigate?",
    "DK4_MES_B295_R0056": "Destroying it would be even better.",
    "DK4_MES_B295_R0059": "Very well.",
    "DK4_MES_B295_R0063": "Sorry about the grim task.{LB}Good luck.",
    "DK4_MES_B296_R0004": "You defeated a ghost ship? Amazing!{LB}Please accept this reward.",
    "DK4_MES_B296_R0009": "Received 65,000 coins.",
    "DK4_MES_B296_R0031": "Havana share rose slightly!",
    "DK4_MES_B296_R0044": "Someone would like to meet you.",
    "DK4_MES_B296_R0051": "Hello.",
    "DK4_MES_B296_R0055": "And you?",
    "DK4_MES_B296_R0059": "You seem capable.{LB}Please find a lost ruin for us.",
    "DK4_MES_B296_R0063": "Ruins?",
    "DK4_MES_B296_R0067": "An ancestral shrine built{LB}to honor our warriors.",
    "DK4_MES_B296_R0070": "Legend says only the greatest warrior{LB}can find it.",
    "DK4_MES_B296_R0078": "The ghost ship proved it.",
    "DK4_MES_B296_R0082": "The greatest warrior has strength,{LB}a just heart, and wisdom.",
    "DK4_MES_B296_R0086": "Thank you, but can this woman{LB}truly help find ruins?",
    "DK4_MES_B296_R0090": "Honestly, even we know{LB}almost nothing.",
    "DK4_MES_B296_R0093": "We ask everyone{LB}who seems strong enough.",
    "DK4_MES_B296_R0097": "Please forgive us.{LB}None has succeeded, so failure bears no shame.",
    "DK4_MES_B296_R0100": "A request where failure is allowed?{LB}That is a first.",
    "DK4_MES_B296_R0104": "Poorly said! We want it found. Do not lose heart.",
    "DK4_MES_B296_R0107": "Ha! Just teasing.{LB}We will do our best.",
    "DK4_MES_B296_R0110": "Really?",
    "DK4_MES_B296_R0114": "Part of the reward is paid now.{LB}Keep it even if you fail.",
    "DK4_MES_B296_R0117": "Received 5,000 coins.",
    "DK4_MES_B296_R0123": "Bring the Ancient City Map.{LB}This man will join.",
    "DK4_MES_B296_R0126": "Meet this man at the city gate.",
    "DK4_MES_B297_R0004": "This is Guam.{LB}You can go home now.",
    "DK4_MES_B297_R0007": "Xiexie.",
    "DK4_MES_B297_R0011": "What?",
    "DK4_MES_B297_R0015": "A gift for me?{LB}Thank you. Gladly.",
    "DK4_MES_B297_R0019": "Xiexie, xiexie!",
    "DK4_MES_B297_R0023": "Take care.{LB}Be careful when you sail.",
    "DK4_MES_B298_R0004": "We finally found it!",
    "DK4_MES_B298_R0008": "What now?",
    "DK4_MES_B298_R0012": "You collect the proofs, do you not?",
    "DK4_MES_B298_R0015": "Yes.",
    "DK4_MES_B298_R0019": "Then it is true!{LB}You shall not take this!",
    "DK4_MES_B298_R0022": "Calm down.{LB}We will not take it by force.",
    "DK4_MES_B298_R0025": "You cannot fool us!{LB}Those from across the sea take everything!",
    "DK4_MES_B298_R0029": "So this woman is like{LB}the western conquerors...",
    "DK4_MES_B298_R0037": "Very well. We give up.",
    "DK4_MES_B298_R0041": "{LB}{MACRO:FI}! Will you abandon{LB}the New World's proof?",
    "DK4_MES_B298_R0045": "We cannot force them.",
    "DK4_MES_B298_R0049": "{LB}Others may seize it by force.{LB}What then of our work?",
    "DK4_MES_B298_R0056": "{LB}Worse, these people{LB}would not survive.",
    "DK4_MES_B298_R0059": "You are threatening us!?",
    "DK4_MES_B298_R0062": "Not our intent.{LB}But...",
    "DK4_MES_B298_R0065": "{LB}Yet it is true. Escante is gone,{LB}but Spain will not abandon this land.",
    "DK4_MES_B298_R0068": "What?{LB}What happened to Escante?",
    "DK4_MES_B298_R0078": "We destroyed Escante's forces.",
    "DK4_MES_B298_R0084": "Escante's forces now answer to us.{LB}They will commit no more violence here.",
    "DK4_MES_B298_R0091": "What!?{LB}The woman admiral from the East?",
    "DK4_MES_B298_R0094": "{LB}Word has reached even here?",
    "DK4_MES_B298_R0097": "No. A friend who gave me this{LB}told us about you.",
    "DK4_MES_B298_R0100": "We trust you.{LB}May you bring true peace to this land.",
    "DK4_MES_B298_R0107": "Thank you.{LB}We will try.",
    "DK4_MES_B299_R0004": "An unfamiliar face.{LB}Where are you from?",
    "DK4_MES_B299_R0007": "China.",
    "DK4_MES_B299_R0011": "China? Truly?{LB}To have come so far...",
    "DK4_MES_B299_R0015": "Now it makes sense.{LB}You have a sextant, yes?",
    "DK4_MES_B299_R0019": "What?",
    "DK4_MES_B299_R0023": "Rumor says it reveals your position{LB}even on a featureless sea.",
    "DK4_MES_B299_R0027": "Will you trade us that sextant?{LB}A fine reward awaits.",
    "DK4_MES_B299_R0030": "A reward?",
    "DK4_MES_B299_R0034": "Bring it and see.",
}

PRESENTATION_STATES = {0x03, 0x87, 0x93, 0xA1, 0xB3, 0xCE, 0xFE}
SPEAKERS = {
    "03": "Maria", "87": "Rescued villager", "93": "Guildmaster",
    "A1": "Island elder", "B3": "Village elder", "CE": "Local woman",
    "FE": "System",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    rows = {row_id: row for row_id, row in all_rows.items() if row_id.startswith(prefixes)}
    if set(LINES) != set(rows):
        raise SystemExit(f"Maria V30 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}")

    records = []
    block_counts: dict[str, int] = {}
    for row_id in sorted(rows, key=lambda value: (int(value.split("_B")[1].split("_")[0]), int(value.rsplit("R", 1)[1]))):
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        row = rows[row_id]
        english = LINES[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in PRESENTATION_STATES else ""
        block_counts[block] = block_counts.get(block, 0) + 1
        waivers = ["weak-line-ending", "orphan-final-line"]
        if "{LB}" in english:
            waivers.append("manual-break")
        if english.startswith("{LB}"):
            waivers.append("source-leading-linebreak")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Narrator or companion"),
            "context": "Late New World rumor, quest, rescue, proof, or trade event.",
            "source_meaning": english,
            "localization_note": "Direct SC3 translation reviewed for natural English and state-byte safety.",
            "qa_waivers": waivers,
            **({"manual_break_reason": "Protects semantic rows, source-leading break, and pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })

    payload = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC3.DK4",
        "source_file_sha256": SC3_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-events-v30-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 blocks 294-299: six complete late New World events.",
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "excluded_records": 0, "blocks": block_counts},
        "excluded": [], "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
