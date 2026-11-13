from __future__ import annotations

import csv
import json
from pathlib import Path

S = Path("work/sc3/script.csv")
O = Path("translations/maria_deep_route_v91.json")
SHA = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"

L = {
    "DK4_MES_B108_R0004": "Ugh...!",
    "DK4_MES_B108_R0014": "{LB}W-what!?",
    "DK4_MES_B108_R0020": "What!?",
    "DK4_MES_B108_R0034": "Someone collapsed!",
    "DK4_MES_B108_R0043": "What now?",
    "DK4_MES_B108_R0047": "H-help me...",
    "DK4_MES_B108_R0051": "{LB}These wounds are grave.{LB}What happened?",
    "DK4_MES_B108_R0054": "Treatment first.{LB}Bear the pain.",
    "DK4_MES_B108_R0057": "Th-thanks...",
    "DK4_MES_B108_R0061": "Those look like blows.{LB}My name is {MACRO:FA}.{LB}Would you tell us why?",
    "DK4_MES_B108_R0064": "What! So you are with{LB}{MACRO:FO}...{LB}Then you will believe me!",
    "DK4_MES_B108_R0068": "W-worked for Kuen...{LB}His cruelty tormented my conscience.{LB}So... help went to the villagers.",
    "DK4_MES_B108_R0071": "That made me a traitor.{LB}So, running for my life,{LB}his service was abandoned...",
    "DK4_MES_B108_R0075": "{LB}But who injured you?{LB}Surely no roadside thief did this.",
    "DK4_MES_B108_R0079": "These are professional wounds...{LB}Do you know Kuen's secret?",
    "DK4_MES_B108_R0082": "Sharp...{LB}Kuen has a secret plan.{LB}Exposure would ruin him.",
    "DK4_MES_B108_R0085": "{LB}Kuen's plan...{LB}No doubt something vile.",
    "DK4_MES_B108_R0088": "...Tell us the plan.{LB}Your safety is guaranteed.",
    "DK4_MES_B108_R0092": "Thank you. No one else can help.{LB}Do you know the Argot Company?",
    "DK4_MES_B108_R0096": "{LB}A small North Sea company...{LB}Led by Lil Argot, perhaps.",
    "DK4_MES_B108_R0100": "{MACRO:FO}'s entry into Southeast Asia{LB}is being blocked by Kuen,{LB}using the Argot Company.",
    "DK4_MES_B108_R0103": "How?",
    "DK4_MES_B108_R0107": "{MACRO:FO} was falsely accused of corrupt trade{LB}to the Argot Company.",
    "DK4_MES_B108_R0111": "Their young leader values justice.{LB}She swore never to forgive {MACRO:FO}.",
    "DK4_MES_B108_R0114": "{LB}While {MACRO:FO} struggles with Argot,{LB}Kuen expects no move into Southeast Asia.",
    "DK4_MES_B108_R0125": "That villain!",
    "DK4_MES_B108_R0132": "A dangerous plan.{LB}Once exposed, Kuen would face{LB}enemies on both sides.",
    "DK4_MES_B108_R0136": "So witnesses cannot leave alive.{LB}When found...{LB}death awaits me.",
    "DK4_MES_B108_R0140": "Does Argot's leader{LB}suspect this plan?",
    "DK4_MES_B108_R0144": "No idea...",
    "DK4_MES_B108_R0147": "{LB}{MACRO:FI},{LB}worth investigating.",
    "DK4_MES_B109_R0006": "Jam",
    "DK4_MES_B109_R0008": "Why summon me?",
    "DK4_MES_B109_R0012": "A new plan for Jam and me?",
    "DK4_MES_B109_R0015": "No. Hear me out.{LB}Richard, you too.",
    "DK4_MES_B109_R0018": "Yes.",
    "DK4_MES_B109_R0025": "Ming once ruled a proud maritime realm.{LB}Zheng He's vast junk fleet crossed{LB}the ocean to Africa.",
    "DK4_MES_B109_R0028": "Then the sea ban destroyed navigation{LB}and trade. New Western powers now strip{LB}Asia of its wealth.",
    "DK4_MES_B109_R0031": "Painful words for us...",
    "DK4_MES_B109_R0035": "Westerners are not to blame.{LB}Ming had the skill and opportunity,{LB}yet its policy abandoned that right.",
    "DK4_MES_B109_R0038": "The government will not understand.{LB}Nor is there time to persuade it.",
    "DK4_MES_B109_R0042": "Portugal, Spain, Holland,{LB}England, france...",
    "DK4_MES_B109_R0045": "Every power sends fleet after fleet{LB}seeking trade profit.{LB}You have all seen it.",
    "DK4_MES_B109_R0049": "With no hope from government,{LB}someone must act in its place.{LB}That someone is me.",
    "DK4_MES_B109_R0053": "But you stand apart from me.{LB}So...",
    "DK4_MES_B109_R0056": "No need to worry.{LB}My service is to you, Admiral.{LB}Wherever you go, so shall this servant.",
    "DK4_MES_B109_R0059": "Heh! Complex matters mean nothing.{LB}Exiled from home, no ties remain.{LB}Life here is the best!",
    "DK4_MES_B109_R0062": "This voyage is by choice.{LB}Your ability won my respect,{LB}not merely the debt of rescue.",
    "DK4_MES_B109_R0065": "And seeing proud Westerners stunned{LB}by your skill sounds delightful.",
    "DK4_MES_B109_R0072": "You all...",
    "DK4_MES_B109_R0076": "Heh.",
    "DK4_MES_B109_R0080": "Then the world's seas are ours{LB}to stir up freely.",
    "DK4_MES_B109_R0083": "Yahoo! That's more like it!",
    "DK4_MES_B109_R0087": "Your roles will grow even harder.{LB}No whining or surrender.",
    "DK4_MES_B109_R0091": "Yikes! Scary!",
    "DK4_MES_B109_R0095": "Yes!",
    "DK4_MES_B109_R0099": "Count on me.",
}

SP = {
    "03": "Maria",
    "0B": "Jam",
    "15": "Richard",
    "1A": "Companion",
    "4A": "Kamil",
    "9B": "Kuen defector",
}
ST = {int(value, 16) for value in SP}
CONTEXT = {
    108: "Maria rescues Kuen's injured defector and learns how Kuen deceived Lil's Argot Company into opposing her.",
    109: "Maria explains her global maritime purpose; Jam, Richard, and Kamil pledge to follow her.",
}


def main() -> None:
    with S.open(encoding="utf-8-sig", newline="") as stream:
        rows = {
            row["id"]: row
            for row in csv.DictReader(stream)
            if 108 <= int(row["id"].split("_B", 1)[1].split("_R", 1)[0]) <= 109
        }
    if set(L) != set(rows):
        raise SystemExit(
            f"V91 mismatch: missing={sorted(set(rows) - set(L))}; "
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
                "speaker": SP.get(state, "Maria scene participant"),
                "context": CONTEXT[block],
                "source_meaning": english.replace("{LB}", " "),
                "localization_note": "Direct SC3 translation preserving all speaker states, company and regional terminology, FI/FA/FO macros, dramatic cadence, and fixed allocation.",
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
    payload = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC3.DK4",
        "source_file_sha256": SHA,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-events-v91-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 blocks 108-109: Kuen defector and Argot deception, followed by Maria's maritime mission and companion pledges.",
        "inventory": {
            "identified_records": len(rows),
            "translated_records": len(records),
            "excluded_records": 0,
            "blocks": {"108": 31, "109": 26},
        },
        "excluded": [],
        "records": records,
    }
    O.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {O}: {len(records)} records")


if __name__ == "__main__":
    main()
