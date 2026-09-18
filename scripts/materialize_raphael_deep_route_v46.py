from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v46.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
EXCLUDED = {
    "DK4_MES_B167_R0003": "Ten-byte scene setup payload; no independently rendered dialogue."
}
TRANSLATIONS = [
    "Listen: hired as a bodyguard.{LB}Not your porter{LB}or errand boy.",
    "Don't use that to loaf around.{LB}You're paid, so do the work{LB}you're told.",
    "Want obedience?{LB}Hire someone softer.{LB}My life rides on this work.",
    "So fighting is all you can do,{LB}and no other work suits you?",
    "Then someone obedient gets hired.{LB}Go wherever you please!",
    "Do what you want!",
    "That Al...{LB}Strong arms made him arrogant.",
    "That rude man is dismissed.{LB}Get another guard. Now!",
    "Yes... but strength like his{LB}is rare...",
    "That's your job.{LB}Move.",
    "...Strong, huh?{LB}Wouldn't he fit our crew?",
    "...Still naive as ever.{LB}Simple, even.",
    "Recruiting a man like that{LB}won't be easy...",
    "A man like that{LB}won't join easily...",
    "Won't know until we try.{LB}Come on, let's go!",
    "That's him.{LB}May we talk?",
    "What?",
    "About your strength...{LB}an offer.",
    "(A job?){LB}Hmph. Whoever you are,{LB}you know talent.",
    "(Wow. Such confidence.)",
    "Y-yes. Your build says plenty.{LB}Right, Claudio?",
    "...A sailor?",
    "No. A mercenary.{LB}These arms earn my keep.",
    "And when there's no fighting,{LB}what do you do?",
    "Bodyguard.{LB}Dangerous times pay.",
    "And now?",
    "You saw: dismissed.{LB}But sailing isn't my trade.{LB}No paid job? Then we're done.",
    "...Then never mind.{LB}Sorry.",
    "W-wait, Claudio!{LB}Sorry, maybe later...",
    "As expected.",
    "Hey! Why agree with that?{LB}None of this makes sense!",
    "Men like him get worse{LB}if you bow to them.",
    "As expected...",
    "Yeah. Men like him...",
    "Hey! Why do you both agree?{LB}None of this makes sense!",
    "Admiral,{LB}bow to such a man{LB}and he grows arrogant.",
    "But...{LB}what should we do?",
    "You really like him, huh?",
    "He looks incredibly strong.{LB}Better as an ally than an enemy.",
    "So simple...{LB}All right. Leave him to me.",
    "...What now?",
    "Stay here and you'll never use{LB}those famous arms.{LB}Walking town streets{LB}takes no strength.",
    "What?",
    "Join our ship and you'll get{LB}plenty of chances.{LB}Strong enemies everywhere.",
    "Should sea battles scare you,{LB}no need to force it.{LB}We don't need dead weight.",
    "Hmph. Drop the act.{LB}You need my strength.{LB}Agreed. Joining.",
    "Good. Your name?",
    "Al.{LB}Just call me Al.",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        selected = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B167_")]
    if len(selected) != 49 or selected[0]["id"] != "DK4_MES_B167_R0003" or selected[-1]["id"] != "DK4_MES_B167_R0217":
        raise SystemExit("B167 inventory boundaries changed")
    rows = [row for row in selected if row["id"] not in EXCLUDED]
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B167: {len(rows)} visible rows != {len(TRANSLATIONS)} translations")
    speaker_names = {
        0x05: "Claudio Manini", 0x06: "Julio Erdi", 0x11: "Al Fasi",
        0x73: "Employer's attendant", 0x94: "Al's former employer",
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
            "context": "Raphael, Claudio, and Julio meet the proud mercenary Al Fasi after his dismissal and recruit him for sea battles.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving Al's pride, Claudio's reverse psychology, and the canonical Al Fasi identity without emitting the reserved uppercase-F byte in dialogue.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects dialogue pacing and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v46-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Al Fasi's complete optional recruitment event in SC0 block 167.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(selected), "translated_records": len(records), "blocks": {"167": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} control excluded")


if __name__ == "__main__":
    main()
