from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/hodram_natural_v2_sc2_b146_blocked.json")
SC2_SHA256 = "c270e84025d6942da2dbe86ff6a0241a0874611bce0d08f80923c5fb6e75d326"

LINES = {
    "DK4_MES_B146_R0005": "Hey, where's Kamil? Didn't he come back?",
    "DK4_MES_B146_R0008": "No. Wasn't Kamil with you, Admiral?",
    "DK4_MES_B146_R0019": "Where the hell did he go?! Even I can't figure out what he's thinking...",
    "DK4_MES_B146_R0025": "Kamil... what's gotten into you?",
    "DK4_MES_B146_R0031": "Meanwhile, Kamil was...",
    "DK4_MES_B146_R0035": "Father... You haven't changed at all, have you?",
    "DK4_MES_B146_R0039": "{MACRO:FI}... What am I supposed to do?",
    "DK4_MES_B146_R0048": "Hey, you! You're white as a sheet! Is something wrong?",
    "DK4_MES_B146_R0051": "Oh! Who are you?",
    "DK4_MES_B146_R0055": "Forgive me. I'm Hodram Bergstrom.",
    "DK4_MES_B146_R0058": "Bergstrom... You mean the Bergstrom Fleet?",
    "DK4_MES_B146_R0061": "More or less.",
    "DK4_MES_B146_R0065": "Oh, forgive me. I should have introduced myself. I'm Kamil Overijssel.",
    "DK4_MES_B146_R0069": "Kamil... Are you feeling ill? Your hands are shaking.",
    "DK4_MES_B146_R0072": "No, I'm all right. It's just...",
    "DK4_MES_B146_R0077": "...! You're...",
    "DK4_MES_B146_R0081": "Oh, you're Hodram... right?",
    "DK4_MES_B146_R0085": "What a coincidence, meeting you here.",
    "DK4_MES_B146_R0089": "Yes...",
    "DK4_MES_B146_R0093": "You don't seem yourself. Is something wrong?",
    "DK4_MES_B146_R0097": "Well... sort of...",
    "DK4_MES_B146_R0101": "How's the girl who was with you? Her name was... {MACRO:FI}, wasn't it?",
    "DK4_MES_B146_R0105": "We're not together right now...",
    "DK4_MES_B146_R0112": "If you aren't sick... then something must be troubling you.",
    "DK4_MES_B146_R0119": "Hmm. Why don't you sail with me for a while?",
    "DK4_MES_B146_R0122": "What? But...",
    "DK4_MES_B146_R0126": "I can't leave you alone like this. You're not thinking of giving up sailing, are you?",
    "DK4_MES_B146_R0129": "No, of course not... But you want me aboard a Bergstrom ship?",
    "DK4_MES_B146_R0132": "Kamil, when something's troubling you, go to sea.",
    "DK4_MES_B146_R0140": "Don't shut yourself away when you're troubled. Keep busy and you'll clear your head. Once you're calm, the answer will come to you.",
    "DK4_MES_B146_R0147": "I had plenty of troubles myself when I was younger...",
    "DK4_MES_B146_R0151": "You did, Hodram?",
    "DK4_MES_B146_R0155": "Yes. Whenever that happened, the man who taught me to sail would take me aboard his ship. Somehow, my worries always faded at sea.",
    "DK4_MES_B146_R0158": "...Thank you. Then I'll take you up on that, for a little while.",
    "DK4_MES_B146_R0162": "Of course. Welcome aboard.",
}


def speaker_for(row_id: str, prefix: str) -> str:
    if row_id == "DK4_MES_B146_R0008":
        return "Unknown officer (unverified 0x97 lead)"
    if row_id == "DK4_MES_B146_R0031":
        return "Narration (unverified 0xFE lead)"
    if prefix == "01":
        return "Hodram Bergstrom"
    if prefix == "02":
        return "Lil Argot"
    if prefix == "09" or row_id in {"DK4_MES_B146_R0051", "DK4_MES_B146_R0058"}:
        return "Kamil"
    if prefix == "14":
        return "Fernando"
    raise SystemExit(f"unresolved B146 speaker: {row_id=} {prefix=}")


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = {
            row["id"]: row
            for row in csv.DictReader(stream)
            if row["id"].startswith("DK4_MES_B146_")
        }
    if set(rows) != set(LINES):
        raise SystemExit(
            f"B146 inventory mismatch: missing={sorted(set(rows) - set(LINES))}, "
            f"extra={sorted(set(LINES) - set(rows))}"
        )

    records = []
    for row_id, english in LINES.items():
        source = bytes.fromhex(rows[row_id]["source_hex"])
        prefix = f"{source[0]:02X}"
        records.append(
            {
                "id": row_id,
                "draft_english": f"{english}{{PAD}}",
                "speaker": speaker_for(row_id, prefix),
                "context": "Kamil leaves Lil after confronting his father; Hodram finds him distraught and invites him aboard to recover at sea.",
                "source_meaning": english.replace("{MACRO:FI}", "Lil"),
                "localization_note": "Localized from the clean Japanese as natural American dialogue; manual source wrapping is intentionally discarded.",
                "source_prefix_hex": prefix,
                "source_length": len(source),
                "blocker": "SC2 block 146 presentation states, bare speaker records, and FI expansion are unmapped; the 0x97 and 0xFE leads are explicitly unverified; this draft is not encodable.",
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": False,
                },
            }
        )

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256,
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "route_owner": "Lil Argot",
        "review_gates": [
            "source",
            "context",
            "localization",
            "naturalness",
            "formatting",
        ],
        "draft_status": "source-first-editorial-draft-blocked-unmapped-sc2-b146-control-state",
        "profile_note": "Non-buildable Lil-route draft retained under a historical Hodram filename. Block 146 mixes 01/02/09/14 leads, bare speaker records, an unverified 0x97 lead, an unverified 0xFE narration lead, and FI.",
        "inventory": {
            "identified_records": 35,
            "translated_drafts": 35,
            "encodable_records": 0,
            "blocked_records": 35,
            "missing_records": 0,
            "blocks": {"146": 35},
        },
        "records": [],
        "blocked_records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} blocked source-first drafts")


if __name__ == "__main__":
    main()
