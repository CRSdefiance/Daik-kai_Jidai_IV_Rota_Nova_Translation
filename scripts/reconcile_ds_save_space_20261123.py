"""Verify the DS paths related to the six archived free-block warnings."""

from pathlib import Path
from struct import pack, unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_SP

from scripts.probe_button_prompt_native import BASE, STACK, STOP, machine
from scripts.reconcile_cartridge_header_check_20261123 import OUT as HEADER_CHECK
from scripts.reconcile_legacy_fleet_and_quit_paths_20261123 import (
    WORKLIST, base, common_message_entries, current, native, owned_entries, stored_record,
    DIRECTORY_OFFSET, TABLE_OFFSET,
)
from scripts.reconcile_lisbon_new_save_20261123 import OUT as PREVIOUS


OUT = PREVIOUS.with_name("ds_save_space_20261123.json")
TITLE, SLOT_WRITER, READ, WRITE, MODAL = 0x3EAB8, 0xEEA14, 0xD62F8, 0xD63A4, 0x5473C
SLOT_SIZE, SYSTEM_OFFSET, SYSTEM_SIZE, SLOT_COUNT = 0xA000, 0x3C000, 0x800, 6
SESSION, ENTRIES, SAVE_BUFFER = 0x02279668, 0x023CC000, 0x023D0000
WRITE_CONFIRM = 0x546F8
EARLIER_FRAGMENTS = (0x5528C, 0x534F4, 0x546B8, 0x5466C)
SAVE_SPACE = {108: ("game data", 4), 109: ("system data", 1), 110: ("game and system data", 5),
              113: ("game data", 4), 114: ("system data", 1), 115: ("game and system data", 5)}


def side_exit(cpu, ret=None):
    if ret is not None:
        cpu.reg_write(UC_ARM_REG_R0, ret)
    cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))


def start(cpu, offset, args):
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    for reg, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), args):
        cpu.reg_write(reg, value)
    cpu.emu_start(BASE + offset, STOP, count=500_000)
    return cpu.reg_read(UC_ARM_REG_PC), cpu.reg_read(UC_ARM_REG_R0)


def notice_pointer(cpu, arm, field):
    pointer, = unpack_from("<I", arm, field)
    assert cpu.reg_read(UC_ARM_REG_R0) == pointer
    offset = pointer - BASE
    text = arm[offset:arm.index(0, offset, offset + 128)].decode("cp932")
    return dict(pointer_field=BASE + field, runtime_pointer=pointer, exact_text=text)


def new_game(arm, occupied, system_record, reading_fault):
    cpu = machine(arm)
    reads, selectors, notices = [], [], []
    cpu.mem_write(SESSION, bytes(0x80))
    cpu.mem_write(0x023120C8, pack("<H", 20))

    def observe(u, pc, _size, _ctx):
        offset = pc - BASE
        if offset == READ:
            address, buf, size = (u.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2))
            slot = address // SLOT_SIZE
            assert address == slot * SLOT_SIZE and slot <= SLOT_COUNT
            assert size == 4 or (size == 0x7C and slot in occupied and slot < SLOT_COUNT)
            payload = (b"DK4R" if (slot in occupied or (slot == SLOT_COUNT and system_record)) else b"\xff" * 4)
            u.mem_write(buf, payload + bytes(size - 4))
            reads.append([address, size])
            side_exit(u, int(reading_fault != (slot, size)))
        elif offset == 0x51EE0:
            descriptors = u.reg_read(UC_ARM_REG_R0)
            assert u.reg_read(UC_ARM_REG_R1) == 6
            continue_enabled = unpack_from("<I", u.mem_read(descriptors + 8, 4))[0]
            selectors.append(dict(continue_enabled=bool(continue_enabled), supplied_index=0))
            side_exit(u, 0)
        elif offset == 0xCA890:
            side_exit(u)
        elif offset == MODAL:
            notices.append(notice_pointer(u, arm, 0xEEF54))
            u.emu_stop()
        elif offset in EARLIER_FRAGMENTS:
            raise AssertionError(f"Unexpected title COMMON lookup at {pc:#x}")

    cpu.hook_add(UC_HOOK_CODE, observe)
    pc, value = start(cpu, TITLE, (SESSION,))
    if reading_fault is None:
        assert (pc, value) == (STOP, 1) and not notices
        assert selectors == [dict(continue_enabled=bool(occupied), supplied_index=0)]
        assert reads == [[i * SLOT_SIZE, 4] for i in range(SLOT_COUNT + 1)] + [[i * SLOT_SIZE, 0x7C] for i in occupied]
    else:
        assert pc == BASE + MODAL and len(notices) == 1 and not selectors
    return dict(occupied=list(occupied), system_record=system_record, supplied_read_failure=reading_fault,
        cartridge_reads=reads, title_choices=selectors, entered_new_game=pc == STOP, notices=notices)


def checked_payload(u, offset, pointer, count, slot):
    data = bytes(u.mem_read(pointer, count))
    assert data[:4] == b"DK4R"
    checksum, = unpack_from("<I", data, 4)
    checksum_end = 0x44 if offset == SYSTEM_OFFSET else SLOT_SIZE
    assert checksum == sum(n if n < 128 else n - 256 for n in data[8:checksum_end]) & 0xFFFFFFFF
    if offset == SYSTEM_OFFSET:
        assert data[0x43] == slot
    return native.digest(data)


def save_slot(arm, slot, overwrite, answer, failed):
    cpu = machine(arm)
    texts, status, writes, notices = [], [], [], []
    cpu.mem_write(STACK, pack("<I", ENTRIES))
    cpu.mem_write(0x0216903C, pack("<I", SAVE_BUFFER))
    cpu.mem_write(SAVE_BUFFER, bytes(SLOT_SIZE))
    cpu.mem_write(SESSION, bytes(0x240))
    ui_calls = {0xCF7A4, 0xEFBB0, 0xEF19C, 0xEF14C, 0xEFCDC, 0xCE890}

    def observe(u, pc, _size, _ctx):
        offset = pc - BASE
        if offset == WRITE_CONFIRM:
            field = 0xEEC28 if overwrite else 0xEEC2C
            src, = unpack_from("<I", arm, field)
            target = u.reg_read(UC_ARM_REG_R0)
            raw = bytes(u.mem_read(src, 128)).split(b"\0", 1)[0]
            assert raw == bytes(u.mem_read(target, 128)).split(b"\0", 1)[0]
            texts.append(dict(pointer_field=BASE + field, runtime_pointer=src, exact_text=raw.decode("cp932")))
            side_exit(u, int(answer))
        elif offset == 0xEEFD0:
            status.append(u.reg_read(UC_ARM_REG_R0))
            side_exit(u)
        elif offset == WRITE:
            address, buf, size = (u.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2))
            expected = [(SYSTEM_OFFSET, SYSTEM_SIZE), (slot * SLOT_SIZE, SLOT_SIZE)]
            assert (address, size) == expected[len(writes)]
            ok = len(writes) != failed
            digest = checked_payload(u, address, buf, size, slot)
            writes.append(dict(backup_offset=address, bytes=size, supplied_success=ok, data_sha256=digest))
            side_exit(u, int(ok))
        elif offset == MODAL:
            notices.append(notice_pointer(u, arm, 0xEEF50))
            u.emu_stop()
        elif offset in ui_calls:
            side_exit(u)
        elif offset in EARLIER_FRAGMENTS:
            raise AssertionError(f"Unexpected Save COMMON lookup at {pc:#x}")

    cpu.hook_add(UC_HOOK_CODE, observe)
    pc, value = start(cpu, SLOT_WRITER, (1 if overwrite else 2, slot, ENTRIES))
    assert len(texts) == 1
    if not answer:
        assert not writes and not status and not notices and (pc, value) == (STOP, 1)
    elif failed is None:
        assert len(writes) == 2 and status == [0x33, 0x32] and not notices and (pc, value) == (STOP, 0)
    else:
        assert len(writes) == failed + 1 and status == [0x33, 0x32][:failed + 1]
        assert len(notices) == 1 and pc == BASE + MODAL
    return dict(slot=slot + 1, occupied=overwrite, supplied_agreement=answer, confirmations=texts,
        progress_modes=status, cartridge_writes=writes, notices=notices, reached_native_return=pc == STOP)


def comparable(row):
    return {k: ([{field: b for field, b in item.items() if field != "exact_text"} for item in v]
                if k in ("confirmations", "notices") else v) for k, v in row.items()}


def entirety(ja, en):
    regions = ((TITLE, 0x3EC10), (0xED708, 0xED7EC), (0xEEF58, 0xEEFB0), (SLOT_WRITER, 0xEEC50),
               (0xEEC50, 0xEECA0), (0xEEF24, 0xEEF58), (WRITE, 0xD644C))
    for start_offset, end_offset in regions:
        assert ja[start_offset:end_offset] == en[start_offset:end_offset]
    return {f"{BASE + a:08x}-{BASE + b:08x}": native.digest(en[a:b]) for a, b in regions}


def cases(ja, en):
    results = {"title": [], "save": []}
    tests = [("title", new_game, (occupied, system, None))
             for occupied in ((), (0,), (5,), tuple(range(SLOT_COUNT))) for system in (False, True)]
    tests += [("title", new_game, ((0,), True, fault)) for fault in ((6, 4), (0, 0x7C))]
    tests += [("save", save_slot, (slot, occupied, True, None)) for slot in range(SLOT_COUNT) for occupied in (False, True)]
    tests += [("save", save_slot, (1, occupied, answer, failed))
              for occupied in (False, True) for answer, failed in ((False, None), (True, 0), (True, 1))]
    for group, run, inputs in tests:
        clean, active = (run(arm, *inputs) for arm in (ja, en))
        assert comparable(clean) == comparable(active)
        results[group].append(dict(registered=active, clean_notices=clean["notices"],
            clean_confirmations=clean.get("confirmations", [])))
    return results, len(tests) * 2


def main():
    release, review, previous, header, inventory = map(base.load, (current.RELEASE, current.REVIEW, PREVIOUS, HEADER_CHECK, WORKLIST))
    ours = release["candidate_sha256"]
    assert base.digest(current.ROM) == ours == review["candidate_sha256"] == previous["candidate_sha256"] == header["candidate_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"] and base.digest(base.REGISTRY) == release["registry_sha256"]
    clean, active = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    ja, en = (rom.read_file(current.ARM) for rom in (clean, active))
    common = active.read_file(current.COMMON)
    assert native.digest(en) == release["target_ARM9_sha256"] and native.digest(common) == release["target_COMMON_sha256"]
    source = common_message_entries(clean.read_file(current.COMMON), ja)
    installed = owned_entries(common, en, native.digest(en[DIRECTORY_OFFSET:TABLE_OFFSET]))
    worklist = {row["message_ID"]: row for row in inventory["records"]}
    binding = {row["message_ID"]: row for row in review["shared_consumer_binding"]["records"]}
    assert len(binding) == len(worklist) == 276
    before = set(previous["remaining_without_scoped_disposition"])
    assert len(before) == 13 and SAVE_SPACE.keys() <= before
    spans = entirety(ja, en)
    outcomes, runs = cases(ja, en)
    reviews = []
    for key, (kind, count) in SAVE_SPACE.items():
        row = stored_record(key, source, installed, worklist, binding)
        row.update(source_record_kind=kind, original_free_block_count=count,
            verified_scope="Native title choice after cartridge enumeration." if key < 111 else "Native Save confirmation and writes to fixed cartridge addresses.",
            checked_DS_outcome=("The title checks for existing saves to set Continue, then accepts New Game." if key < 111 else
                "A cancelled confirmation does not write. The accepted branch writes the system record then the selected slot, or enters the card write warning on failure."))
        reviews.append(row)
    remaining = sorted(before - SAVE_SPACE.keys())
    base.save(OUT, dict(candidate_sha256=ours, reviewed_entries=reviews, remaining_without_scoped_disposition=remaining,
        native_code_spans=spans, verified_case_pairs=outcomes, offline_native_runs=runs,
        hardware_or_gameplay_runs=0, new_ROM=False, reused_ordinary_save=previous["current_save_write"],
        exact_source_checks={str(p): base.digest(p) for p in (PREVIOUS, HEADER_CHECK, current.RELEASE, current.REVIEW, WORKLIST, Path(__file__))}))
    print(f"Verified {runs} paired native title and save runs; {len(remaining)} shared entries remain.")


if __name__ == "__main__":
    main()
