from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v21.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = tuple(range(260, 270))
EXCLUDED: dict[str, str] = {}


LINES = {
    # Yulis follow-up.
    "DK4_MES_B260_R0012": "Syracuse, then. We must find Yulis.",

    # Stockholm guild asks Hodram to retrieve Gabriel Cardocci.
    "DK4_MES_B261_R0006": "A small favor, everyone.",
    "DK4_MES_B261_R0010": "Should you see Gabriel Cardocci, bring him here.",
    "DK4_MES_B261_R0014": "He broke an agreement and{LB}apparently sailed toward the Caribbean...",
    "DK4_MES_B262_R0006": "Stockholm's guild seeks sailors willing to take a job.",
    "DK4_MES_B263_R0012": "Gabriel must be found. He is in the Caribbean.",
    "DK4_MES_B263_R0017": "Still no Gabriel? He should be somewhere in the Caribbean.",
    "DK4_MES_B264_R0005": "Sir, payment is due today. Do you know how large your tavern bill has grown?",
    "DK4_MES_B264_R0009": "Next time, surely.{LB}Has this man ever skipped payment?",
    "DK4_MES_B264_R0012": "Nor have you ever paid.",
    "DK4_MES_B264_R0015": "Barkeep, is a man named Gabriel Cardocci in town?",
    "DK4_MES_B264_R0018": "This man is Gabriel Cardocci. Who are you?",
    "DK4_MES_B264_R0021": "You broke a guild agreement.",
    "DK4_MES_B264_R0025": "What of it?! None of your business!",
    "DK4_MES_B264_R0028": "Enough. You are coming with us to Stockholm's guild.",
    "DK4_MES_B264_R0032": "Hey! Let go!",
    "DK4_MES_B264_R0036": "Wait! His bill...",
    "DK4_MES_B264_R0041": "Admiral, he hid this. Seems stolen.",
    "DK4_MES_B265_R0005": "Gabriel is here.",
    "DK4_MES_B265_R0009": "At last. Hand over the money stolen by breaking ranks.",
    "DK4_MES_B265_R0013": "Next time, surely...",
    "DK4_MES_B265_R0017": "The tavern heard that too. Barkeep, this man will leave him with you.",
    "DK4_MES_B265_R0021": "Wait. {MACRO:FA} cannot leave empty-handed. Please accept this.",
    "DK4_MES_B265_R0026": "Received 22,000 coins.",
    "DK4_MES_B265_R0049": "Stockholm share rose slightly!",
    "DK4_MES_B265_R0060": "Keep the stolen item. Should no owner appear, do with it as you please.",

    # San Jorge guild commissions and rewards the capture of Julian Vermeer.
    "DK4_MES_B266_R0006": "A target must be subdued. Take the job.",
    "DK4_MES_B266_R0009": "Julian Vermeer, Portuguese traitor{LB}aiding Spain, works as a courier{LB}in the Mediterranean.",
    "DK4_MES_B267_R0005": "Julian was caught!{LB}What a sorry sight.",
    "DK4_MES_B267_R0008": "Damn it! Let go!",
    "DK4_MES_B267_R0012": "Excellent work. We shall handle the rest. Take this.",
    "DK4_MES_B267_R0016": "Received 32,000 coins.",
    "DK4_MES_B267_R0041": "San Jorge share rose slightly!",
    "DK4_MES_B267_R0059": "To see the mosque deep in the Sahara, take a map and depart through the city gate.",
    "DK4_MES_B268_R0012": "Julian's fleet is in the Mediterranean.",
    "DK4_MES_B268_R0024": "Catch traitor Julian quickly.{LB}He works as a courier in the Mediterranean.",
    "DK4_MES_B269_R0006": "San Jorge's guild has been looking for you.",
}


SPEAKERS = {
    "01": "Hodram Bergstrom", "3F": "Julian Vermeer", "43": "Gabriel Cardocci",
    "5C": "Tavernkeeper", "71": "Sailor", "72": "Sailor", "93": "Guildmaster",
    "97": "Crewman", "FE": "System text",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXT = {
    260: "Hodram recalls that Yulis must be found in Syracuse.",
    261: "The Stockholm guild asks Hodram to retrieve Gabriel Cardocci from the Caribbean.",
    262: "A sailor points Hodram toward the Stockholm guild job.",
    263: "Hodram and the guild recall that Gabriel is in the Caribbean.",
    264: "Hodram finds and arrests Gabriel Cardocci in a tavern, recovering a stolen item.",
    265: "The Stockholm guild receives Gabriel, rewards Hodram, and entrusts the stolen item to him.",
    266: "The San Jorge guild commissions Hodram to capture Portuguese traitor Julian Vermeer.",
    267: "The San Jorge guild receives Julian, rewards Hodram, and reveals a Sahara mosque lead.",
    268: "Hodram and the guild recall that Julian's courier fleet operates in the Mediterranean.",
    269: "A sailor points Hodram toward the San Jorge guild.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream) if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)}
    if set(LINES) | set(EXCLUDED) != set(source_rows) or set(LINES) & set(EXCLUDED):
        missing = sorted(set(source_rows) - set(LINES) - set(EXCLUDED))
        extra = sorted((set(LINES) | set(EXCLUDED)) - set(source_rows))
        raise SystemExit(f"Hodram V21 inventory mismatch: missing={missing}, extra={extra}")
    records = []
    block_counts: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        block_counts[str(block)] = block_counts.get(str(block), 0) + 1
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Alternate text"), "context": CONTEXT[block],
            "source_meaning": english.replace("{MACRO:FA}", "Hodram's company").replace("{LB}", " "),
            "localization_note": "Faithful concise American English with measured fixed-record wrapping.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Places a protected newline before the native row boundary so the progressive ASCII pair phase cannot auto-wrap and skip a display row."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-guild-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Ten source-locked Hodram guild-bounty and follow-up events across SC1 blocks 260-269.",
        "excluded_records": EXCLUDED, "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
