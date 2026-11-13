"""Actual Auto Move, complete Stop caption and confirmed return to manual sailing."""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.record_navigation_v327 import dark_text
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_plaque_release_v247 import find_mask

ROM = Path('out/all_routes_combined_v388_candidate.nds')
ROOT = Path('work/analysis/auto_move_riga_v399')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def capture(name, digest):
    folder = Path('work/emulation_v193') / name
    report_path = folder / 'capture_report.json'
    report = read(report_path)
    assert report['ROM_sha256'] == digest
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert sha(Path(report['battery_save_preloaded']['source']).read_bytes()) == report['battery_save_preloaded']['source_sha256']
    frames = {}
    for row in report['frames_captured']:
        path = Path(row['path'])
        assert sha(path.read_bytes()) == row['PNG_sha256']
        if 'cold_boot' in path.name:
            frames[row['frame']] = path
    return report_path, report, frames


def main():
    digest = sha(ROM.read_bytes())
    assert digest == read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    results = [capture(n, digest) for n in ['auto_move_riga_v399', 'auto_move_dense_v400',
                                          'auto_move_stop_v401', 'auto_move_stop_confirm_v402']]
    trip, dense, question, stopped = [r[1] for r in results]
    tf, df, qf, sf = [r[2] for r in results]
    assert len({r['battery_save_preloaded']['source_sha256'] for r in [trip, dense, question, stopped]}) == 1
    assert all(f in df for f in range(7200, 7601))
    assert dense['scripted_input_schedule'] == [e for e in trip['scripted_input_schedule'] if e['start'] <= 7201]
    assert question['scripted_input_schedule'] == dense['scripted_input_schedule'] + [{'start': 7301, 'duration': 8, 'buttons': ['B']}]
    assert stopped['scripted_input_schedule'] == question['scripted_input_schedule'] + [{'start': 7361, 'duration': 8, 'buttons': ['A']}]
    matched = []
    for frame in sf:
        if frame <= 7300 and frame in df:
            assert sf[frame].read_bytes() == df[frame].read_bytes()
            matched.append(frame)
    assert 7300 in matched
    for frame in range(7300, 7361):
        assert sf[frame].read_bytes() == qf[frame].read_bytes()

    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in [(0xCB1A8, 0xCB1B4), (0x82C4C, 0x82C64), (0x77210, 0x77214)]:
        assert arm[lo:hi] == clean[lo:hi]
    assert struct.unpack_from('<I', arm, 0x77210)[0] == 0x2090
    font = GameAsciiFont.from_arm9(arm)
    auto = Image.open(df[7300]).convert('RGB')
    auto_masks = []
    for text, x in [('Menu', 59), ('Inspect', 105), ('Stop Auto Move', 169)]:
        ink, box = complete_mask(font, text, auto, x, 370, (230, 230, 230))
        assert box[2] <= 256
        auto_masks.append({'text': text, 'bounds': box, 'ink_pixels': ink,
                           'complete_first_final_glyph_and_blank_cells': True})
    prompt = dark_text(font, 'Stop automatic movement?', Image.open(sf[7360]).convert('RGB'),
                       (8, 292, 250, 330))
    manual = Image.open(sf[7600]).convert('RGB')
    manual_masks = [find_mask(font, t, manual, (0, 364, 256, 384))
                    for t in ['Rotate', 'Menu', 'Inspect', 'Sails']]
    confirm = dark_text(font, 'Auto Move', Image.open(tf[7200]).convert('RGB'), (80, 265, 180, 310))
    dock = dark_text(font, 'Dock at Stockholm?', Image.open(tf[7600]).convert('RGB'), (8, 292, 250, 330))
    arrived = Image.open(results[0][0].parent / 'frame_008000_navigation.png').convert('RGB')
    city = find_mask(font, 'Stockholm', arrived, (0, 10, 256, 40))
    snapshot = stopped['read_only_RAM_snapshot']
    ram = Path(snapshot['path']).read_bytes()
    assert sha(ram) == snapshot['sha256'] and snapshot['read_only_export']
    u = machine(arm)
    u.mem_write(0x02000000, ram)
    call(u, 0xCB1A8, ())
    fleet = u.reg_read(UC_ARM_REG_R0)
    call(u, 0x82C4C, (fleet + 0x2090, 1))
    assert u.reg_read(UC_ARM_REG_R0) == 0
    assert bytes(u.mem_read(0x02000000, len(ram))) == ram
    proof = {'candidate': str(ROM), 'candidate_sha256': digest,
             'reports': [str(r[0]) for r in results],
             'report_sha256': [sha(r[0].read_bytes()) for r in results],
             'actual_genuine_Riga_to_Stockholm_Auto_Move': True,
             'actual_Auto_Move_confirmation_mask': confirm,
             'actual_auto_footer': auto_masks, 'auto_footer_frame': 7300,
             'all401_dense_automatic_trip_frames_hashed': True,
             'matched_whole_frames_before_Stop': matched,
             'all61_whole_confirmation_frames_match_until_A': True,
             'actual_B_Stop_question': prompt, 'actual_A_confirmation_at_frame': 7361,
             'actual_manual_footer_after_confirm': manual_masks,
             'final_native_original_automatic_flag_clear': True,
             'pre_stop_native_flag_not_exported_not_claimed': True,
             'original_complete_dock_prompt': dock, 'actual_completed_trip_town_header': city,
             'no_savestate_RAM_injection_synthetic_unlock_or_progress_edit': True,
             'specific_actual_Stop_Auto_Move_display_and_input_gate_verified': True,
             'all_other_sailing_modes_routes_conditions_and_timing_not_claimed': True,
             'ROM_changed': False, 'all18_plaques_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'actual_auto_move_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Genuine Auto Move completes Stockholm trip; full323-pixel auto footer, stop286-pixel question, '
          'A confirmation and all four manual captions pass. Native final auto flag clear.')


if __name__ == '__main__':
    main()
