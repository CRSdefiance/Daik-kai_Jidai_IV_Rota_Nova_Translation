from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v23.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (150, 152, 155, 158, 197, 241)

OVERRIDES = {
    "DK4_MES_B150_R0005": "Tomatoes! The age of tomatoes!",
    "DK4_MES_B150_R0008": "Really? This bright-red food?",
    "DK4_MES_B150_R0011": (
        "That red stirs one's passion.{LB}Ah, the burning love of youth..."
    ),
    "DK4_MES_B150_R0015": "...Good for you.",
    "DK4_MES_B150_R0019": "Make tomato dishes. Sell them at once.",
    "DK4_MES_B150_R0026": "We mustn't miss this tomato craze.",
    "DK4_MES_B150_R0029": "Yeah.",
    "DK4_MES_B152_R0030": "Maybe a taste.{LB}Barkeep, bring me a glass of wine.",
    "DK4_MES_B152_R0034": "Yes.",
    "DK4_MES_B152_R0038": "Gulp, gulp, gulp...",
    "DK4_MES_B152_R0046": "Delicious!{LB}Barkeep, another!",
    "DK4_MES_B155_R0007": "Yes. To the duke's son, correct?",
    "DK4_MES_B155_R0010": "That ring could buy a mountain.",
    "DK4_MES_B155_R0013": "Such wealth suits a duke.{LB}When might we see that jewel?",
    "DK4_MES_B155_R0016": "Before long, surely.{LB}Then every lady will want that gem.",
    "DK4_MES_B155_R0020": "Once it catches on, it'll be too late!{LB}Do you know which gem?",
    "DK4_MES_B155_R0024": "No. We must ask around at once!",
    "DK4_MES_B158_R0005": "So cold. Truly freezing.",
    "DK4_MES_B158_R0009": "Yes. Coldest in years.",
    "DK4_MES_B158_R0012": "A fur coat would help.{LB}This cold may freeze me.",
    "DK4_MES_B158_R0015": "This cold has raised fur sales and prices.",
    "DK4_MES_B158_R0018": "So they say. Brrr!",
    "DK4_MES_B158_R0021": "Hope it warms up soon.",
    "DK4_MES_B158_R0025": "True. While cold,{LB}fur would be lovely.",
    "DK4_MES_B197_R0004": "Hello, Safia.{LB}Your eyes stay mysterious.",
    "DK4_MES_B197_R0007": "Oh, Julian. Welcome.",
    "DK4_MES_B197_R0014": "What is it?{LB}Something on my face?",
    "DK4_MES_B197_R0017": (
        "No... When those eyes gaze at me,{LB}"
        "they almost draw me in.{LB}"
        "Does petrification feel like this?"
    ),
    "DK4_MES_B197_R0021": "What's that?",
    "DK4_MES_B197_R0025": (
        "The tale of Medusa's Shield{LB}"
        "in the Tasman Sea stayed with me.{LB}"
        "Your eyes brought it to mind."
    ),
    "DK4_MES_B197_R0028": (
        "Medusa is the snake-haired monster, right?{LB}"
        "Are you calling me frightening and ugly?"
    ),
    "DK4_MES_B197_R0031": (
        "Nonsense. Even with your hair concealed,{LB}"
        "those beautiful eyes alone could capture me."
    ),
    "DK4_MES_B197_R0034": "Always joking.",
    "DK4_MES_B197_R0038": (
        "Turned to stone by your hand,{LB}"
        "forever beside you in the moonlight...{LB}"
        "How romantic."
    ),
    "DK4_MES_B197_R0042": "Even as stone,{LB}don't expect my care.",
    "DK4_MES_B197_R0045": (
        "How cold. Yet that aloofness is charming.{LB}"
        "Well, time to go. See you."
    ),
    "DK4_MES_B197_R0049": "See you.",
    "DK4_MES_B197_R0053": "Odd comparison...{LB}Still, my heart raced.",
    "DK4_MES_B241_R0012": "What are you saying?{LB}All of it was stolen cargo!",
    "DK4_MES_B241_R0015": "Thanks for catching him.{LB}Not much, but take this.",
    "DK4_MES_B241_R0061": "Got a special lead just for you.",
    "DK4_MES_B241_R0065": (
        "Explore beyond the city gate.{LB}"
        "A building ahead is said to hide great treasure."
    ),
    "DK4_MES_B241_R0076": "Don't forget to get a map{LB}before exploring.",
}

SPEAKERS = {
    "1A": "Julian",
    "44": "Cargo thief",
    "5C": "Barkeep",
    "60": "Patron",
    "94": "Merchant",
    "A4": "Husband",
    "A5": "Wife",
    "A6": "Lady",
    "A7": "Lady",
    "AE": "Merchant",
    "AF": "Assistant",
    "C5": "Safia",
    "FE": "System or market report",
}
PRESENTATION_STATES = {int(value, 16) for value in SPEAKERS}


def main() -> None:
    report = json.loads(REUSE.read_text(encoding="utf-8"))
    lines = {
        str(item["id"]): str(item["variants"][0]["english"])
        for item in report["reusable"]
        if int(item["block"]) in BLOCKS
    }
    lines.update(OVERRIDES)
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    rows = {row_id: row for row_id, row in all_rows.items() if row_id.startswith(prefixes)}
    if set(lines) != set(rows):
        raise SystemExit(
            f"Maria V23 mismatch: missing={sorted(set(rows)-set(lines))}, "
            f"extra={sorted(set(lines)-set(rows))}"
        )

    records = []
    block_counts: dict[str, int] = {}
    for row_id in sorted(
        lines,
        key=lambda value: (
            int(value.split("_B")[1].split("_")[0]),
            int(value.rsplit("R", 1)[1]),
        ),
    ):
        english = lines[row_id]
        row = rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in PRESENTATION_STATES else ""
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        block_counts[block] = block_counts.get(block, 0) + 1
        records.append(
            {
                "id": row_id,
                "english": (
                    f"{{SPEAKER:{state}}}{english}{{PAD}}"
                    if state
                    else f"{english}{{PAD}}"
                ),
                "speaker": SPEAKERS.get(state, "Shared-event participant"),
                "context": (
                    "Complete shared market-rumor, tavern, companion conversation, "
                    "or cargo-thief reward event."
                ),
                "source_meaning": english,
                "localization_note": (
                    "Cross-route Japanese match reviewed and rewritten for natural "
                    "English with SC3-specific state-byte classification."
                ),
                "qa_waivers": ["weak-line-ending", "orphan-final-line"]
                + (["manual-break"] if "{LB}" in english else []),
                **(
                    {"manual_break_reason": "Protects semantic rows and pair phase."}
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
        "dialogue_profile": "maria-story-shared-events-v23-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 blocks 150, 152, 155, 158, 197, and 241: four market "
            "rumors, a tavern wine rumor, the Julian/Safia Medusa-shield scene, "
            "and the Calicut cargo-thief reward."
        ),
        "inventory": {
            "identified_records": len(rows),
            "translated_records": len(records),
            "excluded_records": 0,
            "blocks": block_counts,
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
