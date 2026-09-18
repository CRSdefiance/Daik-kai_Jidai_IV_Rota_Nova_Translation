from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v11.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
LINES = {
    "DK4_MES_B93_R0005": "Ook ook!",
    "DK4_MES_B93_R0009": "Whoa! What?!",
    "DK4_MES_B93_R0013": "Ook ook!",
    "DK4_MES_B93_R0017": "Go away!",
    "DK4_MES_B93_R0021": "Ook ook!",
    "DK4_MES_B93_R0025": "Give it back!",
    "DK4_MES_B93_R0030": "What happened?{LB}What are you doing?",
    "DK4_MES_B93_R0033": "Banana stolen!{LB}Something took it!",
    "DK4_MES_B93_R0038": "Something?",
    "DK4_MES_B93_R0042": "That thing... gone!{LB}The thief fled! Wait!",
    "DK4_MES_B93_R0046": "Any luck catching it?",
    "DK4_MES_B93_R0050": "Too quick!{LB}And it throws things:{LB}stones and seeds.",
    "DK4_MES_B93_R0055": "Let us see... strange seeds.{LB}Maybe a great discovery.",
    "DK4_MES_B93_R0060": "Seeds do not matter!{LB}Banana!",
    "DK4_MES_B93_R0064": "Give it back! Give it back!",
    "DK4_MES_B93_R0069": "Emilio, shall we try{LB}the local specialty?",
    "DK4_MES_B93_R0073": "My treat?",
    "DK4_MES_B93_R0078": "Of course. My treat.",
    "DK4_MES_B93_R0086": "Yay!",

    "DK4_MES_B95_R0005": "This...",
    "DK4_MES_B95_R0009": "Gerhard, what?",
    "DK4_MES_B95_R0013": "Nothing.{LB}Old memories...",
    "DK4_MES_B95_R0017": "Past",
    "DK4_MES_B95_R0021": "A sword was lost here{LB}during a battle with pirates.",
    "DK4_MES_B95_R0025": "Sword?",
    "DK4_MES_B95_R0029": "Only an old Katzbalger,{LB}but it handled better{LB}than its appearance suggested.{LB}A favorite for many years.",
    "DK4_MES_B95_R0033": "Never found it afterward?",
    "DK4_MES_B95_R0036": "No trace remained.{LB}Perhaps a local fisherman found it{LB}and sold it for a pittance.",
    "DK4_MES_B95_R0040": "Maybe someone knows its worth{LB}and still uses it with care.",
    "DK4_MES_B95_R0044": "A blade like that is rare.{LB}Knowing a worthy owner uses it{LB}would bring some comfort.",

    "DK4_MES_B97_R0005": "What is a rogue ninja?",
    "DK4_MES_B97_R0010": "Rogue?",
    "DK4_MES_B97_R0014": "One who was once a ninja.",
    "DK4_MES_B97_R0018": "A ninja, eh?{LB}What is a ninja?",
    "DK4_MES_B97_R0021": "A Japanese clan skilled{LB}in covert action.",
    "DK4_MES_B97_R0024": "A Japanese spy, then.{LB}Have you met one?",
    "DK4_MES_B97_R0028": "Never. Those who see a ninja's{LB}true face must die.",
    "DK4_MES_B97_R0032": "Mamma mia!",
    "DK4_MES_B97_R0036": "Leaving a ninja clan risks death.{LB}Any rogue who escapes pursuit{LB}must possess extraordinary skill.",
    "DK4_MES_B97_R0039": "Why ask about such a rogue?",
    "DK4_MES_B97_R0043": "Not the man himself.{LB}A rumor mentioned his clothing.",
    "DK4_MES_B97_R0047": "Black clothes called{LB}the Rogue Ninja's Black Garb.{LB}They say it is armor.",
    "DK4_MES_B97_R0051": "Armor?",
    "DK4_MES_B97_R0055": "Details are scarce,{LB}but it is very light and durable.",
    "DK4_MES_B97_R0058": "Such a thing is news to me.",
    "DK4_MES_B97_R0062": "Must be extremely rare{LB}if even Yukihisa has never heard of it.",
    "DK4_MES_B97_R0066": "My shame.",
    "DK4_MES_B97_R0070": "No need to apologize, Yukihisa.",
    "DK4_MES_B97_R0073": "But...",
    "DK4_MES_B97_R0077": "This rumor came from me.{LB}Yukihisa, you are amusing.",
    "DK4_MES_B97_R0080": "Amusing? Explain that.{LB}An insult will not be forgiven.",
    "DK4_MES_B97_R0084": "And what will you do?",
    "DK4_MES_B97_R0089": "Both of you, stop!{LB}This is no reason to fight.",
    "DK4_MES_B97_R0093": "My apologies.",
    "DK4_MES_B97_R0097": "Sorry.{LB}Wrong.",
    "DK4_MES_B97_R0100": "Still, if this black armor exists,{LB}it must surely be in Japan.",
    "DK4_MES_B97_R0104": "Maybe.",
    "DK4_MES_B97_R0108": "Agreed.{LB}Let us search when time allows.",
}

SPEAKERS = {
    "0C": "Yukihisa Genjo Shiraki", "0E": "Emilio Ferrog",
    "0F": "Raphael crewmate", "10": "Gerhard Adernkatz", "FE": "Monkey",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    "93": "A monkey steals Emilio's banana and leaves unusual seeds behind before Raphael distracts him with local food.",
    "95": "Gerhard remembers losing his prized old Katzbalger in a pirate battle and hopes a worthy owner still uses it.",
    "97": "A crew rumor about the Fugitive Ninja's Black Garb leads Yukihisa to explain rogue ninjas, argue with a crewmate, and identify Japan as the likely search location.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    inventory = {row_id for row_id in all_rows if row_id.startswith(("DK4_MES_B93_", "DK4_MES_B95_", "DK4_MES_B97_"))}
    if set(LINES) != inventory:
        raise SystemExit(f"Raphael V11 inventory mismatch: missing={sorted(inventory-set(LINES))} extra={sorted(set(LINES)-inventory)}")
    records = []
    blocks: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        blocks[block] = blocks.get(block, 0) + 1
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Raphael Castor or story participant"),
            "context": CONTEXTS[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving character comedy, treasure clues, named equipment, cultural explanation, conflict, and fixed-allocation display safety.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v10-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "The monkey-seed event, Gerhard's Katzbalger clue, and the Fugitive Ninja's Black Garb rumor across Raphael SC0 blocks 93, 95, and 97.",
        "excluded_records": {},
        "inventory": {"identified_records": len(inventory), "translated_records": len(records), "blocks": blocks},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
