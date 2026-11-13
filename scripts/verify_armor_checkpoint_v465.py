"""Verify ordinary Speyer withdrawal, harbor return, save and cold reload."""

import json
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.read_navigation_snapshot_v391 import inspect
from scripts.record_navigation_v327 import dark_text

ROM = Path('out/all_routes_combined_v464_candidate.nds')
ROOT = Path('work/analysis/armor_voyage_v465')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    digest = sha(ROM.read_bytes())
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    reports = []
    for name, count in [('armor_voyage_v465', 35000), ('armor_checkpoint_reload_v465', 3800)]:
        path = Path('work/emulation_v193') / name / 'capture_report.json'
        report = read(path)
        assert report['ROM_sha256'] == digest and report['frames'] == count
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        reports.append((path, report))
    donor = Path(reports[0][1]['battery_save_preloaded']['source'])
    assert sha(donor.read_bytes()) == reports[0][1]['battery_save_preloaded']['source_sha256']
    saved = Path(reports[0][1]['battery_save_preloaded']['destination'])
    copied = ROOT / 'post_encounter_test_copy.dsv'
    assert saved.read_bytes() == copied.read_bytes()
    assert sha(copied.read_bytes()) == reports[1][1]['battery_save_preloaded']['source_sha256']
    masks = []
    for frame, text in [(8680, 'There it is!'), (21320, 'Admiral, withdrawing!'),
                        (23142, 'Shall we call at Copenhagen?'),
                        (28700, 'Your sailors look tired. Rest at the'),
                        (28700, 'inn?'), (31000, 'Overwrite existing data?'),
                        (31000, 'Continue?')]:
        path = Path('work/emulation_v193/armor_voyage_v465') / f'frame_{frame:06d}_navigation.png'
        image = Image.open(path).convert('RGB')
        masks.append({'frame': frame, 'capture': str(path), 'sha256': sha(path.read_bytes()),
                      'mask': dark_text(font, text, image, (8, 292, 253, 345))})
    load_path = Path('work/emulation_v193/armor_checkpoint_reload_v465/frame_002800_cold_boot.png')
    masks.append({'frame': 2800, 'capture': str(load_path), 'sha256': sha(load_path.read_bytes()),
                  'mask': dark_text(font, 'Load this data?', Image.open(load_path).convert('RGB'),
                                    (8, 292, 253, 345))})
    final_path = Path('work/emulation_v193/armor_voyage_v465/frame_035000_final.png')
    final_image = Image.open(final_path).convert('RGB')
    for text in ['Save', 'Load', 'Quit Game', 'Options']:
        masks.append({'frame': 35000, 'capture': str(final_path), 'sha256': sha(final_path.read_bytes()),
                      'mask': dark_text(font, text, final_image, (90, 240, 167, 335))})
    positions = []
    for frame in [5600, 6950, 7070, 7310, 7690, 8300, 19100, 21720, 23142, 35000]:
        path = Path('work/emulation_v193/armor_voyage_v465') / f'frame_{frame:06d}_arm9_ram.bin'
        positions.append(inspect(path, ROM))
    snapshot = reports[1][1]['read_only_RAM_snapshot']
    raw = Path(snapshot['path']).read_bytes()
    assert snapshot['read_only_export'] and sha(raw) == snapshot['sha256']
    u = machine(arm)
    u.mem_write(0x02000000, raw)
    call(u, 0xCB190, ())
    items = u.reg_read(UC_ARM_REG_R0)
    call(u, 0x4A394, (items + 4 + 49 * 20,))
    assert u.reg_read(UC_ARM_REG_R0) == 1
    assert bytes(u.mem_read(0x02000000, len(raw))) == raw
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'ROM_changed': False,
             'reports': [{'path': str(p), 'sha256': sha(p.read_bytes()),
                          'verified_capture_count': len(r['frames_captured'])} for p, r in reports],
             'ordinary_controller_inputs_and_normal_slot6_save_only': True,
             'full_native_dialogue_masks': masks, 'original_getter_positions': positions,
             'original_prepared_donor_unchanged': True, 'saved_battery': str(copied),
             'saved_battery_sha256': sha(copied.read_bytes()),
             'normal_save_confirmed_and_4000_frames_allowed_for_completion': True,
             'normal_save_cold_loaded_after_terminal_stop': True,
             'earned_Blue_Oak_clue_persists_original_getter': 1,
             'visually_observed_saved_Level': 25, 'visually_observed_saved_crew': 19,
             'visually_observed_saved_fatigue': 43,
             'save_is_supplied_at_sea_not_rested_in_port': True,
             'reload_advances_normal_sailing_time_before_menu_not_exact_date_or_stat_comparison': True,
             'battle_withdrawal_observed_not_victory': True,
             'armor_acquisition_or_equipped_display_verified': False,
             'all18_plaques_incomplete': True, 'all22_historical_requirements_retained': True,
             'full_goal_complete': False, 'hardware_verification': False}
    (ROOT / 'checkpoint_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Normal withdrawal/harbor return/save/reload and twelve complete text masks pass; armor remains open.')


if __name__ == '__main__':
    main()
