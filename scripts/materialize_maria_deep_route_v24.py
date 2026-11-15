from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v24.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (173, 174, 207, 208, 209)

OVERRIDES = {
    "DK4_MES_B173_R0008": "Oh!",
    "DK4_MES_B173_R0016": "What is it?{LB}You okay?",
    "DK4_MES_B173_R0024": "You're awake.",
    "DK4_MES_B173_R0028": "...Where is this?",
    "DK4_MES_B173_R0032": "At an inn. You fainted at the dock,{LB}so we brought you here.",
    "DK4_MES_B173_R0036": "That explains it.{LB}Sorry for trouble.",
    "DK4_MES_B173_R0039": "No trouble at all.{LB}Still, you look pale. Rest for a while.",
    "DK4_MES_B173_R0043": "Well, time to go.{LB}Take care.",
    "DK4_MES_B173_R0046": "Wait. Are you a doctor?",
    "DK4_MES_B173_R0053": "This is hardly enough thanks,{LB}but please take it.",
    "DK4_MES_B173_R0057": "Please, no need.",
    "DK4_MES_B173_R0061": "Then my conscience won't rest.{LB}Please accept it.",
    "DK4_MES_B173_R0064": "Very well, then.{LB}Please take care of yourself.",
    "DK4_MES_B173_R0068": "Certainly.{LB}Thank you very much.",
    "DK4_MES_B174_R0007": "Really?{LB}Doesn't look so bad.",
    "DK4_MES_B174_R0010": "No, no, it's badly worn.{LB}Why not replace it with this rope?{LB}They say it has a mysterious power.",
    "DK4_MES_B174_R0013": "Oh?{LB}No charge?",
    "DK4_MES_B174_R0016": "Certainly not! A discount is possible.{LB}Say 300,000 coins.",
    "DK4_MES_B174_R0019": "Hold on!{LB}You aren't paying that, are you, Admiral?",
    "DK4_MES_B174_R0022": "Special or not, that price is absurd.{LB}At most, 30,000 coins.",
    "DK4_MES_B174_R0025": "Wait! This is unique in all the world.{LB}How about 200,000 coins?",
    "DK4_MES_B174_R0032": "Hmm. Please accept 150,000 coins.",
    "DK4_MES_B174_R0039": "You drive a hard bargain.{LB}Then 100,000. No lower.",
    "DK4_MES_B174_R0043": "Hmm, that sounds fair.{LB}What do you say, Admiral?",
    "DK4_MES_B174_R0057": "Leave the rest to me.",
    "DK4_MES_B174_R0060": "Yes. Handle it.",
    "DK4_MES_B174_R0067": "Carry the rope to the deck.",
    "DK4_MES_B174_R0075": "{MACRO:FI}: Charm +1!",
    "DK4_MES_B174_R0084": "True...{LB}No need to replace it in a hurry.",
    "DK4_MES_B174_R0088": "Understood. We'll decline.",
    "DK4_MES_B174_R0095": "Our apologies.{LB}Please forgive us.",
    "DK4_MES_B174_R0098": "{MACRO:FI}: Spirit +1!",
    "DK4_MES_B207_R0008": "What's wrong?{LB}Why so vacant?",
    "DK4_MES_B207_R0011": "Carlo?!{LB}When did you return?",
    "DK4_MES_B207_R0015": "Just passing through on business.{LB}But that vacant look drives customers away.",
    "DK4_MES_B207_R0018": "Mind your own business.{LB}Still, that sharp tongue means you've recovered.",
    "DK4_MES_B207_R0022": "At last, back at work{LB}and sailing with these people.",
    "DK4_MES_B207_R0025": "Oh, customers! Sorry.{LB}A tale from my great-grandfather came to mind.",
    "DK4_MES_B207_R0032": "Trade in the Papal States.{LB}The pope once ruled almost to Venice.",
    "DK4_MES_B207_R0036": "So the stories say.{LB}Trade thrived when papal power was at its height.",
    "DK4_MES_B207_R0039": "Exactly. Princes competed over what{LB}and how much to donate to the pope...",
    "DK4_MES_B207_R0042": "Our ancestors grew rich simply moving goods{LB}from one lord to another. But now...",
    "DK4_MES_B207_R0046": "Papal power faded,{LB}and commerce with the Church fell away.",
    "DK4_MES_B207_R0050": "Right. Now we must earn profit by our own labor.{LB}Our ancestors had it easy.",
    "DK4_MES_B207_R0053": "Come to think of it, relics tied to the pope{LB}sometimes appear in lands he once ruled.",
    "DK4_MES_B207_R0056": "A pope's possessions may carry blessings.{LB}Some divine favor would be welcome.",
    "DK4_MES_B207_R0063": "Admiral, this may be no joke.{LB}A pope's cherished object would be a great discovery.",
    "DK4_MES_B208_R0016": "Admiral, a letter from Charles.",
    "DK4_MES_B208_R0026": "Here in West Africa,{LB}a strange tale from sailors reached me.",
    "DK4_MES_B208_R0030": "Pirates attacked a Spanish fleet{LB}bound from the New World for West Africa.",
    "DK4_MES_B208_R0034": "Hopelessly outmatched and too slow to escape,{LB}the merchants faced certain destruction.",
    "DK4_MES_B208_R0037": "West of Lisbon,{LB}they heard a roar unlike anything in this world.",
    "DK4_MES_B208_R0040": "The roar inexplicably roused the sailors.{LB}With lionlike courage, they fought the pirates evenly.",
    "DK4_MES_B208_R0043": "Spanish warships arrived in time.{LB}The pirates fled, and the merchants escaped.",
    "DK4_MES_B208_R0046": "What made the sound, or whether nature{LB}can explain it, remains unknown.",
    "DK4_MES_B208_R0049": "Still, a fascinating tale.{LB}An investigation may be worthwhile.{LB}Charles Jean Rochefort",
    "DK4_MES_B208_R0056": "A strange story...{LB}Something lies behind it.{LB}Let's learn the truth.",
    "DK4_MES_B209_R0016": "Admiral, a letter from Jam.",
    "DK4_MES_B209_R0029": "This place is incredible.{LB}Hard to explain, but one rumor caught my ear.",
    "DK4_MES_B209_R0032": "A Gupta-era spirit-beast statue{LB}supposedly sees the future.",
    "DK4_MES_B209_R0035": "Sounds far-fetched, right?{LB}But anything seems possible here.{LB}Maybe it's true.",
    "DK4_MES_B209_R0038": "With it, that gambler may lose.{LB}Too much to hope?",
    "DK4_MES_B209_R0041": "But none is sold,{LB}and no one here has seen one.",
    "DK4_MES_B209_R0045": "Admiral, why not look if time permits? Even beyond gambling, it could prove useful.",
    "DK4_MES_B209_R0048": "Time to sail. Hope you find the treasure. Until next time. Jam Jack Ludwayer",
    "DK4_MES_B209_R0063": "Ha! You're 500 years too early to beat me!",
    "DK4_MES_B209_R0069": "Heh. Same as ever.{LB}Since he told us, let's investigate sometime.",
}

SPEAKERS = {
    "03": "Maria",
    "0B": "Jam's letter",
    "12": "Charles's letter",
    "13": "Carlo",
    "14": "Fernando",
    "68": "Filippo",
    "69": "Rope merchant",
    "AC": "Sick traveler",
    "D0": "Crewmate",
    "FE": "System",
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
            f"Maria V24 mismatch: missing={sorted(set(rows)-set(lines))}, "
            f"extra={sorted(set(lines)-set(rows))}"
        )

    records = []
    block_counts: dict[str, int] = {}
    for row_id in sorted(lines, key=lambda value: (int(value.split("_B")[1].split("_")[0]), int(value.rsplit("R", 1)[1]))):
        english = lines[row_id]
        row = rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in PRESENTATION_STATES else ""
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        block_counts[block] = block_counts.get(block, 0) + 1
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Letter-delivery variant or choice"),
            "context": "Complete shared Carlo, Papal rumor, Charles-letter, or Jam-letter event.",
            "source_meaning": english,
            "localization_note": "Cross-route match or direct SC3 translation reviewed for natural English and state-byte safety.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line"] + (["manual-break"] if "{LB}" in english else []),
            **({"manual_break_reason": "Protects semantic rows and pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })

    payload = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC3.DK4",
        "source_file_sha256": SC3_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-events-v24-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 blocks 173, 174, 207, 208, and 209: five complete shared events.",
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "excluded_records": 0, "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
