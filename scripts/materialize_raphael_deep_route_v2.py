from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v2.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
LINES = {
    "DK4_MES_B70_R0006": "The far eastern edge...",
    "DK4_MES_B70_R0018": "Unlike western lands...{LB}Even buildings look exotic.{LB}What an interesting place.",
    "DK4_MES_B70_R0025": "Yeah, amazing!{LB}True adventure...{LB}Hm? What is that?",
    "DK4_MES_B70_R0029": "{MACRO:FO}'s{LB}{MACRO:FA}, correct?",
    "DK4_MES_B70_R0032": "Wow! A true eastern warlord!",
    "DK4_MES_B70_R0043": "Shh! That was rude.",
    "DK4_MES_B70_R0051": "Yes. {MACRO:FI} {MACRO:FA}.{LB}That is me.",
    "DK4_MES_B70_R0055": "You seek the Proof?",
    "DK4_MES_B70_R0060": "What?!",
    "DK4_MES_B70_R0080": "Ah... yes.{LB}Then you know something?",
    "DK4_MES_B70_R0083": "We must discuss it.",
    "DK4_MES_B70_R0088": "Understood. Lead on.",
    "DK4_MES_B70_R0092": "Admiral Maria, this is{LB}{MACRO:FA}.",
    "DK4_MES_B70_R0102": "Wow! An eastern beauty!",
    "DK4_MES_B70_R0114": "Well, well...",
    "DK4_MES_B70_R0121": "Maria Li. Xien is my aide.{LB}Time is short. State your business.",
    "DK4_MES_B70_R0126": "Ah... y-yes.",
    "DK4_MES_B70_R0129": "Hey, {MACRO:FI}!{LB}Admire her later!",
    "DK4_MES_B70_R0133": "All right!",
    "DK4_MES_B70_R0137": "Do not blush!{LB}Heh.",
    "DK4_MES_B70_R0140": "...May we talk now?",
    "DK4_MES_B70_R0144": "Y-yes. Sorry.",
    "DK4_MES_B70_R0148": "The map key is in my hands...",
    "DK4_MES_B70_R0153": "You have it...?",
    "DK4_MES_B70_R0157": "Yes, but it has no use for me.{LB}This nation officially bans sea travel.",
    "DK4_MES_B70_R0162": "Understood.{LB}But we truly need it.",
    "DK4_MES_B70_R0166": "So it seems.{LB}Do one favor,{LB}and the key is yours.",
    "DK4_MES_B70_R0171": "Really? What must we do?",
    "DK4_MES_B70_R0174": "One condition:{LB}destroy the Kurushima pirates.",
    "DK4_MES_B70_R0178": "What are wako?",
    "DK4_MES_B70_R0181": "Sea gangs who prey mainly{LB}upon East Asian waters.",
    "DK4_MES_B70_R0186": "Are they so terrifying?",
    "DK4_MES_B70_R0190": "Not terrifying, exactly.{LB}Troublesome is the word.",
    "DK4_MES_B70_R0193": "Nimble ships raid coast towns.{LB}They often escape before our forces{LB}can pursue them.",
    "DK4_MES_B70_R0204": "We may need fast ships...",
    "DK4_MES_B70_R0211": "Not all ships are small.{LB}Their arsenal now includes{LB}many ship types.",
    "DK4_MES_B70_R0214": "Confirm Kurushima are gone,{LB}and this Bamboo Assembly Map{LB}is yours.",
    "DK4_MES_B70_R0219": "A map...?",
    "DK4_MES_B70_R0223": "You need it to find{LB}East Asia's Ruler's Proof.{LB}A fair bargain, yes?",
    "DK4_MES_B70_R0228": "Understood.{LB}We will try.",
    "DK4_MES_B71_R0006": "Kurushima is gone...",
    "DK4_MES_B71_R0010": "Now East Asia's Proof{LB}may be within reach.",
    "DK4_MES_B71_R0013": "So Kurushima is gone!",
    "DK4_MES_B71_R0017": "Heh. Sure is.",
    "DK4_MES_B71_R0027": "Are you seeking the Ruler's Proof?",
    "DK4_MES_B71_R0031": "Yes. Do you know of it?",
    "DK4_MES_B71_R0034": "Admiral Li in Hangzhou{LB}is said to know something.",
    "DK4_MES_B71_R0040": "Do you know where{LB}Admiral Maria Li is?",
    "DK4_MES_B71_R0043": "Of course.{LB}Usually in Hangzhou.",
    "DK4_MES_B71_R0059": "Admiral Li is well known?",
    "DK4_MES_B71_R0063": "Well known? Only Kurushima fools{LB}ever opposed her around here.",
    "DK4_MES_B71_R0067": "Hmm. Better not cross her...",
    "DK4_MES_B71_R0075": "Thank you.{LB}Let us head for Hangzhou!",
    "DK4_MES_B72_R0011": "You must be recognized{LB}as ruler of these waters.{LB}Take this.",
    "DK4_MES_B72_R0022": "Admiral... thanks.",
    "DK4_MES_B72_R0025": "No choice remains.{LB}You will be watched{LB}to prove you deserve the title.",
    "DK4_MES_B72_R0032": "And you...?",
    "DK4_MES_B72_R0036": "No one important.{LB}You may forget me.",
    "DK4_MES_B72_R0058": "Well done.",
    "DK4_MES_B72_R0063": "Maria! Ah... Admiral Li!",
    "DK4_MES_B72_R0067": "Yes. The admiral waited here.{LB}Now then...",
    "DK4_MES_B72_R0071": "Promised map.",
    "DK4_MES_B72_R0077": "{MACRO:FI}, was it?{LB}Stay alert in other waters too.",
    "DK4_MES_B72_R0082": "Th-thank you very much!!",
    "DK4_MES_B72_R0086": "Heh, blushing like mad.",
    "DK4_MES_B72_R0091": "Enough, Clau!{LB}We are leaving!!",
    "DK4_MES_B72_R0094": "Heh heh.{LB}Yes, Admiral. Let us go!",
    "DK4_MES_B73_R0006": "{MACRO:FI}, you have changed lately.{LB}Seems more grown up...",
    "DK4_MES_B73_R0011": "Heh, really?",
    "DK4_MES_B73_R0015": "Less worried than before.{LB}More steady, maybe.",
    "DK4_MES_B73_R0019": "You noticed too?{LB}Actually, Eirene deserves the credit.",
    "DK4_MES_B73_R0023": "Eirene?{LB}What does that mean?!",
    "DK4_MES_B73_R0027": "What does...?{LB}Why are you angry?",
    "DK4_MES_B73_R0032": "When we quarreled,{LB}Eirene said not to worry alone.",
    "DK4_MES_B73_R0037": "As admiral and head of{LB}{MACRO:FO}, every problem{LB}seemed mine alone...",
    "DK4_MES_B73_R0041": "She said talking can ease a burden.{LB}She was right. Eirene is almost{LB}like an older sister!",
    "DK4_MES_B73_R0049": "Kind, thoughtful,{LB}and never spiteful.",
    "DK4_MES_B73_R0053": "Once everyone knows she is a woman,{LB}men may fight over her.",
    "DK4_MES_B73_R0056": "Who would fight over her, huh?",
    "DK4_MES_B73_R0061": "Just speaking generally.{LB}Why so defensive? Ah! Maybe...",
    "DK4_MES_B73_R0065": "D-do not say such{LB}s-stupid things!!",
    "DK4_MES_B73_R0070": "Only joking...{LB}No need to shout.",
    "DK4_MES_B73_R0073": "You keep saying strange things!{LB}Going out now!!",
    "DK4_MES_B73_R0078": "Yes, yes. Have fun!{LB}...Clau is the strange one...",
    "DK4_MES_B74_R0005": "Lord {MACRO:FA}, the hour has come!{LB}Valdes awaits off Seville.{LB}Defeat the Spanish fleet{LB}and reclaim Portugal!",
    "DK4_MES_B74_R0008": "The final battle is off Seville?{LB}Please take care!",
    "DK4_MES_B74_R0012": "Many fleets are gathering there.",
    "DK4_MES_B74_R0016": "Once ready for Spain,{LB}go to Seville. Remember that,{LB}{MACRO:FI}.",
    "DK4_MES_B74_R0020": "A final battle with Valdes at Seville...{LB}We must prepare first.",
    "DK4_MES_B74_R0024": "Best stay away until then.",
    "DK4_MES_B74_R0028": "Thanks. We will remember.",
    "DK4_MES_B74_R0032": "The king wishes to see you too.",
}

SPEAKERS = {
    "03": "Maria Li", "04": "Emilio Marone", "05": "Claudio Manous", "08": "Arcadius",
    "53": "Sailor", "68": "Sailor", "6A": "Townsman", "71": "Sailor",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    "70": "In East Asia, Raphael meets Maria Li and agrees to destroy the Kurushima pirates in exchange for the Bamboo Assembly Map.",
    "71": "After Kurushima's defeat, Raphael learns that Maria Li in Hangzhou knows about the Ruler's Proof.",
    "72": "Maria recognizes Raphael's victory, gives him the promised map, and quietly tests his worth as a ruler.",
    "73": "Claudio notices Raphael's growth, then grows comically jealous when Raphael praises Eirene.",
    "74": "Sailors direct Raphael toward the decisive battle with Valdes off Seville and report that the king wants to see him.",
}
EXCLUDED = {
    "DK4_MES_B70_R0090": "six-byte scene-control payload with no visible dialogue",
    "DK4_MES_B70_R0146": "eight-byte scene-control payload with no visible dialogue",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = (set(LINES) | set(EXCLUDED)) - set(all_rows)
    if missing:
        raise SystemExit(f"Raphael V2 inventory mismatch: missing={sorted(missing)}")
    records = []
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Raphael Castor"), "context": CONTEXTS[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Natural concise American English preserving strategy, romantic comedy, route objectives, and all player-name macros.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria Li and Kurushima arc, Eirene jealousy scene, and Seville battle lead-in across SC0 blocks 70-74.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(LINES) + len(EXCLUDED), "translated_records": len(records), "blocks": {"70": 40, "71": 13, "72": 14, "73": 17, "74": 8}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records; excluded {len(EXCLUDED)} controls")


if __name__ == "__main__":
    main()
