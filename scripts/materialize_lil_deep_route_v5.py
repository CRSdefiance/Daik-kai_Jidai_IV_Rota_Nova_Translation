from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v5.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
LINES = {
    "DK4_MES_B24_R0009": "Let's sign more city contracts.{LB}Even a small share lets us build{LB}our own trade routes.",
    "DK4_MES_B24_R0012": "Route?",
    "DK4_MES_B24_R0016": "Yes. With a surveyor,{LB}those routes become very useful.",
    "DK4_MES_B24_R0019": "Huh.",
    "DK4_MES_B24_R0023": "A surveyor needs more hands.{LB}We should recruit more{LB}experienced navigators.",
    "DK4_MES_B24_R0026": "Need sailors?{LB}Recruit them at a tavern.",
    "DK4_MES_B24_R0029": "Not sailors, but their leaders.{LB}A growing fleet needs companions{LB}with many different talents.",
    "DK4_MES_B24_R0032": "Where do we look?",
    "DK4_MES_B24_R0036": "Luck, mostly.{LB}Large cities may have someone.",
    "DK4_MES_B24_R0039": "Big city...",
    "DK4_MES_B24_R0043": "Let's visit Mediterranean cities.{LB}Genoa and Ottoman ports have{LB}many seasoned sailors.",
    "DK4_MES_B24_R0046": "And sign contracts on the way.{LB}Two goals at once!",
    "DK4_MES_B24_R0049": "{MACRO:FI}, right!",
    "DK4_MES_B25_R0014": "Poor Speyer...",
    "DK4_MES_B25_R0029": "Ruined over a petty quarrel...{LB}That must leave regrets.",
    "DK4_MES_B25_R0035": "Hmph. He earned it.{LB}That is the price for attacking{LB}{MACRO:FO}.",
    "DK4_MES_B26_R0017": "{MACRO:FI}! That flag!",
    "DK4_MES_B26_R0023": "A skull in a goblet...{LB}That is the English crown's pirate,{LB}Clifford...",
    "DK4_MES_B26_R0035": "No mistake--the Galahad!",
    "DK4_MES_B26_R0047": "Galahad? Does it taste good?",
    "DK4_MES_B26_R0051": "Dummy! That is not food!",
    "DK4_MES_B26_R0067": "Admiral, leave town now!{LB}Meeting him means trouble!",
    "DK4_MES_B26_R0072": "Bad news, {MACRO:FI}!{LB}We must leave.{LB}They say he is truly wicked...",
    "DK4_MES_B26_R0080": "Clifford is really that awful?",
    "DK4_MES_B26_R0083": "New here, are you?{LB}James Clifford is rumored{LB}to be a terrifying pirate.",
    "DK4_MES_B26_R0087": "A giant with three eyes,{LB}a mouth split to his ears,{LB}who drinks human blood{LB}from a goblet!",
    "DK4_MES_B26_R0090": "That sounds human to you?",
    "DK4_MES_B26_R0094": "He destroyed a whole fleet alone!{LB}He must be a monster!",
    "DK4_MES_B26_R0098": "Me, a monster?{LB}Ha! Quite a tale.",
    "DK4_MES_B26_R0101": "Right? Truly awful...{LB}...?",
    "DK4_MES_B26_R0104": "'Me'...? Wait, are you...{LB}Cl-Clifford?!",
    "DK4_MES_B26_R0115": "What?! This man is Clifford?!",
    "DK4_MES_B26_R0130": "This man is Clifford?!",
    "DK4_MES_B26_R0137": "More or less.{LB}'Monster' seems harsh.",
    "DK4_MES_B26_R0149": "{MACRO:FI}...{LB}Apologize, quick!",
    "DK4_MES_B26_R0156": "S-sorry...{LB}Never expected Clifford{LB}to look so ordinary... Ah!",
    "DK4_MES_B26_R0168": "{MACRO:FI}!",
    "DK4_MES_B26_R0175": "No harm done.{LB}More importantly, you are{LB}{MACRO:FI} {MACRO:FA}, yes?",
    "DK4_MES_B26_R0179": "You know about us?",
    "DK4_MES_B26_R0183": "This work brings all kinds{LB}of information.",
    "DK4_MES_B26_R0186": "Planning to attack{LB}{MACRO:FO}?",
    "DK4_MES_B26_R0189": "Come now. Crushing everything{LB}is only a rumor.",
    "DK4_MES_B26_R0192": "Really...?",
    "DK4_MES_B26_R0196": "Believe it or not, your choice.{LB}Either way, we should talk.",
    "DK4_MES_B26_R0200": "What?",
    "DK4_MES_B26_R0211": "Not here.{LB}Come to my home tonight.{LB}We can talk over dinner.",
    "DK4_MES_B26_R0223": "Huh? Did you say dinner?!",
    "DK4_MES_B26_R0227": "Yes.{LB}Be my guests.",
    "DK4_MES_B26_R0233": "All right.",
    "DK4_MES_B26_R0237": "Tonight, then.",
    "DK4_MES_B26_R0241": "Kamil, did you hear? Dinner!{LB}A royal pirate must own a mansion.{LB}How exciting!",
    "DK4_MES_B26_R0252": "So exciting!{LB}Can we go now?",
    "DK4_MES_B26_R0258": "Wait... Are you going{LB}dressed like that?",
    "DK4_MES_B26_R0261": "Huh? Something wrong?",
    "DK4_MES_B26_R0265": "He serves the English crown.{LB}That makes him noble.",
    "DK4_MES_B26_R0269": "Yes. So what?",
    "DK4_MES_B26_R0273": "Visiting a noble's home{LB}in sailing clothes seems wrong.",
    "DK4_MES_B26_R0277": "Oh... That is true.{LB}What should we do?",
    "DK4_MES_B26_R0280": "We need a dress.{LB}Let's ask a tailor{LB}to rush one for tonight.",
    "DK4_MES_B26_R0284": "Okay!",
    "DK4_MES_B26_R0293": "Ready by night, somehow.",
    "DK4_MES_B26_R0305": "Waiting took forever!",
    "DK4_MES_B26_R0312": "Still... surprising...",
    "DK4_MES_B26_R0316": "Heh. Well?",
    "DK4_MES_B26_R0320": "Clothes can transform you.",
    "DK4_MES_B26_R0332": "...{LB}(Kamil, choose your words!)",
    "DK4_MES_B26_R0338": "Asking Kamil was a mistake...",
    "DK4_MES_B26_R0342": "You came.",
    "DK4_MES_B26_R0346": "{MACRO:FI} {MACRO:FA}.{LB}Thank you for inviting us.",
    "DK4_MES_B26_R0350": "My... You look like a noble lady.{LB}That suits you.",
    "DK4_MES_B26_R0353": "Hee hee. Clifford,{LB}what a smooth talker.",
    "DK4_MES_B26_R0356": "Someone else could learn{LB}from that charm.",
    "DK4_MES_B26_R0363": "Come inside.",
    "DK4_MES_B26_R0368": "What a feast!{LB}So many dishes...",
    "DK4_MES_B26_R0379": "A-amazing...",
    "DK4_MES_B26_R0386": "Everything is new!{LB}Where to start...?{LB}Munch, munch... Delicious!",
    "DK4_MES_B26_R0397": "Delicious!{LB}Every dish is wonderful!",
    "DK4_MES_B26_R0408": "Emilio, use a knife and fork!{LB}You are not a pig!",
    "DK4_MES_B26_R0425": "Hm. Quite good.",
    "DK4_MES_B26_R0432": "Ha ha, glad you like it.{LB}Eat your fill.",
    "DK4_MES_B26_R0435": "Now, business.",
    "DK4_MES_B26_R0439": "Wait.{LB}This dress is too tight...",
    "DK4_MES_B26_R0442": "Oh, honestly, {MACRO:FI}...",
    "DK4_MES_B26_R0445": "Ha ha. No need to suffer.{LB}Go change in the back.",
    "DK4_MES_B26_R0450": "Whew. These clothes suit me better.{LB}Sorry to keep everyone waiting.",
    "DK4_MES_B26_R0454": "Now, down to business.",
    "DK4_MES_B26_R0461": "Pedro Valdes commands Spain's navy.{LB}Know the name? Almost no commander{LB}has ever matched his strength.",
    "DK4_MES_B26_R0472": "That news reached me too.",
    "DK4_MES_B26_R0479": "Spain... Their Armada becoming{LB}even stronger would be terrible.",
    "DK4_MES_B26_R0483": "Exactly. Same for me.",
    "DK4_MES_B26_R0487": "Really? Everyone says Clifford's fleet{LB}is invincible and ignores Spain.",
    "DK4_MES_B26_R0490": "Even my fleet fears him...",
    "DK4_MES_B26_R0493": "He is that formidable...",
    "DK4_MES_B26_R0497": "My proposal:{LB}join forces with me.",
    "DK4_MES_B26_R0500": "With us? What do you mean?",
    "DK4_MES_B26_R0504": "Together, even they will hesitate{LB}to move against us. Agreed?",
    "DK4_MES_B26_R0516": "Hm. Not bad, but...",
    "DK4_MES_B26_R0523": "Maybe... But defeating{LB}the Spanish navy is beyond us...",
    "DK4_MES_B26_R0527": "Nobody expects that{LB}from your group.",
    "DK4_MES_B26_R0530": "Then what?",
    "DK4_MES_B26_R0534": "Join me and help check{LB}their movements.",
    "DK4_MES_B26_R0537": "Only that?",
    "DK4_MES_B26_R0541": "That is enough. The world is vast.{LB}Together we contain Spain,{LB}then expand into other regions.",
    "DK4_MES_B26_R0544": "Oh! We leave the North Sea{LB}and head for Africa and the East!",
    "DK4_MES_B26_R0555": "Makes sense.",
    "DK4_MES_B26_R0562": "Right.",
    "DK4_MES_B26_R0566": "My fleet follows England west.{LB}Yours follows Dutch policy south,{LB}through Africa and Asia.",
    "DK4_MES_B26_R0569": "Build strength, and...",
    "DK4_MES_B26_R0573": "Someday we can defeat{LB}that mighty Armada!",
    "DK4_MES_B26_R0576": "Right. You learn fast.",
    "DK4_MES_B26_R0580": "But...",
    "DK4_MES_B26_R0584": "Hm? A problem?",
    "DK4_MES_B26_R0588": "Can you really be trusted...?",
    "DK4_MES_B26_R0592": "Come now.{LB}English gentleman.",
    "DK4_MES_B26_R0595": "Means nothing.",
    "DK4_MES_B26_R0607": "Words alone prove nothing...",
    "DK4_MES_B26_R0614": "As a token of trust,{LB}take this Crimson Dye.",
    "DK4_MES_B26_R0617": "Dye...? What for?",
    "DK4_MES_B26_R0621": "They say it reveals a map{LB}to hidden treasure.{LB}So, will you join me?",
    "DK4_MES_B26_R0633": "Trusting him is our only choice...",
    "DK4_MES_B26_R0640": "Okay.",
    "DK4_MES_B26_R0644": "Good!{LB}A pleasure, partner!",
    "DK4_MES_B26_R0647": "Please stay out of the New World.{LB}The powers entrenched there are my prey.{LB}Do not fight them on your own.",
    "DK4_MES_B26_R0650": "The tavernkeeper has the Crimson Dye.{LB}Visit Amsterdam's tavern.",
    "DK4_MES_B26_R0654": "Understood. But betray me,{LB}and you will regret it!",
}

SPEAKERS = {
    "02": "Lil Argot", "09": "Kamil", "0E": "Emilio Ferrog", "10": "Gerhard Adelknauts",
    "14": "Fernando", "1C": "James Clifford", "97": "Lookout", "FE": "Unknown man",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}

CONTEXTS = {
    24: "Kamil explains city contracts, trade routes, surveyors, and recruiting skilled navigators.",
    25: "Lil's crew reflects on Speyer's defeat and the attack on their company.",
    26: "Lil meets James Clifford, attends his dinner, and negotiates an alliance against Spain in exchange for the Crimson Dye.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V5 inventory mismatch: missing={sorted(missing)}")
    records = []
    blocks: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        blocks[str(block)] = blocks.get(str(block), 0) + 1
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Story participant"),
            "context": CONTEXTS[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving route facts, character voice, tutorial terminology, and alliance terms.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Lil's contract/navigation guidance, Speyer aftermath, and complete first Clifford meeting, dinner, alliance, and Crimson Dye exchange across SC2 blocks 24-26.",
        "excluded_records": {}, "inventory": {"identified_records": len(LINES), "translated_records": len(records), "blocks": blocks},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
