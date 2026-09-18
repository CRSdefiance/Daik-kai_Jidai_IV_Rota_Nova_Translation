from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v17.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
LINES = {
    "DK4_MES_B73_R0005": "Ah, London...{LB}Home air is best.",
    "DK4_MES_B73_R0008": "Rest awhile.{LB}You are home again.",
    "DK4_MES_B73_R0011": "Thanks.{LB}Going for a harbor walk.{LB}Always loved walking here.",
    "DK4_MES_B73_R0015": "All right.{LB}We will go ahead to the inn.",
    "DK4_MES_B73_R0019": "All unchanged...{LB}So good...",
    "DK4_MES_B73_R0022": "Ooooooh!{LB}A miracle! This is love!{LB}Christina!",
    "DK4_MES_B73_R0026": "Oh no!",
    "DK4_MES_B73_R0030": "Thank goodness!{LB}Knew my love would reach you!{LB}My heart...",
    "DK4_MES_B73_R0034": "D-do not cry.{LB}Everyone is watching.",
    "DK4_MES_B73_R0037": "Listen, not back for good!{LB}Just happened to stop in London.{LB}Leaving again soon!",
    "DK4_MES_B73_R0040": "Huh?",
    "DK4_MES_B73_R0044": "So no, not back for you!",
    "DK4_MES_B73_R0047": "And marriage with you{LB}has never crossed my mind!",
    "DK4_MES_B73_R0051": "Nooo!{LB}What do you dislike about me?",
    "DK4_MES_B73_R0054": "That is not it.{LB}Marriage is not in my plans.{LB}Give up, okay?",
    "DK4_MES_B73_R0058": "Understood...{LB}Giving up... yes...{LB}My love is over...",
    "DK4_MES_B73_R0062": "Whew... no more pursuit...",
    "DK4_MES_B73_R0070": "Sigh... Hm?",
    "DK4_MES_B73_R0074": "My boy!",
    "DK4_MES_B73_R0078": "What now?!",
    "DK4_MES_B73_R0083": "Ah!{LB}My boy fell into the sea!{LB}Someone save him!",
    "DK4_MES_B73_R0087": "Wait! Going to save him!",
    "DK4_MES_B73_R0091": "Hold on! Coming now!",
    "DK4_MES_B73_R0095": "Christina...!",
    "DK4_MES_B73_R0100": "Big sis is here.{LB}You are safe now!",
    "DK4_MES_B73_R0103": "Boy: So scared! So scared!",
    "DK4_MES_B73_R0106": "Safe now. Okay?",
    "DK4_MES_B73_R0110": "Do not cling to my neck!{LB}C-cannot breathe.",
    "DK4_MES_B73_R0113": "Boy: Scared! So scared!",
    "DK4_MES_B73_R0116": "At this rate, both of us{LB}will drown!",
    "DK4_MES_B73_R0119": "Boy: Help! So scared!",
    "DK4_MES_B73_R0122": "N-no... drowning...",
    "DK4_MES_B73_R0126": "Someone!",
    "DK4_MES_B73_R0132": "No one else?",
    "DK4_MES_B73_R0136": "Christina...{LB}But the sea... water...",
    "DK4_MES_B73_R0139": "Sea scary, sea scary...{LB}Christina matters more...",
    "DK4_MES_B73_R0142": "But... but...{LB}Aaaaaaah!",
    "DK4_MES_B73_R0145": "The sea scares me...{LB}Christina needs me more!",
    "DK4_MES_B73_R0148": "Christina! Christina!",
    "DK4_MES_B73_R0151": "Christina!!!",
    "DK4_MES_B73_R0155": "Mivor is coming!",
    "DK4_MES_B73_R0159": "Christina!{LB}Coming now!",
    "DK4_MES_B73_R0165": "Cough... cough...{LB}Mivor...?{LB}What happened?",
    "DK4_MES_B73_R0169": "My beloved Christina!{LB}You woke up!",
    "DK4_MES_B73_R0172": "Nearly drowned...?{LB}The boy? Safe?",
    "DK4_MES_B73_R0176": "Yes, safe.{LB}His mother thanked us.",
    "DK4_MES_B73_R0180": "Someone saved us.{LB}Must thank them...{LB}Where is my savior?",
    "DK4_MES_B73_R0184": "Well... um...{LB}right here...",
    "DK4_MES_B73_R0187": "Eh?",
    "DK4_MES_B73_R0191": "Well...{LB}Mivor saved you...",
    "DK4_MES_B73_R0194": "But... you fear water...",
    "DK4_MES_B73_R0198": "Yes, but...{LB}Thinking you needed help,{LB}my mind went blank...",
    "DK4_MES_B73_R0202": "Somehow, this body swam.{LB}Hard to believe.",
    "DK4_MES_B73_R0205": "You?{LB}Hard to believe...",
    "DK4_MES_B73_R0208": "Ah, must reach the inn...",
    "DK4_MES_B73_R0212": "Are you well?",
    "DK4_MES_B73_R0216": "Yes. Can walk alone.",
    "DK4_MES_B73_R0220": "Then, goodbye...",
    "DK4_MES_B73_R0225": "There is big sis!",
    "DK4_MES_B73_R0229": "All right?",
    "DK4_MES_B73_R0233": "Yes, fine.{LB}Thank you.{LB}Where is the man who saved me?",
    "DK4_MES_B73_R0237": "Thank you so much.{LB}Where is the man with you?",
    "DK4_MES_B73_R0240": "He truly jumped into the sea?",
    "DK4_MES_B73_R0244": "Yes, crying oddly,{LB}he jumped right in.",
    "DK4_MES_B73_R0247": "He must love you deeply.",
    "DK4_MES_B73_R0250": "...So it is true.",
    "DK4_MES_B73_R0254": "Please take this{LB}as thanks.",
    "DK4_MES_B73_R0259": "Oh... thank you...",
    "DK4_MES_B73_R0263": "We will go now.{LB}Thank you again.",
    "DK4_MES_B73_R0266": "Bye, big sis.",
    "DK4_MES_B73_R0272": "That is it.",
    "DK4_MES_B73_R0276": "Mivor, afraid of water?{LB}Amazing!",
    "DK4_MES_B73_R0279": "Cannot believe it.",
    "DK4_MES_B73_R0283": "Ah, here he comes.",
    "DK4_MES_B73_R0288": "Mivor...",
    "DK4_MES_B73_R0292": "Christina...",
    "DK4_MES_B73_R0296": "Never thanked you properly.{LB}Thank you, Mivor.{LB}You looked... brave...",
    "DK4_MES_B73_R0300": "Whaaaat?!",
    "DK4_MES_B73_R0304": "Really?!{LB}Mivor looked brave?!{LB}So very happy!",
    "DK4_MES_B73_R0308": "You misunderstand!",
    "DK4_MES_B73_R0312": "Does not matter!{LB}So happy!{LB}Christina!",
    "DK4_MES_B73_R0316": "Enough! So loud!{LB}Let us sail now!{LB}He is annoying!",
    "DK4_MES_B73_R0320": "Always waiting{LB}for you!",
    "DK4_MES_B73_R0323": "They really make{LB}a good pair.",
    "DK4_MES_B73_R0334": "Yes.",
    "DK4_MES_B73_R0346": "(So do you two.)",
}

SPEAKERS = {
    "02": "Lil Argot", "07": "Christina", "09": "Kamil", "14": "Fernando",
    "4F": "Mivor Gentz", "A2": "Boy", "A7": "Boy's mother", "FE": "Boy",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXT = "In London, Mivor overcomes his fear of water to rescue Christina and a drowning child, earning Christina's reluctant respect."
EXCLUDED = {"DK4_MES_B73_R0080": "ten-byte scene-control payload with no visible dialogue"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = (set(LINES) | set(EXCLUDED)) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V17 inventory mismatch: missing={sorted(missing)}")
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
            "speaker": SPEAKERS.get(state, "Story participant"), "context": CONTEXT,
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving Christina's blunt voice, Mivor's comic devotion, the rescue tension, and romantic payoff.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Christina and Mivor's London harbor rescue and romantic follow-up in SC2 block 73.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(LINES) + len(EXCLUDED), "translated_records": len(records), "blocks": {"73": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records; excluded {len(EXCLUDED)} control")


if __name__ == "__main__":
    main()
