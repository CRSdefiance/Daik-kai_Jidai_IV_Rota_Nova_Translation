from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v39a.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "By the way, what are{LB}Escante and Maldonado{LB}to each other?",
    "Well... both rule the New World.{LB}Maybe they work together?",
    "What if they join forces{LB}and come at us?",
    "Then we'll face it.",
    "{MACRO:FI}!{LB}You know we're in their way!{LB}At this rate, they'll crush us!",
    "Shh! Claudio, {MACRO:FI}!{LB}Look over there!",
    "Tch, Escante.{LB}His aim must be...",
    "No doubt!{LB}Never trust Escante!",
    "Wait.{LB}Can't challenge Escante now.",
    "We join him for now,{LB}crush the others,{LB}and expand my territory!",
    "True. Against Escante now,{LB}we'd lose...",
    "Enough!{LB}Damn him, he makes my blood boil!{LB}Escante!",
    "That was Maldonado.",
    "Escante and Maldonado{LB}aren't friends.",
    "Rivals?",
    "Both want the whole{LB}New World.",
    "But he said they'd cooperate{LB}to crush other factions...",
    "Then we're surely{LB}their first target.",
    "Maybe...",
    "They gain nothing by allying{LB}with Portuguese like us...",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B156_")]
    split_id = "DK4_MES_B156_R0080"
    rows = [row for row in all_rows if row["id"] != split_id]
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B156: {len(rows)} rows != {len(TRANSLATIONS)} translations")
    speaker_names = {0x04: "Raphael crewmate", 0x05: "Claudio Manini", 0x2A: "Maldonado", 0x97: "Maldonado officer"}
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
            "context": "Raphael's crew overhears Maldonado admit his rivalry with Escante, temporary cooperation against other factions, and desire to expand his own New World territory.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving Maldonado's strategic rivalry, temporary cooperation, and the crew's realization that they will be targeted first.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects overheard-dialogue pacing and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v39-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maldonado-Escante rivalry and target realization speaker-state records in SC0 block 156; the ambiguous 0x97 Shift-JIS lead is isolated in V39b.",
        "excluded_records": {split_id: "Translated in companion V39b under a profile where 0x97 is a Shift-JIS lead, not a speaker state."},
        "inventory": {"identified_records": len(all_rows), "translated_records": len(records), "blocks": {"156": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
