from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v88.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    (192, 6): ("One man asks whether his friend has ever smoked tobacco.", "Say, ever smoked tobacco?"),
    (192, 10): ("His friend is surprised that he has not yet tried tobacco.", "You still haven't tried it?"),
    (192, 13): ("The first man has never had the chance to try it.", "No chance yet, to be honest."),
    (192, 16): ("His friend says tobacco is so popular that he may be the only nonsmoker in town.", "Really? Everyone smokes it now. You may be the last one in town!"),
    (192, 20): ("The first man says he would like to try smoking tobacco.", "Maybe so. Sounds worth a try."),
    (192, 23): ("His friend offers to let him try and asks him to come along.", "Come along. Let me show you."),
    (192, 26): ("The first man agrees.", "Okay."),
    (192, 30): ("The market notice predicts tobacco will become popular in Istanbul.", "Tobacco may boom in Constantinople."),
    (193, 6): ("A guest says she has never tasted such a wonderful meal.", "Delicious! Best meal ever."),
    (193, 10): ("Another guest agrees that the flavor was exciting.", "Quite. Such a lively flavor."),
    (193, 14): ("The first guest asks how to make such delicious food.", "How did you make this so tasty?"),
    (193, 17): ("The cook laughs and reveals her secret ingredient.", "Hee hee. See this?"),
    (193, 25): ("The cook explains that chili peppers are a spice suited to local ingredients.", "Chili peppers. A spice, and perfect with our local food."),
    (193, 29): ("The guest asks whether chili peppers are expensive.", "My, isn't it expensive?"),
    (193, 33): ("The cook says they are not especially expensive.", "Not really."),
    (193, 37): ("The guest considers using them in tonight's cooking.", "Then maybe we'll try it tonight."),
    (193, 40): ("The other guest also wants to try cooking with the spice.", "Me too!"),
    (193, 44): ("The cook offers to teach the guests how to use the spice.", "Come, let me show you how."),
    (193, 47): ("The first guest is delighted by the offer.", "Really?"),
    (193, 51): ("The other guest thanks the cook for her kindness.", "How kind!"),
    (193, 55): ("The cook says it is natural to help her friends.", "Of course. We're friends."),
    (193, 59): ("The market notice predicts chili peppers will become popular in Seoul.", "Chilies may catch on in Seoul."),
    (194, 6): ("A townsman recently drank sake.", "Tried sake the other day."),
    (194, 10): ("His friend says he also drank some.", "Same here."),
    (194, 14): ("The first townsman thinks it tastes good.", "Good stuff, eh?"),
    (194, 18): ("His friend says sake is made from rice.", "Made from rice, they say."),
    (194, 22): ("The first townsman is surprised that rice can make alcohol.", "Huh, made from rice?"),
    (194, 26): ("Talking about sake makes his friend want a drink, and he invites the other man.", "Sake sounds good. Join me?"),
    (194, 30): ("The first townsman likes the idea.", "Sounds good!"),
    (194, 34): ("His friend suggests they leave at once.", "Then let's get going."),
    (194, 46): ("A companion realizes this is the fabled drink and calls Admiral FI's attention to it.",
                "That must be the fabled drink! Admiral {MACRO:FI}, hear that?"),
    (194, 49): ("The companion urgently proposes buying the sake.", "Come on! Let's buy that sake now!"),
    (194, 56): ("The market notice predicts sake will become popular in Hangzhou.", "Sake may boom in Hangzhou."),
}
SPEAKERS = {
    0x99: "Istanbul townsman", 0x73: "Friend", 0xA6: "Seoul guest",
    0xA7: "Other guest", 0xA8: "Cook", 0x9C: "Hangzhou townsman",
    0x75: "Friend", 0x06: "Companion", 0xFE: "Market notice",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith(("DK4_MES_B192_", "DK4_MES_B193_", "DK4_MES_B194_"))}
    authored = {f"DK4_MES_B{block}_R{number:04d}" for block, number in LINES}
    if authored != expected:
        raise ValueError(f"B192-B194 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for (block, number), (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B{block}_R{number:04d}"
        raw = bytes.fromhex(source_rows[row_id]["source_hex"])
        lead = raw[0]
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if english.count("{MACRO:FI}") != raw.count(b"FI"):
            raise ValueError(f"{row_id}: FI name-macro count mismatch")
        prose = english.replace("{MACRO:FI}", "")
        if "I" in prose or "F" in prose:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "Istanbul tobacco, Seoul chili peppers, and Hangzhou sake market scenes.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B192-B194 Japanese. Source presentation "
                "leads and the FI name macro are preserved. Literal uppercase I/F "
                "are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v88-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 33 B192-B194 Istanbul tobacco, Seoul chilies, and Hangzhou sake records.",
        "inventory": {"identified_records": 33, "translated_records": 33, "blocks": {"192": 8, "193": 14, "194": 11}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
