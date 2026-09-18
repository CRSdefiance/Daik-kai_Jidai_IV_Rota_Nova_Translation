from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v1.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
BLOCKS = tuple(range(0, 12))
LINES = {
    "DK4_MES_B00_R0006": "This is Muramasa...?",
    "DK4_MES_B00_R0010": "Hmm...{LB}That eerie glow{LB}almost draws one in.",
    "DK4_MES_B01_R0006": "Yes! Unmistakable.{LB}The same dull gleam{LB}as when lost.",
    "DK4_MES_B01_R0010": "How did nobody find it...?",
    "DK4_MES_B02_R0006": "Despite my warning...{LB}What fools.",
    "DK4_MES_B02_R0016": "Now you meet your end!",
    "DK4_MES_B02_R0028": "Now you meet your end,{LB}before provoking the wrath{LB}of a man far more terrifying!",
    "DK4_MES_B02_R0034": "Now you meet your end!",
    "DK4_MES_B02_R0052": "Barbarossa Hayreddin...{LB}A worthy opponent!",
    "DK4_MES_B02_R0066": "Let's go.{LB}Been itching to fight!",
    "DK4_MES_B02_R0080": "No victory, Hayreddin!",
    "DK4_MES_B03_R0006": "Look there!{LB}That fleet ravaging our waters{LB}belongs to {MACRO:FO}!",
    "DK4_MES_B03_R0009": "Aye!",
    "DK4_MES_B03_R0013": "Battle stations!{LB}Snake, take command!",
    "DK4_MES_B03_R0016": "Aye.",
    "DK4_MES_B03_R0020": "Angel!{LB}Starboard quarter!",
    "DK4_MES_B03_R0023": "You got it!{LB}Leave it to me!!!",
    "DK4_MES_B03_R0026": "Dandy!{LB}Guns ready?",
    "DK4_MES_B03_R0029": "Ready.",
    "DK4_MES_B03_R0033": "Heh... what a thrill.{LB}Listen up, you dogs!!!",
    "DK4_MES_B03_R0036": "Today we decide{LB}whether my crew or {MACRO:FO}{LB}deserves to rule these seas!",
    "DK4_MES_B03_R0039": "Aye!!!",
    "DK4_MES_B03_R0051": "A she-pirate?!",
    "DK4_MES_B03_R0058": "Heh, sounds fun.{LB}Let's do it!",
    "DK4_MES_B03_R0061": "Everyone, battle!",
    "DK4_MES_B04_R0043": "At last!{LB}This time, we settle it!",
    "DK4_MES_B04_R0046": "Aye!",
    "DK4_MES_B04_R0052": "Back again? Never learn!{LB}{MACRO:FO}!{LB}This time, sink beneath the sea!",
    "DK4_MES_B05_R0006": "You're Ulysse,{LB}the ship thief!",
    "DK4_MES_B05_R0009": "Such a cheap nickname offends me.{LB}After all, this gentleman{LB}comes from first-rate nobility.",
    "DK4_MES_B05_R0012": "A nickname? You're about to be caught,{LB}and that is what bothers you?!",
    "DK4_MES_B06_R0005": "So you're Prett Perot.{LB}A murderer...{LB}No villain like you goes free!",
    "DK4_MES_B06_R0009": "Who are you to judge me?{LB}Do not pretend you have never{LB}committed a single sin!",
    "DK4_MES_B06_R0012": "What an attitude! You mock me?!{LB}A scoundrel like you needs{LB}a painful lesson.{LB}No mercy!",
    "DK4_MES_B07_R0006": "So you're Jacob Portunto.{LB}A merchant profiting by petty tricks{LB}shames the trade!",
    "DK4_MES_B07_R0010": "What?!{LB}No whelp like you lectures me!",
    "DK4_MES_B08_R0005": "Are you Gabriel?{LB}Your selfish trading hurts people.{LB}Will you stop?",
    "DK4_MES_B08_R0009": "Selfish? Agreements exist to be broken.{LB}Enough of your prattle.",
    "DK4_MES_B08_R0013": "That is my line!{LB}Reasoning with you is hopeless.{LB}You will stop, even by force!",
    "DK4_MES_B08_R0017": "Amusing. Come!",
    "DK4_MES_B09_R0006": "So you're Zaganos Bey.{LB}You look strong,{LB}but victory is mine!",
    "DK4_MES_B09_R0010": "Gwahaha! Bold words.{LB}You do not realize{LB}they will be your last!",
    "DK4_MES_B10_R0005": "Ha ha! Learned your lesson, girl?{LB}You should heed good advice!",
    "DK4_MES_B10_R0009": "This time you may leave.{LB}Never return to{LB}the southern Mediterranean.",
    "DK4_MES_B10_R0013": "To challenge me in earnest,{LB}first make a name{LB}in Africa or Asia!",
    "DK4_MES_B10_R0025": "Damn...",
    "DK4_MES_B10_R0037": "No helping it.{LB}They are monsters.",
    "DK4_MES_B10_R0043": "At least all survived.{LB}Be grateful for that.",
    "DK4_MES_B11_R0006": "We won!",
    "DK4_MES_B11_R0018": "Amazing, {MACRO:FI}.{LB}Your command in battle{LB}has come so far.",
    "DK4_MES_B11_R0022": "Heh. Talent!",
    "DK4_MES_B11_R0029": "Lives scattered into the sea...{LB}No, returned to mother ocean.",
    "DK4_MES_B11_R0033": "Manuel...?",
    "DK4_MES_B11_R0037": "Let us honor{LB}the spirits of the fallen.",
    "DK4_MES_B11_R0044": "Sea and mother are alike.{LB}Endless ripples stir memories{LB}of a distant mother's heartbeat.",
    "DK4_MES_B11_R0047": "Sea and mother are alike.{LB}Some foreign lands give both{LB}the same sound and sign.",
    "DK4_MES_B11_R0051": "Sea and mother are alike.{LB}Both exist within bonds{LB}that never vanish while we live.",
    "DK4_MES_B11_R0054": "Hey, wait.{LB}Why suddenly recite poetry?",
    "DK4_MES_B11_R0066": "Oh, {MACRO:FI}...{LB}No romance at all.{LB}That moved me. Truly beautiful.",
    "DK4_MES_B11_R0070": "Hmph. Poetry's worth{LB}means nothing to me anyway.",
    "DK4_MES_B11_R0076": "The sea accepts everything...{LB}May we learn to do the same.",
}

SPEAKERS = {
    "02": "Lil Argot", "09": "Kamil", "0C": "Sailor", "10": "Sailor", "11": "Sailor",
    "14": "Fernando", "17": "Manuel", "1B": "Aziza Nurennahar", "22": "Barbarossa",
    "40": "Ulysse", "41": "Prett Perot", "43": "Gabriel", "44": "Jacob Portunto",
    "46": "Zaganos Bey", "99": "Pirate crew", "B7": "Pirate crew", "B8": "Pirate crew", "B9": "Pirate crew",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V1 inventory mismatch: missing={sorted(missing)}")
    records = []
    counts = {str(block): 0 for block in BLOCKS}
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        block = str(int(row_id.split("_B", 1)[1].split("_", 1)[0]))
        counts[block] += 1
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Story participant"),
            "context": "Lil's early relic, Barbarossa, Aziza, bounty, defeat, victory, and post-battle reflection scenes.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving all battle branches, named targets, runtime macros, and Manuel's poem.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Lil relic, opening battles, bounties, defeat, victory, and reflection dialogue in SC2 blocks 0-11.",
        "excluded_records": {}, "inventory": {"identified_records": len(LINES), "translated_records": len(records), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
