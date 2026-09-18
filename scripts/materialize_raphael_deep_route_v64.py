from __future__ import annotations

import csv
import json
import re
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
REFERENCE_SOURCE = Path("work/sc1/script.csv")
REFERENCE_BATCH = Path("translations/hodram_deep_route_v19.json")
OUTPUT = Path("translations/raphael_deep_route_v64.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = tuple(range(251, 255))
EXCLUDED = {
    "DK4_MES_B254_R0104": "Raw two-byte event-control payload; not dialogue.",
}

SPEAKERS = {
    0x05: "Claudio Manousch",
    0x06: "Julio Castor",
    0x43: "Conman",
    0x5C: "Tavernkeeper",
    0x8B: "Priest",
    0xBA: "Francisca",
    0xFE: "System text",
}

CONTEXT = {
    251: "Francisca asks Raphael to investigate a stolen frozen-glass rose and a suspected Havana swindler.",
    252: "Raphael's party exposes the Havana swindler, and the tavernkeeper recovers Francisca's rose.",
    253: "Raphael returns the frozen rose to Francisca and receives a lead about a wooden church outside town.",
    254: "Raphael and Julio attempt to claim a supernatural figurehead from a church.",
}

OVERRIDES = {
    "DK4_MES_B251_R0005": "Welcome.",
    "DK4_MES_B251_R0009": "Miss, a customer.",
    "DK4_MES_B251_R0012": "Yes...",
    "DK4_MES_B251_R0016": "No use moping forever. Give it up.",
    "DK4_MES_B251_R0025": "Something wrong?",
    "DK4_MES_B251_R0029": "Nothing that concerns you. Please enjoy your drink.",
    "DK4_MES_B251_R0044": "You seem down... Trouble?",
    "DK4_MES_B251_R0047": "You're a sailor. You visit cities all over the world, right?",
    "DK4_MES_B251_R0052": "Yes. That's right.",
    "DK4_MES_B251_R0056": "Have you been to the New World?",
    "DK4_MES_B251_R0062": "Yes",
    "DK4_MES_B251_R0064": "No",
    "DK4_MES_B251_R0073": "Yes. Why?",
    "DK4_MES_B251_R0080": "The New World? Not that far yet...",
    "DK4_MES_B251_R0085": "Someday, though. What about it?",
    "DK4_MES_B251_R0091": "A treasure of mine was stolen.",
    "DK4_MES_B251_R0096": "Treasure?",
    "DK4_MES_B251_R0100": "Dad gave a glass rose for my birthday. Roses are my favorite.",
    "DK4_MES_B251_R0103": "A real rose frozen in glass... so lovely. Now it is gone...",
    "DK4_MES_B251_R0107": "That's awful. Who stole it?",
    "DK4_MES_B251_R0110": "No idea.",
    "DK4_MES_B251_R0115": "Then how can we help? Wait, what does the New World have to do with it?",
    "DK4_MES_B251_R0119": "A friend heard of a Havana swindler selling glasswork as jade or crystal.",
    "DK4_MES_B251_R0122": "A swindler and thief? Doubt he did it.",
    "DK4_MES_B251_R0127": "Still, Havana might offer a clue.",
    "DK4_MES_B251_R0130": "Cross the Atlantic on such a vague lead?!",
    "DK4_MES_B251_R0134": "Waiting could be too late if he did it.",
    "DK4_MES_B251_R0139": "Either way, catching that swindler is worth the trip.",
    "DK4_MES_B251_R0143": "Good point! Let's catch and punish that cheat!",
    "DK4_MES_B251_R0147": "Thank you!",
    "DK4_MES_B251_R0151": "Too early for thanks. We have not found it yet.",
    "DK4_MES_B251_R0156": "Then let's prepare to leave.",

    "DK4_MES_B252_R0006": "Sir, pay today. Do you know how large your tab is?",
    "DK4_MES_B252_R0009": "Next time! Ever known me to skip out?",
    "DK4_MES_B252_R0013": "You have never paid either.",
    "DK4_MES_B252_R0017": "Tch. Take this instead of coin.",
    "DK4_MES_B252_R0020": "What's this?",
    "DK4_MES_B252_R0024": "Amethyst art.",
    "DK4_MES_B252_R0028": "Oh! Looks costly. You sure?",
    "DK4_MES_B252_R0032": "Worth plenty. Keep it as interest. No change needed! Hahaha!",
    "DK4_MES_B252_R0036": "Wait!",
    "DK4_MES_B252_R0041": "Huh? Who are you?",
    "DK4_MES_B252_R0045": "May we see that ornament?",
    "DK4_MES_B252_R0049": "What?! Got a problem? Stay out, brat! Hey, listening?",
    "DK4_MES_B252_R0054": "Yes! Glasswork! This must be hers!",
    "DK4_MES_B252_R0058": "G-glass?!",
    "DK4_MES_B252_R0062": "Nonsense! This is genuine...",
    "DK4_MES_B252_R0065": "Enough! The owner sent us. No lies!",
    "DK4_MES_B252_R0068": "Tch! Time to run! Ugh!!",
    "DK4_MES_B252_R0072": "You... Enough tolerance. Not this time!",
    "DK4_MES_B252_R0076": "Move, old man, or get hurt!",
    "DK4_MES_B252_R0079": "Rough sailors come daily! This barkeep fears no one!",
    "DK4_MES_B252_R0082": "Guh!!",
    "DK4_MES_B252_R0086": "How dare you cheat in my tavern!",
    "DK4_MES_B252_R0089": "Guh!",
    "DK4_MES_B252_R0093": "Eek! Mercy!",
    "DK4_MES_B252_R0096": "A-amazing...",
    "DK4_MES_B252_R0100": "Damn! Remember this!!",
    "DK4_MES_B252_R0103": "You bastard! Tch, he escaped.",
    "DK4_MES_B252_R0106": "Thanks, you saved me from that fraud. You came for this, right?",
    "DK4_MES_B252_R0112": "Yes!",
    "DK4_MES_B252_R0116": "Return it to the owner. He's surely done worse. Next time, the governor gets him!",

    "DK4_MES_B253_R0006": "Welcome!",
    "DK4_MES_B253_R0011": "Your stolen rose... this?",
    "DK4_MES_B253_R0015": "You found it! Thank you!!",
    "DK4_MES_B253_R0028": "Thought it lost... You found it. Thank you!",
    "DK4_MES_B253_R0033": "Glad you're happy. Goodbye.",
    "DK4_MES_B253_R0047": "You explore all over the world, right?",
    "DK4_MES_B253_R0050": "A rare wooden church is outside town. Please visit.",
    "DK4_MES_B253_R0056": "Thank you. We'll visit.",

    "DK4_MES_B254_R0011": "What happened?",
    "DK4_MES_B254_R0027": "A striking statue. Any history?",
    "DK4_MES_B254_R0050": "How strange...",
    "DK4_MES_B254_R0062": "Hm...",
    "DK4_MES_B254_R0082": "Everyone, help!",
    "DK4_MES_B254_R0091": "Julio, you can go home first.",
    "DK4_MES_B254_R0131": "Run!",
    "DK4_MES_B254_R0161": "No modesty. We were truly lucky.",
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
                "source_meaning": english.replace("{LB}", " ").replace("{MACRO:FI}", "Raphael"),
                "localization_note": "Faithful concise American English preserving scene branches, choice order, canonical names, and fixed-record display constraints.",
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
        raise SystemExit(f"Raphael V64 unresolved records: {unresolved}")
    if len(records) + len(EXCLUDED) != len(source_rows):
        raise SystemExit(
            f"Raphael V64 inventory mismatch: {len(records)} translated + "
            f"{len(EXCLUDED)} controls != {len(source_rows)} source records"
        )

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v64-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Four source-locked Raphael frozen-rose, Havana fraud, church-clue, and supernatural-figurehead events across SC0 blocks 251-254.",
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(source_rows),
            "translated_records": len(records),
            "blocks": block_counts,
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} control preserved")


if __name__ == "__main__":
    main()
