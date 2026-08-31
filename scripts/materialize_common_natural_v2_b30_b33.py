from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import iter_mesfile_records

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "work/analysis/common_clean_inventory.json"
BASE = ROOT / "out/raphael_natural_v2_pre_common_accepted_rollback.nds"
BATCH = ROOT / "translations/common_natural_v2_b30_b33_safe.json"
BLOCKED = ROOT / "translations/common_natural_v2_b30_b33_blocked.json"
AUDIT = ROOT / "work/analysis/common_b30_b33_entry_audit.json"
SOURCE_HASH = "ecb0806b6f36f9bf4164ae46084fbbc12d4122af66b6a8920814197463f19491"

SAFE = {
    (30, 2): "A detailed guide to glassmaking.",
    (30, 4): "A golden cat with a huge appetite for mice.",
    (30, 5): "A magic lime that never runs dry and quenches sailors' thirst at sea.",
    (30, 8): "An S-curved blade whose golden edge resembles a crescent moon.",
    (30, 9): "An ornate curved sword said to prove its bearer is a hero.",
    (30, 10): "A very heavy military sword made entirely of gold.",
    (30, 12): "The Sword of Betrayal, surrounded by an evil, haunted aura.",
    (30, 15): "A fine axe with a black, twisted haft and an eerie air.",
    (30, 16): "A great sword wielded by Kublai Khan, devastating in overhead strikes.",
    (30, 19): "A light, tough martial-arts uniform that can break an attacker's blade.",
    (30, 20): "Strong, breathable armor that keeps its wearer cool.",
    (31, 2): "Terrifying armor found after a knight sold his soul to a demon. Said to choose its wearer.",
    (31, 4): "Mystical leather gloves that protect the hands while raising and lowering sails.",
    (31, 7): "A collection of Arabian folk tales told by a young woman over one thousand and one nights.",
    (31, 8): "A book of painfully bad puns from around the world, supposedly compiled by a Japanese author.",
    (31, 10): "A strange bracelet whose carved angel is said to grant divine aid.",
    (31, 12): "A drum used on the battlefield to signal an army's advance or retreat.",
    (31, 13): "A necklace holding the spirit of Poseidon, god of the sea, and symbolizing courage.",
    (31, 14): "Caesar's account of nearly seven years of war in Gaul, written in the first century BC.",
    (31, 15): "A detailed record of Alexander's fourth-century-BC military campaigns.",
    (31, 18): "A superb plane with a diamond blade that never chips.",
    (31, 19): "The world's oldest medical text, compiled by the Hellenistic physician Herophilus.",
    (31, 21): "An adorable pink apron, though it may not suit every rough sailor.",
    (31, 22): "A small handmade mask invented to block foul odors in the animal room.",
    (32, 0): "Stylish rubber boots made with precious rubber to keep feet clean in the animal room.",
    (32, 3): "A famous Muslim merchant's perfectly accurate set of trading scales.",
    (32, 5): "A killer-whale figurehead whose fearsome pose is said to drive away even terrible storms.",
    (32, 6): "A white-whale figurehead found after the whale vanished. Ships bearing it are said to resist sinking.",
    (32, 8): "A graceful maiden figurehead whose beauty brings comfort and peace.",
    (32, 10): "A Madonna-and-child figurehead whose heavenly protection is said to ward off disease.",
    (32, 15): "Stained glass depicting a small flower in a vase, delicately rendered in colored glass.",
    (32, 16): "An ornate seventh-century gold crown from Silla, Korea's first unified kingdom.",
    (32, 19): "A light, soft silk robe made from exceptionally thin white fabric.",
    (32, 20): "A Goryeo celadon incense burner from Korea with an exquisite glaze.",
    (32, 22): "A solid-gold seal used on official documents by a king of ancient Aksum.",
    (33, 2): "An old map drawn on paper.",
    (33, 3): "An old map drawn on cloth.",
    (33, 6): "An old map etched into the blade of a large knife.",
    (33, 8): "A desert map used by caravans trading with the legendary city of Timbuktu.",
    (33, 10): "A map from ancient Cambodia depicting a central palace or temple.",
    (33, 12): "A map detailing travel between a ruined ancient city and a distant island.",
    (33, 13): "An Aztec pictorial codex recording the kingdom's cultural roots and map.",
    (33, 14): "A blank parchment of unknown purpose.",
    (33, 17): "A vivid, unusual pigment made from an unknown material.",
    (33, 20): "A diamond-bearing phantom crystal said to improve concentration.",
    (33, 21): "A treasured sword from a small eastern island, sharp enough to cut without touching.",
    (33, 22): "A siren figurehead modeled on the creature whose song wrecks ships. Its purpose is unknown.",
    (33, 44): "Could grow around the North Sea.",
    (33, 45): "Should thrive around the Mediterranean.",
    (33, 46): "May grow in Africa or the New World.",
    (33, 47): "Honey from Mediterranean flowers should be delicious.",
    (33, 48): "Shark fins are eaten in China, while shark eggs are eaten around the Black Sea.",
}

# These are source-safe, independently addressable descriptions, but their
# faithful drafts do not pass the shared-pair renderer without a warning or
# encoding failure.  Keep the reviewed English in the blocked inventory rather
# than waiving layout defects or weakening the translation.
LAYOUT_BLOCKED = {
    (30, 5), (30, 9), (30, 10), (30, 12), (30, 16), (30, 19),
    (31, 2), (31, 4), (31, 7), (31, 8), (31, 12), (31, 13), (31, 14),
    (31, 19), (31, 22),
    (32, 0), (32, 3), (32, 6), (32, 10), (32, 16), (32, 19), (32, 20),
    (32, 22),
    (33, 6), (33, 8), (33, 10), (33, 12), (33, 13), (33, 14), (33, 17),
    (33, 21), (33, 22), (33, 45), (33, 47), (33, 48),
}
EDITORIAL_DRAFTS = {key: SAFE[key] for key in LAYOUT_BLOCKED}
SAFE = {key: text for key, text in SAFE.items() if key not in LAYOUT_BLOCKED}

PADDING = {(31, 23), (33, 49)}
FIXED_OVERFLOW = {(33, index) for index in range(25, 44)}


def blocker_for(key: tuple[int, int]) -> tuple[str, str]:
    if key in PADDING:
        return "padding-only", "Padding-only segment; retained byte-identically."
    if key in FIXED_OVERFLOW:
        return (
            "fixed-allocation-overflow",
            "Single map-fragment description, but a faithful English sentence cannot fit its 35-byte allocation.",
        )
    if key in LAYOUT_BLOCKED:
        return (
            "single-message-layout-blocked",
            "Independently addressable, but its faithful draft does not pass shared-pair-live layout QA without a warning or encoding failure.",
        )
    return (
        "packed-multiple-entry",
        "The record contains multiple item descriptions without NUL delimiters; interior entry offsets are unproven.",
    )


def main() -> None:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    clean = {
        (int(row["block_index"]), int(row["segment_index"])): row
        for row in inventory["records"]
        if 30 <= int(row["block_index"]) <= 33
    }
    expected = {(block, index) for block, count in {30: 22, 31: 24, 32: 23, 33: 50}.items() for index in range(count)}
    if set(clean) != expected or set(SAFE) & (PADDING | FIXED_OVERFLOW):
        raise ValueError("block 30-33 classification inventory mismatch")
    common = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    if sha256(common).hexdigest() != SOURCE_HASH:
        raise ValueError("accepted COMMON hash mismatch")
    accepted = {
        (record.block_index, record.segment_index): record
        for record in iter_mesfile_records(common, include_non_japanese=True)
        if 30 <= record.block_index <= 33
    }
    if set(accepted) != expected:
        raise ValueError("accepted block 30-33 inventory mismatch")

    safe_records, blocked_records, audit_records = [], [], []
    for key in sorted(expected):
        block, index = key
        row, base = clean[key], accepted[key]
        if len(base.raw_bytes) != int(row["source_length"]):
            raise ValueError(f"{key}: accepted and clean allocation differ")
        row_id = f"DK4_MES_B{block:02d}_R{index:04d}"
        if key in SAFE:
            english = SAFE[key]
            safe_records.append({
                "id": row_id,
                "english": english + "{PAD}",
                "speaker": "Item description or trade adviser",
                "context": "A shared item, artifact, map, equipment, or cultivation description.",
                "source_meaning": english,
                "localization_note": "Faithfully condenses the clean Japanese description into natural American English within the original fixed allocation.",
                "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
            })
            classification, reason = "single-message", "One independently addressable description suitable for guarded fixed-dialogue QA."
        else:
            classification, reason = blocker_for(key)
            record = {
                "id": row_id,
                "source_length": row["source_length"],
                "source_hex": row["source_hex"],
                "japanese_markup": row["markup"],
                "classification": classification,
                "speaker": "Item description table",
                "context": "Shared item, artifact, map, or equipment description data.",
                "source_meaning": "The clean Japanese source is preserved in full; editorial segmentation is required before safe insertion.",
                "editorial_status": "source-reviewed; interior messages not yet independently addressable",
                "blocker": reason,
                "review": {"source": True, "context": True, "localization": False, "naturalness": False, "formatting": False},
            }
            if key in FIXED_OVERFLOW:
                record["editorial_english"] = "A fragment of an ancient map. Four pieces form a complete map."
                record["review"].update({"localization": True, "naturalness": True})
            elif key in EDITORIAL_DRAFTS:
                record["editorial_english"] = EDITORIAL_DRAFTS[key]
                record["editorial_status"] = "source/context/localization/naturalness reviewed; blocked on shared-pair-live formatting"
                record["review"].update({"localization": True, "naturalness": True})
            blocked_records.append(record)
        audit_records.append({
            "id": row_id,
            "block_index": block,
            "segment_index": index,
            "source_length": row["source_length"],
            "clean_source_hex": row["source_hex"],
            "accepted_source_hex": base.raw_bytes.hex().upper(),
            "japanese_markup": row["markup"],
            "classification": classification,
            "safe_to_replace": key in SAFE,
            "safety_reason": reason,
        })

    BATCH.write_text(json.dumps({
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/COMMON/MESFILE.DK4",
        "source_file_sha256": SOURCE_HASH,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "shared-pair-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-safe single-entry item, artifact, map, equipment, and cultivation descriptions in COMMON blocks 30-33",
        "blocked_records": [record["id"] for record in blocked_records],
        "records": safe_records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    BLOCKED.write_text(json.dumps({
        "format": "dk4-blocked-editorial-inventory-v1",
        "file_path": "/COMMON/MESFILE.DK4",
        "source_file_sha256": SOURCE_HASH,
        "blocks": [30, 31, 32, 33],
        "buildable": False,
        "records": blocked_records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    AUDIT.write_text(json.dumps({
        "format": "dk4-common-entry-safety-audit-v1",
        "file_path": "/COMMON/MESFILE.DK4",
        "blocks": [30, 31, 32, 33],
        "accepted_source_file_sha256": SOURCE_HASH,
        "classification_counts": {
            "single-message": len(SAFE),
            "packed-multiple-entry": sum(blocker_for(key)[0] == "packed-multiple-entry" for key in expected - set(SAFE)),
            "fixed-allocation-overflow": len(FIXED_OVERFLOW),
            "single-message-layout-blocked": len(LAYOUT_BLOCKED),
            "padding-only": len(PADDING),
        },
        "records": audit_records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote block 30-33 audit={len(audit_records)}, safe={len(safe_records)}, blocked={len(blocked_records)}")


if __name__ == "__main__":
    main()
