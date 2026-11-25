from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v91.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("A mysterious woman calls out to a handsome man.", "You there, handsome."),
    9: ("Ian asks whether she means him.", "Me?"),
    14: ("She offers him a book for 8,500 coins.", "Buy this book for 8,500 coins?"),
    17: ("Ian asks what sort of book it is.", "What book?"),
    21: ("She describes an Indian classic about a celestial maiden and sage in love.",
         "A Hindustani romance of a celestial maiden and sage."),
    24: ("Ian asks the admiral what to do.", "Admiral, what now?"),
    31: ("Choose to buy the book.", "Buy it"),
    33: ("Choose not to buy the book.", "Pass"),
    35: ("Leave the decision to Ian.", "Trust"),
    45: ("Ian agrees to accept the book.", "We'll take it."),
    49: ("The woman hopes Ian will fall in love with a celestial maiden.", "May a celestial maiden love you."),
    53: ("Ian says he has no interest.", "No thanks. No interest."),
    57: ("She laments that such a handsome man is uninterested.", "Oh dear. Such a handsome man, too."),
    64: ("Ian declines politely.", "No, thank you."),
    68: ("She says she will find another buyer.", "A shame. Someone else can buy it."),
    74: ("Ian would like to help but cannot afford the book.", "Would love to, but can't afford it."),
    77: ("The woman acknowledges his lack of money.", "Oh."),
    81: ("Ian apologizes for disappointing her.", "Sorry to disappoint you."),
    85: ("The woman decides to give him the book.", "Then take it."),
    89: ("Ian is startled by the gift.", "What?!"),
    93: ("She hopes to love a man like Ian someday.", "Hee hee... Someday, a man like you will be mine."),
    97: ("Ian sees that she has disappeared.", "Vanished..."),
    101: ("Ian wonders whether she was a celestial maiden, then dismisses the thought.",
          "A celestial maiden? Hah! What nonsense."),
    109: ("The system announces Ian's charm rose by one.", "His charm rose by 1!"),
}
EXCLUDED = {
    "DK4_MES_B197_R0022": (
        "Four-byte 21 48 8C A8 packed portrait/scene payload, correlated with "
        "the same nontext event in Hodram SC1 B201; leave unchanged."
    ),
}
SPEAKERS = {0xA9: "Mysterious woman", 0x15: "Ian Dukov", 0xFE: "System notice"}
CHOICES = {31, 33, 35}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B197_")}
    authored = {f"DK4_MES_B197_R{number:04d}" for number in LINES}
    if authored | EXCLUDED.keys() != expected or authored & EXCLUDED.keys():
        raise ValueError(f"B197 coverage mismatch: missing {expected - authored - EXCLUDED.keys()}")
    if source_rows["DK4_MES_B197_R0022"]["source_hex"].upper() != "21488CA8":
        raise ValueError("B197 packed event payload changed")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B197_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if number in CHOICES:
            if lead != 0x94:
                raise ValueError(f"{row_id}: choice has unexpected Shift-JIS lead {lead:02X}")
            prefix, speaker = "", "Purchase choice"
        else:
            if lead not in SPEAKERS:
                raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
            prefix, speaker = f"{{SPEAKER:{lead:02X}}}", SPEAKERS[lead]
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{prefix}{english}{{PAD}}",
            "speaker": speaker,
            "context": "Ian meets a mysterious woman selling an Indian celestial-maiden romance.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B197 Japanese. Choice-leading 94 is Shift-JIS "
                "text. The four-byte portrait payload stays unchanged. Literal "
                "uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v91-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "24 B197 Ian and celestial-maiden text records; one packed event payload excluded unchanged.",
        "inventory": {"identified_records": 25, "translated_records": 24, "blocks": {"197": 24}},
        "excluded_records": EXCLUDED, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records; {len(EXCLUDED)} exclusion")


if __name__ == "__main__":
    main()
