from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v32.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
FRAGMENTS = {
    "DK4_MES_B113_R0004": "60304693803E63",
    "DK4_MES_B113_R0025": "30488BA8",
}

LINES = {
    "DK4_MES_B113_R0019": ("Admiral, look at this!", "Admiral, look!"),
    "DK4_MES_B113_R0021": ("Admiral, look!", "Look here!"),
    "DK4_MES_B113_R0023": ("Admiral, this!", "Admiral, look!"),
    "DK4_MES_B113_R0027": (
        "Beautiful... I've never seen jade this magnificent.",
        "Wow... Never seen jade like this!",
    ),
    "DK4_MES_B113_R0038": (
        "In the New World, as in the East, jade is considered a precious gemstone.",
        "Jade is prized in the New World, just as it is in the East.",
    ),
    "DK4_MES_B113_R0041": (
        "The offering of so much jade suggests that this building had great importance.",
        "That much jade suggests this building had great importance.",
    ),
    "DK4_MES_B114_R0007": ("Hey, young lady!", "Hey, little lady!"),
    "DK4_MES_B114_R0020": (
        "I've been meaning to thank you.",
        "Been meaning to thank you.",
    ),
    "DK4_MES_B114_R0025": (
        "I told you, don't call me a little girl!",
        "Don't call me little lady!",
    ),
    "DK4_MES_B114_R0029": (
        "Sorry, sorry. I've been meaning to thank you.",
        "Sorry! Been meaning to thank you.",
    ),
    "DK4_MES_B114_R0035": (
        "Listen! Illicit dealings in slaves and drugs have dropped sharply recently!",
        "Listen! There's been far less smuggling of slaves and drugs!",
    ),
    "DK4_MES_B114_R0039": ("Wow, really?!", "Wow, really?!"),
    "DK4_MES_B114_R0043": (
        "It's surely because you brought cacao here! It's now this town's specialty.",
        "Thanks to the cacao you brought us! Now it's this town's specialty.",
    ),
    "DK4_MES_B114_R0047": (
        "Then I was useful! I'm happy for you!",
        "So it helped! That's great news!",
    ),
    "DK4_MES_B114_R0050": ("Thanks!", "Thanks!"),
    "DK4_MES_B114_R0060": (
        "I don't know if this will help, but I heard you're looking for something.",
        "Heard you're looking for something. This might help.",
    ),
    "DK4_MES_B114_R0064": (
        "We aren't supposed to tell outsiders, but there are ruins nearby, a little inland, deep in the desert.",
        "We keep this from outsiders, but nearby ruins lie a little inland, deep in the desert.",
    ),
    "DK4_MES_B114_R0067": (
        "I'll show you where the city gate is. Buy the map sold at this town's guild and visit the ruins yourself.",
        "Buy a map at our guild. The city gate is here; go visit the ruins.",
    ),
    "DK4_MES_B114_R0071": (
        "Thank you! I'll go take a look!",
        "Thanks! We'll take a look!",
    ),
}

SPEAKERS = {0x02: "Lil Argot", 0x13: "Crew scholar", 0x68: "Townsman", 0xD6: "Lookout"}
TEXT_LEADS = {0x82, 0x92}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    for row_id, raw_hex in FRAGMENTS.items():
        if source_rows[row_id]["source_hex"] != raw_hex:
            raise ValueError(f"{row_id}: non-prose fragment changed")
    records = []
    counts: Counter[str] = Counter()
    for row_id, (source_meaning, english) in LINES.items():
        row = source_rows[row_id]
        lead = int(row["source_hex"][:2], 16)
        if lead not in SPEAKERS and lead not in TEXT_LEADS:
            raise ValueError(f"{row_id}: unmapped lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: uppercase renderer macro byte in English")
        block = row_id.split("_B", 1)[1].split("_R", 1)[0]
        counts[str(int(block))] += 1
        records.append(
            {
                "id": row_id,
                "english": (f"{{SPEAKER:{lead:02X}}}" if lead in SPEAKERS else "")
                + english
                + "{PAD}",
                "speaker": SPEAKERS.get(lead, "Companion variant"),
                "context": (
                    "Lil's party discovers a jade offering and considers the ruin's importance."
                    if block == "113"
                    else "A townsman thanks Lil for introducing cacao, reports less trafficking, and reveals nearby ruins."
                ),
                "source_meaning": source_meaning,
                "localization_note": (
                    "The short companion response omits the admiral address without adding a gendered title."
                    if row_id == "DK4_MES_B113_R0021"
                    else "Reviewed against clean Japanese and adjacent dialogue for meaning and voice; "
                    "the townsman's familiar address is a diminutive that Lil rejects, not a title or relationship."
                    if block == "114"
                    else "Reviewed against clean Japanese and the connected discovery for the jade offering's meaning."
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
        "dialogue_profile": "lil-story-deep-route-v32-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Lil's jade discovery and cacao follow-up in SC2 B113-B114.",
        "excluded_records": {
            row_id: f"Non-prose scene fragment {raw_hex}; retain byte-identical pending runtime mapping."
            for row_id, raw_hex in FRAGMENTS.items()
        },
        "inventory": {
            "identified_records": len(LINES) + len(FRAGMENTS),
            "translated_records": len(records),
            "blocks": dict(counts),
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records, {len(FRAGMENTS)} exclusions")


if __name__ == "__main__":
    main()
