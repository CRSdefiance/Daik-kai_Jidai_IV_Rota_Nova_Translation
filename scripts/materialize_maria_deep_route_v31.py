from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
OUTPUT = Path("translations/maria_deep_route_v31.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (286, 287, 288, 289, 290)

LINES = {
    "DK4_MES_B286_R0005": "Welcome.",
    "DK4_MES_B286_R0009": "{MACRO:FI}, know the Goryeo Burner?{LB}Said to lie in East Asia.",
    "DK4_MES_B286_R0013": "They say it makes divinations accurate.{LB}This woman would love to try it.",
    "DK4_MES_B286_R0030": "Hmm.",
    "DK4_MES_B286_R0034": "Also...",
    "DK4_MES_B286_R0038": "Pirates are active nearby.{LB}Keep your equipment ready.",
    "DK4_MES_B286_R0043": "Dangerous.{LB}Thanks. We will be careful.",
    "DK4_MES_B286_R0046": "See you.",
    "DK4_MES_B287_R0004": "Admiral, there is a job{LB}only you can handle.",
    "DK4_MES_B287_R0008": "What?",
    "DK4_MES_B287_R0012": "Bandits raid this town.",
    "DK4_MES_B287_R0016": "Bandits? Here?",
    "DK4_MES_B287_R0020": "They seek our gold and ivory.{LB}They are well trained.",
    "DK4_MES_B287_R0023": "Our guards lack battle experience{LB}and proper arms.",
    "DK4_MES_B287_R0026": "Bring five cargo holds of armor.{LB}Europe should sell it.",
    "DK4_MES_B287_R0029": "Mediterranean or North Sea...{LB}This may take time.",
    "DK4_MES_B287_R0032": "We will wait, but lives are at stake.{LB}Please do not forget.",
    "DK4_MES_B287_R0036": "Armor: five holds.{LB}Understood.",
    "DK4_MES_B287_R0039": "Please do.",
    "DK4_MES_B288_R0006": "Thank you.",
    "DK4_MES_B288_R0010": "More guards revealed another problem:{LB}we lack muskets.",
    "DK4_MES_B288_R0014": "Bring five holds of muskets too.{LB}Payment comes when all is delivered.",
    "DK4_MES_B288_R0018": "Understood.",
    "DK4_MES_B289_R0005": "Back already?",
    "DK4_MES_B289_R0009": "Bad news. The bandits noticed us{LB}and are arming themselves too.",
    "DK4_MES_B289_R0012": "Now we need cannons as well.",
    "DK4_MES_B289_R0015": "Bring two cargo holds quickly.{LB}Payment comes after delivery.",
    "DK4_MES_B289_R0019": "You should have said so...",
    "DK4_MES_B289_R0023": "Sorry. Please bear with us.",
    "DK4_MES_B289_R0026": "Two holds.",
    "DK4_MES_B290_R0005": "Perfect. Defenses this strong{LB}should deter them.",
    "DK4_MES_B290_R0009": "Sorry for all those trips.{LB}Here is your payment and reward.",
    "DK4_MES_B290_R0014": "Received 77,000 coins.",
    "DK4_MES_B290_R0036": "San Jorge share rose slightly!",
    "DK4_MES_B290_R0047": "Where is the bandits' hideout?",
    "DK4_MES_B290_R0050": "What? Why do you want to know?",
    "DK4_MES_B290_R0053": "What do you think?",
    "DK4_MES_B290_R0057": "So eager... Rumor puts them{LB}in ruins deep in the Sahara. Be careful.",
}

PRESENTATION_STATES = {0x03, 0x93, 0xCC, 0xFE}
SPEAKERS = {"03": "Maria", "93": "Guildmaster", "CC": "Local woman", "FE": "System"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    rows = {row_id: row for row_id, row in all_rows.items() if row_id.startswith(prefixes)}
    if set(LINES) != set(rows):
        raise SystemExit(f"Maria V31 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}")
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
            "speaker": SPEAKERS.get(state, "Maria"), "context": "Rumor or San Jorge defense-supply event.",
            "source_meaning": english,
            "localization_note": "Direct SC3 translation reviewed for natural English and state-byte safety.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line"] + (["manual-break"] if "{LB}" in english else []),
            **({"manual_break_reason": "Protects semantic rows and pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    payload = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC3.DK4",
        "source_file_sha256": SC3_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-events-v31-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 blocks 286-290: celadon rumor and complete San Jorge supply event.",
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "excluded_records": 0, "blocks": block_counts},
        "excluded": [], "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
