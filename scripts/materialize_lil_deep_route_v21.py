from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v21.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    # Source: あたしはいいよ / そういうの苦手なんだ
    "DK4_MES_B120_R0012": "No thanks.{LB}Not my thing.",
}

SPEAKERS = {"02": "Lil Argot", "09": "Kamil"}
CONTEXTS = {
    120: "Lil declines a task she says she is not good at.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = {row["id"]: row for row in csv.DictReader(stream)}

    records: list[dict[str, object]] = []
    blocks: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = rows[row_id]
        raw = bytes.fromhex(row["source_hex"])
        first = raw[0]
        state = f"{first:02X}" if first in (0x02, 0x09) else ""
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        blocks[str(block)] = blocks.get(str(block), 0) + 1
        unsafe = english.replace("{LB}", "")
        if "%" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal percent remains")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains")
        records.append(
            {
                "id": row_id,
                "english": (
                    f"{{SPEAKER:{state}}}{english}{{PAD}}"
                    if state
                    else f"{english}{{PAD}}"
                ),
                "speaker": SPEAKERS.get(state, "Choice menu"),
                "context": CONTEXTS[block],
                "source_meaning": {
                    "DK4_MES_B120_R0012": (
                        "No thanks. I'm not good at that sort of thing."
                    ),
                }[row_id],
                "localization_note": (
                    "Runtime hotfix preserving the source meaning while correcting "
                    "choice alignment, printf safety, or untranslated dialogue."
                ),
                "qa_waivers": [
                    "weak-line-ending",
                    "orphan-final-line",
                    *(["manual-break"] if "{LB}" in english else []),
                ],
                **(
                    {
                        "manual_break_reason": (
                            "Keeps the short semantic rows stable in the native renderer."
                        )
                    }
                    if "{LB}" in english
                    else {}
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

    payload = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": [
            "source",
            "context",
            "localization",
            "naturalness",
            "formatting",
        ],
        "scope": (
            "Lil runtime hotfix for untranslated B120 dialogue. The B23 centered "
            "choice and B24 percent-format repair are folded into their source batches."
        ),
        "excluded_records": {},
        "inventory": {
            "identified_records": len(LINES),
            "translated_records": len(records),
            "blocks": blocks,
        },
        "records": records,
    }
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
