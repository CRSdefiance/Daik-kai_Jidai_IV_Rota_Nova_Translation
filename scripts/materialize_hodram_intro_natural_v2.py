from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_intro_natural_v2_sc1_b42_b44.json")
SC1_SHA256 = "33981b27375cca1b9293752662d0dedb820dd310526c9dbe0612a397f38313ab"
EXCLUDED = {"DK4_MES_B42_R0032": "Four-byte non-prose command fragment."}

LINES = {
    "DK4_MES_B42_R0015": "Warn them.",
    "DK4_MES_B42_R0019": "Aye!",
    "DK4_MES_B42_R0023": "Warn them!",
    "DK4_MES_B42_R0027": "Aye, aye!",
    "DK4_MES_B42_R0031": "Our patrol controls these waters! Border violators must stop!",
    "DK4_MES_B42_R0034": "Move out!",
    "DK4_MES_B42_R0039": "Well done.",
    "DK4_MES_B42_R0043": "Admiral, address the crew.",
    "DK4_MES_B42_R0047": "Hm.",
    "DK4_MES_B42_R0059": "Think of a young island nation rising in the North Sea.",
    "DK4_MES_B42_R0062": "England permits piracy against Spanish merchants, stealing their wealth to strengthen its navy.",
    "DK4_MES_B42_R0065": "Sweden seeks to rule the Baltic and North Seas. We must build a navy equal to the world's finest.",
    "DK4_MES_B42_R0068": "We were entrusted with this task, though no one expects much from us.",
    "DK4_MES_B42_R0076": "You know the truth. Our so-called navy has only this one ship.",
    "DK4_MES_B42_R0079": "Our superiors call us pirate hunters. We merely fill the gap until a true navy is ready.",
    "DK4_MES_B42_R0082": "A young nation has little money. Supporting the Protestants makes matters worse.",
    "DK4_MES_B42_R0086": "The road ahead will be long and hard. We cannot finish this in two or three years.",
    "DK4_MES_B42_R0090": "One day, the world's greatest navy will sail the Baltic under our command. His Majesty and our people will behold it!",
    "DK4_MES_B42_R0093": "Success depends on every one of you!",
    "DK4_MES_B42_R0096": "Yeah!",
    "DK4_MES_B42_R0100": "(Applause)",
    "DK4_MES_B42_R0105": "Your speeches always give me chills.",
    "DK4_MES_B42_R0109": "Your words moved us to devote our lives to this country. That is no exaggeration.",
    "DK4_MES_B42_R0113": "{MACRO:FA}, you stirred us all!",
    "DK4_MES_B42_R0116": "Enough. Speeches are among my worst duties. More importantly...",
    "DK4_MES_B42_R0120": "The crown will now pay bounties based on the enemy fleets and pirates we defeat.",
    "DK4_MES_B42_R0124": "Great!",
    "DK4_MES_B42_R0128": "Now we can expand the fleet budget.",
    "DK4_MES_B42_R0131": "At last, we can attack.",
    "DK4_MES_B42_R0135": "We must investigate the report that Hanseatic ships entered our waters without permission. Today's prey escaped us.",
    "DK4_MES_B42_R0138": "The crew can rest. Ready the ship afterward.",
    "DK4_MES_B42_R0141": "Sir!",
    "DK4_MES_B42_R0145": "Aye!",
    "DK4_MES_B42_R0149": "Aye, aye!",
    "DK4_MES_B43_R0005": "Let's crush Speyer, reclaiming Baltic trade rights they stole by violating our waters.",
    "DK4_MES_B43_R0016": "Winning at sea weakens the enemy's hold on its ports.",
    "DK4_MES_B43_R0019": "A powerful fleet can protect a wide trade network, whose profits can fund an even stronger fleet.",
    "DK4_MES_B43_R0033": "Exactly. Ships cost a fortune. Regular trade provides the money.",
    "DK4_MES_B43_R0039": "Good trade builds the world's strongest navy fastest.",
    "DK4_MES_B43_R0042": "Exactly. An army without money cannot win a long war.",
    "DK4_MES_B43_R0054": "Sign contracts in many cities, even at one percent. Build routes now and expand shares later.",
    "DK4_MES_B43_R0068": "When an enemy controls a port, invest there after battle to take its share without restraint.",
    "DK4_MES_B43_R0075": "Good. We'll secure North Sea trade and an ocean route.",
    "DK4_MES_B44_R0006": "A young voice: Hey, you!",
    "DK4_MES_B44_R0014": "That ship's yours, right? What are you doing here?",
    "DK4_MES_B44_R0021": "Hey! You with the ship! Listen!",
    "DK4_MES_B44_R0025": "...What is it?",
    "DK4_MES_B44_R0029": "This is my territory. You can't barge in and start trading!",
    "DK4_MES_B44_R0033": "Lil! You can't talk to strangers like that!",
    "DK4_MES_B44_R0037": "A contract makes our trade legal.",
    "DK4_MES_B44_R0041": "Perfectly legal, he says. Ugh! You're so stiff and gloomy.",
    "DK4_MES_B44_R0045": "Stop, Lil. Please.",
    "DK4_MES_B44_R0049": "Oh, now it makes sense. You're military. Even soldiers and pirates are traders now.",
    "DK4_MES_B44_R0053": "Outsiders keep pouring into our territory and acting like they own it. Makes me sick!",
    "DK4_MES_B44_R0056": "Lil!",
    "DK4_MES_B44_R0060": "That is enough, woman!",
    "DK4_MES_B44_R0064": "What? Want to fight?",
    "DK4_MES_B44_R0068": "Gerhard, enough.",
    "DK4_MES_B44_R0072": "But, sir!",
    "DK4_MES_B44_R0076": "Huh. Maybe you're decent after all.",
    "DK4_MES_B44_R0079": "But that's beside the point! Cross me and you'll regret it. Kamil, let's go!",
    "DK4_MES_B44_R0084": "S-sorry... Please don't take it personally. Though you did...",
    "DK4_MES_B44_R0088": "W-well... bye.",
    "DK4_MES_B44_R0104": "Whoa... what a girl.",
    "DK4_MES_B44_R0111": "{MACRO:FI}, you're too forgiving!",
    "DK4_MES_B44_R0114": "Dealing with people like her is worse than any torture...",
    "DK4_MES_B44_R0126": "Best not to stir up trouble. She looks dangerous when angry.",
}

SPEAKERS = {
    "01": "Hodram Bergstrom",
    "02": "Lil Argot",
    "09": "Kamil",
    "10": "Gerhard Ardelknatts",
    "12": "Hodram fleet officer (state 0x12)",
    "17": "Manuel",
    "FE": "Crew or scene presentation (state 0xFE)",
}


def context_for(row_id: str) -> str:
    if "B42_" in row_id:
        return "Hodram's opening fleet exercise, address to his crew, and order to investigate Hanseatic incursions."
    if "B43_" in row_id:
        return "Hodram's officers explain how battle, trade, port shares, and route expansion support his naval objective."
    return "Hodram and his officers encounter Lil and Kamil while beginning their North Sea trade expansion."


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = {
            row["id"]: row
            for row in csv.DictReader(stream)
            if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in (42, 43, 44))
        }
    expected = set(rows) - set(EXCLUDED)
    if set(LINES) != expected:
        raise SystemExit(
            f"Hodram intro inventory mismatch: missing={sorted(expected - set(LINES))}, "
            f"extra={sorted(set(LINES) - expected)}"
        )

    records = []
    for row_id, english in LINES.items():
        source = bytes.fromhex(rows[row_id]["source_hex"])
        prefix = f"{source[0]:02X}"
        records.append(
            {
                "id": row_id,
                "english": f"{{SPEAKER:{prefix}}}{english}{{PAD}}",
                "speaker": SPEAKERS[prefix],
                "context": context_for(row_id),
                "source_meaning": english,
                "localization_note": "Natural American localization from the clean Japanese; source line breaks are treated as layout evidence, not copied prose.",
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": True,
                },
            }
        )

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC1.DK4",
        "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "hodram-story-probe",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": [
            "source",
            "context",
            "localization",
            "naturalness",
            "formatting",
        ],
        "profile_note": "Experimental fixed-allocation English for Hodram's actual SC1 opening through the first Lil/Kamil encounter. Runtime state effects remain pending cold-boot confirmation.",
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(rows),
            "translated_records": len(records),
            "excluded_non_prose_records": len(EXCLUDED),
            "blocks": {"42": 34, "43": 9, "44": 24},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} Hodram opening records")


if __name__ == "__main__":
    main()
