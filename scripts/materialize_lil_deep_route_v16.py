from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v16.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
LINES = {
    "DK4_MES_B71_R0005": "Ah, time to enjoy the city!{LB}So happy!{LB}Shopping after so long!",
    "DK4_MES_B71_R0009": "Huh? Kamil, not ready?{LB}Leaving without you!",
    "DK4_MES_B71_R0012": "{MACRO:FI}, wait!{LB}Just a moment!",
    "DK4_MES_B71_R0015": "Come on! You are a man,{LB}yet take longer than me to dress.{LB}Hurry!",
    "DK4_MES_B71_R0019": "Stop rushing me!",
    "DK4_MES_B71_R0023": "Kamil, still not ready?{LB}Really leaving now!",
    "DK4_MES_B71_R0026": "Sorry. Let us go.",
    "DK4_MES_B71_R0034": "What is it...?",
    "DK4_MES_B71_R0039": "Oh, that is Dukov.",
    "DK4_MES_B71_R0047": "{MACRO:FI}?{LB}Hey, {MACRO:FI}",
    "DK4_MES_B71_R0050": "...So beautiful...{LB}(Such people exist.)",
    "DK4_MES_B71_R0053": "{MACRO:FI}...?{LB}Can you hear me?!",
    "DK4_MES_B71_R0056": "...Oh, sorry.",
    "DK4_MES_B71_R0060": "Your delay left me dazed!{LB}Let us go.",
    "DK4_MES_B71_R0063": "What about Dukov?{LB}You said something before.",
    "DK4_MES_B71_R0066": "Uh... no.{LB}Nothing.",
    "DK4_MES_B71_R0069": "{MACRO:FI}...{LB}do you perhaps like Dukov?",
    "DK4_MES_B71_R0072": "What nonsense!{LB}N-no, nothing like that!",
    "DK4_MES_B71_R0075": "No need to blush.{LB}He is certainly handsome.",
    "DK4_MES_B71_R0078": "No! That is not it!",
    "DK4_MES_B71_R0082": "Well, Dukov is beautiful...{LB}So yes, watched him a little.",
    "DK4_MES_B71_R0085": "See? Knew it!",
    "DK4_MES_B71_R0089": "But that is not love...{LB}More like... well...",
    "DK4_MES_B71_R0093": "Not love?",
    "DK4_MES_B71_R0097": "How to say it... Every woman{LB}would stare at him, right?",
    "DK4_MES_B71_R0101": "Maybe admiration?",
    "DK4_MES_B71_R0105": "Oh, is that so?{LB}Sure, we will call it that.",
    "DK4_MES_B71_R0109": "Hmph! Kamil may not understand{LB}a grown woman's heart.",
    "DK4_MES_B71_R0113": "Ha ha!{LB}A 'grown woman's heart'{LB}from {MACRO:FI}!",
    "DK4_MES_B71_R0117": "Ha ha, my stomach hurts!",
    "DK4_MES_B71_R0121": "Kamil!{LB}How dare you laugh!{LB}Running away, coward!",
    "DK4_MES_B71_R0125": "Of course, before you hit me!",
    "DK4_MES_B71_R0128": "Wait... Kamil,{LB}are you jealous?!",
    "DK4_MES_B71_R0131": "Ah, twisted boy's feelings!",
    "DK4_MES_B71_R0135": "Why be jealous?!",
    "DK4_MES_B71_R0139": "Hm?{LB}The admirals again...{LB}Good friends, but...",
    "DK4_MES_B72_R0005": "So incredibly{LB}persistent!!!",
    "DK4_MES_B72_R0008": "Oh, my beloved Christina!{LB}Why are you so cold?",
    "DK4_MES_B72_R0011": "Are you unwell?{LB}Who follows someone{LB}who hates him this much?",
    "DK4_MES_B72_R0014": "No need for shyness!",
    "DK4_MES_B72_R0018": "Enough! Listen.{LB}Our parents arranged it.{LB}No wish to marry you!",
    "DK4_MES_B72_R0021": "Hearing your voice alone{LB}makes me happy!",
    "DK4_MES_B72_R0024": "Moron!",
    "DK4_MES_B72_R0028": "That man...?",
    "DK4_MES_B72_R0032": "Yes, him.",
    "DK4_MES_B72_R0036": "Looks like trouble?",
    "DK4_MES_B72_R0039": "No trouble at all.{LB}Hey, Christina!",
    "DK4_MES_B72_R0043": "Christina!{LB}Been well?",
    "DK4_MES_B72_R0047": "Grandpa! When reach London?",
    "DK4_MES_B72_R0051": "Just now.{LB}Sailing again, you see.",
    "DK4_MES_B72_R0054": "Again?!{LB}Mom and Dad will stop you.",
    "DK4_MES_B72_R0057": "Only if you tell them.{LB}Ho ho ho.",
    "DK4_MES_B72_R0060": "Come on...",
    "DK4_MES_B72_R0064": "More important:{LB}want to sail too?",
    "DK4_MES_B72_R0067": "What?!{LB}Absolutely not!",
    "DK4_MES_B72_R0070": "Who is this fellow?",
    "DK4_MES_B72_R0073": "Dad's pal's son...{LB}What was his name?",
    "DK4_MES_B72_R0076": "Christina! Do not be shy!{LB}Are you her grandfather?",
    "DK4_MES_B72_R0080": "An honor to meet you!{LB}My name is Mivor!{LB}Mivor Gentz!",
    "DK4_MES_B72_R0083": "Yes, something like that.{LB}Our fathers promised it{LB}without asking me.",
    "DK4_MES_B72_R0087": "Somehow this odd fellow{LB}became my betrothed.",
    "DK4_MES_B72_R0090": "Oh. So.",
    "DK4_MES_B72_R0094": "Do not just say that!",
    "DK4_MES_B72_R0098": "Hm, this pale weakling...",
    "DK4_MES_B72_R0101": "Not only because our parents said so...{LB}Truly, Lady Christina...",
    "DK4_MES_B72_R0105": "Mom and Dad mean:{LB}'Stop swords and settle down.'{LB}What a bother.",
    "DK4_MES_B72_R0108": "Sounds like Herald.{LB}Maybe raised him wrong...",
    "DK4_MES_B72_R0111": "Ahem.",
    "DK4_MES_B72_R0115": "You stay quiet!{LB}Now, about that ship...",
    "DK4_MES_B72_R0119": "Right, right.{LB}Want to come with me?",
    "DK4_MES_B72_R0123": "You are skilled, right?{LB}Sail with Grandpa on my ship?",
    "DK4_MES_B72_R0135": "A beauty joins us? Nice!{LB}Adventure needs a beauty.",
    "DK4_MES_B72_R0139": "Something?",
    "DK4_MES_B72_R0146": "Grandpa,{LB}who are these people?",
    "DK4_MES_B72_R0149": "Well. (One thing after another.){LB}Admiral {MACRO:FI} {MACRO:FA}.",
    "DK4_MES_B72_R0152": "Admiral? Very young.",
    "DK4_MES_B72_R0156": "You wanted foreign sword matches.{LB}Why not train around the world?",
    "DK4_MES_B72_R0159": "No! Absolutely not!",
    "DK4_MES_B72_R0163": "Yes... good.{LB}Count me in.",
    "DK4_MES_B72_R0166": "No! No way!",
    "DK4_MES_B72_R0170": "So noisy!{LB}What will you do?",
    "DK4_MES_B72_R0173": "Going! No time like now.{LB}Right, Grandpa?",
    "DK4_MES_B72_R0176": "My granddaughter.{LB}You understand.",
    "DK4_MES_B72_R0179": "And you?{LB}Chase your beloved?",
    "DK4_MES_B72_R0182": "Well, uh...",
    "DK4_MES_B72_R0186": "He cannot swim.{LB}Terrified of water.{LB}Cannot follow, right?",
    "DK4_MES_B72_R0189": "Then... a duel!",
    "DK4_MES_B72_R0192": "Whoa!",
    "DK4_MES_B72_R0196": "You never understand!{LB}Hyaah!",
    "DK4_MES_B72_R0200": "Aaaah! Ouch!",
    "DK4_MES_B72_R0204": "With that stance,{LB}even a child would win.",
    "DK4_MES_B72_R0207": "Hm. Still sharp.",
    "DK4_MES_B72_R0210": "My rapier!{LB}Dad bought it!",
    "DK4_MES_B72_R0214": "Let us go!{LB}Sword matches are nice,{LB}but sailing sounds fun!",
}

SPEAKERS = {
    "02": "Lil Argot", "06": "Christina's grandfather", "07": "Christina",
    "09": "Kamil", "14": "Fernando", "15": "Ian Dukov", "4F": "Mivor Gentz",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    71: "During a rare day ashore, Lil admires Ian, Kamil becomes jealous, and their teasing turns into a chase while Ian observes them.",
    72: "In London, Christina rejects her parents' chosen fiancé Mivor and accepts her grandfather's invitation to join Lil's voyage for worldwide sword training.",
}
EXCLUDED = {"DK4_MES_B71_R0137": "ten-byte scene-control payload with no visible dialogue"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = (set(LINES) | set(EXCLUDED)) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V16 inventory mismatch: missing={sorted(missing)}")
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
            "localization_note": "Faithful concise American English preserving Lil and Kamil's teasing, Christina's forceful voice, Mivor's comic formality, and recruitment continuity.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Lil and Kamil's Ian jealousy scene and Christina's London recruitment across SC2 blocks 71-72.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(LINES) + len(EXCLUDED), "translated_records": len(records), "blocks": blocks},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records; excluded {len(EXCLUDED)} control")


if __name__ == "__main__":
    main()
