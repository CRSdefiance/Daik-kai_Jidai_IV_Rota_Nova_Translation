"""Replay original whole Sailor Info update prefixes through gender construction."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from unicorn import UC_HOOK_CODE, arm_const

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine
from scripts.replay_room_gender_v694 import cpu, data
from scripts.run_person_gender_v698 import CAP, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
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
        events = read(CAP / f'person_gender_v698_screen1_flag{flag}_observed/observer/events.json')
        assert events['producer_sha256'] == pre['producer_sha256'] and not events['errors']
        for number in (1, 2):
            rows = [r for r in events['rows'] if r['call'] == number and r['kind'] != 'gender_draw']
            assert [r['kind'] for r in rows] == ['update_entry', 'actor_ready', 'raw_gender', 'identity',
                'flag_entry', 'flag_return', 'processed', 'view_ready']
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
                assert [uc.reg_read(r) for r in regs] == list(state[4:19]), (row['kind'], 'registers')
                assert uc.reg_read(arm_const.UC_ARM_REG_CPSR) == state[20], (row['kind'], 'CPSR')
                for address, field in ((0x02000000, 'RAM'), (0x027E0000, 'DTCM'), (0x01FF8000, 'ITCM')):
                    expected = data(row, field)
                    actual = bytes(uc.mem_read(address, len(expected)))
                    if actual != expected:
                        diffs = [{'address': address + i, 'actual': a, 'expected': b}
                                 for i, (a, b) in enumerate(zip(actual, expected, strict=True)) if a != b]
                        save(ROOT / f'native_flag{flag}_call{number}_{field}_failure.json',
                             {'kind': row['kind'], 'differences': diffs})
                    assert actual == expected, (row['kind'], field)

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
                assert u.reg_read(arm_const.UC_ARM_REG_PC) == cpu(end)[2]
                compare(u, end)
                assert reached == [r['kind'] for r in rows[:-1]]
            except Exception as exc:
                save(ROOT / f'native_flag{flag}_call{number}_failure.json',
                    {'error': repr(exc), 'PC': u.reg_read(arm_const.UC_ARM_REG_PC), 'reached': reached})
                raise
            finally:
                u.hook_del(hook)
            results.append({'flag9': flag, 'call': number, 'start_PC': initial[2], 'stop_PC': cpu(end)[2],
                'all8_actual_R0_R14_CPSR_RAM_DTCM_ITCM_checkpoints_exact': True,
                'original_getter_return': cpu(rows[5])[4], 'processed_selector': cpu(rows[6])[8],
                'unique_registered_instructions': len(executed),
                'all_native_actor_stats_portrait_flag_and_view_setup_calls_execute_without_bridges': True,
                'code_sha256': sha(b''.join(struct.pack('<II', pc, size)
                    + bytes(registered.mem_read(pc, size)) for pc, size in sorted(executed)))})
    save(ROOT / 'native_prefix_proof.json', {'cases': results,
        'all4_complete_original_update_prefixes32_recorded_states_exact': True,
        'not_full_info_update_suffix_equivalence_or_V694_suffix_gap_clearance': True,
        'replayer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V698 four full original update-to-gender prefixes match all32 recorded R0-R14/CPSR/RAM/DTCM/ITCM states.', flush=True)


if __name__ == '__main__':
    main()
