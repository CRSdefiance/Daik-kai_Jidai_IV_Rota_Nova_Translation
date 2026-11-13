from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v26.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

# Clean-source meaning precedes each en-US line. Capital I and F are runtime
# macro bytes in this renderer and may not appear as literal English glyphs.
LINES = {
    "DK4_MES_B105_R0005": ("Wow, it's so big!", "Whoa, it's huge!"),
    "DK4_MES_B105_R0010": ("Answer my question.", "Answer me."),
    "DK4_MES_B105_R0014": ("Eek! Who is that?", "Ah! Who's there?!"),
    "DK4_MES_B105_R0020": (
        "I ask you: What animal has four legs in the morning, two at midday, and three in the evening?",
        "Dawn: four legs. Noon: two. Dusk: three. What animal?",
    ),
    "DK4_MES_B105_R0027": ("I know.", "Know it"),
    "DK4_MES_B105_R0029": ("I don't know.", "No clue"),
    "DK4_MES_B105_R0031": ("There is no such animal.", "No such beast"),
    "DK4_MES_B105_R0043": ("Fool! Be gone!", "Begone, fool!"),
    "DK4_MES_B105_R0047": ("Aah!", "Aah!"),
    "DK4_MES_B105_R0059": ("Fool! Be gone!", "Begone, fool!"),
    "DK4_MES_B105_R0063": ("Aah!", "Aah!"),
    "DK4_MES_B105_R0076": ("Well then, what is the animal?", "Name the animal."),
    "DK4_MES_B105_R0083": ("Ourselves: humans.", "Humans"),
    "DK4_MES_B105_R0085": ("You, the Sphinx.", "You"),
    "DK4_MES_B105_R0087": ("Something else.", "Other"),
    "DK4_MES_B105_R0099": ("Fool! Be gone!", "Begone, fool!"),
    "DK4_MES_B105_R0103": ("Aah!", "Aah!"),
    "DK4_MES_B105_R0115": ("Fool! Be gone!", "Begone, fool!"),
    "DK4_MES_B105_R0119": ("Aah!", "Aah!"),
    "DK4_MES_B105_R0132": (
        "This worn-out question bores me... I shall ask another.",
        "That old riddle bores me... Here's one more.",
    ),
    "DK4_MES_B105_R0135": ("Aw, that's cheating!", "No fair!"),
    "DK4_MES_B105_R0143": (
        "There are ten people here, adults and babies. Together, 32 hands and feet touch the floor. How many babies are there?",
        "Ten people, including babies, have 32 hands and feet on the floor. How many babies?",
    ),
    "DK4_MES_B105_R0149": ("Four babies.", "4"),
    "DK4_MES_B105_R0151": ("Five babies.", "5"),
    "DK4_MES_B105_R0153": ("Six babies.", "6"),
    "DK4_MES_B105_R0163": ("Fool! Be gone!", "Begone, fool!"),
    "DK4_MES_B105_R0167": ("Aah!", "Aah!"),
    "DK4_MES_B105_R0179": ("Fool! Be gone!", "Begone, fool!"),
    "DK4_MES_B105_R0183": ("Aah!", "Aah!"),
    "DK4_MES_B105_R0198": ("Um...", "Um..."),
    "DK4_MES_B105_R0213": (
        "Lil, calm down. First calculate how many feet are touching the floor.",
        "{MACRO:FI}, calm down. Count the feet on the floor first.",
    ),
    "DK4_MES_B105_R0220": (
        "Ten people have twenty feet... right?",
        "Ten people have 20 feet, right?",
    ),
    "DK4_MES_B105_R0231": (
        "Subtract those twenty feet from thirty-two...",
        "Take 20 feet from 32...",
    ),
    "DK4_MES_B105_R0238": (
        "That means twelve hands are touching the floor... I know! There are six babies!",
        "There are 12 hands on the floor... Six babies!",
    ),
    "DK4_MES_B105_R0250": ("Amazing!", "Wow!"),
    "DK4_MES_B105_R0259": ("Wise one! Accept this reward!", "Wise one! Take this reward!"),
}

SPEAKERS = {0x02: "Lil Argot", 0x09: "Kamil", 0xCF: "Lil's party", 0xFE: "Sphinx"}
NOTES = {
    "DK4_MES_B105_R0020": "Uses the familiar riddle cadence without inventing a creature.",
    "DK4_MES_B105_R0143": "Thirty-two counts only hands and feet touching the floor, not every limb.",
    "DK4_MES_B105_R0213": "FI expands to Lil's name in this route; preserves the runtime name macro.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    records = []
    for row_id, (source_meaning, english) in LINES.items():
        row = source_rows[row_id]
        lead = int(row["source_hex"][:2], 16)
        literal = english.replace("{MACRO:FI}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: uppercase runtime macro byte in literal English")
        if lead not in SPEAKERS and lead not in {0x82, 0x8E, 0x92}:
            raise ValueError(f"{row_id}: unmapped source lead {lead:02X}")
        records.append(
            {
                "id": row_id,
                "english": (f"{{SPEAKER:{lead:02X}}}" if lead in SPEAKERS else "")
                + english
                + "{PAD}",
                "speaker": SPEAKERS.get(lead, "Choice"),
                "context": "Lil and Kamil answer the Sphinx's two riddles in the temple.",
                "source_meaning": source_meaning,
                "localization_note": NOTES.get(
                    row_id,
                    "Reviewed against the clean Japanese and the full Sphinx question-and-answer sequence.",
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
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v26-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Lil and Kamil answer both Sphinx riddles in SC2 B105.",
        "excluded_records": {},
        "inventory": {
            "identified_records": len(LINES),
            "translated_records": len(records),
            "blocks": {"105": len(records)},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
