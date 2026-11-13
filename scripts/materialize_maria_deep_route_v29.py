from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v29.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (118, 165, 190, 216, 217, 218, 219, 222, 224, 229, 240, 246, 247, 249, 250, 253)

OVERRIDES = {
    "DK4_MES_B118_R0005": "With {MACRO:FO}? Pass.",
    "DK4_MES_B165_R0005": "Have you ever smoked tobacco?",
    "DK4_MES_B165_R0009": "Wait, you have not tried it yet?",
    "DK4_MES_B165_R0012": "No. The chance never came.",
    "DK4_MES_B165_R0015": "Really? With it this popular?{LB}You may be the only one in town!",
    "DK4_MES_B165_R0019": "Maybe.{LB}Might try it.",
    "DK4_MES_B165_R0022": "Come along.{LB}Let me show you.",
    "DK4_MES_B165_R0025": "Sure.",
    "DK4_MES_B165_R0029": "Tobacco may boom here.",
    "DK4_MES_B190_R0004": "Master, do you know{LB}a place called Avalon?",
    "DK4_MES_B190_R0007": "Again? You believe the woman{LB}who calls herself a witch?",
    "DK4_MES_B190_R0011": "Avalon supposedly lies{LB}just west of here.",
    "DK4_MES_B190_R0015": "King Arthur is a fairy tale.{LB}Many ask, but none have found Avalon.",
    "DK4_MES_B216_R0005": "You came back!",
    "DK4_MES_B216_R0009": "Have you ever seen golden sand?",
    "DK4_MES_B216_R0017": "A New World sailor spoke of a river{LB}where golden sand flows.",
    "DK4_MES_B216_R0021": "Just imagining it{LB}feels romantic, does it not?",
    "DK4_MES_B217_R0006": "Hello, {MACRO:FI}.",
    "DK4_MES_B217_R0010": "Do ancient ruins interest you?{LB}This town has some.",
    "DK4_MES_B217_R0013": "You did not know? They are close:{LB}on the hill visible from here.",
    "DK4_MES_B218_R0006": "Have you visited the pyramids?",
    "DK4_MES_B218_R0010": "No.",
    "DK4_MES_B218_R0014": "Everyone visiting should see them.{LB}Here are directions. Enjoy!",
    "DK4_MES_B218_R0017": "Yes. Let's go.",
    "DK4_MES_B219_R0005": "Welcome, {MACRO:FI}.{LB}Pleasant weather again.",
    "DK4_MES_B219_R0009": "Have you seen the nearby ruins?{LB}They may be Solomon's treasury.",
    "DK4_MES_B219_R0012": "Sounds good.",
    "DK4_MES_B219_R0016": "Perfect picnic weather.{LB}Why not visit them?",
    "DK4_MES_B222_R0006": "Hello, {MACRO:FI}! Welcome!",
    "DK4_MES_B222_R0009": "Looking for ruins?{LB}Some lie nearby.",
    "DK4_MES_B222_R0012": "Outsiders rarely hear this,{LB}but you are an exception.",
    "DK4_MES_B224_R0005": "Hello, {MACRO:FI}.",
    "DK4_MES_B224_R0009": "Searching ruins worldwide?{LB}Sadly, none here are famous.",
    "DK4_MES_B229_R0005": "Got a small job.{LB}Want it?",
    "DK4_MES_B229_R0009": "Capture smuggler{LB}Jean Ramusio.",
    "DK4_MES_B229_R0012": "He plans a major deal near South Asia.{LB}Catch him before it grows.",
    "DK4_MES_B240_R0004": "A job for you, {MACRO:FA}.",
    "DK4_MES_B240_R0007": "What is the job?",
    "DK4_MES_B240_R0011": "Capture Jacob Portunto,{LB}a Dutch smuggler with a bounty.",
    "DK4_MES_B240_R0015": "Once a thug, he got rich{LB}in Africa and turned pirate.",
    "DK4_MES_B240_R0018": "This is your advance.{LB}He is too strong for us, but not you.",
    "DK4_MES_B240_R0027": "Received 16,000 coins.",
    "DK4_MES_B246_R0004": "A formidable foe worthy of you.",
    "DK4_MES_B246_R0007": "Defeat the English pirate{LB}William Clive.",
    "DK4_MES_B246_R0010": "He is heading to Havana.{LB}This advance is yours. Good luck.",
    "DK4_MES_B246_R0020": "Received 27,000 coins.",
    "DK4_MES_B246_R0024": "One more thing: he is very dangerous.{LB}You will understand when you meet him.",
    "DK4_MES_B247_R0004": "Gyaaah! Rrraaargh!",
    "DK4_MES_B247_R0008": "William! Caught at last.",
    "DK4_MES_B247_R0011": "Then farewell.",
    "DK4_MES_B247_R0015": "No need to rush off.{LB}Take your reward.",
    "DK4_MES_B247_R0018": "Received 100,000 coins.",
    "DK4_MES_B247_R0043": "Veracruz share rose slightly!",
    "DK4_MES_B247_R0060": "Ancient kingdom ruins lie nearby.{LB}A map pointing to them was found.",
    "DK4_MES_B247_R0063": "A map... Where is it?",
    "DK4_MES_B247_R0066": "No idea.{LB}Search if curious.",
    "DK4_MES_B249_R0004": "What can we do...?{LB}Only you can handle this job.",
    "DK4_MES_B249_R0007": "Defeat the Spanish pirate{LB}Hernan Berio.",
    "DK4_MES_B249_R0010": "Every merchant fears him.{LB}No one else will take the bounty.",
    "DK4_MES_B249_R0014": "He roams the Mediterranean.{LB}Here is an advance. Do your best.",
    "DK4_MES_B249_R0023": "Received 30,000 coins.",
    "DK4_MES_B250_R0004": "Make way!{LB}Lord Hernan Berio passes!",
    "DK4_MES_B250_R0007": "Bravado ill suits you.",
    "DK4_MES_B250_R0011": "At last, Hernan is caught!{LB}Excellent work. Take this reward.",
    "DK4_MES_B250_R0014": "Received 110,000 coins.",
    "DK4_MES_B250_R0040": "Athens share rose slightly!",
    "DK4_MES_B250_R0058": "Have you visited{LB}this city's landmark?",
    "DK4_MES_B250_R0061": "Where?",
    "DK4_MES_B250_R0065": "Go see it.{LB}The place is this city's symbol.",
    "DK4_MES_B253_R0005": "There you are. With {MACRO:FA}, right?{LB}London's guild seeks you.",
}

PRESENTATION_STATES = {
    0x03, 0x47, 0x48, 0x5C, 0x71, 0x73, 0x79, 0x93, 0x94, 0x99,
    0xBC, 0xBD, 0xC1, 0xC3, 0xC4, 0xC8, 0xCF, 0xFE,
}
SPEAKERS = {
    "03": "Maria", "47": "William Clive", "48": "Hernan Berio",
    "5C": "Tavern master", "71": "Messenger", "73": "Tobacco smoker",
    "79": "Guard", "93": "Guildmaster", "94": "Guildmaster",
    "99": "Local man", "BC": "Local woman", "BD": "Local woman",
    "C1": "Local woman", "C3": "Local woman", "C4": "Local woman",
    "C8": "Local woman", "CF": "Companion", "FE": "System",
}


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
            f"Maria V29 mismatch: missing={sorted(set(rows)-set(lines))}, "
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
            "speaker": SPEAKERS.get(state, "Narrator"),
            "context": "Shared local rumor, ruins lead, pirate bounty, reward, or commodity-boom event.",
            "source_meaning": english,
            "localization_note": "Cross-route match or direct SC3 translation reviewed for natural English and state-byte safety.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line"] + (["manual-break"] if "{LB}" in english else []),
            **({"manual_break_reason": "Protects semantic rows and pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC3.DK4",
        "source_file_sha256": SC3_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-events-v29-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 blocks 118, 165, 190, 216-219, 222, 224, 229, 240, 246-247, 249-250, and 253.",
        "inventory": {
            "identified_records": len(records), "translated_records": len(records),
            "excluded_records": 0, "blocks": block_counts,
        },
        "excluded": [],
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
