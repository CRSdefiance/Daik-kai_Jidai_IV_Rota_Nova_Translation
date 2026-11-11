"""Prove that only the original crew notice IDs and three portrait pairs change dispatch."""

import struct
from itertools import product
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2
from unicorn.arm_const import UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.patch.crew_loss_portrait_wrap_v1 import ENTRY, LEGACY, SCOPE, WRAPPER
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_crew_notices_v1 import ARM, OUT
from scripts.probe_button_prompt_native import STACK, STOP, machine
from scripts.town_trend_balanced_runtime_v2162 import BASE, TABLE, decode


PROOF = OUT / 'native_preflight.json'
RESULT = OUT / 'selector_scope.json'
ARGS = (0x0242E000, 0x0242D000, 0x02116EC0, 0xA5A53412)
REGISTERS = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)


def dispatch(cpu, address, stack, targets):
    for offset, value in stack.items():
        cpu.mem_write(STACK + offset, struct.pack('<I', value))
    for register, value in zip(REGISTERS, ARGS, strict=True):
        cpu.reg_write(register, value)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    found = []

    def stop(u, pc, size, data):
        found.append(pc)
        u.emu_stop()

    hooks = [cpu.hook_add(UC_HOOK_CODE, stop, begin=p, end=p) for p in targets]
    try:
        cpu.emu_start(address, STOP, count=128)
    finally:
        for hook in hooks:
            cpu.hook_del(hook)
    pc, = found
    assert pc == cpu.reg_read(UC_ARM_REG_PC)
    assert cpu.reg_read(UC_ARM_REG_SP) == STACK and cpu.reg_read(UC_ARM_REG_LR) == STOP
    values = tuple(cpu.reg_read(reg) for reg in REGISTERS)
    return pc, values


def main():
    assert not RESULT.exists()
    proof = load(PROOF)
    before, after = (NdsImage.open(path).read_file(ARM) for path in (
        proof['runtime']['candidate'], proof['research_ROM']))
    assert digest(proof['research_ROM']) == proof['research_ROM_sha256']
    original, candidate = machine(before), machine(after)
    legacy_rows, used = decode(before[TABLE - BASE:TABLE - BASE + 212])
    assert used == 212
    assert after[TABLE - BASE:TABLE - BASE + used] == before[TABLE - BASE:TABLE - BASE + used]
    pairs = {(parent, table) for parent, values in SCOPE.items() for table in values}
    controls = {(parent, offset, value) for parent, offset, _, values in legacy_rows for value in values}
    assert all((parent, 0x274, value) not in controls for parent, value in pairs)
    parents = {p for p, _, _, _ in legacy_rows} | set(SCOPE) | {0x02053EF0, 0x02053EF8, 0x03053F40}
    for parent, table in product(parents, {v for _, v in pairs}):
        for value in (table - 4, table, table + 4, 0x03000000 | (table & 0xFFFFFF)):
            controls.add((parent, 0x274, value))
    for parent, offset, value in sorted(controls):
        stack = {0x264: parent, 0x270: 0, 0x274: 0, 0x27C: 0, offset: value}
        old, new = (dispatch(cpu, ENTRY, stack, (LEGACY, WRAPPER)) for cpu in (original, candidate))
        expected = WRAPPER if offset == 0x274 and (parent, value) in pairs else LEGACY
        assert old == (LEGACY, ARGS) and new == (expected, ARGS), (parent, offset, value, old, new)

    # Start at the existing shared-notice gate after its parent check. The other
    # branch is checked separately to confirm it cannot enter the crew path.
    modal_entry = 0x01FFD020
    modal_targets = (0x01FFC900, 0x01FFD04C, 0x01FF9FAC)
    unchanged, selected = 0, []
    for number in range(3668):
        stack = {0xC4: 0x020546E8, 0xD0: number}
        a = dispatch(original, modal_entry, stack, modal_targets)
        # The literal helper uses one saved return address. Stop at the
        # selector before its prologue so both branches have the same ABI check.
        b = dispatch(candidate, modal_entry, stack,
            (*modal_targets[:2], proof['selector']['modal_literal_copy_selector'] + 16))
        if number in (338, 339):
            assert a[0] == modal_targets[0] and b[0] == proof['selector']['modal_literal_copy_selector'] + 16
            selected.append(number)
        else:
            assert a == b
            unchanged += 1
    for parent, number in product((0x020546E4, 0x020546EC, 0x02054720, 0x02054764), (338, 339)):
        stack = {0xC4: parent, 0xD0: number}
        a, b = (dispatch(cpu, modal_entry, stack, modal_targets) for cpu in (original, candidate))
        assert a == b and a[0] == modal_targets[0]
    assert selected == [338, 339] and unchanged == 3666
    save(RESULT, dict(research_ROM_sha256=proof['research_ROM_sha256'], portrait_pairs=sorted(pairs),
        exact_portrait_controls=len(controls), original_table_preserved=True,
        modal_unchanged_IDs=unchanged, modal_literal_IDs=selected, modal_wrong_parent_controls=8,
        handoff_stack_registers_and_return_exact=True, branch_scope_only=True,
        evidence={str(p): digest(p) for p in (PROOF, Path(__file__))}))
    print(f'{len(controls)} portrait dispatches and 3668 modal ID dispatches pass.')


if __name__ == '__main__':
    main()
