"""Verify every predecessor paint and all executed words against registered ROM code."""

import argparse
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from unicorn import UC_HOOK_CODE

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts import replay_filter_clock_v693 as replay
from scripts.probe_button_prompt_native import machine
from scripts.run_filter_predecessors_v693 import ROOT
from scripts.verify_village_wrap_v608 import read, save


def main(case):
    pre = read(ROOT / 'preflight.json')
    path = Path(pre['cases'][case]['ROM'])
    assert sha(path.read_bytes()) == pre['cases'][case]['ROM_sha256']
    rom = NdsImage.open(path)
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0xF9C:0xFF4] == clean[0xF9C:0xFF4]
    assert arm[0xD32B8:0xD331C] == clean[0xD32B8:0xD331C]
    expected = machine(arm)
    expected.mem_write(POOL, bytes(MainCodeFile(arm, 0x02000000).sections[3].data[:-48]))
    overlay = loadOverlayTable(rom.rom.arm9OverlayTable, lambda _, file: rom.rom.files[file])[0]
    expected.mem_write(overlay.ramAddress, bytes(overlay.data))
    events = read(replay.CAP / ('filter_clock_v693_' + case) / 'clock_observer/events.json')
    replay.ROOT = ROOT
    original_setup, code_words = replay.setup, set()

    def traced_setup(*args, **kwargs):
        u, mapping = original_setup(*args, **kwargs)

        def code(uc, pc, size, unused):
            assert bytes(uc.mem_read(pc, size)) == bytes(expected.mem_read(pc, size)), hex(pc)
            code_words.add((pc, size))
        u.hook_add(UC_HOOK_CODE, code)
        return u, mapping

    replay.setup = traced_setup
    results = []
    try:
        for index in range(len(events['paints'])):
            code_words.clear()
            row = replay.replay(case, index)
            assert row['complete_output_bytes_different_from_actual_return'] == 0
            assert row['bytes_written'] == 98304 and row['output_bytes_read_before_written'] == 0
            assert row['actual_return_registers_match'] and row['actual_return_CPSR_match']
            row['all_executed_ARM_ITCM_overlay_and_copied_pool_words_exact_registered_ROM'] = True
            row['registered_code_sha256'] = sha(b''.join(struct.pack('<II', pc, size)
                + bytes(expected.mem_read(pc, size)) for pc, size in sorted(code_words)))
            row['clock_helper_and_complete_iterator_original_clean_identical'] = True
            results.append(row)
    finally:
        replay.setup = original_setup
    save(ROOT / (case + '_native_proof.json'), {'cases': results,
        'replay_script_sha256': sha(Path(replay.__file__).read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'V693 {case}:all{len(results)} complete predecessor paints and registered code words exact.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('case', choices=('source_full', 'current_full'))
    main(parser.parse_args().case)
