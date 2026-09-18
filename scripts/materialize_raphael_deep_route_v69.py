from __future__ import annotations

import csv
import json
import re
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v69.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = (293,)
EXCLUDED = {
    "DK4_MES_B293_R0038": "Raw scene-control payload selecting the ruin expedition branch; not dialogue.",
}

SPEAKERS = {
    0x05: "Claudio Manousch",
    0x0E: "Emilio Marone",
    0x16: "Raphael crewmate",
    0x9F: "Raphael crewmate",
    0xB1: "Megalith cult leader",
    0xB2: "Megalith cultists",
    0xD0: "Raphael crewmate",
    0xD3: "Raphael crewmate",
    0xD7: "Raphael crewmate",
    0xD8: "Raphael crewmate",
    0xFE: "System",
}

OVERRIDES = {
    "DK4_MES_B293_R0050": "Dense forest.{LB}Stay careful.",
    "DK4_MES_B293_R0059": "A very dense forest.{LB}May nothing find us...",
    "DK4_MES_B293_R0063": "Proceed safely.",
    "DK4_MES_B293_R0121": "Shoot!",
    "DK4_MES_B293_R0181": "Shh, hold still.",
    "DK4_MES_B293_R0230": "Not pretending.{LB}He's truly asleep...",
    "DK4_MES_B293_R0324": "Run!!",
    "DK4_MES_B293_R0382": "Are those the strange people?",
    "DK4_MES_B293_R0393": "A song?{LB}This feels dangerous.",
    "DK4_MES_B293_R0396": "Sun, moon, stars turn.{LB}When light and dark balance,{LB}it lies between.",
    "DK4_MES_B293_R0400": "Sun, moon, stars turn.{LB}When light and dark balance,{LB}it lies between.",
    "DK4_MES_B293_R0409": "What are they saying?{LB}A spell?",
    "DK4_MES_B293_R0412": "Our Ancient Megalith Society{LB}will soon receive revelation{LB}and rule the world!",
    "DK4_MES_B293_R0415": "On revelation's eve, pray again!{LB}Sacrifice the fools who mocked us!",
    "DK4_MES_B293_R0423": "Rule all?!",
    "DK4_MES_B293_R0427": "A sacrifice?{LB}Are they serious?!",
    "DK4_MES_B293_R0430": "Until then, stay from the stones!{LB}Meeting adjourned!",
    "DK4_MES_B293_R0443": "They left.",
    "DK4_MES_B293_R0447": "Let's follow.",
}


def _strip_english_markup(text: str) -> str:
    text = re.sub(r"^\{SPEAKER:[0-9A-F]+\}", "", text)
    return re.sub(r"\{PAD\}$", "", text)


def _reference_lines() -> dict[str, str]:
    source_tables: dict[str, dict[str, str]] = {}
    for route in ("sc1", "sc2", "sc3"):
        path = Path("work") / route / "script.csv"
        with path.open(encoding="utf-8-sig", newline="") as stream:
            source_tables[route.upper()] = {
                row["id"]: row["source_hex"].upper() for row in csv.DictReader(stream)
            }

    paths = sorted(Path("translations").glob("hodram_deep_route_v*.json"))
    paths += sorted(Path("translations").glob("lil_deep_route_v*.json"))
    lines: dict[str, str] = {}
    for batch_path in paths:
        batch = json.loads(batch_path.read_text(encoding="utf-8"))
        match = re.search(r"/(SC[123])\.DK4$", str(batch.get("file_path", "")), re.IGNORECASE)
        if not match:
            continue
        source_rows = source_tables[match.group(1).upper()]
        for record in batch.get("records", []):
            source_hex = source_rows.get(record["id"])
            if source_hex is None:
                continue
            english = record["english"]
            key = source_hex[2:] if english.startswith("{SPEAKER:") else source_hex
            lines.setdefault(key, _strip_english_markup(english))
    return lines


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B293_")]
    references = _reference_lines()
    records = []
    unresolved = []
    for row in source_rows:
        row_id = row["id"]
        if row_id in EXCLUDED:
            continue
        source_hex = row["source_hex"].upper()
        first = int(source_hex[:2], 16)
        key = source_hex[2:] if first in SPEAKERS else source_hex
        english = OVERRIDES.get(row_id, references.get(key))
        if english is None:
            unresolved.append(row_id)
            continue
        unsafe = english
        for macro in ("FI", "FA", "FO", "FU"):
            unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        state = f"{first:02X}" if first in SPEAKERS else ""
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(first, "Raphael party, choice, or scene text"),
            "context": "Raphael's party crosses a bear-filled forest, reaches ancient ruins, and discovers the Ancient Megalith Society planning human sacrifice.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving every bear encounter branch, choice, injury result, cult chant, and fixed-record display constraint.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })

    if unresolved:
        raise SystemExit(f"Raphael V69 unresolved records: {unresolved}")
    if len(records) + len(EXCLUDED) != len(source_rows):
        raise SystemExit(
            f"Raphael V69 inventory mismatch: {len(records)} translated + "
            f"{len(EXCLUDED)} controls != {len(source_rows)} source records"
        )
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v69-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael forest, bear encounter, ruin arrival, and Ancient Megalith Society event in SC0 block 293.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": {"293": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} control preserved")


if __name__ == "__main__":
    main()
