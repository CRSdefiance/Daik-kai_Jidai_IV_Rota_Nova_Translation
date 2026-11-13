"""Replay complete live branches; retain, rather than waive, return-state gaps."""

import argparse
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from unicorn import UC_HOOK_CODE, arm_const

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine
from scripts.run_room_gender_v694 import CAP, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save


def cpu(row):
    return struct.unpack('<32I', bytes.fromhex(row['CPU128_hex']))


def data(row, key):
    raw = Path(row[key]).read_bytes()
    assert sha(raw) == row[key + '_sha256']
    return raw


def main(case):
    events = read(CAP / ('room_gender_v694_' + case + '_ITCM') / 'observer/events.json')
    assert not events['errors'] and events['all_recorded_CPU_and_ITCM_state_preserved_by_extension']
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    rom = NdsImage.open(ROM)
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x157D8:0x15948] == clean[0x157D8:0x15948]
    expected_code = machine(arm)
    expected_code.mem_write(POOL, bytes(MainCodeFile(arm, 0x02000000).sections[3].data[:-48]))
    overlay = loadOverlayTable(rom.rom.arm9OverlayTable, lambda _, f: rom.rom.files[f])[0]
    expected_code.mem_write(overlay.ramAddress, bytes(overlay.data))
    groups = {}
    for row in events['rows']:
        groups.setdefault(row['call_number'], []).append(row)
    regs = [getattr(arm_const, 'UC_ARM_REG_R' + str(i)) for i in range(13)]
    regs += [arm_const.UC_ARM_REG_SP, arm_const.UC_ARM_REG_LR]
    results = []
    for call_number, rows in groups.items():
        assert rows[0]['kind'] == 'cast_done' and rows[-1]['kind'] == 'after_gender_or_bypass'
        start, ending = rows[0], rows[-1]
        initial = cpu(start)
        raw, dtcm, itcm = (data(start, key) for key in ('RAM', 'DTCM', 'ITCM'))
        assert len(raw) == 0x400000 and len(dtcm) == 0x4000 and len(itcm) == 0x8000
        assert int.from_bytes(bytes.fromhex(start['MDTC_hex']), 'little') == 0x027E0000
        u = machine(arm)
        u.mem_write(0x02000000, raw)
        u.mem_write(0x027E0000, dtcm)
        u.mem_write(0x01FF0000, itcm)
        u.mem_write(0x01FF8000, itcm)
        # The pinned core reads low addresses from actual ITCM, not zero-filled
        # host memory. Keep this explicit bounded mirror for optional text reads.
        u.mem_map(0, 0x8000)
        u.mem_write(0, itcm)
        # armcpu.h places saved SVC/ABT/UND/IRQ SP/LR pairs in CPU128 words24..31.
        # OS context save/restore changes modes even during text setup. The
        # standalone harness's invented banked stacks are not this live state.
        for mode, offset in ((0x13, 24), (0x17, 26), (0x1B, 28), (0x12, 30)):
            u.reg_write(arm_const.UC_ARM_REG_CPSR, (initial[20] & ~0x3F) | mode)
            u.reg_write(arm_const.UC_ARM_REG_SP, initial[offset])
            u.reg_write(arm_const.UC_ARM_REG_LR, initial[offset + 1])
        u.reg_write(arm_const.UC_ARM_REG_CPSR, initial[20])
        for reg, value in zip(regs, initial[4:19], strict=True):
            u.reg_write(reg, value)
        checkpoints = {cpu(r)[2]: r for r in rows}
        reached, instructions = [], set()

        def code(uc, pc, size, unused, instructions=instructions, checkpoints=checkpoints, reached=reached):
            key = (pc, size)
            if key not in instructions:
                assert bytes(uc.mem_read(pc, size)) == bytes(expected_code.mem_read(pc, size)), hex(pc)
                instructions.add(key)
            if pc in checkpoints:
                row = checkpoints[pc]
                state = cpu(row)
                assert [uc.reg_read(r) for r in regs] == list(state[4:19]), (row['kind'], 'registers')
                assert uc.reg_read(arm_const.UC_ARM_REG_CPSR) == state[20], (row['kind'], 'CPSR')
                assert bytes(uc.mem_read(0x02000000, 0x400000)) == data(row, 'RAM'), (row['kind'], 'RAM')
                assert bytes(uc.mem_read(0x027E0000, 0x4000)) == data(row, 'DTCM'), (row['kind'], 'DTCM')
                assert bytes(uc.mem_read(0x01FF8000, 0x8000)) == data(row, 'ITCM'), (row['kind'], 'ITCM')
                reached.append(row['kind'])
        hook = u.hook_add(UC_HOOK_CODE, code)
        try:
            u.emu_start(initial[2], cpu(ending)[2], count=1000000)
        except Exception as exc:
            save(ROOT / f'native_{case}_failure.json', {'call_number': call_number, 'error': repr(exc),
                'PC': u.reg_read(arm_const.UC_ARM_REG_PC), 'reached': reached,
                'script_sha256': sha(Path(__file__).read_bytes())})
            raise
        finally:
            u.hook_del(hook)
        assert u.reg_read(arm_const.UC_ARM_REG_PC) == cpu(ending)[2]
        assert reached == [r['kind'] for r in rows[:-1]]
        expected = cpu(ending)
        assert [u.reg_read(r) for r in regs] == list(expected[4:19])
        assert u.reg_read(arm_const.UC_ARM_REG_CPSR) == expected[20]
        actual_ram, expected_ram = bytes(u.mem_read(0x02000000, 0x400000)), data(ending, 'RAM')
        if actual_ram != expected_ram:
            differences = [i for i, (a, b) in enumerate(zip(actual_ram, expected_ram, strict=True)) if a != b]
            save(ROOT / f'native_{case}_RAM_diagnostic.json', {'call_number': call_number,
                'changed_bytes': len(differences), 'differences': [
                    {'address': 0x02000000 + i, 'actual': actual_ram[i], 'expected': expected_ram[i]}
                    for i in differences],
                'DTCM_exact': bytes(u.mem_read(0x027E0000, 0x4000)) == data(ending, 'DTCM'),
                'ITCM_exact': bytes(u.mem_read(0x01FF8000, 0x8000)) == data(ending, 'ITCM')})
        actual_dtcm = bytes(u.mem_read(0x027E0000, 0x4000))
        actual_itcm = bytes(u.mem_read(0x01FF8000, 0x8000))
        ram_differences = [{'address': 0x02000000 + i, 'actual': a, 'expected': b}
                           for i, (a, b) in enumerate(zip(actual_ram, expected_ram, strict=True)) if a != b]
        dtcm_differences = [{'address': 0x027E0000 + i, 'actual': a, 'expected': b}
                            for i, (a, b) in enumerate(zip(actual_dtcm, data(ending, 'DTCM'), strict=True)) if a != b]
        state_exact = not ram_differences and not dtcm_differences and actual_itcm == data(ending, 'ITCM')
        result = {'call_number': call_number, 'frame': start['frame'],
            'key': start['original_view_actor_parent_selected_room_key'],
            'helper_entered': ending['helper_entered'], 'complete_native_checkpoints': reached + [ending['kind']],
            'all_recorded_intermediate_checkpoint_registers_CPSR_RAM_DTCM_ITCM_exact': True,
            'return_registers_and_CPSR_exact': True,
            'return_whole_RAM_DTCM_ITCM_exact': state_exact,
            'return_RAM_differences_unwaived': ram_differences,
            'return_DTCM_differences_unwaived': dtcm_differences,
            'return_ITCM_exact': actual_itcm == data(ending, 'ITCM'),
            'entry_and_return_frames': [start['frame'], ending['frame']],
            'actual_low_ITCM_mirror_model_no_native_call_or_text_renderer_bridge': True,
            'unique_registered_code_instructions': len(instructions),
            'registered_code_sha256': sha(b''.join(struct.pack('<II', pc, size)
                + bytes(expected_code.mem_read(pc, size)) for pc, size in sorted(instructions)))}
        results.append(result)
        print('V694 native room/gender', case, call_number, ending['helper_entered'], reached, flush=True)
    save(ROOT / f'native_{case}_proof.json', {'cases': results,
        'complete_branch_return_state_proven': all(r['return_whole_RAM_DTCM_ITCM_exact'] for r in results),
        'no_mismatch_removed_or_replaced_by_expected_state': True,
        'actual_main_DTCM_ITCM_source_and_all_registered_code_verified': True,
        'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('case', choices=('hodram', 'maria'))
    main(parser.parse_args().case)
