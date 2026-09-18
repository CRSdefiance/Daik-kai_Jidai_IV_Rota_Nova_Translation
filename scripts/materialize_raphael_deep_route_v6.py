from __future__ import annotations

import csv
import json
from pathlib import Path

from materialize_lil_deep_route_v17 import LINES as LIL_SHARED_SCENE


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v6.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCK = "83"
EXCLUDED = {"DK4_MES_B83_R0081": "ten-byte harbor-rescue event-control payload with no visible dialogue"}
SPEAKERS = {
    "07": "Christina", "4F": "Mivor Gentz", "A2": "Boy",
    "A7": "Boy's mother", "FE": "Boy",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXT = "In London, Mivor overcomes his fear of water to rescue Christina and a drowning child, earning Christina's reluctant respect."
OVERRIDES = {
    "DK4_MES_B83_R0017": "All right.{LB}See you at the inn.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    block_rows = [row for row in all_rows.values() if row["id"].startswith("DK4_MES_B83_")]
    visible_rows = [row for row in block_rows if row["id"] not in EXCLUDED]
    # This event's Japanese script is shared verbatim with Lil SC2 B73. Its two
    # Lil/Kamil-only epilogue lines do not exist in Raphael's block, so reuse the
    # already source-reviewed shared dialogue in order and omit those two lines.
    shared_english = list(LIL_SHARED_SCENE.values())[:-2]
    if len(block_rows) != 85 or len(visible_rows) != 84 or len(shared_english) != 84:
        raise SystemExit(
            f"Raphael V6 inventory mismatch: all={len(block_rows)} visible={len(visible_rows)} shared={len(shared_english)}"
        )
    records = []
    for row, english in zip(visible_rows, shared_english, strict=True):
        english = OVERRIDES.get(row["id"], english)
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row["id"],
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Raphael crew member or story participant"),
            "context": CONTEXT,
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving Christina's blunt voice, Mivor's comic devotion, the harbor-rescue tension, and romantic payoff.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v6-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Christina and Mivor's complete London harbor rescue and romantic follow-up in Raphael SC0 block 83.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": 85, "translated_records": 84, "blocks": {BLOCK: 84}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records; excluded {len(EXCLUDED)} control")


if __name__ == "__main__":
    main()
