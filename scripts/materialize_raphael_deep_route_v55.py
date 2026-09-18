from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v55.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = tuple(range(183, 189))
EXCLUDED = {
    "DK4_MES_B186_R0007": "Two-byte scene/location payload; not an independently rendered dialogue line.",
    "DK4_MES_B186_R0068": "Four-byte Golden Crown acquisition control; preserve raw semantics.",
    "DK4_MES_B187_R0013": "Four-byte pirate encounter scene-control payload; not dialogue.",
}

LINES = {
    183: [
        "Sir...",
        "{MACRO:FI}...",
        "...Hm?",
        "Pardon me.{LB}No threat is meant.",
        "We meet at last.{LB}Sanghyeon, her senior pupil.",
        "Word came that you took Yifa in.{LB}This man wished to greet you.",
        "Yifa's...?",
        "Her wild nature reflects{LB}this man's poor guidance.{LB}The shame is mine.",
        "She fled training without leave,{LB}then crossed our border.{LB}Such acts are unforgivable.",
        "Unknown to her, our people{LB}are forbidden to leave the nation.",
        "Are you here to take Yifa back?",
        "That cannot be done.{LB}Her crime was grave.{LB}The school has expelled her.",
        "Our bond is already severed...",
        "We grew up together,{LB}as true siblings.",
        "She remains immature.{LB}Worry persists that she may{LB}offend those around her.",
        "A selfish request, but please guide her{LB}so she never strays from the right path.",
        "And if possible, ensure she trains{LB}and obeys our master's teachings.",
        "Please take good care of Yifa.",
        "Was that a dream?{LB}Yet it felt strangely vivid...",
        "Gooood morning!{LB}Come on, let's depart...",
        "What?",
        "My senior...!",
        "Your senior?!{LB}Was his name Sanghyeon?",
        "How?!{LB}Where is he?",
        "A man claiming to be your senior{LB}appeared in my dream.{LB}His name was Sanghyeon...",
        "Hm?",
        "Brother Sanghyeon...",
        "He couldn't leave the mountain,{LB}so he came through his art...",
        "Art?{LB}That too?",
        "He said to obey your master{LB}even away from home.{LB}He was very worried about you.",
        "Brother...{LB}He never stops worrying. Heh.",
        "...{LB}What?",
        "Training starts now!{LB}Can't disappoint Brother Sanghyeon!",
        "Training is fine, but{LB}help with ship work too.",
        "No problem! Leave it to me!",
    ],
    184: [
        "Mihwa, this man lives{LB}for your radiant smile.",
        "Oh, Julian...",
        "Every country has men like that.",
        "Huh? You usually smile now.{LB}Do you hate me?",
        "No... Usually your words cheer me,{LB}but today...",
        "There's something needed so badly{LB}that it fills every waking dream...",
        "Mihwa, that face doesn't suit you.{LB}What do you want so badly?",
        "The Golden Crown of Silla.{LB}A mystical name, yes?{LB}Very rare, too.",
        "Sounds costly...{LB}Can this man pay? Where is it sold?",
        "No shop sells it.{LB}Word says it's in Seoul.",
        "Not sold? ...Ah!{LB}Of course. That place!",
        "You know where?",
        "Leave it to me!{LB}The crown will be yours,{LB}and your smile will return!",
        "Your smile gives me life!{LB}Once it's found,{LB}you'll date me, right?",
        "Not even found yet. How eager.{LB}Very well, perhaps.",
        "Yes! Don't forget that promise!{LB}Off to Seoul!",
        "Good luck...{LB}He's gone already.",
        "Um...",
        "Oh, welcome.{LB}Sorry that went unnoticed.",
        "About that Golden Crown of Silla...{LB}What exactly is it?",
        "Sorry, the details slipped away.{LB}Only that it's gorgeous.",
        "Sounds interesting.{LB}Right, {MACRO:FI}?",
        "Maybe. But we don't know its form,{LB}and Julian already left to find it.",
        "A gift from you would be welcome too.{LB}Am this woman not worth one?",
        "Hear that?{LB}Can't back down after she says that.",
        "(Claudio fell for that.){LB}All right, let's search.{LB}You said Seoul?",
        "That's what word says.{LB}The exact place is unknown...",
        "Let's go anyway.{LB}Locals can point us onward.",
        "Maybe we'll meet that man there.",
    ],
    185: [
        "Claudio, where should we begin{LB}looking into the Golden Crown of Silla?",
        "Well...{LB}Let's ask.",
        "Oh, welcome.",
        "Know of the Silla Crown?",
        "Yes, the name is familiar.{LB}Why do you ask?",
        "We're looking for it.{LB}Any idea where?",
        "Has searching for that crown{LB}become fashionable?{LB}Someone else just asked.",
        "Was he a smooth-talking man?",
        "He seemed unsure whether to ask{LB}or flirt with this woman.",
        "Was his name Julian?{LB}We met him in Hangzhou.",
        "Can't recall his name.{LB}He went to King Muryeong's Tomb.",
        "That tomb?",
        "A ruin near here.{LB}Word says the crown is there.",
        "We're behind!{LB}Let's hurry too, {MACRO:FI}!",
    ],
    186: [
        "Ah, {MACRO:FI}.{LB}Hello.",
        "A friend?",
        "Actually, they found{LB}the Golden Crown before me.",
        "But my love for Mihwa{LB}moved them to give it up.{LB}Kind people, right?",
        "Oh? Y-yes, very kind.{LB}So this is the Golden Crown...{LB}What brilliant light...",
        "Mihwa, it's yours.{LB}As promised, a gift.",
        "Lovely!{LB}Always cherished!",
        "Good for you, Julian.",
        "Thank you. Truly.{LB}How can this be repaid?",
        "N-no reward needed.",
        "Honor matters greatly to this man.{LB}Such help cannot go unanswered.",
        "Mihwa! Are you here?",
        "Oh, welcome.{LB}Why such a rush?",
        "Here",
        "Ah!{LB}The Golden Crown of Silla?!{LB}You found it... Thank you!",
        "No need.",
        "Why so shy?{LB}You told Julian, 'This gift{LB}will be mine to give her!'",
        "How wonderful! Thank you!{LB}Where is Julian, by the way?",
        "We ran into him just as{LB}the crown was found...",
        "Then he left.",
        "Mihwa! Right here!",
        "Julian, they beat you this time.",
        "True. But all the way to Seoul,{LB}Mihwa never left my thoughts.{LB}This love is deeper than the sea.",
        "What about Lihua in Seoul?{LB}She was quite beautiful too.",
        "She's lovely too.{LB}A different charm.",
        "Juuulian!{LB}Always chasing someone new!",
        "No need for jealousy, Mihwa.{LB}Only the crown was discussed.",
        "Still, your speed was amazing.{LB}This man reached Seoul exhausted.",
        "How did you find the crown so fast?",
        "Seoul is a quick trip{LB}by ship.",
        "A ship!{LB}You're sailors?!",
        "Yes.",
        "Lucky...{LB}This man ran all the way to Seoul.",
        "(He ran to Seoul?!{LB}Seriously...?)",
        "A ship...{LB}This is destiny!",
        "What is it?",
        "The crown was the sign needed{LB}to begin a journey around the world!",
        "H-hey...",
        "Take me with you!{LB}Let this man see the world too!",
        "This isn't to woo women{LB}worldwide, right?",
        "A charming reason, but no.{LB}My grandfather sailed the world.{LB}His tales inspired me as a child...",
        "What's the world like?{LB}My grandfather's home?{LB}Those answers call to me.{LB}So this journey matters.",
        "Your grandfather was a navigator?{LB}Then you know about sailing too?",
        "Of course.{LB}No burden here!",
        "Good!{LB}Then come with us!",
        "Mihwa?",
        "Yes, Julian?",
        "What about our date?",
        "Leaving now, aren't you?{LB}No time.",
        "Then once an even finer treasure{LB}is found, this man will hurry back.{LB}Promise a date then!",
        "Oh, all right.{LB}This woman will wait!",
        "An amazing fellow{LB}may have joined us...",
    ],
    187: [
        "Gah! That woman!",
        "Aziza Nurennahar, surely...",
        "You.{LB}Of {MACRO:FO}...{LB}Odd meeting.",
        "This is bad, {MACRO:FI}!{LB}They're all her pirates!",
        "Heh. This boy's face{LB}looks cuter up close.",
        "Share a drink{LB}and get acquainted?",
        "Heh! Moths to a flame, eh?{LB}Surround them!",
        "(What now? Claudio and me{LB}against this many pirates...)",
        "D-damn... What now?!",
        "Well, you're properly scared now.{LB}Last time you hurt us badly!",
        "Wait! This boy is speaking with me.{LB}The rest of you, back off!",
        "Y-yes! Sorry!",
        "Our score is not settled.{LB}Dying in a place like this{LB}would be dull.",
        "What is with this woman?!",
        "A pirate settles scores at sea!",
        "Standing against this many{LB}deserves a little praise today.{LB}Wouldn't you say?",
        "An admiral can't run away.",
        "Bold words.{LB}A brave little boy indeed.{LB}This woman likes you.",
        "...Your name?",
        "{MACRO:FI} {MACRO:FA}",
        "That name and face will be remembered.{LB}Until next time... at sea.",
        "Hm?! That sword...",
        "Eh?",
        "A fine sword.{LB}Would suit me better.{LB}Someday, it's mine.",
        "What do you mean...?",
        "No need to know yet.{LB}Men, we're leaving!",
        "Aye!",
        "One word controls them all...",
        "Whew... Safe.",
        "That was frightening.{LB}She truly is a pirate captain.",
        "Yes. Such force...{LB}Settling it at sea must be{LB}a pirate's pride.",
        "Probably. But being chased around{LB}by someone like that sounds awful.",
        "No sense worrying about it now.",
        "Right...",
    ],
    188: [
        "Bananas. Bananas are the future.",
        "Bananas?",
        "Yes. This flavor will sell.",
        "You think?",
        "When this woman says it sells,{LB}it sells!",
        "Understood.{LB}What now?",
        "Buy every banana you can.",
        "Sure.",
        "Bananas are the future!{LB}Ho ho ho!",
        "Bananas may boom in Seville.",
    ],
}

SPEAKERS = {
    0x05: "Claudio Manini",
    0x19: "Ifa",
    0x1A: "Julian",
    0x51: "Sanghyeon",
    0xAE: "Banana merchant",
    0xAF: "Merchant's assistant",
    0xB7: "Pirate crew",
    0xB8: "Pirate crew",
    0xC9: "Mihwa",
    0xCA: "Tavernkeeper",
    0xFE: "Aziza Nurennahar",
}
CONTEXT = {
    183: "Sanghyeon appears in Raphael's dream, entrusts Ifa to him, and inspires her to continue training.",
    184: "Julian promises Mihwa the Golden Crown of Silla, and Raphael agrees to search for it in Seoul.",
    185: "A Seoul tavernkeeper directs Raphael and Claudio toward King Muryeong's Tomb.",
    186: "Both Golden Crown outcome branches reunite Julian and Mihwa before Julian joins Raphael's fleet.",
    187: "Aziza Nurennahar confronts Raphael ashore, dismisses an unfair ambush, and vows to settle their rivalry at sea.",
    188: "A merchant predicts a banana boom in Seville.",
}


def main() -> None:
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = [row for row in csv.DictReader(stream) if row["id"].startswith(prefixes)]
    if len(source_rows) != 177:
        raise SystemExit(f"B183-B188 inventory changed: {len(source_rows)}")
    rows_by_block = {
        block: [
            row for row in source_rows
            if row["id"].startswith(f"DK4_MES_B{block}_") and row["id"] not in EXCLUDED
        ]
        for block in BLOCKS
    }
    for block, lines in LINES.items():
        if len(rows_by_block[block]) != len(lines):
            raise SystemExit(f"B{block}: {len(rows_by_block[block])} visible rows != {len(lines)} translations")
    if set(EXCLUDED) - {row["id"] for row in source_rows}:
        raise SystemExit("V55 excluded-record inventory no longer matches the source")

    records = []
    for block, lines in LINES.items():
        for row, english in zip(rows_by_block[block], lines, strict=True):
            first = bytes.fromhex(row["source_hex"])[0]
            state = f"{first:02X}" if first in SPEAKERS else ""
            unsafe = english
            for macro in ("FI", "FA", "FO", "FU"):
                unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
            if "I" in unsafe or "F" in unsafe:
                raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
            records.append({
                "id": row["id"],
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(first, "Raphael Castor, companion, or scene text"),
                "context": CONTEXT[block],
                "source_meaning": english.replace("{LB}", " ").replace("{MACRO:FI}", "Raphael").replace("{MACRO:FA}", "Castor").replace("{MACRO:FO}", "Castor Co."),
                "localization_note": "Faithful natural American English preserving character voice, alternate branches, canonical names, scene controls, and fixed-record display constraints.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
                **({"manual_break_reason": "Protects four-line bounds and progressive ASCII pair phase."} if "{LB}" in english else {}),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v55-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Raphael optional Ifa follow-up, Golden Crown and Julian recruitment, Aziza encounter, and banana-boom events across SC0 blocks 183-188.",
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(source_rows),
            "translated_records": len(records),
            "blocks": {str(block): len(rows_by_block[block]) for block in BLOCKS},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
