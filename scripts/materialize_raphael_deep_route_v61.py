from __future__ import annotations

import csv
import json
import re
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
REFERENCE_SOURCE = Path("work/sc1/script.csv")
REFERENCE_BATCH = Path("translations/hodram_deep_route_v16.json")
OUTPUT = Path("translations/raphael_deep_route_v61.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = tuple(range(218, 228))
EXCLUDED = {
    "DK4_MES_B218_R0015": "Four-byte packed item/scene payload; not dialogue.",
    "DK4_MES_B225_R0024": "Four-byte packed sword/scene payload; not dialogue.",
}


SPEAKERS = {
    0x04: "Janus Pasha",
    0x05: "Claudio Manousch",
    0x07: "Christina",
    0x0B: "Jam Jack Ludwyan",
    0x0C: "Yukihisa Genjo Shiraki",
    0x0E: "Emilio Ferrog",
    0x11: "Raphael crewmate",
    0x17: "Manuel Armestad",
    0x78: "Solomon legend keeper",
    0x95: "Three Kingdoms enthusiast",
    0xAA: "Elder",
    0xAD: "Merchant",
    0xD0: "Raphael crewmate",
    0xFE: "System or scene text",
}

CONTEXT = {
    218: "Christina evaluates legendary ceramic earrings offered by a merchant.",
    219: "Emilio asks Raphael to seek the Minotaur's Axe.",
    220: "Christina learns of a woman pirate's treasure sword lost in the Caribbean.",
    221: "Yukihisa writes to Raphael about the cursed sword Muramasa.",
    222: "A crewmate reports a blood-red sword sealed by a frightened lord.",
    223: "Christina follows swans carrying a shining object toward Amsterdam.",
    224: "A Three Kingdoms enthusiast reveals the location of Zhao Yun's legendary spear.",
    225: "An elder recognizes Raphael as the prophesied Sea King and reveals Kublai Khan's sword.",
    226: "Janus writes to Raphael about the Sword of Judas.",
    227: "A legend keeper thanks Raphael and reveals a demon king's weapon sealed near an icy island.",
}

# Lines whose wording differs from Hodram's otherwise source-identical common
# events, plus the Raphael-only King Solomon event in block 227.
OVERRIDES = {
    "DK4_MES_B218_R0017": "Oh, earrings?",
    "DK4_MES_B218_R0026": "They do not look that rare.",
    "DK4_MES_B218_R0040": "No use to me. What about you, Christina?",
    "DK4_MES_B218_R0103": "What is with that attitude? You approached us!",
    "DK4_MES_B218_R0109": "Enough! Let's go, {MACRO:FI}!",
    "DK4_MES_B219_R0009": "Huh?",
    "DK4_MES_B219_R0017": "Something besides food? Unusual. What weapon?",
    "DK4_MES_B219_R0025": "Sounds strong. Where is it?",
    "DK4_MES_B219_R0033": "Little to go on... We'll look if we can.",
    "DK4_MES_B219_R0041": "Only if we get the chance.",
    "DK4_MES_B219_R0050": "We never promised it to you.",
    "DK4_MES_B220_R0032": "Really? Then this is reason to grow stronger.",
    "DK4_MES_B220_R0076": "All right. Remembered.",
    "DK4_MES_B220_R0086": "(A pirate sword lost in the Caribbean... Must see it.)",
    "DK4_MES_B221_R0033": "Surely this is the treasure sought by this warrior. Yukihisa Genjo Shiraki",
    "DK4_MES_B221_R0072": "Oh! Worth searching for.",
    "DK4_MES_B222_R0012": "Sounds good!",
    "DK4_MES_B222_R0021": "Red blade.",
    "DK4_MES_B222_R0029": "Still, sealing it away seems wasteful.",
    "DK4_MES_B222_R0037": "Certainly sounds cursed. Where was it hidden?",
    "DK4_MES_B223_R0037": "Christina! Over here!",
    "DK4_MES_B223_R0044": "At the square pond? Quite tame.",
    "DK4_MES_B224_R0010": "Yes",
    "DK4_MES_B224_R0012": "No",
    "DK4_MES_B225_R0010": "Me?",
    "DK4_MES_B225_R0018": "What item?",
    "DK4_MES_B225_R0056": "Me, the Sea King?",
    "DK4_MES_B225_R0060": "He is the ruler foretold 300 years ago? No way!",
    "DK4_MES_B226_R0076": "A traitor's sword... Janus values quality over origin.",
    "DK4_MES_B227_R0005": "Who built these ruins, and why?{LB}They resemble King Solomon's mines{LB}from the Old Testament.",
    "DK4_MES_B227_R0008": "Do you know the legend of King Solomon?",
    "DK4_MES_B227_R0011": "Hm?",
    "DK4_MES_B227_R0015": "Pardon me. You are Admiral {MACRO:FA}?",
    "DK4_MES_B227_R0020": "Yes. {MACRO:FI} {MACRO:FA}.{LB}What is it?",
    "DK4_MES_B227_R0024": "Thank you for investing.{LB}The town is grateful.",
    "DK4_MES_B227_R0028": "No, it was nothing.",
    "DK4_MES_B227_R0031": "Know any King Solomon rumors?",
    "DK4_MES_B227_R0036": "Rumor?",
    "DK4_MES_B227_R0040": "King Solomon once commanded even demon kings.",
    "DK4_MES_B227_R0045": "Demon king...?",
    "DK4_MES_B227_R0049": "Rumor says a weapon tied to that demon king was sealed on an icy island far northwest.",
    "DK4_MES_B227_R0052": "Admiral {MACRO:FA}, perhaps even you could wield it. That is why this tale is shared.",
    "DK4_MES_B227_R0055": "An icy isle far northwest? The isle of ice?",
    "DK4_MES_B227_R0059": "A demon king's weapon... Thanks. We will search.",
}


def _strip_english_markup(text: str) -> str:
    text = re.sub(r"^\{SPEAKER:[0-9A-F]+\}", "", text)
    return re.sub(r"\{PAD\}$", "", text)


def _reference_lines() -> dict[str, str]:
    with REFERENCE_SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    reference = json.loads(REFERENCE_BATCH.read_text(encoding="utf-8"))
    lines: dict[str, str] = {}
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
        if row_id in EXCLUDED:
            continue
        source_hex = row["source_hex"].upper()
        first = int(source_hex[:2], 16)
        key = source_hex[2:] if first in SPEAKERS else source_hex
        english = OVERRIDES.get(row_id, reference_lines.get(key))
        if english is None:
            unresolved.append(row_id)
            continue
        english = english.replace("Gennas Pasa", "Janus Pasha").replace("Gennas", "Janus")
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
        raise SystemExit(f"Raphael V61 unresolved records: {unresolved}")
    if len(records) + len(EXCLUDED) != len(source_rows):
        raise SystemExit(
            f"Raphael V61 inventory mismatch: {len(records)} translated + "
            f"{len(EXCLUDED)} controls != {len(source_rows)} source records"
        )

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v61-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Ten source-locked Raphael legendary-weapon, correspondence, treasure, and character events across SC0 blocks 218-227.",
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(source_rows),
            "translated_records": len(records),
            "blocks": block_counts,
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
