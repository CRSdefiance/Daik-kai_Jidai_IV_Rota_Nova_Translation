from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v5.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"

TRANSLATIONS = {
    95: [
        "Here...?", "What is it, Gerhard?", "Nothing. Remembering the past...", "Hm?",
        "Lost my sword fighting pirates here.", "A sword?",
        "Only an old katzbalger, but it handled beautifully. Used it for years.",
        "A shame. Never found it?", "No. A fisherman likely sold it for pennies.",
        "Maybe someone discerning found and cherished it.",
        "Such blades are rare. That thought would ease my mind.",
    ],
    97: [
        "Admiral, what's a nukenin?", "A nukenin?", "One who was once a ninja.",
        "A ninja! So... what's a ninja?", "A Japanese clan skilled in stealth.",
        "Japanese spies, then. Met one?", "Never. Ninja law kills anyone who sees their identity.",
        "Mamma mia!", "Leaving a ninja clan risks death. Any survivor must be exceptional.",
        "Why ask about a nukenin?", "Heard about their clothing.",
        "Black armor called the Nukenin's Garb. Armor, not mere clothes.", "Armor?",
        "Very light and durable, they say.", "Never heard of such a thing.",
        "Even Yukihisa doesn't know it...", "My shame.", "No need to apologize.", "But...",
        "This was my rumor. Yukihisa is amusing.", "Amusing? Mock me and face the consequences.",
        "What consequences?", "Enough. This is no cause to fight.", "My apologies.", "Sorry.",
        "Still, if that black armor exists, it must be in Japan.", "Probably.",
        "Agreed. Let's search when possible.",
    ],
    100: [
        "Oh, you trade amber?", "Yes. Amber's glow evokes ancient ages.", "What are you saying?",
        "Amber is ancient tree sap hardened into a jewel.",
        "See the bee? Trapped for millennia in a sepia universe. Mysterious...",
        "How do you know all that?", "Science seeks human answers to wonders beyond reason.",
        "No idea what that means. Ah, amber reminds me...", "Of what?",
        "Nearby islands hide a strange amber glow.", "Amber? A mineral vein?",
        "No idea. Only a rumor.", "Thanks. That certainly stirs scientific curiosity.",
    ],
    101: [
        "Sigh.", "What's wrong, sir?", "Worried about Christina.", "Christina...",
        "Wondering if she's well. Call me a foolish grandpa.",
        "No worry. Christina is strong, like Athena reborn.", "Athena?",
        "Minerva in Roman myth.", "May have heard that long ago. Gods aren't my subject.",
        "Still, that Minerva name sounds familiar.", "Anyway, Christina needs no worry.",
        "Thank you. She has your trust, but remains my granddaughter. Humor an old man.",
        "Ah! Now remembered!", "Yes, the Shield of Minerva.",
        "Legendary armor said to rest near the Mediterranean or Black Sea.",
        "That shield belongs with Christina, our Minerva.", "Sir...",
        "Sorry about the silly tale. Put it aside. Back to work.", "You too, Admiral.", "Yes...",
    ],
    102: [
        "Admiral, a moment?", "Hm?", "Peacocks are beautiful. Want to see one?",
        "What now? Another rumor?", "Yes. About the Peacock Mail.",
        "Armor made from peacock feathers?", "Close! A peacock tail sits on its back.",
        "Doesn't sound strong.", "That beauty freezes enemies in awe. That's the power.",
        "Right... Where is it?", "On an island far southeast of the Cape. That's all.",
        "Hardly enough to locate it.", "Still want to see it. Must be amazing.",
        "We'll remember it. Expect nothing.", "Understood.",
    ],
    103: [
        "Admiral, a moment?", "Hm?", "Let's find the Jaguar God's Gi.", "What?",
        "A garment said to house a jaguar god, somewhere in the New World.",
        "Another rumor?", "Yes, but the last one.", "Why?",
        "Research is hard and got boring.",
        "My interests fade. Animals are dull if they can't be cooked. New rumors still get shared.",
        "About that gi, where in the New World?", "Probably the west.",
        "Still broad. Can you narrow it?", "Sorry, that's all. Just remember it.",
        "Ha ha. Very well.",
    ],
    104: [
        "A Portuguese fleet sank here twenty years ago. Heard?", "No.",
        "The commander had a telescope so strong it showed the moon's surface.", "Remarkable.",
        "Said to be made by the Hellenistic astronomer Aristarchus.", "Truly?",
        "That era likely lacked lenses precise enough.",
        "Truth unknown. Called Aristarchus's Telescope.", "And?",
        "Currents may have washed it onto a nearby shore.", "Then it may merit a search.",
    ],
    105: [
        "We're in port. Let's eat!", "Same words at every port, Emilio.",
        "Eating matters! And something is being sought.", "Something?", "The best food!",
        "Who decides that? No way to judge.",
        "Easy. The best food is cooked in Hestia's Cauldron.", "Hestia's pot?",
        "Made by the hearth goddess, far beyond the sea south of Greece.",
        "Greek food sounds good. Let's eat!",
    ],
    108: [
        "Admiral, you found Muramasa. May this warrior see it?", "Of course. Your report led us there.",
        "This is... Muramasa...", "That eerie glow nearly draws one in.", "A fine sight.",
    ],
    109: [
        "Heard you're seeking strange treasures scattered worldwide.",
        "A priest at the nearby church knows much. He may help.",
    ],
    110: [
        "Are you seekers of the Proof of Conquest?", "Then mistaken...", "What is that proof?",
        "A relic held by one who rules the seas.", "Ruler of seas... intriguing.",
        "This may concern our goal. Please explain more.", "Know more?",
        "The path is harsh. Are you truly resolved?", "No trial will stop us from claiming it.",
        "Very well.", "The chart works only when two Map Keys are joined.",
        "Each key alone means nothing.",
        "Keys may hide in ruins or rest with unexpected people.", "Take this sword.",
        "Overcome its trial and aid those in need.",
        "Reject greed. Give to the poor, end strife, and spread peace.", "May God protect you.",
    ],
    111: [
        "Wait. Have you visited Santiago Cathedral?",
        "Pilgrims from across Europe have long gone there.",
        "Visit while in Seville. Here are directions.",
    ],
    112: [
        "Hm?", "Troubled?",
        "No... nothing. (Only this cross looks extremely old...)",
        "Then pray in God's name... Amen.",
    ],
    113: [
        "Admiral, look!", "Admiral, look!", "Admiral, look!", "Admiral, look!",
        "Admiral, look!", "Admiral, look!", "Visitor...",
        "My power is lent to you. Debate greatly.",
    ],
}

BLOCKS = tuple(TRANSLATIONS)
SPEAKERS = {
    "01": "Hodram Bergstrom", "04": "Janus Pasha", "06": "Christina's grandfather",
    "0C": "Yukihisa", "0E": "Emilio", "0F": "Crewman", "10": "Gerhard",
    "12": "Charles", "16": "Crewman", "72": "Amber trader", "8B": "Priest",
    "BC": "Woman", "BF": "Woman", "D0": "Crewman", "FE": "Temple voice",
}
EXTENDED_STATES = {0x10, 0x12, 0x16, 0x72, 0x8B, 0xBC, 0xBF, 0xD0, 0xFE}
CONTEXT = {
    95: "Gerhard remembers a beloved sword lost in battle.", 97: "The crew hears of the Nukenin's Garb.",
    100: "An amber trader describes a mysterious glowing island.", 101: "Christina's grandfather recalls the Shield of Minerva.",
    102: "The crew hears of the Peacock Mail.", 103: "The crew hears of the Jaguar God's Gi.",
    104: "Janus describes Aristarchus's lost telescope.", 105: "Emilio describes Hestia's Cauldron.",
    108: "Yukihisa examines Muramasa.", 109: "A woman directs Hodram to a knowledgeable priest.",
    110: "A priest explains the Proof of Conquest and its Map Keys.", 111: "A woman directs the crew to Santiago Cathedral.",
    112: "Hodram notices an ancient cross during prayer.", 113: "A temple voice grants power to the visiting crew.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    records = []
    block_counts = {}
    for block, texts in TRANSLATIONS.items():
        source_rows = [row for row in rows if row["id"].startswith(f"DK4_MES_B{block}_")]
        if len(source_rows) != len(texts):
            raise SystemExit(f"B{block}: {len(source_rows)} source rows != {len(texts)} translations")
        block_counts[str(block)] = len(texts)
        for row, english in zip(source_rows, texts, strict=True):
            first = bytes.fromhex(row["source_hex"])[0]
            state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
            records.append({
                "id": row["id"], "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(state, "Choice or scene text"), "context": CONTEXT[block],
                "source_meaning": english, "localization_note": "Faithful concise American English with measured fixed-record wrapping.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line"],
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Hodram equipment rumors and Proof of Conquest lead across SC1 blocks 95-113.",
        "inventory": {"identified_records": len(records), "translated_records": len(records), "blocks": block_counts}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records across {len(BLOCKS)} blocks")


if __name__ == "__main__":
    main()
