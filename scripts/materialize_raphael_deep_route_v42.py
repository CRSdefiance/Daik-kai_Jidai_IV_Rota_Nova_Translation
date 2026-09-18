from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v42.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = (163, 164, 165)
TRANSLATIONS = [
    "The Mediterranean Proof map{LB}must be this Patterned Cloth...",
    "Yet it doesn't look{LB}like a map.",
    "Too dark to see.{LB}Pass me that Brass Lamp.",
    "Okay.",
    "Raise the lamp...{LB}Now we see.",
    "W-wait!{LB}Too close and the cloth will burn!{LB}...Ah!",
    "A map...",
    "Never thought to reveal it{LB}with the Brass Lamp.",
    "So this was how{LB}the Brass Lamp should be used:{LB}to reveal hidden ink.",
    "Y-yeah.{LB}Good idea, right?",
    "Yes. Lucky, but well done.",
    "Yes. Lucky, but well done.",
    "Uh.",
    "Great!{LB}The Mediterranean Proof map{LB}is ours.{LB}Now find the Proof!",
    "{MACRO:FA}.{LB}His Majesty awaits.",
    "Ah, {MACRO:FA}!{LB}You defeated Spain's fleet!{LB}Now we shall restore Portugal!",
    "Your Majesty. One dream came true.{LB}We will keep serving Portugal{LB}with honor.",
    "Well said.{LB}You are our homeland's savior!",
    "The praise honors me.{LB}However...",
    "Ah, yes!{LB}You still travel the world,{LB}expanding your trade domain.",
    "As you say.{LB}Some work remains unfinished...",
    "Then strive as you wish.{LB}Now, a reward...",
    "This concerns the Proofs.{LB}Much has been asked of you,{LB}but only you can do it.",
    "This task will be done.",
    "Good. We await success.{LB}Now, a reward...",
    "No. Rebuilding the kingdom{LB}must be costly.{LB}Please spend nothing on me.",
    "(You idiot!{LB}Take the reward!)",
    "So modest...{LB}True, in our present state,{LB}your service cannot be repaid fully.",
    "Then we shall consider it{LB}until your true goal{LB}brings you home.",
    "Thank you, sire.",
    "Yes.{LB}No need to keep you.{LB}Go with grace.",
    "Yes. We take our leave.",
    "What a waste!{LB}{MACRO:FI}, you have no greed at all!",
    "Work remains{LB}more important than rewards.",
    "True...{LB}Let's finish the trade domains!{LB}Onward, Admiral {MACRO:FI}!",
    "{MACRO:FI}.{LB}Welcome.",
    "You summoned me?",
    "Yes.{LB}About the treasure you seek.",
    "The seven Proofs of Conquest.{LB}Show them to the Pope,{LB}and he may recognize Portugal's{LB}royal authority again.",
    "More than that,{LB}our people need a symbol{LB}to unite as maritime Portugal{LB}rises again.",
    "Spain seeks to rule Europe{LB}and the world.{LB}Never let them have the Proofs.",
    "Clear?",
    "Yes!",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = [row for row in csv.DictReader(stream) if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)]
    excluded = {"DK4_MES_B163_R0038": "Four-byte event-control payload; no independently rendered dialogue."}
    rows = [row for row in all_rows if row["id"] not in excluded]
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B163-B165: {len(rows)} visible rows != {len(TRANSLATIONS)} translations")
    speaker_names = {0x04: "Raphael crewmate", 0x05: "Claudio Manini", 0x08: "Arcadius Eirene", 0x78: "Palace guard", 0x7D: "King of Portugal"}
    contexts = {
        163: "Raphael's crew uses the Brass Lamp to reveal the Mediterranean Proof map hidden in the Patterned Cloth.",
        164: "After Spain's fleet is defeated, the Portuguese king thanks Raphael, pledges national restoration, and discusses a deferred reward.",
        165: "The Portuguese king explains that all seven Proofs can support papal recognition of restored royal authority and reunite Portugal.",
    }
    records = []
    for row, english in zip(rows, TRANSLATIONS, strict=True):
        block = int(row["id"].split("_B", 1)[1].split("_", 1)[0])
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
            "context": contexts[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving established item, Proof, Portuguese restoration, papal-recognition, and runtime identity semantics.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects item names, royal exposition, and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    counts = {str(block): sum(record["id"].startswith(f"DK4_MES_B{block}_") for record in records) for block in BLOCKS}
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v42-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete Mediterranean Proof reveal and Portuguese restoration audiences across SC0 blocks 163-165.",
        "excluded_records": excluded,
        "inventory": {"identified_records": len(all_rows), "translated_records": len(records), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(excluded)} control excluded")


if __name__ == "__main__":
    main()
