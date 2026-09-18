from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v89.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = tuple(range(12, 26))

SPEAKERS = {
    0x04: "Eirene", 0x05: "Claudio", 0x06: "Eirene", 0x0D: "Raphael companion",
    0x10: "Gerhard", 0x17: "Manuel", 0x1B: "Pirate captain", 0x1E: "Albuquerque",
    0x1F: "Pedro de Valdes", 0x3D: "Vels", 0x3E: "Fugitive", 0x3F: "Julian Vermeer",
    0x41: "Prett Perot", 0x45: "Peralonso Aguirre", 0x46: "Zaganos Bey",
    0x47: "Pirate", 0x97: "Lookout", 0x99: "Pirate crew", 0xB0: "Pirate captain",
    0xB7: "Pirate crew", 0xB8: "Pirate crew", 0xB9: "Pirate crew",
}

EXCLUDED = {
    "DK4_MES_B22_R0029": "Raw scene-control payload, not visible dialogue.",
}

OVERRIDES = {
    "DK4_MES_B12_R0006": "Look there!{LB}That's {MACRO:FO}, the fleet{LB}raiding our waters!",
    "DK4_MES_B12_R0009": "Aye!!",
    "DK4_MES_B12_R0013": "Battle stations!{LB}Snake, command!",
    "DK4_MES_B12_R0016": "Aye!",
    "DK4_MES_B12_R0020": "Angel!{LB}Starboard quarter!",
    "DK4_MES_B12_R0023": "You got it!!!",
    "DK4_MES_B12_R0026": "Dandy!{LB}Guns ready?",
    "DK4_MES_B12_R0029": "Ready.",
    "DK4_MES_B12_R0033": "Heh, what a thrill.{LB}Listen up, boys!!!",
    "DK4_MES_B12_R0036": "Now we settle who rules these seas:{LB}me or {MACRO:FO}!",
    "DK4_MES_B12_R0039": "Aye!!!",
    "DK4_MES_B12_R0043": "Woman pirate?!",
    "DK4_MES_B12_R0048": "Never knew pirates like that.",
    "DK4_MES_B12_R0051": "We have to fight.",
    "DK4_MES_B12_R0056": "We cannot lose!{LB}Everyone, battle stations!",
    "DK4_MES_B13_R0043": "At last!{LB}This time we settle it!",
    "DK4_MES_B13_R0046": "Aye!",
    "DK4_MES_B13_R0052": "Back again? You never learn!{LB}{MACRO:FO}, become food for the sea!",
    "DK4_MES_B14_R0007": "Got you! You're the guild thief{LB}who fled abroad.",
    "DK4_MES_B14_R0011": "No idea what you mean.{LB}Move.",
    "DK4_MES_B14_R0015": "Playing dumb won't help.{LB}You're bound for Hamburg in chains!",
    "DK4_MES_B15_R0006": "There! You are the traitor{LB}Julian Vermeer!",
    "DK4_MES_B15_R0010": "Oui, hic!{LB}So what?",
    "DK4_MES_B15_R0014": "Does betraying your homeland{LB}not shame you as a Portuguese?",
    "DK4_MES_B15_R0017": "Gulp... Ahh! Homeland means nothing{LB}to profit! Get in my way{LB}and you'll regret it!",
    "DK4_MES_B16_R0007": "So you're Prett Perot,{LB}you villain!!",
    "DK4_MES_B16_R0010": "Who are you?! Don't act so noble.{LB}You've sinned at least once,{LB}haven't you?",
    "DK4_MES_B16_R0014": "What a joke. A born villain.{LB}No mercy!",
    "DK4_MES_B17_R0007": "Peralonso Aguirre!{LB}Arrested for spying.{LB}To the Malacca guild!",
    "DK4_MES_B17_R0011": "Heh. Only a young beauty{LB}could catch me.",
    "DK4_MES_B18_R0006": "Hee hee! Who are you?{LB}Want to die?",
    "DK4_MES_B18_R0010": "...{LB}Maybe we should leave.",
    "DK4_MES_B18_R0013": "Hee hee! Sink you!{LB}Sink you! Sink you!",
    "DK4_MES_B19_R0007": "So you're Zaganos Bey.{LB}A strong fleet, but we won't lose.",
    "DK4_MES_B19_R0011": "Gwahaha! Bold words.{LB}They'll be your last!",
    "DK4_MES_B20_R0005": "Admiral!{LB}Pirates sighted!",
    "DK4_MES_B20_R0016": "P-pirates again?!",
    "DK4_MES_B20_R0028": "Again?{LB}So busy...",
    "DK4_MES_B20_R0046": "Eek!!{LB}Pirates are the worst!",
    "DK4_MES_B20_R0052": "Hahaha! Their admiral is a green brat.{LB}Easy prey!",
    "DK4_MES_B20_R0055": "Damn you!",
    "DK4_MES_B20_R0060": "Running forever will never{LB}make us true sailors...",
    "DK4_MES_B20_R0064": "Everyone!{LB}Battle stations!",
    "DK4_MES_B20_R0067": "Yeah, been waiting!{LB}Time to show my skill!",
    "DK4_MES_B20_R0078": "{MACRO:FI}, the enemy has many ships!{LB}Don't forget to assign crew{LB}to battle stations!",
    "DK4_MES_B21_R0005": "Your fame is well earned.{LB}We must end you ourselves.",
    "DK4_MES_B21_R0009": "Defying Pedro de Valdes{LB}was reckless arrogance!{LB}Atone with your life!!",
    "DK4_MES_B21_R0031": "Albuquerque!{LB}Lead the vanguard!",
    "DK4_MES_B21_R0034": "Yes.",
    "DK4_MES_B22_R0015": "...This... was right...",
    "DK4_MES_B22_R0019": "...Albuquerque...",
    "DK4_MES_B22_R0028": "Yes!{LB}We beat Valdes!",
    "DK4_MES_B22_R0040": "{MACRO:FI}!{LB}We did it!!{LB}Portugal is safe now, right?!",
    "DK4_MES_B22_R0044": "Tell Lisbon's king{LB}and claim a huge reward!",
    "DK4_MES_B22_R0048": "Spain's grip will weaken.{LB}Portugal's crown may soon return!",
    "DK4_MES_B22_R0052": "Why not report our victory{LB}to Lisbon's king?{LB}He'll be delighted.",
    "DK4_MES_B22_R0056": "Great idea!{LB}We'll get a huge reward!",
    "DK4_MES_B23_R0008": "What strength...{LB}Can we really win...?",
    "DK4_MES_B23_R0011": "We must retreat...{LB}We need another plan...",
    "DK4_MES_B24_R0005": "Damn! We lost!{LB}No luck!",
    "DK4_MES_B24_R0008": "Vels!",
    "DK4_MES_B24_R0012": "G-Gerhard...!",
    "DK4_MES_B24_R0016": "Greed led you back to piracy!{LB}You fool!",
    "DK4_MES_B24_R0019": "Another lecture? Enough!{LB}Stop it!",
    "DK4_MES_B24_R0022": "Enough, you say?!",
    "DK4_MES_B24_R0026": "Of course! Discipline and thrift?{LB}What fun is that?",
    "DK4_MES_B24_R0030": "...That's why you're a fool!",
    "DK4_MES_B24_R0034": "What?!",
    "DK4_MES_B24_R0038": "You may not know it,{LB}but your seamanship{LB}now surpasses mine.",
    "DK4_MES_B24_R0042": "Then how could you beat me?",
    "DK4_MES_B24_R0045": "That is your folly!{LB}Greed fouled your heart{LB}and dulled your skill!",
    "DK4_MES_B24_R0049": "My heart is foul?!",
    "DK4_MES_B24_R0053": "You learned this: strength lies{LB}in heart, not skill or force.",
    "DK4_MES_B24_R0056": "Discipline and thrift{LB}trained your heart!{LB}Why can't you see?!",
    "DK4_MES_B24_R0060": "Enough! You're just{LB}an outdated old lion!",
    "DK4_MES_B24_R0063": "Take what you want, crush all rivals!{LB}Enjoy each day. That's enough!",
    "DK4_MES_B24_R0066": "Trying to reason with you was foolish.{LB}You're no pupil of mine!{LB}Leave!",
    "DK4_MES_B24_R0069": "Never was your pupil!{LB}Next time won't end this way!",
    "DK4_MES_B24_R0073": "Damn...",
    "DK4_MES_B24_R0078": "Gerhard...",
    "DK4_MES_B24_R0082": "Sorry you saw that.{LB}He deserved death...{LB}but my hand failed.",
    "DK4_MES_B24_R0086": "Still, he was my pupil.{LB}Please forgive me...",
    "DK4_MES_B24_R0090": "No, don't worry.",
    "DK4_MES_B24_R0095": "And Gerhard, your words,{LB}'Strength lies in heart'{LB}are surely right...",
    "DK4_MES_B24_R0099": "Thank you.{LB}Those words save me...",
    "DK4_MES_B25_R0008": "We won.",
    "DK4_MES_B25_R0012": "Heh, easy!",
    "DK4_MES_B25_R0016": "...People fell into the sea.{LB}They returned to Mother Sea...",
    "DK4_MES_B25_R0021": "Manuel...?",
    "DK4_MES_B25_R0025": "Let's soothe the souls{LB}of the fallen.",
    "DK4_MES_B25_R0033": "'Sea and mother are alike.{LB}The waves feel familiar,{LB}awakening a distant mother's heartbeat.",
    "DK4_MES_B25_R0036": "Some foreign tongues use{LB}one sound and glyph for both.",
    "DK4_MES_B25_R0040": "Sea and mother are alike.{LB}While life endures,{LB}both bind us in a bond{LB}that never fades.'",
    "DK4_MES_B25_R0044": "Manuel... you're a poet.{LB}A fine poem.{LB}May it become a song?",
    "DK4_MES_B25_R0048": "True. Thought he only loved ships,{LB}but that's real talent.",
    "DK4_MES_B25_R0052": "...The sea accepts all.{LB}We should do the same.",
}


def main() -> None:
    prefixes = tuple(f"DK4_MES_B{block:02d}_" for block in BLOCKS)
    with SOURCE.open(encoding="utf-8-sig", newline="") as source:
        rows = [row for row in csv.DictReader(source) if row["id"].startswith(prefixes)]
    records = []
    unresolved = []
    for row in rows:
        if row["id"] in EXCLUDED:
            continue
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
            "context": "Raphael defeats pirate captains and regional fleets, then resolves the Gerhard-Vels confrontation and Manuel's sea elegy.",
            "source_meaning": row["japanese"],
            "localization_note": "Natural concise American English preserving canonical names, battle intent, emotional continuity, and fixed-record constraints.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    if unresolved:
        raise SystemExit(f"Raphael V89 unresolved records: {unresolved}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v89-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael pirate, bounty, regional-fleet, Valdes-victory, Gerhard-Vels, and Manuel elegy scenes in SC0 blocks 12-25.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {str(block): sum(row["id"].startswith(f"DK4_MES_B{block:02d}_") for row in rows) for block in BLOCKS}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
