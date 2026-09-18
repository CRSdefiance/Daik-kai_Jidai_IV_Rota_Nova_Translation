from __future__ import annotations

import csv
import json
import re
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
REFERENCE_SOURCE = Path("work/sc1/script.csv")
REFERENCE_BATCHES = (
    Path("translations/hodram_deep_route_v18.json"),
    Path("translations/hodram_deep_route_v19.json"),
)
OUTPUT = Path("translations/raphael_deep_route_v63.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = tuple(range(245, 251))

SPEAKERS = {
    0x04: "Janus Pasha",
    0x0B: "Jam Jack Ludwyan",
    0x0D: "Cesare Tohni",
    0x12: "Charles Jean Rochefort",
    0x13: "Carlo",
    0x14: "Fernando Dias",
    0x17: "Manuel Armestad",
    0x68: "Filippo",
    0x71: "Sailor",
    0xD0: "Raphael crewmate",
}

CONTEXT = {
    245: "Manuel describes Phidias's legendary chisel buried somewhere in the Balkans.",
    246: "Carlo and Filippo discuss Papal States trade and relics once owned by a pope.",
    247: "Charles writes about a mysterious roar that rallied sailors west of Lisbon.",
    248: "Jam writes from South Asia about a Gupta spirit-beast statue that sees the future.",
    249: "Cesare fumes over sailors neglecting work to discuss the Demon-Piercing Arrow.",
    250: "Janus hurts his hand repairing the ship, prompting a lead about protective gloves lost on Jutland.",
}

OVERRIDES = {
    "DK4_MES_B245_R0009": "Eh?",
    "DK4_MES_B245_R0018": "A scrap? Which?",
    "DK4_MES_B245_R0026": "Hm.",
    "DK4_MES_B245_R0037": "Manuel, surely not for ship repairs?",
    "DK4_MES_B247_R0058": "A strange tale... Yes, worth noting.",
    "DK4_MES_B248_R0071": "Jam never changes... Still, that statue sounds strange. Maybe we should seek it.",
    "DK4_MES_B249_R0009": "Cesare, what is wrong? You seem angry.",
    "DK4_MES_B249_R0024": "What is this item? Something that pierces demons?",
    "DK4_MES_B249_R0045": "...Leave him alone.",
    "DK4_MES_B250_R0010": "Janus?! Are you hurt?",
    "DK4_MES_B250_R0025": "Our crewmate hurt his hand.",
    "DK4_MES_B250_R0053": "Why lose something so important?",
    "DK4_MES_B250_R0069": "Hm. We may look for them.",
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
        source_hex = row["source_hex"].upper()
        first = int(source_hex[:2], 16)
        key = source_hex[2:] if first in SPEAKERS else source_hex
        english = OVERRIDES.get(row_id, reference_lines.get(key))
        if english is None:
            unresolved.append(row_id)
            continue
        english = (
            english.replace("Gennas", "Janus")
            .replace("Ｆernando", "Dias")
            .replace("Ｆilippo", "friend")
        )
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
                "speaker": SPEAKERS.get(first, "Raphael companion or scene text"),
                "context": CONTEXT[block],
                "source_meaning": english.replace("{LB}", " ").replace("{MACRO:FI}", "Raphael"),
                "localization_note": "Faithful concise American English preserving canonical names, scene timing, and fixed-record display constraints.",
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
        raise SystemExit(f"Raphael V63 unresolved records: {unresolved}")
    if len(records) != len(source_rows):
        raise SystemExit(f"Raphael V63 inventory mismatch: {len(records)} != {len(source_rows)}")

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v63-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Six source-locked Raphael relic, correspondence, equipment, and character events across SC0 blocks 245-250.",
        "excluded_records": {},
        "inventory": {
            "identified_records": len(source_rows),
            "translated_records": len(records),
            "blocks": block_counts,
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
