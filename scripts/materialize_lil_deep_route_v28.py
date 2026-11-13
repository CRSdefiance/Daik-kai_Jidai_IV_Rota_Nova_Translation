from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v28.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
NON_PROSE_ID = "DK4_MES_B107_R0003"
NON_PROSE_HEX = "10469480"

LINES = {
    "DK4_MES_B107_R0006": ("Traveler...", "Guest."),
    "DK4_MES_B107_R0010": ("Eek! What is happening?!", "Ah! What's happening?!"),
    "DK4_MES_B107_R0014": ("Fulfill my wish.", "Grant my wish."),
    "DK4_MES_B107_R0018": ("Who is that?!", "Who?!"),
    "DK4_MES_B107_R0022": (
        "I wear dazzling gold like the sun and pale silver like moonlight.",
        "Gold shines on me like the sun, and silver like the moon.",
    ),
    "DK4_MES_B107_R0026": (
        "Yet I know nothing of starlight. Adorn me purely like a new star. Adorn me purely like a new star.",
        "Yet starlight is missing. Make me shine like a pure new star. Make me shine like a pure new star.",
    ),
    "DK4_MES_B107_R0034": ("Eek!", "Aaah!"),
    "DK4_MES_B107_R0038": ("What? What did that mean?", "What? What does that mean?"),
    "DK4_MES_B107_R0047": (
        "What? I have no idea what that was about...",
        "Huh? No clue...",
    ),
    "DK4_MES_B107_R0050": (
        "I do not understand a word of what it said!",
        "What was it even saying?!",
    ),
    "DK4_MES_B107_R0053": (
        "At times like this, I wish Kamil were here...",
        "(Wish Kamil were here...)"),
    "DK4_MES_B107_R0059": (
        "'Adorn me purely like a new star'? If it says adorn, perhaps it wants an ornament, like jewelry.",
        "A pure new star? Something ornamental... maybe jewelry.",
    ),
    "DK4_MES_B107_R0062": ("An ornament?", "Jewelry?"),
    "DK4_MES_B107_R0066": ("Gems or precious metals...", "Gems or gold..."),
    "DK4_MES_B107_R0070": (
        "But that covers far too much! I have no idea what to bring!",
        "That's too broad! How would we know what to bring?",
    ),
    "DK4_MES_B107_R0074": ("This is difficult...", "Tricky..."),
}

SPEAKERS = {0x02: "Lil Argot", 0x09: "Kamil", 0x97: "Sailor", 0xFE: "Temple voice"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    if source_rows[NON_PROSE_ID]["source_hex"] != NON_PROSE_HEX:
        raise ValueError("B107 opening control fragment changed; review before excluding")
    records = []
    for row_id, (source_meaning, english) in LINES.items():
        row = source_rows[row_id]
        lead = int(row["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unmapped lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: uppercase renderer macro byte in English")
        records.append(
            {
                "id": row_id,
                "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
                "speaker": SPEAKERS[lead],
                "context": (
                    "An unseen temple voice describes gold, silver, and a missing star ornament; "
                    "Lil, Kamil, and a sailor puzzle over the clue."
                ),
                "source_meaning": source_meaning,
                "localization_note": (
                    "The deliberate repeated star request is retained."
                    if row_id == "DK4_MES_B107_R0026"
                    else "Reviewed against the clean Japanese and adjacent clue dialogue."
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
        "dialogue_profile": "lil-story-deep-route-v27-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Lil's temple star-ornament clue and party responses in SC2 B107.",
        "excluded_records": {
            NON_PROSE_ID: (
                "Unmapped four-byte 10 46 94 80 opening control fragment with no "
                "coherent prose; retained byte-identical pending runtime mapping."
            )
        },
        "inventory": {
            "identified_records": len(LINES) + 1,
            "translated_records": len(records),
            "blocks": {"107": len(records)},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records and one exclusion")


if __name__ == "__main__":
    main()
