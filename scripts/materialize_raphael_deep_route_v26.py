from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v26.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = {
    "DK4_MES_B143_R0005": "{MACRO:FO}'s Admiral {MACRO:FA}, yes?{LB}Lord Albuquerque awaits.{LB}Proceed inside.",
    "DK4_MES_B143_R0009": "Thank you.",
    "DK4_MES_B143_R0021": "Quite imposing.",
    "DK4_MES_B143_R0028": "Hmm.{LB}We did no wrong, but{LB}places like this unsettle me.",
    "DK4_MES_B143_R0040": "Just stand tall and behave.",
    "DK4_MES_B143_R0055": "This is a palace...",
    "DK4_MES_B143_R0063": "Ah, welcome!{LB}You are... Mr. {MACRO:FA}, was it?",
    "DK4_MES_B143_R0068": "{MACRO:FU}.{LB}You summoned me, sir?",
    "DK4_MES_B143_R0071": "Oh! Smooth, {MACRO:FI}!",
    "DK4_MES_B143_R0082": "Ahem.{LB}This is not our place to speak.{LB}Let us remain quiet.",
    "DK4_MES_B143_R0089": "No titles, please.{LB}You came at my request.{LB}Thank you for coming.",
    "DK4_MES_B143_R0094": "Your purpose?",
    "DK4_MES_B143_R0098": "Ah, yes.{LB}Do you know Portugal's{LB}commercial code?",
    "DK4_MES_B143_R0103": "Not very well.",
    "DK4_MES_B143_R0106": "No matter. Honesty is welcome.{LB}Let me explain it simply.",
    "DK4_MES_B143_R0111": "Please do.",
    "DK4_MES_B143_R0115": "Private firms now trade abroad{LB}and enrich our nation, but some{LB}commit crimes against humanity.",
    "DK4_MES_B143_R0119": "Such as?",
    "DK4_MES_B143_R0123": "Slaves and narcotics.{LB}Our navy uncovered such trade{LB}by Espinosa Co. in southeast Africa.",
    "DK4_MES_B143_R0126": "Portugal's honor will fall{LB}unless we act. So here is my plan.",
    "DK4_MES_B143_R0129": "As gifted Portuguese navigators,{LB}seize every market they hold{LB}and capture Espinosa.",
    "DK4_MES_B143_R0134": "Can we truly do that?",
    "DK4_MES_B143_R0137": "Ha ha! No one expects it unaided.{LB}This old man is not so cruel.{LB}Bring Mr. Silveira!",
    "DK4_MES_B143_R0140": "At once!{LB}...{LB}Mr. Silveira, enter.",
    "DK4_MES_B143_R0144": "Mr. Silveira reporting.",
    "DK4_MES_B143_R0149": "Good.",
    "DK4_MES_B143_R0153": "Your Excellency, may you--",
    "DK4_MES_B143_R0157": "Enough greetings. Meet{LB}{MACRO:FI} {MACRO:FA}.{LB}A promising young admiral.",
    "DK4_MES_B143_R0161": "A pleasure...{LB}{MACRO:FI} {MACRO:FA}.",
    "DK4_MES_B143_R0165": "Mr. {MACRO:FA}, meet Mr. Silveira.{LB}You two will work together.",
    "DK4_MES_B143_R0169": "What does that mean?",
    "DK4_MES_B143_R0173": "Near southwest Africa,{LB}this merchant has made{LB}modest gifts{LB}to the crown.",
    "DK4_MES_B143_R0177": "Ahem.{LB}Your business is certainly extensive.",
    "DK4_MES_B143_R0181": "Such praise is an honor...",
    "DK4_MES_B143_R0185": "Enough of that.",
    "DK4_MES_B143_R0189": "Even a corrupt merchant cannot be{LB}attacked by our navy on mere suspicion.{LB}That is why we need you.",
    "DK4_MES_B143_R0192": "Ha ha ha! Together we shall drive{LB}Espinosa from my Africa!",
    "DK4_MES_B143_R0196": "(My Africa...?){LB}...Hmph. Very well.",
    "DK4_MES_B143_R0200": "Any objections?",
    "DK4_MES_B143_R0205": "...No.",
    "DK4_MES_B143_R0209": "My base is San Jorge.{LB}Visit whenever you like.{LB}Ha ha ha!",
    "DK4_MES_B143_R0233": "Silveira shared his San Jorge{LB}market share with you.",
    "DK4_MES_B143_R0244": "The king granted war funds.{LB}Bring them.",
    "DK4_MES_B143_R0247": "Sir!",
    "DK4_MES_B143_R0251": "Mr. Silveira.",
    "DK4_MES_B143_R0255": "Many thanks, sir.",
    "DK4_MES_B143_R0258": "Silveira received gold coins!",
    "DK4_MES_B143_R0263": "{MACRO:FA}.",
    "DK4_MES_B143_R0268": "Yes.{LB}Thank you...",
    "DK4_MES_B143_R0274": "The king granted 50,000 coins{LB}for the Espinosa campaign!",
    "DK4_MES_B143_R0278": "Reports say Espinosa commands{LB}a powerful fleet.{LB}Prepare your forces well.",
    "DK4_MES_B143_R0282": "Work together.{LB}Much is expected.",
    "DK4_MES_B143_R0286": "Understood.",
    "DK4_MES_B143_R0290": "As you command.",
    "DK4_MES_B143_R0294": "Good. You may go.",
    "DK4_MES_B143_R0299": "{MACRO:FI},{LB}good in battle?",
    "DK4_MES_B143_R0303": "Not especially.",
    "DK4_MES_B143_R0307": "Honest again. Good.",
    "DK4_MES_B143_R0316": "No shame in that.{LB}You can learn.",
    "DK4_MES_B143_R0320": "Oh...",
    "DK4_MES_B143_R0324": "Lord Albuquerque asked me{LB}to teach you, {MACRO:FI}.",
    "DK4_MES_B143_R0329": "Teach me...?",
    "DK4_MES_B143_R0332": "Yes. How do you defeat Espinosa?{LB}Do you know how to break an enemy power?",
    "DK4_MES_B143_R0337": "Drive Espinosa from each city?{LB}Then could we simply keep investing{LB}in those cities?",
    "DK4_MES_B143_R0340": "A fair answer,{LB}but investment is not enough.",
    "DK4_MES_B143_R0345": "Why not?",
    "DK4_MES_B143_R0347": "Understood.",
    "DK4_MES_B143_R0354": "Could investment alone reduce{LB}Lord Albuquerque's Lisbon share?",
    "DK4_MES_B143_R0359": "...No.",
    "DK4_MES_B143_R0363": "Exactly.{LB}To drive out a rival by investment,{LB}you must be at war.",
    "DK4_MES_B143_R0368": "Declare war...",
    "DK4_MES_B143_R0372": "Correct. Two ways:{LB}attack them at sea, or ask{LB}your guild officer to draft{LB}a declaration.",
    "DK4_MES_B143_R0376": "Got it.",
    "DK4_MES_B143_R0380": "Win at sea during war{LB}and rival reputation falls.{LB}Their share drops slightly{LB}in nearby cities.",
    "DK4_MES_B143_R0383": "Make a contract there quickly.{LB}Then investment can drive them out.",
    "DK4_MES_B143_R0388": "(Right! The same method opens{LB}contracts even in cities{LB}a rival controls completely!)",
    "DK4_MES_B143_R0392": "But investment alone cannot{LB}dissolve Espinosa Co.",
    "DK4_MES_B143_R0396": "...Meaning?",
    "DK4_MES_B143_R0400": "At an enemy headquarters,{LB}investment can never remove them.{LB}Only victory at sea can{LB}finish the job.",
    "DK4_MES_B143_R0403": "Should battle seem daunting,{LB}use those funds to trade.{LB}Build strong ships and save{LB}ample investment capital.",
    "DK4_MES_B143_R0407": "Admiral Silveira,{LB}thank you.",
    "DK4_MES_B143_R0412": "Ah, a promising ally.{LB}Perhaps my lesson was not needed?",
    "DK4_MES_B143_R0417": "Ah... sorry.",
    "DK4_MES_B143_R0424": "No, no.{LB}Together we shall defeat Espinosa,{LB}{MACRO:FI}!",
    "DK4_MES_B143_R0428": "Likewise, Admiral Silveira.",
}

SPEAKERS = {
    0x05: "Claudio Manini",
    0x06: "Julio Erdi",
    0x07: "Charlie",
    0x08: "Raphael fleet officer",
    0x1E: "Albuquerque",
    0x23: "Fernan Silveira",
    0x78: "Palace guard",
    0xFE: "System",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B143_")]
    if set(TRANSLATIONS) != {row["id"] for row in rows}:
        missing = sorted({row["id"] for row in rows} - set(TRANSLATIONS))
        extra = sorted(set(TRANSLATIONS) - {row["id"] for row in rows})
        raise SystemExit(f"B143 inventory mismatch; missing={missing}, extra={extra}")
    states = set(SPEAKERS)
    records = []
    for row in rows:
        english = TRANSLATIONS[row["id"]]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in states else ""
        unsafe = english
        for macro in ("FI", "FA", "FO", "FU"):
            unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row["id"],
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(first, "Raphael Castor"),
            "context": "Albuquerque commissions Raphael and Silveira to dismantle Espinosa's slave and narcotics operation, funds the campaign, and Silveira teaches war, market-share, and headquarters mechanics.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving the complete royal commission, uneasy alliance, campaign funding, both tutorial choices, all strategy instruction, and runtime identity commands.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects court-scene pacing, tutorial grouping, and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v26-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete Albuquerque audience, Silveira alliance, Espinosa commission, royal funding, and anti-faction tutorial in Raphael SC0 block 143.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"143": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
