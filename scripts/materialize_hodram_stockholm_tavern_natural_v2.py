from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_stockholm_tavern_natural_v2_sc1_b134.json")
SC1_SHA256 = "33981b27375cca1b9293752662d0dedb820dd310526c9dbe0612a397f38313ab"

LINES = {
    "DK4_MES_B134_R0005": (
        "Hodram Bergstrom",
        "Hey, Gerhard.",
        "Hodram greets Gerhard when the player enters Stockholm's tavern.",
        "Hodram gives Gerhard a casual greeting.",
        "Uses Gerhard's established name and a brief, familiar greeting.",
    ),
    "DK4_MES_B134_R0009": (
        "Gerhard Ardelknatts",
        "Perfect timing, Admiral. Some men were wounded, so we're recruiting sailors. Your orders?",
        "Gerhard reports the crew shortage and asks Hodram how to proceed.",
        "Gerhard says the admiral arrived at a good time: casualties have led him to recruit sailors, and he asks for instructions.",
        "Condenses the polite request into a crisp officer's report without losing the cause or request for orders.",
    ),
    "DK4_MES_B134_R0015": (
        "Hodram Bergstrom",
        "All right.",
        "Hodram approves taking direct control of sailor recruitment.",
        "Hodram agrees to proceed.",
        "A natural affirmative that exactly fills the choice record's ten-byte allocation.",
    ),
    "DK4_MES_B134_R0017": (
        "Hodram Bergstrom",
        "You handle it.",
        "Hodram delegates sailor recruitment to Gerhard.",
        "Hodram tells Gerhard to take care of it.",
        "A direct delegation that exactly fills the choice record's fourteen-byte allocation.",
    ),
    "DK4_MES_B134_R0025": (
        "Gerhard Ardelknatts",
        "Buy the patrons a round and men looking for work will gather. Then you can recruit sailors quickly.",
        "Gerhard explains the tavern's sailor-recruitment mechanic after Hodram chooses to handle it.",
        "Gerhard explains that buying drinks attracts people looking for work, after which sailors can be recruited efficiently.",
        "Localizes the mechanic as buying the patrons a round and keeps the sequence of attracting workers before recruiting them.",
    ),
    "DK4_MES_B134_R0028": (
        "Tutorial narration",
        "Hire extra sailors for boarding. More sailors shorten fleet range, so be careful.",
        "The tutorial explains the tradeoff between boarding strength and sailing range.",
        "The tutorial advises hiring more sailors for a boarding-focused strategy, but warns that doing so reduces fleet endurance.",
        "Uses boarding actions and fleet range as concise, player-facing nautical terms.",
    ),
    "DK4_MES_B134_R0033": (
        "Gerhard Ardelknatts",
        "Understood. Leave it to me.",
        "Gerhard accepts the task after Hodram delegates recruitment.",
        "Gerhard acknowledges Hodram and asks him to leave the work in Gerhard's hands.",
        "A confident, natural acknowledgement suitable for Hodram's dependable officer.",
    ),
}

SPEAKER_TOKENS = {
    "DK4_MES_B134_R0005": "01",
    "DK4_MES_B134_R0009": "10",
    "DK4_MES_B134_R0025": "10",
    "DK4_MES_B134_R0028": "FE",
    "DK4_MES_B134_R0033": "10",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = {
            row["id"]: row
            for row in csv.DictReader(stream)
            if row["id"].startswith("DK4_MES_B134_")
        }

    if set(rows) != set(LINES):
        raise SystemExit(
            f"Stockholm tavern inventory mismatch: missing={sorted(set(rows) - set(LINES))}, "
            f"extra={sorted(set(LINES) - set(rows))}"
        )

    records = []
    for row_id, (speaker, english, context, source_meaning, note) in LINES.items():
        token = SPEAKER_TOKENS.get(row_id, "")
        prefix = f"{{SPEAKER:{token}}}" if token else ""
        records.append(
            {
                "id": row_id,
                "english": f"{prefix}{english}{{PAD}}",
                "speaker": speaker,
                "context": context,
                "source_meaning": source_meaning,
                "localization_note": note,
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
        "file_path": "/data/SC1.DK4",
        "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "hodram-story-probe",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": [
            "source",
            "context",
            "localization",
            "naturalness",
            "formatting",
        ],
        "scope": "Hodram's first Stockholm tavern sailor-recruitment tutorial (SC1 block 134)",
        "profile_note": "Fixed-allocation companion layer to the existing Hodram opening probe. States 0x01, 0x10, and 0xFE are reused only within the same SC1 route profile; runtime confirmation remains required.",
        "inventory": {"block": 134, "identified_records": 7, "translated_records": 7},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} Stockholm tavern records")


if __name__ == "__main__":
    main()
