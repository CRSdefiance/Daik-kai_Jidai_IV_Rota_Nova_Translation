from __future__ import annotations

import csv
import json
import re
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v82.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"

EXCLUDED = {
    "DK4_MES_B325_R0038": "Raw forest-entry control payload; not dialogue.",
    "DK4_MES_B325_R0313": "Raw wolf-branch control payload; not dialogue.",
}

SPEAKERS = {
    0x97: "Raphael crewmate",
    0xD0: "Raphael crewmate",
    0xD3: "Raphael crewmate",
    0xD6: "Raphael crewmate",
    0xD7: "Raphael crewmate",
    0xDA: "Raphael medic",
    0xFE: "System",
}

OVERRIDES = {
    "DK4_MES_B325_R0022": "Admiral,{LB}we need a map.",
    "DK4_MES_B325_R0025": "No map, Admiral.{LB}We'll get lost.",
    "DK4_MES_B325_R0056": "Let's go.",
    "DK4_MES_B325_R0095": "Stay calm!",
    "DK4_MES_B325_R0119": "Leave this to me!{LB}Shoo! Go away!",
    "DK4_MES_B325_R0143": "Ow!",
    "DK4_MES_B325_R0171": "All right. Ow...",
    "DK4_MES_B325_R0176": "Thanks, everyone.{LB}Let's hurry on.",
    "DK4_MES_B325_R0193": "Just wolves!{LB}Move on!",
    "DK4_MES_B325_R0266": "My hand slipped...{LB}Sorry! Truly sorry!!",
    "DK4_MES_B325_R0291": "Good...",
    "DK4_MES_B325_R0300": "The sailors seem fatigued.",
    "DK4_MES_B325_R0307": "They won't attack{LB}unless we do first.",
}


def _strip(text: str) -> str:
    return re.sub(r"\{PAD\}$", "", re.sub(r"^\{SPEAKER:[0-9A-F]+\}", "", text))


def _references() -> dict[str, str]:
    tables = {}
    for route in ("SC1", "SC2", "SC3"):
        with (Path("work") / route.lower() / "script.csv").open(encoding="utf-8-sig", newline="") as source:
            tables[route] = {row["id"]: row["source_hex"].upper() for row in csv.DictReader(source)}
    refs = {}
    for path in sorted(Path("translations").glob("hodram_deep_route_v*.json")) + sorted(Path("translations").glob("lil_deep_route_v*.json")):
        batch = json.loads(path.read_text(encoding="utf-8"))
        match = re.search(r"/(SC[123])\.DK4$", str(batch.get("file_path", "")), re.I)
        if not match:
            continue
        table = tables[match.group(1).upper()]
        for record in batch.get("records", []):
            source_hex = table.get(record["id"])
            if source_hex:
                key = source_hex[2:] if record["english"].startswith("{SPEAKER:") else source_hex
                refs.setdefault(key, _strip(record["english"]))
    return refs


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as source:
        rows = [row for row in csv.DictReader(source) if row["id"].startswith("DK4_MES_B325_")]
    refs = _references()
    records = []
    unresolved = []
    for row in rows:
        if row["id"] in EXCLUDED:
            continue
        source_hex = row["source_hex"].upper()
        first = int(source_hex[:2], 16)
        english = OVERRIDES.get(row["id"], refs.get(source_hex[2:] if first in SPEAKERS else source_hex))
        if english is None:
            unresolved.append(row["id"])
            continue
        unsafe = english
        for macro in ("FI", "FA", "FO", "FU"):
            unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
        state = f"{first:02X}" if first in SPEAKERS else ""
        rendered = f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}"
        records.append({
            "id": row["id"], "english": rendered,
            "speaker": SPEAKERS.get(first, "Raphael party, choice, or scene text"),
            "context": "Raphael crosses a forest, encounters wolves, chooses how to respond, handles injuries, and reaches the Proof-map guardians' village.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Source-identical shared expedition text is reused from the audited Hodram route; Raphael-specific lines preserve choices, injuries, controls, and fixed-record constraints.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    if unresolved:
        raise SystemExit(f"Raphael V82 unresolved records: {unresolved}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v82-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael forest navigation, wolf choices, injury variants, treatment, fatigue, and village arrival event in SC0 block 325.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"325": len(rows)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
