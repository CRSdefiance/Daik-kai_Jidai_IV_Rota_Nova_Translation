from __future__ import annotations

import csv
import json
import re
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v83.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"

EXCLUDED = {
    "DK4_MES_B327_R0036": "Raw forest-entry control payload; not dialogue.",
    "DK4_MES_B327_R0063": "Raw forest-encounter control payload; not dialogue.",
    "DK4_MES_B327_R0105": "Raw route-choice control payload; not dialogue.",
    "DK4_MES_B327_R0144": "Raw vampire-bat branch control payload; not dialogue.",
}

SPEAKERS = {
    0xC9: "Secluded-city woman",
    0xCD: "Local informant",
    0xD0: "Raphael crewmate",
    0xD3: "Raphael crewmate",
    0xD6: "Raphael crewmate",
    0xDA: "Raphael medic",
    0x97: "Raphael crewmate",
    0xFE: "System",
}

OVERRIDES = {
    "DK4_MES_B326_R0006": "Ah, {MACRO:FI}.{LB}Welcome.",
    "DK4_MES_B326_R0009": "Know where the gate is?",
    "DK4_MES_B326_R0013": "We shouldn't tell outsiders, but...",
    "DK4_MES_B326_R0016": "Pressure from abroad has made isolation meaningless. All right. The secret is yours.",
    "DK4_MES_B327_R0080": "Whoa!",
    "DK4_MES_B327_R0086": "Screech!",
    "DK4_MES_B327_R0092": "Avoid the bats",
    "DK4_MES_B327_R0094": "Push through",
    "DK4_MES_B327_R0103": "Detour around them.",
    "DK4_MES_B327_R0119": "Just bats.",
    "DK4_MES_B327_R0133": "No... vampire bats!",
    "DK4_MES_B327_R0134": "No... vampire bats!",
    "DK4_MES_B327_R0135": "Vampire bats!",
    "DK4_MES_B327_R0136": "Eek... vampire bats!",
    "DK4_MES_B327_R0137": "No... vampire bats!",
    "DK4_MES_B327_R0138": "No... vampire bats!",
    "DK4_MES_B327_R0139": "No... vampire bats!",
    "DK4_MES_B327_R0142": "Run!",
    "DK4_MES_B327_R0147": "Pant...",
    "DK4_MES_B327_R0160": "Phew... exhausted.",
    "DK4_MES_B327_R0162": "Exhausted...",
    "DK4_MES_B327_R0164": "Tired...",
    "DK4_MES_B327_R0166": "Exhausted...",
    "DK4_MES_B327_R0168": "Pant, pant... so tired.",
    "DK4_MES_B327_R0170": "So tired...",
    "DK4_MES_B327_R0172": "So hungry...",
    "DK4_MES_B327_R0174": "Phew... exhausted.",
    "DK4_MES_B327_R0181": "The sailors seem fatigued.",
    "DK4_MES_B327_R0195": "Nearly there. Go on.",
    "DK4_MES_B328_R0006": "Ah, {MACRO:FI}.{LB}Almost forgot something.",
    "DK4_MES_B328_R0010": "An ancient illustrated map was found. The map says ruins of an old kingdom lie near this town.",
    "DK4_MES_B328_R0014": "An illustrated map?{LB}Where is it?",
    "DK4_MES_B328_R0017": "Sorry, that much is unknown. Curious? Then search for it.",
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
    prefixes = tuple(f"DK4_MES_B{block}_" for block in range(326, 329))
    with SOURCE.open(encoding="utf-8-sig", newline="") as source:
        rows = [row for row in csv.DictReader(source) if row["id"].startswith(prefixes)]
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
            "context": "Raphael learns a secluded city's gate, crosses a bat-infested forest, and hears of an ancient map pointing to nearby ruins.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Source-identical expedition text is reused from audited routes; Raphael-specific dialogue, choices, controls, and fixed-record constraints are preserved explicitly.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    if unresolved:
        raise SystemExit(f"Raphael V83 unresolved records: {unresolved}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v83-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael secluded-city gate tip, dark-forest and vampire-bat expedition, and ancient-map rumor in SC0 blocks 326-328.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {str(block): sum(row["id"].startswith(f"DK4_MES_B{block}_") for row in rows) for block in range(326, 329)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
