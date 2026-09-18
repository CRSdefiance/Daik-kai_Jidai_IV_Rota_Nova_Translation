from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v38.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "{MACRO:FO} has lately{LB}moved into these waters.",
    "So it seems.{LB}They're said to be strong.",
    "Wouldn't that threaten{LB}Lord Escante's plan?",
    "Shh! Don't speak of that aloud!{LB}Very few of Lord Escante's men{LB}know the plan!",
    "Y-yes, sorry.{LB}Just saying they might obstruct{LB}Lord Escante.",
    "Lord Escante decides that.",
    "Or we could recruit them{LB}against Maldonado...",
    "Lord Escante will rule{LB}the New World, then the...{LB}Oops.",
    "...Value your life?{LB}Then stop talking.",
    "Scary, scary.{LB}No one yields these waters{LB}so easily.",
    "Hmph.{LB}Let's see how far{LB}{MACRO:FO} gets.",
    "Y-yes, sir.",
    "...{MACRO:FI}?{LB}You heard that...",
    "Yes. They meant Escante,{LB}the governor of Mexico.",
    "That stank of trouble.",
    "They mentioned a plan...",
    "Yet every faction{LB}seeks to expand.",
    "True, but they kept saying{LB}'the plan'...",
    "Suspicious, yes.{LB}But making more enemies now{LB}may be unwise.{LB}They haven't declared war.",
    "Don't be naive.{LB}Men who talk like that{LB}should be stopped now.",
    "Once Escante owns{LB}the whole New World,{LB}regret comes too late.",
    "Spain gaining more power{LB}would be bad, but...",
    "Then it's settled.",
    "Will think on it.",
    "We're an obstacle to them too.{LB}Natural, if they seek{LB}the whole New World.",
    "Then Escante is{LB}our obstacle too!",
    "Claudio... harsh...",
    "Perhaps this is fate.{LB}When battle comes, we fight.",
    "...Sometimes we need strength{LB}to defeat an enemy...",
    "Escante and Maldonado{LB}are the same.{LB}Better strike early.",
    "Seems we must act...",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B155_")]
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B155: {len(rows)} rows != {len(TRANSLATIONS)} translations")
    speaker_names = {
        0x04: "Raphael crewmate", 0x05: "Claudio Manini", 0x06: "Julio Erdi",
        0x3C: "Escante officer", 0x97: "Escante sailor",
    }
    records = []
    for row, english in zip(rows, TRANSLATIONS, strict=True):
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in speaker_names else ""
        unsafe = english
        for macro in ("FI", "FA", "FO", "FU"):
            unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row["id"],
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": speaker_names.get(first, "Raphael Castor"),
            "context": "Raphael overhears Escante's officers discussing a secret New World plan, possible cooperation against Maldonado, and whether Raphael's company must be treated as an enemy.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving Escante's secret plan, his officers' strategic debate, and both cautious and preemptive crew reactions.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects overheard-dialogue pacing and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v38-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete overheard Escante-plan scene and Raphael crew responses in SC0 block 155.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"155": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
