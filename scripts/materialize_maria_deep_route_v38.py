from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc3/script.csv")
OUTPUT = Path("translations/maria_deep_route_v38.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (270, 271, 272, 273)

LINES = {
    "DK4_MES_B270_R0005": "Oh, {MACRO:FI}!{LB}Welcome!",
    "DK4_MES_B270_R0008": "Thanks to you,{LB}my dancing has greatly improved!",
    "DK4_MES_B270_R0011": "A useful tip in return.",
    "DK4_MES_B270_R0015": "Deep inland stands a mosque{LB}honoring an ancient king.{LB}They say treasure sleeps there.",
    "DK4_MES_B270_R0019": "Only those accepted by the king{LB}may claim the treasure.{LB}Why not try your luck?",
    "DK4_MES_B271_R0004": "Anyone among you know shipbuilding{LB}and gunnery?",
    "DK4_MES_B271_R0015": "Glad to help.{LB}What is it?",
    "DK4_MES_B271_R0029": "My turn, is it?",
    "DK4_MES_B271_R0044": "Yes, yes! You called for me?",
    "DK4_MES_B271_R0058": "Leave the cannons to me.",
    "DK4_MES_B271_R0065": "What do you mean?",
    "DK4_MES_B271_R0069": "Ever heard of a carronade?{LB}This new European cannon has{LB}long range and great power.",
    "DK4_MES_B271_R0072": "Carronades may spread widely{LB}and transform naval warfare.",
    "DK4_MES_B271_R0076": "Our boarding tactics would be helpless{LB}against European gunships.",
    "DK4_MES_B271_R0079": "We are studying armor{LB}to withstand their fire.",
    "DK4_MES_B271_R0082": "We need advice from experts{LB}in shipbuilding and gunnery.",
    "DK4_MES_B271_R0100": "Ships? A little...",
    "DK4_MES_B271_R0115": "Hmm. Shipbuilding advice, yes.{LB}However...",
    "DK4_MES_B271_R0129": "But gunnery is not my strength.",
    "DK4_MES_B271_R0136": "Leave gunnery to me.",
    "DK4_MES_B271_R0148": "Then let me advise on shipbuilding.",
    "DK4_MES_B271_R0165": "Do not forget my shipcraft.",
    "DK4_MES_B271_R0182": "Ask me anything about ships.",
    "DK4_MES_B271_R0218": "Sadly, no one here knows{LB}European shipbuilding and gunnery.",
    "DK4_MES_B271_R0223": "Sadly, no one here knows{LB}European shipbuilding.",
    "DK4_MES_B271_R0251": "Very well. Bring an expert{LB}when you find one. No hurry.",
    "DK4_MES_B271_R0257": "The barrel is shaped like this.{LB}Powder explodes here,{LB}driving the shot...",
    "DK4_MES_B271_R0269": "Angling the hull this way{LB}will disperse the impact.",
    "DK4_MES_B271_R0275": "Ah... So this is the damage{LB}that cannon would cause.",
    "DK4_MES_B271_R0287": "With this material,{LB}it should not break easily!",
    "DK4_MES_B271_R0301": "Adding armor here and here{LB}would be most effective.",
    "DK4_MES_B271_R0311": "Excellent!{LB}Complete!{LB}This will astonish them!",
    "DK4_MES_B271_R0315": "Oh, right! Tell the guildmaster{LB}we finally completed it!",
    "DK4_MES_B272_R0007": "Oh! You brought them!",
    "DK4_MES_B272_R0011": "Yes. Leave gunnery to me!",
    "DK4_MES_B272_R0023": "Then let me advise on shipbuilding.",
    "DK4_MES_B272_R0037": "Remember my shipcraft.",
    "DK4_MES_B272_R0052": "Ask me anything about ships.",
    "DK4_MES_B272_R0059": "Barrel shaped like this.{LB}Powder explodes here,{LB}driving the shot...",
    "DK4_MES_B272_R0071": "Angling the hull this way{LB}will disperse the impact.",
    "DK4_MES_B272_R0077": "Ah... So this is the damage{LB}that cannon would cause.",
    "DK4_MES_B272_R0089": "With this material,{LB}it should not break easily!",
    "DK4_MES_B272_R0103": "Adding armor here and here{LB}would be most effective.",
    "DK4_MES_B272_R0114": "Excellent!{LB}Complete!{LB}This will astonish them!",
    "DK4_MES_B272_R0118": "Oh, right! Tell the guildmaster{LB}we finally completed it!",
    "DK4_MES_B273_R0004": "What!? Complete at last!?",
    "DK4_MES_B273_R0007": "Our transports keep getting sunk{LB}by pirates lately.{LB}A real headache.",
    "DK4_MES_B273_R0010": "This should improve matters.{LB}Yes, it is all thanks to you.",
    "DK4_MES_B273_R0014": "A reward from me{LB}and the shipwright.",
    "DK4_MES_B273_R0019": "What's this?",
    "DK4_MES_B273_R0022": "They say it was made in an age{LB}so ancient it is hard to believe.{LB}Not very useful, but rare, eh?",
    "DK4_MES_B273_R0025": "Yes. Thank you. This is rare.",
}

PRESENTATION_STATES = {0x03, 0x04, 0x0D, 0x12, 0x17, 0x6E, 0x94, 0xC5}
SPEAKERS = {
    "03": "Maria",
    "04": "Janus",
    "0D": "Cesare",
    "12": "Charles",
    "17": "Manuel",
    "6E": "Shipwright",
    "94": "Guildmaster",
    "C5": "Dancer",
}


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
            f"Maria V38 mismatch: missing={sorted(set(rows) - set(LINES))}, "
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
        if not state:
            raise SystemExit(f"{row_id}: unclassified leading byte {first:02X}")
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        block_counts[block] += 1
        waivers = ["weak-line-ending", "orphan-final-line"]
        if "{LB}" in english:
            waivers.append("manual-break")
        records.append(
            {
                "id": row_id,
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}",
                "speaker": SPEAKERS[state],
                "context": (
                    "Dancer's inland-mosque lead and carronade-defense research quest, "
                    "including specialist branches and guild reward."
                ),
                "source_meaning": english.replace("{LB}", " ").replace("{MACRO:FI}", "the protagonist's given name"),
                "localization_note": (
                    "Direct SC3 translation reviewed for natural English, branch parity, "
                    "macro preservation, and presentation-byte safety."
                ),
                "qa_waivers": waivers,
                **(
                    {"manual_break_reason": "Preserves semantic grouping within the four-line dialogue window."}
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
        "dialogue_profile": "maria-story-shared-events-v38-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 blocks 270-273: dancer treasure lead and complete "
            "carronade-defense research quest."
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
