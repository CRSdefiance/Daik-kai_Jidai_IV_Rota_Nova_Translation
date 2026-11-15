"""Current shared-name research, route formatting and stable COMMON identities.

Never creates a playable ROM or registers a partially migrated name release.
"""

import copy
import json
import struct
from pathlib import Path

from dk4tool.dialogue.codec import parse_markup, tokens_to_markup
from dk4tool.dialogue.model import DialogueToken
from dk4tool.dialogue.profiles import DialogueProfile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.patch.confirmed_character_names import FIELDS
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_confirmed_name_common_v228 import TEXT, native_lock
from scripts.verify_confirmed_name_fields_v198 import accessor
from scripts.verify_ordinary_name_fidelity_research import initialized

ROOT = Path("work/analysis/confirmed_names_v276")
ROM = Path("out/all_routes_combined_v275_candidate.nds")
DIGEST = "94fa82c8edd99de4f21829bc94b1b98013929f98cc1378c73fe0768e1d1caddf"
ARM9 = "5d152c714ab1218e9f3df796c6dfc7c3e58f2ae0fff12cb45c76932605962db0"


def safe_literal_markup(markup):
    """Preserve controls/macros; encode only literal reserved I/F as native Latin."""
    result = []
    for token in parse_markup(markup):
        if token.kind == "text":
            value = token.value.replace("I", "Ｉ").replace("F", "Ｆ")
            token = DialogueToken("text", value, value.encode("cp932"))
        result.append(token)
    return tokens_to_markup(result)


def name_fields(source, clean):
    assert sha(source) == ARM9
    target, rows = bytearray(source), []
    for record_id, index, column, offset, capacity, japanese, prior, english in FIELDS:
        field = 0x120B80 + index * 32 + column
        pointer = 0x02000000 + offset
        assert all(struct.unpack_from("<I", arm, field)[0] == pointer for arm in (source, clean))
        assert clean[offset:offset + capacity] == (japanese.encode("cp932") + b"\0").ljust(capacity, b"\0")
        assert source[offset:offset + capacity] == (prior.encode("cp932") + b"\0").ljust(capacity, b"\0")
        word = struct.pack("<I", pointer)
        assert [i for i in range(len(source) - 3) if source[i:i + 4] == word] == [field]
        encoded = (english.encode("ascii") + b"\0").ljust(capacity, b"\0")
        assert len(encoded) == capacity
        target[offset:offset + capacity] = encoded
        rows.append({"id": record_id, "index": index, "column": column, "offset": offset,
                     "capacity": capacity, "table_field": field, "Japanese": japanese,
                     "before": prior, "after": english})
    restored = bytearray(target)
    for row in rows:
        off, size = row["offset"], row["capacity"]
        restored[off:off + size] = source[off:off + size]
    assert restored == source
    return bytes(target), rows


def main():
    assert sha(ROM.read_bytes()) == DIGEST
    rom, original = NdsImage.open(ROM), NdsImage.open("work/clean.nds")
    source, clean = rom.read_file("/__arm9__.bin"), original.read_file("/__arm9__.bin")
    target, fields = name_fields(source, clean)
    (ROOT / "name_fields_research_only_arm9.bin").write_bytes(target)
    before, after = initialized(source), initialized(target)
    expected = {(row["index"], row["column"]): row["after"].encode("ascii") for row in fields}
    selections = []
    for index in range(207):
        for column, address in [(0, 0x7EB0C), (4, 0x7EAF4), (8, 0x7EADC)]:
            old_pointer, old_text = accessor(source, before, index, address)
            pointer, text = accessor(target, after, index, address)
            assert pointer == old_pointer and text == expected.get((index, column), old_text)
            selections.append({"index": index, "column": column, "pointer": pointer,
                               "before_hex": old_text.hex(), "after_hex": text.hex()})
    packet = json.loads((ROOT / "confirmed_source_locked_drafts.json").read_text(encoding="utf-8"))
    route_rows, legacy_common, checks = [], [], []
    for row in packet["records"]:
        if row["file_path"].startswith("/COMMON/"):
            legacy_common.append({"file_path": row["file_path"], "id": row["id"],
                                  "status": "superseded-physical-coordinates-use-native-ID-manuscript"})
            continue
        authored = copy.deepcopy(row)
        profile_data = dict(packet["proposed_profiles_not_registered"][row["proposed_profile"]])
        profile_data["leading_speaker_bytes"] = frozenset(profile_data["leading_speaker_bytes"])
        profile = DialogueProfile(**profile_data)
        encoded_markup = safe_literal_markup(row["english"])
        audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), encoded_markup, profile)
        authored["compiler_safe_markup"] = encoded_markup
        authored["compiler_encoding_note"] = "Only literal I/F receive established native full-width Latin encoding. Editable prose, control tokens and macro tokens remain unchanged."
        authored["current_layout_audit"] = audit
        route_rows.append(authored)
        checks.append({"file_path": row["file_path"], "id": row["id"],
                       "issues": audit["issues"], "needs_allocation_solution": any(i["severity"] == "error" for i in audit["issues"])})
    path = "/COMMON/MESFILE.DK4"
    japanese = common_message_entries(original.read_file(path), clean)
    current = common_message_entries(rom.read_file(path), source, clean=False)
    prior_review = json.loads(Path("translations/confirmed_name_common_manuscript_v1.json").read_text(encoding="utf-8"))
    reviewed = {r["message_id"]: r for r in prior_review["records"]}
    common_rows = []
    for message_id, (english, _, _) in TEXT.items():
        row = copy.deepcopy(reviewed[message_id])
        assert bytes.fromhex(row["source_hex"]) == japanese[message_id].text
        assert row["readable_english"] == english
        row["current_native_lock"] = native_lock(current[message_id])
        row["clean_native_lock"] = native_lock(japanese[message_id])
        common_rows.append(row)
    manuscript = {**prior_review, "parent_ROM": ROM.as_posix(), "parent_ROM_sha256": DIGEST,
                  "parent_common_sha256": sha(rom.read_file(path)), "records": common_rows,
                  "historical_source_review_retained_after_exact_clean_text_comparison": True}
    (ROOT / "current_common_manuscript.json").write_text(json.dumps(manuscript, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    packet["records"] = route_rows
    packet["superseded_legacy_COMMON_and_HELP_drafts"] = legacy_common
    packet["native_COMMON_source_manuscript"] = str(ROOT / "current_common_manuscript.json")
    packet["HELP_source_manuscript"] = "translations/confirmed_name_help_manuscript_v1.json"
    packet["HELP_allocation_and_consumer_still_pending"] = True
    (ROOT / "current_route_migration_packet.json").write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    failures = [row for row in checks if row["needs_allocation_solution"]]
    proof = {"format": "dk4-current-confirmed-name-migration-v276", "source_ROM": str(ROM),
             "source_ROM_sha256": DIGEST, "source_ARM9_sha256": ARM9,
             "research_name_ARM9_sha256": sha(target), "name_fields": fields,
             "native_accessor_selections": 621, "changed_accessor_outputs": 5,
             "other616_accessor_outputs_exact": True, "accessor_cases": selections,
             "native_startup_complete_pool_copy_and_stack_executed": True,
             "route_records": len(route_rows), "route_current_diagnostics": checks,
             "route_records_needing_allocation_or_layout_work": len(failures),
             "allocation_backlog": failures, "editorial_override_records": sum(bool(r.get("editorial_override")) for r in route_rows),
             "superseded_physical_COMMON_HELP_draft_count": len(legacy_common),
             "native_COMMON_global_ID_records": list(TEXT),
             "name_only_playable_release_is_not_safe_until_macro_text_and_art_migration_complete": True,
             "playable_ROM_modified": False, "full_goal_complete": False}
    (ROOT / "current_migration_proof.json").write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"route_records": len(route_rows), "native_getters": 621,
                      "changed_fields": 5, "superseded_COMMON_HELP_drafts": len(legacy_common),
                      "current_native_COMMON_IDs": list(TEXT), "allocation_or_layout_backlog": len(failures)}))


if __name__ == "__main__":
    main()
