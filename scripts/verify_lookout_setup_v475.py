"""Persisted real Lookout captions and source city marker/entrance geometry."""

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
from scripts.verify_plaque_release_v247 import find_mask

ROM = Path('out/all_routes_combined_v474_candidate.nds')
ROOT = Path('work/analysis/harbor_geometry_v475')
CAPTURE = Path('work/emulation_v193/lookout_setup_v475')
RELOAD = Path('work/emulation_v193/lookout_reload_v475')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def city_points(arm):
    original = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    ranges = [(0xB5600, 0xB56A8), (0xCD6B8, 0xCD6CC)]
    assert all(arm[a:b] == original[a:b] for a, b in ranges)
    path = Path('work/emulation_v193/east_med_v472/frame_013100_arm9_ram.bin')
    raw = path.read_bytes()
    u = machine(arm)
    u.mem_write(0x02000000, raw)
    call(u, 0xCB178, ())
    store = u.reg_read(UC_ARM_REG_R0)
    rows = []
    for index in range(114):
        actor = store + 4 + index * 108
        call(u, 0xB5600, (actor,))
        assert u.reg_read(UC_ARM_REG_R0) == index
        call(u, 0xCD6B8, (index,))
        metadata = bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 116))
        marker, entrance = struct.unpack_from('<2i', metadata, 4), struct.unpack_from('<2i', metadata, 12)
        for function, expected in [(0xB566C, marker), (0xB5648, entrance)]:
            out = 0x02470020
            u.mem_write(out - 16, b'\xA5' * 40)
            call(u, function, (out, actor))
            assert struct.unpack('<2i', u.mem_read(out, 8)) == expected
            assert bytes(u.mem_read(out - 16, 16)) == bytes(u.mem_read(out + 8, 16)) == b'\xA5' * 16
        rows.append({'city_id': index, 'marker_native_map_units': marker,
                     'entrance_native_map_units': entrance})
    assert bytes(u.mem_read(0x02000000, len(raw))) == raw
    return {'source_exact_getter_ranges': ranges, 'captured_snapshot': str(path),
            'snapshot_sha256': sha(raw), 'snapshot_source_candidate': 'V468',
            'all114_original_actor_indices_and_both_point_getters_pass': rows,
            'captured_RAM_preserved': True, 'live_discovery_or_docking_not_proven': True}


def main():
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    digest = sha(ROM.read_bytes())
    reports = []
    for folder, frame in [(CAPTURE, 9000), (RELOAD, 3800)]:
        path = folder / 'capture_report.json'
        report = read(path)
        assert report['ROM_sha256'] == digest and report['frames'] == frame
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        reports.append((path, report))
    donor = reports[0][1]['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    saved = ROOT / 'genoa_lookout_test_copy.dsv'
    assert saved.read_bytes() == Path(donor['destination']).read_bytes()
    assert sha(saved.read_bytes()) == reports[1][1]['battery_save_preloaded']['source_sha256']
    font = GameAsciiFont.from_arm9(arm)
    selection = Image.open(CAPTURE / 'frame_003900_navigation.png').convert('RGB')
    skill = [find_mask(font, text, selection, region) for text, region in
             [('Lookout', (70, 20, 190, 45)), ('Skill: Observe', (70, 35, 225, 60)),
              ('70', (104, 48, 155, 78)), ('128', (124, 87, 170, 110))]]
    masks = []
    before = Image.open(CAPTURE / 'frame_004000_navigation.png').convert('RGB')
    after = Image.open(RELOAD / 'frame_003800_final.png').convert('RGB')
    assert before.crop((0, 0, 256, 192)).tobytes() == after.crop((0, 0, 256, 192)).tobytes()
    for image in (before, after):
        masks.append({'role': find_mask(font, 'Lookout', image, (70, 20, 190, 45)),
                      'name': find_mask(font, 'Manuel Almeida', image, (70, 37, 240, 65)),
                      'voice': dark_text(font, 'On watch! Eyes open.', image, (8, 110, 253, 180))})
    geometry = city_points(arm)
    fine = ROOT / 'istanbul_fine/water_route_proof.json'
    route = read(fine)
    assert route['candidate_sha256'] == digest and route['grid_step_native_map_units'] == 1
    assert route['waypoint_world_points'] == [[2968576, 699008], [2968576, 699008]]
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'ROM_changed': False,
             'reports': [{'path': str(p), 'sha256': sha(p.read_bytes())} for p, _ in reports],
             'original_repaired_Genoa_donor_unchanged': True,
             'normal_assignment_confirmed_and_save_completed_then_cold_loaded': True,
             'actual_Observe128_exceeds_required70': skill,
             'complete_persisted_role_name_and_spoken_caption': masks,
             'whole_upper192_rows49152_pixels_exact_after_cold_load': True,
             'lower_selection_cursor_differs_not_a_graphics_defect': True,
             'saved_battery': str(saved), 'saved_battery_sha256': sha(saved.read_bytes()),
             'source_city_geometry': geometry, 'fine_grid_route_proof': str(fine),
             'fine_grid_route_proof_sha256': sha(fine.read_bytes()),
             'fine_grid_does_not_reach_requested_inner_harbor_goal': True,
             'Lookout_effect_on_Istanbul_discovery_not_yet_gameplay_verified': True,
             'all22_historical_requirements_retained': True, 'all18_plaques_incomplete': True,
             'occupied_Weapon_remains_open': True, 'hardware_verification': False, 'full_goal_complete': False}
    (ROOT / 'lookout_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Genuine Lookout assignment/save/cold load and complete captions;114 marker/entrance getters pass.')


if __name__ == '__main__':
    main()
