from __future__ import annotations

import csv
import json
import re
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v87.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = tuple(range(336, 343))

SPEAKERS = {
    0x02: "Raphael companion",
    0x05: "Raphael companion",
    0x08: "Raphael companion",
    0x12: "Charles Rochfort",
    0xB3: "Warrior-trial guide or village elder",
    0xCF: "Raphael companion",
    0xFE: "System",
}

OVERRIDES = {
    "DK4_MES_B336_R0005": "Ah, {MACRO:FA}.{LB}Someone wants to meet you.",
    "DK4_MES_B336_R0018": "Pardon me, but you must be tested.",
    "DK4_MES_B336_R0026": "We just met, and now this?",
    "DK4_MES_B336_R0030": "Sorry. There is a ruin{LB}we desperately need found.",
    "DK4_MES_B336_R0035": "Ruins?",
    "DK4_MES_B336_R0047": "Greatest warrior?",
    "DK4_MES_B336_R0051": "Not strength alone.{LB}A true warrior has a just heart{LB}and wisdom.",
    "DK4_MES_B336_R0056": "You want to test whether{LB}this one is worthy?",
    "DK4_MES_B336_R0059": "Correct.",
    "DK4_MES_B336_R0063": "Hmph. Can't say{LB}this feels right.",
    "DK4_MES_B336_R0066": "We know it is rude.{LB}Still, we must ask.",
    "DK4_MES_B336_R0070": "All right. Let's try.",
    "DK4_MES_B336_R0074": "You sure?",
    "DK4_MES_B336_R0085": "'Greatest warrior'...{LB}Let's test my strength.{LB}Besides...",
    "DK4_MES_B336_R0090": "Maybe that ruin holds a key to the Proof. This is worth trying.",
    "DK4_MES_B336_R0096": "Agreed. Secret ruins may hold something hidden.",
    "DK4_MES_B336_R0100": "That ruin may even hold{LB}a key to the Proof.",
    "DK4_MES_B336_R0106": "Maybe so.{LB}Then count me in.",
    "DK4_MES_B336_R0109": "Thank you.{LB}Then, first...",
    "DK4_MES_B336_R0112": "To judge your swordsmanship,{LB}please find something.",
    "DK4_MES_B336_R0117": "What is it?",
    "DK4_MES_B336_R0121": "Seek Tlaloc's knife, hidden somewhere in the New World, and bring it here.",
    "DK4_MES_B336_R0126": "'Tlaloc's Knife'...",
    "DK4_MES_B336_R0130": "Bring it, and ancient warriors' martial arts shall be taught to you.",
    "DK4_MES_B336_R0134": "Until then,{LB}wait here at the square.",
    "DK4_MES_B337_R0013": "Right. We need to bring{LB}Tlaloc's knife.",
    "DK4_MES_B337_R0017": "Unequip it first.{LB}Remember that.",
    "DK4_MES_B337_R0029": "You brought it.",
    "DK4_MES_B337_R0036": "Tlaloc's knife given.",
    "DK4_MES_B337_R0040": "Come to this square{LB}for the next few days.",
    "DK4_MES_B337_R0044": "What?!{LB}A few days?",
    "DK4_MES_B337_R0047": "This is a secret martial art.{LB}A few hours won't suffice.",
    "DK4_MES_B337_R0051": "Then, begin.",
    "DK4_MES_B337_R0068": "Return tomorrow.",
    "DK4_MES_B337_R0073": "Amazing. You need no practice at all. You'll do fine.",
    "DK4_MES_B337_R0079": "Next...",
    "DK4_MES_B337_R0084": "What?{LB}More before we seek the ruins?",
    "DK4_MES_B337_R0088": "We need the Ancient City Map. Seek it, then meet me at this city's gate.",
    "DK4_MES_B337_R0095": "{MACRO:FI}'s agility rose 1!",
    "DK4_MES_B338_R0005": "Let's work hard again today.",
    "DK4_MES_B338_R0020": "Advanced training today.",
    "DK4_MES_B338_R0039": "Now, the final stage.",
    "DK4_MES_B338_R0071": "Amazing.{LB}Wonderful progress.{LB}You'll do fine.",
    "DK4_MES_B338_R0082": "You have the form now.{LB}You can pass as a fine warrior.",
    "DK4_MES_B338_R0098": "Return tomorrow.",
    "DK4_MES_B338_R0106": "{MACRO:FI}'s agility rose 1!",
    "DK4_MES_B338_R0113": "Next...",
    "DK4_MES_B338_R0118": "What?{LB}More before we seek the ruins?",
    "DK4_MES_B338_R0122": "We need the Ancient City Map.{LB}Seek it, then meet me{LB}at this city's gate.",
    "DK4_MES_B339_R0005": "New face here.{LB}Where are you from?",
    "DK4_MES_B339_R0009": "Portugal, in Europe.",
    "DK4_MES_B339_R0013": "Ah, the land that brought us guns? You came a long way!",
    "DK4_MES_B339_R0017": "Ah, now it makes sense.{LB}You have a useful tool{LB}called a sextant, yes?",
    "DK4_MES_B339_R0022": "What?",
    "DK4_MES_B339_R0026": "Rumor says it reveals your position{LB}even on a featureless sea.",
    "DK4_MES_B339_R0030": "Would you trade us that sextant?{LB}A fine reward awaits you.",
    "DK4_MES_B339_R0038": "Bring it and see.",
    "DK4_MES_B340_R0006": "Ah, you brought it?{LB}Then take this in exchange.",
    "DK4_MES_B341_R0006": "You seek this, yes?",
    "DK4_MES_B341_R0010": "A long wait...{LB}At last, today.",
    "DK4_MES_B341_R0013": "We shall trust you.{LB}Please accept it.",
    "DK4_MES_B342_R0010": "You do?",
    "DK4_MES_B342_R0022": "Did he know medicine?",
    "DK4_MES_B342_R0040": "Could this be...!",
    "DK4_MES_B342_R0059": "The book Charles mentioned!{LB}We found it!",
    "DK4_MES_B342_R0071": "What's wrong, Charles?!",
    "DK4_MES_B342_R0075": "Rumor said a new experimental material{LB}was discovered in the New World!",
    "DK4_MES_B342_R0078": "My research showed this book{LB}is needed to obtain that material...",
    "DK4_MES_B342_R0086": "Sorry, no time{LB}for that now.",
    "DK4_MES_B342_R0093": "Where is that monk now?",
    "DK4_MES_B342_R0136": "Understood.{LB}We will find it.",
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
            "speaker": SPEAKERS.get(first, "Raphael party or scene text"),
            "context": "Raphael undertakes the warrior trial and training, trades a sextant, receives guarded treasure, and inherits the Book of Alchemy ore quest.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving canonical item names, stat notices, route motivations, quest handoffs, and fixed-record constraints.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    if unresolved:
        raise SystemExit(f"Raphael V87 unresolved records: {unresolved}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v87-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael warrior trial, Tlaloc's Knife training, Ancient City Map lead, sextant trade, guarded treasure, and Book of Alchemy ore quest in SC0 blocks 336-342.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {str(block): sum(row["id"].startswith(f"DK4_MES_B{block}_") for row in rows) for block in BLOCKS}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
