from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v45.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("This town is an important link between the North Sea and the Mediterranean.", "A vital link between the North Sea and the Med."),
    8: ("Portugal's army and companies control it, so they won't let us trade.", "Portugal's navy and merchants control it. We can't trade."),
    13: ("Um...", "Um..."),
    17: ("What is it?", "What?"),
    22: ("You're FI of FO, right?", "{MACRO:FO}'s {MACRO:FI}?"),
    26: ("I must be famous now. Who are you?", "Oh, so you know me! Who are you?"),
    30: ("I'm Raphael Castor of the Castor Company.", "Raphael Castor, of Castor Co."),
    35: ("You're the one from the Castor Company?", "You're that Castor Co. admiral?!"),
    43: ("You're still just a child!", "You look like a kid!"),
    52: ("A child...", "Kid..."),
    56: ("You're hardly one to talk. Right, Raphael?", "You're one to talk! Right, Raphael?"),
    59: ("What? Is this rude muscleman picking a fight with me?", "What?! Who's this rude muscleman? Looking for a fight?"),
    63: ("You started it!", "Hey, you started it!"),
    66: ("FI, he's right.", "{MACRO:FI}, he has a point!"),
    71: ("Clau, calm down.", "Easy, Clau."),
    75: ("You should be angry too!", "You should be mad too!"),
    80: ("It's fine. I don't mind.", "No harm done. Really."),
    83: ("Honestly, you...", "You..."),
    87: ("Is this man really an admiral?", "He's really an admiral?"),
    92: ("Yes, I am.", "Yes..."),
    96: ("That's a letdown.", "That's... underwhelming."),
    105: ("Ahem. Did you want something from me?", "Ahem. Did you need me?"),
    109: ("You want a contract in this town, right?", "You want a contract here?"),
    113: ("That's sudden, but yes.", "That came out of nowhere! But yes..."),
    117: ("Then will you trade your Nantes share for my Lisbon share?", "Then how about a trade? Your Nantes share for my Lisbon share."),
    120: ("You want to exchange shares?", "A trade?!"),
    125: ("Only if you're willing.", "Only if you want to."),
    129: ("It isn't a bad offer, but one percent each?", "One percent each? Not bad..."),
    132: ("Lisbon is a major transport hub. Two to one is fair.", "Hold on. Lisbon's a major hub. Two Nantes shares for one Lisbon share."),
    136: ("We give you two percent of Nantes for one percent of Lisbon?", "So you get 2% of Nantes, and we get 1% of Lisbon?"),
    141: ("Yes.", "Yes."),
    145: ("If you don't like it, we'll ask someone else.", "No deal? We'll ask someone else."),
    149: ("What do you think?", "Well?"),
    155: ("Hmm... all right.", "Hmm... all right."),
    157: ("Are you stupid?", "Are you nuts?"),
    164: ("Your pampered face makes me stop caring about the terms.", "That pampered face... Oh, who cares about the terms?"),
    167: ("And I can't reach the Mediterranean without passing Lisbon.", "Can't reach the Mediterranean without Lisbon."),
    171: ("Then we have a deal.", "Deal!"),
    175: ("Now we've got a foothold in the North Sea.", "Great! A foothold in the North Sea!"),
    179: ("Thanks, FI. Let's stay on good terms.", "Thanks, {MACRO:FI}! Let's keep in touch!"),
    190: ("Shares in Nantes and Lisbon were exchanged.", "Nantes and Lisbon shares traded."),
    194: ("I'm not falling for that sales pitch.", "Hmph! Nice try, but no deal."),
    198: ("Too bad. I thought it was a good offer.", "Oh... Too bad. Seemed fair to me."),
    201: ("We'll have to ask someone else.", "Ask someone else."),
    206: ("Clau, stop. We were relying too much on others. Better to make our own steady progress.", "That's enough, Clau. We asked too much. Better to build our own stake bit by bit."),
    209: ("Making money slowly isn't my style.", "Tch. Slow work's not my style."),
    213: ("They're strange people.", "Odd pair..."),
}

SPEAKERS = {0x02: "Lil Argot", 0x05: "Claudio Manousch", 0x09: "Kamil", 0xFE: "Share exchange panel"}
TEXT_LEADS = {0x82, 0x83, 0x8E, 0x8F, 0x96, 0x46}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B133_")}
    if {f"DK4_MES_B133_R{number:04d}" for number in LINES} != expected:
        raise ValueError("B133 coverage does not match clean source")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B133_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS and lead not in TEXT_LEADS:
            raise ValueError(f"{row_id}: unmapped lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "").replace("{MACRO:FO}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": (f"{{SPEAKER:{lead:02X}}}" if lead in SPEAKERS else "") + english + "{PAD}",
            "speaker": SPEAKERS.get(lead, "Lil response choice" if number in {155, 157} else "Raphael Castor"),
            "context": (
                "Lil meets Raphael and Claudio at a Portuguese-controlled hub. Raphael offers a two-to-one "
                "Nantes-for-Lisbon town-share exchange, with acceptance and refusal branches."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural American English from clean B133 Japanese; preserves Castor Co., Clau, FI/FO name macros, "
                "the exact 2% Nantes for 1% Lisbon terms, both bare-text response starts, and the reward panel. "
                "Other Raphael records have ordinary Japanese text leads, not source speaker selectors. "
                "Guarded automatic wrapping protects first and continuation glyphs."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v45-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 47 B133 Raphael Castor crossover, two-to-one town-share exchange and refusal records.",
        "inventory": {"identified_records": 47, "translated_records": len(records), "blocks": {"133": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
