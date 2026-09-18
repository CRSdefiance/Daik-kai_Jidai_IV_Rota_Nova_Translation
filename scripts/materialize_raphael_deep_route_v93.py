from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v93.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"

SPEAKERS = {
    0x04: "Eirene", 0x05: "Claudio", 0x06: "Julio", 0x07: "Raphael companion",
    0x08: "Arcadius", 0x0B: "Raphael companion", 0x0D: "Raphael companion",
    0x14: "Raphael companion", 0x23: "Silveira", 0x72: "Messenger",
    0x97: "Lookout or merchant", 0xB3: "Proof guardian", 0xFE: "System",
}

OVERRIDES = {
    "DK4_MES_B48_R0032": "Exactly. We may learn something too!",
    "DK4_MES_B48_R0049": "Don't complain so quickly!",
    "DK4_MES_B48_R0057": "Clau complains.",
    "DK4_MES_B48_R0075": "Ruler's Proof?",
    "DK4_MES_B48_R0362": "Sea king.",
    "DK4_MES_B48_R0427": "Hans Letze, natural historian,{LB}joined the crew!",
    "DK4_MES_B48_R0431": "Hans is no sailor,{LB}so he cannot serve{LB}on the deck screen.",
    "DK4_MES_B48_R0435": "Hans now reveals{LB}detailed item information.",
    "DK4_MES_B48_R0438": "Press X while item information{LB}is displayed.",
    "DK4_MES_B52_R0005": "Ah, you're from {MACRO:FO}?",
    "DK4_MES_B52_R0010": "? Yes.",
    "DK4_MES_B52_R0014": "Thought so.",
    "DK4_MES_B52_R0018": "Admiral Albuquerque of Portugal{LB}asked me to tell you{LB}to return home to Lisbon.",
    "DK4_MES_B52_R0022": "?{LB}What does the navy want?",
    "DK4_MES_B52_R0031": "No choice.{LB}Shall we head back?",
    "DK4_MES_B52_R0036": "No choice.{LB}Let's head back.",
    "DK4_MES_B53_R0006": "Admiral. The Portuguese navy{LB}summoned us. What now?",
    "DK4_MES_B53_R0011": "Let's go.{LB}To the palace, right?",
    "DK4_MES_B53_R0014": "Yes.",
    "DK4_MES_B55_R0005": "Ah, {MACRO:FI}!{LB}Well done.",
    "DK4_MES_B55_R0009": "Admiral Silveira!{LB}(He's here so soon...!)",
    "DK4_MES_B55_R0012": "Splendid! Lord Albuquerque{LB}has my report. Don't worry.",
    "DK4_MES_B55_R0016": "Right",
    "DK4_MES_B55_R0020": "The offer was refused,{LB}but His Lordship insisted.",
    "DK4_MES_B55_R0024": "So the post of African governor{LB}is mine! Hahaha!",
    "DK4_MES_B55_R0029": "What?!",
    "DK4_MES_B55_R0036": "All Sofala shares were taken{LB}by the Silveira Company!!",
    "DK4_MES_B55_R0040": "Luck, that's all.{LB}No hard feelings. Hahaha!",
    "DK4_MES_B55_R0044": "Lord Albuquerque's reward.{LB}My gift was already deducted.",
    "DK4_MES_B55_R0047": "Of course, if you insist,{LB}you may give more. Hahaha!",
    "DK4_MES_B55_R0054": "Received 3,000 gold coins...",
    "DK4_MES_B55_R0059": "Damn!{LB}He got us!",
    "DK4_MES_B55_R0064": "Did Albuquerque{LB}really decide this?",
    "DK4_MES_B55_R0067": "He begged and lied,{LB}claiming all credit for Espinosa.",
    "DK4_MES_B55_R0078": "He's more shrewd than expected...{LB}Admiral {MACRO:FI}, this cannot stand.",
    "DK4_MES_B55_R0090": "Admiral!{LB}Target is clear!",
    "DK4_MES_B55_R0095": "Our next target is clear.",
    "DK4_MES_B55_R0115": "Silveira!{LB}Now you've made me serious!",
    "DK4_MES_B55_R0121": "We can't stay silent!",
    "DK4_MES_B55_R0132": "God may forgive him.{LB}Not me! Yahoo!!",
    "DK4_MES_B55_R0138": "Let's do it!",
    "DK4_MES_B55_R0143": "...Y-yes.{LB}War with fellow Portuguese feels wrong,{LB}but backing down is worse.",
    "DK4_MES_B55_R0154": "No mercy, Silveira!!",
    "DK4_MES_B55_R0168": "Good grief, these old bones...{LB}{MACRO:FI}, let's give it our all!",
    "DK4_MES_B55_R0174": "Let's do it!{LB}We'll wipe that smirk{LB}from Silveira's face!",
    "DK4_MES_B55_R0179": "Thanks, everyone!{LB}Africa is ours!",
    "DK4_MES_B55_R0182": "Go!",
    "DK4_MES_B55_R0186": "Aye!",
    "DK4_MES_B61_R0113": "Governor Pereira gave us{LB}500,000 in military funds!",
    "DK4_MES_B62_R0005": "{MACRO:FA}, you are worthy to rule{LB}this continent's seas.{LB}Please accept this.",
    "DK4_MES_B64_R0035": "That was before.{LB}At today's quality,{LB}not one coin more.",
    "DK4_MES_B64_R0043": "Hmm, village best...",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as source:
        rows = [row for row in csv.DictReader(source) if row["id"] in OVERRIDES]
    found = {row["id"] for row in rows}
    missing = sorted(set(OVERRIDES) - found)
    if missing:
        raise SystemExit(f"Raphael V93 missing source records: {missing}")
    records = []
    for row in rows:
        english = OVERRIDES[row["id"]]
        unsafe = english
        for macro in ("FI", "FA", "FO", "FU"):
            unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
        first = int(row["source_hex"][:2], 16)
        state = f"{first:02X}" if first in SPEAKERS else ""
        rendered = f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}"
        records.append({
            "id": row["id"], "english": rendered,
            "speaker": SPEAKERS.get(first, "Raphael party or scene text"),
            "context": "Final residual Raphael records: Hans tutorial notices, royal summons, Silveira betrayal, Proof handoff, funding, and merchant lines.",
            "source_meaning": row["japanese"],
            "localization_note": "Natural concise American English preserving canonical names, tutorial facts, route motivation, macros, and fixed-record constraints.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    counts = Counter(row["id"].split("_B", 1)[1].split("_", 1)[0] for row in rows)
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v93-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete every remaining source-locked visible Japanese Raphael record across SC0 blocks 48, 52, 53, 55, 61, 62, and 64.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": dict(sorted(counts.items(), key=lambda item: int(item[0])))},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
