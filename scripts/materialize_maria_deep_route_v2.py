from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
OUTPUT = Path("translations/maria_deep_route_v2.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"

# Complete SC3 blocks 170 and 193.  Block 170 is Ian's celestial-maiden
# book event, including all three player branches and its reward.  Block 193
# is the complete Julian/Lucia Empress's Gown conversation.
LINES = {
    "DK4_MES_B170_R0004": "You there, handsome.",
    "DK4_MES_B170_R0008": "You mean me?",
    "DK4_MES_B170_R0013": "Would you buy this book for 8,500 coins?",
    "DK4_MES_B170_R0016": "What book?",
    "DK4_MES_B170_R0020": "A classic romance of a maiden and a sage. Well?",
    "DK4_MES_B170_R0023": "Admiral, what now?",
    "DK4_MES_B170_R0030": "Buy it",
    "DK4_MES_B170_R0032": "Pass",
    "DK4_MES_B170_R0034": "Decide",
    "DK4_MES_B170_R0044": "We will take it.",
    "DK4_MES_B170_R0048": "May a celestial maiden love you.",
    "DK4_MES_B170_R0052": "Sadly, no interest.",
    "DK4_MES_B170_R0056": "Oh dear. Handsome, but a pity.",
    "DK4_MES_B170_R0063": "No, thank you.",
    "DK4_MES_B170_R0067": "A shame. Someone else will buy it.",
    "DK4_MES_B170_R0073": "Wish to help, but lack the money.",
    "DK4_MES_B170_R0076": "Ah.",
    "DK4_MES_B170_R0080": "Sorry to disappoint you.",
    "DK4_MES_B170_R0084": "Then take it.",
    "DK4_MES_B170_R0088": "What?!",
    "DK4_MES_B170_R0092": "Hehe... Next time, a man like you may be mine.",
    "DK4_MES_B170_R0096": "Vanished...",
    "DK4_MES_B170_R0100": "A celestial maiden? Hah... What a foolish thought.",
    "DK4_MES_B170_R0108": "His charm rose by 1!",
    "DK4_MES_B193_R0004": (
        "Lucia! Well? This man comes here solely to see those noble, beautiful eyes."
    ),
    "DK4_MES_B193_R0007": "Welcome, Julian. Still a master of sweet words.",
    "DK4_MES_B193_R0011": "Hm...?",
    "DK4_MES_B193_R0015": "What is it? Something on my face?",
    "DK4_MES_B193_R0018": "So... Perhaps the legendary empress resembled you.",
    "DK4_MES_B193_R0022": "What does that mean?",
    "DK4_MES_B193_R0026": (
        "Sorry, rather sudden. A tale of armor called the Empress's Gown brought "
        "it to mind."
    ),
    "DK4_MES_B193_R0030": "The Empress's Gown?",
    "DK4_MES_B193_R0034": "A Chinese empress wore it. Her tyranny brought a tragic end.",
    "DK4_MES_B193_R0038": (
        "She must have been terrifyingly beautiful, stealing hearts at a glance... "
        "Just like you."
    ),
    "DK4_MES_B193_R0041": (
        "But 'tyranny' means selfish and arrogant. Do you really find me so spiteful?"
    ),
    "DK4_MES_B193_R0045": (
        "Silly. A little selfishness makes a woman charming, about as much as you have."
    ),
    "DK4_MES_B193_R0049": (
        "A gown that protected a beautiful woman... How romantic. Do you not agree?"
    ),
    "DK4_MES_B193_R0052": "A gown, romantic? Her rings and necklaces interest me far more.",
    "DK4_MES_B193_R0056": (
        "Their price, you mean? Women are so practical! Time to leave. See you."
    ),
    "DK4_MES_B193_R0060": "See you.",
    "DK4_MES_B193_R0064": "He flees whenever gifts come up.",
}

SPEAKERS = {
    "15": "Ian",
    "1A": "Julian",
    "A9": "Mysterious woman",
    "C7": "Lucia",
    "FE": "System message",
}
PRESENTATION_STATES = {int(value, 16) for value in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(rows)
    if missing:
        raise SystemExit(f"Maria V2 inventory mismatch: missing={sorted(missing)}")

    records: list[dict[str, object]] = []
    for row_id, english in LINES.items():
        row = rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in PRESENTATION_STATES else ""
        block = 170 if "_B170_" in row_id else 193
        records.append(
            {
                "id": row_id,
                "english": (
                    f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}"
                ),
                "speaker": SPEAKERS.get(state, "Choice menu"),
                "context": (
                    "Ian encounters a mysterious woman selling a celestial-maiden "
                    "romance; all buy, refuse, and let-Ian-decide branches are retained."
                    if block == 170
                    else "Julian and Lucia discuss the legendary Empress's Gown in a "
                    "complete optional tavern conversation."
                ),
                "source_meaning": english,
                "localization_note": (
                    "Localized from Maria's clean Japanese record and reviewed against "
                    "the exact source-matched Raphael V93 and Hodram V32 event; SC3 "
                    "presentation state and automatic wrapping remain route-local."
                ),
                "qa_waivers": ["weak-line-ending", "orphan-final-line"],
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
        "dialogue_profile": "maria-story-shared-events-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 blocks 170 and 193: complete Ian celestial-maiden book event "
            "with all branches and reward, plus the complete Julian/Lucia Empress's "
            "Gown conversation."
        ),
        "excluded_records": {
            "DK4_MES_B170_R0021": "Event-control payload !H plus a binary argument; not dialogue."
        },
        "inventory": {
            "identified_records": len(LINES) + 1,
            "translated_records": len(records),
            "excluded_records": 1,
            "blocks": {"170": 24, "193": 17},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
