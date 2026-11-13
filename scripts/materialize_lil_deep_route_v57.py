from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v57.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    (148, 6): ("Lil asks the local man for his attention.", "Hey, mister."),
    (148, 10): ("The man asks what Lil wants.", "What is it, miss?"),
    (148, 14): ("Lil asks whether he knows Kuhn's son.", "Um... do you know Kuhn's son?"),
    (148, 18): ("The man is surprised she has heard about the son.", "Where'd you hear that?"),
    (148, 22): ("Lil avoids explaining her source.", "Just..."),
    (148, 26): ("The man recalls the boy's delicate, pretty face.", "Such a pretty boy. Looked almost like a girl."),
    (148, 30): ("Kuhn's wife and son disappeared years ago; rumor says they left home.", "His wife and son left years ago. Heard they moved away..."),
    (148, 34): ("Lil asks where Kuhn's wife and son are now.", "Where are they now?"),
    (148, 38): ("The man does not know; Kuhn never discusses them and no rumors followed.", "No idea. Kuhn won't speak of them. Not one rumor since."),
    (148, 41): ("Lil insists she must meet Kuhn's son and asks for any lead.", "Please, help me find his son! Tell me anything you know!"),
    (148, 45): ("The man cannot recall the boy's real name but remembers his nickname, Kamil.", "Can't recall his real name. We called him Kamil back then."),
    (148, 57): ("Fernando reacts in shock to Kamil's name.", "Kamil?!"),
    (148, 64): ("Lil asks if the man really said Kamil.", "Kamil? Did you just say Kamil?"),
    (148, 67): ("The man explains that the pretty boy was given the girl's nickname Kamil.", "Yes. Kamil's a girl's name, see? He was so pretty, we gave him that nickname."),
    (148, 70): ("The man notices Lil is upset.", "Miss? Something wrong?"),
    (148, 74): ("Lil denies anything is wrong and thanks him.", "N-no. Nothing. Thanks."),
    (148, 77): ("The man apologizes that he could not help more.", "Sorry, that's all."),
    (148, 82): ("Lil realizes Kamil may be Kuhn's son and she knows little about him.", "Kuhn's son is Kamil...? We hardly know a thing about him..."),
    (148, 94): ("Fernando has known Kamil a long time but did not know this secret.", "Same here. Known him for years, yet he hid that..."),
    (148, 100): ("Lil remembers Kamil said his father was dead.", "He even said his father was dead..."),
    (148, 103): ("Lil wonders if Kamil knew of Kuhn's methods and opposed him for that reason.", "Did Kamil know Kuhn's methods? Was that why he opposed him...?"),
    (148, 115): ("Fernando says Kamil knew but was torn because he could not tell the crew.", "He knew, but couldn't tell us... That fool."),
    (148, 130): ("Emilio pities Kamil.", "Poor Kamil..."),
    (148, 137): ("Lil quietly apologizes to Kamil.", "Kamil... please forgive me..."),
    (149, 5): ("Lil finds the Tang Bamboo Craft so intricate it gives her a headache.", "This Tang Bamboo Craft is so intricate. Just looking at it gives me a headache!"),
    (149, 17): ("Emilio jokes that merely looking at it makes him hungry.", "Just looking at it makes me hungry!"),
    (149, 28): ("Kamil says the Bamboo Assembly Plan shows how it works.", "The Bamboo Assembly Plan shows how it's made. Just follow the diagram."),
    (149, 32): ("Lil admits crafts are not her strength and asks Kamil to help.", "Crafts aren't my thing! You're good at this, Kamil!"),
    (149, 35): ("Kamil begins taking the craft apart.", "Right... this part comes off..."),
    (149, 38): ("Kamil believes he has disassembled it completely.", "Phew. That should be every piece."),
    (149, 41): ("Lil praises Kamil's skill with delicate work.", "Nice, Kamil! Such nimble hands!"),
    (149, 44): ("Kamil teases Lil for knowing when to flatter him.", "Oh, {MACRO:FI}. Such a flatterer."),
    (149, 48): ("Lil says her praise was sincere, then playfully hits Kamil.", "Hey! That was sincere! No more praise! (Bonk!)"),
    (149, 53): ("Fernando admires whoever designed the craft.", "Whoever made this is a genius."),
    (149, 56): ("Fernando suggests following the Bamboo Assembly Plan to dismantle it.", "Can't we take it apart by following the Bamboo Assembly Plan?"),
    (149, 60): ("Lil cannot manage it and asks Fernando to do it.", "That's why we asked! You try."),
    (149, 63): ("Fernando struggles with the craft, comparing it to reading dice.", "Me? Here goes... Harder than dice!"),
    (149, 67): ("Fernando finishes taking the craft apart.", "There. That should be all of it."),
    (149, 79): ("After Lil's playful blow, Kamil spots a drawing on the bamboo's underside.", "Ow, just kidding! Hey, a drawing under here!"),
    (149, 85): ("Lil grudgingly admits Kamil has done well.", "N-not bad."),
    (149, 89): ("Fernando boasts about his own skill.", "Pure skill."),
    (149, 93): ("Fernando spots a drawing on the bamboo's underside.", "Hey, a drawing under here!"),
    (149, 100): ("Lil recognizes the map to East Asia's Proof.", "A map to East Asia's Proof!"),
    (149, 110): ("Kamil urges the crew to search for the Proof.", "We did it! Let's go find it!"),
    (149, 115): ("Fernando urges the crew to find the Proof quickly.", "What luck! Let's go find the Proof!"),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x09: "Kamil", 0x0E: "Emilio",
    0x14: "Fernando Dias", 0x5C: "Batavia local man",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {
        row_id for row_id in source_rows
        if row_id.startswith(("DK4_MES_B148_", "DK4_MES_B149_"))
    }
    authored = {f"DK4_MES_B{block}_R{number:04d}" for block, number in LINES}
    if authored != expected:
        raise ValueError(f"B148-B149 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for (block, number), (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B{block}_R{number:04d}"
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
                "In Batavia, Lil discovers that Kamil may be Kuhn's estranged son. "
                if block == 148 else
                "The crew dismantles the Tang Bamboo Craft using the Bamboo Assembly Plan "
                "and discovers the map to East Asia's Proof. Kamil and Fernando have alternate branches."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from the clean Japanese source; preserves speaker leads, "
                "the Kamil identity clue, established item names, alternate companion lines, "
                "and the exact FI name macro."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v48-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 45 text records in B148-B149; no event controls excluded.",
        "inventory": {"identified_records": 45, "translated_records": 45, "blocks": {"148": 24, "149": 21}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
