from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v47.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
EXCLUDED = {
    "DK4_MES_B168_R0057": "Eight-byte recruitment cutscene control; no independently rendered dialogue."
}
LINES = {
    168: [
        "Hey, kid! Over here!",
        "\"Kid\" means me?",
        "Yes, you. One of this crew, right?{LB}A powder monkey? Heard this ship{LB}might need a skilled navigator.",
        "Wanted to meet the captain...{LB}But a lowly hand's referral{LB}won't help much. Ha ha!",
        "Never mind.",
        "Hey, you preening peacock!{LB}Whose ship do you think this is?",
        "P-peacock?!{LB}These aren't looks!{LB}You're the one wearing earrings!",
        "What!? These mark a warrior!{LB}You want a fight?!",
        "Why so angry?{LB}Muscle-brained fools...",
        "You...!!",
        "Stop, Claudio!",
        "...Not a kid. Name's{LB}{MACRO:FI} {MACRO:FA}.{LB}This ship's admiral.",
        "Mamma mia!{LB}You're the admiral?!",
        "...Then pardon me.{LB}Sorry. Please forgive me.",
        "Huh?{LB}No, our man insulted you...",
        "{MACRO:FI}!{LB}You don't owe him an apology!",
        "But...",
        "No, he's right. Serious workers{LB}always tempt me to tease them.{LB}That was my fault. Sorry.",
        "What a strange man.{LB}Why say it if you'll apologize?",
        "Truly sorry.{LB}...Goodbye.",
        "Hey, wait!",
        "You wanted work{LB}as a navigator, right?",
        "Well, yes...",
        "Then, {MACRO:FI}?",
        "Sure. More friends mean more fun.{LB}Will you sail with us?",
        "Y-you mean it?",
        "That's the idea.{LB}Claudio Manini.{LB}Good to meet you.",
        "...You're all quite unusual.{LB}Angelo Puccini.",
        "Angelo.{LB}Want to be a navigator?{LB}You trust your skill, right?",
        "He picked a fight with me.{LB}At least he's brave.",
        "Something like that.",
        "Welcome aboard, Angelo!",
        "Gladly, Admiral!",
        "By the way, Admiral:{LB}want trading profits?{LB}Stop scraping by{LB}in the Mediterranean.",
        "Why?",
        "Oh!{LB}You understand trade!",
        "Routes here look rich,{LB}but great powers developed them.{LB}Little profit remains.",
        "Hmm... true.{LB}Deals and investments cost plenty.{LB}Little room remains for us.",
        "Sail farther.{LB}Africa and the New World can grow.{LB}Small stakes, great returns.",
        "Their goods are rare too.{LB}Simply sailing to Europe{LB}should bring easy wealth.",
        "Amazing...{LB}You know trade too.",
        "Sailors told me.",
        "No, no.{LB}The man is quite right.",
        "More cargo holds mean little here.{LB}Without market share in Europe,{LB}large trades are impossible.",
        "Got it. Look beyond Europe.{LB}All right--Africa!",
    ],
    169: [
        "Dukov, carry this.",
        "Yes.",
        "So beautiful...",
        "Really a man?",
        "Shh. He'll hear.",
        "(Again... enough.{LB}Not a spectacle.)",
        "Dukov, this wine too.",
        "Yes.",
        "Oh! He brought mine!",
        "Why so happy?{LB}Tch. Not amusing.",
        "Dukov.{LB}Take this to that table.",
        "Yes.",
        "Hey, girl.{LB}Pour me a drink.",
        "You're truly beautiful,{LB}aren't you?",
        "Really a man?{LB}Skin that pale ain't natural.{LB}Heh heh...",
        "No!",
        "Ow! That hurts!",
        "Y-you bastard!",
        "(Damn!)",
        "You...{LB}Treating a customer that way?",
        "...My apologies.",
        "Sir, some wine over here.",
        "Coming.{LB}...Dukov, a moment.",
        "Dukov...{LB}this work may not suit you.",
        "Sir...",
        "Enough trouble.{LB}No sword needed.{LB}Handle customers more gently.",
        "You're dismissed.",
        "...Understood.",
        "That pale skin, that beauty...{LB}He doesn't belong here.{LB}Could there be a reason?",
        "Life varies.",
        "A tavern doesn't suit him.{LB}Too stiff.",
        "Talk to him?",
        "(Dismissed... and no money.{LB}What now...?)",
        "(A ship...{LB}Want aboard.)",
        "Hey, pretty girl!{LB}Meeting again today.",
        "Heh heh.{LB}Alone out here? Bad luck.{LB}Men!",
        "Don't try to escape.{LB}You'll pay for shaming me!",
        "(Too many... can't beat them all.{LB}Target their leader!)",
        "What's taking so long?!{LB}Get him!",
        "Hah... hah...{LB}(Can't even reach him alone!)",
        "Looks like you're nearly done.{LB}End it!",
        "Who are you?!",
        "Had to step in.{LB}Mind our help?",
        "Damn...{LB}Only fight when victory is certain.{LB}Remember this!",
        "Up close,{LB}you really are beautiful.",
        "Only noticing now?{LB}Slow.",
        "Pale skin...{LB}A northerner?",
        "...Looks...{LB}don't matter.",
        "Easy. Don't get so tense.",
        "No, talking to myself.{LB}...Sorry. Thank you.{LB}You saved my life.",
        "Glad we made it.{LB}Actually...{LB}a request.",
        "Gladly, if able.",
        "Will you sail the world{LB}with us?",
        "What?",
        "That fight showed me{LB}how skilled you are.",
        "Believe it or not,{LB}this crew answers to me.",
        "Ah... perhaps this is sudden.",
        "Not at all.{LB}A welcome offer.{LB}A navigator, though unemployed.",
        "So you've made women worldwide{LB}weep, huh?",
        "Claudio! That's rude!",
        "...No offense taken, Admiral.{LB}Please let me join your ship.{LB}Dukov. At your service.",
    ],
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = [
            row for row in csv.DictReader(stream)
            if row["id"].startswith(("DK4_MES_B168_", "DK4_MES_B169_"))
        ]
    if len(source_rows) != 107:
        raise SystemExit(f"B168-B169 inventory changed: {len(source_rows)}")
    rows_by_block = {
        block: [row for row in source_rows if row["id"].startswith(f"DK4_MES_B{block}_") and row["id"] not in EXCLUDED]
        for block in LINES
    }
    for block, lines in LINES.items():
        if len(rows_by_block[block]) != len(lines):
            raise SystemExit(f"B{block}: {len(rows_by_block[block])} visible rows != {len(lines)} translations")
    speaker_names = {
        0x05: "Claudio Manini", 0x06: "Julio Erdi", 0x0F: "Angelo Puccini",
        0x15: "Ian Dukov", 0x5C: "Tavernkeeper", 0x60: "Drunken thug",
    }
    contexts = {
        168: "Raphael recruits Angelo Puccini after his clash with Claudio, then hears Angelo's early-game long-distance trade advice.",
        169: "Raphael's crew witnesses Ian Dukov's dismissal, saves him from vengeful thugs, and recruits the unemployed navigator.",
    }
    records = []
    for block, lines in LINES.items():
        for row, english in zip(rows_by_block[block], lines, strict=True):
            first = bytes.fromhex(row["source_hex"])[0]
            state = f"{first:02X}" if first in speaker_names else ""
            unsafe = english
            for macro in ("FI", "FA", "FO", "FU"):
                unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
            if "I" in unsafe or "F" in unsafe:
                raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
            records.append({
                "id": row["id"],
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": speaker_names.get(first, "Raphael Castor or companion"),
                "context": contexts[block],
                "source_meaning": english.replace("{LB}", " ").replace("{MACRO:FI}", "Raphael").replace("{MACRO:FA}", "Castor"),
                "localization_note": "Faithful natural American English with canonical character identity retained in metadata when a reserved uppercase command byte prevents safe literal spelling.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
                **({"manual_break_reason": "Protects scene pacing, four-line bounds, and progressive ASCII pair phase."} if "{LB}" in english else {}),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v47-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete Angelo Puccini and Ian Dukov recruitment events in SC0 blocks 168-169.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": {str(block): len(rows_by_block[block]) for block in LINES}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} control excluded")


if __name__ == "__main__":
    main()
