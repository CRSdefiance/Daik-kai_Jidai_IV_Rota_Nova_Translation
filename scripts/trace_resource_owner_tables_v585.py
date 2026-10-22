"""Bind initialized PXL owners, pointer tables and original cache-list admission.

No computed-address or global non-use claim follows from a missing literal.
"""

import json
import struct
from collections import defaultdict
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine

ROOT = Path("work/analysis/resource_owners_v585")
ROM = Path("out/all_routes_combined_v581_candidate.nds")
FRAME, CONFIRM = 0x02313F60, 0x023139C0
HEADER = 0x02440000


def word(u, address):
    return int.from_bytes(u.mem_read(address, 4), "little")


def initialize(rom):
    arm = rom.read_file("/__arm9__.bin")
    u = machine(arm)
    writes = []
    hook = u.hook_add(UC_HOOK_MEM_WRITE, lambda u, a, address, size, value, d:
                      writes.append((address, size, value)))
    try:
        executed = call(u, 0x10E190, ())
    finally:
        u.hook_del(hook)
    nonstack = [r for r in writes if not 0x027EF000 <= r[0] <= 0x027F0000]
    vtable = word(u, FRAME)
    owners = sorted({address for address, size, value in nonstack if size == 4 and value == vtable})
    assert len(owners) == 315 and CONFIRM in owners
    assert all(0x02312000 <= address < 0x02315000 for address, _, _ in nonstack)
    filenames = {}
    for owner in owners:
        values = struct.unpack("<5I", u.mem_read(owner, 20))
        assert values[1:3] == (owner + 4, owner + 4) and values[4] == 0xFFFFFFFF
        filename = bytes(u.mem_read(values[3], 128)).split(b"\0")[0].decode("ascii")
        assert filename.endswith(".pxl")
        filenames[owner] = filename
    assert filenames[FRAME] == "_pxl/__frame.pxl" and filenames[CONFIRM] == "_pxl/kakutei.pxl"
    for owner in (FRAME, CONFIRM):
        escapes = [(address, size, value) for address, size, value in nonstack
                   if owner <= value < owner + 20]
        assert escapes == [(owner + 4, 4, owner + 4), (owner + 8, 4, owner + 4)]
    return u, arm, executed, nonstack, owners, filenames


def getter_list_contract(rom):
    u, arm, _, _, _, _ = initialize(rom)
    # These exact original list helpers execute; only the final cache-ID lookup
    # is bridged to a supplied header. No disk load or image display is claimed.
    head = word(u, 0x020D6600)
    assert head == 0x02312734
    u.mem_write(head, struct.pack("<2I", head, head))
    u.mem_write(HEADER, rom.read_file("/_pxl/__frame.pxl"))
    cache_lookups = []

    def bridge(uc, address, size, data):
        if address == 0x020D68F0:
            assert uc.reg_read(UC_ARM_REG_R1) in (7, 8)
            cache_lookups.append([uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)])
            uc.reg_write(UC_ARM_REG_R0, HEADER)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, bridge)
    observations = []
    try:
        for index, owner in enumerate((FRAME, CONFIRM)):
            u.mem_write(owner + 16, struct.pack("<I", 7 + index))
            executed = call(u, 0xD6558, (owner,))
            assert {0x020D66E8, 0x020D6704, 0x020D68F0} <= executed
            assert not {0x020DF0A0, 0x020DED50, 0x020DEBDC} & executed
            assert u.reg_read(UC_ARM_REG_R0) == HEADER
            assert word(u, head) == owner + 4 and word(u, owner + 8) == head
            chain = []
            cursor = word(u, head)
            while cursor != head:
                assert cursor not in chain and len(chain) < 3
                chain.append(cursor)
                cursor = word(u, cursor)
            assert chain == ([FRAME + 4] if index == 0 else [CONFIRM + 4, FRAME + 4])
            observations.append({"owner": owner, "cache_list_after_getter": chain,
                                 "original_list_helpers_executed": True,
                                 "cached_lookup_only_no_file_load": True})
        # Remove Confirm through its original intrusive-list unlink operation.
        call(u, 0xD66E8, (CONFIRM + 4,))
        assert word(u, head) == FRAME + 4 and word(u, FRAME + 8) == head
        assert word(u, CONFIRM + 4) == word(u, CONFIRM + 8) == CONFIRM + 4
    finally:
        u.hook_del(hook)
    return {"list_head": head, "observations": observations, "cache_lookups": cache_lookups,
            "original_unlink_restores_self_links": True,
            "cache_header_binding_supplied_not_actual_load_or_rendering": True,
            "code_sha256": sha(arm[0xD6558:0xD6720])}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom, clean = NdsImage.open(ROM), NdsImage.open("work/clean.nds")
    digest = sha(ROM.read_bytes())
    assert digest == "542c2faf58bde6f408c873a930e29cdb215ef4940375aeffb650644c26d41e68"
    u, arm, executed, writes, owners, names = initialize(rom)
    original, _, clean_executed, clean_writes, clean_owners, clean_names = initialize(clean)
    assert (executed, writes, owners, names) == (clean_executed, clean_writes, clean_owners, clean_names)
    assert all(bytes(u.mem_read(a, 4)) == bytes(original.mem_read(a, 4)) for a in executed)
    initialized = set(owners)
    refs, loads, initializer_literals = defaultdict(list), defaultdict(list), defaultdict(set)
    sections = [(f"main{i}", s.ramAddress, bytes(s.data)) for i, s in enumerate(MainCodeFile(arm, 0x02000000).sections)]
    sections += [(f"overlay{i}", o.ramAddress, bytes(o.data)) for i, o in loadOverlayTable(
        rom.rom.arm9OverlayTable, lambda _id, file_id: rom.rom.files[file_id]).items()]
    for name, base, data in sections:
        # All byte positions are scanned for stored absolute pointers, including
        # unaligned data. ARM literal-use classification requires alignment.
        for at in range(len(data) - 3):
            value = struct.unpack_from("<I", data, at)[0]
            if value in initialized:
                refs[value].append({"unit": name, "address": base + at, "aligned": (base + at) % 4 == 0})
        for at in range(0, len(data) - 3, 4):
            instruction = struct.unpack_from("<I", data, at)[0]
            if instruction & 0x0F7F0000 != 0x051F0000:
                continue
            offset = at + 8 + (instruction & 4095) * (1 if instruction & 0x800000 else -1)
            if 0 <= offset <= len(data) - 4:
                value = struct.unpack_from("<I", data, offset)[0]
                if value in initialized:
                    row = {"instruction": base + at, "literal": base + offset,
                           "executed_initializer_instruction": base + at in executed}
                    loads[value].append(row)
                    if row["executed_initializer_instruction"]:
                        initializer_literals[value].add(base + offset)
    records = []
    file_paths = rom.path_map()
    for owner in owners:
        outside = [r for r in refs[owner] if r["address"] not in initializer_literals[owner]]
        records.append({"owner": owner, "filename": names[owner],
                        "literal_filename_exists_in_ROM": "/" + names[owner] in file_paths,
                        "same_basename_paths_not_assumed_aliases": [p for p in file_paths
                            if p.rsplit("/", 1)[-1] == names[owner].rsplit("/", 1)[-1]],
                        "initializer_literal_locations": sorted(initializer_literals[owner]),
                        "stored_absolute_pointer_references": refs[owner],
                        "outside_initializer_literal_references": outside,
                        "aligned_ARM_literal_load_candidates": loads[owner],
                        "no_external_stored_absolute_owner_pointer": not outside})
    no_external = [r for r in records if r["no_external_stored_absolute_owner_pointer"]]
    assert len(no_external) == 35
    assert next(r for r in records if r["owner"] == CONFIRM)["no_external_stored_absolute_owner_pointer"]
    assert len(next(r for r in records if r["owner"] == FRAME)["outside_initializer_literal_references"]) == 29
    # Positive controls: established portrait/map/Extras paths use stored tables
    # even when they have no non-initializer direct PC-relative owner load.
    controls = {}
    for filename in ("_pxl/person16bit_00.pxl", "_pxl/mysterymap/10_1.pxl", "_pxl/title/title05.pxl"):
        row = next(r for r in records if r["filename"] == filename)
        assert row["outside_initializer_literal_references"]
        controls[filename] = row["outside_initializer_literal_references"]
    current_list, clean_list = getter_list_contract(rom), getter_list_contract(clean)
    assert current_list == clean_list
    result = {"candidate": str(ROM), "candidate_sha256": digest,
              "script_sha256": sha(Path(__file__).read_bytes()),
              "initialized_PXL_owners": len(owners), "initializer_unique_instructions": len(executed),
              "initializer_nonstack_write_count": len(writes),
              "original_current_initializer_instructions_writes_and_filenames_exact": True,
              "initializer_does_not_publish_frame_or_Confirm_pointer_to_lookup_table": True,
              "all_main_sections_and_declared_overlays_stored_pointer_bytes_scanned": True,
              "no_external_stored_absolute_owner_pointer_count": len(no_external),
              "no_external_pointer_filenames": [r["filename"] for r in no_external],
              "positive_pointer_table_controls": controls,
              "resource_catalogue": records, "original_cache_list_contract": current_list,
              "limits": ["A PC-load-only inventory misclassifies table-selected resources; use stored-pointer references too.",
                         "Aligned ARM literal candidates may include data; they are not a whole-program call graph.",
                         "No external stored pointer is not proof of unused art: computed/relative addresses, copied pixels and dynamic lookup remain possible.",
                         "Cached header lookup is explicitly bridged; no actual disk load, ordinary menu, GPU or complete game traversal is added."],
              "ordinary_miniature_Confirm_standalone_logo_and_legacy_contexts_remain_open": True,
              "ROM_and_patch_changed": False, "full_goal_complete": False}
    assert sha(ROM.read_bytes()) == digest
    (ROOT / "owner_table_proof.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"V585: {len(owners)} original/current owners exact;{len(no_external)} without stored external pointers;table controls/cache-list admission pass;no global non-use claim.")


if __name__ == "__main__":
    main()
