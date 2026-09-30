from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v60.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    (152, 5): ("A local notices the Ancient Kingdom Coin.", "That Ancient Kingdom Coin..."),
    (152, 9): ("Lil asks what is special about the coin.", "Hm? What about it?"),
    (152, 13): ("The local says the coin hides the legendary Ruler's Proof map.", "A map to the Ruler's Proof! You're no ordinary sailor..."),
    (152, 17): ("Lil is surprised but cannot see any map on the coin.", "A Proof map? Where? There's no map on this coin!"),
    (152, 21): ("The local admits he only heard that the coin is a map.", "Hm? Someone told me it was a map..."),
    (152, 25): ("Lil decides to investigate and thanks him.", "Then it must be! Let's look closer. Thanks, mister!"),
    (153, 5): ("Lil considers how the Ancient Kingdom Coin could hold a Proof map.", "The coin holds a Proof map? Then..."),
    (153, 8): ("Kamil thinks another item may be needed.", "Perhaps it needs something else?"),
    (153, 11): ("Lil suggests the Lotion Jar and wonders how to use it.", "Then the Lotion Jar. But how?"),
    (153, 14): ("Kamil suggests putting the coin into the jar.", "Put it in the jar."),
    (153, 18): ("Lil agrees to try.", "Right. Let's try..."),
    (153, 22): ("Lil sings as she rubs the coin.", "Scrub, scrub!"),
    (153, 26): ("The coin's surface dissolves and a map appears.", "The coin's surface melts... A map! There it is!"),
    (153, 29): ("Kamil celebrates the Southeast Asian Proof map and praises Lil by name.", "Now we have Southeast Asia's Proof map! Well done, {MACRO:FI}!"),
    (153, 33): ("Lil says the map is only the beginning and urges the search.", "Don't celebrate yet! The hard part starts now. Let's find the Proof!"),
}

SPEAKERS = {0x02: "Lil Argot", 0x09: "Kamil", 0x5C: "Local man"}
EXCLUDED = {"DK4_MES_B153_R0024": "Opaque four-byte map reveal event payload (23 48 9F A8)."}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {
        row_id for row_id in source_rows
        if row_id.startswith(("DK4_MES_B152_", "DK4_MES_B153_"))
    }
    authored = {f"DK4_MES_B{block}_R{number:04d}" for block, number in LINES}
    if authored | EXCLUDED.keys() != expected or authored & EXCLUDED.keys():
        raise ValueError(f"B152-B153 coverage mismatch: missing {expected - authored - EXCLUDED.keys()}")
    if source_rows["DK4_MES_B153_R0024"]["source_hex"].upper() != "23489FA8":
        raise ValueError("B153 R0024 map reveal event payload changed")
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
                "A local recognizes the Ancient Kingdom Coin as a hidden map. "
                "Lil and Kamil use the Lotion Jar to reveal the Southeast Asian Ruler's Proof map."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B152-B153 Japanese; uses the established item names, "
                "preserves the FI name macro, and leaves the map reveal event unchanged."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v48-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 15 text records in B152-B153; preserves one opaque map reveal event.",
        "inventory": {"identified_records": 16, "translated_records": 15, "blocks": {"152": 6, "153": 9}},
        "excluded_records": EXCLUDED, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records, {len(EXCLUDED)} control excluded")


if __name__ == "__main__":
    main()
