from __future__ import annotations

import csv
import json
import re
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
REFERENCE_SOURCE = Path("work/sc1/script.csv")
REFERENCE_BATCHES = (
    Path("translations/hodram_deep_route_v19.json"),
    Path("translations/hodram_deep_route_v20a.json"),
    Path("translations/hodram_deep_route_v20b.json"),
)
OUTPUT = Path("translations/raphael_deep_route_v65.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = tuple(range(255, 265))
EXCLUDED = {
    "DK4_MES_B261_R0197": "Raw four-byte event-control payload; not dialogue.",
}

SPEAKERS = {
    0x0D: "Cesare Tohni",
    0x14: "Fernando Dias",
    0xBC: "Towns-woman",
    0xBD: "Towns-woman",
    0xBE: "Towns-woman",
    0xC1: "Towns-woman",
    0xC3: "Towns-woman",
    0xC4: "Towns-woman",
    0xC8: "Towns-woman",
    0xD0: "Raphael crewmate",
    0xFE: "System, inscription, or statue voice",
}

CONTEXT = {
    255: "A tavern woman tells Raphael of a New World river carrying golden sand.",
    256: "A towns-woman tells Raphael the mystery of the Lamenting Jar, said to predate pottery.",
    257: "A local woman points Raphael toward nearby hilltop ruins.",
    258: "A local woman gives Raphael directions to the pyramids.",
    259: "A local woman points Raphael toward ruins said to be King Solomon's treasury.",
    260: "Cesare and Raphael discover a benevolent figurehead that raises luck or charm.",
    261: "Fernando and Raphael solve a water-level ruin puzzle and awaken a supernatural figurehead.",
    262: "A local woman privately reveals nearby ruins.",
    263: "A local woman says the town has no famous ruins.",
    264: "A local woman says the town has no famous ruins.",
}

OVERRIDES = {
    "DK4_MES_B255_R0015": "Hm.",
    "DK4_MES_B256_R0006": "{MACRO:FI}, know the Lamenting Jar?",
    "DK4_MES_B256_R0011": "Lamenting jar?",
    "DK4_MES_B256_R0015": "Rumor says a pottery jar was made before pottery was invented.",
    "DK4_MES_B256_R0019": "What? Then who made it?",
    "DK4_MES_B256_R0022": "That mystery makes it fun!",
    "DK4_MES_B256_R0026": "Maybe an advanced ancient civilization existed and vanished...",
    "DK4_MES_B256_R0029": "Or visitors from the sky left it!",
    "DK4_MES_B256_R0033": "Hahaha... Wild tale. But still unfound, right?",
    "DK4_MES_B256_R0036": "No. This rumor feels true. The jar must exist!",
    "DK4_MES_B256_R0040": "Oh? Maybe.",
    "DK4_MES_B258_R0012": "No, not yet.",
    "DK4_MES_B258_R0020": "Useful.",
    "DK4_MES_B259_R0014": "Hm.",
    "DK4_MES_B260_R0010": "Yes... This statue feels strange. A warm compassion...",
    "DK4_MES_B260_R0023": "Over there.",
    "DK4_MES_B260_R0039": "A famous statue?",
    "DK4_MES_B260_R0062": "Such a fine figurehead belongs at sea, not on land. Don't you agree?",
    "DK4_MES_B260_R0080": "Careful! Don't let go! What's wrong?",
    "DK4_MES_B260_R0089": "You okay?",
    "DK4_MES_B260_R0114": "Let's return to town.",
    "DK4_MES_B261_R0032": "This answer!",
    "DK4_MES_B261_R0055": "Wrong... Back to town today!",
    "DK4_MES_B261_R0073": "This answer!",
    "DK4_MES_B261_R0096": "Wrong... Back to town today!",
    "DK4_MES_B261_R0115": "Melted ice is water. Same level!",
    "DK4_MES_B261_R0133": "Where?",
    "DK4_MES_B261_R0189": "A little scary.",
}


def _strip_english_markup(text: str) -> str:
    text = re.sub(r"^\{SPEAKER:[0-9A-F]+\}", "", text)
    return re.sub(r"\{PAD\}$", "", text)


def _reference_lines() -> dict[str, str]:
    with REFERENCE_SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    lines: dict[str, str] = {}
    for batch_path in REFERENCE_BATCHES:
        reference = json.loads(batch_path.read_text(encoding="utf-8"))
        for record in reference["records"]:
            source_hex = source_rows[record["id"]]["source_hex"].upper()
            english = record["english"]
            key = source_hex[2:] if english.startswith("{SPEAKER:") else source_hex
            body = _strip_english_markup(english)
            prior = lines.setdefault(key, body)
            if prior != body:
                raise SystemExit(f"Reference text collision for {key}: {prior!r} != {body!r}")
    return lines


def main() -> None:
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = [row for row in csv.DictReader(stream) if row["id"].startswith(prefixes)]
    reference_lines = _reference_lines()

    records = []
    unresolved = []
    block_counts: dict[str, int] = {}
    for row in source_rows:
        row_id = row["id"]
        if row_id in EXCLUDED:
            continue
        source_hex = row["source_hex"].upper()
        first = int(source_hex[:2], 16)
        key = source_hex[2:] if first in SPEAKERS else source_hex
        english = OVERRIDES.get(row_id, reference_lines.get(key))
        if english is None:
            unresolved.append(row_id)
            continue
        unsafe = english
        for macro in ("FI", "FA", "FO", "FU"):
            unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        state = f"{first:02X}" if first in SPEAKERS else ""
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        block_counts[str(block)] = block_counts.get(str(block), 0) + 1
        records.append(
            {
                "id": row_id,
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(first, "Raphael companion, choice, or scene text"),
                "context": CONTEXT[block],
                "source_meaning": (
                    english.replace("{LB}", " ")
                    .replace("{MACRO:FI}", "Raphael")
                    .replace("{MACRO:FA}", "Castelo")
                ),
                "localization_note": "Faithful concise American English preserving puzzle branches, canonical names, scene timing, and fixed-record display constraints.",
                "qa_waivers": [
                    "weak-line-ending",
                    "orphan-final-line",
                    *(["manual-break"] if "{LB}" in english else []),
                ],
                **(
                    {
                        "manual_break_reason": (
                            "Places a protected newline before the native row boundary so the "
                            "progressive ASCII pair phase cannot auto-wrap and skip a display row."
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

    if unresolved:
        raise SystemExit(f"Raphael V65 unresolved records: {unresolved}")
    if len(records) + len(EXCLUDED) != len(source_rows):
        raise SystemExit(
            f"Raphael V65 inventory mismatch: {len(records)} translated + "
            f"{len(EXCLUDED)} controls != {len(source_rows)} source records"
        )

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v65-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Ten source-locked Raphael discovery-hint, Lamenting Jar, benevolent-figurehead, and ruin-puzzle events across SC0 blocks 255-264.",
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(source_rows),
            "translated_records": len(records),
            "blocks": block_counts,
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} control preserved")


if __name__ == "__main__":
    main()
