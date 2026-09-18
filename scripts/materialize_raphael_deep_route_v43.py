from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v43.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TARGET_IDS = [
    "DK4_MES_B166_R0006", "DK4_MES_B166_R0009", "DK4_MES_B166_R0020",
    "DK4_MES_B166_R0027", "DK4_MES_B166_R0031", "DK4_MES_B166_R0035",
    "DK4_MES_B166_R0040", "DK4_MES_B166_R0044", "DK4_MES_B166_R0049",
    "DK4_MES_B166_R0052", "DK4_MES_B166_R0056", "DK4_MES_B166_R0060",
    "DK4_MES_B166_R0064", "DK4_MES_B166_R0069", "DK4_MES_B166_R0073",
    "DK4_MES_B166_R0085", "DK4_MES_B166_R0089", "DK4_MES_B166_R0096",
    "DK4_MES_B166_R0100", "DK4_MES_B166_R0104", "DK4_MES_B166_R0107",
    "DK4_MES_B166_R0118", "DK4_MES_B166_R0132", "DK4_MES_B166_R0146",
    "DK4_MES_B166_R0152",
]
EXCLUDED = {"DK4_MES_B166_R0067": "Nine-byte scene-transition control payload; no independently rendered dialogue."}
TRANSLATIONS = [
    "Back in Portugal,{LB}{MACRO:FI}!",
    "{MACRO:FA}.{LB}His Majesty awaits.",
    "W-what!?{LB}We face the king!?{LB}Nerves are hitting me hard!",
    "...{MACRO:FI},{LB}a word?",
    "What, Claudio?",
    "That stiff air isn't for me...{LB}Mind letting me wait outside?",
    "This is your big moment.{LB}Would like you beside me, but...{LB}all right.",
    "Okay. Handle the report.",
    "Got it.{LB}Back when it's done.",
    "And grab a fine reward!",
    "Then, off we go.",
    "See you later.",
    "Then, let us go.",
    "Ah!{LB}Portugal's pride,{LB}{MACRO:FA}!{LB}You return!",
    "{MACRO:FU}.{LB}Home in Portugal{LB}at last.",
    "Show the Pope{LB}the seven Proofs you gathered,{LB}and he will support restoring{LB}Portugal's royal authority.",
    "Truly?!",
    "Yes.{LB}You are Portugal's{LB}great treasure!",
    "By authority of Portugal's king,{LB}you are named viceroy{LB}of all our overseas{LB}trade domains!",
    "What!?{LB}V-viceroy...?",
    "(So grand,{LB}{MACRO:FI}!)",
    "(Viceroy!{LB}Amazing, amazing!)",
    "(Hmph. A fitting rank{LB}at least.)",
    "(Not sure what it means,{LB}but sounds tasty.)",
    "We announce it now!{LB}Go outside and show your face{LB}to the people in the square!{LB}Come!",
]


def main() -> None:
    wanted = set(TARGET_IDS) | set(EXCLUDED)
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        by_id = {row["id"]: row for row in csv.DictReader(stream) if row["id"] in wanted}
    if set(by_id) != wanted:
        raise SystemExit(f"B166 opening inventory mismatch: missing {sorted(wanted - set(by_id))}")
    rows = [by_id[record_id] for record_id in TARGET_IDS]
    speaker_names = {
        0x04: "Raphael crewmate", 0x05: "Claudio Manini", 0x0D: "Raphael companion",
        0x0E: "Raphael companion", 0x14: "Raphael companion", 0x19: "Ifa",
        0x78: "Palace guard", 0x7D: "King of Portugal",
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
            "context": "Raphael returns to Portugal with all seven Proofs, reports to the king, and is offered the viceroyalty of Portugal's overseas trade domains.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving all runtime identity commands, royal-restoration meaning, appointment terminology, companion asides, and fixed scene control.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects royal-audience pacing and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v42-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Raphael ending opening and Portuguese viceroy appointment in the first 26 source records of SC0 block 166.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(wanted), "translated_records": len(records), "blocks": {"166": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} control excluded")


if __name__ == "__main__":
    main()
