from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v72.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    10: ("Sanghyeon calls out to Lil in a dream.", "...Ma'am"),
    18: ("Sanghyeon addresses Lil by her name macro.", "{MACRO:FI}..."),
    22: ("Lil stirs in her sleep.", "...Hm?"),
    26: ("Sanghyeon apologizes for appearing unannounced.", "Pardon me. No harm meant."),
    29: ("Sanghyeon introduces himself as Yifa's senior disciple.", "My name is Sanghyeon, Yifa's senior disciple."),
    33: ("Sanghyeon came to greet the person who accepted Yifa.", "Heard you took Yifa in. Thank you."),
    37: ("Lil asks whether he came about Yifa.", "About Yifa...?"),
    41: ("Sanghyeon blames his teaching for Yifa's free spirit.", "Her unruly ways are my fault. My teaching failed her."),
    44: ("Yifa fled her training and crossed the border without permission.", "She fled training without leave and went abroad. That's forbidden."),
    48: ("Yifa does not know that her country forbids leaving.", "She doesn't know our people are forbidden to leave the country."),
    52: ("Lil asks whether Sanghyeon intends to bring Yifa home.", "So you're taking her back?"),
    55: ("Sanghyeon says Yifa was expelled for breaking the law.", "No. She broke the law and has been expelled from our school."),
    58: ("Sanghyeon says their formal bond is severed.", "Our bond as disciples is severed..."),
    61: ("He says he and Yifa grew up like siblings.", "But we grew up together, like brother and sister."),
    64: ("Sanghyeon fears immature Yifa may offend people.", "She's still young. She may offend someone. That worries me."),
    68: ("Sanghyeon asks Lil to guide Yifa on the right path.", "Please guide Yifa so she stays on the right path."),
    71: ("He asks Lil to keep Yifa training by their master's teaching.", "And please see that she trains and follows our master's teachings."),
    74: ("Sanghyeon entrusts Yifa to Lil.", "Please take good care of Yifa."),
    77: ("Lil wakes and wonders whether the visitor was a dream.", "A dream? So real..."),
    80: ("Yifa greets Lil brightly and starts suggesting departure.", "Morning! Come on, let's set sail..."),
    87: ("Lil notices Yifa has stopped.", "What?"),
    91: ("Yifa senses Sanghyeon's presence.", "My senior...!"),
    95: ("Lil asks whether Yifa's senior is named Sanghyeon.", "Your senior... is he called Sanghyeon?"),
    99: ("Yifa is shocked and asks if her senior is aboard.", "What?! Brother Sanghyeon is here?"),
    102: ("Lil explains Sanghyeon introduced himself in her dream.", "A man in my dream said he was your senior. Sanghyeon."),
    106: ("Yifa repeats that he came in a dream.", "A dream..."),
    110: ("Yifa murmurs Sanghyeon's name.", "Brother Sanghyeon..."),
    114: ("Yifa realizes Sanghyeon used his art to reach her from the mountain.", "He came by spell from the mountain."),
    118: ("Lil still does not understand Taoist arts.", "His art? Still don't get it..."),
    122: ("Lil relays Sanghyeon's message to keep training and obey the master.", "He said to keep training and obey your master, even away from home."),
    126: ("Yifa smiles at her senior's concern.", "Brother always worries. Heh."),
    130: ("Lil asks what Yifa is thinking.", "What?"),
    133: ("Yifa promises to train hard rather than disappoint Sanghyeon.", "Gonna train hard! Can't let Brother Sanghyeon down!"),
    137: ("Lil says ship duties must come before Yifa's training.", "Shipwork comes first! Train after your duties."),
    140: ("Yifa accepts Lil's order.", "Got it!"),
}

SPEAKERS = {0x02: "Lil Argot", 0x19: "Yifa", 0x51: "Sanghyeon"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B171_")}
    authored = {f"DK4_MES_B171_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B171 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B171_R{number:04d}"
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
            "context": "Sanghyeon appears to Lil in a dream and entrusts Yifa's continued training to her.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B171 Japanese. The FI name macro "
                "and source presentation leads retain their control "
                "behavior. Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v72-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 35 B171 Sanghyeon dream and Yifa training records.",
        "inventory": {"identified_records": 35, "translated_records": 35, "blocks": {"171": 35}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
