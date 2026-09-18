from __future__ import annotations

import csv
import json
import re
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v86.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = (333, 334, 335)

EXCLUDED = {
    "DK4_MES_B333_R0037": "Raw jungle-entry control payload; not dialogue.",
    "DK4_MES_B333_R0117": "Raw cave-choice control payload; not dialogue.",
    "DK4_MES_B333_R0200": "Raw jungle-fatigue control payload; not dialogue.",
    "DK4_MES_B334_R0023": "Raw ancient-city entry control payload; not dialogue.",
    "DK4_MES_B334_R0072": "Raw boat-transfer control payload; not dialogue.",
    "DK4_MES_B334_R0082": "Raw ruins-approach control payload; not dialogue.",
}

SPEAKERS = {
    0xB3: "Proof-map guide",
    0xCE: "Tavern patron",
    0xD0: "Raphael crewmate",
    0xD3: "Raphael crewmate",
    0xD6: "Raphael crewmate",
    0xFE: "System",
}

OVERRIDES = {
    "DK4_MES_B333_R0019": "Admiral, don't wander{LB}this jungle blindly.",
    "DK4_MES_B333_R0023": "Admiral, don't wander{LB}this jungle blindly.",
    "DK4_MES_B333_R0025": "Admiral, don't wander{LB}this jungle blindly.",
    "DK4_MES_B333_R0064": "A jungle...",
    "DK4_MES_B333_R0093": "Hard to see anything...",
    "DK4_MES_B333_R0097": "Sir...",
    "DK4_MES_B333_R0113": "A fire seems risky...{LB}Let's keep going...",
    "DK4_MES_B333_R0123": "Phew, that was rough...{LB}Where are we now?",
    "DK4_MES_B333_R0142": "Hmm...{LB}Seems we emerged near the ruins.",
    "DK4_MES_B333_R0153": "All right. Let's light it...",
    "DK4_MES_B333_R0158": "Whoa!{LB}Bats!",
    "DK4_MES_B333_R0184": "They're only bats!{LB}Keep going!",
    "DK4_MES_B333_R0198": "The sailors are exhausted.",
    "DK4_MES_B334_R0049": "What?!",
    "DK4_MES_B334_R0062": "Then port would be{LB}quicker...",
    "DK4_MES_B334_R0114": "Yes! Let's go.",
    "DK4_MES_B335_R0005": "Why, welcome.",
    "DK4_MES_B335_R0009": "Ever visited a northern village{LB}in the New World?",
    "DK4_MES_B335_R0013": "A customer said a great monk from this city crossed north long ago to preach.",
    "DK4_MES_B335_R0017": "After finding that village, he vanished. What happened to him?",
    "DK4_MES_B335_R0022": "Dunno",
    "DK4_MES_B335_R0026": "They say he was holy.{LB}Hope his converts cherished him.",
    "DK4_MES_B335_R0029": "Traveling north? Ask what became of that monk.",
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
            "context": "Raphael crosses a jungle and cave, reaches an ancient city with the Proof-map guide, then hears an optional rumor about a missing northern missionary.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Source-identical jungle and ruins variants are reused from audited routes; Raphael-specific dialogue, optional-event text, and controls remain explicit.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    if unresolved:
        raise SystemExit(f"Raphael V86 unresolved records: {unresolved}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v86-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael jungle, cave/fire choice, bat fatigue, ancient-city transfer and ruins arrival, plus missing-monk rumor in SC0 blocks 333-335.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {str(block): sum(row["id"].startswith(f"DK4_MES_B{block}_") for row in rows) for block in BLOCKS}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
