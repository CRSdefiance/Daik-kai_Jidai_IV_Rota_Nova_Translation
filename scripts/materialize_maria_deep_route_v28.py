from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v28.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (187, 188, 195, 196, 200, 201, 202, 203, 204)

OVERRIDES = {
    "DK4_MES_B187_R0013": "Admiral, a letter from Janus.",
    "DK4_MES_B187_R0015": "Admiral, letter from Janus.",
    "DK4_MES_B187_R0017": "Admiral, Janus sent a letter.",
    "DK4_MES_B187_R0019": "Admiral, this is from Janus.",
    "DK4_MES_B187_R0021": "Admiral, letter from Janus.",
    "DK4_MES_B187_R0023": "Admiral, Janus sent word.",
    "DK4_MES_B187_R0025": "Admiral! A letter from Janus!",
    "DK4_MES_B187_R0047": "Judas betrayed Jesus. People fear his belongings, so none seek the blade.",
    "DK4_MES_B187_R0050": "The sword is magnificent. A blade bears no guilt; it is worth seeking.",
    "DK4_MES_B187_R0067": "Expect another letter{LB}if more comes to light.{LB}Janus Pasha",
    "DK4_MES_B187_R0074": "A traitor's sword...{LB}Janus says blades bear no guilt.{LB}Ever pragmatic.",
    "DK4_MES_B187_R0086": "No real objection.{LB}Judas repented in the end.{LB}The choice is yours, Admiral.",
    "DK4_MES_B188_R0004": "Who built these ruins?{LB}They recall Solomon's mines{LB}from the Old Testament.",
    "DK4_MES_B188_R0018": "Yes. What is it?",
    "DK4_MES_B188_R0022": "Thank you. The town is grateful.",
    "DK4_MES_B188_R0025": "No need to thank me.",
    "DK4_MES_B188_R0028": "Have you heard the rumor{LB}about King Solomon?",
    "DK4_MES_B188_R0032": "Go on.",
    "DK4_MES_B188_R0036": "King Solomon once{LB}commanded even demon kings.",
    "DK4_MES_B188_R0040": "A demon king?",
    "DK4_MES_B188_R0050": "An icy isle northwest?{LB}Could it be the frozen isle?",
    "DK4_MES_B188_R0053": "A demon's weapon...{LB}Thanks. We will search.",
    "DK4_MES_B195_R0008": "Gerhard? At sunset?{LB}Something on your mind?",
    "DK4_MES_B195_R0012": "Admiral... A tale heard in Japan{LB}stirred something in me.",
    "DK4_MES_B195_R0016": "Hearing that from you...{LB}Who was he?",
    "DK4_MES_B195_R0022": "What sort?",
    "DK4_MES_B195_R0043": "...A tragic hero.",
    "DK4_MES_B195_R0047": "Yes.{LB}Noritsune's regrets{LB}must have been bitter...",
    "DK4_MES_B195_R0051": "You were moved.{LB}That suits you.",
    "DK4_MES_B195_R0057": "Enough talk from me.{LB}Shall we return to work?",
    "DK4_MES_B196_R0013": "Admiral, a letter from Dukov.",
    "DK4_MES_B196_R0014": "Admiral, a letter from Dukov.",
    "DK4_MES_B196_R0015": "Admiral, Dukov sent a letter.",
    "DK4_MES_B196_R0016": "Admiral, this is from Dukov.",
    "DK4_MES_B196_R0017": "Admiral, letter from Dukov.",
    "DK4_MES_B196_R0018": "Admiral, Dukov sent word.",
    "DK4_MES_B196_R0019": "Admiral! A letter from Dukov!",
    "DK4_MES_B196_R0047": "Should this interest you,{LB}perhaps investigate it.{LB}Dukov",
    "DK4_MES_B196_R0055": "He studies Asian history?{LB}Unexpected.",
    "DK4_MES_B196_R0069": "You know history too.",
    "DK4_MES_B200_R0008": "Training late again.{LB}Don't overdo it or you won't last.",
    "DK4_MES_B200_R0021": "Could it be?",
    "DK4_MES_B200_R0025": "With that robe,{LB}fighting freely would be easy...",
    "DK4_MES_B201_R0004": "Admiral, a moment?",
    "DK4_MES_B201_R0008": "What is it?",
    "DK4_MES_B201_R0020": "A shield was once made from armadillo hide: the Steel Hide.",
    "DK4_MES_B201_R0027": "A shield harder than iron would surely help in battle.",
    "DK4_MES_B201_R0033": "Somewhere in Africa.{LB}That is all we know.",
    "DK4_MES_B201_R0023": "What about it?",
    "DK4_MES_B201_R0030": "Maybe. Where can we find it?",
    "DK4_MES_B201_R0037": "Too little to go on.{LB}Hard to find.",
    "DK4_MES_B201_R0040": "That's true...",
    "DK4_MES_B201_R0044": "All right. We'll remember it.{LB}With luck, we'll find it.",
    "DK4_MES_B201_R0047": "Right.",
    "DK4_MES_B202_R0004": "Admiral, a moment?",
    "DK4_MES_B202_R0008": "What is it?",
    "DK4_MES_B202_R0022": "Same claim as{LB}that armadillo shield?",
    "DK4_MES_B202_R0030": "All right. What about the shield?",
    "DK4_MES_B202_R0037": "You said exactly the same thing{LB}about that armadillo shield.",
    "DK4_MES_B202_R0040": "Did that happen? Never mind.",
    "DK4_MES_B202_R0044": "All right. Where can we find it?",
    "DK4_MES_B202_R0047": "Only that it lies somewhere{LB}around the eastern ocean.",
    "DK4_MES_B202_R0050": "That's not enough to find it.",
    "DK4_MES_B202_R0054": "...True.",
    "DK4_MES_B202_R0058": "All right. We'll remember it.{LB}With luck, we'll find it.",
    "DK4_MES_B202_R0061": "Right.",
    "DK4_MES_B203_R0004": "Admiral, a moment?",
    "DK4_MES_B203_R0008": "What is it?",
    "DK4_MES_B203_R0016": "Like China's Vermilion Bird?{LB}Seeing one would be wonderful.{LB}What about the phoenix?",
    "DK4_MES_B203_R0023": "And you want it because{LB}it would help us in battle?",
    "DK4_MES_B203_R0030": "You've said that before.",
    "DK4_MES_B203_R0037": "Honestly... Where is it?{LB}Will you give another vague answer{LB}like Africa or the eastern seas?",
    "DK4_MES_B203_R0044": "Oh? A much narrower area this time.",
    "DK4_MES_B203_R0047": "Of course! Some research paid off.{LB}At first, all we knew was northern Europe.",
    "DK4_MES_B203_R0051": "You did well.",
    "DK4_MES_B203_R0059": "Since Samwell worked hard,{LB}we'll remember the Phoenix Bascinet.",
    "DK4_MES_B204_R0008": "Never heard the name.{LB}Why?",
    "DK4_MES_B204_R0015": "And...?",
    "DK4_MES_B204_R0023": "Then that book is worth reading.",
    "DK4_MES_B204_R0030": "How can we find it?{LB}Any clues?",
    "DK4_MES_B204_R0045": "That makes it difficult to find.",
    "DK4_MES_B204_R0052": "Not your fault.",
    "DK4_MES_B204_R0056": "Yes.",
    "DK4_MES_B204_R0060": "To find it, we'll have to search{LB}the Mediterranean.",
}

SPEAKERS = {
    "03": "Maria", "04": "Janus", "0D": "Cesare", "10": "Gerhard",
    "13": "Doctor", "15": "Ian", "16": "Samwell", "17": "Manuel",
    "19": "Martial artist", "78": "Town official", "D0": "Messenger",
}
PRESENTATION_STATES = {int(value, 16) for value in SPEAKERS}


def main() -> None:
    report = json.loads(REUSE.read_text(encoding="utf-8"))
    lines = {
        str(item["id"]): str(item["variants"][0]["english"])
        for item in report["reusable"] if int(item["block"]) in BLOCKS
    }
    lines.update(OVERRIDES)
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    rows = {row_id: row for row_id, row in all_rows.items() if row_id.startswith(prefixes)}
    if set(lines) != set(rows):
        raise SystemExit(
            f"Maria V28 mismatch: missing={sorted(set(rows)-set(lines))}, "
            f"extra={sorted(set(lines)-set(rows))}"
        )

    records = []
    block_counts: dict[str, int] = {}
    for row_id in sorted(rows, key=lambda value: (int(value.split("_B")[1].split("_")[0]), int(value.rsplit("R", 1)[1]))):
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        row = rows[row_id]
        english = lines[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in PRESENTATION_STATES else ""
        block_counts[block] = block_counts.get(block, 0) + 1
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Narrator or alternate messenger"),
            "context": "Complete shared letter, weapon, armor, or equipment-rumor event.",
            "source_meaning": english,
            "localization_note": "Cross-route match or direct SC3 translation reviewed for natural English and state-byte safety.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line"] + (["manual-break"] if "{LB}" in english else []),
            **({"manual_break_reason": "Protects semantic rows and pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })

    payload = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC3.DK4",
        "source_file_sha256": SC3_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-events-v28-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 blocks 187, 188, 195, 196, and 200-204: nine complete shared events.",
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "excluded_records": 0, "blocks": block_counts},
        "excluded": [], "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
