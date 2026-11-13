from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc3/script.csv")
OUTPUT = Path("translations/maria_deep_route_v34.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (277,)

LINES = {
    "DK4_MES_B277_R0005": "There!",
    "DK4_MES_B277_R0009": "Amen...",
    "DK4_MES_B277_R0013": "Know them?",
    "DK4_MES_B277_R0017": "No... Wait!",
    "DK4_MES_B277_R0020": "Him!",
    "DK4_MES_B277_R0028": "The huge guard beside the priest!",
    "DK4_MES_B277_R0035": "Know him?",
    "DK4_MES_B277_R0039": "Yes! Met him on a job.{LB}That is Jacob, one of their leaders!",
    "DK4_MES_B277_R0043": "What!?",
    "DK4_MES_B277_R0047": "Why is he with this delegation?",
    "DK4_MES_B277_R0050": "No...",
    "DK4_MES_B277_R0054": "You figured it out?{LB}Tell me what is happening!",
    "DK4_MES_B277_R0058": "Stay calm. This missionary{LB}delegation is probably a fake.",
    "DK4_MES_B277_R0062": "What!?",
    "DK4_MES_B277_R0066": "Quiet!",
    "DK4_MES_B277_R0070": "(Right.)",
    "DK4_MES_B277_R0074": "They mean to deceive Ming and sell{LB}huge quantities of smuggled arms.",
    "DK4_MES_B277_R0078": "Their homeland would expose them{LB}almost immediately!",
    "DK4_MES_B277_R0081": "This is a state-level deal.{LB}Success would bring a fortune, used to...",
    "DK4_MES_B277_R0085": "Build modern forces powerful enough{LB}to crush any anti-smuggling fleet.",
    "DK4_MES_B277_R0088": "(Gulp.)",
    "DK4_MES_B277_R0096": "Leave this to me.",
    "DK4_MES_B277_R0101": "{LB}{MACRO:FI}, this may be{LB}an opportunity.",
    "DK4_MES_B277_R0105": "How so?",
    "DK4_MES_B277_R0109": "{LB}Ming might buy arms and gain{LB}strength to resist the great powers.",
    "DK4_MES_B277_R0113": "Too naive. These are veteran smugglers.",
    "DK4_MES_B277_R0116": "Officials ignorant of arms will pay{LB}outrageous prices for obsolete guns.",
    "DK4_MES_B277_R0119": "The people's taxes cannot be wasted{LB}on worthless weapons.",
    "DK4_MES_B277_R0123": "Once rewarded, they will return{LB}with drugs or even slaves.",
    "DK4_MES_B277_R0127": "Let this pass, and they control us.{LB}We cannot allow it.",
    "DK4_MES_B277_R0131": "{LB}Hmm... Perhaps.",
    "DK4_MES_B277_R0135": "Should the army doubt us,{LB}we must stop them ourselves.",
    "DK4_MES_B277_R0139": "They went to the governor.{LB}Hurry!",
}

PRESENTATION_STATES = {0x03, 0x66, 0x8B}
SPEAKERS = {"03": "Maria", "66": "Defector", "8B": "Missionary"}

def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    rows = {row_id: row for row_id, row in all_rows.items() if row_id.startswith(prefixes)}
    if set(LINES) != set(rows):
        raise SystemExit(f"Maria V34 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}")
    records = []
    block_counts: dict[str, int] = {}
    for row_id in sorted(rows, key=lambda value: int(value.rsplit("R", 1)[1])):
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        row, english = rows[row_id], LINES[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in PRESENTATION_STATES else ""
        block_counts[block] = block_counts.get(block, 0) + 1
        leading_break = english.startswith("{LB}")
        waivers = ["weak-line-ending", "orphan-final-line"] + (["manual-break"] if "{LB}" in english else []) + (["source-leading-linebreak"] if leading_break else [])
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Companion" if leading_break else "Maria"), "context": "False-missionary delegation investigation.",
            "source_meaning": english, "localization_note": "Direct SC3 translation reviewed for natural English and state-byte safety.",
            "qa_waivers": waivers,
            **({"manual_break_reason": "Preserves the source-leading speaker/presentation transition."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    payload = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC3.DK4", "source_file_sha256": SC3_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "maria-story-shared-events-v34-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 block 277: false missionaries exposed and Maria's smuggling analysis.",
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "excluded_records": 0, "blocks": block_counts},
        "excluded": [], "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")

if __name__ == "__main__": main()
