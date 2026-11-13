from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v70.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("Lil asks what Kamil is doing.", "Kamil, what are you doing?"),
    8: ("Kamil is researching the Proof of Conqueror but worries about his source.", "Been studying the Proof, {MACRO:FI}. But the expert..."),
    12: ("Lil asks who knows about the Proof.", "Who is it?"),
    16: ("Mikhail announces he is the expert and greets Lil.", "None other than me! Ah, {MACRO:FI}, dear!"),
    20: ("Lil threatens to strike Mikhail if he touches her again.", "The old creep again! Touch me and you'll get another punch!"),
    24: ("Kamil tells Lil she went too far.", "Easy, {MACRO:FI}..."),
    28: ("Mikhail calls Lil cute despite her cold greeting.", "So cold, {MACRO:FI}! And yet so cute!"),
    32: ("Kamil addresses Mikhail as a learned professor and asks about the Proof.", "Professor, explain the Proof."),
    35: ("Mikhail accepts the title and asks Lil whether she is interested.", "Well, since you called me Professor... {MACRO:FI}, dear, curious about the Proof?"),
    38: ("Lil says Kamil asked and presses Mikhail for an explanation.", "Kamil asked! What is this Proof?"),
    41: ("Mikhail says the Proofs are regional sea treasures for those who rule them.", "Each sea has a treasure for its ruler. Much remains unknown."),
    44: ("Ancient records say seven sages marked seven treasures on maps.", "Ancient texts name seven treasures. Seven sages marked them on different maps."),
    47: ("A ruler of each sea is destined to receive its map.", "Rulers are fated to find their maps."),
    51: ("Kamil imagines their fleet acquiring the Proofs.", "So if {MACRO:FO} found a Proof...!"),
    55: ("Lil calls them proof of maritime rule.", "Proof of rule."),
    67: ("Lil's grandfather grudgingly praises Mikhail.", "Hmm. Mikhail can talk sense sometimes."),
    82: ("Ian says the Proof would establish the fleet's dominance in each sea.", "{MACRO:FO} would rule the sea..."),
    97: ("Fernando wants to gather all seven despite not grasping the theory.", "Not sure about all that. Let's find every Proof!"),
    104: ("Mikhail asks whether they are impressed by his scholarship.", "Well? Amazed by my learning?"),
    107: ("Lil admits Mikhail is useful but warns him not to touch her.", "Well, you're aboard to help. Just keep your hands off me!"),
    111: ("Mikhail says not to worry and laughs.", "Don't worry! Ho ho ho!"),
    115: ("Lil remains skeptical of Mikhail.", "That's hardly reassuring!"),
    119: ("Kamil asks how they can gather the Proofs.", "How do we find them?"),
    123: ("Mikhail advises gaining power and asking regional leaders for clues.", "Rule each sea. Leaders hold clues."),
    126: ("Mikhail says they may need to defeat evil holders of clues.", "Should an evil ruler hold one, you'll have to defeat them."),
    130: ("Lil summarizes that they must defeat villains.", "So we beat the villains. Got it."),
    133: ("Mikhail directs them to city ruins for sealed Proof mysteries.", "Then find ruins in the cities and solve the Proof's hidden riddles."),
    137: ("Lil asks how they can locate ruins.", "How do we find the ruins?"),
    141: ("Mikhail cryptically answers that women can tell them.", "Women."),
    145: ("Lil is baffled.", "What?!"),
    149: ("Mikhail says major cities hold leads to nearby ruins.", "Ask in big cities about ruins."),
    152: ("Lil asks what that has to do with women.", "And the women?"),
    156: ("Mikhail says tavern women hear sailors' tales from around the world.", "Tavern girls hear sailors' tales from everywhere. They may know something."),
    160: ("Mikhail warns that important leads will not be free.", "They won't share such valuable news for nothing."),
    163: ("Lil calls the informants stingy.", "How stingy!"),
    167: ("Mikhail says the payment is small beside the treasure's value.", "Give and take, my dear. A small price beside the treasure's worth."),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x06: "Lil's grandfather", 0x09: "Kamil",
    0x14: "Fernando", 0x15: "Ian Dukov", 0x4C: "Mikhail Lett",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B169_")}
    authored = {f"DK4_MES_B169_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B169 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B169_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "").replace("{MACRO:FO}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "Mikhail explains the seven Proofs of Conqueror, regional power, ruins, and tavern leads.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B169 Japanese. The FI and FO name "
                "macros and source presentation leads retain their control "
                "behavior. Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v69-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 36 B169 Proof of Conqueror explanation and discovery tutorial records.",
        "inventory": {"identified_records": 36, "translated_records": 36, "blocks": {"169": 36}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
