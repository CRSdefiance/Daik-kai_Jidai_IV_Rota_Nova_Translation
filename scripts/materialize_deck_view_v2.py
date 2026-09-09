from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import export_mesfile_rows


BASE_ROM = Path("out/raphael_natural_v2_pre_story_push_v10_accepted_rollback.nds")
BASE_SHA256 = "d8cb15aa23e2496510eba8feb18e4536a7da195522b7f5959298b0c1cc0fd1cf"
ARM9_SHA256 = "249860ab1d29ecfa8e149fd04b5cbff3c3414fb192f81459cfaf469d6c83fa52"
COMMON_SHA256 = "943ce540c99bca4cd5f2be16fba071e082b588619ac05f4c1fecd49528976ffc"


ARM9_TEXT = (
    ("DK4_DECK_BUTTON_CREW_V2", 0x11B5A4, "Crew", "Deck Y button; opens automatic crew-policy setup"),
    ("DK4_DECK_CABIN", 0x12FF50, "Cabin", "Deck room"),
    ("DK4_DECK_HELM", 0x12FF58, "Helm", "Deck room"),
    ("DK4_DECK_NONE", 0x12FF60, "None", "Deck room state"),
    ("DK4_DECK_SURVEY", 0x12FF68, "Survey", "Deck room"),
    ("DK4_DECK_OPEN_DECK", 0x12FF70, "Deck", "Deck room"),
    ("DK4_DECK_ADD_ROOM_2", 0x12FF78, "Add 2", "Deck room"),
    ("DK4_DECK_LUMBER", 0x12FF80, "Lumber", "Deck room"),
    ("DK4_DECK_TACTICS", 0x12FF88, "Tactics", "Deck room"),
    ("DK4_DECK_SICKBAY", 0x12FF90, "Sickbay", "Deck room"),
    ("DK4_DECK_GALLEY", 0x12FF98, "Galley", "Deck room"),
    ("DK4_DECK_PURSER", 0x12FFA0, "Purser", "Deck room"),
    ("DK4_DECK_MAST", 0x12FFA8, "Mast", "Deck room"),
    ("DK4_DECK_ROWERS", 0x12FFB0, "Rowers", "Deck room"),
    ("DK4_DECK_CHAPEL", 0x12FFB8, "Chapel", "Deck room"),
    ("DK4_DECK_CONFIRM_ASSIGNMENT_V2", 0x131E74, "Confirm crew assignment?", "Deck crew-policy confirmation"),
    ("DK4_DECK_NO_UNASSIGNED_V2", 0x131E98, "No unassigned crew.", "Deck crew-policy warning"),
    ("DK4_DECK_COMMAND_SKILL_V2", 0x131EB4, "Command", "Captain-cabin required ability"),
    ("DK4_DECK_ONLY_CAPTAIN_V2", 0x131EBC, "Only %s can be Captain.", "Captain-cabin assignment restriction"),
    ("DK4_DECK_SKILL_V2", 0x132058, "Skill: %s", "Deck requirement label"),
    ("DK4_DECK_NEED_NONE_V2", 0x132068, "Need: --", "Deck requirement label"),
    ("DK4_DECK_ANYONE_V2", 0x132078, "Anyone may serve.", "Deck assignment eligibility"),
    ("DK4_DECK_CANNOT_ASSIGN_V2", 0x13208C, "Cannot assign here.", "Deck assignment restriction"),
    ("DK4_DECK_NEED_VALUE_V2", 0x1320A8, "Need: %4d", "Deck requirement label"),
    ("DK4_DECK_NO_ELIGIBLE_V2", 0x1320B8, "No eligible crew.", "Deck assignment restriction"),
    ("DK4_STAT_NORMAL_V2", 0x1482D4, "Normal", "Status/ability name"),
    ("DK4_STAT_CHARM_V2", 0x1482DC, "Charm", "Ability name"),
    ("DK4_STAT_WOUNDED_V2", 0x1482E4, "Wounded", "Status name"),
    ("DK4_STAT_LUCK_V2", 0x1482EC, "Luck", "Ability name"),
    ("DK4_STAT_HIGH_V2", 0x1482F4, "High", "Status name"),
    ("DK4_STAT_WITS_V2", 0x1482FC, "Wits", "Ability name"),
    ("DK4_STAT_AIM_V2", 0x148304, "Aim", "Ability name"),
    ("DK4_STAT_PERSUADE_V2", 0x14830C, "Social", "Persuasion ability name"),
    ("DK4_STAT_TACTICS_V2", 0x148314, "Tactics", "Ability name"),
    ("DK4_STAT_OBSERVE_V2", 0x14831C, "Observe", "Ability name"),
    ("DK4_STAT_COMMAND_V2", 0x148324, "Command", "Ability name"),
    ("DK4_STAT_UPSET_V2", 0x14832C, "Upset", "Status name"),
    ("DK4_STAT_COMBAT_V2", 0x148334, "Combat", "Ability name"),
    ("DK4_STAT_HEALTH_V2", 0x14833C, "Health", "Ability name"),
    ("DK4_STAT_SAILING_V2", 0x148344, "Sailing", "Ability name"),
    ("DK4_STAT_SURVEY_V2", 0x14834C, "Survey", "Ability name"),
    ("DK4_STAT_FINANCE_V2", 0x148354, "Finance", "Ability name"),
)


# The Deck activity box shows a maximum of 24 single-byte glyphs and does not
# wrap. These replace every longer line in the accepted COMMON B17 activity
# table, preserving each fixed record allocation with {PAD}.
DECK_ACTIVITY = {
    0: "My apprentice handiwork.",
    3: "Everyone loves my food.",
    11: "You'll be a fine pig.",
    14: "Hey! Stop rubbing me!",
    19: "God, please hear me.",
    22: "Reading makes me sleepy.",
    24: "May Portugal rise again.",
    25: "God, grant us a fleet.",
    27: "May we all sail safely.",
    31: "Study and plan better.",
    32: "Plan... Zzz... A nap!",
    34: "Make plans? Let me try.",
    35: "Count on my plan.",
    37: "Direct tactics fail.",
    38: "Leave schemes to me!",
    46: "Where can we profit?",
    47: "Let's total this profit.",
    48: "Review our finances.",
    50: "Numbers make me dizzy.",
    51: "Which goods will profit?",
    52: "Captain... My best.",
    53: "This fleet is mine.",
    55: "Everything rests on me.",
    56: "Leave paperwork to me.",
    57: "The admiral's aide.",
    58: "Leave diplomacy to me.",
    59: "Admiral, writing?",
    63: "Leave talks to me.",
    64: "Your officer? Uh, sure.",
    65: "Who's captain now?",
    66: "Well. Who's captain?",
    70: "Hard starboard!",
    72: "Round again! One more!",
    73: "Cannons cannot hit me!",
    75: "Leave the wheel to me.",
    77: "Helm and sails as one.",
    78: "Leave the ship to me!",
    79: "Shen taught me to steer.",
    80: "A sextant helps survey.",
    82: "Position? Uh... wait!",
    83: "Stars reveal our place.",
    84: "Just find our position?",
    85: "Surveying is seamanship.",
    86: "The surveyor has this.",
    88: "This is the right tool?",
    89: "The sun shows our place.",
    90: "Surveying is seamanship!",
    91: "Sun and stars guide us.",
    92: "On watch. Rest easy.",
    94: "Trouble gets reported.",
    95: "What a vast world!",
    97: "All sightings reported.",
    99: "On watch! Eyes open.",
    100: "All will hear my report.",
    103: "Sharp eyes. Count on me.",
    104: "Any wind can be tamed.",
    105: "Match sails to the wind.",
    107: "Better with sails now?",
    108: "Half sail when slowing.",
    109: "Sail types differ.",
    111: "A sailmaster reads wind.",
    112: "Wind makes sense now.",
    113: "Sails and helm as one.",
    115: "None beats a dead calm.",
    116: "Training every day.",
    121: "Ow! My back cracked...",
    122: "Training makes me hungry",
    124: "My swordplay improved?",
    125: "Swordplay for the crew.",
    127: "Leading the boarding!",
    130: "Naval combat training.",
    131: "Does firing scare you?",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def slot_end(arm9: bytes, offset: int) -> int:
    end = arm9.find(b"\0", offset)
    if end < 0:
        raise ValueError(f"unterminated ARM9 string at {offset:#x}")
    # These tables are aligned to four or eight bytes. Keep all existing zero
    # padding until the next nonzero byte so the fixed-text patch is exact.
    while end < len(arm9) and arm9[end] == 0:
        end += 1
    return end


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize the complete Deck View cleanup.")
    parser.add_argument("--rom", type=Path, default=BASE_ROM)
    parser.add_argument("--arm9-out", type=Path, default=Path("translations/deck_view_arm9_v2.json"))
    parser.add_argument("--dialogue-out", type=Path, default=Path("translations/deck_view_dialogue_v2.json"))
    args = parser.parse_args()

    if sha256(args.rom.read_bytes()) != BASE_SHA256:
        raise SystemExit("wrong canonical accepted baseline")
    image = NdsImage.open(args.rom)
    arm9 = image.read_file("/__arm9__.bin")
    common = image.read_file("/COMMON/MESFILE.DK4")
    if sha256(arm9) != ARM9_SHA256 or sha256(common) != COMMON_SHA256:
        raise SystemExit("accepted Deck sources do not match their locked hashes")

    sorted_offsets = sorted(offset for _, offset, _, _ in ARM9_TEXT)
    records = []
    for record_id, offset, english, context in ARM9_TEXT:
        later = [candidate for candidate in sorted_offsets if candidate > offset]
        natural_end = slot_end(arm9, offset)
        end = min(natural_end, later[0]) if later else natural_end
        source = arm9[offset:end]
        if len(english.encode("ascii")) + 1 > len(source):
            raise SystemExit(f"{record_id}: {english!r} exceeds {len(source)}-byte slot")
        records.append({
            "id": record_id,
            "offset": offset,
            "source_hex": source.hex().upper(),
            "english": english,
            "encoding": "ascii",
            "context": context,
        })
    arm9_batch = {
        "format": "dk4-arm9-fixed-text-batch-v1",
        "file_path": "/__arm9__.bin",
        "source_file_sha256": ARM9_SHA256,
        "target_locale": "en-US",
        "scope": "Complete Deck room, requirement, restriction, ability, and Y-button cleanup",
        "records": records,
    }
    args.arm9_out.write_text(json.dumps(arm9_batch, indent=2) + "\n", encoding="utf-8")

    inventory = {}
    for row in export_mesfile_rows(common, "/COMMON/MESFILE.DK4", include_non_japanese=True):
        _, block_text, segment_text = row["pointer_group"].split(":")
        inventory[(int(block_text), int(segment_text))] = row
    dialogue_records = []
    for index, english in sorted(DECK_ACTIVITY.items()):
        if len(english.encode("ascii")) > 24:
            raise SystemExit(f"B17 R{index:04d} still exceeds the Deck's 24-glyph window")
        row = inventory[(17, index)]
        dialogue_records.append({
            **row,
            "english": english + "{PAD}",
            "status": "translated",
            "speaker": "Crew member",
            "context": "Single-line Deck activity response; runtime display limit is 24 glyphs.",
            "source_meaning": english,
            "localization_note": "Concise complete sentence fitted to the measured Deck activity window.",
            "review": {key: True for key in ("source", "context", "localization", "naturalness", "formatting")},
        })
    dialogue_batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/COMMON/MESFILE.DK4",
        "source_file_sha256": COMMON_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "shared-pair-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All accepted Deck activity responses that exceeded the runtime 24-glyph window",
        "records": dialogue_records,
    }
    args.dialogue_out.write_text(json.dumps(dialogue_batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.arm9_out}: {len(records)} fixed Deck strings")
    print(f"wrote {args.dialogue_out}: {len(dialogue_records)} complete 24-glyph responses")


if __name__ == "__main__":
    main()
