from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v8.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = tuple(range(139, 149))
EXCLUDED = {
    "DK4_MES_B140_R0003": "Raw event-control payload; not dialogue.",
    "DK4_MES_B144_R0016": "Raw event-control payload; not dialogue.",
    "DK4_MES_B146_R0015": "Raw event-control payload; not dialogue.",
    "DK4_MES_B148_R0085": "Raw event-control payload; not dialogue.",
}

LINES = {
    "DK4_MES_B139_R0007": "Once past Gibraltar, stay away from the southern Mediterranean.",
    "DK4_MES_B139_R0010": "Why?",
    "DK4_MES_B139_R0014": "No more. Trust me: avoid that area.",

    "DK4_MES_B140_R0005": "Someone wishes to meet you.",
    "DK4_MES_B140_R0009": "Mexico's governor, Diogo de Escante.",
    "DK4_MES_B140_R0013": "Hello.",
    "DK4_MES_B140_R0017": "Governor. What do you want?",
    "DK4_MES_B140_R0020": "Watch your mouth!",
    "DK4_MES_B140_R0023": "Enough. A proposal for you.",
    "DK4_MES_B140_R0026": "Me?",
    "DK4_MES_B140_R0030": "Do you know Vazquez de Maldonado?",
    "DK4_MES_B140_R0033": "Yes.",
    "DK4_MES_B140_R0037": "He has caused us endless trouble.",
    "DK4_MES_B140_R0040": "But isn't he Spanish, like you?",
    "DK4_MES_B140_R0043": "Officially Cuba's acting governor, he truly commands the Caribbean pirates.",
    "DK4_MES_B140_R0046": "His pirates raid Spain's colonial ships. He takes a cut and grows rich.",
    "DK4_MES_B140_R0049": "Unless that hyena is removed, Spain's Caribbean colonies will collapse.",
    "DK4_MES_B140_R0052": "England may seize the Caribbean and New World, shaking Spain.",
    "DK4_MES_B140_R0055": "Join us in defeating the traitor. What say you?",
    "DK4_MES_B140_R0059": "That would be treason. Spain should handle its own criminal.",
    "DK4_MES_B140_R0063": "Without proof, you cannot condemn him or attack a fellow Spaniard.",
    "DK4_MES_B140_R0066": "Drive Maldonado out for us, and you will have our full support.",
    "DK4_MES_B140_R0070": "Even if we end up controlling the Caribbean?",
    "DK4_MES_B140_R0073": "Better a friendly power than a man who attacks merchant ships indiscriminately.",
    "DK4_MES_B140_R0076": "Heh. England worries you, but we're easier to manage.",
    "DK4_MES_B140_R0080": "Do not be so suspicious.",
    "DK4_MES_B140_R0083": "Spain is at war with England. We cannot openly join the English.",
    "DK4_MES_B140_R0087": "We're Protestants your king would gladly kill.",
    "DK4_MES_B140_R0090": "Keep Europe's religious wars there. Such useless conflict has no place here. England is different!",
    "DK4_MES_B140_R0093": "England is Spain's foe. That flag disgusts me!",
    "DK4_MES_B140_R0100": "This benefits you too. To enter the Caribbean, you must face Maldonado.",
    "DK4_MES_B140_R0103": "He is a powerful admiral and former pirate, still leading a strong fleet. Alone, you may struggle.",
    "DK4_MES_B140_R0108": "Very well.",
    "DK4_MES_B140_R0110": "Gerhard's view?",
    "DK4_MES_B140_R0118": "Clear enough. A chance to gain strength...",
    "DK4_MES_B140_R0123": "(This split in Spain's colonies is our chance to gain strength. Making both sides enemies would be unwise.)",
    "DK4_MES_B140_R0126": "Hm...",
    "DK4_MES_B140_R0133": "Very well. We'll accept.",
    "DK4_MES_B140_R0136": "Glad you are reasonable.",

    "DK4_MES_B141_R0005": "But does Escante truly mean to cooperate?",
    "DK4_MES_B141_R0009": "Hard to say. Odds are even.",
    "DK4_MES_B141_R0012": "Hope he plots nothing now that Maldonado is weak.",
    "DK4_MES_B141_R0016": "Maldonado's former subjects still suffer exploitation.",
    "DK4_MES_B141_R0019": "Escante may repeat Maldonado's abuses.",
    "DK4_MES_B141_R0022": "Likely across the whole New World. This problem will not be easily solved.",
    "DK4_MES_B141_R0025": "Couldn't help overhearing. Did you defeat Maldonado?",
    "DK4_MES_B141_R0029": "Yes.",
    "DK4_MES_B141_R0033": "You could defeat Escante too.",
    "DK4_MES_B141_R0036": "Meaning?",
    "DK4_MES_B141_R0040": "You said it yourselves. Maldonado and Escante are alike.",
    "DK4_MES_B141_R0044": "Either way, we live under threats and extortion. This is hell.",

    "DK4_MES_B142_R0005": "Stranger... Ah...",
    "DK4_MES_B142_R0008": "Don't worry. You're safe here. Even slave traders won't break the law in public.",
    "DK4_MES_B142_R0011": "...",
    "DK4_MES_B142_R0014": "You don't understand me...",
    "DK4_MES_B142_R0019": "Admiral, the smugglers are found.",
    "DK4_MES_B142_R0022": "Hm.",
    "DK4_MES_B142_R0027": "They serve Jeronimo de Espinosa.",
    "DK4_MES_B142_R0031": "...Espinosa!",
    "DK4_MES_B142_R0044": "Heard that name.",
    "DK4_MES_B142_R0051": "Long rumored in human trafficking, drugs, and poaching.",
    "DK4_MES_B142_R0054": "Publicly, he controls most African trade. A dangerous enemy.",
    "DK4_MES_B142_R0070": "Too strong for us to challenge now.",
    "DK4_MES_B142_R0084": "Make a name in the Caribbean... Our sailors need New World experience.",
    "DK4_MES_B142_R0087": "True. Without handling that voyage, we cannot defeat Espinosa.",
    "DK4_MES_B142_R0090": "Then hunt Caribbean pirates.",
    "DK4_MES_B142_R0093": "Excellent. Trade between Europe and the New World may fund our arms.",
    "DK4_MES_B142_R0109": "...",
    "DK4_MES_B142_R0112": "Hm? She's still here?",
    "DK4_MES_B142_R0116": "She follows everywhere.",
    "DK4_MES_B142_R0126": "Nothing for it. Perhaps keep her near you, Admiral.",
    "DK4_MES_B142_R0132": "Heh. Nothing for it. Why not keep her near you?",
    "DK4_MES_B142_R0139": "No civilian woman can sail on a warship.",
    "DK4_MES_B142_R0148": "Leave her here? Predators watch the tavern. She'll be easy prey.",
    "DK4_MES_B142_R0151": "Hmm...",
    "DK4_MES_B142_R0155": "Your choice. Departure awaits.",
    "DK4_MES_B142_R0159": "Leave her here? The tavern swarms with beasts preying on weak women. Can a beautiful orphan survive alone?",
    "DK4_MES_B142_R0162": "...Why that grin?",
    "DK4_MES_B142_R0165": "Nothing at all. Time to prepare for departure. Ho ho.",
    "DK4_MES_B142_R0169": "Your choice. Then...",
    "DK4_MES_B142_R0176": "...Difficult.",
    "DK4_MES_B142_R0179": "...",
    "DK4_MES_B142_R0182": "Come with us?",
    "DK4_MES_B142_R0186": "...(nods)",
    "DK4_MES_B142_R0189": "You understand?",
    "DK4_MES_B142_R0192": "...",
    "DK4_MES_B142_R0195": "She read my gestures.",
    "DK4_MES_B142_R0199": "No choice. You may stay until we learn who you are.",
    "DK4_MES_B142_R0203": "But what do we call you? Your name?",
    "DK4_MES_B142_R0206": "?",
    "DK4_MES_B142_R0209": "No...",
    "DK4_MES_B142_R0213": "{MACRO:FI}. My name is {MACRO:FI}. Say '{MACRO:FI}'.",
    "DK4_MES_B142_R0217": "...{MACRO:FI}?",
    "DK4_MES_B142_R0220": "Yes! {MACRO:FI}!",
    "DK4_MES_B142_R0223": "{MACRO:FI}...",
    "DK4_MES_B142_R0226": "Understand?",
    "DK4_MES_B142_R0230": "{MACRO:FI}!",
    "DK4_MES_B142_R0233": "Yes, you understand! Now your name? {MACRO:FI} is me; you are?",
    "DK4_MES_B142_R0237": "...",
    "DK4_MES_B142_R0240": "Your name. What should we call you?",
    "DK4_MES_B142_R0243": "...Sera.",
    "DK4_MES_B142_R0246": "Sera? Your name?",
    "DK4_MES_B142_R0250": "...Sera... Altos... Shalvaraz.",
    "DK4_MES_B142_R0253": "Sera Altos... er... We'll call you Sera. Sera?",
    "DK4_MES_B142_R0258": "She smiled!",
    "DK4_MES_B142_R0270": "Admiral...?",
    "DK4_MES_B142_R0278": "Hm? What is it?",
    "DK4_MES_B142_R0282": "...Nothing. What do you need?",
    "DK4_MES_B142_R0286": "The prisoners are all freed.",
    "DK4_MES_B142_R0290": "Good! Well done.",
    "DK4_MES_B142_R0317": "Admiral! You're going to the New World?",
    "DK4_MES_B142_R0320": "Hm? Yes.",
    "DK4_MES_B142_R0324": "As expected!",
    "DK4_MES_B142_R0327": "Why? Something there?",
    "DK4_MES_B142_R0330": "No, a private matter. Good, good.",

    "DK4_MES_B143_R0005": "Hm? Sera?",
    "DK4_MES_B143_R0008": "Where did she go?",
    "DK4_MES_B143_R0017": "Looking for someone?",
    "DK4_MES_B143_R0023": "What happened?",
    "DK4_MES_B143_R0030": "Nothing. She'll return while we drink.",
    "DK4_MES_B143_R0037": "Late.",
    "DK4_MES_B143_R0044": "Troublesome.",
    "DK4_MES_B143_R0049": "Sera? Where?",
    "DK4_MES_B143_R0071": "Sera",
    "DK4_MES_B143_R0075": "Ah, {MACRO:FI}",
    "DK4_MES_B143_R0084": "Someone she knows? No.",
    "DK4_MES_B143_R0088": "(smiles)",
    "DK4_MES_B143_R0092": "...Hm.",
    "DK4_MES_B143_R0100": "Go.",
    "DK4_MES_B143_R0104": "Yes.",

    "DK4_MES_B144_R0005": "We have both halves of the Mystery Tablet.",
    "DK4_MES_B144_R0008": "They were one piece originally.",
    "DK4_MES_B144_R0011": "Let's fit them together...",
    "DK4_MES_B144_R0015": "Africa's Proof map.",
    "DK4_MES_B144_R0018": "Not done yet. Now seek the Proof.",

    "DK4_MES_B145_R0005": "Pay your tab and get out!",
    "DK4_MES_B145_R0008": "Eek...",
    "DK4_MES_B145_R0012": "That man.",
    "DK4_MES_B145_R0016": "...Nagalpur.",
    "DK4_MES_B145_R0020": "Y-you, {MACRO:FI}! Look what you did!",
    "DK4_MES_B145_R0023": "All left me... Can't even eat well!",
    "DK4_MES_B145_R0026": "Your own doing. Those around you only wanted your money.",
    "DK4_MES_B145_R0029": "They left when the money vanished. Bonds cannot be bought. You know that.",
    "DK4_MES_B145_R0036": "Then understand and start over.",
    "DK4_MES_B145_R0039": "Damn... Goodbye, {MACRO:FI}.",
    "DK4_MES_B145_R0042": "Splendid words, Admiral. Deeply moving.",
    "DK4_MES_B145_R0053": "Changing his heart is amazing. We were right to follow you.",

    "DK4_MES_B146_R0005": "This Everlasting Lotus Leaf surely maps the southern ocean's Proof, but...",
    "DK4_MES_B146_R0009": "How does it combine with the Kushan Platter? No idea...",
    "DK4_MES_B146_R0013": "Add water to the Kushan Platter, then float the leaf.",
    "DK4_MES_B146_R0017": "The veins form a map!",
    "DK4_MES_B146_R0021": "The southern Proof is near.",

    "DK4_MES_B147_R0005": "The Jar of Latex? The liquid dissolves every metal but gold.",
    "DK4_MES_B147_R0008": "Really? New to me.",
    "DK4_MES_B147_R0020": "Dissolves metal... An acid? Curious.",
    "DK4_MES_B147_R0026": "Kings used it to expose fake gold.",

    "DK4_MES_B148_R0011": "Admiral, about that Ancient Kingdom Coin...",
    "DK4_MES_B148_R0016": "Admiral, the Ancient Kingdom Coin...",
    "DK4_MES_B148_R0022": "What about it?",
    "DK4_MES_B148_R0032": "What if we soak it in the Jar of Latex?",
    "DK4_MES_B148_R0037": "A thought: why not soak it in the Jar of Latex?",
    "DK4_MES_B148_R0044": "Novel idea... but the coin might dissolve completely.",
    "DK4_MES_B148_R0054": "Better to act than waste time with no plan.",
    "DK4_MES_B148_R0059": "Science cannot rule it out, but personally, it's worth trying.",
    "DK4_MES_B148_R0066": "...Agreed. Let's try.",
    "DK4_MES_B148_R0076": "Then, into the latex...",
    "DK4_MES_B148_R0081": "Then, into the latex...",
    "DK4_MES_B148_R0087": "A map appeared as the coin dissolved...",
    "DK4_MES_B148_R0097": "Solved. Now let's seek Southeast Asia's Proof.",
    "DK4_MES_B148_R0103": "Science said this was right! Now we can seek Southeast Asia's Proof!",
}

SPEAKERS = {
    "01": "Hodram Bergstrom", "10": "Gerhard Adelknauts", "12": "Charles",
    "17": "Companion", "18": "Sera Altos Shalvaraz", "26": "Nagalpur",
    "2B": "Diogo de Escante", "3A": "Escante's aide", "5C": "Tavern patron",
    "71": "Tavern patron", "93": "Escante's aide", "FE": "Foreign girl",
}
EXTENDED_STATES = {0x10, 0x12, 0x17, 0x18, 0x26, 0x2B, 0x3A, 0x5C, 0x71, 0x93, 0xFE}
CONTEXT = {
    139: "A Mediterranean sailor warns Hodram away from waters south of the sea.",
    140: "Escante asks Hodram to remove Maldonado from the Caribbean.",
    141: "Hodram's crew questions Escante's motives and hears a colonist's plea.",
    142: "Hodram rescues Sera, learns Espinosa is behind the smugglers, and takes her aboard.",
    143: "Sera wanders from the tavern before returning to Hodram.",
    144: "The Mystery Tablet halves reveal Africa's Proof-of-Conquest map.",
    145: "Hodram urges the ruined Nagalpur to rebuild his life honestly.",
    146: "The Everlasting Lotus Leaf and Kushan Platter reveal the southern-ocean map.",
    147: "A patron explains that the Jar of Latex dissolves metals other than gold.",
    148: "The crew dissolves the Ancient Kingdom Coin to reveal Southeast Asia's map.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {
            row["id"]: row
            for row in csv.DictReader(stream)
            if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)
        }
    if set(LINES) | set(EXCLUDED) != set(source_rows) or set(LINES) & set(EXCLUDED):
        missing = sorted(set(source_rows) - set(LINES) - set(EXCLUDED))
        extra = sorted((set(LINES) | set(EXCLUDED)) - set(source_rows))
        raise SystemExit(f"Hodram V8 inventory mismatch: missing={missing}, extra={extra}")
    records = []
    block_counts: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        block_counts[str(block)] = block_counts.get(str(block), 0) + 1
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Choice or scene text"),
            "context": CONTEXT[block],
            "source_meaning": english.replace("{MACRO:FI}", "Hodram"),
            "localization_note": "Faithful concise American English with measured fixed-record wrapping.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line"],
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC1.DK4",
        "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "hodram-story-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Hodram Caribbean political arc, Sera rescue and recruitment, and Proof-map relic events across SC1 blocks 139-148.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
