from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v58.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    8: ("Clifford greets Lil's party.", "Hey!"),
    12: ("Lil recognizes Clifford.", "Oh, Clifford!"),
    24: ("Gerhard greets Clifford respectfully.", "Ah, Clifford!"),
    31: ("Clifford has heard that Lil's crew has done well abroad.", "Long time! Heard you're doing well everywhere."),
    42: ("Kamil says Clifford also seems to be thriving.", "Thanks. You're doing well yourself, Clifford."),
    48: ("Lil asks whether Clifford is expanding in the New World.", "So you're expanding into the New World, Clifford?"),
    52: ("Clifford confirms, then hesitates.", "More or less, but..."),
    56: ("Lil read Clifford's letter and asks what happened.", "Got your letter. What's wrong?"),
    60: ("Clifford explains that three factions now vie for the New World.", "Yes. Trouble. Three powers now vie for the New World."),
    63: ("Maldonado and Escante allied against Clifford, forming a huge force.", "Maldonado, Escante, and me. But those two have joined forces. They're huge now."),
    74: ("Fernando sees how difficult Clifford's position is.", "That's rough."),
    81: ("Clifford is hemmed in and embarrassed to seek help after boasting he would defeat them.", "My fleet's hemmed in. Hard to ask after calling them my prey, but..."),
    84: ("Lil guesses Clifford wants some help from her.", "So you need a little help from me?"),
    87: ("Clifford praises Lil for grasping the situation quickly.", "You catch on fast."),
    91: ("Lil knows both Maldonado and Escante will be hard to defeat.", "Maldonado and Escante? Neither will be easy to beat."),
    94: ("Clifford proposes striking Maldonado first.", "We hit Maldonado first!"),
    97: ("Clifford says their foes do not expect Lil's faction in the New World yet.", "They won't expect {MACRO:FO} here yet. Now's our chance."),
    108: ("Charles approves the plan to catch the enemies off guard.", "Aha! Catch them off guard. Clever!"),
    114: ("Clifford warns that Escante's power and resources far exceed Maldonado's.", "Escante's the real problem. His power and resources dwarf Maldonado's."),
    118: ("Clifford wants to build strength against Escante while defeating Maldonado.", "As we fight Maldonado, we'll build strength for Escante."),
    122: ("Lil doubts the plan but agrees because she sees no better option.", "Hmm... will that work? There's no better plan. All right, let's try."),
    126: ("Clifford entrusts the mission to Lil.", "Thanks."),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x09: "Kamil", 0x10: "Gerhard",
    0x12: "Charles Jean Rochefort", 0x14: "Fernando Dias",
    0x1C: "Clifford Guilford",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B150_")}
    authored = {f"DK4_MES_B150_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B150 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B150_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        literal = english.replace("{MACRO:FO}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": (
                "Clifford tells Lil that Maldonado and Escante have allied in the New World. "
                "He asks her to strike Maldonado while they build strength to face Escante."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from the clean B150 Japanese; preserves each speaker lead, "
                "Clifford's two-stage strategy, and the exact FO faction macro."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v48-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 22 dialogue records in B150; no event controls excluded.",
        "inventory": {"identified_records": 22, "translated_records": 22, "blocks": {"150": 22}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
