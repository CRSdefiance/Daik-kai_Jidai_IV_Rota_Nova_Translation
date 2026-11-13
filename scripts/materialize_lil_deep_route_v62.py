from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v62.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("Angelo calls out to a young deckhand.", "Hey, you! Deckhand!"),
    9: ("Kamil asks if Angelo means him.", "...You mean me?"),
    13: ("Angelo asks to meet the ship's admiral.", "Yeah, you. You're on this ship, right? Need to see your admiral."),
    17: ("Angelo decides a lowly deckhand cannot introduce him and dismisses Kamil.", "Wait, a deckhand's word won't help me. Ha ha! Sorry. Run along."),
    25: ("Lil rebukes Angelo with a jab at his effeminate appearance.", "Hey! What a rude pretty boy!"),
    28: ("Angelo angrily rejects the insult and calls Lil a child.", "Pretty boy?! Watch it! And who are you? Beat it, kid!"),
    32: ("Lil objects to being called a child by a suspicious-looking stranger.", "Kid?! You're the shady one here! Don't call me a child!"),
    43: ("Fernando chides Lil for acting like a child.", "Easy, {MACRO:FI}... (That's why he calls you a kid.)"),
    50: ("Kamil stops Lil and introduces himself by full name.", "Stop, {MACRO:FI}. Name's Kamil Overijssel."),
    53: ("Kamil introduces Lil as the admiral using her name macros.", "She's {MACRO:FI} {MACRO:FA}. Our admiral."),
    57: ("Angelo is shocked to learn Lil is the admiral.", "Mamma mia! You're the admiral?!"),
    61: ("Angelo apologizes to Lil.", "Sorry. Please forgive me."),
    64: ("Kamil admits Lil also insulted Angelo.", "Oh... she was rude too."),
    68: ("Lil says Angelo belittled them first.", "Kamil! He mocked us. Don't apologize!"),
    72: ("Kamil hesitates.", "But..."),
    76: ("Angelo owns his teasing and admits he was drawn to Kamil's looks.", "She's right, Kamil. Cute boys make me want to tease them. Sorry."),
    79: ("Kamil awkwardly accepts Angelo's apology.", "Oh... um... never mind. Don't worry about it."),
    82: ("Angelo takes his leave.", "...Bye."),
    86: ("Kamil calls Angelo back and asks about navigator work.", "Wait! You wanted navigator work?"),
    90: ("Angelo confirms.", "Yeah."),
    94: ("Kamil asks Lil whether they can recruit Angelo.", "Okay, {MACRO:FI}?"),
    97: ("Lil is aghast that Kamil would hire a man who insulted him.", "You'd hire him? He mocked you! You're too nice!"),
    109: ("Fernando agrees Angelo insulted Kamil.", "Kamil! He mocked you!"),
    115: ("Kamil says Angelo seems decent and varied company improves a voyage.", "He seems decent. More people make the voyage fun."),
    127: ("Fernando sees Kamil's kindness as both weakness and strength.", "You're too soft... but that's what makes you Kamil."),
    131: ("Fernando cannot read Angelo even with his keen insight.", "Still, that man's odd. Even my eye for people can't read him."),
    138: ("Lil reluctantly agrees to Kamil's request.", "Oh, all right! You win. Okay!"),
    142: ("Kamil welcomes Angelo, then realizes he does not know his name.", "Then you're with us! Wait... we never asked your name."),
    146: ("Angelo asks if they are serious.", "H-hey... you mean it?"),
    150: ("Kamil says Lil agreed.", "Sure. {MACRO:FI} said yes."),
    154: ("Angelo notes Kamil talked Lil into agreeing and accepts the offer.", "Sounded like you made her say it... Ah, well. Glad to join you."),
    158: ("Angelo apologizes again and introduces himself by full name.", "Sorry about earlier. Angelo Puccini."),
    161: ("Kamil offers to show Angelo to the ship.", "Angelo, come see the ship."),
    164: ("Lil protests at being left behind.", "Hey! Wait for me!"),
    168: ("Angelo catches himself calling Lil a child and addresses the admiral.", "Aye, kid... er, Admiral!"),
    171: ("Lil welcomes Angelo and warns she will work him hard.", "Good to meet you! Work hard for me!"),
    189: ("Angelo advises Lil to seek trade profits beyond the Mediterranean.", "Admiral, want profit? Trade beyond the Mediterranean."),
    193: ("Lil asks why.", "Huh? Why's that?"),
    205: ("Lil's grandfather praises Angelo's understanding of trade.", "Oh! You know your trade, young man!"),
    215: ("Angelo says established powers already dominate developed Mediterranean routes.", "Great powers own these routes. Little profit remains."),
    219: ("Lil agrees that contracts and investments are costly and rivals dominate.", "True. Deals cost a fortune, and rivals control nearly every port."),
    223: ("Angelo recommends Africa for low-cost investment and large returns.", "Sail on. Africa can grow. Small stakes, big returns."),
    226: ("Angelo says rare African goods can sell well in Europe.", "Those rare goods sell for a fortune back in Europe."),
    229: ("Lil admits Angelo knows more about trade than she expected.", "You know your trade after all!"),
    232: ("Angelo modestly credits what he heard from sailors.", "Just what sailors told me."),
    243: ("Lil's grandfather agrees with Angelo.", "No, no. The young man is right."),
    246: ("Lil's grandfather explains cargo capacity is wasted where market share is hard to win.", "A bigger hold means little here. Without market share, we can't move much cargo."),
    252: ("Lil resolves to sail for Africa and earn a large profit.", "Then let's go! We'll make a fortune in Africa!"),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x06: "Lil's grandfather", 0x09: "Kamil",
    0x0F: "Angelo Puccini", 0x14: "Fernando Dias",
}
EXCLUDED = {
    "DK4_MES_B155_R0059": "Opaque five-byte recruitment scene event payload (20 31 46 EA 80)."
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B155_")}
    authored = {f"DK4_MES_B155_R{number:04d}" for number in LINES}
    if authored | EXCLUDED.keys() != expected or authored & EXCLUDED.keys():
        raise ValueError(f"B155 coverage mismatch: missing {expected - authored - EXCLUDED.keys()}")
    if source_rows["DK4_MES_B155_R0059"]["source_hex"].upper() != "203146EA80":
        raise ValueError("B155 R0059 scene event payload changed")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B155_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": (
                "Angelo Puccini insults Kamil and Lil, apologizes, joins Lil's crew, "
                "and recommends African trade over crowded Mediterranean routes."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B155 Japanese. FI/FA name macros, all source "
                "presentation leads, and the five-byte recruitment event retain their "
                "control behavior. Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v61-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 48 B155 text records, preserving one opaque scene event payload.",
        "inventory": {"identified_records": 49, "translated_records": 48, "blocks": {"155": 48}},
        "excluded_records": EXCLUDED, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records, {len(EXCLUDED)} control excluded")


if __name__ == "__main__":
    main()
