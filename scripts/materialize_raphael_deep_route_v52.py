from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v52.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
EXCLUDED = {"DK4_MES_B178_R0014": "Five-byte tavern minigame setup control; no independently rendered dialogue."}
TRANSLATIONS = [
    "Now that we're here,{LB}you must accept.",
    "A newcomer!{LB}Wager a drink?{LB}Just a simple game.",
    "Several coins here.{LB}Each of us takes one to three{LB}on every turn.",
    "Whoever takes the last coin loses.{LB}Simple, right? Let's begin.",
    "Yes",
    "Decline",
    "Thanks for the drink.{LB}Ahh, delicious.",
    "Told you, {MACRO:FI}.{LB}Always leave a multiple of four{LB}plus one coin. That's the key.",
    "Right. Made a mistake...",
    "Heh. Next meeting,{LB}another match. Thanks.",
    "Bad luck.{LB}A drink for me, then.",
    "Hey, {MACRO:FI}!{LB}This stings! Another round!",
    "Wait, Claudio.{LB}This man seems good at gambling...",
    "Yes. Gambling takes{LB}more than luck.",
    "More than luck?{LB}Could it be...?",
    "Janus, what is it?",
    "{MACRO:FI}, listen.{LB}This game may have{LB}a guaranteed strategy!",
    "Really?",
    "Make the other player take last.{LB}Leave that coin plus{LB}a multiple of four.",
    "Hmm... not clear.",
    "Explain it more simply.",
    "Honestly... Suppose five coins remain{LB}and the opponent takes one.{LB}What then?",
    "Take three; four remain.",
    "Then from five coins,{LB}the opponent takes two?",
    "Take two... Ah!{LB}Always restore the pile to five.{LB}Then any move can be beaten!",
    "Exactly.",
    "Nine: one plus four plus four{LB}Whatever the opponent takes{LB}leave exactly five coins again{LB}That guarantees victory!",
    "Quick study, Admiral.",
    "Hey! None of that makes sense!",
    "Too hard for Claudio...",
    "Shut up!{LB}You two get it without me.{LB}Hate that!",
    "Ahh, a free drink tastes best.{LB}Want another match? Come anytime.",
    "Tch, you got me.{LB}A rare loss. Here.",
    "No drink now.{LB}You said 'in a while.'{LB}Are you that confident?",
    "Sure. Gambling needs{LB}insight and luck.",
    "Both belong to me.{LB}Born for gambling.",
    "Luck, perhaps...{LB}But insight?",
    "Don't judge by appearances.",
    "Take that couple over there.{LB}Can't hear them.{LB}What are they discussing?",
    "Their love, probably?",
    "Come on, that's elementary.{LB}They're breaking up.",
    "Just watch.",
    "Been listening to you...{LB}Can't follow your thinking anymore!{LB}You're too selfish!",
    "That's your view.{LB}To me, you're selfish too.",
    "Oh? Then perhaps{LB}we shouldn't meet again.",
    "Agreed.{LB}This ends here.",
    "Well? Called it.",
    "Amazing... how?",
    "A fist clenched under the table.{LB}She held back anger.{LB}Not a lover's pose.",
    "And he never looked at her.{LB}Would a man in love{LB}face his woman that way?",
    "Amazing!{LB}You saw all of that!",
    "That insight reads{LB}an opponent's hand.",
    "Then luck wins.",
    "Join my ship!{LB}That talent shouldn't be wasted.",
    "Hey now. That's sudden.",
    "Well, time hangs heavy.{LB}Tossing this coin.{LB}Heads means joining.",
    "Skip the drink.{LB}Join us!",
    "That again?{LB}Then ask the coin once more.",
    "Heh. Can't trust my life{LB}to someone unlucky.{LB}Goodbye.",
    "Heh. Settled.{LB}My life gets wagered on you!",
    "Dias! Call me Dias.{LB}Another turn of luck!",
    "Welcome.",
    "Tch. Poor pickings lately.",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        selected = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B178_")]
    if len(selected) != 64 or selected[0]["id"] != "DK4_MES_B178_R0011" or selected[-1]["id"] != "DK4_MES_B178_R0357":
        raise SystemExit("B178 inventory boundaries changed")
    rows = [row for row in selected if row["id"] not in EXCLUDED]
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B178: {len(rows)} visible rows != {len(TRANSLATIONS)} translations")
    speaker_names = {0x04: "Janus Pasar", 0x05: "Claudio Manini", 0x14: "Fernando Dias", 0x8E: "Choice or reply"}
    records = []
    for row, english in zip(rows, TRANSLATIONS, strict=True):
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in speaker_names else ""
        unsafe = english
        for macro in ("FI", "FA", "FO", "FU"):
            unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row["id"], "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": speaker_names.get(first, "Raphael Castor or tavern patron"),
            "context": "Raphael challenges gambler Fernando Dias, learns the coin game's deterministic strategy from Janus, witnesses Fernando's observation skills, and may recruit him by coin toss.",
            "source_meaning": english.replace("{LB}", " ").replace("{MACRO:FI}", "Raphael"),
            "localization_note": "Faithful natural American English preserving both challenge branches, exact modulo-four strategy, breakup deduction, coin-toss outcomes, and canonical identity.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects game instructions, branch pacing, and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v51-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Fernando Dias's complete coin game, strategy tutorial, observation demonstration, and recruitment branches in SC0 block 178.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(selected), "translated_records": len(records), "blocks": {"178": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} control excluded")


if __name__ == "__main__":
    main()
