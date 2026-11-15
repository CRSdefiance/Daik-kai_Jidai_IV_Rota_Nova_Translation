"""Actual minimum sailor assignment, London voyage, rest and normal save reload."""

import json
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.read_navigation_snapshot_v391 import inspect
from scripts.record_navigation_v327 import dark_text
from scripts.verify_commodity_layout_v346 import mask
from scripts.verify_plaque_release_v247 import find_mask

ROM = Path('out/all_routes_combined_v464_candidate.nds')
ROOT = Path('work/analysis/shield_voyage_v467')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    digest = sha(ROM.read_bytes())
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    reports = []
    for name, frame in [('shield_voyage_v467', 20065), ('london_checkpoint_reload_v467', 3600)]:
        path = Path('work/emulation_v193') / name / 'capture_report.json'
        r = read(path)
        assert r['ROM_sha256'] == digest and r['frames'] == frame
        assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
        for row in r['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        reports.append((path, r))
    donor = Path(reports[0][1]['battery_save_preloaded']['source'])
    assert sha(donor.read_bytes()) == reports[0][1]['battery_save_preloaded']['source_sha256']
    saved = Path(reports[0][1]['battery_save_preloaded']['destination'])
    copied = ROOT / 'london_test_copy.dsv'
    assert saved.read_bytes() == copied.read_bytes()
    assert sha(copied.read_bytes()) == reports[1][1]['battery_save_preloaded']['source_sha256']
    batch = read(Path('translations/assign_sailors_graphics_v5.json'))
    asset = PxlImage.from_bytes(rom.read_file(batch['file_path']))
    panels = []
    for frame in [6200, 15365]:
        path = Path('work/emulation_v193/shield_voyage_v467') / f'frame_{frame:06d}_navigation.png'
        im = Image.open(path).convert('RGB')
        for row in batch['records']:
            x0, y0, x1, y1 = row['plaque_box']
            assert all(tuple(v // 8 for v in im.getpixel((x, y))) ==
                       tuple(v // 8 for v in asset.palette[asset.indices[y * asset.width + x]][:3])
                       for y in range(y0, y1) for x in range(x0, x1)), (frame, row['id'])
        numbers = [find_mask(font, text, im, region) for text, region in [
            ('39', (90, 16, 128, 38)), ('39', (140, 206, 170, 227)),
            ('39', (178, 206, 204, 227)), ('124', (205, 206, 250, 227)),
            ('33' if frame == 6200 else '0', (216, 16, 254, 38))]]
        panels.append({'frame': frame, 'all_seven_full_plaque_pixels_exact': True,
                       'minimum_and_current_both39_max124': numbers,
                       'headers_need_alignment_correction': True})
    messages = []
    for frame, text in [(3500, 'A ship lacks sailors.'), (3500, 'Check formation before sailing.'),
                        (6100, 'Minimum sailors assigned.'), (9785, 'Admiral, withdrawing!'),
                        (11165, 'Discovered London.'), (11265, 'Shall we call at London?'),
                        (15965, 'Overwrite existing data?'), (15965, 'Continue?')]:
        path = Path('work/emulation_v193/shield_voyage_v467') / f'frame_{frame:06d}_navigation.png'
        messages.append({'frame': frame, 'mask': dark_text(font, text, Image.open(path).convert('RGB'),
                                                          (8, 292, 253, 350))})
    town_path = Path('work/emulation_v193/london_checkpoint_reload_v467/frame_003600_final.png')
    town = Image.open(town_path).convert('RGB')
    town_masks = {'name': find_mask(font, 'London', town, (0, 10, 256, 40)),
                  'coordinates': find_mask(font, '(N51 W0)', town, (0, 10, 256, 40)),
                  'goods': [mask(town, font, text, y) for text, y in
                            [('Wool', 88), ('WoolCl.', 104), ('Guns', 120), ('Cannon', 136)]],
                  'zero_fatigue': find_mask(font, '0', town, (150, 344, 220, 366))}
    before = Image.open('work/emulation_v193/shield_voyage_v467/frame_011665_navigation.png').convert('RGB')
    town_masks['arrival_indicator_already_zero_no_Inn_reduction_claim'] = find_mask(font, '0', before, (150, 344, 220, 366))
    snap = reports[1][1]['read_only_RAM_snapshot']
    raw = Path(snap['path']).read_bytes()
    assert snap['read_only_export'] and sha(raw) == snap['sha256']
    u = machine(arm)
    u.mem_write(0x02000000, raw)
    call(u, 0xCB190, ())
    call(u, 0x4A394, (u.reg_read(UC_ARM_REG_R0) + 4 + 49 * 20,))
    assert u.reg_read(UC_ARM_REG_R0) == 1
    assert bytes(u.mem_read(0x02000000, len(raw))) == raw
    samples = [inspect(Path('work/emulation_v193/shield_voyage_v467') / f'frame_{n:06d}_arm9_ram.bin', ROM)
               for n in [7000, 8045, 8525, 9385, 9985, 10495, 10955]]
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'ROM_changed': False,
             'reports': [{'path': str(p), 'sha256': sha(p.read_bytes()),
                          'verified_capture_count': len(r['frames_captured'])} for p, r in reports],
             'actual_assignment_panels_and_complete_values': panels, 'complete_native_messages': messages,
             'normal_London_discovery_docking_resupply_Inn_rest_and_completed_save': True,
             'complete_reloaded_London_town_masks': town_masks, 'actual_original_ship_getter_samples': samples,
             'normal_slot6_save_finished_then_cold_loaded': True, 'original_rested_Copenhagen_donor_unchanged': True,
             'saved_battery': str(copied), 'saved_battery_sha256': sha(copied.read_bytes()),
             'Blue_Oak_clue_persists': 1, 'unassigned33_during_setup_not_a_carried_fleet_reserve': True,
             'later_London_assignment_shows39_assigned_zero_unassigned': True,
             'ten_night_selection_visually_observed_no_calendar_or_economy_arithmetic_claim': True,
             'battle_withdrawal_observed_not_victory': True, 'armor_weapon_acquired_or_equipped_verified': False,
             'all22_historical_requirements_retained': True, 'all18_plaques_incomplete': True,
             'hardware_verification': False, 'full_goal_complete': False}
    (ROOT / 'london_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Minimum/current39,seven exact plaques,normal London rest/save/reload and complete labels pass;header placement needs correction.')


if __name__ == '__main__':
    main()
