"""Replay complete original actor/flag/gender construction prefixes from live state.

The stop is the recorded completed gender-view construction, not the return of
the larger info/portrait update. V694's separate suffix-memory gap is retained.
"""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from unicorn import UC_HOOK_CODE, arm_const

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine
from scripts.replay_room_gender_v694 import cpu, data
from scripts.run_gender_exception_v697 import CAP, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    registered = machine(arm)
    registered.mem_write(POOL, bytes(MainCodeFile(arm, 0x02000000).sections[3].data[:-48]))
    overlay = loadOverlayTable(rom.rom.arm9OverlayTable, lambda _, f: rom.rom.files[f])[0]
    registered.mem_write(overlay.ramAddress, bytes(overlay.data))
    regs = [getattr(arm_const, 'UC_ARM_REG_R' + str(i)) for i in range(13)]
    regs += [arm_const.UC_ARM_REG_SP, arm_const.UC_ARM_REG_LR]
    results = []
    for flag in (0, 1):
        events = read(CAP / f'gender_exception_v697_flag{flag}_observed/observer/events.json')
        rows = events['rows'][:7]
        assert [r['kind'] for r in rows] == ['selection_entry', 'helper_entry', 'raw_gender',
            'identity', 'flag_entry', 'flag_return', 'view_ready']
        start, end = rows[0], rows[-1]
        initial = cpu(start)
        raw, dtcm, itcm = [data(start, name) for name in ('RAM', 'DTCM', 'ITCM')]
        u = machine(arm)
        u.mem_write(0x02000000, raw)
        u.mem_write(0x027E0000, dtcm)
        u.mem_write(0x01FF0000, itcm)
        u.mem_write(0x01FF8000, itcm)
        u.mem_map(0, 0x8000)
        u.mem_write(0, itcm)
        for mode, offset in ((0x13, 24), (0x17, 26), (0x1B, 28), (0x12, 30)):
            u.reg_write(arm_const.UC_ARM_REG_CPSR, (initial[20] & ~0x3F) | mode)
            u.reg_write(arm_const.UC_ARM_REG_SP, initial[offset])
            u.reg_write(arm_const.UC_ARM_REG_LR, initial[offset + 1])
        u.reg_write(arm_const.UC_ARM_REG_CPSR, initial[20])
        for reg, value in zip(regs, initial[4:19], strict=True):
            u.reg_write(reg, value)
        checkpoints = {cpu(r)[2]: r for r in rows}
        reached, executed = [], set()

        def compare(uc, row):
            state = cpu(row)
            assert [uc.reg_read(r) for r in regs] == list(state[4:19]), row['kind']
            assert uc.reg_read(arm_const.UC_ARM_REG_CPSR) == state[20]
            for address, field in ((0x02000000, 'RAM'), (0x027E0000, 'DTCM'), (0x01FF8000, 'ITCM')):
                expected = data(row, field)
                assert bytes(uc.mem_read(address, len(expected))) == expected, (row['kind'], field)

        def code(uc, pc, size, unused, checkpoints=checkpoints, reached=reached, executed=executed):
            if (pc, size) not in executed:
                assert bytes(uc.mem_read(pc, size)) == bytes(registered.mem_read(pc, size)), hex(pc)
                executed.add((pc, size))
            if pc in checkpoints:
                row = checkpoints[pc]
                compare(uc, row)
                reached.append(row['kind'])
        hook = u.hook_add(UC_HOOK_CODE, code)
        try:
            u.emu_start(initial[2], cpu(end)[2], count=1000000)
        finally:
            u.hook_del(hook)
        assert u.reg_read(arm_const.UC_ARM_REG_PC) == cpu(end)[2]
        compare(u, end)
        assert reached == [r['kind'] for r in rows[:-1]]
        results.append({'flag9': flag, 'start_PC': initial[2], 'stop_PC': cpu(end)[2],
            'all7_actual_R0_R14_CPSR_RAM_DTCM_ITCM_checkpoints_exact': True,
            'actual_flag_getter_return': cpu(rows[-2])[4], 'processed_selector': cpu(end)[12],
            'native_flag_query_and_view_constructor_execute_without_bridges': True,
            'unique_registered_instructions': len(executed),
            'code_sha256': sha(b''.join(struct.pack('<II', pc, size)
                + bytes(registered.mem_read(pc, size)) for pc, size in sorted(executed)))})
    save(ROOT / 'native_prefix_proof.json', {'cases': results,
        'complete_selected_actor_to_gender_construction_prefixes_no_native_calls_bridged': True,
        'not_full_info_update_return_equivalence_V694_suffix_gap_remains_open': True,
        'replayer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V697 both full original selection-to-gender construction prefixes match all14 actual R0-R14/CPSR/RAM/DTCM/ITCM checkpoints.', flush=True)


if __name__ == '__main__':
    main()
