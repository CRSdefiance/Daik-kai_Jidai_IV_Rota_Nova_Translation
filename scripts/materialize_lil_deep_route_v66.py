from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v66.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    6: ("Lil marvels at a large-eared animal.", "What is that huge-eared thing?"),
    9: ("Kamil names the elephant.", "That's an elephant."),
    13: ("Lil is impressed.", "Amazing!"),
    25: ("Emilio wonders whether a roasted elephant would taste good.", "Would it taste good roasted?"),
    37: ("Fernando asks Emilio to think of something besides food.", "Emilio, think beyond food for once!"),
    47: ("Samwell hawks the goods at his stall.", "Come on, buy something! Only fine goods here!"),
    50: ("Samwell notices unusual visitors and asks if they travel.", "Well, rare customers! You're travelers, right?"),
    53: ("Samwell asks to join them and see countries beyond the elephants.", "Take me along! Elephants bore me. Want to see other lands. Well?"),
    56: ("Lil objects to Samwell's brazen request.", "Who do you think you are? We don't take anyone who asks!"),
    60: ("Kamil asks Lil to calm down before anger gives her wrinkles.", "Easy, {MACRO:FI}. Keep scowling and you'll get wrinkles."),
    63: ("Lil scolds Kamil for mentioning wrinkles.", "Kamil! How dare you say that!"),
    66: ("Kamil apologizes for Lil and says she loves to get angry.", "Sorry. She loves a good tantrum. Don't mind her."),
    69: ("Samwell says he is too generous to mind what he calls a chubby girl.", "No worries. Tubby's words don't bother me. Big heart, see?"),
    73: ("Lil denies being fat and threatens Samwell.", "Tubby?! Where do you see any fat? Keep it up and you'll regret it!"),
    77: ("Samwell teases Lil for anger and says he likes round faces.", "You do love to rage! Don't worry. Round faces are cute."),
    81: ("Lil is speechless with anger.", "Whaaaat?! Grr..."),
    85: ("Kamil fears Lil's temper, stops Samwell teasing, and asks about his skill.", "Please stop teasing her! You'll get me killed. So, what can you do?"),
    88: ("Samwell proudly says cooking is his special talent.", "Glad you asked! Cooking! Great cooking, too!"),
    100: ("Emilio lights up at the prospect of a cook.", "Cooking?!"),
    106: ("Lil dismisses Samwell's claim and his insults toward a lady.", "Kamil, let's go! He's a liar, and rude to ladies!"),
    109: ("Samwell protests that calling Lil chubby is not an insult.", "Tubby? That's no insult!"),
    112: ("Lil insists it is an insult and tells Kamil to leave.", "Yes, it is! Come on, Kamil. We've wasted enough time!"),
    124: ("Emilio asks Samwell to join the crew.", "Join us!"),
    128: ("Lil objects to Emilio inviting Samwell without asking her.", "Hey! Who said you could invite him?"),
    132: ("Emilio hesitates.", "B-but..."),
    139: ("Kamil asks Samwell to demonstrate his cooking skill.", "Hold on. Show us your skill. Cook something for us."),
    143: ("Samwell agrees and asks for a moment.", "Easy. Give me a moment."),
    149: ("Samwell serves his dish.", "Ready! Go on, taste it."),
    153: ("Kamil tastes the food and is startled.", "Let's see... (munch) Wow!"),
    157: ("Kamil finds Samwell's cooking even better than Lil's and catches himself.", "Delicious! Better than {MACRO:FI}'s... oh!"),
    161: ("Lil demands to know what Kamil almost said.", "Kamil! What was that?"),
    172: ("Emilio savors the dish.", "So good!"),
    179: ("Kamil urges Lil to taste the food too.", "N-no... {MACRO:FI}, try it yourself!"),
    183: ("Lil warns that Samwell's dish had better be good.", "This had better taste good!"),
    186: ("Lil reluctantly admits the dish is tasty.", "Oh... it is good. Damn it."),
    189: ("Kamil introduces himself and admiral Lil to Samwell.", "Settled, then! Kamil. And this is {MACRO:FI}, our admiral."),
    193: ("Lil accepts Samwell for his cooking despite his teasing.", "All right... Cook this well daily and you can stay."),
    196: ("Samwell greets Lil with the teasing nickname again.", "Sure thing, Tubby!"),
    199: ("Lil angrily threatens Samwell again.", "That's it! You're dead!"),
    202: ("Kamil sighs about the trouble ahead.", "Long voyage ahead..."),
    213: ("Emilio asks for another serving.", "Seconds!"),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x09: "Kamil", 0x0E: "Emilio",
    0x14: "Fernando Dias", 0x16: "Samwell",
}
EXCLUDED = {
    "DK4_MES_B159_R0045": "Opaque five-byte market scene event payload (21 51 46 EE 80)."
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B159_")}
    authored = {f"DK4_MES_B159_R{number:04d}" for number in LINES}
    if authored | EXCLUDED.keys() != expected or authored & EXCLUDED.keys():
        raise ValueError(f"B159 coverage mismatch: missing {expected - authored - EXCLUDED.keys()}")
    if source_rows["DK4_MES_B159_R0045"]["source_hex"].upper() != "215146EE80":
        raise ValueError("B159 R0045 scene event payload changed")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B159_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": (
                "In an elephant market, Samwell asks to join Lil's crew; after trading "
                "insults, he wins them over with his cooking."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B159 Japanese. Four FI name macros, "
                "source presentation leads, and the five-byte market event retain "
                "their control behavior. Literal uppercase I/F are unsafe."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v64-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 41 B159 Samwell recruitment text records, preserving one market event.",
        "inventory": {"identified_records": 42, "translated_records": 41, "blocks": {"159": 41}},
        "excluded_records": EXCLUDED, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records, {len(EXCLUDED)} control excluded")


if __name__ == "__main__":
    main()
