"""Identify the two uses of the graphics table that contains COMMON key 3584's number."""

from pathlib import Path
from struct import unpack_from

from unicorn import UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R5, UC_ARM_REG_SP

from scripts import reconcile_shared_display_20261121 as shared
from scripts import register_rafael_mediterranean_followups_20261123 as release
from scripts.probe_button_prompt_native import BASE, STACK, machine


base, native = release.base, release.native
TABLE = 0x0214532C
SELECT, PARAMETER = 0x04000488, 0x0400048C
POINTERS = (0x0206C500, 0x020F5788)
LOADERS = (
    (0x0206C3C8, 0x0206C4A8, (0x0206C40C, 0x0206C444, 0x0206C468, 0x0206C488)),
    (0x020F4EF4, 0x020F4FC4, (0x020F4F2C, 0x020F4F58, 0x020F4F7C, 0x020F4FA0)),
)
OUTPUT = Path("translations/editorial_checkpoints/shared_display_20261123/graphics_table_3584.json")
INVENTORY = Path("work/analysis/remaining_common_numeric_references_clean.json")


def word(arm, address):
    return unpack_from("<I", arm, address - BASE)[0]


def trace(arm, index):
    pointer = POINTERS[index]
    start, stop, expected_reads = LOADERS[index]
    assert word(arm, pointer) == TABLE
    u = machine(arm)
    u.mem_map(0x04000000, 0x1000)
    if index == 0:
        assert (word(arm, 0x0206C504), word(arm, 0x0206C50C)) == (SELECT, PARAMETER)
        u.emu_start(0x0206C3B8, 0x0206C3BC, count=1)
        u.reg_write(UC_ARM_REG_R5, 0)
    else:
        assert (word(arm, 0x020F5710), word(arm, 0x020F5718)) == (SELECT, PARAMETER)
        u.emu_start(0x020F4AAC, 0x020F4AB8, count=3)
        u.reg_write(UC_ARM_REG_SP, STACK)
    u.reg_write(UC_ARM_REG_R0, 0)
    u.reg_write(UC_ARM_REG_R1, 0)
    reads, writes, literals = [], [], []
    u.hook_add(UC_HOOK_MEM_READ, lambda cpu, _, at, size, __, ___: reads.append(
        (cpu.reg_read(UC_ARM_REG_PC), at, size)), begin=TABLE, end=TABLE+15)
    u.hook_add(UC_HOOK_MEM_READ, lambda cpu, _, at, size, __, ___: literals.append(
        (cpu.reg_read(UC_ARM_REG_PC), at, size)), begin=pointer, end=pointer+3)
    u.hook_add(UC_HOOK_MEM_WRITE, lambda cpu, _, at, size, value, __: writes.append(
        (cpu.reg_read(UC_ARM_REG_PC), at, size, value)), begin=SELECT, end=PARAMETER+3)
    u.emu_start(start, stop, count=160)
    assert u.reg_read(UC_ARM_REG_PC) == stop
    selected = [entry for entry in writes if entry[1] == SELECT]
    slots = [TABLE + 4 * slot for slot in (3, 2, 1, 0)]
    assert reads == [(pc, at, 4) for pc, at in zip(expected_reads, slots, strict=True)]
    assert len(literals) == (1 if index == 0 else 4) and all(at == pointer and size == 4 for _, at, size in literals)
    assert [(at, size, value) for _, at, size, value in selected] == [(SELECT, 4, word(arm, at)) for at in slots]
    assert len([entry for entry in writes if entry[1] == PARAMETER]) == 8
    assert selected[-1][3] == word(arm, TABLE) == 0x00D00E00
    return dict(instruction_range=(start, stop), initial_selection=0, pointer_reads=literals,
                table_reads=reads, graphics_IO_writes=writes)


def main():
    registered = base.load(release.RELEASE)
    active = base.digest(release.ROM)
    assert active == registered["candidate_sha256"] and base.digest(base.REGISTRY) == registered["registry_sha256"]
    assert base.digest(native.CLEAN) == registered["clean_input_sha256"]
    clean, current = map(base.NdsImage.open, (native.CLEAN, release.ROM))
    before, after = [image.read_file(shared.ARM) for image in (clean, current)]
    assert native.digest(after) == registered["target_ARM9_sha256"]
    assert native.digest(current.read_file(shared.COMMON)) == registered["target_COMMON_sha256"]
    cases = [trace(before, i) for i in range(2)]
    assert cases == [trace(after, i) for i in range(2)]

    message_ID = word(before, TABLE) & 0xFFFF
    assert message_ID == 3584
    source = shared.workflow.common_message_entries(clean.read_file(shared.COMMON), before)[message_ID]
    installed = shared.entries(current)[message_ID]
    row, = [r for r in base.load(shared.OUTPUT)["records"] if r["message_ID"] == message_ID]
    assert shared.workflow.reference(source) == row["source_reference"] and source.text.hex() == row["source_hex"]
    assert shared.workflow.reference(installed) == row["current_reference"] and installed.text.hex() == row["current_hex"]
    assert not OUTPUT.exists()
    base.save(OUTPUT, dict(candidate_sha256=active, arm_sha256=native.digest(after), common_sha256=registered["target_COMMON_sha256"],
        clean_arm_sha256=native.digest(before), graphics_table_address=TABLE, literal_pointers=POINTERS,
        raw_table_word=word(before, TABLE), low_halfword=message_ID, native_graphics_reads_and_writes=cases,
        inventory=dict(path=str(INVENTORY), sha256=base.digest(INVENTORY)), shared_record=row,
        isolated_native_traces=True, player_facing_COMMON_display_gate_open=True, new_gameplay_runs=0,
        new_editorial_credit=0))
    print("Both address matches read the packed graphics word and write it to the graphics I/O register.")


if __name__ == "__main__":
    main()
