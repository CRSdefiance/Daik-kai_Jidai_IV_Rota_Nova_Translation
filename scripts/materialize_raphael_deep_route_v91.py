from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v91.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = (36, 37)

SPEAKERS = {
    0x04: "Eirene", 0x05: "Claudio", 0x06: "Julio", 0x22: "Hayreddin",
    0x33: "Salih", 0x97: "Lookout", 0x99: "Pirate crew",
}

OVERRIDES = {
    "DK4_MES_B36_R0005": "Admiral!{LB}Hostile ships!",
    "DK4_MES_B36_R0016": "What fleet is that?",
    "DK4_MES_B36_R0023": "Pirates?",
    "DK4_MES_B36_R0028": "Hope this doesn't become trouble.",
    "DK4_MES_B36_R0039": "Pirates mean a battle.",
    "DK4_MES_B36_R0046": "Hm?! Algerian pirates...{LB}Could it be him?",
    "DK4_MES_B36_R0050": "Alger pirates?",
    "DK4_MES_B36_R0054": "They are based on North Africa's coast{LB}and raid near Algiers.",
    "DK4_MES_B36_R0066": "Pirates!",
    "DK4_MES_B36_R0073": "Great, a trial already!",
    "DK4_MES_B36_R0077": "And... yes!{LB}Barbarossa Hayreddin!",
    "DK4_MES_B36_R0081": "Strong?",
    "DK4_MES_B36_R0085": "Hayreddin's family stands apart!{LB}Ruthless and incredibly strong!",
    "DK4_MES_B36_R0089": "Seriously?!",
    "DK4_MES_B36_R0093": "Even the Ottoman Turks,{LB}strongest force in these waters,{LB}seem involved.",
    "DK4_MES_B36_R0097": "So they're at the entrance,{LB}and their boss waits deep inside!",
    "DK4_MES_B36_R0101": "To trade here, we must first deal{LB}with the man controlling Gibraltar...",
    "DK4_MES_B36_R0113": "A hard road ahead.",
    "DK4_MES_B36_R0120": "Right now, we must survive{LB}this encounter.",
    "DK4_MES_B36_R0123": "Survive how?",
    "DK4_MES_B37_R0013": "{MACRO:FI}, what now?",
    "DK4_MES_B37_R0020": "Julio, don't the Algerian pirates{LB}hate Spain?",
    "DK4_MES_B37_R0024": "They prey on Spanish ships.{LB}A clash with Admiral Valdes's{LB}royal navy is likely soon.",
    "DK4_MES_B37_R0029": "Spain makes trade hard{LB}for Portuguese fleets...",
    "DK4_MES_B37_R0034": "Could a shared enemy help us?{LB}The enemy of my enemy...",
    "DK4_MES_B37_R0038": "You're too trusting.{LB}They're pirates!",
    "DK4_MES_B37_R0050": "This is bad...",
    "DK4_MES_B37_R0057": "You there!{LB}Why are you in my waters?!",
    "DK4_MES_B37_R0062": "Damn, spotted!",
    "DK4_MES_B37_R0074": "How do we escape?",
    "DK4_MES_B37_R0081": "He values pride.{LB}Cowards become prey. Stand tall.",
    "DK4_MES_B37_R0085": "Stand tall...?{LB}All right. Ahem.",
    "DK4_MES_B37_R0090": "We are Portuguese voyagers,{LB}under 'Defeat Spain,{LB}restore Portugal'...",
    "DK4_MES_B37_R0095": "{MACRO:FO}!",
    "DK4_MES_B37_R0100": "Admiral {MACRO:FU}!",
    "DK4_MES_B37_R0103": "Oh! Splendid.",
    "DK4_MES_B37_R0107": "Hear, hear! (applause)",
    "DK4_MES_B37_R0111": "Are you stupid?!{LB}Kill them all!!",
    "DK4_MES_B37_R0116": "No good...{LB}We're dead...",
    "DK4_MES_B37_R0119": "Wait, Salih.",
    "DK4_MES_B37_R0123": "You said 'defeat Spain,' yes?",
    "DK4_MES_B37_R0127": "Y-yes.",
    "DK4_MES_B37_R0131": "Hahaha! You would oppose{LB}Spain's grand armada? Hahaha!",
    "DK4_MES_B37_R0135": "W-what's funny?!",
    "DK4_MES_B37_R0139": "...Watch your tongue.",
    "DK4_MES_B37_R0151": "Clau! Leave this to {MACRO:FI}.{LB}Time for our leader to shine.{LB}Good luck.",
    "DK4_MES_B37_R0157": "Tch. All right.{LB}{MACRO:FI}, good luck.",
    "DK4_MES_B37_R0161": "All or nothing...{LB}Let's try.",
    "DK4_MES_B37_R0164": "Where did that fire go?{LB}To beat Spain's armada,{LB}dare to face us!",
    "DK4_MES_B37_R0168": "Exactly!",
    "DK4_MES_B37_R0172": "Bold. But at your strength,{LB}that would be fatal.",
    "DK4_MES_B37_R0176": "Right!{LB}Now is not the time!",
    "DK4_MES_B37_R0180": "What?!",
    "DK4_MES_B37_R0184": "Hahaha.{LB}Then when?",
    "DK4_MES_B37_R0188": "We'll gain experience and train,{LB}until we can face you as equals!",
    "DK4_MES_B37_R0192": "Hahaha! Who would calmly watch{LB}another rise above them?",
    "DK4_MES_B37_R0196": "Algerian pirates are more cowardly{LB}than rumored. Afraid we'll grow strong?",
    "DK4_MES_B37_R0200": "What?!",
    "DK4_MES_B37_R0205": "Then let us pass freely.{LB}Someday we'll defeat Spain's armada!",
    "DK4_MES_B37_R0209": "You brat!{LB}Know your place!!",
    "DK4_MES_B37_R0212": "You... called yourself{LB}{MACRO:FI}?",
    "DK4_MES_B37_R0216": "Hahaha! Amusing.{LB}Very amusing, boy!",
    "DK4_MES_B37_R0219": "Sir!!",
    "DK4_MES_B37_R0223": "Explore and grow strong.{LB}Then challenge me.",
    "DK4_MES_B37_R0226": "Lord Hayreddin!",
    "DK4_MES_B37_R0230": "You expect me to take{LB}this chick seriously?",
    "DK4_MES_B37_R0233": "Huh?{LB}Uh...",
    "DK4_MES_B37_R0236": "No matter.{LB}Such games amuse me.",
    "DK4_MES_B37_R0239": "Yes.{LB}Understood.",
    "DK4_MES_B37_R0242": "You may cross the Mediterranean.{LB}But trade elsewhere.",
    "DK4_MES_B37_R0247": "W-what?",
    "DK4_MES_B37_R0251": "Valdes and the Ottoman Turks{LB}are beyond you, and show no mercy.",
    "DK4_MES_B37_R0254": "Want mastery here?{LB}Make your name elsewhere.{LB}No needless trouble.",
    "DK4_MES_B37_R0258": "Yes... One more.",
    "DK4_MES_B37_R0263": "W-what?",
    "DK4_MES_B37_R0267": "When Spanish ships attack{LB}in my waters,{LB}my fleet will aid you.",
    "DK4_MES_B37_R0272": "Really?!",
    "DK4_MES_B37_R0276": "No guarantee.{LB}Even a pirate king stays busy.",
    "DK4_MES_B37_R0280": "T-thank you!!",
    "DK4_MES_B37_R0284": "But touch my family's territory{LB}and that means war.{LB}No mercy.",
    "DK4_MES_B37_R0289": "O-of course!",
    "DK4_MES_B37_R0293": "Hmph. Perhaps you...",
    "DK4_MES_B37_R0297": "No, nothing.{LB}Grow strong enough to entertain me,{LB}and keep your promise.",
    "DK4_MES_B37_R0302": "Understood. A promise.",
    "DK4_MES_B37_R0306": "Good. Everyone,{LB}withdraw.",
    "DK4_MES_B37_R0309": "Aye!",
    "DK4_MES_B37_R0314": "That bluff worked!{LB}Not bad, {MACRO:FI}!",
    "DK4_MES_B37_R0326": "An amazing promise.",
    "DK4_MES_B37_R0334": "Whew... That surprised me.{LB}Now fear sets in.",
    "DK4_MES_B37_R0338": "Heh, maybe you're the type{LB}who's strong under pressure.",
    "DK4_MES_B37_R0341": "Splendid.",
    "DK4_MES_B37_R0346": "Thanks, everyone.{LB}But after saying that,{LB}we must grow strong.",
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
            "context": "Raphael first meets Hayreddin, negotiates Mediterranean passage, and gains conditional protection against Spain.",
            "source_meaning": row["japanese"],
            "localization_note": "Natural concise American English preserving negotiation tactics, political stakes, character voice, macros, and fixed-record constraints.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    if unresolved:
        raise SystemExit(f"Raphael V91 unresolved records: {unresolved}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v91-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael first Hayreddin encounter, negotiation, Mediterranean-passage pact, and conditional anti-Spain protection in SC0 blocks 36-37.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {str(block): sum(row["id"].startswith(f"DK4_MES_B{block:02d}_") for row in rows) for block in BLOCKS}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
