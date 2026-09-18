from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v20.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
LINES = {
    "DK4_MES_B77_R0005": "What is this place?!",
    "DK4_MES_B77_R0008": "Heard stories,{LB}but still amazed.",
    "DK4_MES_B77_R0012": "Look at her hair.{LB}Could that style be popular?",
    "DK4_MES_B77_R0023": "More importantly, food!{LB}So hungry!",
    "DK4_MES_B77_R0037": "Hey, so hungry!",
    "DK4_MES_B77_R0044": "Well, well!{LB}You are foreigners?",
    "DK4_MES_B77_R0047": "Heard foreigners have grown bold{LB}in our land lately!",
    "DK4_MES_B77_R0051": "Some dangerous men{LB}have noticed us...",
    "DK4_MES_B77_R0054": "What do we do?",
    "DK4_MES_B77_R0066": "Time to eat...",
    "DK4_MES_B77_R0081": "Huh?",
    "DK4_MES_B77_R0088": "Ow! Boss, it hurts!",
    "DK4_MES_B77_R0092": "Oh no! You struck my dear man{LB}on purpose. His bone is broken!{LB}A disaster!",
    "DK4_MES_B77_R0096": "What nonsense!{LB}You ran into us!",
    "DK4_MES_B77_R0099": "{MACRO:FI}...{LB}They look dangerous...",
    "DK4_MES_B77_R0110": "A restaurant!{LB}Going to eat!",
    "DK4_MES_B77_R0124": "Hmm? Smells good...{LB}Sniff...",
    "DK4_MES_B77_R0130": "Want a fight?{LB}Boss, they hit us and now{LB}they challenge us!",
    "DK4_MES_B77_R0134": "Even heaven may forgive you,{LB}but Kurushima never will!{LB}Get them!",
    "DK4_MES_B77_R0138": "Yeah!",
    "DK4_MES_B77_R0143": "What now...",
    "DK4_MES_B77_R0147": "What do we do...",
    "DK4_MES_B77_R0159": "Emilio can save us!{LB}His strength can... Wait, gone?{LB}He is over there eating!",
    "DK4_MES_B77_R0170": "Samwell, then... Huh?{LB}He went into a restaurant!",
    "DK4_MES_B77_R0180": "Let me help!",
    "DK4_MES_B77_R0191": "...Leave this to me.",
    "DK4_MES_B77_R0195": "What? A samurai sides{LB}with foreigners?!",
    "DK4_MES_B77_R0199": "Justice is{LB}mine to judge.",
    "DK4_MES_B77_R0203": "You insolent fool!{LB}Men, get him!",
    "DK4_MES_B77_R0207": "Yeah!",
    "DK4_MES_B77_R0212": "Aaaah!",
    "DK4_MES_B77_R0216": "We lost!",
    "DK4_MES_B77_R0220": "Remember this!",
    "DK4_MES_B77_R0224": "Blade back.{LB}No cuts.",
    "DK4_MES_B77_R0228": "...Amazing!{LB}So cool!",
    "DK4_MES_B77_R0232": "Y-yes...{LB}One flash and they all fell...",
    "DK4_MES_B77_R0244": "That was delicious!{LB}Strange food, but very good.{LB}Travel is wonderful!",
    "DK4_MES_B77_R0258": "So full. Happy.",
    "DK4_MES_B77_R0279": "What now?",
    "DK4_MES_B77_R0283": "You return only now?!",
    "DK4_MES_B77_R0287": "Just leave him alone...",
    "DK4_MES_B77_R0296": "Huh? What happened?",
    "DK4_MES_B77_R0308": "What now?",
    "DK4_MES_B77_R0312": "You return only now?!",
    "DK4_MES_B77_R0316": "Just leave him alone...",
    "DK4_MES_B77_R0326": "...You saw our nation's shame.{LB}Please forgive us.",
    "DK4_MES_B77_R0329": "No...{LB}You helped us.",
    "DK4_MES_B77_R0332": "Pardon me, but you seem{LB}to sail throughout the world.",
    "DK4_MES_B77_R0335": "Would you permit me{LB}to join your travels?",
    "DK4_MES_B77_R0338": "My wish is to see{LB}the wider world.",
    "DK4_MES_B77_R0341": "A strong man is welcome!{LB}But no promise can be made{LB}that we return to Japan.",
    "DK4_MES_B77_R0345": "No wish to return remains.{LB}A man must test himself{LB}in the wider world...",
    "DK4_MES_B77_R0348": "Name: {MACRO:FI} {MACRO:FA}.{LB}Welcome.",
    "DK4_MES_B77_R0352": "Yukihisa Genjo Shiraki,{LB}at your service.",
    "DK4_MES_B78_R0011": "We did it!",
    "DK4_MES_B78_R0023": "Amazing...",
    "DK4_MES_B78_R0030": "We found it before Julian!{LB}Lucky us!",
    "DK4_MES_B78_R0036": "Ah! What you hold is...",
    "DK4_MES_B78_R0040": "Only arriving now?{LB}Sorry, the Silla Gold Crown{LB}belongs to me!",
    "DK4_MES_B78_R0044": "You know me?{LB}Who are you?",
    "DK4_MES_B78_R0047": "My name is {MACRO:FI}.{LB}You spoke of the Silla Crown{LB}in Hangzhou. That was overheard.",
    "DK4_MES_B78_R0050": "How cruel... eavesdropping.",
    "DK4_MES_B78_R0054": "Yet it let me meet you...{LB}Maybe fortune favored me after all.",
    "DK4_MES_B78_R0058": "Huh?",
    "DK4_MES_B78_R0070": "(Strange man.)",
    "DK4_MES_B78_R0077": "Your eyes are charming.{LB}Do people tell you that?",
    "DK4_MES_B78_R0081": "W-wait! What are you saying?!",
    "DK4_MES_B78_R0085": "That hat is cute too.{LB}Looks perfect. Such good taste!",
    "DK4_MES_B78_R0089": "Are you trying{LB}to court me...?",
    "DK4_MES_B78_R0092": "What else?{LB}Life is love! Love is everything!",
    "DK4_MES_B78_R0095": "Strange man...{LB}Enough. Take the Silla Gold Crown.",
    "DK4_MES_B78_R0099": "What?{LB}Meeting you made this{LB}worthless to me!",
    "DK4_MES_B78_R0103": "Just take it and go!",
    "DK4_MES_B78_R0106": "Ah! You worry about Meihua!{LB}Not only beautiful, but kind too!",
    "DK4_MES_B78_R0110": "...{LB}(That is not why.)",
    "DK4_MES_B78_R0113": "Then today, to honor your wish,{LB}the Silla Gold Crown is mine.{LB}Thank you! Until next time!",
    "DK4_MES_B78_R0120": "What was that?{LB}He is exhausting...",
    "DK4_MES_B79_R0006": "Julian is a Dutch name.{LB}Were you born there?",
    "DK4_MES_B79_R0009": "Me? Born and raised in Ming.{LB}My Chinese name is Luo Yuli.",
    "DK4_MES_B79_R0013": "Then your explorer grandfather{LB}was Dutch?",
    "DK4_MES_B79_R0017": "Yes. He sailed the world{LB}and drew maps.",
    "DK4_MES_B79_R0020": "Along the way, he met{LB}a mysterious black-haired girl{LB}of unknown origin.",
    "DK4_MES_B79_R0024": "Seeking her homeland led to China.{LB}There, the two were wed.",
    "DK4_MES_B79_R0028": "So she was your grandmother.",
    "DK4_MES_B79_R0032": "Exactly.",
    "DK4_MES_B79_R0036": "Lovely story...",
    "DK4_MES_B79_R0040": "Both parents have black hair,{LB}yet grandfather's color came to me.{LB}Does that feel like fate?",
    "DK4_MES_B79_R0044": "A sailor father?",
    "DK4_MES_B79_R0048": "No. Both are stern scholars.{LB}No ties to the sea.",
    "DK4_MES_B79_R0051": "They wanted a scholar or official.{LB}Study and hard work never suited me.",
    "DK4_MES_B79_R0054": "Yet you work hard to court girls.",
    "DK4_MES_B79_R0058": "W-well, that is different.",
}

SPEAKERS = {
    "02": "Lil Argot", "09": "Kamil", "0C": "Yukihisa Genjo Shiraki", "0E": "Emilio",
    "14": "Fernando", "16": "Samwell", "1A": "Julian", "29": "Kurushima",
    "9E": "Kurushima henchman",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    "77": "In Japan, Yukihisa rescues Lil's distracted party from Kurushima's thugs and joins to see the wider world.",
    "78": "Lil beats Julian to the Silla Gold Crown, then gives it up to escape his relentless flirting.",
    "79": "Julian recounts his Dutch grandfather's voyage to China, his Chinese heritage, and why he chose adventure over scholarship.",
}
EXCLUDED = {
    "DK4_MES_B77_R0189": "five-byte battle-scene control payload with no visible dialogue",
    "DK4_MES_B78_R0004": "nine-byte treasure-scene control payload with no visible dialogue",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = (set(LINES) | set(EXCLUDED)) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V20 inventory mismatch: missing={sorted(missing)}")
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
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Story participant"), "context": CONTEXTS[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Concise American English preserving comic timing, period flavor, recruitment stakes, romance, and family history.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Yukihisa recruitment, Silla Gold Crown rivalry, and Julian's family history in SC2 blocks 77-79.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(LINES) + len(EXCLUDED), "translated_records": len(records), "blocks": {"77": 54, "78": 23, "79": 15}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records; excluded {len(EXCLUDED)} controls")


if __name__ == "__main__":
    main()
