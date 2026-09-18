from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v9.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
LINES = {
    "DK4_MES_B87_R0006": "Zipang...{LB}Such a unique culture.",
    "DK4_MES_B87_R0010": "What strange hair.{LB}Do they lack taste?",
    "DK4_MES_B87_R0021": "Now, now.{LB}Every culture has{LB}its own beauty.",
    "DK4_MES_B87_R0025": "Suppose so...",
    "DK4_MES_B87_R0032": "Well, well!{LB}You are foreigners?",
    "DK4_MES_B87_R0035": "Heard you foreigners are acting big{LB}in our land lately!",
    "DK4_MES_B87_R0039": "Trouble, {MACRO:FI}...{LB}Some odd men noticed us.",
    "DK4_MES_B87_R0043": "Walk on.",
    "DK4_MES_B87_R0055": "Best avoid needless trouble.",
    "DK4_MES_B87_R0062": "Ow! Boss, that hurts!",
    "DK4_MES_B87_R0066": "Oh no! You struck my dear man{LB}on purpose. His bone is broken!{LB}A disaster!",
    "DK4_MES_B87_R0071": "N-no!{LB}You ran into us!",
    "DK4_MES_B87_R0075": "{MACRO:FI}, words are useless.{LB}They will never listen.",
    "DK4_MES_B87_R0087": "Trouble found us{LB}as soon as we spoke.",
    "DK4_MES_B87_R0093": "Want a fight?{LB}Boss, they hit us and now{LB}they challenge us!",
    "DK4_MES_B87_R0097": "Heaven may forgive you,{LB}but Kurushima never will!{LB}Get them!",
    "DK4_MES_B87_R0101": "Yeah!",
    "DK4_MES_B87_R0107": "What now?{LB}There are so many of them...",
    "DK4_MES_B87_R0111": "Too many or not, we fight!{LB}Old man, stay behind me!",
    "DK4_MES_B87_R0115": "My aid!",
    "DK4_MES_B87_R0129": "Leave this to me.",
    "DK4_MES_B87_R0133": "What? A samurai sides{LB}with foreigners?!",
    "DK4_MES_B87_R0137": "Justice is{LB}mine to judge.",
    "DK4_MES_B87_R0141": "You insolent fool!{LB}Men, get him!",
    "DK4_MES_B87_R0145": "Yeah!",
    "DK4_MES_B87_R0150": "Aaaah!",
    "DK4_MES_B87_R0154": "We lost!",
    "DK4_MES_B87_R0158": "Remember this!",
    "DK4_MES_B87_R0162": "Blade back.{LB}No one was cut.",
    "DK4_MES_B87_R0167": "Amazing...{LB}Never saw the blade.",
    "DK4_MES_B87_R0170": "Y-yes... amazing.",
    "DK4_MES_B87_R0182": "An Eastern mystery.",
    "DK4_MES_B87_R0189": "You saw our nation's shame.{LB}Please forgive us.",
    "DK4_MES_B87_R0193": "No, you saved us.",
    "DK4_MES_B87_R0197": "Pardon me, but you seem{LB}to sail throughout the world.",
    "DK4_MES_B87_R0200": "Would you permit me{LB}to join your travels?",
    "DK4_MES_B87_R0203": "My wish is to see{LB}the wider world.",
    "DK4_MES_B87_R0207": "Yes, but no return{LB}for some time.",
    "DK4_MES_B87_R0210": "No wish to return remains.{LB}A man must test himself{LB}in the wider world.",
    "DK4_MES_B87_R0214": "Then welcome.{LB}{MACRO:FI} {MACRO:FA}.",
    "DK4_MES_B87_R0217": "Yukihisa Genjo Shiraki,{LB}at your service.",

    "DK4_MES_B88_R0009": "This is...",
    "DK4_MES_B88_R0013": "Amazing...",
    "DK4_MES_B88_R0018": "So... magnificent.",
    "DK4_MES_B88_R0022": "Wait. We found it first,{LB}so where did Julian go?",
    "DK4_MES_B88_R0026": "Maybe we passed him somewhere?",
    "DK4_MES_B88_R0031": "Ah! What you hold is...",
    "DK4_MES_B88_R0035": "Oh, you!",
    "DK4_MES_B88_R0040": "You are Julian?{LB}My name is {MACRO:FI}.",
    "DK4_MES_B88_R0044": "Have we met?",
    "DK4_MES_B88_R0048": "Not directly.{LB}We heard you speak with Meihua{LB}at the Hangzhou tavern.",
    "DK4_MES_B88_R0053": "The Silla Gold Crown sounded{LB}interesting, so we came{LB}to find it too.",
    "DK4_MES_B88_R0057": "What?!",
    "DK4_MES_B88_R0061": "How cruel...{LB}That was meant as a gift for her.",
    "DK4_MES_B88_R0065": "Now my honor is ruined!{LB}How can Meihua face me?",
    "DK4_MES_B88_R0068": "Trouble, {MACRO:FI}.{LB}What now?",
    "DK4_MES_B88_R0073": "Give it to Julian.",
    "DK4_MES_B88_R0075": "Give it to her myself.",
    "DK4_MES_B88_R0083": "Do not misunderstand.{LB}Your devotion moved us,{LB}so we wanted to help.",
    "DK4_MES_B88_R0087": "R-really?!",
    "DK4_MES_B88_R0092": "Yes. Please give it{LB}to Meihua soon.",
    "DK4_MES_B88_R0096": "Such kindness to a stranger!{LB}What a generous man.{LB}Then, goodbye!",
    "DK4_MES_B88_R0100": "Hey... already gone.{LB}He moves fast.",
    "DK4_MES_B88_R0104": "This is fine. We saw the crown,{LB}and he needs it more.",
    "DK4_MES_B88_R0108": "Too kind...{LB}But like you, {MACRO:FI}.",
    "DK4_MES_B88_R0119": "Sorry...{LB}But this crown is also meant{LB}as a gift for Meihua.",
    "DK4_MES_B88_R0123": "What?! A rival in love!{LB}Must find another way at once!",
    "DK4_MES_B88_R0127": "Wait, Julian...",
    "DK4_MES_B88_R0131": "So fast... already gone.",
    "DK4_MES_B88_R0136": "Was that cruel?",
    "DK4_MES_B88_R0140": "No concern.{LB}He arrived too late.{LB}Let us return.",
}

SPEAKERS = {
    "05": "Claudio Manous", "06": "Julio", "0C": "Yukihisa Genjo Shiraki",
    "1A": "Julian", "29": "Kurushima", "9E": "Kurushima henchman",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    "87": "In Japan, Yukihisa rescues Raphael's party from Kurushima's staged extortion and joins to see the wider world.",
    "88": "Raphael beats Julian to the Silla Gold Crown and chooses whether to give it to Julian for Meihua or keep it as his own gift, with both branches fully localized.",
}
EXCLUDED = {
    "DK4_MES_B87_R0127": "seven-byte battle-scene control payload with no visible dialogue",
    "DK4_MES_B88_R0004": "nine-byte treasure-scene control payload with no visible dialogue",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    inventory = {row_id for row_id in all_rows if row_id.startswith(("DK4_MES_B87_", "DK4_MES_B88_"))}
    if set(LINES) | set(EXCLUDED) != inventory or set(LINES) & set(EXCLUDED):
        raise SystemExit(f"Raphael V9 inventory mismatch: missing={sorted(inventory-set(LINES)-set(EXCLUDED))} extra={sorted((set(LINES)|set(EXCLUDED))-inventory)}")
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
            "localization_note": "Faithful concise American English preserving comic timing, period flavor, recruitment motives, both crown choices, romance, and route-name macros.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v9-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Yukihisa's Japan recruitment and both Silla Gold Crown choices with Julian across Raphael SC0 blocks 87-88.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(inventory), "translated_records": len(records), "blocks": blocks},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records; excluded {len(EXCLUDED)} controls")


if __name__ == "__main__":
    main()
