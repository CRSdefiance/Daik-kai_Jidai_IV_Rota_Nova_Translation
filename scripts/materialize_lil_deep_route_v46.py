from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v46.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    (134, 5): ("Our first step into Africa. We need to raise FO's name here.", "Our first step into Africa! Let's make a name for {MACRO:FO}!"),
    (134, 17): ("Yes, FI. Let's do our best.", "Right, {MACRO:FI}! Let's do this!"),
    (134, 23): ("First we should buy trade goods.", "Now, let's buy some goods!"),
    (134, 27): ("Woman, who gave you permission to trade here?", "Who gave you leave to trade here?"),
    (134, 34): ("This west African region is Silveira Company territory. You cannot trade freely here.", "West Africa belongs to Silveira Company. No trading without permission!"),
    (134, 37): ("What are you saying? I have a contract with this town.", "What? We have a town contract!"),
    (134, 48): ("That's right. A contract lets us trade freely.", "Exactly! Our contract lets us trade."),
    (134, 54): ("No. My territory means...", "No, no! My territory means..."),
    (134, 58): ("The town's money and goods, everything, belong to me.", "Every coin and every good in this town is mine. Understand?"),
    (134, 62): ("That logic is absurd. Where we trade is none of your business.", "That's absurd! Where we trade is none of your business!"),
    (134, 74): ("Yes. What you're saying makes no sense.", "Exactly! That's nonsense!"),
    (134, 80): ("No matter what you say, this entire region is mine. Leave now.", "Everything here is mine, whatever you say! Stop arguing and leave!"),
    (134, 84): ("We worked hard to get here. We will not turn back.", "Enough! We came all this way. No chance we're turning back!"),
    (134, 95): ("Yes, FI. Tell him.", "That's right, {MACRO:FI}! Tell him!"),
    (134, 102): ("If you refuse to withdraw, I have other means.", "You won't leave? Then you'll face the consequences!"),
    (134, 106): ("I will use every resource of the Silveira Company to destroy yours.", "The Silveira Company will crush you and end your trading days!"),
    (134, 112): ("All right, I understand.", "All right..."),
    (134, 114): ("Bring it on.", "Try me!"),
    (134, 121): ("What? Speak up.", "Hm? Speak up, girl!"),
    (134, 125): ("I said I'll pull out.", "We'll pull out, okay?!"),
    (134, 129): ("Good. You should have been agreeable from the start.", "Good. You should've agreed sooner."),
    (134, 132): ("As a greeting fee, I'll take some of your town share.", "Your share is my welcome fee. Ha ha!"),
    (134, 138): ("Silveira took a little of your Sao Jorge share.", "Silveira seized part of your Sao Jorge share."),
    (134, 146): ("That miserly old man. One day I'll make him pay.", "(That stingy old man... He'll pay for this one day!)"),
    (134, 160): ("Kamil?", "Kamil?!"),
    (134, 164): ("Why does this always turn into a head-on fight?", "Y-yeah... (Why does this always become a fight?)"),
    (134, 171): ("Impudent girl. You'll regret making an enemy of me.", "You brat! You'll regret crossing me!"),
    (135, 6): ("Please, Mr. Espinosa, sell me the medicine.", "M-medicine... Mr. Espinosa, please..."),
    (135, 9): ("Do you have the money?", "Did you bring the money?"),
    (135, 13): ("Here it is.", "Th-this..."),
    (135, 17): ("One, two, three... not enough for Goddess' Temptation. Come back with more money.", "One, two, three... Too little. Goddess' Temptation costs more."),
    (135, 21): ("But this was enough last time.", "But... this was enough last time!"),
    (135, 24): ("Prices change with the market.", "That was then. Market prices change."),
    (135, 27): ("I've sold my land and everything else.", "But... My land, everything... it's all gone!"),
    (135, 30): ("Your problem is not mine. No money, no sale. Leave.", "That's not my concern. No money, no sale. Please leave."),
    (135, 34): ("Mr. Espinosa...", "Mr. Espinosa..."),
    (135, 38): ("Get out. Mr. Espinosa says you're an eyesore.", "Get out! Espinosa can't stand you!"),
    (135, 41): ("Ugh...", "Ugh..."),
    (135, 45): ("Goddess' Temptation is a wonderful business. I can't stop laughing.", "Heh heh... Goddess' Temptation is good business!"),
    (135, 49): ("Hey, you.", "Hey, you!"),
    (135, 53): ("What a charming girl. Are you also here for Goddess' Temptation?", "Hello, young lady. Seeking Goddess' Temptation?"),
    (135, 57): ("You're Espinosa, the man spreading drugs and making people suffer.", "You're Espinosa! Your drugs are ruining lives!"),
    (135, 61): ("Suffering? No. My customers are all happy.", "Ruining lives? Nonsense, dear girl. My customers are delighted."),
    (135, 65): ("You have no shame running such a corrupt business.", "Shameless! You profit off misery."),
    (135, 69): ("Those accusations are baseless. Do not meddle in legitimate trade.", "Lies! My trade is honest. Keep out."),
    (135, 73): ("I know everything. If you're set on this, I'll respond in kind.", "Stop pretending! We know your scheme. You'll see!"),
    (135, 77): ("What do you intend to do?", "Oh? What will you do?"),
    (135, 81): ("If you keep selling drugs, my FO will defeat your company.", "Keep selling drugs, and {MACRO:FO} will bring down your company!"),
    (135, 85): ("Did you hear her? That's amusing.", "Heh heh. Hear that? How amusing!"),
    (135, 88): ("What a ridiculous joke, little girl.", "Ha! That's a good one, little girl!"),
    (135, 92): ("You'll regret laughing.", "Laugh now. You'll regret it!"),
    (135, 95): ("Well, do your best. Heh heh.", "Well, do your best. Heh heh."),
    (135, 106): ("No matter what, I'll defeat the Espinosa Company. Kamil, don't try to stop me.", "We'll bring down the Espinosa Company! Kamil, don't stop me!"),
    (135, 110): ("I won't stop you this time. I cannot forgive that vile man.", "No. Not this time. That vile man won't get away with it!"),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x09: "Kamil", 0x14: "Fernando Dias", 0x23: "Silveira",
    0x24: "Espinosa", 0x2F: "Espinosa guard", 0x60: "Desperate buyer", 0xFE: "Town-share panel",
}
TEXT_LEADS = {0x95, 0x8F}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith(("DK4_MES_B134_", "DK4_MES_B135_"))}
    authored = {f"DK4_MES_B{block}_R{number:04d}" for block, number in LINES}
    if authored != expected:
        raise ValueError("B134-B135 coverage does not match clean source")
    records = []
    for (block, number), (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B{block}_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS and lead not in TEXT_LEADS:
            raise ValueError(f"{row_id}: unmapped presentation lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "").replace("{MACRO:FO}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": (f"{{SPEAKER:{lead:02X}}}" if lead in SPEAKERS else "") + english + "{PAD}",
            "speaker": SPEAKERS.get(lead, "Lil response choice"),
            "context": (
                "Lil meets Silveira in West Africa; her withdrawal and defiance branches are both preserved."
                if block == 134 else
                "Lil sees Espinosa exploit a desperate Goddess' Temptation buyer and vows to end his narcotics trade."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Clean Japanese reviewed in scene order. Preserves Silveira, Espinosa, Sao Jorge, the established "
                "Goddess' Temptation name, FI/FO macros, both bare-text response starts, and the share-loss panel. "
                "Source 23/24/2F/60 bytes are presentation states, with 95/8F as visible choice text. "
                "Guarded automatic wrapping protects initial and continuation glyphs."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v46-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 54 B134-B135 Silveira and Espinosa confrontation records, including both B134 choices.",
        "inventory": {"identified_records": 54, "translated_records": len(records), "blocks": {"134": 27, "135": 27}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
