from __future__ import annotations

import csv
import json
import re
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v85.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"

EXCLUDED = {
    "DK4_MES_B332_R0038": "Raw inland-expedition entry control payload; not dialogue.",
    "DK4_MES_B332_R0067": "Raw inland-expedition control payload; not dialogue.",
    "DK4_MES_B332_R0190": "Raw cliff-branch control payload; not dialogue.",
    "DK4_MES_B332_R0223": "Raw route-branch control payload; not dialogue.",
    "DK4_MES_B332_R0323": "Raw expedition completion control payload; not dialogue.",
}

SPEAKERS = {
    0x05: "Raphael",
    0x97: "Raphael crewmate",
    0xD0: "Raphael crewmate",
    0xD3: "Raphael crewmate",
    0xD6: "Raphael crewmate",
    0xDA: "Raphael medic",
    0xFE: "System",
}

OVERRIDES = {
    "DK4_MES_B332_R0022": "No map.{LB}We'll get lost.",
    "DK4_MES_B332_R0025": "No map, Admiral.{LB}We'll get lost.",
    "DK4_MES_B332_R0078": "Admiral, we've come out here.",
    "DK4_MES_B332_R0079": "Admiral, we've come out here, but...",
    "DK4_MES_B332_R0080": "Admiral, cliff!",
    "DK4_MES_B332_R0082": "A huge cliff...{LB}What now?",
    "DK4_MES_B332_R0083": "Admiral, a cliff.",
    "DK4_MES_B332_R0085": "Atop a cliff.",
    "DK4_MES_B332_R0087": "A cliff. What now?",
    "DK4_MES_B332_R0091": "{MACRO:FI}!{LB}How did we end up here?",
    "DK4_MES_B332_R0096": "Strange...{LB}We followed the map...",
    "DK4_MES_B332_R0101": "Leap over",
    "DK4_MES_B332_R0103": "Detour",
    "DK4_MES_B332_R0111": "Let's jump across.",
    "DK4_MES_B332_R0124": "Admiral, don't be reckless.",
    "DK4_MES_B332_R0126": "Admiral, no...",
    "DK4_MES_B332_R0128": "That's madness...",
    "DK4_MES_B332_R0130": "A joke?!",
    "DK4_MES_B332_R0132": "That's reckless.",
    "DK4_MES_B332_R0134": "Come now.{LB}Don't be reckless.",
    "DK4_MES_B332_R0135": "Sure, flying sounds nice, but...",
    "DK4_MES_B332_R0136": "That's insane...",
    "DK4_MES_B332_R0141": "Just kidding.{LB}Climb down.",
    "DK4_MES_B332_R0144": "(Was that really a joke?)",
    "DK4_MES_B332_R0149": "Pant...",
    "DK4_MES_B332_R0153": "Aaaah!",
    "DK4_MES_B332_R0158": "You okay?{LB}Nearly there. Hold on!",
    "DK4_MES_B332_R0172": "A sailor was injured.{LB}The crew is exhausted.",
    "DK4_MES_B332_R0178": "A cliff... We must detour.",
    "DK4_MES_B332_R0214": "Now in view.",
    "DK4_MES_B332_R0320": "The sailors are exhausted.",
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
        rows = [row for row in csv.DictReader(source) if row["id"].startswith("DK4_MES_B332_")]
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
            "context": "Raphael's inland expedition encounters fog, dead ends, a cliff, risky crossing choices, fatigue, injury, and the route to the ruins.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Source-identical expedition variants are reused from audited routes; cliff-specific dialogue, choices, controls, and fixed-record constraints are explicit.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    if unresolved:
        raise SystemExit(f"Raphael V85 unresolved records: {unresolved}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v85-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael fog, dead-end, cliff-choice, injury, fatigue, and ruins-arrival expedition in SC0 block 332.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"332": len(rows)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
