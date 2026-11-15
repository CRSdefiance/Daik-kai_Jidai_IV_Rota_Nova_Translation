from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v61.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("Al says he was hired as a bodyguard, not a porter or errand boy.", "Listen. You hired me to guard you, not carry your bags or run errands."),
    13: ("His employer says wages mean Al should do every assigned job.", "Bah. Loafing again? You're on my payroll. Do your job."),
    16: ("Al tells the employer to hire someone more docile; he risks his life as a guard.", "Want a yes-man? Hire one. This work can cost me my life."),
    20: ("The employer mocks Al as good only at fighting.", "So you're only good at fighting? Nothing else?"),
    24: ("The employer fires Al and says he will hire someone more obedient.", "Then we're done. A better man can take your place. Get out!"),
    30: ("Al accepts the dismissal and walks off.", "Have it your way!"),
    34: ("The attendant grumbles that Al's strength has made him arrogant.", "Al's strong, but far too proud."),
    38: ("The employer orders the attendant to find another bodyguard immediately.", "That brute is fired! Get a new guard, now!"),
    41: ("The attendant says Al's strength is unusually hard to replace.", "Strong men like Al are rare..."),
    45: ("The employer says finding a replacement is the attendant's job.", "Your job is to find one. Come on."),
    49: ("Kamil notices how muscular Al is.", "He had some serious muscles..."),
    53: ("Lil finds Al wild and attractive.", "Wild, huh? Pretty cool."),
    65: ("Emilio claims he has impressive muscles too.", "Hey, check out my muscles!"),
    68: ("Lil teases Emilio that his bulk is fat, not muscle.", "That's flab, Emilio!"),
    75: ("Kamil teases Lil for judging men by looks and having a small vocabulary.", "Oh, {MACRO:FI}. A man's either cool or not to you. Such a limited vocabulary."),
    78: ("Lil decides to invite Al aboard.", "Who cares? Let's ask him to join us!"),
    81: ("Kamil indulges Lil's decision.", "Sure, whatever you say."),
    84: ("Lil praises Kamil for agreeing so readily today.", "Heh, Kamil. So agreeable today!"),
    87: ("Kamil notes Lil never listens to his opinion in these situations.", "You never ask my opinion at times like this..."),
    90: ("Lil pretends not to hear Kamil's complaint.", "Huh? Can't hear you!"),
    95: ("Lil catches up with Al.", "Hey, you! Wait up!"),
    98: ("Al asks what Lil wants.", "What?"),
    102: ("Lil asks whether Al is strong.", "Hey, are you strong?"),
    106: ("Al says his strength should be obvious.", "Can't you tell?"),
    110: ("Lil accepts that he is strong.", "So you are."),
    114: ("Al tells Lil not to address him so casually.", "Watch how you speak to me."),
    118: ("Lil asks him to join and beat whoever blocks her way.", "Join us, then! Help us beat anyone in our way!"),
    122: ("Al says he will not babysit a child.", "No babysitting."),
    126: ("Lil twists his objection into agreement and asks his name.", "Then it's settled! You won't be babysitting. Your name?"),
    134: ("Kamil is appalled by Lil's absurd reasoning.", "(Th-that's absurd.)"),
    146: ("Fernando is baffled by Lil's reasoning.", "This woman... makes no sense."),
    156: ("Al begins to laugh.", "Heh... ha ha ha!"),
    160: ("Lil asks why he is laughing.", "What's funny?"),
    164: ("Al admits Lil has won him over completely.", "Heh... nothing. You win. Completely."),
    167: ("Al says sailing with Lil should supply plenty of fights.", "With you, there's always a fight."),
    170: ("Kamil privately agrees that Lil draws fights.", "(Sadly, true...)"),
    174: ("Al accepts and introduces himself; his canonical name is Al Fasi.", "All right. Al. Call me Al."),
    178: ("Lil introduces herself with both name macros and says she is an admiral.", "Al, meet {MACRO:FI} {MACRO:FA}. Your admiral."),
    182: ("Al accepts Lil's command and laughs at the prospect of a ridiculous voyage.", "Likewise, Admiral. This should be one ridiculous voyage... Ha ha!"),
    190: ("Lil finds Al odd.", "...Weirdo."),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x09: "Kamil", 0x0E: "Emilio",
    0x11: "Al Fasi", 0x14: "Fernando Dias",
    0x73: "Employer's attendant", 0x94: "Employer",
}
EXCLUDED = {
    "DK4_MES_B154_R0003": "Opaque ten-byte scene event payload (95 46 7D 80 29 63 05 05 2C 63)."
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B154_")}
    authored = {f"DK4_MES_B154_R{number:04d}" for number in LINES}
    if authored | EXCLUDED.keys() != expected or authored & EXCLUDED.keys():
        raise ValueError(f"B154 coverage mismatch: missing {expected - authored - EXCLUDED.keys()}")
    if source_rows["DK4_MES_B154_R0003"]["source_hex"].upper() != "95467D80296305052C63":
        raise ValueError("B154 R0003 scene event payload changed")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B154_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": (
                "After Al Fasi is fired as a bodyguard, Lil bluntly recruits him. "
                "Kamil, Fernando, and Emilio react to her impulsive approach."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B154 Japanese; 94 and 73 are Al's employer and attendant. "
                "The Al Fasi surname cannot be printed literally because uppercase F is a renderer "
                "macro byte, so his spoken introduction uses Al. FI/FA names and the ten-byte "
                "event payload retain their exact control behavior."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v61-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 40 B154 text records, preserving one opaque scene event payload.",
        "inventory": {"identified_records": 41, "translated_records": 40, "blocks": {"154": 40}},
        "excluded_records": EXCLUDED, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records, {len(EXCLUDED)} control excluded")


if __name__ == "__main__":
    main()
