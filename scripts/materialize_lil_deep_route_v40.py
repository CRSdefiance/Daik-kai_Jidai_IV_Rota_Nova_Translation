from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v40.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    6: ("So this is the Bruges trading post. There are so many things I've never seen. What's that?", "So this is Bruges' trading post! So many new things... What's that?"),
    10: ("Put that aside. Since we've come to the trading post, let's learn about trading.", "Never mind that. Since we're here, let's learn how trading works."),
    16: ("How do you trade?", "How do we trade?"),
    18: ("I know how to trade already.", "Already know how."),
    28: ("Really...?", "...Really?"),
    32: ("What?", "Hey!"),
    36: ("Wow... Maybe she'll become a surprisingly great admiral.", "(Wow... She may be a great admiral.)"),
    46: ("Again? Not another lesson...", "Again? Seriously?"),
    50: ("FI, you're the admiral after all...", "Admiral {MACRO:FI}..."),
    53: ("Oh, Kamil, you sound like my mother. All right, I understand.", "Kamil, you sound like my mother! Okay, okay!"),
    57: ("Buy trade goods cheaply and sell them for a high price. That's the basic rule. At first you can't handle many kinds of goods...", "Buy low, sell high. That's trading. Start with a few kinds of goods."),
    61: ("Think of the quantity filling one cargo hold as one unit of goods for trading. More holds let you buy more goods.", "Treat a full cargo hold as one unit of goods. More holds mean you can buy more."),
    64: ("Even when you have empty holds, a town might not sell you goods. That depends on your share in the town.", "Even with empty holds, a town might not sell you goods. Your market share affects that."),
    67: ("Share means how much you can trade with a town. A higher share lets you buy more at one time.", "Market share is how much you can trade with a town. Higher share lets you buy more at once."),
    70: ("Whew... Making money is really hard...", "Whew... Making money sure is hard."),
}
SPEAKERS = {0x02: "Lil Argot", 0x09: "Kamil"}
TEXT_LEADS = {0x8C}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B126_")}
    if {f"DK4_MES_B126_R{number:04d}" for number in LINES} != expected:
        raise ValueError("B126 coverage does not match clean source")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B126_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS and lead not in TEXT_LEADS:
            raise ValueError(f"{row_id}: unmapped presentation lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": (f"{{SPEAKER:{lead:02X}}}" if lead in SPEAKERS else "") + english + "{PAD}",
            "speaker": SPEAKERS.get(lead, "Lil response choice"),
            "context": "Lil's Bruges trading-post tutorial: Kamil explains buying, selling, cargo-hold units and market share after either response choice.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Localized from clean Japanese with the complete lesson and both choices reviewed. "
                "Preserves Bruges, trading mechanics, the FI runtime name macro and the source 02/09 speaker states. "
                "8C choice starts are visible text, not a speaker command; guarded automatic wrapping protects every opening glyph."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v34-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 15 B126 Bruges trading-post tutorial and response-choice records.",
        "inventory": {"identified_records": 15, "translated_records": len(records), "blocks": {"126": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
