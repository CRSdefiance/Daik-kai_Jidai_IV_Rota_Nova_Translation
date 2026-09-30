from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v37.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("Admiral, over there! A ship is on fire!", "Admiral! Look! A ship's on fire!"),
    9: ("That ship is Clifford's Galahad!", "That's Clifford's ship, the Galahad!"),
    20: ("We must help him!", "Help him!"),
    24: ("It's already impossible. We can't get close to it!", "Too late... We can't get close!"),
    27: ("But...!", "But...!"),
    35: ("Heh, for me to end up like this... How disgraceful...", "Heh... What a sorry sight..."),
    39: ("Clifford!", "Clifford!"),
    51: ("Clifford!", "Clifford!"),
    58: ("Those voices... Is that FI and the others?", "Those voices... {MACRO:FI}...?"),
    61: ("Clifford, can you hear me? You're there, aren't you?!", "Clifford! Hear me? Are you there?!"),
    72: ("Clifford, please escape!", "Clifford! Get out of there!"),
    79: ("Are they trying to rescue me...?", "Trying to save me...?"),
    83: ("As always, they're softhearted... or perhaps straightforward...", "Still so softhearted... So honest..."),
    87: ("But I, the pirate Clifford, cannot accept charity from anyone else.", "But a pirate like Clifford can't accept anyone's pity."),
    90: ("Burn this into your memory: how the pirate Clifford dies...", "Remember this... How the pirate Clifford dies..."),
    94: ("Galahad, shall we go? This time let's run wild in the next world...", "Galahad... On to the next world! Let's raise hell..."),
    98: ("Clifford!", "Clifford!"),
    102: ("Clifford, why? Why choose death? You didn't have to die...!", "Clifford... Why?! Why choose death? You didn't have to die...!"),
    106: ("I believed in you... I believed you were one of my friends...", "You had my trust... You were my friend..."),
    117: ("I think I can understand how Clifford feels...", "Maybe... His feelings make sense."),
    121: ("He must have regretted deceiving FI...", "He must have regretted deceiving you, {MACRO:FI}..."),
    124: ("Do you think so...?", "Really?"),
    128: ("Without the ties binding him to the British royal family, this wouldn't have happened. I think he wanted to get along with us...", "His ties to Britain's Crown caused this... He wanted to be our friend."),
    138: ("Admiral, we found this box in the wreckage...", "Admiral! A box in the wreck!"),
    142: ("This is...", "This..."),
    152: ("It's the stolen Proof of Conquest!", "The stolen Proof!"),
    158: ("It's the Proof of Conquest. Oh, this letter...", "The Proof. Oh, a letter..."),
    162: ("Dear FI and Kamil,", "Dear {MACRO:FI} and Kamil,"),
    165: ("I'm sorry. I pray for your success. James Clifford.", "So sorry. Wishing you both success. James Clifford"),
    169: ("Clifford... At least, rest in peace...", "Clifford... May you rest in peace..."),
}
SPEAKERS = {0x02: "Lil Argot", 0x09: "Kamil", 0x97: "Lookout", 0xFE: "Clifford offscreen voice"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B122_")}
    if {f"DK4_MES_B122_R{number:04d}" for number in LINES} != expected:
        raise ValueError("B122 coverage does not match clean source")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B122_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unmapped lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer macro byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}" + english + "{PAD}",
            "speaker": "Clifford's letter" if number in {162, 165} else SPEAKERS[lead],
            "context": (
                "Lil and Kamil try to save Clifford from his burning Galahad, but he refuses rescue and dies."
                if number <= 106 else
                "Kamil reflects on Clifford's remorse and royal obligations; the wreck yields the stolen Proof and a farewell letter."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Localized from clean Japanese with the full scene reviewed. "
                "Preserves Galahad, Clifford's refusal of pity, remorse and royal ties, the stolen Proof, and three FI macros. "
                "FE is the existing offscreen/text presentation state; staging Japanese line breaks are not carried into prose."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v34-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 30 B122 Clifford death and farewell-letter records.",
        "inventory": {"identified_records": 30, "translated_records": len(records), "blocks": {"122": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
