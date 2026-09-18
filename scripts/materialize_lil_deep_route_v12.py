from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v12.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
LINES = {
    "DK4_MES_B61_R0006": "Enough.",
    "DK4_MES_B61_R0016": "Hey! Let go of me!",
    "DK4_MES_B61_R0021": "What are you doing? Let go!{LB}You...!!",
    "DK4_MES_B61_R0035": "What is this?!",
    "DK4_MES_B61_R0042": "Clifford?!{LB}What is this?",
    "DK4_MES_B61_R0045": "Those pests finally{LB}dropped dead.",
    "DK4_MES_B61_R0048": "{MACRO:FI},{LB}you helped me in many ways.{LB}You have my thanks.",
    "DK4_MES_B61_R0052": "And asking this now{LB}truly pains me, but...",
    "DK4_MES_B61_R0055": "Give me all your proofs.{LB}Do that, and he lives.",
    "DK4_MES_B61_R0059": "What is this?!{LB}A hostage? Coward!",
    "DK4_MES_B61_R0070": "What is this?!{LB}This is not like you!",
    "DK4_MES_B61_R0081": "We were allies!{LB}We worked together{LB}and helped each other!",
    "DK4_MES_B61_R0085": "That is over.",
    "DK4_MES_B61_R0091": "We are allies!{LB}Drawing a sword on your ally{LB}takes nerve!",
    "DK4_MES_B61_R0095": "Ended, now.",
    "DK4_MES_B61_R0102": "Planned from the start...?",
    "DK4_MES_B61_R0106": "Sorry. Exactly.",
    "DK4_MES_B61_R0118": "We were all deceived...",
    "DK4_MES_B61_R0125": "Cruel...",
    "DK4_MES_B61_R0129": "The proofs interested me too.",
    "DK4_MES_B61_R0133": "But the crown ordered me{LB}to watch Spain.{LB}My freedom is limited.",
    "DK4_MES_B61_R0137": "So someone else had to gather{LB}the proofs.{LB}You were perfect for that.",
    "DK4_MES_B61_R0149": "That is inhuman!{LB}Using someone like that!",
    "DK4_MES_B61_R0155": "You used me completely...{LB}Clifford!{LB}Never forgiven!",
    "DK4_MES_B61_R0159": "Recall what you said as allies.{LB}Think my conscience felt nothing?{LB}But this was my only path.",
    "DK4_MES_B61_R0170": "Conscience?!{LB}Why do this?",
    "DK4_MES_B61_R0177": "{MACRO:FI},{LB}my dream is yours.{LB}Understand.",
    "DK4_MES_B61_R0181": "Your dream matches mine?{LB}Do not make me laugh!",
    "DK4_MES_B61_R0184": "Why hide it now?{LB}You seek the proofs to conquer{LB}every sea in the world too.",
    "DK4_MES_B61_R0187": "No! We are different!",
    "DK4_MES_B61_R0191": "My dream is to help people...{LB}No. You will never hear it.{LB}You could never understand{LB}my dream.",
    "DK4_MES_B61_R0194": "Not the same dream? A shame.{LB}Still, your proofs are mine.",
    "DK4_MES_B61_R0198": "No wish to kill your comrade.{LB}Do not make me a worse villain.{LB}Hand them over.",
    "DK4_MES_B61_R0201": "...Okay.",
    "DK4_MES_B61_R0213": "{MACRO:FI}!{LB}No! Do not!",
    "DK4_MES_B61_R0216": "But Kamil's life matters more!",
    "DK4_MES_B61_R0222": "A wise choice.{LB}Gladly accepted.",
    "DK4_MES_B61_R0238": "Thales' Paper Map was stolen!",
    "DK4_MES_B61_R0250": "Ull's Bow was stolen!",
    "DK4_MES_B61_R0270": "Periander's Stone Map was stolen!",
    "DK4_MES_B61_R0282": "Axum's Gold Seal was stolen!",
    "DK4_MES_B61_R0302": "Solon's Leaf Map was stolen!",
    "DK4_MES_B61_R0314": "Rig Veda was stolen!",
    "DK4_MES_B61_R0334": "Cleobulus' Cloth Map was stolen!",
    "DK4_MES_B61_R0346": "Cambyses' Crown was stolen!",
    "DK4_MES_B61_R0366": "Chiron's Bamboo Map was stolen!",
    "DK4_MES_B61_R0378": "Qin's Changxin Lamp was stolen!",
    "DK4_MES_B61_R0410": "Bias' Coin Map was stolen!",
    "DK4_MES_B61_R0425": "Kediri's Eternal Talisman was stolen!",
    "DK4_MES_B61_R0445": "Pittacus' Blade Map was stolen!",
    "DK4_MES_B61_R0457": "Crystal Skull was stolen!",
    "DK4_MES_B62_R0017": "Escante...{LB}His elite Spanish navy is gone.",
    "DK4_MES_B62_R0022": "Escante once dominated{LB}the waters near Veracruz,{LB}but now he is gone...",
    "DK4_MES_B62_R0030": "Escante is finished...{LB}A formidable enemy.",
    "DK4_MES_B62_R0044": "A nation ruled by him{LB}would have been terrifying.{LB}Endless wars, suffering people...",
    "DK4_MES_B62_R0063": "Admiral, Escante's study{LB}held this...",
    "DK4_MES_B62_R0068": "{MACRO:FI}!{LB}This was found{LB}in Escante's study.",
    "DK4_MES_B62_R0094": "After his submission,{LB}Escante's men brought this.",
    "DK4_MES_B62_R0100": "After his submission,{LB}Escante's men brought this.",
    "DK4_MES_B62_R0110": "A sword sheath?{LB}Could this concern{LB}a Proof of Supremacy?",
    "DK4_MES_B63_R0005": "The Ceremonial Knife fits{LB}the Sun-Patterned Sheath.{LB}Can we try it?",
    "DK4_MES_B63_R0015": "Maybe. But something may happen.{LB}Could be dangerous.",
    "DK4_MES_B63_R0021": "Wait.{LB}There might be a trap...",
    "DK4_MES_B63_R0027": "Too cautious! No way.{LB}We only slide the knife{LB}into the sheath...{LB}Aah!",
    "DK4_MES_B63_R0036": "What is that light?!",
    "DK4_MES_B63_R0042": "What is that light?!",
    "DK4_MES_B63_R0049": "So bright!{LB}What is happening?!",
    "DK4_MES_B63_R0059": "Whew... seems safe now.{LB}But what is this?",
    "DK4_MES_B63_R0062": "A map?{LB}Out of a knife???",
    "DK4_MES_B63_R0065": "No idea...{LB}But this must be a map{LB}to the New World's proof, right?",
    "DK4_MES_B63_R0069": "M-maybe so.{LB}Strange, but finding it is good...{LB}right?",
    "DK4_MES_B63_R0074": "Whew... seems safe now.{LB}But what is this?",
    "DK4_MES_B63_R0077": "A map?{LB}Out of a knife???",
    "DK4_MES_B63_R0080": "How should we know?{LB}But is this a map{LB}to the New World's proof?",
    "DK4_MES_B63_R0083": "M-maybe so.{LB}Strange, but finding it is good...{LB}right?",
}

EXCLUDED = {
    "DK4_MES_B61_R0226": "Two-byte branch control fragment (94 82), not dialogue.",
    "DK4_MES_B61_R0258": "Two-byte branch control fragment (96 82), not dialogue.",
    "DK4_MES_B61_R0290": "Two-byte branch control fragment (97 82), not dialogue.",
    "DK4_MES_B61_R0322": "Two-byte branch control fragment (95 82), not dialogue.",
    "DK4_MES_B61_R0354": "Two-byte branch control fragment (99 82), not dialogue.",
    "DK4_MES_B61_R0386": "Two-byte branch control fragment (98 82), not dialogue.",
    "DK4_MES_B61_R0393": "Two-byte branch control fragment (9F 82), not dialogue.",
    "DK4_MES_B61_R0433": "Two-byte branch control fragment (9A 82), not dialogue.",
}
SPEAKERS = {
    "02": "Lil Argot", "06": "Old sailor", "07": "Crewmate", "09": "Kamil",
    "10": "Gerhard", "14": "Fernando", "1C": "James Clifford", "97": "Sailor",
    "FE": "System notice",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    61: "Clifford takes Kamil hostage, reveals he used Lil to gather the Proofs of Supremacy, steals all assembled proof items, and ends their alliance.",
    62: "Lil reflects on Escante's defeat or submission and receives the Sun-Patterned Sheath from his estate or retainers.",
    63: "Lil combines the Ceremonial Knife with the Sun-Patterned Sheath and reveals the New World Proof of Supremacy map.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = (set(LINES) | set(EXCLUDED)) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V12 inventory mismatch: missing={sorted(missing)}")
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
            "localization_note": "Faithful concise American English preserving Clifford's betrayal, proof-item losses, branch rewards, ritual logic, and character tone.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Clifford's betrayal and proof theft, Escante outcomes and sheath reward, and the New World proof-map ritual across SC2 blocks 61-63.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(LINES) + len(EXCLUDED), "translated_records": len(records), "blocks": blocks},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records; {len(EXCLUDED)} control exclusions")


if __name__ == "__main__":
    main()
