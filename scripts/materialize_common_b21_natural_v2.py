from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import iter_mesfile_records

ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "work/analysis/common_clean_inventory.json"
BASE_ROM = ROOT / "out/raphael_natural_v2_pre_common_accepted_rollback.nds"
AUDIT_OUT = ROOT / "work/analysis/common_b21_entry_audit.json"
BATCH_OUT = ROOT / "translations/common_natural_v2_b21_safe.json"
BLOCKED_OUT = ROOT / "translations/common_natural_v2_b21_blocked.json"
SOURCE_HASH = "ecb0806b6f36f9bf4164ae46084fbbc12d4122af66b6a8920814197463f19491"


EDITORIAL_ENGLISH = {
    2: "Yes! Enemy admiral hit! We won!",
    3: "Enemy admiral hit! Victory is ours!",
    4: "Enemy admiral hit! We won!",
    5: "Admiral, enemy admiral hit! We won!",
    6: "Enemy admiral hit! We won!",
    7: "Enemy admiral hit! Victory is ours!",
    8: "%s! Duel me now!",
    10: "%s! Duel me now!",
    11: "%s! Duel me!",
    13: "Challenge accepted!",
    17: "Grr... Next time, you're dead!",
    18: "Next time, you'll lose!",
    19: "Damn! Next time, you lose!",
    21: "%s, run! Everyone, cover them!",
    22: "%s, run! We'll protect you!",
    24: "Too slow! Eyes on me!",
    25: "Come on! Are you trying?",
    27: "Whoa! Missed...",
    28: "Damn... Slipped!",
    29: "Missed! Got too cocky...",
    30: "Ugh! So annoying!",
    32: "Whoa! They dodged it!",
    33: "Ugh... No good at combat...",
    34: "Admiral, run! Everyone, cover him!",
    35: "Run, Admiral! We'll cover!",
    36: "Admiral, run! Everyone, cover him!",
    37: "Admiral, run! Men, cover him!",
    38: "Run, Admiral! Everyone, cover him!",
    39: "Admiral, run! Everyone, cover him!",
    40: "Admiral, leave the cover to us! Run!",
    41: "Behold my twin blades!",
    42: "Playtime is over!",
    43: "Afterimage! Twin Shadow Array!",
    44: "Such a dull attack won't work!",
    47: "You're done!",
    48: "Aaaah! You're going flying!",
    49: "So many openings!",
    50: "Taoist arts! Hyaah!",
    51: "%s has surrendered!",
    53: "%s has surrendered!",
    54: "%s wants to surrender!",
    55: "%s has surrendered!",
    56: "Enemy flagship sunk!",
    57: "Lead ship sunk!",
    58: "Lead ship sunk!",
    59: "Lead ship sunk!",
    60: "The enemy flagship sank!",
    62: "Admiral, we're hit! Taking water!",
    63: "Admiral, ship's done! Taking water!",
    64: "Admiral, we're done! Taking water!",
    65: "Admiral, this ship won't hold! Taking water!",
    66: "Enemy crew defeated. Ship captured!",
    67: "Admiral! Enemy crew beaten. Ship captured!",
    68: "Enemy crew down. Lead ship captured!",
    69: "We beat the enemy crew and took their ship!",
    70: "Enemy crew defeated. Ship captured!",
    71: "All sailors are dead! Abandon ship!",
    72: "Crew dead! Admiral, abandon ship!",
    73: "Crew's down! Admiral, change ships!",
    74: "The crew is falling! Admiral, abandon ship!",
    75: "The sailors are dying! Admiral, abandon ship!",
    76: "Crew's down! Admiral, change ships!",
    77: "Resistance is pointless. Surrender peacefully.",
    78: "Resistance is useless. Surrender.",
    79: "There's no point fighting! Just surrender!",
    80: "Resistance is useless! Surrender!",
    81: "You can't win! Surrender already!",
    82: "Resistance is useless. Surrender!",
    83: "No point fighting! Just surrender!",
    84: "You cannot win! Surrender immediately!",
    85: "No more lives wasted... We surrender.",
}


PACKED_DRAFTS = {
    0: [
        "The nearby fleet under %s will lend us a hand!",
        "The nearby fleet under %s says they'll help us!",
    ],
    1: [
        "The nearby fleet under %s will reinforce us!",
        "Admiral, we shot the enemy admiral! Victory is ours!",
    ],
    9: [
        "%s! Let us settle this honorably in a duel!",
        "Ah, %s! Face me in a duel!",
        "%s! Let us settle this with a duel!",
        "Well, if it isn't %s! Fight me one-on-one!",
    ],
    12: [
        "So, it's %s! Let us settle this in a duel!",
        "Interesting. I accept your challenge!",
    ],
    14: ["All right! I accept!", "Fine! I accept your challenge!"],
    15: [
        "Interesting! I accept!",
        "All right! I'll do it!",
        "Next time won't go this way!",
    ],
    16: ["You won't escape next time!", "I won't let you escape next time!"],
    20: [
        "%s, run! Everyone, provide cover!",
        "%s, hurry and run! We'll all cover you!",
        "%s, hurry and run! Everyone, provide cover!",
        "%s, get away! Men, provide cover!",
    ],
    23: [
        "Perfect!",
        "...I saw through it!",
        "That kind of attack won't work on me!",
    ],
    26: ["There! A sure hit!", "Yay, I hit!", "Yes, right there!"],
    31: ["Damn, I rushed it!", "Ugh... It's nothing. This isn't over yet."],
    45: [
        "That swordplay is child's play compared with Gerhard's training!",
        "Do you think a brute-force swing like that will work? Take this!",
    ],
    46: [
        "Ha ha ha! It's showtime!",
        "Hey, hey! What's wrong? I'm not even serious yet!",
        "I'll show you the sword I honed on the battlefield!",
    ],
    52: ["Admiral! %s has surrendered!", "%s has surrendered!"],
    61: [
        "Enemy flagship destroyed!",
        "Admiral, our flagship is lost! We can't stop the flooding!",
    ],
}


SOURCE_MEANING_OVERRIDES = {
    2: "The speaker celebrates shooting the enemy admiral and winning.",
    3: "The speaker reports successfully shooting the enemy admiral and declares victory.",
    4: "The speaker reports a successful shot on the enemy admiral and celebrates victory.",
    5: "The speaker tells the admiral that the enemy admiral was successfully shot and declares victory.",
    6: "The speaker says their shot hit the enemy admiral and celebrates their side's victory.",
    7: "The speaker reports shooting the enemy admiral and declares their side victorious.",
    8: "The speaker recognizes %s and challenges them to a one-on-one duel.",
    10: "The speaker recognizes %s and proposes settling matters in a one-on-one duel.",
    11: "The speaker recognizes %s and challenges them to a duel.",
    13: "The speaker finds the challenge interesting and accepts it.",
    17: "The defeated speaker growls and threatens the opponent's life next time.",
    18: "The defeated speaker promises to defeat the opponent next time.",
    19: "The defeated speaker curses and says things will be different next time.",
    21: "The speaker tells %s to flee and orders everyone to provide cover.",
    22: "The speaker tells %s to flee and says everyone will protect them.",
    24: "The speaker calls the attack naive and asks where the opponent is looking.",
    25: "The speaker taunts the opponent and asks whether they are even trying.",
    27: "The speaker cries out and admits the attempt failed.",
    28: "The speaker realizes they let their guard down.",
    29: "The speaker missed and admits getting carried away.",
    30: "The speaker complains in frustration.",
    32: "The speaker cries out because the opponent dodged.",
    33: "The speaker groans and admits fighting is not their strength.",
    41: "The speaker promises to demonstrate their dual-wielding technique.",
    43: "The speaker invokes an afterimage technique named White Tree Sword Style: Twin Shadow Formation.",
    44: "The speaker asks whether the opponent thought such a monotonous attack would work.",
    47: "The speaker declares the finishing blow.",
    48: "The speaker screams and says they will throw the opponent away.",
    49: "The speaker points out that the opponent is full of openings.",
    50: "The speaker invokes Taoist arts and gives a battle cry.",
    60: "The speaker says the enemy flagship has sunk.",
    62: "The speaker tells the admiral that the flagship was hit and the flooding cannot be stopped.",
    63: "The speaker tells the admiral the flagship is finished and the flooding cannot be stopped.",
    64: "The speaker tells the admiral they are done for and the water will not stop.",
    65: "The speaker tells the admiral the flagship cannot hold and the flooding cannot be stopped.",
    66: "The speaker reports defeating every sailor on the enemy flagship and capturing it.",
    67: "The speaker tells the admiral they defeated the enemy flagship's crew and captured the ship.",
    68: "The speaker reports defeating the enemy flagship's entire crew and capturing it.",
    69: "The speaker reports beating the enemy flagship's crew and taking the whole ship.",
    70: "The speaker reports defeating the enemy flagship's entire crew and capturing the ship.",
    71: "The speaker reports that all sailors are dead and orders an evacuation to another ship.",
    72: "The speaker reports all sailors dead and urgently orders the admiral to another ship.",
    73: "The speaker says the whole crew is down and urges the admiral to flee to another ship.",
    74: "The speaker says the crew is falling one after another and urges the admiral to abandon ship.",
    75: "The speaker says sailors are dying one after another and tells the admiral to abandon ship.",
    76: "The speaker says the whole crew is down and tells the admiral to flee to another ship.",
    77: "The speaker says further fighting is meaningless and asks the enemy to surrender peacefully.",
    78: "The speaker says further resistance is meaningless and orders a peaceful surrender.",
    79: "The speaker says further fighting is pointless and asks the enemy to surrender peacefully.",
    80: "The speaker says further resistance is meaningless and orders the enemy to surrender peacefully.",
    81: "The speaker says the enemy has no chance of winning and orders them to surrender quickly.",
    82: "The speaker says further resistance is meaningless and commands the enemy to surrender.",
    83: "The speaker says further fighting is pointless and asks the enemy to surrender peacefully.",
    84: "The speaker says the enemy cannot win and advises surrendering as soon as possible.",
    85: "The speaker refuses to let more comrades die needlessly and surrenders the ship.",
}


def context_for(index: int) -> str:
    if index <= 7:
        return "A shared battle report announces allied help or a successful shot against the enemy admiral."
    if index <= 19:
        return "A named combatant issues, accepts, or answers a one-on-one duel challenge."
    if index <= 40:
        return "A battle voice warns an admiral to flee, provides cover, or reacts to a shot."
    if index <= 50:
        return "A named combatant delivers a special attack or evasive battle line."
    if index <= 70:
        return "A shared naval battle report announces surrender, a sunk flagship, flooding, or capture."
    return "A shared naval battle voice orders evacuation or demands the enemy's surrender."


def main() -> None:
    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    clean_rows = {int(r["segment_index"]): r for r in inventory["records"] if int(r["block_index"]) == 21}
    if set(clean_rows) != set(range(86)):
        raise ValueError("clean block 21 inventory is not the expected 86 records")
    mesfile = NdsImage.open(BASE_ROM).read_file("/COMMON/MESFILE.DK4")
    if sha256(mesfile).hexdigest() != SOURCE_HASH:
        raise ValueError("accepted baseline MESFILE hash does not match the required source lock")
    baseline_rows = {
        r.segment_index: r
        for r in iter_mesfile_records(mesfile, include_non_japanese=True)
        if r.block_index == 21
    }
    if set(baseline_rows) != set(range(86)):
        raise ValueError("accepted block 21 is not the expected 86 records")
    single, packed = set(EDITORIAL_ENGLISH), set(PACKED_DRAFTS)
    if single & packed or single | packed != set(range(86)):
        raise ValueError("classification does not cover block 21 exactly once")

    audit_records, safe_records, blocked_records = [], [], []
    for index in range(86):
        clean, baseline = clean_rows[index], baseline_rows[index]
        if len(baseline.raw_bytes) != int(clean["source_length"]):
            raise ValueError(f"record {index}: accepted and clean allocations differ")
        english = EDITORIAL_ENGLISH.get(index)
        drafts = PACKED_DRAFTS.get(index)
        meaning = " / ".join(drafts) if drafts else SOURCE_MEANING_OVERRIDES.get(index, english)
        row_id = f"DK4_MES_B21_R{index:04d}"
        is_safe = index in single
        audit_records.append({
            "id": row_id,
            "block_index": 21,
            "segment_index": index,
            "source_offset": clean["source_offset"],
            "source_length": clean["source_length"],
            "clean_source_hex": clean["source_hex"],
            "accepted_source_hex": baseline.raw_bytes.hex().upper(),
            "japanese_markup": clean["markup"],
            "accepted_markup_for_structure_only": baseline.text,
            "accepted_differs_from_clean": baseline.raw_bytes.hex().upper() != clean["source_hex"],
            "classification": "single-message" if is_safe else "packed-multiple-entry",
            "source_meaning": meaning,
            "safe_to_replace": is_safe,
            "safety_reason": (
                "One independently addressable Japanese message selected for guarded fixed-dialogue QA."
                if is_safe
                else "Multiple adjacent messages appear without NUL delimiters; their interior entry offsets are unproven."
            ),
        })
        record = {
            "id": row_id,
            "speaker": "Multiple shared battle voices" if drafts else "Shared battle voice or named combatant",
            "context": context_for(index),
            "source_meaning": meaning,
        }
        if is_safe:
            record.update({
                "english": english + "{PAD}",
                "localization_note": "Uses concise, idiomatic American English while preserving the battle outcome, intent, tone, and runtime substitutions.",
                "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")},
            })
            safe_records.append(record)
        else:
            record.update({
                "source_length": clean["source_length"],
                "japanese_markup": clean["markup"],
                "draft_messages": drafts,
                "blocker": "Multiple concatenated messages have unproven interior entry offsets.",
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": False},
            })
            blocked_records.append(record)

    AUDIT_OUT.write_text(json.dumps({
        "format": "dk4-common-entry-safety-audit-v1",
        "file_path": "/COMMON/MESFILE.DK4",
        "block_index": 21,
        "source": "work/analysis/common_clean_inventory.json generated from work/clean.nds",
        "accepted_source_file_sha256": SOURCE_HASH,
        "classification_counts": {"single-message": len(single), "packed-multiple-entry": len(packed), "padding-only": 0, "likely-identifier": 0},
        "replacement_counts": {"safe_to_replace": len(single), "blocked": len(packed)},
        "records": audit_records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    BATCH_OUT.write_text(json.dumps({
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/COMMON/MESFILE.DK4",
        "source_file_sha256": SOURCE_HASH,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "shared-pair-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Independently addressable Japanese records in shared MESFILE block 21",
        "blocked_packed_records": [f"DK4_MES_B21_R{i:04d}" for i in sorted(packed)],
        "blocked_records": [r["id"] for r in blocked_records],
        "records": safe_records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    BLOCKED_OUT.write_text(json.dumps({
        "format": "dk4-blocked-editorial-inventory-v1",
        "file_path": "/COMMON/MESFILE.DK4",
        "source_file_sha256": SOURCE_HASH,
        "block_index": 21,
        "buildable": False,
        "records": blocked_records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote block-21 audit={len(audit_records)}, safe={len(safe_records)}, blocked={len(blocked_records)}")


if __name__ == "__main__":
    main()
