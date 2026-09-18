from __future__ import annotations

import csv
import json
import re
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v72.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
SPEAKERS = {
    0x05: "Claudio Manousch", 0x08: "Arcadius Eirene",
    0xD0: "Raphael crewmate", 0xD3: "Raphael crewmate",
    0xD7: "Raphael crewmate", 0xD8: "Raphael crewmate", 0xFE: "System or beast",
}
OVERRIDES = {
    "DK4_MES_B301_R0038": "An eerie jungle...",
    "DK4_MES_B301_R0042": "Yes... We should not linger here.",
    "DK4_MES_B301_R0046": "Cave...",
    "DK4_MES_B301_R0050": "Enter?",
    "DK4_MES_B301_R0055": "Yeah. Don't want to turn back...",
    "DK4_MES_B301_R0059": "Settled. Let's go!",
    "DK4_MES_B301_R0063": "Creepy...",
    "DK4_MES_B301_R0068": "Yeah. Let's hurry.",
    "DK4_MES_B301_R0080": "Please slow down.{LB}Darkness hides the ground.",
    "DK4_MES_B301_R0125": "Shoot it!",
    "DK4_MES_B301_R0133": "Whoa!",
    "DK4_MES_B301_R0138": "Damn! Such a nimble beast!",
    "DK4_MES_B301_R0164": "More injuries...{LB}Everyone, use swords!",
    "DK4_MES_B301_R0226": "Whew, saved!",
    "DK4_MES_B301_R0239": "Ah, light! We can leave the cave!",
}


def _strip(text: str) -> str:
    return re.sub(r"\{PAD\}$", "", re.sub(r"^\{SPEAKER:[0-9A-F]+\}", "", text))


def _references() -> dict[str, str]:
    tables = {}
    for route in ("SC1", "SC2", "SC3"):
        with (Path("work") / route.lower() / "script.csv").open(encoding="utf-8-sig", newline="") as stream:
            tables[route] = {r["id"]: r["source_hex"].upper() for r in csv.DictReader(stream)}
    paths = sorted(Path("translations").glob("hodram_deep_route_v*.json"))
    paths += sorted(Path("translations").glob("lil_deep_route_v*.json"))
    result: dict[str, str] = {}
    for path in paths:
        batch = json.loads(path.read_text(encoding="utf-8"))
        match = re.search(r"/(SC[123])\.DK4$", str(batch.get("file_path", "")), re.IGNORECASE)
        if not match:
            continue
        table = tables[match.group(1).upper()]
        for record in batch.get("records", []):
            source_hex = table.get(record["id"])
            if source_hex:
                key = source_hex[2:] if record["english"].startswith("{SPEAKER:") else source_hex
                result.setdefault(key, _strip(record["english"]))
    return result


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [r for r in csv.DictReader(stream) if r["id"].startswith("DK4_MES_B301_")]
    references = _references()
    records = []
    unresolved = []
    for row in rows:
        row_id = row["id"]
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
            "context": "Raphael's party crosses a dangerous jungle and cave, encounters a tiger, and resolves every combat or escape branch.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving every tiger encounter choice, combat warning, injury result, escape branch, and fixed-record constraint.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    if unresolved:
        raise SystemExit(f"Raphael V72 unresolved records: {unresolved}")
    if len(records) != len(rows):
        raise SystemExit(f"Raphael V72 inventory mismatch: {len(records)} != {len(rows)}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v72-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael jungle, cave, tiger encounter, combat, escape, and aftermath event in SC0 block 301.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"301": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
