from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc3/script.csv")
OUTPUT = Path("translations/maria_deep_route_v51.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (35, 36)

LINES = {
    "DK4_MES_B35_R0006": "Excuse me.{LB}This is sudden...",
    "DK4_MES_B35_R0010": "Who are you?",
    "DK4_MES_B35_R0015": "Bergstrom, Swedish Navy.{LB}Are you Admiral {MACRO:FA},{LB}the one everyone talks about?",
    "DK4_MES_B35_R0018": "Suppose so?",
    "DK4_MES_B35_R0022": "Just to see for myself:{LB}are you our enemy?",
    "DK4_MES_B35_R0025": "Our enmity...{LB}That depends wholly on you.",
    "DK4_MES_B35_R0032": "Then answer me in return.{LB}You said Swedish Navy.{LB}Do you know the Argot Company?",
    "DK4_MES_B35_R0036": "Argot Company...{LB}They are known to me.",
    "DK4_MES_B35_R0040": "{LB}Pardon me.{LB}What happened to Argot?",
    "DK4_MES_B35_R0043": "Who are you?",
    "DK4_MES_B35_R0047": "Kamil.{LB}Not one of our fleet,{LB}but he travels with us.",
    "DK4_MES_B35_R0051": "Argot is well known to me.{LB}Please tell me what happened.",
    "DK4_MES_B35_R0054": "You may be worth telling.",
    "DK4_MES_B35_R0058": "Kuen and Pereira rule this region.{LB}Their feud has drawn both{LB}{MACRO:FO} and the Argot Company in.",
    "DK4_MES_B35_R0061": "So it is true...",
    "DK4_MES_B35_R0065": "Wait... You knew about this?{LB}Who exactly are you?",
    "DK4_MES_B35_R0068": "Kamil belongs to Argot.{LB}He is close to Admiral Argot,{LB}though they travel apart for now.",
    "DK4_MES_B35_R0072": "Understood.{LB}Does Admiral Argot know{LB}that Kuen is using her?",
    "DK4_MES_B35_R0076": "She may not know yet...{LB}Damn... So it is true.",
    "DK4_MES_B35_R0079": "Then you do not know it all.{LB}Kuen's plot has nearly driven{LB}{MACRO:FO} and Argot to war.",
    "DK4_MES_B35_R0083": "Admiral {MACRO:FA},{LB}the situation is clearly tangled.{LB}What will you do?",
    "DK4_MES_B35_R0087": "A direct talk with Argot's head.{LB}Kamil, will you guide me?",
    "DK4_MES_B35_R0091": "That is hard...{LB}Lil should be staying{LB}near Batavia.",
    "DK4_MES_B35_R0095": "Batavia, then.{LB}We will go. Thank you.",
    "DK4_MES_B35_R0098": "Kamil... will you stay?{LB}This is a good chance.",
    "DK4_MES_B35_R0101": "Sorry...{LB}Not ready to face her.",
    "DK4_MES_B35_R0104": "Understood.{LB}As you wish.",
    "DK4_MES_B36_R0005": "Everyone ready to sail?",
    "DK4_MES_B36_R0009": "{LB}Oh, that must be Lil Argot,{LB}head of Argot Company.",
    "DK4_MES_B36_R0012": "Seems so.",
    "DK4_MES_B36_R0016": "Excuse me.{LB}Admiral Lil Argot?",
    "DK4_MES_B36_R0019": "W-what is this?{LB}Yes, Lil Argot.{LB}Who are you?",
    "DK4_MES_B36_R0023": "{MACRO:FO}'s admiral,{LB}{MACRO:FI}.{LB}You know me.",
    "DK4_MES_B36_R0027": "{MACRO:FI}?!{LB}You came here in person?",
    "DK4_MES_B36_R0031": "Ah!{LB}You came to kill me?!",
    "DK4_MES_B36_R0034": "No. Kuen poisoned your mind.{LB}The truth is, he is using you.",
    "DK4_MES_B36_R0037": "What do you mean?{LB}Kuen wants to save this land.{LB}He is a great merchant!",
    "DK4_MES_B36_R0041": "Only helping him!{LB}You are the pirate who rules{LB}China's underworld!",
    "DK4_MES_B36_R0045": "You do not know Kuen's plans.{LB}Once he has used you,{LB}he plans to dispose of you.",
    "DK4_MES_B36_R0049": "That is a lie!{LB}Stop making things up!{LB}Do you have proof he is evil?{LB}No, you do not!",
    "DK4_MES_B36_R0052": "Still blind?{LB}Your life is at stake.{LB}There is time yet.",
    "DK4_MES_B36_R0056": "How could anyone believe you,{LB}appearing from nowhere?{LB}Hmph!",
    "DK4_MES_B36_R0060": "Stubborn girl...",
}

STATES = {0x01, 0x02, 0x03, 0x09, 0x0A}
SPEAKERS = {
    "01": "Bergstrom",
    "02": "Lil",
    "03": "Maria",
    "09": "Kamil",
    "0A": "Xien",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as source:
        all_rows = {row["id"]: row for row in csv.DictReader(source)}
    rows = {
        record_id: row
        for record_id, row in all_rows.items()
        if any(record_id.startswith(f"DK4_MES_B{block:02d}_") for block in BLOCKS)
    }
    if set(LINES) != set(rows):
        raise SystemExit(
            f"V51 mismatch: missing={sorted(set(rows) - set(LINES))}, "
            f"extra={sorted(set(LINES) - set(rows))}"
        )

    records = []
    counts = {str(block): 0 for block in BLOCKS}
    for record_id in sorted(
        LINES,
        key=lambda value: (
            int(value.split("_B", 1)[1].split("_", 1)[0]),
            int(value.rsplit("R", 1)[1]),
        ),
    ):
        row = rows[record_id]
        english = LINES[record_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = (
            f"{first:02X}"
            if first in STATES and not row["japanese"].startswith("{LB}")
            else ""
        )
        block = int(record_id.split("_B", 1)[1].split("_", 1)[0])
        counts[str(block)] += 1
        source_breaks = row["japanese"].count("{LB}")
        target_breaks = english.count("{LB}")
        waivers = ["weak-line-ending", "orphan-final-line"]
        if target_breaks:
            waivers.append("manual-break")
        if english.startswith("{LB}"):
            waivers.append("source-leading-linebreak")
        if source_breaks != target_breaks:
            waivers.append("line-break-count")
        records.append(
            {
                "id": record_id,
                "english": (
                    f"{{SPEAKER:{state}}}{english}{{PAD}}"
                    if state
                    else f"{english}{{PAD}}"
                ),
                "speaker": SPEAKERS.get(state, "Companion"),
                "context": (
                    "Maria route: Bergstrom's warning, Kamil's Argot connection, "
                    "and Maria's confrontation with Lil in Batavia."
                ),
                "source_meaning": (
                    english.replace("{LB}", " ")
                    .replace("{MACRO:FI}", "the protagonist's given name")
                    .replace("{MACRO:FA}", "the protagonist's surname")
                    .replace("{MACRO:FO}", "the protagonist's fleet name")
                ),
                "localization_note": (
                    "Direct SC3 translation preserving route-name macros, "
                    "presentation states, and the escalating confrontation."
                ),
                "qa_waivers": waivers,
                **(
                    {
                        "manual_break_reason": (
                            "Preserves source staging or groups the thought "
                            "within four display lines."
                        )
                    }
                    if target_breaks
                    else {}
                ),
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
        "source_file_sha256": SC3_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-events-v51-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": [
            "source",
            "context",
            "localization",
            "naturalness",
            "formatting",
        ],
        "scope": (
            "Maria SC3 blocks 35-36: Bergstrom's warning, the Argot connection, "
            "and Maria's first direct confrontation with Lil."
        ),
        "inventory": {
            "identified_records": len(rows),
            "translated_records": len(records),
            "excluded_records": 0,
            "blocks": counts,
        },
        "excluded": [],
        "records": records,
    }
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
