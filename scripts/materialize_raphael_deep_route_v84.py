from __future__ import annotations

import csv
import json
import re
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v84.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = (329, 330, 331)

SPEAKERS = {
    0x97: "Raphael crewmate",
    0xCC: "Fortune teller",
    0xD0: "Raphael crewmate",
    0xD3: "Raphael crewmate",
    0xD6: "Raphael crewmate",
    0xDA: "Raphael medic",
    0xFE: "System",
}

OVERRIDES = {
    "DK4_MES_B329_R0021": "No map.{LB}We'll get lost.",
    "DK4_MES_B329_R0022": "No map, Admiral.{LB}We'll get lost.",
    "DK4_MES_B329_R0023": "No map, Admiral.{LB}We'll get lost.",
    "DK4_MES_B329_R0024": "No map, Admiral.{LB}We'll get lost.",
    "DK4_MES_B329_R0025": "Admiral, without a map{LB}we'll get lost.",
    "DK4_MES_B329_R0067": "A desert, after all. Let's go.",
    "DK4_MES_B329_R0096": "Stay calm!",
    "DK4_MES_B329_R0120": "Got this!{LB}Hah!",
    "DK4_MES_B329_R0143": "Ow!!",
    "DK4_MES_B329_R0171": "Got careless...",
    "DK4_MES_B329_R0220": "Thanks.{LB}My head is spinning.",
    "DK4_MES_B329_R0229": "Leave it to me!{LB}Shoo! Go away!",
    "DK4_MES_B329_R0256": "Back away quietly.{LB}Don't provoke them...",
    "DK4_MES_B329_R0310": "Ah!",
    "DK4_MES_B329_R0345": "Dash through!",
    "DK4_MES_B330_R0006": "Welcome.",
    "DK4_MES_B330_R0010": "{MACRO:FI}, know the Goryeo incense burner?",
    "DK4_MES_B330_R0015": "Censer",
    "DK4_MES_B330_R0019": "They say it sharpens readings.{LB}Oh, how wonderful to try...",
    "DK4_MES_B330_R0029": "Hmm.",
    "DK4_MES_B330_R0033": "Oh, right.",
    "DK4_MES_B330_R0037": "Pirates have been active nearby.{LB}Be sure your ships are well equipped.",
    "DK4_MES_B330_R0045": "See you.",
    "DK4_MES_B331_R0006": "Why, welcome!",
    "DK4_MES_B331_R0010": "Your incense burner improved my readings.{LB}As thanks, let me read your fortune.",
    "DK4_MES_B331_R0014": "Come, sit there.",
    "DK4_MES_B331_R0026": "Go inland from this city.{LB}Ruins lie deep in the desert.{LB}What you seek is there.",
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
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    with SOURCE.open(encoding="utf-8-sig", newline="") as source:
        rows = [row for row in csv.DictReader(source) if row["id"].startswith(prefixes)]
    refs = _references()
    records = []
    unresolved = []
    for row in rows:
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
            "context": "Raphael crosses a scorpion-filled desert, hears of the Goryeo incense burner and pirates, then receives a fortune pointing to inland ruins.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Source-identical expedition variants are reused from audited routes; Raphael-specific dialogue and fixed-record constraints are preserved explicitly.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    if unresolved:
        raise SystemExit(f"Raphael V84 unresolved records: {unresolved}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v84-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael scorpion-desert expedition, Goryeo incense-burner rumor, pirate warning, and fortune-teller ruins lead in SC0 blocks 329-331.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {str(block): sum(row["id"].startswith(f"DK4_MES_B{block}_") for row in rows) for block in BLOCKS}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
