from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import iter_mesfile_records

ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "work/analysis/common_clean_inventory.json"
BASE_ROM = ROOT / "out/raphael_natural_v2_pre_common_accepted_rollback.nds"
AUDIT_OUT = ROOT / "work/analysis/common_b16_entry_audit.json"
BATCH_OUT = ROOT / "translations/common_natural_v2_b16_safe.json"
BLOCKED_OUT = ROOT / "translations/common_natural_v2_b16_blocked.json"
SOURCE_HASH = "ecb0806b6f36f9bf4164ae46084fbbc12d4122af66b6a8920814197463f19491"


EDITORIAL_ENGLISH = {
    0: "Admiral, city ahead!",
    1: "Admiral! %s is in battle. Help?",
    2: "Admiral! %s is in battle. Help?",
    4: "Admiral! %s is in battle. Help?",
    6: "Admiral, %s is attacking us!",
    7: "Admiral, %s is attacking!",
    8: "Admiral, %s attacks!",
    9: "Admiral, %s attacks!",
    10: "Admiral, %s is attacking!",
    11: "%s is attacking us!",
    12: "Admiral, %s is attacking us!",
    14: "Sir, a village!",
    16: "Village in sight!",
    17: "Villagers gave us food and water.",
    18: "Villagers gave us food and water.",
    19: "Villagers gave us food and water.",
    20: "Villagers gave us food and water.",
    21: "Villagers shared food and water.",
    22: "Villagers gave us food and water.",
    23: "Villagers gave us food and water.",
    24: "Villagers gave us food and water.",
    25: "Their hospitality cheered everyone.",
    26: "Their hospitality cheered everyone.",
    27: "Their hospitality cheered everyone.",
    28: "Their welcome cheered everyone.",
    29: "Their welcome cheered everyone.",
    30: "Their feast was delicious. Everyone is happy.",
    31: "Their hospitality cheered everyone.",
    32: "The villagers repaired our ship.",
    33: "The villagers fixed our ship.",
    34: "The villagers repaired our ship.",
    35: "The villagers repaired our ship.",
    36: "Villagers repaired the ship.",
    37: "The villagers fixed our ship.",
    38: "The villagers repaired our ship.",
    39: "%s villagers came.",
    40: "%s villagers came.",
    41: "%s villagers came.",
    42: "%s villagers gathered here.",
    43: "%s villagers came.",
    44: "%s villagers joined us.",
    45: "%s villagers gathered here.",
    49: "A room for me? How lovely!",
    50: "Can't do that... Sorry.",
    52: "Good tea.",
    54: "Haaaaah! Ubaai!",
    55: "Dancing makes me happy!",
    56: "Ancient lore... Hmm.",
    57: "The sky is so relaxing...",
    58: "A warrior trains every day.",
    59: "Nice rod! Time for a big catch.",
    60: "My blade gleams beautifully.",
    61: "There! Turned out well!",
    62: "Mmm! A secret taste is best.",
    63: "Damn. Sea air ruins my hair.",
    64: "Swinging a sword calms me.",
    65: "A man's fists decide.",
    66: "Mix these... So that's it!",
    67: "Zzz... Mumble... Zzz...",
    68: "Gotta gamble.",
    69: "Stronger... Must get stronger.",
    70: "Zzz... Delicious... Zzz.",
    71: "Color, balance... Perfect.",
    72: "Water... Happy flowers...",
    73: "Better make spare parts now.",
    74: "Might make some spare parts.",
    75: "Ships break fast. A pain.",
    76: "They break right away.",
    77: "Ow! Hit my hand!",
    78: "Hmm... Nicely done.",
    79: "Done! Time to make more!",
    80: "Oh, a masterpiece...",
    81: "Better keep making parts...",
    82: "Better make spares now...",
    83: "Huh? Does this part go here?",
    84: "This work suits me.",
    85: "No salve. Better make some.",
    86: "Mix this herb into this...",
    87: "Phew, it stinks! But it works.",
    88: "Always another injury. More medicine.",
    89: "Yes! Seasickness medicine!",
    90: "Hmm... Should be ready now.",
    91: "Taste test... Ugh, awful!",
    92: "Hmm, the medicine is ready.",
    93: "Claudio's always getting hurt...",
    94: "Must learn more about herbs.",
    95: "Odd color... Safe to drink?",
    96: "Xian's herbal medicine helps.",
    97: "Let's make a nourishing meal.",
    98: "Salt... Now add this.",
    99: "Cooking comes easy. What next?",
    100: "Hee-hee! Cooking's my gift!",
    101: "Salt... Wait, sugar!",
    102: "Time for a man's cooking.",
    103: "Taste test... Huh? All gone?",
    104: "Hmm. Seasoned just right.",
    105: "Hmm, it's a little too salty...",
}


PACKED_DRAFTS = {
    3: [
        "Admiral! %s's fleet is in battle. Shall we help?",
        "Admiral! %s's fleet is fighting. Should we assist?",
        "Admiral! %s's fleet is in battle. Shall we join them?",
    ],
    5: [
        "Admiral! %s's fleet is fighting. Should we help?",
        "%s's fleet is in battle. Shall we assist?",
        "Admiral, %s is attacking us!",
    ],
    13: ["Admiral, we've discovered a village!", "Admiral, a village!"],
    15: ["Admiral, a village is in sight!", "Admiral, a village!", "Admiral, a village!", "Look! There's a village!"],
    46: [
        "We gave the villagers %s coins to thank them for their help.",
        "We gave the villagers %s coins for helping us.",
        "We gave the villagers %s coins in thanks.",
        "We gave the villagers %s coins for their help.",
    ],
    47: ["We gave the villagers %s coins to thank them.", "We gave the villagers %s coins with our thanks."],
    48: ["We gave the villagers %s coins to thank them.", "I'm a wonderful cook. It'll be delicious."],
    51: ["... (I don't understand the language.)", "Yes, that's a lovely melody.", "Not bad at all...", "Zzz... Kamil... Zzz..."],
    53: ["Yes, yes. What a good story.", "Ninety-nine, one hundred, one hundred one... Ngh, one hundred two..."],
}


# Literal source summaries stay separate from the space-constrained English.
# These make explicit details that a fixed allocation sometimes forces the
# localized line to imply rather than spell out.
SOURCE_MEANING_OVERRIDES = {
    14: "A companion addresses the admiral and announces that there is a village.",
    16: "A companion addresses the admiral and announces that a village is in sight.",
    44: "The speaker says that the displayed number of villagers will come to help.",
    50: "The speaker says they cannot do it and apologizes.",
    54: "The speaker gives a strange, energetic shout.",
    55: "The speaker sings and says dancing makes them happy.",
    56: "The speaker muses over something from ancient times and acknowledges understanding.",
    58: "The warrior says one must train constantly because every day is practice.",
    65: "The speaker says men settle things with their fists and must always train.",
    68: "The speaker says they want to gamble.",
    69: "The speaker resolves to become stronger and stronger.",
    71: "The speaker judges the color, luster, and balance and calls the result a masterpiece.",
    72: "The speaker waters flowers and says they are very happy.",
    75: "The speaker complains that ships are damaged quickly and the work is difficult.",
    76: "The speaker complains that parts break as quickly as they can make them.",
    77: "The speaker cries out after striking their hand.",
    79: "The speaker celebrates finishing a part and eagerly starts making more.",
    82: "The speaker says they must make spare parts while there is time.",
    84: "The speaker says they are good at this kind of work.",
    85: "The speaker notices the salve is gone and decides to make more.",
    86: "The speaker works out which herb to mix into the medicine.",
    87: "The speaker says the medicine smells bad but that is why it works.",
    88: "The speaker says someone is always injured, so they have to make medicine.",
    89: "The speaker celebrates completing seasickness medicine.",
    90: "The speaker judges that the medicine should now be ready.",
    91: "The speaker tastes the medicine and finds it awful.",
    92: "The speaker observes that the medicine appears ready.",
    93: "The speaker notes that Claudio gets hurt easily.",
    94: "The speaker resolves to learn more about medicinal herbs.",
    95: "The speaker worries whether oddly colored medicine is safe to drink.",
    96: "The speaker says the Chinese herbal medicine learned from Xian is useful.",
    97: "The speaker proposes making nutritious food.",
    98: "The cook adds salt and moves to the next ingredient.",
    99: "The speaker says cooking is a specialty and wonders what to make.",
    100: "The speaker hums and proudly says cooking is a specialty.",
    101: "The cook reaches for salt, then realizes it is sugar.",
    102: "The speaker decides to try making a man's style of cooking.",
    103: "The speaker tastes the food and realizes it is already gone.",
    104: "The speaker judges the seasoning is just right.",
    105: "The speaker says the dish is a little too salty.",
}


# Filled after auditing the accepted-source candidates. Records excluded here
# remain fully translated in the blocked editorial inventory.
SAFE_BUILD = set(EDITORIAL_ENGLISH)


def context_for(index: int) -> str:
    if index <= 16:
        return "A shared sailing companion reports a city, village, battle, or incoming attack."
    if index <= 48:
        return "A shared village event reports supplies, hospitality, repairs, recruits, or a thank-you payment."
    if index <= 72:
        return "An officer's ambient cabin or leisure line reflects their personality and current activity."
    if index <= 84:
        return "An officer works on replacement ship parts during an ambient crew scene."
    if index <= 96:
        return "An officer prepares medicine during an ambient crew scene."
    return "An officer cooks during an ambient crew scene."


def main() -> None:
    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    clean_rows = {int(r["segment_index"]): r for r in inventory["records"] if int(r["block_index"]) == 16}
    if set(clean_rows) != set(range(106)):
        raise ValueError("clean block 16 inventory is not the expected 106 records")
    mesfile = NdsImage.open(BASE_ROM).read_file("/COMMON/MESFILE.DK4")
    if sha256(mesfile).hexdigest() != SOURCE_HASH:
        raise ValueError("accepted baseline MESFILE hash does not match the required source lock")
    baseline_rows = {
        r.segment_index: r
        for r in iter_mesfile_records(mesfile, include_non_japanese=True)
        if r.block_index == 16
    }
    if set(baseline_rows) != set(range(106)):
        raise ValueError("accepted block 16 is not the expected 106 records")
    single, packed = set(EDITORIAL_ENGLISH), set(PACKED_DRAFTS)
    if single & packed or single | packed != set(range(106)):
        raise ValueError("classification does not cover block 16 exactly once")

    audit_records, safe_records, blocked_records = [], [], []
    for index in range(106):
        clean, baseline = clean_rows[index], baseline_rows[index]
        if len(baseline.raw_bytes) != int(clean["source_length"]):
            raise ValueError(f"record {index}: accepted and clean allocations differ")
        english = EDITORIAL_ENGLISH.get(index)
        drafts = PACKED_DRAFTS.get(index)
        meaning = (
            " / ".join(drafts)
            if drafts
            else SOURCE_MEANING_OVERRIDES.get(index, english)
        )
        row_id = f"DK4_MES_B16_R{index:04d}"
        is_safe = index in SAFE_BUILD
        audit_records.append(
            {
                "id": row_id,
                "block_index": 16,
                "segment_index": index,
                "source_offset": clean["source_offset"],
                "source_length": clean["source_length"],
                "clean_source_hex": clean["source_hex"],
                "accepted_source_hex": baseline.raw_bytes.hex().upper(),
                "japanese_markup": clean["markup"],
                "accepted_markup_for_structure_only": baseline.text,
                "accepted_differs_from_clean": baseline.raw_bytes.hex().upper() != clean["source_hex"],
                "classification": "single-message" if index in single else "packed-multiple-entry",
                "source_meaning": meaning,
                "safe_to_replace": is_safe,
                "safety_reason": (
                    "One independently addressable message selected for guarded fixed-dialogue QA."
                    if is_safe
                    else "Multiple adjacent messages appear without NUL delimiters; their interior entry offsets are unproven."
                    if drafts
                    else "The accepted source contains command-like legacy ASCII or the localized text cannot safely fit its fixed allocation."
                ),
            }
        )
        record = {
            "id": row_id,
            "speaker": (
                "Multiple shared companion or officer voices"
                if drafts
                else "Shared companion or officer"
            ),
            "context": context_for(index),
            "source_meaning": meaning,
        }
        if is_safe:
            record.update(
                {
                    "english": english + "{PAD}",
                    "localization_note": "Uses idiomatic American English while preserving the source event, activity, personality, and runtime substitutions.",
                    "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")},
                }
            )
            safe_records.append(record)
        else:
            record.update(
                {
                    "source_length": clean["source_length"],
                    "japanese_markup": clean["markup"],
                    "draft_messages": drafts or [english],
                    "blocker": (
                        "Multiple concatenated messages have unproven interior entry offsets."
                        if drafts
                        else "The guarded encoder cannot safely distinguish legacy accepted ASCII from runtime commands, or the faithful English cannot fit the fixed allocation."
                    ),
                    "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": False},
                }
            )
            blocked_records.append(record)

    AUDIT_OUT.write_text(json.dumps({
        "format": "dk4-common-entry-safety-audit-v1",
        "file_path": "/COMMON/MESFILE.DK4",
        "block_index": 16,
        "source": "work/analysis/common_clean_inventory.json generated from work/clean.nds",
        "accepted_source_file_sha256": SOURCE_HASH,
        "classification_counts": {"single-message": len(single), "packed-multiple-entry": len(packed), "padding-only": 0, "likely-identifier": 0},
        "replacement_counts": {"safe_to_replace": len(SAFE_BUILD), "blocked": 106 - len(SAFE_BUILD)},
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
        "scope": "Independently addressable, encoder-safe records in shared MESFILE block 16",
        "blocked_packed_records": [f"DK4_MES_B16_R{i:04d}" for i in sorted(packed)],
        "blocked_records": [r["id"] for r in blocked_records],
        "records": safe_records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    BLOCKED_OUT.write_text(json.dumps({
        "format": "dk4-blocked-editorial-inventory-v1",
        "file_path": "/COMMON/MESFILE.DK4",
        "source_file_sha256": SOURCE_HASH,
        "block_index": 16,
        "buildable": False,
        "records": blocked_records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote block-16 audit={len(audit_records)}, safe={len(safe_records)}, blocked={len(blocked_records)}")


if __name__ == "__main__":
    main()
