from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v73.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    7: ("Julian tells Mihwa her smile is his reason to live.", "Mihwa, your smile gives me life."),
    11: ("Mihwa reacts bashfully to Julian's line.", "Oh, Julian..."),
    15: ("Lil is amazed Julian can say such a line openly.", "Wow. How can he say that out loud?"),
    18: ("Julian notices Mihwa is not smiling and fears she dislikes him.", "No smile? Do you dislike me?"),
    22: ("Mihwa says Julian usually cheers her up but she is distracted.", "No, Julian. Your words help, but..."),
    26: ("Mihwa cannot stop thinking about something she wants.", "There's something on my mind, day and night."),
    30: ("Julian asks what Mihwa wants so badly.", "Mihwa, that look doesn't suit you. What do you want so badly?"),
    34: ("Mihwa names the rare Golden Crown of Silla.", "Golden Crown of Silla. Rare and beautiful."),
    38: ("Julian fears the crown is costly and asks where to buy it.", "Sounds pricey. Where is it sold?"),
    41: ("Mihwa says it is not sold and may be in Seoul.", "No shop sells it. Word is it's somewhere in Seoul."),
    44: ("Julian realizes a likely location.", "No shop? Wait... That place!"),
    47: ("Mihwa asks whether Julian has a lead.", "You know where it is?"),
    51: ("Julian promises to obtain the crown and restore Mihwa's smile.", "Leave it to me! You'll smile again!"),
    55: ("Julian says Mihwa's smile gives him strength and asks for a date.", "Your smile keeps me going. A date when it's yours?"),
    58: ("Mihwa says Julian is getting ahead of himself but will consider it.", "Too soon! But maybe."),
    62: ("Julian is thrilled and leaves at once for Seoul.", "Yes! Remember that! Off to Seoul!"),
    65: ("Mihwa sees Julian has already run off.", "Good luck... Oh, he's gone."),
    68: ("Lil speaks up to Mihwa.", "Um..."),
    72: ("Mihwa apologizes for not noticing Lil.", "Oh, hello! Sorry, didn't see you."),
    75: ("Lil asks what the Golden Crown of Silla is.", "Overheard you. What's the Golden Crown of Silla?"),
    78: ("Mihwa remembers only that the crown is beautiful.", "Only remember that it's lovely."),
    82: ("Lil wants to see the crown herself.", "Now that sounds worth seeing."),
    85: ("Mihwa offers to show it to Lil if it is found.", "You too? Come see it once found."),
    88: ("Lil declines, intending to find the crown herself in Seoul.", "No thanks! Planning to find it myself. You said Seoul?"),
    92: ("Mihwa confirms Seoul but does not know the exact location.", "Yes, Seoul. Exact place? No idea."),
    96: ("Lil says she can ask around in Seoul.", "That's enough. We can ask around."),
    100: ("Mihwa asks Lil to show her the crown if she finds it.", "Then show me when you find it!"),
}

SPEAKERS = {0x02: "Lil Argot", 0x1A: "Julian", 0xC9: "Mihwa"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B172_")}
    authored = {f"DK4_MES_B172_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B172 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B172_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "Julian promises Mihwa the Golden Crown of Silla; Lil learns it may be in Seoul.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B172 Japanese. Source presentation "
                "leads retain their control behavior. Literal uppercase I/F "
                "are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v73-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 27 B172 Golden Crown of Silla lead records.",
        "inventory": {"identified_records": 27, "translated_records": 27, "blocks": {"172": 27}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
