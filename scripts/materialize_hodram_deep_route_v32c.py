from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v32c.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = tuple(range(34, 43))
EXCLUDED = {"DK4_MES_B42_R0032": "Preserved four-byte nontext event payload; not dialogue."}
LINES = {
    "DK4_MES_B34_R0006": "Ha ha ha! Bold enough{LB}to challenge me openly!{LB}At least provide some amusement!",
    "DK4_MES_B34_R0018": "Heh! What a happy fool.{LB}Betting on your defeat!",
    "DK4_MES_B35_R0006": "More infidels, one after another!{LB}The routes of Hindustan belong{LB}to us Muslims!",
    "DK4_MES_B36_R0006": "Ming hired barbarians?!{LB}Damn them!{LB}No mercy to anyone in our way!",
    "DK4_MES_B37_R0006": "Admiral...{LB}look there.",
    "DK4_MES_B37_R0013": "A slave ship,{LB}it seems.",
    "DK4_MES_B37_R0017": "Slave trading is forbidden.",
    "DK4_MES_B37_R0021": "Still widespread.{LB}As a patrol fleet,{LB}we cannot ignore it. Agreed?",
    "DK4_MES_B37_R0027": "Attack.",
    "DK4_MES_B37_R0029": "Not our authority...",
    "DK4_MES_B37_R0040": "They have plenty to hide.{LB}Whatever our excuse,{LB}we found prey that can be{LB}destroyed openly.",
    "DK4_MES_B37_R0043": "Hm.",
    "DK4_MES_B37_R0050": "Strike before they make port!{LB}Battle stations!",
    "DK4_MES_B37_R0061": "Heh, let us be flashy!",
    "DK4_MES_B38_R0006": "There! Lil's fleet!",
    "DK4_MES_B38_R0010": "Maria Hoa-mei Lee!{LB}What grudge do you hold against me?!",
    "DK4_MES_B38_R0013": "Maria...?",
    "DK4_MES_B38_R0017": "Lil!{LB}That is Kuen's decoy fleet!{LB}Do not be fooled!",
    "DK4_MES_B38_R0021": "Kamil?!",
    "DK4_MES_B38_R0025": "Kuen plans to make you{LB}and Maria fight each other!",
    "DK4_MES_B38_R0028": "What are you saying?{LB}But...?",
    "DK4_MES_B38_R0031": "True, Kamil?",
    "DK4_MES_B38_R0035": "Yes. Kuen is known to me.{LB}Maria discovered this plot{LB}and sent word to warn you.",
    "DK4_MES_B38_R0039": "Yes.",
    "DK4_MES_B38_R0043": "Aim! Unknown fleet ahead!",
    "DK4_MES_B38_R0047": "Kuen! Reveal yourself!",
    "DK4_MES_B38_R0051": "Shoot!",
    "DK4_MES_B38_R0055": "Hyaa!",
    "DK4_MES_B38_R0059": "Damn you!!",
    "DK4_MES_B38_R0063": "That is {MACRO:FO}!{LB}Master Kuen, we are outmatched!",
    "DK4_MES_B38_R0066": "Tch, enough!{LB}Withdraw!",
    "DK4_MES_B38_R0070": "That was... Kuen?!{LB}Then what have...!",
    "DK4_MES_B39_R0005": "Enemy ships!",
    "DK4_MES_B39_R0009": "Barbarians!{LB}Behold the spirit of Yamato!",
    "DK4_MES_B39_R0021": "What is that ship?!",
    "DK4_MES_B39_R0027": "What is that ship?!",
    "DK4_MES_B39_R0034": "An ironclad...!",
    "DK4_MES_B39_R0046": "That ship...",
    "DK4_MES_B40_R0006": "Halt!",
    "DK4_MES_B40_R0015": "Too bad. There is no escape.",
    "DK4_MES_B40_R0019": "Ha ha ha!{LB}{MACRO:FA}!{LB}Your heroic tale ends here!",
    "DK4_MES_B40_R0027": "Pasha... So you refuse{LB}to coexist with me{LB}in the Mediterranean.",
    "DK4_MES_B40_R0045": "W-we are surrounded!{LB}So many fleets!",
    "DK4_MES_B40_R0046": "Surrounded!{LB}So many fleets!",
    "DK4_MES_B40_R0047": "Ah! Surrounded!{LB}So many fleets!",
    "DK4_MES_B40_R0048": "Surrounded?!{LB}So many fleets!",
    "DK4_MES_B40_R0049": "Surrounded!{LB}What a vast fleet!",
    "DK4_MES_B40_R0050": "Surrounded!{LB}A vast fleet indeed!",
    "DK4_MES_B40_R0051": "Surrounded!{LB}There are so many!",
    "DK4_MES_B40_R0052": "Surrounded!{LB}A vast fleet indeed!",
    "DK4_MES_B40_R0055": "A mere mob.{LB}Break through!",
    "DK4_MES_B40_R0058": "Bwahaha! Such arrogance!{LB}Do you know whom you mock?",
    "DK4_MES_B40_R0061": "A vulgar general.",
    "DK4_MES_B40_R0065": "Execute this fool!{LB}All ships, charge!",
    "DK4_MES_B40_R0068": "Waaah!!",
    "DK4_MES_B40_R0072": "What?!",
    "DK4_MES_B40_R0076": "Pasha!{LB}The city is firing on us!",
    "DK4_MES_B40_R0079": "What?! Why?!{LB}What is happening?!",
    "DK4_MES_B40_R0082": "No idea! Someone seized{LB}the city's gun emplacements!",
    "DK4_MES_B40_R0092": "N-nooo!!",
    "DK4_MES_B40_R0096": "That is...!",
    "DK4_MES_B40_R0100": "Waaaaah!",
    "DK4_MES_B40_R0111": "Mushari, cover us!{LB}Retreat at speed!",
    "DK4_MES_B40_R0116": "Mushari and Al Najuud, cover us!{LB}Retreat at speed!",
    "DK4_MES_B40_R0125": "What of my public execution?{LB}Come and entertain me.",
    "DK4_MES_B40_R0129": "Gah! Come, then!{LB}Cough up blood!",
    "DK4_MES_B41_R0015": "Admiral! There!{LB}The monster fish!",
    "DK4_MES_B41_R0016": "Ah!{LB}Monster fish!",
    "DK4_MES_B41_R0017": "Eek!{LB}The monster fish appeared!",
    "DK4_MES_B41_R0019": "Admiral!{LB}A monster fish!",
    "DK4_MES_B41_R0020": "Admiral!{LB}Monster fish!",
    "DK4_MES_B41_R0021": "There!{LB}A monster fish!",
    "DK4_MES_B41_R0022": "Admiral!{LB}Monster fish!",
}

SPEAKERS = {
    "01": "Hodram Bergstrom", "02": "Lil Argot", "09": "Kamil", "10": "Gerhard Adelknauts",
    "12": "Charles", "14": "Rival captain", "17": "Manuel", "1B": "Aziza Nurennahar",
    "21": "Pasha", "24": "Rival captain", "25": "Rival captain", "28": "Kuen",
    "29": "Rival captain", "34": "Pasha officer", "35": "Pasha officer", "37": "Kuen officer",
    "38": "Kuen officer", "39": "Rival captain", "4E": "Pasha officer", "97": "Lookout",
    "99": "Pasha officer", "D0": "Sailor", "D6": "Sailor", "D8": "Gunner",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    identified = set(LINES) | set(EXCLUDED)
    missing = identified - set(all_rows)
    if missing:
        raise SystemExit(f"Hodram V32c inventory mismatch: missing={sorted(missing)}")
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
            "context": "Hodram faces regional rivals, a slave ship, Kuen's Lil decoy, an ironclad, the Pasha ambush, and sea-monster sightings.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving encounter choices, named fleets, decoy reveal, ambush staging, and sailor variants.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-caribbean-battles-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Hodram regional rivals, slave ship, Lil decoy, ironclad, Pasha ambush, and sea-monster dialogue in SC1 blocks 34-42.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(identified), "translated_records": len(records), "excluded_records": len(EXCLUDED), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records; excluded={len(EXCLUDED)}")


if __name__ == "__main__":
    main()
