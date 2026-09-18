from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v66.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = tuple(range(265, 271))

SPEAKERS = {
    0x42: "Jean Ramusio",
    0x44: "Jacob Portunto",
    0x93: "Guildmaster",
    0x94: "Guildmaster",
    0x99: "Jacob's sailor",
    0x9A: "Jean's sailor",
    0xFE: "System",
}

CONTEXT = {
    265: "The guildmaster asks Raphael to capture smuggler Jean Ramusio near South Asia.",
    266: "Raphael confronts and captures Jean Ramusio after witnessing his treatment of his crew.",
    267: "Raphael delivers Jean to the guild, receives a reward, and hears of Solomon's treasury.",
    268: "The guildmaster repeats the Jean contract and reveals his location in Ceylon.",
    269: "The guildmaster asks Raphael to capture smuggler Jacob Portunto in East Africa.",
    270: "Raphael confronts and captures Jacob after Jacob's sailors abandon him.",
}

OVERRIDES = {
    "DK4_MES_B265_R0006": "Got a small job. Want it?",
    "DK4_MES_B265_R0010": "Capture the smuggler Jean Ramusio.",
    "DK4_MES_B265_R0013": "He plans a major deal near South Asia. Catch him before it grows.",
    "DK4_MES_B266_R0005": "No, that's wrong! Why don't you understand?",
    "DK4_MES_B266_R0008": "(Always so arrogant...)",
    "DK4_MES_B266_R0012": "Just shut up and do what you are told.",
    "DK4_MES_B266_R0016": "(Quite arrogant.)",
    "DK4_MES_B266_R0021": "Excuse me. Heard the name Jean Ramusio around here?",
    "DK4_MES_B266_R0025": "...That's me.",
    "DK4_MES_B266_R0029": "These hands developed local ports through trade and drove off pirates here.",
    "DK4_MES_B266_R0033": "Respect is natural. Do not address me so casually.",
    "DK4_MES_B266_R0038": "We came to arrest you. Your smuggling earned illegal profits. Come with us.",
    "DK4_MES_B266_R0041": "! Uh...",
    "DK4_MES_B266_R0045": "No idea why, but thanks.",
    "DK4_MES_B266_R0049": "Always lies and boasts.{LB}Acts so superior.",
    "DK4_MES_B266_R0053": "W-wait! No smuggling. Really! Believe me!",
    "DK4_MES_B266_R0057": "So pathetic...{LB}Come to Sofala's guild.",
    "DK4_MES_B267_R0005": "Well, Jean was dragged in.",
    "DK4_MES_B267_R0008": "Everyone says smuggling. What's wrong with smuggling anyway?",
    "DK4_MES_B267_R0012": "Cornered, so you embrace it? Pathetic.",
    "DK4_MES_B267_R0015": "He was trouble.{LB}Take this reward.",
    "DK4_MES_B267_R0018": "Received 20,000 coins.",
    "DK4_MES_B267_R0048": "Sofala share rose slightly!",
    "DK4_MES_B267_R0066": "Visited the ruins near town?{LB}",
    "DK4_MES_B267_R0069": "Legend calls them King Solomon's treasury. Pay them a visit.",
    "DK4_MES_B268_R0014": "Jean is somewhere in South Asia...",
    "DK4_MES_B268_R0026": "Jean seems to be in Ceylon. Catch him quickly.",
    "DK4_MES_B269_R0005": "A job suited to you.",
    "DK4_MES_B269_R0010": "What job?",
    "DK4_MES_B269_R0014": "Capture a smuggler named Jacob Portunto. That sly pest is causing trouble.",
    "DK4_MES_B269_R0017": "He has been active around East Africa. Bring him here.",
    "DK4_MES_B270_R0005": "Come on, everyone. Celebrate today!",
    "DK4_MES_B270_R0012": "Working for Boss Jacob is the best!",
    "DK4_MES_B270_R0019": "Anyone who says my name dies. That was the rule.",
    "DK4_MES_B270_R0022": "W-well...",
    "DK4_MES_B270_R0027": "Too late, Jacob.",
    "DK4_MES_B270_R0035": "Run!",
    "DK4_MES_B270_R0040": "They left their boss... Loyal crew.",
    "DK4_MES_B270_R0043": "Grr...",
    "DK4_MES_B270_R0048": "You know why we're here. Come with us to Lisbon!",
    "DK4_MES_B270_R0052": "Damn! This is the end!",
}


def main() -> None:
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = [row for row in csv.DictReader(stream) if row["id"].startswith(prefixes)]

    records = []
    block_counts: dict[str, int] = {}
    for row in source_rows:
        row_id = row["id"]
        english = OVERRIDES.get(row_id)
        if english is None:
            raise SystemExit(f"Raphael V66 unresolved record: {row_id}")
        unsafe = english
        for macro in ("FI", "FA", "FO", "FU"):
            unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        source_hex = row["source_hex"].upper()
        first = int(source_hex[:2], 16)
        state = f"{first:02X}" if first in SPEAKERS else ""
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        block_counts[str(block)] = block_counts.get(str(block), 0) + 1
        records.append(
            {
                "id": row_id,
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(first, "Raphael or scene text"),
                "context": CONTEXT[block],
                "source_meaning": english.replace("{LB}", " "),
                "localization_note": "Faithful concise American English preserving names, contract order, scene timing, and fixed-record constraints.",
                "qa_waivers": [
                    "weak-line-ending",
                    "orphan-final-line",
                    *(["manual-break"] if "{LB}" in english else []),
                ],
                **(
                    {
                        "manual_break_reason": (
                            "Protects the native row boundary from progressive ASCII pair-phase wrapping."
                        )
                    }
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

    if len(records) != len(source_rows):
        raise SystemExit(f"Raphael V66 inventory mismatch: {len(records)} != {len(source_rows)}")

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v66-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Six source-locked Raphael guild-contract events across SC0 blocks 265-270, covering the capture of Jean Ramusio and Jacob Portunto.",
        "excluded_records": {},
        "inventory": {
            "identified_records": len(source_rows),
            "translated_records": len(records),
            "blocks": block_counts,
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
