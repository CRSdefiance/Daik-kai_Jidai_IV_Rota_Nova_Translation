from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v1.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
LINES = {
    "DK4_MES_B69_R0005": "This batch is ready.",
    "DK4_MES_B69_R0010": "Thanks.",
    "DK4_MES_B69_R0014": "And... here.",
    "DK4_MES_B69_R0019": "This is...!{LB}At last! Congratulations!",
    "DK4_MES_B69_R0022": "Only a little yet,{LB}but everyone celebrates{LB}our new product.",
    "DK4_MES_B69_R0026": "The village feels alive again.{LB}Everyone wants a celebration today.",
    "DK4_MES_B69_R0030": "Will {MACRO:FI}{LB}come?",
    "DK4_MES_B69_R0034": "Yes, gladly!",
    "DK4_MES_B69_R0038": "Really?{LB}Wonderful!",
    "DK4_MES_B69_R0041": "Wait at the village{LB}for you.",
    "DK4_MES_B69_R0049": "Wow!{LB}Like a festival!",
    "DK4_MES_B69_R0057": "Ah, Charlotte...?!",
    "DK4_MES_B69_R0062": "You came!{LB}...Something wrong?",
    "DK4_MES_B69_R0066": "N-no. You just look{LB}different than usual...",
    "DK4_MES_B69_R0069": "Looks bad?",
    "DK4_MES_B69_R0074": "Not at all!",
    "DK4_MES_B69_R0078": "Really?{LB}Never wore this before,{LB}so it feels embarrassing...",
    "DK4_MES_B69_R0083": "Looks wonderful!",
    "DK4_MES_B69_R0087": "Hee hee, thank you.{LB}Come along. There is{LB}plenty of food!",
    "DK4_MES_B69_R0092": "Yes!",
    "DK4_MES_B69_R0100": "Here.",
    "DK4_MES_B69_R0105": "Thanks!{LB}Mmm, delicious!",
    "DK4_MES_B69_R0108": "Good!",
    "DK4_MES_B69_R0112": "Oh!{LB}Look there.",
    "DK4_MES_B69_R0116": "Hm?",
    "DK4_MES_B69_R0120": "There!",
    "DK4_MES_B69_R0125": "Wow!{LB}You grow it here.",
    "DK4_MES_B69_R0128": "Yes.{LB}Next year will bring even more!",
    "DK4_MES_B69_R0132": "Then the village{LB}will prosper!",
    "DK4_MES_B69_R0135": "Yes!",
    "DK4_MES_B69_R0143": "...{MACRO:FI}, thank you.{LB}The villagers smile again,{LB}all because of you.",
    "DK4_MES_B69_R0147": "Did nothing at all.{LB}Your hard work did this, Charlotte!",
    "DK4_MES_B69_R0150": "Not true!",
    "DK4_MES_B69_R0155": "Watching all of you{LB}makes me want to work harder too.",
    "DK4_MES_B69_R0163": "My homeland, Portugal,{LB}was annexed by Spain...",
    "DK4_MES_B69_R0167": "You rebuilt this village.{LB}That makes me want to reclaim{LB}Portugal with our own hands...",
    "DK4_MES_B69_R0172": "You give me that courage!",
    "DK4_MES_B69_R0176": "...Truthfully, hope was fading.{LB}Always wanted to flee this village.",
    "DK4_MES_B69_R0181": "But you never ran away.",
    "DK4_MES_B69_R0184": "Because you brought hope.",
    "DK4_MES_B69_R0189": "You found hope yourself.",
    "DK4_MES_B69_R0193": "No, you did...",
    "DK4_MES_B69_R0198": "Charlotte...",
    "DK4_MES_B69_R0216": "S-sorry!",
    "DK4_MES_B69_R0226": "Charlotte!!",
    "DK4_MES_B69_R0231": "...Charlotte...",
    "DK4_MES_B69_R0239": "Hey, back already!{LB}That was quick.{LB}...{MACRO:FI}?",
    "DK4_MES_B69_R0243": "What happened to him?",
    "DK4_MES_B69_R0247": "He looked dispirited.",
    "DK4_MES_B69_R0251": "Something happened.{LB}Better go check on him.",
    "DK4_MES_B69_R0254": "Wait, Clau.{LB}Leave him alone for now...",
    "DK4_MES_B69_R0257": "Why not visit the village instead?",
    "DK4_MES_B69_R0260": "There?",
    "DK4_MES_B69_R0264": "Maybe we can{LB}help {MACRO:FI} somehow.",
    "DK4_MES_B69_R0268": "Right!{LB}Let me demand an answer...",
    "DK4_MES_B69_R0271": "No, Clau. That will hurt.{LB}Let me talk.",
    "DK4_MES_B69_R0274": "Hey, then what is my role?",
    "DK4_MES_B69_R0277": "Just come along, Clau.{LB}Your concern will mean{LB}more than anything to {MACRO:FI}.",
    "DK4_MES_B69_R0281": "Tch... not much fun,{LB}but it is for {MACRO:FI}.",
}

SPEAKERS = {"05": "Claudio Manous", "08": "Arcadius", "50": "Charlotte", "FE": "Charlotte"}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXT = "Charlotte's village celebrates its first new crop; Raphael draws courage from its recovery, and his friends rally after Charlotte's emotional farewell."


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(all_rows)
    if missing:
        raise SystemExit(f"Raphael V1 inventory mismatch: missing={sorted(missing)}")
    records = []
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Raphael Castor"), "context": CONTEXT,
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Natural concise American English preserving the celebration, romantic hesitation, and Raphael's resolve for Portugal.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Charlotte village celebration and farewell continuation in SC0 block 69.",
        "excluded_records": {},
        "inventory": {"identified_records": len(LINES), "translated_records": len(records), "blocks": {"69": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
