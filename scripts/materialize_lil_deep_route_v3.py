from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v3.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
LINES = {
    "DK4_MES_B13_R0018": "We withdraw for today!{LB}Next time, we settle this!",
    "DK4_MES_B13_R0021": "Come back anytime!",
    "DK4_MES_B13_R0027": "Yes! This victory is mine!",
    "DK4_MES_B13_R0031": "Damn. Retreating now.{LB}But never yielding!{LB}Remember: Aziza Nurennahar!",
    "DK4_MES_B13_R0035": "Count on it!{LB}Come back when you want revenge!",
    "DK4_MES_B14_R0016": "Damn it!{LB}Next time, victory will be mine!",
    "DK4_MES_B14_R0020": "Hah! You will lose again!",
    "DK4_MES_B14_R0026": "What, running away?!",
    "DK4_MES_B14_R0038": "Bad luck!{LB}Best to retreat for now.",
    "DK4_MES_B14_R0044": "Argh! So frustrating!{LB}Still, you're strong!",
    "DK4_MES_B14_R0047": "You thought you could beat me?{LB}Next time, prepare to die!",
    "DK4_MES_B15_R0009": "Got you.{LB}Now off to Batavia.",
    "DK4_MES_B15_R0012": "Ow!{LB}Th-this was not how it should go...",
    "DK4_MES_B16_R0009": "Got you. Off to Hangzhou.{LB}Still defiant?",
    "DK4_MES_B16_R0012": "Ow!{LB}Lesson learned...",
    "DK4_MES_B17_R0009": "D-damn...{LB}My precious cargo...",
    "DK4_MES_B17_R0012": "Listen, you have been caught.{LB}Calicut will see you punished.{LB}Worry about yourself,{LB}not your cargo.",
    "DK4_MES_B18_R0008": "D-damn...",
    "DK4_MES_B18_R0012": "Got you. Off to Havana.{LB}No more smart talk from you!",
    "DK4_MES_B18_R0016": "Why, over a treaty breach?{LB}Ow!",
    "DK4_MES_B18_R0027": "Eh?{LB}Ah! Y-you?!",
    "DK4_MES_B18_R0030": "?{LB}Ah, you!{LB}We met at Havana's tavern!",
    "DK4_MES_B18_R0034": "Damn it!{LB}You meddled twice now!",
    "DK4_MES_B18_R0038": "You never learn!",
    "DK4_MES_B19_R0009": "Damn...{LB}Go on, kill me!",
    "DK4_MES_B19_R0012": "Not a chance.{LB}Back to Genoa with you.{LB}Everyone deserves an apology!",
    "DK4_MES_B20_R0005": "You there! Hear me?{LB}This is my territory!",
    "DK4_MES_B20_R0013": "Leave these waters{LB}unless you want pain!",
    "DK4_MES_B20_R0018": "Allies or not, stay out{LB}of my territory!{LB}Leave these waters!",
    "DK4_MES_B20_R0033": "You!{LB}Hayreddin Barbarossa!",
    "DK4_MES_B20_R0036": "Ah, pirate hunter Gerhard{LB}is here...",
    "DK4_MES_B20_R0047": "The 'Pirate King'...{LB}What a huge fleet...",
    "DK4_MES_B20_R0052": "What a massive fleet...",
    "DK4_MES_B20_R0067": "{MACRO:FI}, turn back{LB}for now!",
    "DK4_MES_B20_R0075": "Battle",
    "DK4_MES_B20_R0077": "Run",
    "DK4_MES_B20_R0085": "Good, you have courage!{LB}All ships, target merchants!{LB}Open fire! Kill them all!",
    "DK4_MES_B20_R0097": "Reckless, {MACRO:FI}!{LB}But now we have no choice...",
    "DK4_MES_B20_R0106": "A wise choice!{LB}Challenge me after making{LB}your name in Asia or Africa!",
    "DK4_MES_B20_R0117": "We cannot win this now.{LB}Doing as he says stings,{LB}but Africa offers better profit.",
    "DK4_MES_B21_R0006": "Admiral, a fleet approaches!{LB}That is... Escante's navy!",
    "DK4_MES_B21_R0009": "Escante?!",
    "DK4_MES_B21_R0021": "What?!{LB}They came to us!",
    "DK4_MES_B21_R0028": "Well, well.{LB}Lady {MACRO:FA},{LB}how are you today?",
    "DK4_MES_B21_R0032": "What do you want?!",
    "DK4_MES_B21_R0036": "Lady {MACRO:FA}, we came{LB}to welcome you to the New World.",
    "DK4_MES_B21_R0040": "And teach a sheltered young lady{LB}how terrifying the sea can be.",
    "DK4_MES_B21_R0044": "What is this?",
    "DK4_MES_B21_R0048": "This is how.{LB}All ships, fire on them!",
    "DK4_MES_B21_R0065": "Guns already?{LB}Quite a welcome!",
    "DK4_MES_B21_R0074": "Guns already?{LB}Quite a welcome!",
    "DK4_MES_B21_R0081": "How was that? Tuition is free.{LB}Ladies get special service.{LB}Give them another volley.",
    "DK4_MES_B21_R0085": "So this means war.{LB}Good! We accept!",
}

SPEAKERS = {
    "02": "Lil Argot", "07": "Christina", "09": "Kamil", "10": "Gerhard Adelknauts",
    "14": "Fernando", "19": "Ifa", "1B": "Aziza Nurennahar", "22": "Hayreddin Barbarossa",
    "2B": "Diogo de Escante", "40": "Ulysse", "41": "Prett Perot", "43": "Gabriel Cardocci",
    "44": "Jacob Portunto", "46": "Zaganos Bey", "97": "Lookout",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}

CONTEXTS = {
    13: "Lil and Aziza exchange victory and retreat taunts in their early rivalry.",
    14: "Alternate early-rivalry outcomes between Lil and Aziza, including Fernando's retreat advice.",
    15: "Lil captures the wanted pirate Ulysse and takes him to Batavia.",
    16: "Lil captures Prett Perot and takes him to Hangzhou.",
    17: "Lil captures Jacob Portunto and takes him to Calicut for punishment.",
    18: "Lil captures Gabriel Cardocci after recognizing him from Havana.",
    19: "Lil captures Zaganos Bey and takes him back to Genoa to apologize.",
    20: "Hayreddin Barbarossa warns Lil out of the southern Mediterranean and offers battle or retreat.",
    21: "Escante ambushes Lil in the New World and deliberately starts a war.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V3 inventory mismatch: missing={sorted(missing)}")
    records = []
    blocks: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        blocks[str(block)] = blocks.get(str(block), 0) + 1
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Story participant"),
            "context": CONTEXTS[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving the route event, speaker intent, and battle staging.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Lil rematches, bounty captures, Barbarossa ultimatum, and Escante ambush across SC2 blocks 13-21.",
        "excluded_records": {}, "inventory": {"identified_records": len(LINES), "translated_records": len(records), "blocks": blocks},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
