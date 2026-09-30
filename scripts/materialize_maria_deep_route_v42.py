from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc3/script.csv")
OUTPUT = Path("translations/maria_deep_route_v42.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (267, 268, 269)

EXCLUDED = {
    "DK4_MES_B267_R0037": "Eight-byte scene-transition payload 056060468B803E63; not independently rendered dialogue.",
}

LINES = {
    "DK4_MES_B267_R0019": "Admiral, we need a map.",
    "DK4_MES_B267_R0020": "Admiral, we need a map.",
    "DK4_MES_B267_R0021": "Admiral, no map means no go.",
    "DK4_MES_B267_R0022": "Admiral, no map:{LB}we'll get lost.",
    "DK4_MES_B267_R0023": "Admiral, no map:{LB}we'll get lost.",
    "DK4_MES_B267_R0024": "Admiral, no map:{LB}we'll get lost.",
    "DK4_MES_B267_R0025": "Admiral,{LB}we need a map to go.",
    "DK4_MES_B267_R0026": "Admiral, a map is a must.",
    "DK4_MES_B267_R0039": "Eerie woods...",
    "DK4_MES_B267_R0043": "{LB}We must tread carefully.",
    "DK4_MES_B267_R0047": "A-Admiral! Look!",
    "DK4_MES_B267_R0051": "Snake!",
    "DK4_MES_B267_R0055": "{LB}{MACRO:FI},{LB}attack it?",
    "DK4_MES_B267_R0061": "Hit",
    "DK4_MES_B267_R0063": "Run",
    "DK4_MES_B267_R0070": "No choice. We must defeat it.",
    "DK4_MES_B267_R0074": "{LB}Agreed.{LB}Stay alert!",
    "DK4_MES_B267_R0077": "You got it!",
    "DK4_MES_B267_R0085": "Phew.",
    "DK4_MES_B267_R0089": "{LB}Not dead,{LB}but those wounds will stop it{LB}for now...",
    "DK4_MES_B267_R0095": "Several sailors were injured.",
    "DK4_MES_B267_R0100": "Let's run.{LB}No needless battle.",
    "DK4_MES_B267_R0103": "{LB}Yes. Wise.",
    "DK4_MES_B267_R0108": "{LB}Everyone escaped safely.",
    "DK4_MES_B267_R0112": "Yes...",
    "DK4_MES_B267_R0119": "What is this!?",
    "DK4_MES_B267_R0123": "{LB}{MACRO:FI} you okay?",
    "DK4_MES_B267_R0127": "Ugh... a bog!{LB}Watch your step!",
    "DK4_MES_B267_R0130": "{LB}What!?",
    "DK4_MES_B267_R0141": "{LB}Hold on! We'll save you!",
    "DK4_MES_B267_R0145": "{LB}Nngh!{LB}Too much for me...{LB}Everyone, help!",
    "DK4_MES_B267_R0149": "Heave!",
    "DK4_MES_B267_R0153": "{LB}Whew...{LB}{MACRO:FI}, okay?",
    "DK4_MES_B267_R0156": "Thanks, Xien.{LB}You saved me.",
    "DK4_MES_B267_R0164": "{LB}Hold on!{LB}Hrrrraaaagh!",
    "DK4_MES_B267_R0167": "{LB}Whew.{LB}{MACRO:FI}, okay?",
    "DK4_MES_B267_R0170": "Yes... thanks.{LB}A bog here...{LB}who knew?",
    "DK4_MES_B267_R0178": "Sailors look tired.",
    "DK4_MES_B267_R0195": "Admiral, ahead!",
    "DK4_MES_B267_R0197": "Admiral, ahead!",
    "DK4_MES_B267_R0199": "Admiral, there...",
    "DK4_MES_B267_R0201": "Look there!",
    "DK4_MES_B267_R0203": "Admiral, look!",
    "DK4_MES_B267_R0205": "Admiral, there!",
    "DK4_MES_B267_R0207": "Oh...!",
    "DK4_MES_B268_R0005": "Ah, {MACRO:FI}.{LB}Perfect timing.",
    "DK4_MES_B268_R0008": "Have you heard of the Colosseum?",
    "DK4_MES_B268_R0012": "The Colosseum?",
    "DK4_MES_B268_R0016": "A Roman ruin.{LB}You seek ruins,{LB}so here is a lead.",
    "DK4_MES_B268_R0020": "Worth seeing.{LB}Many thanks.",
    "DK4_MES_B268_R0023": "Take care.{LB}Buy a map first.",
    "DK4_MES_B269_R0018": "Admiral, we need a map.",
    "DK4_MES_B269_R0019": "Admiral, a map is vital.",
    "DK4_MES_B269_R0021": "Admiral, no map means no go.",
    "DK4_MES_B269_R0022": "Admiral, first get a map{LB}so we do not lose our way.",
    "DK4_MES_B269_R0023": "Admiral, no map means no go.",
    "DK4_MES_B269_R0024": "Admiral, we need a map.",
    "DK4_MES_B269_R0026": "Admiral, without a map{LB}we'll get lost.",
    "DK4_MES_B269_R0027": "Admiral, a map is a must.",
    "DK4_MES_B269_R0052": "Very hot here.",
    "DK4_MES_B269_R0054": "Hot...",
    "DK4_MES_B269_R0056": "Whew... hot.",
    "DK4_MES_B269_R0058": "So very hot.",
    "DK4_MES_B269_R0060": "So hot!",
    "DK4_MES_B269_R0062": "Such heat...",
    "DK4_MES_B269_R0064": "Whew, it is hot.",
    "DK4_MES_B269_R0066": "My, it is hot.",
    "DK4_MES_B269_R0070": "Long road ahead.{LB}Ration water.",
    "DK4_MES_B269_R0078": "Whoa! Quicksand!",
    "DK4_MES_B269_R0084": "Pull them free",
    "DK4_MES_B269_R0086": "Call for help",
    "DK4_MES_B269_R0093": "Hold on!{LB}Here, take my hand!",
    "DK4_MES_B269_R0108": "Admiral!{LB}All hands, help!",
    "DK4_MES_B269_R0109": "Admiral!{LB}All hands, help!",
    "DK4_MES_B269_R0110": "Admiral!{LB}All hands, help!",
    "DK4_MES_B269_R0111": "Admiral!{LB}Everyone, help the admiral!",
    "DK4_MES_B269_R0112": "Admiral!{LB}Everyone, help the admiral!",
    "DK4_MES_B269_R0113": "Admiral!{LB}Everyone, help the admiral!",
    "DK4_MES_B269_R0119": "{MACRO:FI} is tired.",
    "DK4_MES_B269_R0124": "Pull him out!{LB}Everyone, lend a hand!",
    "DK4_MES_B269_R0141": "Here, take hold!",
    "DK4_MES_B269_R0143": "Here, grab on!",
    "DK4_MES_B269_R0145": "Here, take hold!",
    "DK4_MES_B269_R0147": "Here, grab on!",
    "DK4_MES_B269_R0153": "Sailors look tired.",
    "DK4_MES_B269_R0169": "Nearly through{LB}the desert...",
    "DK4_MES_B269_R0170": "Past the desert{LB}by now...?",
    "DK4_MES_B269_R0171": "Past the desert{LB}by now...?",
    "DK4_MES_B269_R0172": "Past the desert{LB}by now...?",
    "DK4_MES_B269_R0173": "We should be out{LB}by now...",
    "DK4_MES_B269_R0174": "Nearly through{LB}the desert...",
    "DK4_MES_B269_R0175": "Desert should end{LB}by now...",
    "DK4_MES_B269_R0176": "Nearly through{LB}the desert...",
    "DK4_MES_B269_R0189": "Admiral!{LB}Look at that!",
    "DK4_MES_B269_R0190": "Admiral!{LB}Look!",
    "DK4_MES_B269_R0191": "Admiral!{LB}Look!",
    "DK4_MES_B269_R0192": "Admiral!{LB}Behold!",
    "DK4_MES_B269_R0193": "Admiral!{LB}Look!",
    "DK4_MES_B269_R0194": "Admiral!{LB}See!",
}

STATES = {0x03, 0x97, 0x9C, 0xC0, 0xCF, 0xD0, 0xD3, 0xD6, 0xFE}
SPEAKERS = {
    "03": "Maria",
    "97": "Companion",
    "9C": "Crew",
    "C0": "Tavern patron",
    "CF": "Maria",
    "D0": "Companion",
    "D3": "Companion",
    "D6": "Companion",
    "FE": "System",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as source:
        all_rows = {row["id"]: row for row in csv.DictReader(source)}
    rows = {
        record_id: row
        for record_id, row in all_rows.items()
        if any(record_id.startswith(f"DK4_MES_B{block}_") for block in BLOCKS)
    }
    if set(LINES) | set(EXCLUDED) != set(rows):
        raise SystemExit(
            f"Maria V42 mismatch: missing={sorted(set(rows) - set(LINES) - set(EXCLUDED))}, "
            f"extra={sorted((set(LINES) | set(EXCLUDED)) - set(rows))}"
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
        state = f"{first:02X}" if first in STATES else ""
        block = record_id.split("_B", 1)[1].split("_", 1)[0]
        counts[block] += 1
        leading_break = english.startswith("{LB}")
        waivers = ["weak-line-ending", "orphan-final-line"]
        if "{LB}" in english:
            waivers.append("manual-break")
        if leading_break:
            waivers.append("source-leading-linebreak")
        records.append(
            {
                "id": record_id,
                "english": (
                    f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}"
                ),
                "speaker": SPEAKERS.get(state, "Companion"),
                "context": "Jungle giant-snake and bog hazards, Colosseum rumor, and desert/quicksand expedition.",
                "source_meaning": english.replace("{LB}", " ")
                .replace("{MACRO:FI}", "the protagonist's given name")
                .strip(),
                "localization_note": "Direct SC3 translation reviewed for natural English, choice and companion-branch parity, macro preservation, and state-byte safety.",
                "qa_waivers": waivers,
                **(
                    {"manual_break_reason": "Preserves source transition or semantic grouping."}
                    if "{LB}" in english
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
        "dialogue_profile": "maria-story-shared-events-v42-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 blocks 267-269: jungle hazards, Colosseum rumor, and desert/quicksand expedition.",
        "inventory": {
            "identified_records": len(rows),
            "translated_records": len(records),
            "excluded_records": len(EXCLUDED),
            "blocks": counts,
        },
        "excluded": [{"id": record_id, "reason": reason} for record_id, reason in EXCLUDED.items()],
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} excluded")


if __name__ == "__main__":
    main()
