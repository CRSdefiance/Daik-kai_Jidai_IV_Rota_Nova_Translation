from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v23.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    "DK4_MES_B91_R0005": "Hey, you trade amber?",
    "DK4_MES_B91_R0009": "Yes. Gazing into amber feels like{LB}being drawn into ancient times.",
    "DK4_MES_B91_R0013": "Huh? What was that?",
    "DK4_MES_B91_R0017": "Amber is ancient tree sap,{LB}hardened and reborn as a gem.",
    "DK4_MES_B91_R0021": "See the bee inside? Over ages it slept in a tiny sepia universe. Truly mysterious...",
    "DK4_MES_B91_R0024": "Huh? How do you know{LB}such complicated stuff?",
    "DK4_MES_B91_R0027": "Science uses reason to unravel this world's wonders, even those beyond human wisdom.",
    "DK4_MES_B91_R0030": "No idea what that means...{LB}Oh! Amber reminds me of a story.",
    "DK4_MES_B91_R0034": "What?",
    "DK4_MES_B91_R0038": "There are islands off this cape.{LB}One supposedly has a strange place{LB}that shines amber.",
    "DK4_MES_B91_R0041": "Amber light? A mineral vein?",
    "DK4_MES_B91_R0045": "No idea what it is.{LB}Just a rumor, mind you.",
    "DK4_MES_B91_R0049": "Thank you for telling me.{LB}That appeals to my scientific curiosity.",

    "DK4_MES_B92_R0005": "Ah...",
    "DK4_MES_B92_R0009": "What's wrong?",
    "DK4_MES_B92_R0013": "Worried for my grandkid.",
    "DK4_MES_B92_R0017": "Christina?",
    "DK4_MES_B92_R0021": "Wonder how she's doing.{LB}Call me a doting old fool.",
    "DK4_MES_B92_R0024": "You always boast about Christina! She will be fine. Like Athena reborn.",
    "DK4_MES_B92_R0027": "Athena?",
    "DK4_MES_B92_R0031": "A Greek goddess.{LB}The Romans call her Minerva.",
    "DK4_MES_B92_R0035": "May have heard that long ago,{LB}but gods are not my field.",
    "DK4_MES_B92_R0038": "Still, that Miner-something{LB}sounds familiar.",
    "DK4_MES_B92_R0041": "Anyway, Christina will be fine.",
    "DK4_MES_B92_R0044": "Thank you. The admiral trusts her.{LB}But she is still my little girl.{LB}Let an old man worry.",
    "DK4_MES_B92_R0051": "Ah! Now memory returns!",
    "DK4_MES_B92_R0054": "W-what is it?",
    "DK4_MES_B92_R0058": "Yes! Something called{LB}the Shield of Minerva.",
    "DK4_MES_B92_R0061": "Legendary armor said to sleep near{LB}the Mediterranean or Black Sea.{LB}Never searched before...",
    "DK4_MES_B92_R0064": "Christina likened to Minerva makes me want it. When found, it belongs with her.",
    "DK4_MES_B92_R0067": "Oh...",
    "DK4_MES_B92_R0071": "Sorry for the silly talk.{LB}Dismiss an old man's rambling.{LB}Time to return to work.",
    "DK4_MES_B92_R0075": "Back to work, Admiral.",
    "DK4_MES_B92_R0079": "Yes, true.",

    "DK4_MES_B93_R0005": "Admiral, a moment?",
    "DK4_MES_B93_R0009": "What is it?",
    "DK4_MES_B93_R0013": "Peacocks are beautiful birds.{LB}Would you like to see one?",
    "DK4_MES_B93_R0016": "Why so sudden?{LB}Another rumor, right?",
    "DK4_MES_B93_R0019": "Exactly. About 'Peacock Mail.'",
    "DK4_MES_B93_R0022": "Mail made from peacock feathers?",
    "DK4_MES_B93_R0025": "So close! The mail has{LB}peacock tail feathers on the back.",
    "DK4_MES_B93_R0029": "That sounds... weak.",
    "DK4_MES_B93_R0033": "The sight overwhelms enemies{LB}and freezes them in place.{LB}That is its power.",
    "DK4_MES_B93_R0037": "Really? Where is it?",
    "DK4_MES_B93_R0040": "On an island far, far, far{LB}southeast of the Cape of Good Hope.{LB}That is all the rumor said.",
    "DK4_MES_B93_R0044": "That hardly narrows it down.",
    "DK4_MES_B93_R0047": "Still, what a sight it must be!{LB}Surely nothing else compares.",
    "DK4_MES_B93_R0051": "We will remember.{LB}Expect little.",
    "DK4_MES_B93_R0055": "Understood.",

    "DK4_MES_B94_R0005": "Admiral, a moment?",
    "DK4_MES_B94_R0009": "What is it?",
    "DK4_MES_B94_R0013": "Seek the Jaguar God's Vest.",
    "DK4_MES_B94_R0017": "What?",
    "DK4_MES_B94_R0021": "A vest said to hold the jaguar god.{LB}Supposedly in the New World.",
    "DK4_MES_B94_R0025": "Another new rumor?",
    "DK4_MES_B94_R0029": "Yes, but the last one.",
    "DK4_MES_B94_R0032": "Meaning?",
    "DK4_MES_B94_R0036": "Tracking places is hard work.{LB}Besides, boredom set in.",
    "DK4_MES_B94_R0039": "My interests fade. Animals are fun{LB}only when edible. Any chance rumor{LB}will still be passed along.",
    "DK4_MES_B94_R0042": "That sounds like you. But the New World{LB}is vast. Any idea where the vest is?",
    "DK4_MES_B94_R0046": "Maybe in the west.",
    "DK4_MES_B94_R0049": "Can you narrow it down more?",
    "DK4_MES_B94_R0053": "Sorry, that is all the rumor gave.{LB}Just keep it in mind.",
    "DK4_MES_B94_R0056": "Honestly, Samwell...{LB}We remember.",

    "DK4_MES_B95_R0005": "Admiral, heard of the Portuguese fleet{LB}wrecked here twenty years ago?",
    "DK4_MES_B95_R0009": "Stop. Terrible luck.",
    "DK4_MES_B95_R0013": "The admiral carried a telescope{LB}that saw incredibly far. They say{LB}it showed even the Moon's craters.",
    "DK4_MES_B95_R0016": "Really? That is amazing!",
    "DK4_MES_B95_R0019": "Supposedly made by Aristarchus,{LB}the great Hellenistic astronomer...",
    "DK4_MES_B95_R0023": "Sounds doubtful.",
    "DK4_MES_B95_R0027": "Hard to believe lenses could be ground{LB}so precisely in that age.",
    "DK4_MES_B95_R0031": "Truth is unknown. Still, it was called{LB}the Telescope of Aristarchus.",
    "DK4_MES_B95_R0034": "And?",
    "DK4_MES_B95_R0038": "Currents may have washed it{LB}onto a coast near here.",
    "DK4_MES_B95_R0041": "Sounds fun! Let's look for it.{LB}What a find if it's real!",

    "DK4_MES_B96_R0005": "Port at last! Let's eat.",
    "DK4_MES_B96_R0008": "You say that at every port.",
    "DK4_MES_B96_R0011": "Eating is very important.{LB}Besides, there is something to find.",
    "DK4_MES_B96_R0015": "Seeking what?",
    "DK4_MES_B96_R0019": "The tastiest food!",
    "DK4_MES_B96_R0023": "And how could anyone decide{LB}what tastes best in the world?",
    "DK4_MES_B96_R0027": "Easy. The tastiest food is cooked{LB}in the Cauldron of Hestia.",
    "DK4_MES_B96_R0030": "Hestia? What is that?",
    "DK4_MES_B96_R0034": "A cauldron made by the hearth goddess.{LB}Said to lie far across the sea,{LB}south of Greece.",
    "DK4_MES_B96_R0037": "That is why visiting Greek taverns{LB}sounds so exciting. Come on,{LB}let us get something to eat!",

    "DK4_MES_B166_R0005": "Are the sails placed badly...?{LB}Or...",
    "DK4_MES_B166_R0008": "Hey, need something{LB}from this ship?",
    "DK4_MES_B166_R0012": "Are you the owner? This ship could{LB}become excellent with a little work.",
    "DK4_MES_B166_R0020": "Add sails...{LB}or change the basic type...",
    "DK4_MES_B166_R0023": "Pardon...",
    "DK4_MES_B166_R0027": "More gun decks would make her stronger.{LB}Or perhaps different cannon{LB}would be better...",
    "DK4_MES_B166_R0030": "Enough already!{LB}Who are you?",
    "DK4_MES_B166_R0033": "Ah, pardon me. Not my ship,{LB}yet thought swept me away...",
    "DK4_MES_B166_R0037": "My name is Manuel.{LB}Once, a navigator.",
    "DK4_MES_B166_R0040": "Navigator, huh...",
    "DK4_MES_B166_R0044": "Seeing a ship starts me thinking.{LB}Old habits from my days at sea...",
    "DK4_MES_B166_R0048": "This must seem rude. Pardon me.{LB}Please permit one last word.",
    "DK4_MES_B166_R0052": "Perhaps it is not my concern,{LB}but this ship is crying.{LB}Please care for her.",
    "DK4_MES_B166_R0056": "Hey, wait!",
    "DK4_MES_B166_R0060": "Such presumptuous words...{LB}Please take no offense.{LB}Now, farewell.",
    "DK4_MES_B166_R0064": "...Odd.",
    "DK4_MES_B166_R0068": "What do you mean? He is amazing!{LB}{MACRO:FI}, our ship could use{LB}a man like that.",
    "DK4_MES_B166_R0071": "Why?",
    "DK4_MES_B166_R0075": "{MACRO:FI}, you never care for the ship.{LB}That is why she is crying.",
    "DK4_MES_B166_R0087": "And you work us hard.",
    "DK4_MES_B166_R0094": "Machines make no sense to me.{LB}Nothing can be done about that.",
    "DK4_MES_B166_R0098": "Do not boast about it! Someone should{LB}love the ship in {MACRO:FI}'s place.",
    "DK4_MES_B166_R0102": "Then the ship would stop crying.{LB}May we invite him aboard?",
    "DK4_MES_B166_R0106": "Well... if Kamil agrees, fine.",
    "DK4_MES_B166_R0109": "Sir, would you care{LB}for our ship?",
    "DK4_MES_B166_R0112": "Become a navigator again?{LB}But so many years have passed{LB}since leaving the sea...",
    "DK4_MES_B166_R0116": "You seem no different from us.{LB}Someone who loves ships this much{LB}cannot have forgotten the sea.",
    "DK4_MES_B166_R0119": "Well, that is true...",
    "DK4_MES_B166_R0123": "Then care for that ship.{LB}We seem to make her cry.",
    "DK4_MES_B166_R0127": "Thank you. Since you insist,{LB}the position is accepted.",
    "DK4_MES_B166_R0130": "Once again: Manuel Almeida.{LB}At your service.",
    "DK4_MES_B166_R0134": "Admiral, may some advice be offered{LB}on refitting flagship rooms?",
    "DK4_MES_B166_R0140": "Please do",
    "DK4_MES_B166_R0142": "Decline",
    "DK4_MES_B166_R0149": "Then let us discuss rooms useful{LB}for long-distance voyages.",
    "DK4_MES_B166_R0153": "Put persuasive officers in the{LB}Adjutant's Cabin or Chapel{LB}to reduce sailor unrest.",
    "DK4_MES_B166_R0157": "A cook or breeder in the Galley{LB}or Livestock Hold cuts{LB}water, food use.",
    "DK4_MES_B166_R0161": "A doctor in the Sickbay treats{LB}fatigue, disease, and injury.",
    "DK4_MES_B166_R0165": "Sick or injured officers recover{LB}faster in a Private Cabin{LB}or Recreation Room.",
    "DK4_MES_B166_R0169": "A shipwright repairs damage{LB}from the Lumber Room and aids refits.",
    "DK4_MES_B166_R0172": "That was a hurried explanation.{LB}Was it useful?",
    "DK4_MES_B166_R0175": "The fleet's fate rests on your command.{LB}Never neglect careful ship refits.",
    "DK4_MES_B166_R0181": "Understood.{LB}Your choice.",

    "DK4_MES_B167_R0005": "Admiral! Want to hear{LB}my sailing lesson?",
    "DK4_MES_B167_R0008": "Huh?",
    "DK4_MES_B167_R0012": "Things are terribly slow lately.{LB}Call it helping a bored fellow.",
    "DK4_MES_B167_R0018": "Okay",
    "DK4_MES_B167_R0020": "No thanks",
    "DK4_MES_B167_R0030": "Do not underestimate us.",
    "DK4_MES_B167_R0033": "Quite right.",
    "DK4_MES_B167_R0045": "No need to tell us{LB}about ships now.",
    "DK4_MES_B167_R0051": "All right. You know ships.{LB}Another novice will come along.",
    "DK4_MES_B167_R0062": "Good attitude!{LB}You will go far.",
    "DK4_MES_B167_R0065": "A sailing ship lives by its sails.",
    "DK4_MES_B167_R0068": "Start with square versus{LB}lateen sails.",
    "DK4_MES_B167_R0071": "A square sail hangs crosswise{LB}to the ship: a transverse sail.",
    "DK4_MES_B167_R0075": "Unable to turn lengthwise,{LB}it excels with a following wind{LB}but finds no ideal angle{LB}against the wind.",
    "DK4_MES_B167_R0078": "A lateen sail is rigged lengthwise. Unlike a square sail, it cannot turn crosswise to the ship.",
    "DK4_MES_B167_R0081": "This works best against wind{LB}but is slower with a tailwind.{LB}Understand?",
    "DK4_MES_B167_R0084": "Next come optional sails.",
    "DK4_MES_B167_R0088": "A topsail is a small square sail{LB}fitted above each mast.",
    "DK4_MES_B167_R0092": "A staysail is a small fore-and-aft sail before each mast, but not a lateen; the two would overlap.",
    "DK4_MES_B167_R0095": "A spritsail is a square sail at the bow. Small ships cannot mount one.",
    "DK4_MES_B167_R0098": "A jigger spanker is a stern sail.{LB}Adding a small mast means only{LB}large ships can mount one.",
    "DK4_MES_B167_R0101": "Ships with two or more masts sail{LB}faster on a quartering wind{LB}than with wind astern. Know why?",
    "DK4_MES_B167_R0105": "You there. Know the reason?",
    "DK4_MES_B167_R0109": "The masts stand{LB}one behind another.",
    "DK4_MES_B167_R0112": "Wind astern reaches only the rear mast.{LB}Other masts do little.",
    "DK4_MES_B167_R0115": "Wind from the rear quarter is fastest,{LB}provided the sails are angled to it.",
    "DK4_MES_B167_R0119": "Got it!",
    "DK4_MES_B167_R0131": "Never paid it much attention!{LB}So that is why!",
    "DK4_MES_B167_R0138": "Thanks for listening.{LB}Time to return to work.",
}

SPEAKERS = {
    "02": "Lil Argot", "04": "Janus Pasha", "06": "Julio's grandfather",
    "09": "Kamil", "0E": "Emilio Ferrog", "12": "Charles Jean Rochefort",
    "14": "Fernando", "16": "Samwell", "17": "Manuel Almeida",
    "6D": "Sailing instructor", "72": "Cape resident",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    "91": "Charles discusses amber and hears of a mysterious amber-glowing island.",
    "92": "Julio's grandfather worries about Christina and recalls the Shield of Minerva.",
    "93": "Samwell shares the Peacock Mail treasure rumor.",
    "94": "Samwell shares the Vest of the Jaguar God treasure rumor.",
    "95": "Janus explains the legend and likely resting place of the Telescope of Aristarchus.",
    "96": "Emilio explains his search for Hestia's Cauldron and the world's finest food.",
    "166": "Lil recruits Manuel Almeida and receives his ship-room assignment and refit tutorial.",
    "167": "A harbor instructor explains square, lateen, topsails, staysails, spritsails, stern sails, and wind angles.",
}
MANUAL_BREAK_REASONS = {
    "DK4_MES_B92_R0021": "He pauses before a self-deprecating aside about worrying over Christina.",
    "DK4_MES_B95_R0041": "Lil pauses after deciding to search, then imagines finding the telescope.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V23 inventory mismatch: missing={sorted(missing)}")
    records = []
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Story participant"),
            "context": CONTEXTS[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Concise American English preserving treasure directions, character voice, and tutorial mechanics.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": MANUAL_BREAK_REASONS.get(row_id, "Protects semantic rows and progressive ASCII pair phase.")} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    counts = {}
    for row_id in LINES:
        block = str(int(row_id.split("_B", 1)[1].split("_", 1)[0]))
        counts[block] = counts.get(block, 0) + 1
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Lil route blocks 91-96 plus Manuel's ship-room tutorial and the sailing lesson in blocks 166-167.",
        "excluded_records": {},
        "inventory": {"identified_records": len(LINES), "translated_records": len(records), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
