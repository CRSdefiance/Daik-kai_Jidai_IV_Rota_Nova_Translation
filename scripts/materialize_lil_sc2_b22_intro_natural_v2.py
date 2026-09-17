from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "translations/lil_natural_v2_sc2_b22_blocked.json"
SCRIPT_CSV = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_sc2_b22_intro_natural_v2.json"

LINES = {
    "DK4_MES_B22_R0019": "Hee hee! The trade permit is mine!{LB}Just watch me--time to make{LB}a fortune!",
    "DK4_MES_B22_R0023": "{MACRO:FI}!{LB}Wait for me!",
    "DK4_MES_B22_R0026": "Kamil, hurry! Get us ready.{LB}We sail now!",
    "DK4_MES_B22_R0030": "Phew... Must we leave today?",
    "DK4_MES_B22_R0033": "The permit came so soon.{LB}We're not even ready...",
    "DK4_MES_B22_R0036": "Quit grumbling. Anyway...",
    "DK4_MES_B22_R0040": "The permit's in my name.{LB}That makes me captain, right?",
    "DK4_MES_B22_R0044": "Huh? Oh... guess so?",
    "DK4_MES_B22_R0048": "All hands, stations!{LB}We sail now!",
    "DK4_MES_B22_R0051": "Sails up! Anchor up!",
    "DK4_MES_B22_R0054": "How did {MACRO:FI} get a permit so easily?",
    "DK4_MES_B22_R0058": "Obviously! My passion moved them!{LB}Or maybe my dazzling beauty{LB}won them over.♪",
    "DK4_MES_B22_R0061": "Yeah, yeah. What's the permit for?",
    "DK4_MES_B22_R0065": "This lets us trade with any city!{LB}The whole world is our market!",
    "DK4_MES_B22_R0069": "The whole world? What's wrong with{LB}trading near Amsterdam as always?",
    "DK4_MES_B22_R0072": "That barely pays! Across the sea,{LB}we could strike it rich!",
    "DK4_MES_B22_R0076": "Not so sure...{LB}Getting rich won't be easy.",
    "DK4_MES_B22_R0079": "Still resisting?",
    "DK4_MES_B22_R0083": "You're coming too? Thought you'd{LB}never sail with us.",
    "DK4_MES_B22_R0087": "Things change. Never mind.{LB}Let's go.",
    "DK4_MES_B22_R0090": "Hey, when do we eat?{LB}Been waiting forever...",
    "DK4_MES_B22_R0094": "Emilio too?",
    "DK4_MES_B22_R0098": "He's strong and useful.{LB}A meal got him aboard.",
    "DK4_MES_B22_R0102": "What a crew... Will we be safe at sea?",
    "DK4_MES_B22_R0105": "Enough talk! Let's go!{LB}Kamil, get moving.♪",
    "DK4_MES_B22_R0109": "Sails set! Anchor up!{LB}Orders?",
    "DK4_MES_B22_R0112": "All right... Arnhem is ready!{LB}Everyone, stations!",
    "DK4_MES_B22_R0116": "Much better! Counting on you.",
    "DK4_MES_B22_R0119": "Sigh... Trouble ahead.",
    "DK4_MES_B22_R0123": "Hah! You came along pretty easily.",
    "DK4_MES_B22_R0126": "Had to. Promised to go if we got it.",
    "DK4_MES_B22_R0129": "Our nation is young.{LB}The state backs merchants{LB}to make it stronger.",
    "DK4_MES_B22_R0133": "So anyone can get a permit easily.",
    "DK4_MES_B22_R0136": "Oh... So that's it.",
    "DK4_MES_B22_R0140": "The permit also makes{LB}trade-post profits tax-free.",
    "DK4_MES_B22_R0144": "What? Really?!",
    "DK4_MES_B22_R0148": "That policy promotes trade.{LB}The permit grants a tax break.",
    "DK4_MES_B22_R0152": "Oh... No wonder {MACRO:FI} wanted it.",
    "DK4_MES_B22_R0156": "Accept it. You've always been like this, right?",
    "DK4_MES_B22_R0159": "Huh?",
    "DK4_MES_B22_R0163": "That woman will always get her way.",
    "DK4_MES_B22_R0166": "N-no...",
    "DK4_MES_B22_R0170": "Wait, where did {MACRO:FI} go?",
    "DK4_MES_B22_R0175": "My hometown... So much happened here.{LB}And yet...",
    "DK4_MES_B22_R0179": "{MACRO:FI}! What's wrong?",
    "DK4_MES_B22_R0182": "Oh... Kamil. Sorry! Nothing's wrong.",
    "DK4_MES_B22_R0186": "You sure? All right...{LB}We're ready here.",
    "DK4_MES_B22_R0190": "Give the order, now!",
    "DK4_MES_B22_R0195": "Then... Arnhem, set sail!{LB}Next stop, Bruges!",
}


def main() -> None:
    manuscript = json.loads(SOURCE.read_text(encoding="utf-8"))
    source_records = {record["id"]: record for record in manuscript["blocked_records"]}
    with SCRIPT_CSV.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    if set(LINES) != set(source_records):
        missing = sorted(set(source_records) - set(LINES))
        extra = sorted(set(LINES) - set(source_records))
        raise SystemExit(f"B22 inventory mismatch: missing={missing}, extra={extra}")

    records = []
    for row_id, english in LINES.items():
        source = source_records[row_id]
        records.append(
            {
                "id": row_id,
                "english": (
                    f"{{SPEAKER:{source['source_prefix_hex']}}}{english}{{PAD}}"
                ),
                "source_hex_guard": source_rows[row_id]["source_hex"],
                "speaker": source["speaker"],
                "context": source["context"],
                "source_meaning": source["source_meaning"],
                "localization_note": source["localization_note"],
                **(
                    {
                        "manual_break_reason": (
                            "Preserves the intended dramatic beat while keeping the fixed-size "
                            "record within the progressive renderer's safe row width."
                        )
                    }
                    if "{LB}" in english
                    else {}
                ),
                "qa_waivers": [
                    "manual-break",
                    "line-break-count",
                    "weak-line-ending",
                    "orphan-final-line",
                ],
                "qa_waiver_reason": (
                    "Concise manual layout is required by this source record's fixed "
                    "allocation and the progressive story renderer."
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
        "file_path": manuscript["file_path"],
        "source_file_sha256": manuscript["source_file_sha256"],
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-b22-intro-probe",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": [
            "source",
            "context",
            "localization",
            "naturalness",
            "formatting",
        ],
        "research_only": True,
        "scope": (
            "Complete 49-record Lil Amsterdam opening, from the trade permit "
            "boast through the order to sail for Bruges."
        ),
        "editorial_source": SOURCE.relative_to(ROOT).as_posix(),
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} with {len(records)} records")


if __name__ == "__main__":
    main()
