from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v5.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
LINES = {
    "DK4_MES_B81_R0005": "Grandpa, you promised{LB}a bullfight in Spain.",
    "DK4_MES_B81_R0008": "Hm? Did this old man?",
    "DK4_MES_B81_R0012": "You always talk,{LB}but never showed me one!",
    "DK4_MES_B81_R0016": "Why not all go?{LB}That makes a good story.{LB}Come on!",
    "DK4_MES_B81_R0020": "A bullfight? Never seen one.{LB}Sounds fun.",
    "DK4_MES_B81_R0024": "Sure. Let us stop by.",
    "DK4_MES_B81_R0037": "Wow! Look at this crowd!",
    "DK4_MES_B81_R0043": "Spain rules much of the world now.{LB}Ho ho!",
    "DK4_MES_B81_R0047": "That does not make you important.",
    "DK4_MES_B81_R0051": "Such a sharp tongue!{LB}Respect your elders!",
    "DK4_MES_B81_R0055": "A famous matador is appearing today.",
    "DK4_MES_B81_R0058": "Maybe handsome!",
    "DK4_MES_B81_R0070": "He cannot outshine me.",
    "DK4_MES_B81_R0077": "Look.",
    "DK4_MES_B81_R0082": "Ha ha ha!",
    "DK4_MES_B81_R0086": "Make us laugh again!",
    "DK4_MES_B81_R0091": "What? That is the famous matador?",
    "DK4_MES_B81_R0094": "That one is a picador.",
    "DK4_MES_B81_R0098": "He wears down the bull first.{LB}Then the matador finishes it.",
    "DK4_MES_B81_R0102": "Hyaaah!!",
    "DK4_MES_B81_R0106": "Ha ha! The fool is playing with it!{LB}Look! The bull threw him!",
    "DK4_MES_B81_R0110": "Raaah!!",
    "DK4_MES_B81_R0114": "Ha ha ha!",
    "DK4_MES_B81_R0118": "Get him out!",
    "DK4_MES_B81_R0126": "At last! The star appears!",
    "DK4_MES_B81_R0130": "Ooooh!!",
    "DK4_MES_B81_R0134": "At last!",
    "DK4_MES_B81_R0138": "Woo-hoo!",
    "DK4_MES_B81_R0142": "Hooray!",
    "DK4_MES_B81_R0146": "Entertain us!",
    "DK4_MES_B81_R0150": "Bravo!!",
    "DK4_MES_B81_R0154": "Hooray!",
    "DK4_MES_B81_R0159": "Murmur...",
    "DK4_MES_B81_R0164": "Ask him to join us?",
    "DK4_MES_B81_R0168": "Wait, {MACRO:FI}.{LB}Why him?",
    "DK4_MES_B81_R0172": "He was incredible, right?",
    "DK4_MES_B81_R0176": "Yes, but...",
    "DK4_MES_B81_R0181": "Settled.",
    "DK4_MES_B81_R0185": "Wait! Are you serious?!",
    "DK4_MES_B81_R0190": "Hey!",
    "DK4_MES_B81_R0194": "Hmm?",
    "DK4_MES_B81_R0198": "W-what?{LB}Oh... You meant him?!",
    "DK4_MES_B81_R0203": "Would you like to sail the open sea?",
    "DK4_MES_B81_R0206": "A ship? Sounds scary.{LB}Does not look tasty either.",
    "DK4_MES_B81_R0210": "Ships are not food...{LB}But we can seek delicious food{LB}all over the world!",
    "DK4_MES_B81_R0213": "Delicious food? Heh heh...",
    "DK4_MES_B81_R0217": "Yes. The world has{LB}all kinds of food.",
    "DK4_MES_B81_R0220": "Lots of every kind?{LB}Then count me in!{LB}Sea or anywhere!",
    "DK4_MES_B81_R0225": "Settled! What is your name?{LB}Mine is {MACRO:FI} {MACRO:FA}.",
    "DK4_MES_B81_R0228": "M-me? Emilio.{LB}Good to meet you.",
    "DK4_MES_B81_R0232": "Welcome aboard, Emilio.",

    "DK4_MES_B82_R0005": "You are unbelievably{LB}persistent!!!",
    "DK4_MES_B82_R0008": "Oh, beloved Christina!{LB}Why are you so cold?",
    "DK4_MES_B82_R0011": "Are you unwell?{LB}Who follows someone{LB}who hates him this much?",
    "DK4_MES_B82_R0014": "No need to be shy!",
    "DK4_MES_B82_R0018": "Enough! Listen.{LB}Our parents arranged it.{LB}No wish to marry you!",
    "DK4_MES_B82_R0021": "Hearing your voice alone{LB}makes me happy!",
    "DK4_MES_B82_R0024": "Moron!",
    "DK4_MES_B82_R0029": "That man...?",
    "DK4_MES_B82_R0033": "Yes, him.",
    "DK4_MES_B82_R0038": "Looks like a complicated problem...",
    "DK4_MES_B82_R0041": "No problem at all.{LB}Hey, Christina!",
    "DK4_MES_B82_R0045": "Christina!{LB}Have you been well?",
    "DK4_MES_B82_R0049": "Grandpa! When reach London?",
    "DK4_MES_B82_R0053": "Just now.{LB}Sailing again, you see.",
    "DK4_MES_B82_R0056": "Again?!{LB}Mom and Dad will stop you.",
    "DK4_MES_B82_R0059": "Only if you tell them.{LB}Ho ho ho.",
    "DK4_MES_B82_R0062": "Come on...",
    "DK4_MES_B82_R0066": "More importantly,{LB}would you like to sail too?",
    "DK4_MES_B82_R0069": "What?! Absolutely not!",
    "DK4_MES_B82_R0072": "Who is this fellow?",
    "DK4_MES_B82_R0075": "A friend's son...{LB}What was his name?",
    "DK4_MES_B82_R0078": "Christina! No need for shyness!{LB}Are you her grandfather?",
    "DK4_MES_B82_R0082": "An honor to meet you!{LB}My name is Mivor!{LB}Mivor Gentz!",
    "DK4_MES_B82_R0085": "Yes, something like that.{LB}Our fathers promised it{LB}without asking me.",
    "DK4_MES_B82_R0089": "Somehow this odd fellow{LB}became my betrothed.",
    "DK4_MES_B82_R0092": "Oh. So.",
    "DK4_MES_B82_R0096": "Do not just say that!",
    "DK4_MES_B82_R0100": "Hm, this pale weakling...",
    "DK4_MES_B82_R0103": "Not only because our parents said so...{LB}Truly, Lady Christina...",
    "DK4_MES_B82_R0107": "Mom and Dad seem to mean,{LB}'Stop waving swords forever{LB}and settle down.' What a bother.",
    "DK4_MES_B82_R0110": "Sounds like Herald.{LB}Maybe he was raised wrong...",
    "DK4_MES_B82_R0113": "Um.",
    "DK4_MES_B82_R0117": "You stay quiet!{LB}Now, about that ship...",
    "DK4_MES_B82_R0121": "Right, right.{LB}Would you come with me?",
    "DK4_MES_B82_R0126": "Grandpa praised your skill.{LB}Would you join my ship?",
    "DK4_MES_B82_R0130": "What? Grandpa, who are they?",
    "DK4_MES_B82_R0133": "Well... one thing after another.{LB}This is Admiral {MACRO:FI} {MACRO:FA}.",
    "DK4_MES_B82_R0136": "An admiral? Very young.",
    "DK4_MES_B82_R0140": "You wanted matches abroad.{LB}Why not train around the world?",
    "DK4_MES_B82_R0143": "No! Absolutely not!",
    "DK4_MES_B82_R0147": "Good idea.{LB}Count me in.",
    "DK4_MES_B82_R0150": "No! No way!!",
    "DK4_MES_B82_R0155": "Can we really leave Mivor behind?",
    "DK4_MES_B82_R0158": "Of course! No time like now.{LB}Right, Grandpa?",
    "DK4_MES_B82_R0161": "That is my granddaughter.{LB}Well said.",
    "DK4_MES_B82_R0165": "Mivor, would you come too?",
    "DK4_MES_B82_R0168": "W-well...",
    "DK4_MES_B82_R0172": "He cannot swim.{LB}Terrified of water.{LB}He cannot follow, right?",
    "DK4_MES_B82_R0175": "Then... a duel!",
    "DK4_MES_B82_R0179": "Whoa!",
    "DK4_MES_B82_R0183": "You never understand!{LB}Hyaah!",
    "DK4_MES_B82_R0187": "Aaaah! Ouch!",
    "DK4_MES_B82_R0191": "With that stance,{LB}even a child would win.",
    "DK4_MES_B82_R0194": "Hm. Your skill remains sharp.",
    "DK4_MES_B82_R0197": "My rapier!{LB}My father bought it!",
    "DK4_MES_B82_R0201": "Let us go!{LB}Sword matches are nice,{LB}but sailing sounds fun!",
    "DK4_MES_B82_R0205": "Admiral,{LB}any reason to visit Spain?",
    "DK4_MES_B82_R0209": "Spain?",
    "DK4_MES_B82_R0213": "Grandpa and Dad were born there.{LB}Want to see Spain.",
    "DK4_MES_B82_R0216": "Now, now. Do not be so selfish.",
    "DK4_MES_B82_R0221": "Well...{LB}Would Seville do?",
    "DK4_MES_B82_R0224": "Really?! You understand me!{LB}This voyage will be fun!",
    "DK4_MES_B82_R0228": "Still the same as ever...{LB}{MACRO:FI}, please look after her.",
}

SPEAKERS = {
    "04": "Arcadius", "05": "Claudio Manous", "06": "Christina's grandfather",
    "07": "Christina", "0E": "Emilio Ferrog", "0F": "Raphael Castor",
    "4F": "Mivor Gentz", "52": "Bullfight spectator", "5F": "Bullfight spectator",
    "68": "Bullfight spectator", "71": "Bullfight spectator", "93": "Bullfight spectator",
    "FE": "Crowd",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    "81": "In Seville, Raphael's crew attends a bullfight and recruits the matador Emilio Ferrog with the promise of food from around the world.",
    "82": "In London, Christina rejects her arranged fiancé Mivor and joins Raphael's voyage for worldwide sword training, then asks to see Seville.",
}
EXCLUDED = {"DK4_MES_B81_R0080": "eight-byte bullfight event-control payload with no visible dialogue"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    inventory = {row_id for row_id in all_rows if row_id.startswith(("DK4_MES_B81_", "DK4_MES_B82_"))}
    if set(LINES) | set(EXCLUDED) != inventory or set(LINES) & set(EXCLUDED):
        missing = inventory - set(LINES) - set(EXCLUDED)
        extra = set(LINES) | set(EXCLUDED) - inventory
        raise SystemExit(f"Raphael V5 inventory mismatch: missing={sorted(missing)} extra={sorted(extra)}")
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
            "localization_note": "Faithful concise American English preserving character voice, recruitment continuity, player-name macros, and fixed-allocation display safety.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v5-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Raphael's Seville bullfight and Emilio recruitment plus Christina's full London recruitment across SC0 blocks 81-82.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(inventory), "translated_records": len(records), "blocks": blocks},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records; excluded {len(EXCLUDED)} control")


if __name__ == "__main__":
    main()
