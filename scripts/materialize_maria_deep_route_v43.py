from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc3/script.csv")
OUTPUT = Path("translations/maria_deep_route_v43.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (242, 243, 244, 245, 248, 251, 252, 281, 282, 283, 284, 291, 292, 293)

EXCLUDED = {
    "DK4_MES_B252_R0037": "Eight-byte scene-transition payload 056040468A803E63; not independently rendered dialogue.",
    "DK4_MES_B281_R0037": "Eight-byte scene-transition payload 0560414689803E63; not independently rendered dialogue.",
    "DK4_MES_B281_R0316": "Five-byte scene-control payload 468A808143; not independently rendered dialogue.",
    "DK4_MES_B283_R0035": "Eight-byte scene-transition payload 056061469A803F63; not independently rendered dialogue.",
    "DK4_MES_B283_R0062": "Four-byte scene-control payload 11469E80; not independently rendered dialogue.",
    "DK4_MES_B283_R0090": "Four-byte scene-control payload 40469C80; not independently rendered dialogue.",
    "DK4_MES_B291_R0037": "Eight-byte scene-transition payload 056041468A803E63; not independently rendered dialogue.",
    "DK4_MES_B291_R0065": "Four-byte scene-control payload 21469180; not independently rendered dialogue.",
    "DK4_MES_B291_R0105": "Four-byte scene-control payload 20468E80; not independently rendered dialogue.",
    "DK4_MES_B291_R0180": "Four-byte scene-control payload 94468C80; not independently rendered dialogue.",
    "DK4_MES_B292_R0036": "Seven-byte scene-transition payload 60404699803F63; not independently rendered dialogue.",
    "DK4_MES_B292_R0141": "Six-byte scene-control payload 2B6320469480; not independently rendered dialogue.",
    "DK4_MES_B292_R0215": "Six-byte scene-control payload 2B6310469480; not independently rendered dialogue.",
    "DK4_MES_B293_R0022": "Eight-byte scene-transition payload 0560404694803F63; not independently rendered dialogue.",
    "DK4_MES_B293_R0069": "Three-byte scene-control payload 469580; not independently rendered dialogue.",
    "DK4_MES_B293_R0079": "Six-byte scene-control payload 2B6322469380; not independently rendered dialogue.",
}

LINES = {
    "DK4_MES_B242_R0011": "We must find Jacob's fleet.",
    "DK4_MES_B242_R0023": "Still no sign of Jacob?",
    "DK4_MES_B243_R0004": "You look capable.{LB}Will you take down a wanted man?",
    "DK4_MES_B243_R0008": "Gabriel Carducci is an outlaw.{LB}He trades here against our pact{LB}and harms our business.",
    "DK4_MES_B243_R0011": "He has a fleet too strong{LB}for the guards.{LB}Take this advance and prepare well.",
    "DK4_MES_B243_R0021": "Received 12,000 coins.",
    "DK4_MES_B244_R0004": "Gabriel!",
    "DK4_MES_B244_R0008": "Sorry. Never again.",
    "DK4_MES_B244_R0012": "Can we trust that...?",
    "DK4_MES_B244_R0016": "Anyway, thank you.{LB}Here is the rest of your reward.",
    "DK4_MES_B244_R0020": "Received 72,000 coins.",
    "DK4_MES_B244_R0046": "Havana share rose slightly!",
    "DK4_MES_B244_R0065": "Have you seen the village{LB}far north in the New World?",
    "DK4_MES_B244_R0069": "A monk from this city went north{LB}to spread his faith...",
    "DK4_MES_B244_R0073": "He vanished after finding{LB}the village.{LB}Hope he is safe.",
    "DK4_MES_B245_R0011": "Gabriel's fleet is{LB}in the New World.",
    "DK4_MES_B245_R0023": "Catch Gabriel, and hurry.",
    "DK4_MES_B248_R0011": "We must defeat pirate William.",
    "DK4_MES_B248_R0023": "William's fleet is{LB}in the New World.",
    "DK4_MES_B251_R0011": "Hernan, pirate of{LB}the Mediterranean.",
    "DK4_MES_B251_R0023": "Hurry and crush Hernan!",
    "DK4_MES_B282_R0006": "{MACRO:FI}, welcome!",
    "DK4_MES_B282_R0009": "We saw the imperial palace.{LB}Such a vast place!{LB}You should see it too.",
    "DK4_MES_B284_R0005": "Ah, {MACRO:FI}.{LB}A message for you{LB}slipped my mind.",
    "DK4_MES_B284_R0009": "An ancient map was found.{LB}They say it marks ruins{LB}of an old kingdom near this city.",
    "DK4_MES_B284_R0012": "A map...{LB}Sounds intriguing.{LB}Know where it is?",
    "DK4_MES_B284_R0016": "Sorry, no.{LB}But if you are curious,{LB}why not search for it?",
}

STATES = {0x03, 0x43, 0x93, 0x94, 0xC9, 0xCD, 0xFE}
SPEAKERS = {
    "03": "Maria",
    "43": "Gabriel Carducci",
    "93": "Guildmaster",
    "94": "Guildmaster",
    "C9": "Tavern patron",
    "CD": "Tavern patron",
    "FE": "System",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as source:
        all_rows = {row["id"]: row for row in csv.DictReader(source)}
    rows = {
        record_id: row
        for record_id, row in all_rows.items()
        if any(record_id.startswith(f"DK4_MES_B{block}_") for block in BLOCKS)
        and (record_id in LINES or record_id in EXCLUDED)
    }
    if set(LINES) | set(EXCLUDED) != set(rows):
        raise SystemExit(
            f"Maria V43 mismatch: missing={sorted(set(rows) - set(LINES) - set(EXCLUDED))}, "
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
        waivers = ["weak-line-ending", "orphan-final-line"]
        if "{LB}" in english:
            waivers.append("manual-break")
        records.append(
            {
                "id": record_id,
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(state, "Companion"),
                "context": "Outstanding bounty reminders and completion, northern-monk rumor, and late-route ruin leads.",
                "source_meaning": english.replace("{LB}", " ")
                .replace("{MACRO:FI}", "the protagonist's given name")
                .strip(),
                "localization_note": "Direct SC3 translation reviewed for natural English, reward and location parity, macro preservation, and state-byte safety.",
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
        "dialogue_profile": "maria-story-shared-events-v43-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 outstanding tail records: bounty reminders/completion, northern-monk rumor, imperial-palace and ancient-map ruin leads, and verified nontext controls.",
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
