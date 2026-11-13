"""Verify the original ship-command descriptor with an explicit modal boundary."""

import struct
from hashlib import sha256
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2

from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.native_call_abi_v764 import call
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


ROOT = Path('translations/editorial_checkpoints/SharedText_20261110_v1')
OUTPUT = ROOT / 'ship_command_native_descriptor.json'
BASE = 0x02000000
TABLE = 0x1150B0
HELPER = 0x51E7C
BOUNDARY = 0x51FC0


def main():
    assert not OUTPUT.exists()
    comparison = ROOT / 'contextual_comparison_pending_consumers.json'
    proof = load(comparison)
    ctx = RegisteredRuntime('work/lil261_B323_B335_release_v1/registered_release_verification.json',
        'work/lil261_B323_B335_release_v1/own_registered_startup_verification.json', captain=3)
    assert ctx.release['candidate_sha256'] == proof['candidate_sha256']
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = [(0x2C4C4, 0x2C598), (0x2C654, 0x2C658), (HELPER, 0x51EE0), (TABLE, TABLE + 8)]
    code = []
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    for start, end in spans:
        assert ctx.arm[start:end] == clean[start:end]
        code.append(dict(offset=start, bytes=end-start, source_andcurrent_hex=clean[start:end].hex(),
            disassembly=[dict(address=i.address, mnemonic=i.mnemonic, operands=i.op_str)
                         for i in md.disasm(clean[start:end], BASE+start)]))
    assert struct.unpack_from('<I', ctx.arm, 0x2C654)[0] == BASE + TABLE
    assert struct.unpack_from('<I', ctx.arm, TABLE+4)[0] == BASE + 0x134E54
    cpu, get, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    before = bytes(cpu.mem_read(BASE+TABLE, 8))
    events = []
    selected = 0

    def modal_boundary(u, pc, size, unused):
        descriptor = u.reg_read(UC_ARM_REG_R0)
        data = bytes(u.mem_read(descriptor, 20))
        words = struct.unpack('<5I', data)
        assert (u.reg_read(UC_ARM_REG_R1), u.reg_read(UC_ARM_REG_R2)) == (1, 1)
        assert words[1:4] == (BASE+TABLE, 2, 0)
        assert words[4] in [0, 1]
        events.append(dict(descriptor_hex=data.hex(), table_pointer=words[1],
            entries=words[2], initial_selection=words[4], supplied_modal_return=selected))
        u.reg_write(UC_ARM_REG_R0, selected & 0xFFFFFFFF)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    hook = cpu.hook_add(UC_HOOK_CODE, modal_boundary, begin=BASE+BOUNDARY, end=BASE+BOUNDARY)
    cases = []
    for initial in [-1, 0, 1]:
        for selected in [-1, 0, 1]:
            count = len(events)
            call(cpu, HELPER, (BASE+TABLE, 2, 0, initial & 0xFFFFFFFF))
            assert cpu.reg_read(UC_ARM_REG_R0) == selected & 0xFFFFFFFF
            assert len(events) == count+1
            assert events[-1]['initial_selection'] == (1 if initial == -1 else initial)
            cases.append(dict(initial=initial, modal_return=selected, returned_native_value=selected,
                descriptor=events[-1], complete_saved_register_stack_andreturn_ABI=True))
    count = len(events)
    call(cpu, HELPER, (BASE+TABLE, 0, 0, 0))
    assert cpu.reg_read(UC_ARM_REG_R0) == 0xFFFFFFFF and len(events) == count
    cpu.hook_del(hook)
    assert bytes(cpu.mem_read(BASE+TABLE, 8)) == before
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    executed = sorted(provider.executed_current)
    assert executed and all(BASE+HELPER <= pc < BASE+0x51ED8 or pc == BASE+BOUNDARY for pc in executed)
    save(OUTPUT, dict(runtime=ctx.receipt(), source_andcurrent_spans=code,
        cases=cases, zero_count_returns_minus_one_without_modal_call=True,
        ship_command_table=BASE+TABLE, ship_command_index=1, pointer_field=TABLE+4,
        current_ship_command='船を捨てる', proposed_English='Abandon Ship',
        original_caller_loads_exact_table_andcalls_original_descriptor_helper=True,
        all_executed_instructions_exact_registered_code=True, executed_addresses=executed,
        table_actor_bytes_stack_and_saved_registers_preserved=True,
        modal_UI_creation_at_02051FC0_is_an_explicit_unexecuted_boundary=True,
        supplied_modal_result_is_offline_ABI_test_input_not_observed_gameplay=True,
        font_bounds_cursor_pagination_transitions_andactual_command_outcome_pending=True,
        replacement_storage_andpointer_integration_pending=True,
        original_event_conditions_andactual_gameplay_not_tested=True,
        new_ROM=False, new_completion_credit=0, guide_photos=False, full_goal_complete=False,
        evidence={str(p):digest(p) for p in [comparison, Path(__file__)]}))
    print('PASS nine native ship-command descriptor cases and the zero-count branch. Modal rendering remains pending.')


if __name__ == '__main__':
    main()
