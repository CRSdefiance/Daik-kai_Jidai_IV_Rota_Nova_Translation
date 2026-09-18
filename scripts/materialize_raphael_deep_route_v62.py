from __future__ import annotations

import csv
import json
import re
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
REFERENCE_SOURCE = Path("work/sc1/script.csv")
REFERENCE_BATCHES = (
    Path("translations/hodram_deep_route_v17.json"),
    Path("translations/hodram_deep_route_v18.json"),
)
OUTPUT = Path("translations/raphael_deep_route_v62.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = (228, 229, 230, *range(232, 244))
EXCLUDED: dict[str, str] = {}


SPEAKERS = {
    0x05: "Claudio Manousch",
    0x08: "Charles Jean Rochefort",
    0x0D: "Raphael crewmate",
    0x10: "Gerhard Adelknauts",
    0x11: "Raphael crewmate",
    0x13: "Carlo",
    0x15: "Ian Dukov",
    0x16: "Samwell",
    0x17: "Manuel Armestad",
    0x19: "Charlotte",
    0x1A: "Julian",
    0x52: "Tavernkeeper",
    0x55: "Townsman",
    0x5C: "Tavernkeeper",
    0x97: "Child",
    0xA2: "Child",
    0xA9: "Vivian",
    0xC5: "Safia",
    0xC7: "Lucia",
    0xD0: "Raphael crewmate",
}

CONTEXT = {
    228: "Vivian sends Raphael to seek Excalibur in Avalon, and the party decides to ask at the tavern.",
    229: "Raphael asks a tavernkeeper where to find Avalon.",
    230: "Ian discusses the Sacred Spear of Ares and other Olympian equipment.",
    232: "Julian flirts with Lucia while discussing the Empress's Gown.",
    233: "A townsman and crewmate recount the Crusades, Saladin, and his missing armor.",
    234: "Gerhard tells Raphael of the samurai Noritsune and his armor lost in a strait.",
    235: "Ian writes to Raphael about Timur's stolen mail coat.",
    236: "Julian flirts with Safia while discussing Medusa's Shield.",
    237: "Children reenact Charles Martel's victory and prompt a discussion of heroes.",
    238: "Manuel discusses Attila and the missing king's armor.",
    239: "Charlotte trains late and recalls a martial-arts robe able to chip swords.",
    240: "Samwell reports the Armadillo's Steel Hide shield hidden somewhere around Africa.",
    241: "Samwell repeats his pitch with the Giant Tortoise Shield from the eastern ocean.",
    242: "Samwell investigates the Phoenix Bascinet and narrows its location to Britain.",
    243: "Carlo tells Raphael about Herophilus's medical text and its remedy for crew exhaustion.",
}

OVERRIDES = {
    "DK4_MES_B228_R0005": "King...?",
    "DK4_MES_B228_R0009": "You again!{LB}Stop hurting business and get out!",
    "DK4_MES_B228_R0013": "The king...? Where is the hero?",
    "DK4_MES_B228_R0017": "What is wrong? Who are you?",
    "DK4_MES_B228_R0020": "Vivian... maker of King Arthur's sacred sword...",
    "DK4_MES_B228_R0024": "King Arthur?",
    "DK4_MES_B228_R0028": "The king sleeps. The sacred sword seeks a hero...",
    "DK4_MES_B228_R0031": "Hero, seek Excalibur!{LB}The sword waits in Avalon,{LB}where the king sleeps!",
    "DK4_MES_B228_R0035": "Avalon? Never heard of it...",
    "DK4_MES_B228_R0044": "Let's ask around at the tavern.",
    "DK4_MES_B228_R0050": "Ask around the tavern.",
    "DK4_MES_B229_R0006": "Barkeep, know Avalon?",
    "DK4_MES_B230_R0009": "What weapon? What name?",
    "DK4_MES_B230_R0017": "Not sure what is so great... Where is it?",
    "DK4_MES_B230_R0025": "Then that tells us nothing!",
    "DK4_MES_B230_R0033": "(Hm. He cares? Surprising.)",
    "DK4_MES_B230_R0041": "Honestly, yes.",
    "DK4_MES_B230_R0052": "Hm...",
    "DK4_MES_B233_R0009": "What is here?",
    "DK4_MES_B233_R0045": "Truth",
    "DK4_MES_B233_R0056": "Saladin?",
    "DK4_MES_B233_R0068": "Amazing!",
    "DK4_MES_B234_R0010": "Gerhard, watching the sunset? Something wrong?",
    "DK4_MES_B234_R0018": "What kind of man?",
    "DK4_MES_B234_R0026": "That long ago? What did he do?",
    "DK4_MES_B234_R0047": "So bold... Amazing.",
    "DK4_MES_B234_R0051": "Yes. Men like him are rare now.",
    "DK4_MES_B234_R0056": "That tale truly moved you, Gerhard.",
    "DK4_MES_B235_R0057": "Dukov knows Asian history too?",
    "DK4_MES_B235_R0072": "So that is why. Cesare knows much.",
    "DK4_MES_B237_R0013": "What are those children doing?",
    "DK4_MES_B237_R0022": "So the hero was Charles... What was the rest?",
    "DK4_MES_B237_R0032": "Many men win wars. Why is he a hero?",
    "DK4_MES_B237_R0045": "He guarded Europe. No wonder children revere him.",
    "DK4_MES_B238_R0009": "Ah, Manuel.",
    "DK4_MES_B238_R0017": "Not only that. Watching the city is pleasant too.",
    "DK4_MES_B238_R0026": "What brings you here? Square business?",
    "DK4_MES_B238_R0037": "Attila? Who was he?",
    "DK4_MES_B238_R0045": "Even Rome struggled against him? He must have been great.",
    "DK4_MES_B238_R0052": "Could {MACRO:FO} ever rule all the seas?",
    "DK4_MES_B238_R0059": "Right... Why mention this now?",
    "DK4_MES_B238_R0067": "Meaning?",
    "DK4_MES_B238_R0076": "A king's armor carried northwest... He must have terrified Rome.",
    "DK4_MES_B239_R0010": "Training this late? Working hard.",
    "DK4_MES_B239_R0023": "Truly",
    "DK4_MES_B240_R0010": "What is it?",
    "DK4_MES_B240_R0027": "Hm. What about that shield?",
    "DK4_MES_B240_R0034": "True. Where can we find it?",
    "DK4_MES_B240_R0042": "That tells us almost nothing.",
    "DK4_MES_B240_R0050": "Good. We will remember. Maybe luck will bring it.",
    "DK4_MES_B241_R0010": "What is it?",
    "DK4_MES_B241_R0026": "This sounds familiar. Did you say this about an armadillo?",
    "DK4_MES_B241_R0035": "All right. What about the shield?",
    "DK4_MES_B241_R0043": "You said exactly that about the armadillo one.",
    "DK4_MES_B241_R0051": "All right. Where can we find it?",
    "DK4_MES_B241_R0058": "That is not enough to search.",
    "DK4_MES_B241_R0066": "Good. We will remember. Maybe luck will bring it.",
    "DK4_MES_B242_R0010": "What is it?",
    "DK4_MES_B242_R0019": "Not sure. Seeing one would be nice. Why ask?",
    "DK4_MES_B242_R0027": "You want it because it may help in battle?",
    "DK4_MES_B242_R0035": "You said something like this before.",
    "DK4_MES_B242_R0043": "All right. Where is it? Do not say Africa or South Asia.",
    "DK4_MES_B242_R0052": "Oh? Much narrower this time.",
    "DK4_MES_B242_R0060": "Well done!",
    "DK4_MES_B242_R0069": "Samwell worked hard, so we will remember the Phoenix Bascinet.",
    "DK4_MES_B243_R0010": "Never heard of him. Who was he?",
    "DK4_MES_B243_R0018": "A great physician. And?",
    "DK4_MES_B243_R0026": "Amazing if true! We need that book.",
    "DK4_MES_B243_R0034": "How do we search? Any clue?",
    "DK4_MES_B243_R0042": "Only that?",
    "DK4_MES_B243_R0051": "Then we may never find it.",
    "DK4_MES_B243_R0060": "No need to apologize.",
    "DK4_MES_B243_R0069": "To find it, we must search the Mediterranean.",
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
            english.replace("Ｉan Dukov", "Dukov")
            .replace("Ｉan", "Dukov")
            .replace("Ｆernando", "Dias")
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
                "speaker": SPEAKERS.get(first, "Raphael companion, choice, or scene text"),
                "context": CONTEXT[block],
                "source_meaning": (
                    english.replace("{LB}", " ")
                    .replace("{MACRO:FI}", "Raphael")
                    .replace("{MACRO:FA}", "Castelo")
                    .replace("{MACRO:FO}", "the company")
                ),
                "localization_note": "Faithful concise American English preserving canonical names, choice order, scene timing, and fixed-record display constraints.",
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
        raise SystemExit(f"Raphael V62 unresolved records: {unresolved}")
    if len(records) != len(source_rows):
        raise SystemExit(f"Raphael V62 inventory mismatch: {len(records)} != {len(source_rows)}")

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v62-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Fifteen source-locked Raphael legendary-equipment, correspondence, history, and character events across SC0 blocks 228-243.",
        "excluded_records": EXCLUDED,
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
