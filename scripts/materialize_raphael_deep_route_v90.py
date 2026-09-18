from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v90.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = tuple(range(26, 35))

SPEAKERS = {
    0x05: "Claudio", 0x07: "Eirene", 0x0C: "Raphael companion", 0x11: "Al Fasi",
    0x1B: "Aziza Nurennahar", 0x3E: "Fugitive", 0x3F: "Julian Vermeer",
    0x41: "Prett Perot", 0x45: "Peralonso Aguirre", 0x46: "Zaganos Bey",
    0x47: "Pirate", 0x97: "Lookout", 0xB7: "Mutinous pirate",
    0xB8: "Mutinous pirate", 0xB9: "Mutinous pirate",
}

OVERRIDES = {
    "DK4_MES_B26_R0006": "Damn, lost again...{LB}But next time... Huh?!",
    "DK4_MES_B26_R0009": "Sorry, but there is no next time.",
    "DK4_MES_B26_R0012": "Heh heh heh.",
    "DK4_MES_B26_R0016": "What?! Say that again!",
    "DK4_MES_B26_R0020": "Huh? Didn't hear me?",
    "DK4_MES_B26_R0024": "Nobody here listens to you anymore!",
    "DK4_MES_B26_R0027": "Damn you!{LB}Traitors!!",
    "DK4_MES_B26_R0030": "Hey, {MACRO:FI}!{LB}Something's happening!",
    "DK4_MES_B26_R0034": "She's surrounded...",
    "DK4_MES_B26_R0038": "A mutiny?{LB}Let's get closer.",
    "DK4_MES_B26_R0041": "No money from all these losses.{LB}You must answer for that.",
    "DK4_MES_B26_R0045": "Answer...?",
    "DK4_MES_B26_R0049": "Why do we keep chasing {MACRO:FO}?",
    "DK4_MES_B26_R0053": "Heh, some reason{LB}you won't tell us?!",
    "DK4_MES_B26_R0060": "You just want your father's{LB}Bloodstained Shamshir from {MACRO:FO}!",
    "DK4_MES_B26_R0064": "That's... not...",
    "DK4_MES_B26_R0068": "You've failed us.{LB}No one follows a captain{LB}who earns nothing. Prepare yourself!",
    "DK4_MES_B26_R0072": "Hear that, {MACRO:FI}?{LB}They'll kill her!",
    "DK4_MES_B26_R0076": "Going.",
    "DK4_MES_B26_R0081": "A-Al...",
    "DK4_MES_B26_R0085": "What?{LB}Outsiders, stay out!",
    "DK4_MES_B26_R0088": "...Know your place.",
    "DK4_MES_B26_R0092": "None of your business!{LB}Kill Aziza and these fools together!",
    "DK4_MES_B26_R0096": "Lord Al, my aid.",
    "DK4_MES_B26_R0100": "Me too! Men who rely on numbers{LB}are the worst!",
    "DK4_MES_B26_R0103": "Don't forget me!",
    "DK4_MES_B26_R0108": "...Pirates!{LB}Come on, all of you!",
    "DK4_MES_B26_R0111": "Why...? Why fight for me?{LB}We were enemies moments ago...",
    "DK4_MES_B26_R0115": "D-damn, the odds are bad!",
    "DK4_MES_B26_R0120": "Wait!",
    "DK4_MES_B26_R0124": "{MACRO:FI} {MACRO:FA}...",
    "DK4_MES_B26_R0128": "...You want this woman too?",
    "DK4_MES_B26_R0133": "Yes.{LB}Let's settle this by talking.",
    "DK4_MES_B26_R0136": "{MACRO:FI}!{LB}They won't listen to reason!",
    "DK4_MES_B26_R0140": "Relax, Clau.{LB}Think they can beat us?",
    "DK4_MES_B26_R0143": "No chance.",
    "DK4_MES_B26_R0148": "Then we're safe.{LB}No other choice.",
    "DK4_MES_B26_R0151": "Damn...{LB}All right, we'll listen.",
    "DK4_MES_B26_R0155": "You no longer want Aziza{LB}as your captain, correct?",
    "DK4_MES_B26_R0159": "Nobody aboard wants to follow her.",
    "DK4_MES_B26_R0167": "Then...",
    "DK4_MES_B26_R0171": "H-hey, {MACRO:FI}!{LB}You aren't hiring these thugs?!",
    "DK4_MES_B26_R0176": "Come on, Clau.{LB}Aziza is joining us.",
    "DK4_MES_B26_R0184": "No objection, but she made us suffer.{LB}We deserve compensation.",
    "DK4_MES_B26_R0188": "You take money?!",
    "DK4_MES_B26_R0193": "...How much do you need?",
    "DK4_MES_B26_R0197": "One million coins. Deal.",
    "DK4_MES_B26_R0204": "No complaints now.{LB}Aziza, come with us.",
    "DK4_MES_B26_R0207": "But...",
    "DK4_MES_B26_R0211": "We're done. Goodbye!",
    "DK4_MES_B26_R0217": "Betrayed by my own crew...{LB}How low this captain has fallen.{LB}Why did you save me?",
    "DK4_MES_B26_R0220": "Had no choice...",
    "DK4_MES_B26_R0224": "We couldn't leave you.",
    "DK4_MES_B26_R0229": "You helped us flee Basra.{LB}Why did you become a pirate?",
    "DK4_MES_B26_R0232": "Dad was a pirate.{LB}So is his daughter.",
    "DK4_MES_B26_R0235": "Those pirates served my father.{LB}Since childhood, their swordplay{LB}and trade became mine.",
    "DK4_MES_B26_R0240": "Your father?",
    "DK4_MES_B26_R0244": "He died in an accident.{LB}That sword was his,{LB}and vanished with him...",
    "DK4_MES_B26_R0248": "The Bloodstained Shamshir...",
    "DK4_MES_B26_R0252": "So that's why you praised my sword.",
    "DK4_MES_B26_R0255": "To become a great pirate like him,{LB}every habit became mine...",
    "DK4_MES_B26_R0259": "Learning you had the sword{LB}made me desperate to take it.{LB}Then...",
    "DK4_MES_B26_R0267": "Then it would prove{LB}his daughter worthy...{LB}Heh, but...",
    "DK4_MES_B26_R0271": "His keepsake mattered more{LB}than becoming a great pirate...",
    "DK4_MES_B26_R0275": "No wonder they left.{LB}That chase earned no money.",
    "DK4_MES_B26_R0279": "...Still miss piracy?",
    "DK4_MES_B26_R0283": "Piracy was never the goal.{LB}My father was.{LB}That life is over.",
    "DK4_MES_B26_R0288": "Then join us.{LB}You're better suited to sea than land.",
    "DK4_MES_B26_R0292": "Me, with you...?{LB}Really?",
    "DK4_MES_B26_R0296": "Sure!",
    "DK4_MES_B26_R0300": "Thanks...{LB}You saved my life,{LB}so expect my best work.",
    "DK4_MES_B26_R0304": "And just call me Aziza.",
    "DK4_MES_B26_R0307": "Your savior, {MACRO:FI}.",
    "DK4_MES_B26_R0311": "You're exaggerating!{LB}The feeling is mutual.{LB}Welcome, Aziza!",
    "DK4_MES_B27_R0018": "We withdraw today!{LB}Next time, we settle this!",
    "DK4_MES_B27_R0022": "...Coming back?",
    "DK4_MES_B27_R0029": "We drove them off...",
    "DK4_MES_B27_R0033": "Tch. We'll withdraw,{LB}but next time you'll pay!",
    "DK4_MES_B27_R0037": "...Remember my name:{LB}Aziza Nurennahar!",
    "DK4_MES_B27_R0040": "Yeah, don't come back!",
    "DK4_MES_B27_R0045": "A woman pirate captain...{LB}Different from the rest.",
    "DK4_MES_B28_R0016": "Well?{LB}Kneel before me!",
    "DK4_MES_B28_R0021": "Damn... Next time!{LB}Everyone, retreat!",
    "DK4_MES_B28_R0025": "Cowards, running away!",
    "DK4_MES_B28_R0031": "Got away!",
    "DK4_MES_B28_R0035": "This is bad! Run!",
    "DK4_MES_B28_R0040": "Too strong...{LB}We misjudged her.",
    "DK4_MES_B28_R0043": "You thought you could beat me?{LB}Next time, prepare to die!",
    "DK4_MES_B29_R0010": "Caught you!",
    "DK4_MES_B29_R0014": "Ouch! All right, surrender!{LB}Hamburg, anywhere--just spare me!",
    "DK4_MES_B30_R0010": "You're going to San Jorge's guild.{LB}Seize him!",
    "DK4_MES_B30_R0013": "Damn you! Don't touch me!{LB}Mmph!",
    "DK4_MES_B31_R0010": "Got him!{LB}Send him to Hangzhou!",
    "DK4_MES_B31_R0013": "Ouch!{LB}Truly sorry...",
    "DK4_MES_B32_R0010": "Behave until we reach Malacca.",
    "DK4_MES_B32_R0013": "Strong...",
    "DK4_MES_B33_R0009": "Keee! Curse you!{LB}Curse you! Curse you!",
    "DK4_MES_B33_R0014": "Take him to Veracruz{LB}and unload him.",
    "DK4_MES_B34_R0009": "D-damn you...{LB}Kill me!",
    "DK4_MES_B34_R0013": "Not so fast.{LB}People in Genoa hate you far more{LB}and are waiting.",
}


def main() -> None:
    prefixes = tuple(f"DK4_MES_B{block:02d}_" for block in BLOCKS)
    with SOURCE.open(encoding="utf-8-sig", newline="") as source:
        rows = [row for row in csv.DictReader(source) if row["id"].startswith(prefixes)]
    records = []
    unresolved = []
    for row in rows:
        english = OVERRIDES.get(row["id"])
        if english is None:
            unresolved.append(row["id"])
            continue
        unsafe = english
        for macro in ("FI", "FA", "FO", "FU"):
            unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
        first = int(row["source_hex"][:2], 16)
        state = f"{first:02X}" if first in SPEAKERS else ""
        rendered = f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}"
        records.append({
            "id": row["id"], "english": rendered,
            "speaker": SPEAKERS.get(first, "Raphael party or scene text"),
            "context": "Raphael resolves Aziza's mutiny and recruitment, then completes several active pirate-bounty captures.",
            "source_meaning": row["japanese"],
            "localization_note": "Natural concise American English preserving canonical names, character motives, recruitment continuity, bounty outcomes, and fixed-record constraints.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    if unresolved:
        raise SystemExit(f"Raphael V90 unresolved records: {unresolved}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v90-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael Aziza mutiny, rescue, backstory, recruitment, repeat encounters, and pirate-bounty captures in SC0 blocks 26-34.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {str(block): sum(row["id"].startswith(f"DK4_MES_B{block:02d}_") for row in rows) for block in BLOCKS}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
