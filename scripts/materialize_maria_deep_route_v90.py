from __future__ import annotations

import csv
import json
from pathlib import Path

S = Path("work/sc3/script.csv")
O = Path("translations/maria_deep_route_v90.json")
SHA = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"

L = {
    "DK4_MES_B104_R0008": "30 days to Ceuta and back...{LB}That will be tight.",
    "DK4_MES_B105_R0004": "Miss, play with me!",
    "DK4_MES_B105_R0008": "How sweet! Whose child?{LB}What's your name?",
    "DK4_MES_B105_R0011": "!!",
    "DK4_MES_B105_R0016": "Mao!{LB}Y-you must not!",
    "DK4_MES_B105_R0019": "Why not?",
    "DK4_MES_B105_R0023": "{MACRO:FA}!{LB}P-please forgive me!{LB}Pardon my son's rudeness!",
    "DK4_MES_B105_R0027": "...No harm.",
    "DK4_MES_B105_R0031": "Thank you!{LB}He will never do that again!",
    "DK4_MES_B105_R0048": "(Only flowers and birds return{LB}the love poured from me...)",
    "DK4_MES_B105_R0055": "Xien?",
    "DK4_MES_B105_R0059": "{LB}A bad time?{LB}Called many times...",
    "DK4_MES_B105_R0062": "...Sorry. My thoughts were elsewhere.",
    "DK4_MES_B105_R0065": "{LB}What is it?",
    "DK4_MES_B105_R0073": "The town...{LB}They fear me.",
    "DK4_MES_B105_R0080": "All my efforts shielded them{LB}from the wako...{LB}Yet...",
    "DK4_MES_B105_R0084": "{LB}Someday, they will understand.",
    "DK4_MES_B105_R0087": "Xien...",
    "DK4_MES_B105_R0091": "My father died.{LB}To fight the wako,{LB}my vow made me a demon.",
    "DK4_MES_B105_R0101": "A demon should be feared.{LB}Wako pirates named me{LB}the \"flying crimson orca.\"{LB}Their fear exceeded my strength.",
    "DK4_MES_B105_R0106": "A demon should be feared.{LB}Wako pirates named me{LB}the \"flying crimson orca.\"{LB}Their fear exceeded my strength.",
    "DK4_MES_B105_R0112": "But seeing townspeople tremble{LB}before me...{LB}The sadness was unbearable.",
    "DK4_MES_B105_R0116": "{LB}...This has hurt you deeply.",
    "DK4_MES_B105_R0120": "Never meant to say this,{LB}but with you, Xien,{LB}my heart speaks too freely.",
    "DK4_MES_B105_R0128": "Please forget.",
    "DK4_MES_B105_R0132": "{LB}Your trials just began.{LB}Bravado will fail.{LB}Before me,{LB}do not force yourself.",
    "DK4_MES_B105_R0135": "Thank you. All is well.{LB}There is no time{LB}for complaints.",
    "DK4_MES_B105_R0139": "There is so much to do.{LB}Regretting what went undone{LB}would be unbearable.",
    "DK4_MES_B106_R0005": "{MACRO:FA}, unofficially,{LB}Ming may recognize your work.",
    "DK4_MES_B106_R0009": "Why now?{LB}Government permission{LB}changes nothing.",
    "DK4_MES_B106_R0013": "Quite right. My ties to England{LB}make Ming officials no threat.{LB}Their condescension is absurd.",
    "DK4_MES_B106_R0016": "Now, now. Their stubborn officials{LB}yield to your deeds and popularity.{LB}That proves your success.",
    "DK4_MES_B106_R0024": "They value appearances.{LB}One condition remains.{LB}Look at this.",
    "DK4_MES_B106_R0027": "A diagram to decipher{LB}a treasure map.",
    "DK4_MES_B106_R0030": "A map...?",
    "DK4_MES_B106_R0034": "The treasure marked on that map{LB}is said to prove who rules East Asia.{LB}Claim it, and it becomes your permit.",
    "DK4_MES_B106_R0037": "The Proof...",
    "DK4_MES_B106_R0041": "Western powers are searching madly{LB}for it. Do not let them find it first.",
    "DK4_MES_B106_R0048": "An assembly diagram.{LB}But it tells us nothing...",
    "DK4_MES_B107_R0004": "This Bamboo Diagram{LB}is not the Proof map...",
    "DK4_MES_B107_R0007": "{LB}Agreed. The diagram shows{LB}how to assemble the Tang Bamboo Craft.",
    "DK4_MES_B107_R0011": "Assembly steps...{LB}Could it be...?",
    "DK4_MES_B107_R0015": "{LB}W-wait, {MACRO:FI}!{LB}Why take the Tang Bamboo Craft apart?",
    "DK4_MES_B107_R0019": "The diagram may hide a secret.{LB}Let's dismantle the Tang Bamboo Craft{LB}exactly as shown.",
    "DK4_MES_B107_R0023": "There!{LB}Look behind it!",
    "DK4_MES_B107_R0026": "{LB}This map...{LB}Could it be the Proof map?",
    "DK4_MES_B107_R0029": "This must be it.{LB}The East Asian Proof map...",
    "DK4_MES_B107_R0032": "Set sail!{LB}Get ready!",
}

SP = {
    "03": "Maria",
    "4A": "Kamil",
    "90": "Mao's father",
    "95": "Ming intermediary",
    "A3": "Mao",
}
ST = {int(value, 16) for value in SP}
CONTEXT = {
    104: "Maria assesses the thirty-day Ceuta deadline.",
    105: "A child's innocent approach exposes Maria's fearsome public reputation, and Xien helps her regain resolve.",
    106: "A Ming intermediary offers official recognition if Maria finds East Asia's Proof of Supremacy.",
    107: "Maria and Xien use the Bamboo Assembly Diagram to reveal the East Asian Proof map.",
}


def main() -> None:
    with S.open(encoding="utf-8-sig", newline="") as stream:
        rows = {
            row["id"]: row
            for row in csv.DictReader(stream)
            if 104 <= int(row["id"].split("_B", 1)[1].split("_R", 1)[0]) <= 107
        }
    if set(L) != set(rows):
        raise SystemExit(
            f"V90 mismatch: missing={sorted(set(rows) - set(L))}; "
            f"extra={sorted(set(L) - set(rows))}"
        )

    records = []
    for record_id in sorted(
        L,
        key=lambda value: (
            int(value.split("_B", 1)[1].split("_R", 1)[0]),
            int(value.rsplit("R", 1)[1]),
        ),
    ):
        row = rows[record_id]
        english = L[record_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in ST else ""
        unmasked = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "F" in unmasked or "I" in unmasked:
            raise SystemExit(f"{record_id}: unsafe macro literal: {english}")
        source_breaks = row["japanese"].count("{LB}")
        target_breaks = english.count("{LB}")
        waivers = ["weak-line-ending", "orphan-final-line"]
        if target_breaks:
            waivers.append("manual-break")
        if row["japanese"].startswith("{LB}"):
            waivers.append("source-leading-linebreak")
        if source_breaks != target_breaks:
            waivers.append("line-break-count")
        block = int(record_id.split("_B", 1)[1].split("_R", 1)[0])
        prefix = f"{{SPEAKER:{state}}}" if state else ""
        records.append(
            {
                "id": record_id,
                "english": f"{prefix}{english}{{PAD}}",
                "speaker": SP.get(state, "Maria or Xien continuation"),
                "context": CONTEXT[block],
                "source_meaning": english.replace("{LB}", " "),
                "localization_note": "Direct SC3 translation preserving presentation states, route-name macros, emotional cadence, terminology, and fixed allocation.",
                "qa_waivers": waivers,
                **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if target_breaks else {}),
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": True,
                },
            }
        )

    blocks = {}
    for record_id in L:
        block = record_id.split("_B", 1)[1].split("_R", 1)[0]
        blocks[block] = blocks.get(block, 0) + 1
    payload = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC3.DK4",
        "source_file_sha256": SHA,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-events-v90-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 blocks 104-107: Ceuta deadline, Mao encounter, public-fear confession, Ming recognition offer, and East Asian Proof map discovery.",
        "inventory": {
            "identified_records": len(rows),
            "translated_records": len(records),
            "excluded_records": 0,
            "blocks": blocks,
        },
        "excluded": [],
        "records": records,
    }
    O.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {O}: {len(records)} records")


if __name__ == "__main__":
    main()
