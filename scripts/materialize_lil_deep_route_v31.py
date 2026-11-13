from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v31.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
NON_PROSE_ID = "DK4_MES_B112_R0010"
NON_PROSE_HEX = "468F8080431E63"

LINES = {
    "DK4_MES_B112_R0006": ("Let's go back.", "Let's go back."),
    "DK4_MES_B112_R0029": (
        "Hm? There's someone on the sandbar.",
        "Look! On the sandbar!",
    ),
    "DK4_MES_B112_R0031": (
        "Someone is on the sandbar.",
        "Someone's there!",
    ),
    "DK4_MES_B112_R0033": (
        "Hm? Someone is on the sandbar.",
        "Hm? Someone's there!",
    ),
    "DK4_MES_B112_R0035": (
        "Oh? Someone's there.",
        "Someone's there!",
    ),
    "DK4_MES_B112_R0039": ("What's wrong?", "What's wrong?"),
    "DK4_MES_B112_R0043": (
        "Traveler, you came at a good time! Please save my grandson!",
        "Thank heavens you're here! Save my grandson!",
    ),
    "DK4_MES_B112_R0046": ("Your grandson?", "Boy?"),
    "DK4_MES_B112_R0050": ("Grandpa!", "Grandpa! Help!"),
    "DK4_MES_B112_R0054": ("A boy is drowning!", "A boy's drowning!"),
    "DK4_MES_B112_R0069": ("Leave it to me!", "Leave it to me!"),
    "DK4_MES_B112_R0071": ("Leave it to me!", "On it!"),
    "DK4_MES_B112_R0073": ("Let me go!", "Let me!"),
    "DK4_MES_B112_R0075": ("Leave it to me!", "Got it!"),
    "DK4_MES_B112_R0077": ("Leave this to me!", "Leave this to me!"),
    "DK4_MES_B112_R0079": ("Let me go!", "Let me go!"),
    "DK4_MES_B112_R0083": ("That was scary!", "That was scary!"),
    "DK4_MES_B112_R0087": (
        "You're safe now! Thank goodness!",
        "You're safe now! Thank goodness!",
    ),
    "DK4_MES_B112_R0090": (
        "Traveler, thank you so very much!",
        "Thank you! Thank you so much!",
    ),
    "DK4_MES_B112_R0093": (
        "I'm glad the boy is safe!",
        "Glad the boy's safe!",
    ),
    "DK4_MES_B112_R0096": (
        "I have nothing to give you... Oh, wait here a moment!",
        "There's nothing to give you... Oh! Wait here!",
    ),
    "DK4_MES_B112_R0100": ("Please take this.", "Please, take this."),
    "DK4_MES_B112_R0104": ("What is it?", "What?"),
    "DK4_MES_B112_R0108": (
        "When I was young, the governor gave me this as a reward for defeating the bandits who lived nearby.",
        "The governor gave me this years ago for driving bandits from here.",
    ),
    "DK4_MES_B112_R0111": (
        "I don't know its origin, but I've heard it's quite valuable.",
        "The origin is a mystery, but they say it is valuable.",
    ),
    "DK4_MES_B112_R0115": (
        "But you should keep it as a memento, sir.",
        "But you should keep it as a memento.",
    ),
    "DK4_MES_B112_R0119": (
        "I can't let the person who saved my grandson leave empty-handed. Please don't worry. It has no value sitting with me.",
        "No, no! You saved my grandson. Please take it. Keeping it means nothing to me.",
    ),
    "DK4_MES_B112_R0122": ("...Thank you.", "Thank you..."),
    "DK4_MES_B112_R0128": ("Safe travels, traveler.", "Safe travels."),
    "DK4_MES_B112_R0132": ("Bye-bye, miss!", "Bye-bye!"),
}

SPEAKERS = {
    0x02: "Lil Argot",
    0xA3: "Boy",
    0xAA: "Grandfather",
    0xD0: "Selected crewmate",
    0xD6: "Lookout",
    0xD7: "Rescuer",
}
TEXT_LEADS = {0x81, 0x82, 0x8E, 0x94}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    if source_rows[NON_PROSE_ID]["source_hex"] != NON_PROSE_HEX:
        raise ValueError("B112 seven-byte scene fragment changed; review before excluding")
    records = []
    for row_id, (source_meaning, english) in LINES.items():
        row = source_rows[row_id]
        lead = int(row["source_hex"][:2], 16)
        if lead not in SPEAKERS and lead not in TEXT_LEADS:
            raise ValueError(f"{row_id}: unmapped lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: uppercase renderer macro byte in English")
        records.append(
            {
                "id": row_id,
                "english": (f"{{SPEAKER:{lead:02X}}}" if lead in SPEAKERS else "")
                + english
                + "{PAD}",
                "speaker": SPEAKERS.get(lead, "Companion variant"),
                "context": (
                    "Lil's party rescues a boy from a sandbar. His grandfather "
                    "gives them a valuable object as thanks."
                ),
                "source_meaning": source_meaning,
                "localization_note": (
                    "Reviewed against clean Japanese and matching rescue-scene "
                    "source in the other routes; kinship is explicit only for "
                    "the boy and his grandfather."
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
        "dialogue_profile": "lil-story-deep-route-v31-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Lil's sandbar rescue and the grandfather's reward in SC2 B112.",
        "excluded_records": {
            NON_PROSE_ID: (
                "Unmapped seven-byte 46 8F 80 80 43 1E 63 scene fragment with no "
                "coherent prose; retain byte-identical pending runtime mapping."
            )
        },
        "inventory": {
            "identified_records": len(LINES) + 1,
            "translated_records": len(records),
            "blocks": {"112": len(records)},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records and one exclusion")


if __name__ == "__main__":
    main()
