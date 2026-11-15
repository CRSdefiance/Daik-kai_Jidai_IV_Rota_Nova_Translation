"""Construct a bounded current name catalog; ARM9 research only, no ROM."""

import json
import struct

from ndspy.code import MainCodeFile

from dk4tool.patch.confirmed_name_message_catalog import CALLS, MACRO, helper
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.rom.nds import NdsImage
from scripts.prepare_name_catalog_v277 import ROOT
from scripts.probe_common_display_name_hook import branch_link
from scripts.revalidate_name_migration_v276 import ARM9, DIGEST, ROM, name_fields


def main():
    assert sha(ROM.read_bytes()) == DIGEST
    preparation = json.loads((ROOT / "preparation_and_scope.json").read_text(encoding="utf-8"))
    assert preparation["source_ROM_sha256"] == DIGEST
    assert preparation["all_four_route_strings_have_only_intended_matches"]
    assert not preparation["COMMON_matching_keys_requiring_further_scope_review"]
    source = NdsImage.open(ROM).read_file("/__arm9__.bin")
    assert sha(source) == ARM9
    clean = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    named, fields = name_fields(source, clean)
    code = MainCodeFile(named, BASE)
    before = [bytes(section.data) for section in code.sections]
    assert len(before) == 4 and code.sections[3].ramAddress == STAGE
    assert cache_plan(named) and len(before[3]) == 82448
    packed = bytearray(before[3][:-48])
    pointers = {}

    def store(raw):
        assert raw and b"\0" not in raw and len(raw) < 512
        if raw not in pointers:
            packed.extend(bytes((-len(packed)) % 4))
            pointers[raw] = POOL + len(packed)
            packed.extend(raw + b"\0")
        return pointers[raw]

    records = []
    for row in preparation["keys"]:
        key, target = bytes.fromhex(row["key_hex"]), bytes.fromhex(row["target_hex"])
        records.append({**row, "key_pointer": store(key), "target_pointer": store(target),
                        "key_bytes_with_NUL": len(key) + 1})
    packed.extend(bytes((-len(packed)) % 4))
    table = POOL + len(packed)
    for row in records:
        packed.extend(struct.pack("<3I", row["key_pointer"], row["target_pointer"], row["key_bytes_with_NUL"]))
    entry = POOL + len(packed)
    implementation = helper(entry, table, len(records))
    packed.extend(implementation)
    for field in CALLS:
        assert struct.unpack_from("<I", source, field)[0] == branch_link(BASE + field, MACRO)
        struct.pack_into("<I", code.sections[0].data, field, branch_link(BASE + field, entry))
    packed.extend(bytes((-len(packed)) % 32))
    size = len(packed) + 64
    assert POOL + size <= STAGE and STAGE + size + 48 <= 0x023F4000
    cache_entry, copy_entry = STAGE + len(packed), STAGE + size
    packed.extend(wrapper(cache_entry, copy_entry, size, named))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack("<I", size)
    struct.pack_into("<I", code.sections[0].data, 0x8E4, branch_link(BASE + 0x8E4, cache_entry))
    struct.pack_into("<I", code.sections[0].data, 0xE45DC, POOL + size)
    saved = bytes(code.save())
    parsed = MainCodeFile(saved, BASE)
    restored = bytearray(parsed.sections[0].data)
    for field in (*CALLS, 0x8E4, 0xE45DC):
        restored[field:field + 4] = before[0][field:field + 4]
    offset = code.codeSettingsOffs
    restored[offset:offset + 12] = before[0][offset:offset + 12]
    assert bytes(restored) == before[0]
    assert all(bytes(parsed.sections[n].data) == before[n] for n in (1, 2))
    assert bytes(parsed.sections[3].data[:len(before[3]) - 48]) == before[3][:-48]
    (ROOT / "catalog_research_only_arm9.bin").write_bytes(saved)
    plan = {"format": "dk4-current-name-catalog-research-v277", "source_ROM_sha256": DIGEST,
            "source_arm9_sha256": ARM9, "target_arm9_sha256": sha(saved),
            "name_fields": fields, "prepared_records": preparation["records"], "records": records,
            "entry": entry, "table": table, "helper_bytes": len(implementation),
            "pool_payload_bytes": size, "copy_entry": copy_entry, "cache": cache_plan(saved),
            "pool_span": [POOL, POOL + size], "staging_span": [STAGE, STAGE + size + 48],
            "inherited_pool_bytes_preserved": len(before[3]) - 48,
            "scoped_call_sites": [BASE + field for field in CALLS],
            "all_other_main_code_ITCM_DTCM_inherited_helpers_and_strings_preserved": True,
            "native_lookup_and_actual_macro_copy_verification_pending": True,
            "editorial_complete_pixels_and_full_name_text_art_integration_pending": True,
            "research_only_no_playable_ROM_generated": True, "full_goal_complete": False}
    (ROOT / "catalog_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"records": len(plan["prepared_records"]), "unique_keys": len(records),
                      "pool_payload_bytes": size, "remaining_before_STAGING": STAGE - POOL - size}))


if __name__ == "__main__":
    main()
