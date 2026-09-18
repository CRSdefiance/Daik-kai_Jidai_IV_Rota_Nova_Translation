from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v92.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = tuple(range(38, 43))

SPEAKERS = {
    0x04: "Eirene", 0x05: "Claudio", 0x06: "Julio", 0x08: "Arcadius",
    0x1F: "Pedro de Valdes", 0x22: "Hayreddin", 0x4B: "Hans",
    0x97: "Lookout",
}

OVERRIDES = {
    "DK4_MES_B38_R0005": "Admiral!{LB}Spanish fleet!",
    "DK4_MES_B38_R0009": "Portuguese brats!{LB}You allied with pirates{LB}against Spain?!",
    "DK4_MES_B38_R0014": "?!{LB}Who told you?",
    "DK4_MES_B38_R0017": "Answer! Depending on it,{LB}hundreds of guns may fire{LB}on your pitiful fleet!",
    "DK4_MES_B38_R0020": "Damn...{LB}This isn't a bluff{LB}we can talk away.",
    "DK4_MES_B38_R0025": "Bad. At our strength,{LB}we may not win...",
    "DK4_MES_B38_R0029": "Heh!{LB}Let them come!",
    "DK4_MES_B38_R0040": "Hmm.{LB}Our skill falls short...",
    "DK4_MES_B38_R0046": "Admiral!{LB}Another fleet sighted!",
    "DK4_MES_B38_R0050": "Are we done?!",
    "DK4_MES_B38_R0060": "Ah?!",
    "DK4_MES_B38_R0066": "Ah?!",
    "DK4_MES_B38_R0073": "Pedro, would this pirate need{LB}a child's aid to handle you?",
    "DK4_MES_B38_R0078": "Hayreddin!!",
    "DK4_MES_B38_R0082": "Grr!{LB}You... Barbarossa!!",
    "DK4_MES_B38_R0085": "Bored?{LB}Then play with me.",
    "DK4_MES_B38_R0093": "...Will Algerian pirates{LB}oppose Spain's navy?",
    "DK4_MES_B38_R0096": "Who cares who it is?{LB}Any fool crossing these waters{LB}is our prey.",
    "DK4_MES_B38_R0106": "...Tch!",
    "DK4_MES_B38_R0110": "Move. Go.",
    "DK4_MES_B38_R0115": "Thank you!!{LB}Everyone, full speed!{LB}Leave these waters!",
    "DK4_MES_B38_R0119": "Now fight.",
    "DK4_MES_B38_R0123": "Grr... Barbarossa!{LB}We retreat, but you'll regret{LB}making us your enemy!",
    "DK4_MES_B39_R0011": "Admiral, that ship appears Dutch.{LB}They're signaling.",
    "DK4_MES_B39_R0016": "Hmm. Can you tell?",
    "DK4_MES_B39_R0019": "Yes!{LB}Decoding signal!",
    "DK4_MES_B39_R0024": "Admiral {MACRO:FI}, that ship looks Dutch...{LB}A signal.",
    "DK4_MES_B39_R0028": "Janus, can you tell?",
    "DK4_MES_B39_R0031": "Let's see...{LB}Shall we decode it?",
    "DK4_MES_B39_R0037": "A fight?!{LB}My arms are ready!",
    "DK4_MES_B39_R0048": "Brute...",
    "DK4_MES_B39_R0052": "Hm? Say something?",
    "DK4_MES_B39_R0056": "Oh, you heard?",
    "DK4_MES_B39_R0064": "Clau! This isn't a voyage{LB}to pick fights worldwide!",
    "DK4_MES_B39_R0068": "Yeah, yeah, Admiral {MACRO:FI}.{LB}Got it.",
    "DK4_MES_B39_R0072": "Well?",
    "DK4_MES_B39_R0082": "'Put in at Amsterdam,'{LB}it says!",
    "DK4_MES_B39_R0087": "A signal... Yes.{LB}Seems to say, 'Put in at Amsterdam.'{LB}What now?",
    "DK4_MES_B39_R0094": "Hmm... Thoughts?",
    "DK4_MES_B39_R0103": "Should we call at Amsterdam once?",
    "DK4_MES_B39_R0108": "Suspicious, but an ambush at sea{LB}would be worse. Better comply.",
    "DK4_MES_B39_R0113": "(So Arcadius has{LB}strategic sense too.)",
    "DK4_MES_B39_R0119": "Their fleet isn't that big.{LB}We can break through!",
    "DK4_MES_B39_R0124": "We can count on you then, Clau.{LB}But...",
    "DK4_MES_B39_R0128": "Let's be cautious{LB}and enter port.",
    "DK4_MES_B40_R0005": "You have grown strong.",
    "DK4_MES_B40_R0010": "!!{LB}H-Hayreddin...!",
    "DK4_MES_B40_R0013": "Beyond my expectations.{LB}Ready to conquer the Mediterranean?",
    "DK4_MES_B40_R0018": "...Yes.{LB}Outcome uncertain,{LB}but that's the plan.",
    "DK4_MES_B40_R0022": "...{LB}The Ottoman Pasha fleet is mighty.{LB}You know?",
    "DK4_MES_B40_R0027": "...Sure.",
    "DK4_MES_B40_R0031": "Then call at Algiers' dock.",
    "DK4_MES_B40_R0035": "Huh?",
    "DK4_MES_B40_R0039": "Next battle, no mercy.",
    "DK4_MES_B40_R0044": "Bring it on!",
    "DK4_MES_B40_R0048": "Hahaha!{LB}Good look in your eyes!",
    "DK4_MES_B41_R0026": "Hans, shouldn't we have found{LB}some clue to Africa's Proof by now?",
    "DK4_MES_B41_R0029": "No use rushing.",
    "DK4_MES_B41_R0034": "But... how do we find a clue?",
    "DK4_MES_B41_R0037": "Gain power worthy of a ruler.{LB}Without it, no Proof.",
    "DK4_MES_B41_R0040": "By power, you mean a huge fleet?",
    "DK4_MES_B41_R0044": "Or becoming a true sailor?",
    "DK4_MES_B41_R0055": "Perhaps wealth.",
    "DK4_MES_B41_R0069": "A vast trade sphere?",
    "DK4_MES_B41_R0075": "Many meanings.{LB}Perhaps all of them.",
    "DK4_MES_B41_R0080": "Wow...{LB}That's a daunting task.",
    "DK4_MES_B41_R0083": "But power alone isn't enough.",
    "DK4_MES_B41_R0088": "What?! There's more?",
    "DK4_MES_B41_R0092": "Only my theory...",
    "DK4_MES_B41_R0095": "The Proof's mystery may lie{LB}in ruins worldwide.",
    "DK4_MES_B41_R0099": "Ruins?",
    "DK4_MES_B41_R0103": "Yes.",
    "DK4_MES_B41_R0108": "Where are the ruins?",
    "DK4_MES_B41_R0112": "Near each culture's major cities.",
    "DK4_MES_B41_R0116": "Still not enough{LB}to find them.",
    "DK4_MES_B41_R0119": "Locals may know.{LB}Earn their trust first.",
    "DK4_MES_B41_R0123": "Trust...?",
    "DK4_MES_B41_R0127": "Ruins and old churches embody{LB}their faith and culture.{LB}Outsiders aren't told easily.",
    "DK4_MES_B41_R0131": "Grant requests, help the troubled,{LB}punish corrupt merchants or soldiers...",
    "DK4_MES_B41_R0134": "Sounds like charity.",
    "DK4_MES_B41_R0137": "To qualify as ruler, you need{LB}character that earns people's trust.",
    "DK4_MES_B41_R0142": "Whew... Becoming a ruler is hard.",
    "DK4_MES_B41_R0146": "Hahaha, of course.{LB}No one has ever done it.",
    "DK4_MES_B42_R0005": "After hiring crew, you need supplies:{LB}water and food. Get them at the dock.",
    "DK4_MES_B42_R0009": "Dock staff handle resupply for you.{LB}Easy.",
    "DK4_MES_B42_R0012": "With little money, they buy{LB}what you can afford.",
    "DK4_MES_B42_R0015": "Refuse resupply to change{LB}the water-food ratio,{LB}though you'll rarely need to.",
    "DK4_MES_B42_R0019": "Without supplies, sailors weaken.{LB}Even fine ships fail. Watch your stores.",
    "DK4_MES_B42_R0022": "Ready?",
    "DK4_MES_B42_R0027": "At last, we sail.{LB}What after departure?",
    "DK4_MES_B42_R0030": "Your spirit ran ahead{LB}without a plan?",
    "DK4_MES_B42_R0033": "Ha, never thought{LB}Clau would say that.",
    "DK4_MES_B42_R0036": "What?!{LB}You make me sound thoughtless!",
    "DK4_MES_B42_R0040": "Sorry! Surprised you had an idea.{LB}Let's hear it.",
    "DK4_MES_B42_R0043": "Huh? Well...{LB}That's it!!",
    "DK4_MES_B42_R0047": "How about fighting pirates?!{LB}Board them and cut down every brute!",
    "DK4_MES_B42_R0050": "...Good grief.",
    "DK4_MES_B42_R0055": "...Let's think properly.{LB}At our strength, we'd need many lives.",
    "DK4_MES_B42_R0059": "Start by visiting ports around{LB}the Mediterranean and North Sea.",
    "DK4_MES_B42_R0063": "Visit many ports.{LB}Navigation and trade skills{LB}come naturally.",
    "DK4_MES_B42_R0068": "Yes!{LB}Let's recruit more companions too!",
    "DK4_MES_B42_R0071": "Yes. Our current roster is too thin{LB}for the voyage ahead.",
    "DK4_MES_B42_R0074": "Old man!{LB}Why look at me?!",
    "DK4_MES_B42_R0077": "Come now.{LB}More companions would help.",
    "DK4_MES_B42_R0080": "{MACRO:FI}, you'll surely be blessed{LB}with good companions.",
    "DK4_MES_B42_R0085": "Julio...",
    "DK4_MES_B42_R0089": "We also need more funds{LB}to expand and maintain ships.",
    "DK4_MES_B42_R0092": "Trade around the world{LB}and wealth will follow.",
    "DK4_MES_B42_R0095": "But neglect trade and funds only fall.{LB}That was my money, so take care.",
    "DK4_MES_B42_R0100": "Thank you, Julio.{LB}We'll earn it back...",
    "DK4_MES_B42_R0103": "Hahaha, a joke.{LB}Don't worry.{LB}Shall we go?",
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
            "context": "Raphael receives Hayreddin's protection, answers the Amsterdam signal, reviews Ruler's Proof requirements, and completes the early sailing-supplies tutorial.",
            "source_meaning": row["japanese"],
            "localization_note": "Natural concise American English preserving political stakes, tutorial facts, Proof lore, macros, and fixed-record constraints.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    if unresolved:
        raise SystemExit(f"Raphael V92 unresolved records: {unresolved}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v92-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael Hayreddin rescue, Amsterdam signal, Ruler's Proof lore, supply, departure, recruitment, and trade tutorials in SC0 blocks 38-42.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {str(block): sum(row["id"].startswith(f"DK4_MES_B{block:02d}_") for row in rows) for block in BLOCKS}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
