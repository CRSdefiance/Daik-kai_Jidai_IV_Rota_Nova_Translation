"""Verify the legacy memory-card check against the original DS header scanner."""

from pathlib import Path
from struct import iter_unpack, unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_SP

from scripts.probe_button_prompt_native import BASE, STACK, STOP, machine
from scripts.reconcile_legacy_fleet_and_quit_paths_20261123 import (
    OUT as PREVIOUS, WORKLIST, base, common_message_entries, current, native,
    owned_entries, stored_record, DIRECTORY_OFFSET, TABLE_OFFSET,
)
from scripts.reconcile_legacy_setup_and_recruitment_20261123 import registered_review


OUT = PREVIOUS.with_name("cartridge_header_check_20261123.json")
SAVE = Path("releases/all_routes_editorial_20261119_save_dialogue_candidate")
SETUP = Path("releases/all_routes_editorial_20261115_setup_confirmation_prose_candidate")
HEADERS, READ, MODAL = 0xEEF58, 0xD62F8, 0x5473C
SYSTEM_DATA_NOTICE = 0x546B8
CALLERS = (0xED714, 0xEE800, 0xEECC8)
PARENTS = {
    "game_slot_check": (0xED708, 0xED73C, (0,)),
    "system_data_read": (0xEE7E0, 0xEE80C, (0, 1)),
    "save_or_load_slot_check": (0xEECA0, 0xEECDC, (0, 1)),
}


def run(arm, parent, mode, failed_header):
    start, success, _ = PARENTS[parent]
    cpu = machine(arm)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    cpu.reg_write(UC_ARM_REG_R0, mode)
    reads = []
    selected = None
    terminal = None

    def observe(u, pc, _size, _ctx):
        nonlocal selected, terminal
        offset = pc - BASE
        if offset in (success, MODAL, SYSTEM_DATA_NOTICE):
            terminal = offset
            if offset == MODAL:
                ptr = u.reg_read(UC_ARM_REG_R0)
                write = parent == "save_or_load_slot_check" and mode == 1
                field = 0xEEF50 if write else 0xEEF54
                assert ptr == unpack_from("<I", arm, field)[0]
                selected = dict(ARM9_pointer_field=BASE + field, ARM9_text_pointer=ptr)
            elif offset == SYSTEM_DATA_NOTICE:
                common = u.reg_read(UC_ARM_REG_R0)
                assert parent == "system_data_read" and mode == 1 and common == 123
                selected = dict(COMMON_argument=common)
            u.emu_stop()
        elif offset in (0x5528C, 0x534F4):
            raise AssertionError(f"Unexpected COMMON lookup at {pc:#x}")
        elif offset == READ:
            address, buf, size = (u.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2))
            assert size == 4 and address == len(reads) * 0xA000 and STACK - 0x300 < buf < STACK
            reads.append(dict(backup_offset=address, bytes=size))
            u.mem_write(buf, bytes(size))
            u.reg_write(UC_ARM_REG_R0, int(len(reads) - 1 != failed_header))
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
        elif offset == 0xCEBF8:
            assert parent == "system_data_read" and u.reg_read(UC_ARM_REG_R1) == 0x2000
            u.mem_write(u.reg_read(UC_ARM_REG_R0), bytes(0x2000))
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    cpu.hook_add(UC_HOOK_CODE, observe)
    cpu.emu_start(BASE + start, STOP, count=4000)
    assert len(reads) == (7 if failed_header is None else failed_header + 1)
    if failed_header is None:
        assert terminal == success and selected is None
    elif parent == "system_data_read" and mode == 1:
        assert terminal == SYSTEM_DATA_NOTICE and selected == {"COMMON_argument": 123}
    else:
        assert terminal == MODAL and selected is not None
    return dict(parent=parent, supplied_mode=mode, supplied_failed_header=failed_header, original_fixed_header_reads=reads,
        boundary=BASE + terminal, selected_notice=selected, stopped_at_notice_receiver=True)


def parent_code(ja, en):
    def callers(arm):
        found = []
        for index, (word,) in enumerate(iter_unpack("<I", arm)):
            if word & 0x0F000000 != 0x0B000000:
                continue
            offset = index * 4
            if offset + 8 + 4 * (((word & 0xFFFFFF) ^ 0x800000) - 0x800000) == HEADERS:
                found.append(offset)
        return tuple(found)

    assert callers(ja) == callers(en) == CALLERS
    spans = ((HEADERS, 0xEEFB0), (0xED708, 0xED73C), (0xEE7E0, 0xEE80C),
             (0xEE848, 0xEE864), (0xEE9E8, 0xEE9FC),
             (0xEECA0, 0xEECDC), (0xEEF24, 0xEEF58))
    for start, end in spans:
        assert ja[start:end] == en[start:end]
    return {f"{BASE + start:08X}-{BASE + end:08X}": native.digest(en[start:end]) for start, end in spans}


def main():
    release, review, prior = map(base.load, (current.RELEASE, current.REVIEW, PREVIOUS))
    assert base.digest(current.ROM) == release["candidate_sha256"] == review["candidate_sha256"] == prior["candidate_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    clean, active = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    ja, en = (rom.read_file(current.ARM) for rom in (clean, active))
    common = active.read_file(current.COMMON)
    assert native.digest(en) == release["target_ARM9_sha256"] and native.digest(common) == release["target_COMMON_sha256"]
    source = common_message_entries(clean.read_file(current.COMMON), ja)
    installed = owned_entries(common, en, native.digest(en[DIRECTORY_OFFSET:TABLE_OFFSET]))
    inventory = {row["message_ID"]: row for row in base.load(WORKLIST)["records"]}
    binding = {row["message_ID"]: row for row in review["shared_consumer_binding"]["records"]}
    record = stored_record(116, source, installed, inventory, binding)
    runtime = parent_code(ja, en)
    cases = []
    for parent, (_, _, modes) in PARENTS.items():
        for mode in modes:
            for fault in (None, *range(7)):
                original, localized = (run(arm, parent, mode, fault) for arm in (ja, en))
                assert original == localized
                cases.append(localized)

    save, save_path = registered_review(SAVE)
    warnings = []
    for key, field in (("DK4_LOAD_READ_ERROR", 0xEEF54), ("DK4_SAVE_WRITE_ERROR", 0xEEF50)):
        row, = [row for row in save["records"] if row["id"] == key]
        assert all(row["review"].values()) and row["native_pages"] == 1
        ranges = ((ja, row["source_reference"], row["source_hex"]),
                  (en, row["registered_reference"], row["registered_reference"]["exact_stored_hex"]))
        for raw, pointer, payload in ranges:
            offset = pointer["offset"]
            assert pointer["pointer_field"] == BASE + field
            assert unpack_from("<I", raw, field)[0] == BASE + offset
            assert raw[offset:offset + pointer["allocation"]] == bytes.fromhex(payload)
        warnings.append(row)
    setup, setup_path = registered_review(SETUP)
    system, = [row for row in setup["records"] if row["message_ID"] == 123]
    assert all(system["review"].values()) and source[123].text.hex() == system["source_hex"]
    assert installed[123].text.hex() == system["deployed_hex"]
    warnings.append(system)
    record["verified_scoped_path"] = ("The DS header scanner reads fixed addresses on the game card. "
        "Failed scans select the game-card read or write warning by caller mode, or COMMON 123 for system data. "
        "The successfully supplied header reads proceed without a memory-card progress warning.")
    remaining = set(prior["remaining_without_scoped_disposition"])
    assert len(remaining) == 22 and 116 in remaining
    base.save(OUT, dict(candidate_sha256=release["candidate_sha256"], reviewed_entries=[record],
        remaining_without_scoped_disposition=sorted(remaining - {116}), original_ARM9_spans=runtime,
        original_ARM9_direct_callers=[BASE + offset for offset in CALLERS], cases=cases,
        offline_runs=len(cases) * 2, supplied_cartridge_reads=True,
        retained_notice_reviews=warnings, ordinary_gameplay_runs=0, new_ROM=False, hardware=False,
        evidence={str(path): base.digest(path) for path in (PREVIOUS, WORKLIST, save_path, setup_path,
            current.RELEASE, current.REVIEW, Path(__file__))}))
    print(f"Verified {len(cases) * 2} clean/current game-card header cases; {len(remaining) - 1} shared entries remain.")


if __name__ == "__main__":
    main()
