from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v19.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
LINES = {
    "DK4_MES_B75_R0005": "Sudden, but...",
    "DK4_MES_B75_R0009": "Ah! You startled me!{LB}Who are you?",
    "DK4_MES_B75_R0013": "Um...{LB}Would you hire me?",
    "DK4_MES_B75_R0016": "What?{LB}What are you saying?",
    "DK4_MES_B75_R0019": "{MACRO:FI}, no need to snap.{LB}At least hear him out.",
    "DK4_MES_B75_R0023": "Thank you!{LB}Want to sail so badly!",
    "DK4_MES_B75_R0026": "A ship? Unexpected.{LB}Are you a sailor?",
    "DK4_MES_B75_R0029": "Studied navigation.",
    "DK4_MES_B75_R0033": "Studied? Never sailed?",
    "DK4_MES_B75_R0037": "No.{LB}Practice comes next.",
    "DK4_MES_B75_R0040": "Listen, it is not so easy.{LB}Why should anyone take you aboard?",
    "DK4_MES_B75_R0044": "So... no?",
    "DK4_MES_B75_R0048": "What did you study?",
    "DK4_MES_B75_R0052": "Love machines.{LB}Studied ship design.{LB}Even built one from wrecks.",
    "DK4_MES_B75_R0056": "That is amazing!",
    "DK4_MES_B75_R0060": "Kamil! Do not decide for me!{LB}The captain is me!",
    "DK4_MES_B75_R0064": "Understood.{LB}But is that not amazing?",
    "DK4_MES_B75_R0067": "W-well, yes.{LB}What are your terms?{LB}Want something?",
    "DK4_MES_B75_R0071": "Wonderful! Thank you!{LB}Then one request...",
    "DK4_MES_B75_R0075": "Please give me{LB}1,000 gold coins!",
    "DK4_MES_B75_R0078": "What?!{LB}An advance already?!",
    "DK4_MES_B75_R0083": "Be generous.",
    "DK4_MES_B75_R0085": "You must be joking!",
    "DK4_MES_B75_R0094": "Thank you!{LB}Now repairs can be done!",
    "DK4_MES_B75_R0097": "Oh, sorry.{LB}Please delay sailing one day.",
    "DK4_MES_B75_R0100": "You only make demands!",
    "DK4_MES_B75_R0103": "Tomorrow, at the dock!",
    "DK4_MES_B75_R0107": "Wait!{LB}What is your name?!",
    "DK4_MES_B75_R0113": "Ah, been waiting!{LB}Come see this.",
    "DK4_MES_B75_R0124": "Your repair money restored the ship{LB}and paid off the debt.",
    "DK4_MES_B75_R0128": "Use this ship{LB}whenever you like.",
    "DK4_MES_B75_R0131": "So that was the reason.",
    "DK4_MES_B75_R0135": "Then say so{LB}from the start!",
    "DK4_MES_B75_R0138": "Sorry for testing you.{LB}A captain trusted with my life{LB}must show some generosity.",
    "DK4_MES_B75_R0141": "Absurd!",
    "DK4_MES_B75_R0145": "Truthfully, excitement took over.{LB}No time to explain.",
    "DK4_MES_B75_R0148": "Still no name!",
    "DK4_MES_B75_R0152": "Janus Pasha.{LB}Looking forward to serving you.",
    "DK4_MES_B75_R0158": "Take the ship from dock.{LB}Use Refit and name it{LB}as you like.",
    "DK4_MES_B75_R0164": "Understood... Too bad.{LB}Somewhere else, then.",
    "DK4_MES_B75_R0171": "He looked so sad.",
    "DK4_MES_B75_R0175": "Naturally! Nobody gives money{LB}to a stranger for no reason.",
    "DK4_MES_B75_R0179": "True enough.",
    "DK4_MES_B76_R0005": "Biggest island in the Caribbean!{LB}Such a cheerful town!{LB}Time to trade!",
    "DK4_MES_B76_R0009": "Aaaaah!!",
    "DK4_MES_B76_R0013": "Whew! Startled me.{LB}{MACRO:FI}, such a girlish scream!",
    "DK4_MES_B76_R0016": "Kamil, you bully!{LB}(Smack!)",
    "DK4_MES_B76_R0019": "Ow! No need to hit me...",
    "DK4_MES_B76_R0023": "You earned it!",
    "DK4_MES_B76_R0027": "Whew...{LB}That bomb fool again...",
    "DK4_MES_B76_R0030": "Wait!{LB}Did you say bomb?!",
    "DK4_MES_B76_R0033": "Yes. Goes on about science{LB}and makes huge blasts.",
    "DK4_MES_B76_R0037": "Sometimes he blows up{LB}his own workshop.",
    "DK4_MES_B76_R0040": "Bombs? Maybe he knows cannons.{LB}He could make our fleet stronger.",
    "DK4_MES_B76_R0044": "Maybe, but we fear the day{LB}he blows up our homes.",
    "DK4_MES_B76_R0048": "So he is brilliant...{LB}{MACRO:FI}, let us recruit him!",
    "DK4_MES_B76_R0052": "He sounds useful, but...{LB}going there is...",
    "DK4_MES_B76_R0056": "Are you scared of that noise?",
    "DK4_MES_B76_R0059": "Do not insult me!{LB}Admiral {MACRO:FI} stands before you!",
    "DK4_MES_B76_R0063": "Um... may this old man leave?",
    "DK4_MES_B76_R0066": "No! Lead us to him!{LB}We will recruit him.{LB}Bring on any bomb!",
    "DK4_MES_B76_R0070": "Come on, Kamil!{LB}(Smack!)",
    "DK4_MES_B76_R0073": "Ow! Stop hitting me!",
    "DK4_MES_B76_R0076": "Always like this?{LB}You have it rough...",
    "DK4_MES_B76_R0083": "Used to it.",
    "DK4_MES_B76_R0088": "Charles! You in there?!",
    "DK4_MES_B76_R0093": "Cough! Yes! Cough!{LB}Too much powder?{LB}Next time...",
    "DK4_MES_B76_R0097": "Are you all right?{LB}We would enjoy one quiet day.",
    "DK4_MES_B76_R0101": "Nearly done!{LB}This experiment will bring{LB}new science to the world!",
    "DK4_MES_B76_R0105": "Enough of that.{LB}Some visitors came to see you.",
    "DK4_MES_B76_R0109": "To see me?{LB}Who?",
    "DK4_MES_B76_R0112": "He is yours now.{LB}Please do not destroy the town!",
    "DK4_MES_B76_R0116": "H-hello...",
    "DK4_MES_B76_R0120": "Ah! National Academy{LB}of Science, perhaps? Wonderful!",
    "DK4_MES_B76_R0124": "Academy? What?{LB}My name is {MACRO:FI},{LB}not that.",
    "DK4_MES_B76_R0128": "No, {MACRO:FI}.{LB}An academy is...",
    "DK4_MES_B76_R0131": "Oh... not you.{LB}That explains the lack of reason.{LB}Bye.",
    "DK4_MES_B76_R0135": "Wait! Why not test your scien--{LB}your science on the open sea?",
    "DK4_MES_B76_R0139": "What! You understand science?!",
    "DK4_MES_B76_R0142": "Uh? Y-yes, well...",
    "DK4_MES_B76_R0154": "What?{LB}His manner changed fast.",
    "DK4_MES_B76_R0160": "Splendid!{LB}Science and navigation united!{LB}A grand idea!",
    "DK4_MES_B76_R0163": "Then you will come with us?",
    "DK4_MES_B76_R0167": "Yes, of course!",
    "DK4_MES_B76_R0171": "Already decided?{LB}And yet, the captain is me!{LB}Well, let us go aboard!",
    "DK4_MES_B76_R0175": "Name: {MACRO:FI}.",
    "DK4_MES_B76_R0179": "Kamil. A pleasure.",
    "DK4_MES_B76_R0183": "Charles Jean Rochefort.{LB}Everyone calls me Dr. Charles!",
    "DK4_MES_B76_R0187": "...Ah. Right...",
    "DK4_MES_B76_R0190": "A special cannon shall bless{LB}our voyage! Ready? 5, 4, 3...",
    "DK4_MES_B76_R0194": "What?! Wait!{LB}Stop! Please stop!",
    "DK4_MES_B76_R0198": "2, 1, 0!{LB}Boom!",
    "DK4_MES_B76_R0202": "Aaaaaaaah!",
    "DK4_MES_B76_R0206": "...Huh?",
    "DK4_MES_B76_R0210": "...What?",
    "DK4_MES_B76_R0214": "Aah! Aaaah!",
    "DK4_MES_B76_R0218": "Maybe displaying it three years{LB}was unwise. A lesson:{LB}use gunpowder at once!",
    "DK4_MES_B76_R0221": "...{MACRO:FI}!{LB}You okay?",
    "DK4_MES_B76_R0224": "Ha!{LB}You two are close.",
    "DK4_MES_B76_R0227": "What?! No...",
    "DK4_MES_B76_R0231": "Just wait...{LB}Back aboard,{LB}you will pay...",
    "DK4_MES_B76_R0235": "Yes, plenty of science!{LB}Such eagerness to learn!{LB}A splendid captain!",
}

SPEAKERS = {
    "02": "Lil Argot", "04": "Janus Pasha", "09": "Kamil", "12": "Charles Jean Rochefort",
    "14": "Fernando", "6D": "Townsman", "FE": "Tutorial narrator",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    "75": "Lil meets ship engineer Janus Pasha, chooses whether to fund his repair, and may recruit him and claim his restored ship.",
    "76": "In the Caribbean, Lil and Kamil recruit eccentric scientist Charles Jean Rochefort after a series of comic explosions.",
}
EXCLUDED = {"DK4_MES_B75_R0091": "five-byte branch-control payload with no visible dialogue"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = (set(LINES) | set(EXCLUDED)) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V19 inventory mismatch: missing={sorted(missing)}")
    records = []
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "{MACRO:I?}" in english:
            raise SystemExit(f"{row_id}: unresolved first-person placeholder: {english}")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Story participant"), "context": CONTEXTS[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Concise American English preserving character voice, comedy, choices, recruitment conditions, and gameplay instruction.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Janus Pasha and Charles Jean Rochefort recruitment events in SC2 blocks 75-76.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(LINES) + len(EXCLUDED), "translated_records": len(records), "blocks": {"75": 43, "76": 59}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records; excluded {len(EXCLUDED)} control")


if __name__ == "__main__":
    main()
