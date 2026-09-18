from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v2.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = tuple(range(61, 71))

LINES = {
    # B61: Sera recognizes a place from her escape from the Ottomans.
    "DK4_MES_B61_R0009": "Here...",
    "DK4_MES_B61_R0013": "What?",
    "DK4_MES_B61_R0017": "Known place.",
    "DK4_MES_B61_R0021": "What?! Then your homeland is nearby?",
    "DK4_MES_B61_R0024": "...No.",
    "DK4_MES_B61_R0028": "Then you passed here when they brought you away?",
    "DK4_MES_B61_R0032": "Escaped the Ottomans.",
    "DK4_MES_B61_R0036": "The Ottoman Empire! Did its army destroy your country?",
    "DK4_MES_B61_R0044": "Too hard? Ottoman soldiers attacked your home, yes?",
    "DK4_MES_B61_R0048": "Yes.",
    "DK4_MES_B61_R0052": "So...",

    # B62: Hodram and Sera speak about her lost homeland and place aboard.
    "DK4_MES_B62_R0009": "Sera? What brings you here?",
    "DK4_MES_B62_R0012": "Busy city.",
    "DK4_MES_B62_R0016": "Yes. This is a great trade center. Do crowds bother you?",
    "DK4_MES_B62_R0020": "Crowds?",
    "DK4_MES_B62_R0024": "Hate crowds?",
    "DK4_MES_B62_R0028": "No. Not dislike. Just... surprising.",
    "DK4_MES_B62_R0031": "Not used to them. This is quiet.",
    "DK4_MES_B62_R0039": "...What was your homeland like?",
    "DK4_MES_B62_R0042": "Homeland?",
    "DK4_MES_B62_R0046": "Where you were born.",
    "DK4_MES_B62_R0054": "Wide grasslands... spring flowers.",
    "DK4_MES_B62_R0057": "Rivers, birds, goats, sheep... and...",
    "DK4_MES_B62_R0061": "Sea... far away.",
    "DK4_MES_B62_R0065": "The sea?",
    "DK4_MES_B62_R0069": "Blue, blue sea.",
    "DK4_MES_B62_R0073": "Beautiful... Someday, perhaps.",
    "DK4_MES_B62_R0076": "But... all burned...",
    "DK4_MES_B62_R0083": "...Yes. Sorry.",
    "DK4_MES_B62_R0086": "No. {MACRO:FI}, don't worry.",
    "DK4_MES_B62_R0089": "...Our town, surely...",
    "DK4_MES_B62_R0092": "Hm? What about it?",
    "DK4_MES_B62_R0096": "Can't... explain.",
    "DK4_MES_B62_R0104": "No home? Stay aboard.",
    "DK4_MES_B62_R0107": "Woman on warship, bad...",
    "DK4_MES_B62_R0110": "You still remember that?",
    "DK4_MES_B62_R0114": "No matter. The crew loves your cooking.",

    # B63: Hodram clashes with the wealthy and arrogant Nagalpur.
    "DK4_MES_B63_R0005": "Lord Nagalpur's party! You there, Westerner, clear the road!",
    "DK4_MES_B63_R0008": "Nagalpur?",
    "DK4_MES_B63_R0012": "What is this procession?",
    "DK4_MES_B63_R0015": "Ho ho! Make way! Hm? Do you need something?",
    "DK4_MES_B63_R0019": "What? We're not blocking your way...",
    "DK4_MES_B63_R0022": "Ah, you want a tip. Here!",
    "DK4_MES_B63_R0034": "What a fool! How absurd!",
    "DK4_MES_B63_R0041": "How dare you mock Admiral {MACRO:FI}!",
    "DK4_MES_B63_R0045": "Nagalpur... what does this mean?",
    "DK4_MES_B63_R0048": "Not enough? Money is plentiful!",
    "DK4_MES_B63_R0052": "Nagalpur... now it comes back. The notorious upstart merchant!",
    "DK4_MES_B63_R0056": "You seem to earn quite well.",
    "DK4_MES_B63_R0060": "Money, money, money! Money is everything!",
    "DK4_MES_B63_R0063": "Money is all? Pitiful.",
    "DK4_MES_B63_R0075": "Money has its uses, but men who worship it are rotten.",
    "DK4_MES_B63_R0082": "Hm? Did you say something?",
    "DK4_MES_B63_R0085": "Got a problem, Westerner?",
    "DK4_MES_B63_R0089": "Ugly in body and soul... Enough. Let's go.",
    "DK4_MES_B63_R0092": "Exactly.",
    "DK4_MES_B63_R0096": "You dare oppose me? How reckless!",
    "DK4_MES_B63_R0100": "No one can match my wealth!",
    "DK4_MES_B63_R0111": "He thinks money solves everything.",
    "DK4_MES_B63_R0117": "What arrogance!",
    "DK4_MES_B63_R0121": "Let him talk. Wealth is useless in incompetent hands.",
    "DK4_MES_B63_R0125": "Ho ho! Stop babbling and learn how to become rich like me.",
    "DK4_MES_B63_R0129": "Come now. Clear the road!",
    "DK4_MES_B63_R0132": "Move aside!",
    "DK4_MES_B63_R0137": "No common ground with that man...",
    "DK4_MES_B63_R0140": "Utterly disgraceful! Our fleet should teach him how the world works.",

    # B64: Sera identifies Hodram with the sea-king legend.
    "DK4_MES_B64_R0011": "{MACRO:FA}, king of the eastern ocean, please accept this.",
    "DK4_MES_B64_R0021": "Hm?",
    "DK4_MES_B64_R0025": "You... sea king.",
    "DK4_MES_B64_R0029": "What?",
    "DK4_MES_B64_R0033": "This",
    "DK4_MES_B64_R0037": "A gift? This is...?",
    "DK4_MES_B64_R0051": "This leaf...? Why give it to me?",
    "DK4_MES_B64_R0055": "Our legend.",
    "DK4_MES_B64_R0059": "Tale?",
    "DK4_MES_B64_R0063": "Silver hair, blue eyes, iron ship. Sea king finds our treasure.",
    "DK4_MES_B64_R0066": "Me? A king on an iron ship?",
    "DK4_MES_B64_R0070": "(Nods.)",
    "DK4_MES_B64_R0078": "Ha ha ha! Nonsense. Just a fairy tale.",
    "DK4_MES_B64_R0081": "{MACRO:FI}. You mock our legend.",
    "DK4_MES_B64_R0084": "Hard to believe. Silver hair, blue eyes... too convenient.",
    "DK4_MES_B64_R0087": "{MACRO:FI}. You mocked me.",
    "DK4_MES_B64_R0090": "No... that wasn't meant.",
    "DK4_MES_B64_R0097": "Sorry. But the story must mean someone else, not me.",
    "DK4_MES_B64_R0101": "{MACRO:FI}, find treasure.",
    "DK4_MES_B64_R0104": "Yes, the treasure. Don't look angry.",

    # B65: Sera reunites with her people and leaves Hodram for now.
    "DK4_MES_B65_R0010": "Shirud!",
    "DK4_MES_B65_R0026": "What?! You know him?",
    "DK4_MES_B65_R0030": "My people!",
    "DK4_MES_B65_R0034": "What!",
    "DK4_MES_B65_R0046": "Others survived... A reunion.",
    "DK4_MES_B65_R0049": "Good. You're safe.",
    "DK4_MES_B65_R0057": "Hm?",
    "DK4_MES_B65_R0061": "Going home.",
    "DK4_MES_B65_R0065": "...Yes. That's best.",
    "DK4_MES_B65_R0068": "{MACRO:FI}, sea king.",
    "DK4_MES_B65_R0071": "Those words honor my dream of the finest navy.",
    "DK4_MES_B65_R0074": "{MACRO:FI}. When king...",
    "DK4_MES_B65_R0081": "When...",
    "DK4_MES_B65_R0085": "What?",
    "DK4_MES_B65_R0089": "...Meet again.",
    "DK4_MES_B65_R0093": "Hope so.",
    "DK4_MES_B65_R0101": "Beware Westerners... me too.",
    "DK4_MES_B65_R0108": "{MACRO:FI}!",
    "DK4_MES_B65_R0112": "Hm?",
    "DK4_MES_B65_R0124": "What?",
    "DK4_MES_B65_R0128": "Nothing... Thank you! Goodbye!",
    "DK4_MES_B65_R0132": "Yes... goodbye.",
    "DK4_MES_B65_R0157": "Are you sure?",
    "DK4_MES_B65_R0161": "She's strong. No worry.",

    # B66: Hodram encounters Kamil alone in Southeast Asia.
    "DK4_MES_B66_R0006": "You're new. Leave before Kuhn and Pereira drag you into their feud.",
    "DK4_MES_B66_R0026": "Whoever wins, people here gain nothing... Right, lad?",
    "DK4_MES_B66_R0031": "Y-yes.",
    "DK4_MES_B66_R0035": "You...?!",
    "DK4_MES_B66_R0039": "What? Ah!",
    "DK4_MES_B66_R0045": "You were... Kamil?",
    "DK4_MES_B66_R0049": "{MACRO:FI}... right?",
    "DK4_MES_B66_R0052": "Why are you here? Where's Lil?",
    "DK4_MES_B66_R0056": "Well... we're traveling separately for now.",
    "DK4_MES_B66_R0059": "Hm?",
    "DK4_MES_B66_R0063": "Well then...",
    "DK4_MES_B66_R0072": "There is more to this.",

    # B67: Maria tests Hodram and recruits him against Kuhn and Pereira.
    "DK4_MES_B67_R0005": "{MACRO:FA}, yes? Someone wishes to meet you. Will you come?",
    "DK4_MES_B67_R0008": "Me?",
    "DK4_MES_B67_R0012": "Relax. This won't take long.",
    "DK4_MES_B67_R0029": "Welcome.",
    "DK4_MES_B67_R0033": "Your name?",
    "DK4_MES_B67_R0036": "Someone who may become your enemy.",
    "DK4_MES_B67_R0039": "My enemy?",
    "DK4_MES_B67_R0043": "Should you be one more Westerner seeking to devour Asia, yes.",
    "DK4_MES_B67_R0051": "Our goal is a world-class navy for our homeland.",
    "DK4_MES_B67_R0055": "A noble excuse. You pushed others aside all the way here.",
    "DK4_MES_B67_R0059": "Think what you will.",
    "DK4_MES_B67_R0063": "Our fleet inspires a grand vision that cannot be denied.",
    "DK4_MES_B67_R0066": "Sailors everywhere vie for command of the seas. No greater stage exists for us.",
    "DK4_MES_B67_R0073": "Pfft! You say that shamelessly?",
    "DK4_MES_B67_R0081": "Hee hee, pardon me. You seem trustworthy. Very well; you may help.",
    "DK4_MES_B67_R0084": "Nothing you say makes sense. More importantly, who are you?",
    "DK4_MES_B67_R0089": "Me? Maria Hoamei Lee.",
    "DK4_MES_B67_R0098": "What?! The Lee family? Why here?",
    "DK4_MES_B67_R0102": "Call it spying. Tell no one. This meeting never happened.",
    "DK4_MES_B67_R0111": "{MACRO:FA}, do you know Kuhn and Pereira?",
    "DK4_MES_B67_R0126": "Yes.",
    "DK4_MES_B67_R0132": "Kuhn?",
    "DK4_MES_B67_R0147": "Pereira?",
    "DK4_MES_B67_R0153": "...No.",
    "DK4_MES_B67_R0165": "They are my enemies. Both want the spice islands.",
    "DK4_MES_B67_R0168": "Nothing stops them. They bombard towns, seize them, and monopolize production.",
    "DK4_MES_B67_R0172": "Kuhn is worst. He jails any citizen who resists and crushes rebellion by force.",
    "DK4_MES_B67_R0175": "Now your enemy is clear. So how can we help?",
    "DK4_MES_B67_R0179": "Stay out of my plan, to begin.",
    "DK4_MES_B67_R0182": "Hindrance?",
    "DK4_MES_B67_R0186": "Let them weaken each other. Then both can be driven from Asia at once.",
    "DK4_MES_B67_R0190": "Will that work?",
    "DK4_MES_B67_R0194": "With time.",
    "DK4_MES_B67_R0198": "Until then, their tyranny continues.",
    "DK4_MES_B67_R0205": "Will you hear my proposal?",
    "DK4_MES_B67_R0209": "...What?",
    "DK4_MES_B67_R0213": "No tricks. We'll drive them out. Done.",
    "DK4_MES_B67_R0216": "You will?",
    "DK4_MES_B67_R0220": "Enough theater. You wanted that answer.",
    "DK4_MES_B67_R0223": "...Heh.",
    "DK4_MES_B67_R0227": "You win. My fleet can't reach here yet.",
    "DK4_MES_B67_R0230": "Still... leaving this to you seems risky.",
    "DK4_MES_B67_R0234": "Bold words.",
    "DK4_MES_B67_R0238": "Kuhn seized Portugal's holdings almost overnight. He's dangerous.",
    "DK4_MES_B67_R0241": "Don't rush. His counterattack will hurt. Our plan proceeds regardless.",
    "DK4_MES_B67_R0244": "...Do as you wish.",

    # B68-B69: Hodram helps Kamil rescue Lil and reconcile with her.
    "DK4_MES_B68_R0005": "{MACRO:FI}! Please help!",
    "DK4_MES_B68_R0008": "Kamil? What happened?",
    "DK4_MES_B68_R0012": "Lil is in danger!",
    "DK4_MES_B68_R0016": "What happened?",
    "DK4_MES_B68_R0020": "Kuhn deceived her! She's walking into his trap!",
    "DK4_MES_B68_R0024": "No idea what's happening, but where?",
    "DK4_MES_B68_R0027": "Batavia! Sorry. Everything will be explained later!",
    "DK4_MES_B68_R0030": "Good. Come with us!",
    "DK4_MES_B69_R0006": "Lil! Thank goodness.",
    "DK4_MES_B69_R0011": "Sorry, Kamil... You warned me, but that man fooled me...",
    "DK4_MES_B69_R0014": "Don't worry, Lil.",
    "DK4_MES_B69_R0019": "No. Maria nearly became my enemy. Thanks for coming back.",
    "DK4_MES_B69_R0023": "Thank {MACRO:FI}.",
    "DK4_MES_B69_R0026": "All that happened was a ride here. The rest is unclear, but you two seem reconciled.",
    "DK4_MES_B69_R0030": "Um... Lil, could you take me aboard again?",
    "DK4_MES_B69_R0034": "Of course! Life was awful without you. Work twice as hard now!",
    "DK4_MES_B69_R0038": "Looks settled.",
    "DK4_MES_B69_R0042": "{MACRO:FI}, you helped without any explanation. Thank you so much.",
    "DK4_MES_B69_R0045": "Enough. Get along now.",

    # B70: Kuhn's hoard is returned and a significant object remains.
    "DK4_MES_B70_R0006": "Admiral, Kuhn's hoard was found.",
    "DK4_MES_B70_R0009": "Distribute it all among his victims.",
    "DK4_MES_B70_R0012": "This was mixed in with it...",
    "DK4_MES_B70_R0015": "This?",
}

SPEAKERS = {
    "01": "Hodram Bergstrom",
    "02": "Lil Argot",
    "03": "Maria Hoamei Lee",
    "09": "Kamil",
    "0A": "Maria's attendant",
    "10": "Gerhard Adelknauts",
    "11": "Hodram officer",
    "12": "Charles",
    "14": "Hodram sailor",
    "18": "Sera",
    "26": "Nagalpur",
    "69": "Indian Ocean elder",
    "74": "Tavern patron",
    "9A": "Nagalpur attendant",
}

EXTENDED_STATES = {0x10, 0x11, 0x12, 0x14, 0x18, 0x26, 0x69, 0x74, 0x9A}

CONTEXT = {
    61: "Sera recognizes a port from her escape and reveals that the Ottomans destroyed her homeland.",
    62: "Hodram and Sera discuss her lost homeland and her welcome place aboard his ship.",
    63: "Hodram and his officers clash with the arrogant merchant Nagalpur.",
    64: "Sera identifies Hodram with her homeland's legend of a silver-haired sea king.",
    65: "Sera reunites with a survivor of her people and parts from Hodram for now.",
    66: "Hodram encounters Kamil traveling alone amid the Kuhn-Pereira conflict.",
    67: "Maria Hoamei Lee tests Hodram and recruits him against Kuhn and Pereira.",
    68: "Kamil asks Hodram to help rescue Lil from Kuhn's trap in Batavia.",
    69: "Hodram helps Kamil and Lil reconcile after the rescue.",
    70: "After Kuhn's defeat, Hodram returns the tyrant's hoard to his victims.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {
            row["id"]: row
            for row in csv.DictReader(stream)
            if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)
        }
    if set(LINES) != set(source_rows):
        raise SystemExit(
            f"Hodram V2 inventory mismatch: missing={sorted(set(source_rows)-set(LINES))}, "
            f"extra={sorted(set(LINES)-set(source_rows))}"
        )

    records = []
    block_counts: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        source = bytes.fromhex(row["source_hex"])
        first = source[0]
        state = (
            f"{first:02X}"
            if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES)
            else ""
        )
        prefix = f"{{SPEAKER:{state}}}" if state else ""
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        block_counts[str(block)] = block_counts.get(str(block), 0) + 1
        records.append(
            {
                "id": row_id,
                "english": f"{prefix}{english}{{PAD}}",
                "speaker": SPEAKERS.get(state, "Choice or scene text"),
                "context": CONTEXT[block],
                "source_meaning": english.replace("{LB}", " ").replace("{MACRO:FI}", "Hodram").replace("{MACRO:FA}", "Bergstrom"),
                "localization_note": "Faithful concise American English from the clean Japanese; established character and route terminology is retained and wrapping uses the measured Hodram renderer profile.",
                "qa_waivers": [
                    "weak-line-ending",
                    "orphan-final-line",
                    *(["manual-break"] if "{LB}" in english else []),
                ],
                **(
                    {
                        "manual_break_reason": (
                            "Preserves the source record's leading line-feed control; "
                            "removing it would change this scene's native vertical placement."
                        )
                    }
                    if "{LB}" in english
                    else {}
                ),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            }
        )

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC1.DK4",
        "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "hodram-story-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Hodram's Indian Ocean and Southeast Asia continuation across SC1 blocks 61-70.",
        "profile_note": "Second large source-locked Hodram continuation: Sera's past and departure, Nagalpur, Maria's alliance, Kuhn and Pereira, Kamil and Lil's reconciliation, and Kuhn's defeat.",
        "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records across {len(BLOCKS)} blocks")


if __name__ == "__main__":
    main()
