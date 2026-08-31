from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import iter_mesfile_records

ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "work/analysis/common_clean_inventory.json"
BASE_ROM = ROOT / "out/raphael_natural_v2_pre_common_accepted_rollback.nds"
AUDIT_OUT = ROOT / "work/analysis/common_b15_entry_audit.json"
BATCH_OUT = ROOT / "translations/common_natural_v2_b15_safe.json"
BLOCKED_OUT = ROOT / "translations/common_natural_v2_b15_blocked.json"
SOURCE_HASH = "ecb0806b6f36f9bf4164ae46084fbbc12d4122af66b6a8920814197463f19491"


EDITORIAL_ENGLISH = {
    0: "Admiral, we checked on %s.",
    1: "I looked into %s.",
    2: "Admiral, I investigated %s.",
    3: "Admiral, I obtained information on %s.",
    4: "I checked up on %s.",
    5: "Admiral, I obtained information about %s.",
    7: "%s, %s fought %s's fleet, but they were defeated.",
    8: "%s, %s attacked %s. What a terrible thing to do.",
    10: "Today is a blessed day. Come, let us pray together.",
    11: "Hm? Have you come to take part in the rite?",
    13: "Aaaah... Aaaaah!",
    14: "What?!",
    15: "Ooooh, aaah... Incomprehensible chanting!",
    16: "What?",
    20: "You've come to take part in the rite of %s?",
    21: "Go on in.",
    22: "What brings you to these ruins? If you have no business here, leave at once.",
    23: "Haaaaaah!",
    24: "What?! Haaaaah! Ooooh! Incomprehensible chanting!",
    26: "Dance?",
    27: "What dance?",
    28: "Cast aside all distractions. Forget everything, body and soul, and surrender to this gentle music.",
    29: "Release the heat rising from deep within you. Yes, that's it.",
    30: "We will now begin the fast. Are you prepared?",
    32: "Now, pray in silence.",
    34: "...",
    36: "Hurry. We must return before sunset, or wild beasts will devour us.",
    37: "You need %s coins, but you don't have enough.",
    38: "It costs %s coins. Is that all right?",
    39: "The officers here will recover their health and morale.",
    40: "With a carpenter aboard, you can repair damaged ships.",
    43: "With a purser aboard, you can bargain and corner markets.",
    44: "Admiral, let me help.",
    45: "Admiral, {MACRO:I}C will help with the refit too.",
    46: "Admiral, let me help with the refit.",
    51: "Extra Armor 2 further increases durability, but slightly reduces speed.",
    52: "A bow gun lets you fire forward, though it has low power.",
    53: "A stern gun lets you fire behind you, though it has low accuracy.",
    54: "A ram lets you strike the side of an enemy ship.",
    55: "A marine officer increases boarding power. You can install up to four quarters.",
    57: "A cargo hold carries trade goods. You can install up to five holds.",
    58: "You can add a cargo hold here, but it will slightly reduce speed.",
    59: "You can add a ram or bow gun here. Medium and larger ships can also add a split sail.",
    60: "You can equip Extra Armor here.",
    62: "You can change the type of cannon installed on the ship.",
    63: "Lateen sails perform well against the wind, but you cannot mount a square sail behind one.",
    66: "Admiral! We found a city!",
}

# These records are both independently addressable and encodable from the
# accepted baseline. Most other single-message records contain a literal ASCII
# `I` in the legacy accepted bytes. The dialogue codec necessarily interprets
# that byte as the runtime I macro, so replacing those records through the
# guarded encoder would either preserve a false command or remove a purported
# command. They remain editorial-only until that baseline ambiguity is mapped.
SAFE_BUILD = {0, 13, 14, 16, 21, 23, 26, 27, 32, 34, 44, 66}

SOURCE_GLOSS_OVERRIDES = {
    0: "The companion tells the admiral that they investigated the named subject.",
    27: "The speaker asks what the other person means by dancing.",
    44: "The companion tells the admiral that they will also help with the ship modification.",
}


PACKED_DRAFTS = {
    6: ["We don't have enough money.", "%s, %s fought %s's fleet and won a splendid victory."],
    9: ["%s, %s attacked %s, but the raid failed miserably. Serves them right.", "Oh, are you leaving already?"],
    12: ["Come, let us sing a song of joy.", "Kneel there. Now then... Ahem."],
    17: ["Huh? What?", "Then help us prepare at once.", "Help?", "Did you say help?"],
    18: ["Help with what?", "Help?", "Come, don't stop working!"],
    19: ["(What is going on?)", "God watches all your deeds."],
    25: ["You are pilgrims, I see. Line up and offer your prayers in turn.", "Then join the circle and dance."],
    31: ["What?!", "What did you say?!", "Nooo!", "(I suppose I have no choice...)"],
    33: ["(Grrrr...)", "(Grrrr...)", "(I'm starving...)"],
    35: ["We will climb the sacred mountain to draw holy water. Is that understood?", "Then follow me. Do not fall behind."],
    41: [
        "With a doctor aboard, you can cure illnesses affecting officers and sailors.",
        "With a cook aboard, you conserve water and food, and sailors tire less easily.",
        "The officers here recover their morale and help sailors tire less easily.",
        "With a keeper aboard, food is consumed more slowly.",
    ],
    42: [
        "With a missionary aboard, sailors' dissatisfaction is relieved. You can also distribute trade goods in the square.",
        "With a strategist aboard, you can devise plots in taverns.",
    ],
    47: ["Admiral, I'll lend a hand.", "Admiral, I'll help with the refit."],
    48: [
        "Admiral, I'll help with the refit.",
        "Admiral, let me help with the refit...",
        "If they help, I'll cut the refit cost by %s%.",
        "Which ship do you want to rename?",
        "Then give it any name you like.",
    ],
    49: ["Which ship do you want to refit?", "It'll take %s days."],
    50: [
        "A split sail improves square-sail performance and increases speed with the wind.",
        "A jigger spanker improves fore-and-aft performance and increases speed against the wind.",
        "Extra armor increases durability but slightly reduces speed.",
    ],
    56: [
        "A gunner makes cannon fire faster. You can install up to four quarters.",
        "This room stores water and food.",
    ],
    61: [
        "You can add a stern gun here. Large ships can instead add a jigger spanker.",
        "You can mount a figurehead you own here.",
    ],
    64: [
        "A topsail improves square-sail performance and increases speed with the wind.",
        "Square sails perform well with the wind, but you cannot mount a lateen sail ahead of one.",
        "A staysail improves fore-and-aft performance and increases speed against the wind.",
        "This sail improves both fore-and-aft and square-sail performance.",
    ],
    65: [
        "Admiral! A city is in sight!",
        "Admiral! I can see a city!",
        "Admiral! There's a city!",
        "Admiral! City ahead!",
        "Admiral, that appears to be a city.",
    ],
}


CONTEXTS = {
    **{index: "A shared companion reports intelligence about a named target." for index in range(10)},
    **{index: "A ritual or ruins encounter presents a spoken response or instruction." for index in range(10, 37)},
    37: "A facility attendant reports that the displayed fee exceeds the party's funds.",
    38: "A facility attendant asks whether to pay the displayed fee.",
    39: "A facility tutorial explains recovery effects for officers.",
    40: "A ship tutorial explains the carpenter's repair benefit.",
    41: "A packed tutorial record contains several independently addressed crew-role explanations.",
    42: "A packed tutorial record contains missionary and strategist explanations.",
    43: "A tutorial explains the purser's commercial benefits.",
    **{index: "A shipyard refit interaction uses one or more companion or attendant messages." for index in range(44, 50)},
    **{index: "A shipyard tutorial explains one or more ship components or installation points." for index in range(50, 65)},
    65: "A packed record contains five companion variants announcing a city sighting.",
    66: "A youthful companion announces a city sighting.",
    67: "A one-byte padding segment contains no user-facing message.",
}


def source_meaning(index: int, english: str | None, drafts: list[str] | None) -> str:
    if index in SOURCE_GLOSS_OVERRIDES:
        return SOURCE_GLOSS_OVERRIDES[index]
    if drafts:
        return " / ".join(drafts)
    if index == 67:
        return "A single ASCII space used as padding; it has no linguistic content."
    assert english is not None
    return english.replace("{MACRO:I}", "the runtime I substitution")


def main() -> None:
    clean_inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    clean_rows = {
        int(row["segment_index"]): row
        for row in clean_inventory["records"]
        if int(row["block_index"]) == 15
    }
    if set(clean_rows) != set(range(68)):
        raise ValueError("clean block 15 inventory is not the expected 68 records")

    baseline_mesfile = NdsImage.open(BASE_ROM).read_file("/COMMON/MESFILE.DK4")
    if sha256(baseline_mesfile).hexdigest() != SOURCE_HASH:
        raise ValueError("accepted baseline MESFILE hash does not match the required source lock")
    baseline_rows = {
        record.segment_index: record
        for record in iter_mesfile_records(baseline_mesfile, include_non_japanese=True)
        if record.block_index == 15
    }
    if set(baseline_rows) != set(range(68)):
        raise ValueError("baseline block 15 is not the expected 68 records")

    packed = set(PACKED_DRAFTS)
    single = set(EDITORIAL_ENGLISH)
    if single & packed or single | packed | {67} != set(range(68)):
        raise ValueError("classification does not cover block 15 exactly once")

    audit_records = []
    batch_records = []
    blocked_records = []
    for index in range(68):
        clean = clean_rows[index]
        baseline = baseline_rows[index]
        if len(baseline.raw_bytes) != int(clean["source_length"]):
            raise ValueError(f"record {index}: accepted and clean allocations differ")
        english = EDITORIAL_ENGLISH.get(index)
        drafts = PACKED_DRAFTS.get(index)
        classification = "single-message" if index in single else "packed-multiple-entry" if index in packed else "padding-only"
        meaning = source_meaning(index, english, drafts)
        row_id = f"DK4_MES_B15_R{index:04d}"
        audit_records.append(
            {
                "id": row_id,
                "block_index": 15,
                "segment_index": index,
                "source_offset": clean["source_offset"],
                "source_length": clean["source_length"],
                "clean_source_hex": clean["source_hex"],
                "accepted_source_hex": baseline.raw_bytes.hex().upper(),
                "accepted_markup_for_structure_only": baseline.text,
                "accepted_differs_from_clean": baseline.raw_bytes.hex().upper() != clean["source_hex"],
                "japanese_markup": clean["markup"],
                "classification": classification,
                "source_meaning": meaning,
                "safe_to_replace": index in SAFE_BUILD,
                "safety_reason": (
                    "One independently addressable message that passes the accepted-source fixed-dialogue encoder."
                    if index in SAFE_BUILD
                    else "The message is independently addressable, but legacy ASCII in the accepted source is parsed as a runtime I macro; removing or preserving that apparent command is unsafe without runtime evidence."
                    if index in single
                    else "Multiple adjacent messages appear without NUL delimiters; their interior entry offsets are unproven."
                    if index in packed
                    else "Structural padding has no user-facing text to translate."
                ),
            }
        )
        if index in SAFE_BUILD:
            batch_records.append(
                {
                    "id": row_id,
                    "english": english + "{PAD}",
                    "speaker": "Shared companion or facility attendant",
                    "context": CONTEXTS[index],
                    "source_meaning": meaning,
                    "localization_note": "Uses concise idiomatic American English while preserving the source intent and every runtime substitution.",
                    "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
                }
            )
        elif index in packed or index in single:
            blocked_records.append(
                {
                    "id": row_id,
                    "source_length": clean["source_length"],
                    "japanese_markup": clean["markup"],
                    "draft_messages": drafts or [english],
                    "speaker": "Multiple shared voices or facility attendants" if drafts else "Shared companion or facility attendant",
                    "context": CONTEXTS[index],
                    "source_meaning": meaning,
                    "blocker": (
                        "The record contains multiple concatenated messages with unproven interior entry offsets. Replacing it as one paragraph could move or erase alternate entry points."
                        if drafts
                        else "Legacy ASCII in the accepted source is parsed as a runtime I macro by the guarded dialogue codec. The clean Japanese source does not establish a matching command, so preserving or deleting it would be unsafe without runtime mapping."
                    ),
                    "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": False},
                }
            )

    AUDIT_OUT.write_text(
        json.dumps(
            {
                "format": "dk4-common-entry-safety-audit-v1",
                "file_path": "/COMMON/MESFILE.DK4",
                "block_index": 15,
                "source": "work/analysis/common_clean_inventory.json generated from work/clean.nds",
                "accepted_source_file_sha256": SOURCE_HASH,
                "classification_counts": {
                    "single-message": len(single),
                    "packed-multiple-entry": len(packed),
                    "padding-only": 1,
                    "likely-identifier": 0,
                },
                "replacement_counts": {
                    "safe_to_replace": len(SAFE_BUILD),
                    "blocked_accepted_source_ambiguity": len(single - SAFE_BUILD),
                    "blocked_packed_multiple_entry": len(packed),
                    "not_applicable_padding": 1,
                },
                "records": audit_records,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    BATCH_OUT.write_text(
        json.dumps(
            {
                "format": "dk4-ilnk-translation-batch-v1",
                "file_path": "/COMMON/MESFILE.DK4",
                "source_file_sha256": SOURCE_HASH,
                "encoder": "dialogue-fixed-v1",
                "dialogue_profile": "shared-pair-live",
                "translation_policy": "natural-dialogue-v2",
                "target_locale": "en-US",
                "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
                "scope": "Independently addressable, structurally safe records in shared MESFILE block 15",
                "blocked_packed_records": [f"DK4_MES_B15_R{index:04d}" for index in sorted(packed)],
                "blocked_accepted_source_records": [f"DK4_MES_B15_R{index:04d}" for index in sorted(single - SAFE_BUILD)],
                "records": batch_records,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    BLOCKED_OUT.write_text(
        json.dumps(
            {
                "format": "dk4-blocked-editorial-inventory-v1",
                "file_path": "/COMMON/MESFILE.DK4",
                "source_file_sha256": SOURCE_HASH,
                "block_index": 15,
                "buildable": False,
                "records": blocked_records,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {AUDIT_OUT.relative_to(ROOT)} ({len(audit_records)} records)")
    print(f"wrote {BATCH_OUT.relative_to(ROOT)} ({len(batch_records)} safe records)")
    print(f"wrote {BLOCKED_OUT.relative_to(ROOT)} ({len(blocked_records)} blocked records)")


if __name__ == "__main__":
    main()
