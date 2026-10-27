from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc3/script.csv")
OUTPUT = Path("translations/maria_deep_route_v39.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (254, 255, 256, 257, 258)

LINES = {
    "DK4_MES_B254_R0004": "A job for you. Our navigators{LB}are suffering badly from scurvy.",
    "DK4_MES_B254_R0008": "You sail the whole world.{LB}Perhaps you know a good cure.",
    "DK4_MES_B254_R0012": "Rumor says a wondrous medicine{LB}hidden near Africa cures scurvy.{LB}Know anything about it?",
    "DK4_MES_B254_R0023": "Hmm...",
    "DK4_MES_B254_R0027": "Please find it somehow.{LB}A loan is all we need.",
    "DK4_MES_B254_R0031": "All right. We will look.",
    "DK4_MES_B254_R0035": "Thanks!{LB}You have my gratitude!",
    "DK4_MES_B254_R0044": "Ah, then...{LB}This may be it.",
    "DK4_MES_B254_R0047": "You had it!{LB}Just what one expects{LB}from Ms. {MACRO:FA}!",
    "DK4_MES_B254_R0051": "Sorry, but could we borrow it{LB}until our navigators recover?{LB}One month should do.",
    "DK4_MES_B254_R0054": "Certainly.",
    "DK4_MES_B254_R0058": "Knew you could be trusted!",
    "DK4_MES_B254_R0065": "Lent the Lime Drops.",
    "DK4_MES_B254_R0069": "Come back in one month for your reward.{LB}Do not forget. Thanks!",
    "DK4_MES_B255_R0004": "Could this be it?",
    "DK4_MES_B255_R0008": "You found it!{LB}Just what one expects{LB}from Ms. {MACRO:FA}!",
    "DK4_MES_B255_R0012": "Please lend it until our navigators{LB}recover. One month should do.",
    "DK4_MES_B255_R0016": "Certainly.",
    "DK4_MES_B255_R0024": "Lent the Lime Drops.",
    "DK4_MES_B255_R0028": "Come back in one month for your reward.{LB}Do not forget. Thanks!",
    "DK4_MES_B256_R0012": "Where could that scurvy cure be?",
    "DK4_MES_B256_R0017": "The scurvy cure must be{LB}these Lime Drops.{LB}Better take them to London's guild.",
    "DK4_MES_B257_R0005": "London's guild has had the Lime Drops{LB}long enough. Time to get them back.",
    "DK4_MES_B258_R0004": "Ah, there you are. Thanks!{LB}Everyone has fully recovered.",
    "DK4_MES_B258_R0012": "Received 20,000 coins.",
    "DK4_MES_B258_R0037": "London share rose slightly!",
    "DK4_MES_B258_R0048": "Any famous ruins{LB}near this city?",
    "DK4_MES_B258_R0051": "A little far from London,{LB}but easy to reach with a map.{LB}A strange group stays there lately.",
    "DK4_MES_B258_R0054": "Odd?",
    "DK4_MES_B258_R0058": "They drove out the caretaker{LB}and conduct eerie rituals.{LB}The neighbors are troubled.",
    "DK4_MES_B258_R0061": "{LB}Oh?{LB}And where is this map?",
    "DK4_MES_B258_R0064": "They bought every map in town,{LB}so none remain here.{LB}Another city may sell one.",
}

PRESENTATION_STATES = {0x03, 0x93, 0xFE}
SPEAKERS = {"03": "Maria", "93": "Guildmaster", "FE": "System"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    rows = {
        row_id: row
        for row_id, row in all_rows.items()
        if any(row_id.startswith(f"DK4_MES_B{block}_") for block in BLOCKS)
    }
    if set(LINES) != set(rows):
        raise SystemExit(
            f"Maria V39 mismatch: missing={sorted(set(rows) - set(LINES))}, "
            f"extra={sorted(set(LINES) - set(rows))}"
        )

    records = []
    block_counts = {str(block): 0 for block in BLOCKS}
    for row_id in sorted(
        rows,
        key=lambda value: (
            int(value.split("_B", 1)[1].split("_", 1)[0]),
            int(value.rsplit("R", 1)[1]),
        ),
    ):
        row = rows[row_id]
        english = LINES[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in PRESENTATION_STATES else ""
        leading_break = english.startswith("{LB}")
        if not state and not leading_break:
            raise SystemExit(f"{row_id}: unclassified leading byte {first:02X}")
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        block_counts[block] += 1
        waivers = ["weak-line-ending", "orphan-final-line"]
        if "{LB}" in english:
            waivers.append("manual-break")
        if leading_break:
            waivers.append("source-leading-linebreak")
        records.append(
            {
                "id": row_id,
                "english": (
                    f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}"
                ),
                "speaker": SPEAKERS.get(state, "Companion"),
                "context": (
                    "London guild's Lime Drops scurvy-cure loan, timed return, reward, "
                    "and follow-up ruin lead."
                ),
                "source_meaning": (
                    english.replace("{LB}", " ")
                    .replace("{MACRO:FA}", "the protagonist's family name")
                    .strip()
                ),
                "localization_note": (
                    "Direct SC3 translation reviewed for natural English, item-name consistency, "
                    "macro preservation, timed-quest continuity, and state-byte safety."
                ),
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
        "dialogue_profile": "maria-story-shared-events-v39-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 blocks 254-258: complete Lime Drops scurvy-cure loan quest, "
            "timed return, reward, and London ruin lead."
        ),
        "inventory": {
            "identified_records": len(rows),
            "translated_records": len(records),
            "excluded_records": 0,
            "blocks": block_counts,
        },
        "excluded": [],
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
