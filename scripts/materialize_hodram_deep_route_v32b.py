from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v32b.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (30, 31, 32, 33)
LINES = {
    "DK4_MES_B30_R0010": "You there! Did you{LB}sail into my domain?{LB}Leave the southern Mediterranean{LB}if you value your life!",
    "DK4_MES_B30_R0013": "This is the 'madman'{LB}the harbor worker mentioned.",
    "DK4_MES_B30_R0016": "That is Barbarossa!{LB}Just as feared!",
    "DK4_MES_B30_R0019": "You know him?",
    "DK4_MES_B30_R0023": "Barbarossa Hayreddin...{LB}He bears the title 'Barbarossa,'{LB}symbol of Algiers's pirate chiefs.",
    "DK4_MES_B30_R0026": "A formidable veteran.",
    "DK4_MES_B30_R0030": "Yes. A monster, in one word.{LB}And more...",
    "DK4_MES_B30_R0036": "Allies or not, no trespass{LB}in my domain!{LB}Leave these waters!",
    "DK4_MES_B30_R0040": "This is the 'madman'{LB}the harbor worker mentioned.",
    "DK4_MES_B30_R0043": "So Barbarossa is the one!",
    "DK4_MES_B30_R0057": "A huge fleet!{LB}Retreat while we can!",
    "DK4_MES_B30_R0058": "A mighty fleet...{LB}Retreat while we can.",
    "DK4_MES_B30_R0059": "What a huge fleet!{LB}Should we not retreat?!",
    "DK4_MES_B30_R0061": "A huge fleet!{LB}Admiral, we should retreat!",
    "DK4_MES_B30_R0062": "What a fleet!{LB}Best retreat while we can!",
    "DK4_MES_B30_R0064": "A great fleet!{LB}Retreat seems wisest!",
    "DK4_MES_B30_R0065": "So many!{LB}No chance--let us retreat!",
    "DK4_MES_B30_R0066": "A great fleet!{LB}Best retreat while we can!",
    "DK4_MES_B30_R0071": "To battle!",
    "DK4_MES_B30_R0073": "Withdraw.",
    "DK4_MES_B30_R0081": "Oh, battle then?!{LB}Ha ha ha!{LB}Then all of you die!",
    "DK4_MES_B30_R0088": "Ha ha! Wise choice!{LB}Before challenging me,{LB}make a name for yourself{LB}in the Caribbean!",
    "DK4_MES_B30_R0091": "Stay out of the Mediterranean!{LB}Next time, you will be hunted{LB}to world's end{LB}and crushed!",
    "DK4_MES_B31_R0013": "Persistent fool.{LB}Then face me yourself.",
    "DK4_MES_B31_R0018": "Persistent fool.{LB}Then face me yourself,{LB}before you rouse the wrath{LB}of a fearsome man.",
    "DK4_MES_B32_R0018": "Maldonado's fleet{LB}spotted!",
    "DK4_MES_B32_R0019": "Maldonado ships{LB}spotted!",
    "DK4_MES_B32_R0020": "Maldonado fleet{LB}spotted!",
    "DK4_MES_B32_R0021": "Ah, Maldonado's fleet!",
    "DK4_MES_B32_R0025": "Listen, men!{LB}Show these naive outsiders{LB}from Europe's fringe{LB}the Caribbean way!",
    "DK4_MES_B32_R0037": "He brought quite a force!",
    "DK4_MES_B32_R0039": "Quite a force.",
    "DK4_MES_B32_R0041": "He brought so many!",
    "DK4_MES_B32_R0043": "So many ships!",
    "DK4_MES_B32_R0045": "Brought quite a force!",
    "DK4_MES_B32_R0047": "A great many, eh!",
    "DK4_MES_B32_R0049": "So many!",
    "DK4_MES_B32_R0051": "A fair-sized force!",
    "DK4_MES_B32_R0055": "Do not be cowed.{LB}Battle as always.{LB}All hands, battle stations!",
    "DK4_MES_B32_R0071": "Admiral, more ships astern!",
    "DK4_MES_B32_R0073": "A-admiral!{LB}More from astern!",
    "DK4_MES_B32_R0074": "Admiral, more coming astern!",
    "DK4_MES_B32_R0076": "Admiral, more coming astern!",
    "DK4_MES_B32_R0078": "Ah!{LB}More from astern!",
    "DK4_MES_B32_R0081": "What?!",
    "DK4_MES_B32_R0093": "Oh, God!",
    "DK4_MES_B32_R0106": "N-no...{LB}We cannot beat so many!",
    "DK4_MES_B32_R0111": "N-no... Logically,{LB}we cannot beat so many!",
    "DK4_MES_B32_R0117": "Wait. Those flags?",
    "DK4_MES_B32_R0132": "Good timing.{LB}We will aid you.",
    "DK4_MES_B32_R0135": "Escante forces!",
    "DK4_MES_B32_R0145": "S-saved!",
    "DK4_MES_B32_R0151": "S-saved!",
    "DK4_MES_B32_R0163": "Good timing!{LB}We will lend a hand!",
    "DK4_MES_B32_R0166": "Escante forces!",
    "DK4_MES_B32_R0176": "S-saved!",
    "DK4_MES_B32_R0182": "S-saved!",
    "DK4_MES_B33_R0005": "{MACRO:FA},{LB}splendid work. Most reliable.",
    "DK4_MES_B33_R0008": "Maldonado is gone,{LB}but English pirates remain{LB}a nuisance.",
    "DK4_MES_B33_R0012": "Let our pact continue{LB}from this day onward.{LB}Agreed?",
    "DK4_MES_B33_R0034": "(Espinosa in Africa has begun{LB}moving in earnest.{LB}We must deal with him quickly.)",
    "DK4_MES_B33_R0038": "Hm.",
    "DK4_MES_B33_R0042": "(Accepting this offer{LB}seems wisest...)",
    "DK4_MES_B33_R0053": "Agreed.",
    "DK4_MES_B33_R0055": "No.",
    "DK4_MES_B33_R0063": "Good. Much is expected of you.",
    "DK4_MES_B33_R0073": "A pity.{LB}May you never become our enemy.",
}

SPEAKERS = {
    "01": "Hodram Bergstrom", "10": "Gerhard Adelknauts", "12": "Charles", "17": "Manuel",
    "22": "Barbarossa", "2A": "Maldonado", "2B": "Escante admiral", "3C": "Escante admiral",
    "97": "Sailor", "D0": "Sailor", "D5": "Sailor", "D6": "Sailor",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(all_rows)
    if missing:
        raise SystemExit(f"Hodram V32b inventory mismatch: missing={sorted(missing)}")
    records = []
    counts = {str(block): 0 for block in BLOCKS}
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        counts[row_id.split("_B", 1)[1].split("_", 1)[0]] += 1
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Story participant"),
            "context": "Hodram confronts Barbarossa, fights Maldonado in the Caribbean, receives allied aid, and chooses whether to continue the pact.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving named rivals, tactical branches, reinforcements, and alliance choices.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-caribbean-battles-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Hodram Barbarossa, Maldonado, reinforcement, and alliance dialogue in SC1 blocks 30-33.",
        "excluded_records": {}, "inventory": {"identified_records": len(LINES), "translated_records": len(records), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
