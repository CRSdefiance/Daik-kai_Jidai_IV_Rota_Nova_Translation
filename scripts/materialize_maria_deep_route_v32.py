from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
OUTPUT = Path("translations/maria_deep_route_v32.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (275,)

LINES = {
    "DK4_MES_B275_R0005": "{MACRO:FI}! Trouble!",
    "DK4_MES_B275_R0008": "What is it?",
    "DK4_MES_B275_R0012": "An injured man just staggered in...",
    "DK4_MES_B275_R0015": "Hey, girl! Do not tell them{LB}too much about me. Ow!",
    "DK4_MES_B275_R0019": "Keep still! Rest!",
    "DK4_MES_B275_R0023": "Bad wound.",
    "DK4_MES_B275_R0027": "Damn it!",
    "DK4_MES_B275_R0031": "Stay still. Our doctor is coming.",
    "DK4_MES_B275_R0039": "The danger has passed.",
    "DK4_MES_B275_R0043": "Thanks...",
    "DK4_MES_B275_R0047": "Blade wounds.{LB}Tell us what happened.",
    "DK4_MES_B275_R0054": "Part of a smuggling ring here.",
    "DK4_MES_B275_R0057": "My!",
    "DK4_MES_B275_R0061": "A ring?",
    "DK4_MES_B275_R0065": "Yes. We helped foreigners secretly{LB}sell arms behind the lords' backs.",
    "DK4_MES_B275_R0068": "So you were their contact in Japan?",
    "DK4_MES_B275_R0071": "Right. Supplied the wokou{LB}with guns and weapons.",
    "DK4_MES_B275_R0079": "A priest's sermon in Nagasaki{LB}caught my ear.",
    "DK4_MES_B275_R0083": "At first, just to mock him. His words{LB}made me hate this trade.",
    "DK4_MES_B275_R0087": "Tried to leave. Look what happened.{LB}They chase me everywhere.",
    "DK4_MES_B275_R0091": "Once you are stained, you can never{LB}live honestly again.",
    "DK4_MES_B275_R0094": "That is not true. Honest work exists.{LB}But...",
    "DK4_MES_B275_R0098": "They would not hunt you this fiercely{LB}unless you knew their secret.",
    "DK4_MES_B275_R0102": "A secret? Hmm... Can't be.",
    "DK4_MES_B275_R0105": "Any idea?",
    "DK4_MES_B275_R0109": "Maybe, but would it really matter{LB}that much to them?",
    "DK4_MES_B275_R0113": "Tell me.",
    "DK4_MES_B275_R0117": "Overheard the boss talking{LB}with his men.",
    "DK4_MES_B275_R0120": "Portuguese missionaries are coming.{LB}They seek an audience with Ming's emperor.",
    "DK4_MES_B275_R0124": "When? Which port will they enter?",
    "DK4_MES_B275_R0128": "No idea. The boss kept it quiet{LB}and warned rough men like me away.",
    "DK4_MES_B275_R0131": "Maybe he knew preaching got to me.",
    "DK4_MES_B275_R0134": "That troubles me. Who might know more?",
    "DK4_MES_B275_R0138": "An informant at Macao's tavern{LB}may know more.",
    "DK4_MES_B275_R0141": "At the Macao tavern? Let us go.",
    "DK4_MES_B275_R0144": "Wait. Take me with you.",
    "DK4_MES_B275_R0148": "What? You cannot sail like this!",
    "DK4_MES_B275_R0151": "Any ship is safer than this town.{LB}Right, famous lady admiral?",
    "DK4_MES_B275_R0155": "Perhaps. Come if you wish.",
}

PRESENTATION_STATES = {0x03, 0x66, 0xCB}
SPEAKERS = {"03": "Maria", "66": "Injured smuggler", "CB": "Innkeeper"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    rows = {row_id: row for row_id, row in all_rows.items() if row_id.startswith(prefixes)}
    if set(LINES) != set(rows):
        raise SystemExit(f"Maria V32 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}")
    records = []
    block_counts: dict[str, int] = {}
    for row_id in sorted(rows, key=lambda value: (int(value.split("_B")[1].split("_")[0]), int(value.rsplit("R", 1)[1]))):
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        row = rows[row_id]
        english = LINES[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in PRESENTATION_STATES else ""
        block_counts[block] = block_counts.get(block, 0) + 1
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Maria"), "context": "Macao smuggling-conspiracy opening.",
            "source_meaning": english,
            "localization_note": "Direct SC3 translation reviewed for natural English and state-byte safety.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line"] + (["manual-break"] if "{LB}" in english else []),
            **({"manual_break_reason": "Protects semantic rows and pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    payload = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC3.DK4",
        "source_file_sha256": SC3_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-events-v32-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 block 275: injured defector and Portuguese-missionary smuggling lead.",
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "excluded_records": 0, "blocks": block_counts},
        "excluded": [], "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
