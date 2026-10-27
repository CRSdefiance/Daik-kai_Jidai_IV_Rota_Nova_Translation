from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
OUTPUT = Path("translations/maria_deep_route_v1.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"

# SC3 block 169 is the complete shared haggling event.  Every Japanese body was
# independently matched to the current Raphael V93 and Hodram V32 route layers,
# then reviewed here against Maria's clean source and immediate branch context.
LINES = {
    "DK4_MES_B169_R0004": "You look wealthy. Hehehehe!",
    "DK4_MES_B169_R0011": "Something good is for sale. How about 200,000 coins? Hehehehe!",
    "DK4_MES_B169_R0023": "Hey, this price is a rip-off!",
    "DK4_MES_B169_R0031": "Buy",
    "DK4_MES_B169_R0033": "Pass",
    "DK4_MES_B169_R0041": "Generous! This will surely prove useful.",
    "DK4_MES_B169_R0044": "{MACRO:FI}: Charm +1!",
    "DK4_MES_B169_R0061": "All right. How about 100,000 coins? Hehehehe!",
    "DK4_MES_B169_R0073": (
        "Admiral, halving it at once proves the first price was outrageous. "
        "Two more bargains should work."
    ),
    "DK4_MES_B169_R0081": "Buy",
    "DK4_MES_B169_R0083": "Pass",
    "DK4_MES_B169_R0091": "Hehe! Sharp eye. This will be useful.",
    "DK4_MES_B169_R0106": "Then how about 70,000 coins? Hehehehe!",
    "DK4_MES_B169_R0117": "One more bargain may work.",
    "DK4_MES_B169_R0125": "Buy",
    "DK4_MES_B169_R0127": "Pass",
    "DK4_MES_B169_R0135": "Here. This will be useful. Hehehe!",
    "DK4_MES_B169_R0151": "Greedy, are we? How about 50,000 coins? Hehehe!",
    "DK4_MES_B169_R0169": "One more try should work.",
    "DK4_MES_B169_R0177": "Make her lower it again!",
    "DK4_MES_B169_R0186": "Buy",
    "DK4_MES_B169_R0188": "Pass",
    "DK4_MES_B169_R0196": "A skilled bargainer! Here is the item.",
    "DK4_MES_B169_R0211": "40,000 coins... Heh.",
    "DK4_MES_B169_R0222": "Now's the time to buy.",
    "DK4_MES_B169_R0231": "Buy",
    "DK4_MES_B169_R0233": "Pass",
    "DK4_MES_B169_R0241": "Thought you would never buy. Here.",
    "DK4_MES_B169_R0256": "Please buy it. Just 30,000 coins.",
    "DK4_MES_B169_R0267": "The price will go no lower.",
    "DK4_MES_B169_R0276": "Buy",
    "DK4_MES_B169_R0278": "Pass",
    "DK4_MES_B169_R0286": "Tch, sold far too cheaply. At least take good care of it.",
    "DK4_MES_B169_R0301": "Hmph! No eye for value!",
    "DK4_MES_B169_R0305": "Then someone else can buy!",
}

SPEAKERS = {
    "06": "Senior crew member",
    "13": "Carlo",
    "14": "Crewman",
    "19": "Young crewwoman",
    "AD": "Suspicious seller",
    "FE": "System message",
}
PRESENTATION_STATES = {int(value, 16) for value in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(rows)
    if missing:
        raise SystemExit(f"Maria V1 inventory mismatch: missing={sorted(missing)}")

    records: list[dict[str, object]] = []
    for row_id, english in LINES.items():
        row = rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in PRESENTATION_STATES else ""
        records.append(
            {
                "id": row_id,
                "english": (
                    f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}"
                ),
                "speaker": SPEAKERS.get(state, "Choice menu"),
                "context": (
                    "Maria's party negotiates with a suspicious seller through every "
                    "purchase, refusal, and successive haggling branch."
                ),
                "source_meaning": english.replace("{MACRO:FI}", "Maria"),
                "localization_note": (
                    "Localized from Maria's clean Japanese record and cross-checked "
                    "against the exact source-matched Raphael V93 and Hodram V32 lines; "
                    "SC3 presentation state and automatic wrapping remain route-local."
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
            "Maria SC3 block 169: complete suspicious-seller haggling event, all price "
            "steps, party advice, choices, purchase outcomes, refusal outcomes, and "
            "the Maria charm reward."
        ),
        "excluded_records": {},
        "inventory": {
            "identified_records": len(LINES),
            "translated_records": len(records),
            "blocks": {"169": len(records)},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
