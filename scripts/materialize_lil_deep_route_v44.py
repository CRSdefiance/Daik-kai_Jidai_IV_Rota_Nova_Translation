from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v44.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    (130, 5): ("About the gift from Clifford...", "About Clifford's gift..."),
    (130, 14): ("Gift? What are you talking about?", "Gift? What gift?"),
    (130, 17): ("Here is the letter.", "This letter."),
    (130, 21): ("Let me see. So you're the girl. Wait a moment.", "Let's see... Ah, you're the girl. Wait here."),
    (130, 25): ("Here you go.", "Here."),
    (130, 31): ("Clifford told me. This is what he meant, right?", "Clifford told me. This, right?"),
    (130, 34): ("So this is the key to the map.", "So this unlocks the map..."),
    (131, 5): ("I think this Old Parchment is a map to the Ruler's Proof.", "Old Parchment... Maybe the Ruler's Proof map!"),
    (131, 15): ("It looks blank, but there must be a hidden trick.", "Looks like plain paper. Something's hidden, though..."),
    (131, 20): ("But there's nothing on it. What's the trick?", "Nothing's written on it. So what's the trick?"),
    (131, 26): ("Could we use the Crimson Pigment?", "Could the Crimson Pigment help?"),
    (131, 30): ("Nothing else comes to mind. This must be it.", "Nothing else makes sense. This has to be it!"),
    (131, 42): ("How will you use it?", "How?"),
    (131, 57): ("FI, what are you doing?", "Wait, {MACRO:FI}! What are you doing?!"),
    (131, 64): ("I'll pour it over the parchment.", "Pour it over the parchment!"),
    (131, 76): ("Something is appearing.", "Hey! Something's appearing!"),
    (131, 82): ("I was right. We now have the map to the North Sea's Ruler's Proof.", "Ha! Knew it! The North Sea Ruler's Proof map is ours!"),
    (131, 92): ("FI, amazing. Let's go find the Ruler's Proof.", "Great, {MACRO:FI}! Ruler's Proof awaits!"),
    (131, 98): ("Clever. Let's go find the Ruler's Proof.", "Good eye! Ruler's Proof awaits!"),
    (131, 105): ("Now the North Sea is mine.", "Now the North Sea is mine!"),
    (132, 6): ("You aren't planning to trade in the southern Mediterranean, are you?", "You're not headed to the southern Mediterranean to trade, are you?"),
    (132, 10): ("Why? Is there something there?", "Why? What's down there?"),
    (132, 21): ("The southern Mediterranean is a fine place to make money. We can't miss it.", "Southern trade pays well! Let's go!"),
    (132, 27): ("Don't. Do not trade in the southern Mediterranean.", "Don't trade in the southern Mediterranean."),
    (132, 30): ("What do you mean?", "What do you mean?!"),
    (132, 34): ("I have warned you. Don't forget it.", "That's my warning. Remember it!"),
    (132, 45): ("What does he mean? What should we do, FI?", "What was that about? What now, {MACRO:FI}?"),
    (132, 51): ("Don't go to the southern Mediterranean? Why?", "Stay out of southern waters... Why?"),
}

EXCLUDED = {
    "DK4_MES_B131_R0080": (
        "Four-byte #H9BA8 event payload between the pigment reveal and Lil's response; "
        "no parseable Japanese dialogue or speaker, so preserve raw bytes pending runtime correlation."
    )
}
SPEAKERS = {0x02: "Lil Argot", 0x09: "Kamil", 0x14: "Fernando Dias", 0x5C: "Local man"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith(("DK4_MES_B130_", "DK4_MES_B131_", "DK4_MES_B132_"))}
    authored = {f"DK4_MES_B{block}_R{number:04d}" for block, number in LINES}
    if authored | EXCLUDED.keys() != expected or authored & EXCLUDED.keys():
        raise ValueError("B130-B132 source coverage mismatch")
    records = []
    for (block, number), (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B{block}_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unmapped speaker {lead:02X}")
        if "I" in english.replace("{MACRO:FI}", "") or "F" in english.replace("{MACRO:FI}", ""):
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": (
                "Clifford's letter yields a map key; Lil uses Crimson Pigment on Old Parchment to reveal the North Sea Ruler's Proof map."
                if block < 132 else
                "A local man warns Lil against trading in the southern Mediterranean."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Clean Japanese reviewed in scene order; uses the established Old Parchment, Crimson Pigment and "
                "Ruler's Proof terms. Preserves source speaker selectors and FI macro. "
                "The opaque four-byte B131 R0080 event payload is excluded unchanged."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v41-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "B130-B132 map-key reveal and southern Mediterranean warning: 28 translated records, one raw event exclusion.",
        "inventory": {"identified_records": 29, "translated_records": len(records), "excluded_records": 1, "blocks": {"130": 7, "131": 13, "132": 8}},
        "excluded_records": EXCLUDED,
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records, {len(EXCLUDED)} exclusion")


if __name__ == "__main__":
    main()
