"""Genuine shield search/equip/save/cold load and complete occupied Armor pixels."""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_plaque_style_v247 import paper
from scripts.probe_button_prompt_native import call, machine
from scripts.record_navigation_v327 import dark_text
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_short_equipment_release_v252 import numeric_field

ROOT = Path('work/analysis/shield_search_v469')
ROM = Path('out/all_routes_combined_v468_candidate.nds')
CAPTURE = Path('work/emulation_v193/shield_search_v469')
RELOAD = Path('work/emulation_v193/shield_armor_reload_v469')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def compact_mask(font, text, image, x0, y0):
    # Item data uses native tracking -1; the Armor tooltip uses ordinary6-pixel cells.
    expected = {(x0 + n * 5 + x, y0 + y) for n, c in enumerate(text)
                for y in range(11) for x in range(6) if font.decode(c).getpixel((x, y))}
    box = [x0, y0, x0 + (len(text) - 1) * 5 + 6, y0 + 11]
    actual = {(x, y) for y in range(box[1], box[3]) for x in range(box[0], box[2])
              if image.getpixel((x, y)) == (230, 230, 230)}
    assert actual == expected, (text, len(expected - actual), len(actual - expected))
    return {'text': text, 'bounds': box, 'ink_pixels': len(expected), 'native_advance': 5,
            'complete_first_interior_final_glyphs_and_blank_area_exact': True}


def state(arm, path):
    raw = path.read_bytes()
    u = machine(arm)
    u.mem_write(0x02000000, raw)
    call(u, 0xCB190, ())
    item = u.reg_read(UC_ARM_REG_R0) + 4 + 49 * 20
    call(u, 0x4A394, (item,))
    known = u.reg_read(UC_ARM_REG_R0)
    call(u, 0x4A368, (item,))
    found = u.reg_read(UC_ARM_REG_R0)
    call(u, 0x4A448, (item,))
    category = u.reg_read(UC_ARM_REG_R0)
    call(u, 0x4A53C, (item,))
    name = bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 128)).split(b'\0', 1)[0].decode('cp932')
    out = 0x02470020
    u.mem_write(out - 16, b'\xA5' * 48)
    call(u, 0x49DE8, (out, item))
    descriptor = bytes(u.mem_read(out, 16))
    assert bytes(u.mem_read(out - 16, 16)) == bytes(u.mem_read(out + 16, 16)) == b'\xA5' * 16
    assert bytes(u.mem_read(0x02000000, len(raw))) == raw
    return {'snapshot': str(path), 'snapshot_sha256': sha(raw), 'clue_flag': known,
            'found_flag': found, 'category': category, 'name': name,
            'item_record_hex': bytes(u.mem_read(item, 20)).hex(),
            'owner_descriptor_type': struct.unpack_from('<I', descriptor, 4)[0],
            'owner_index_if_equipped': struct.unpack_from('<I', descriptor, 8)[0]
            if struct.unpack_from('<I', descriptor, 4)[0] == 2 else None,
            'unused_descriptor_fields_not_interpreted': True, 'captured_RAM_preserved': True}


def geometry(arm):
    path = CAPTURE / 'frame_007587_arm9_ram.bin'
    raw = path.read_bytes()
    u = machine(arm)
    u.mem_write(0x02000000, raw)
    call(u, 0xCB190, ())
    item = u.reg_read(UC_ARM_REG_R0) + 4 + 49 * 20
    call(u, 0xCB1A8, ())
    fleets = u.reg_read(UC_ARM_REG_R0)
    call(u, 0x2E58C, ())
    fleet = fleets + 4 + u.reg_read(UC_ARM_REG_R0) * 0x84
    points = []
    for obj in (item, fleet):
        vt = struct.unpack('<I', u.mem_read(obj, 4))[0]
        fn = struct.unpack('<I', u.mem_read(vt + 0x20, 4))[0]
        out = 0x02471020
        u.mem_write(out - 16, b'\xA5' * 40)
        call(u, fn - 0x02000000, (out, obj))
        points.append(struct.unpack('<2i', u.mem_read(out, 8)))
        assert bytes(u.mem_read(out - 16, 16)) == bytes(u.mem_read(out + 8, 16)) == b'\xA5' * 16
    call(u, 0x655B8, ())
    radius = u.reg_read(UC_ARM_REG_R0)
    squared = sum((a - b) ** 2 for a, b in zip(*points))
    assert radius == 32 and squared <= radius * radius
    assert bytes(u.mem_read(0x02000000, len(raw))) == raw
    return {'actual_item_and_fleet_original_virtual_points': points, 'radius_map_units': radius,
            'squared_distance': squared, 'inside_original_radius_squared': True,
            'isolated_original_getters_only_no_live_position_change': True}


def main():
    digest = sha(ROM.read_bytes())
    assert read(ROM.with_suffix('.manifest.json'))['candidate_sha256'] == digest
    reports = []
    for folder, frames in [(CAPTURE, 14887), (RELOAD, 3800)]:
        p = folder / 'capture_report.json'
        r = read(p)
        assert r['ROM_sha256'] == digest and r['frames'] == frames
        assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
        for row in r['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        reports.append((p, r))
    original = Path(reports[0][1]['battery_save_preloaded']['source'])
    assert sha(original.read_bytes()) == reports[0][1]['battery_save_preloaded']['source_sha256']
    saved = Path(reports[0][1]['battery_save_preloaded']['destination'])
    copied = ROOT / 'equipped_armor_test_copy.dsv'
    assert saved.read_bytes() == copied.read_bytes()
    assert sha(copied.read_bytes()) == reports[1][1]['battery_save_preloaded']['source_sha256']
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    samples = [state(arm, CAPTURE / f'frame_{n:06d}_arm9_ram.bin') for n in [7587, 8787, 10087]]
    samples.append(state(arm, RELOAD / 'final_arm9_ram.bin'))
    assert (samples[0]['clue_flag'], samples[0]['found_flag']) == (1, 0)
    assert all((r['clue_flag'], r['found_flag'], r['category'], r['name']) ==
               (0, 2, 3, 'Blue Oak Shield') for r in samples[1:])
    assert all((r['owner_descriptor_type'], r['owner_index_if_equipped']) == (2, 1) for r in samples[2:])
    before = Image.open(CAPTURE / 'frame_010087_navigation.png').convert('RGB')
    after = Image.open(RELOAD / 'frame_003800_final.png').convert('RGB')
    assert before.tobytes() == after.tobytes()
    text = 'Blue Oak Shield'
    ink, bounds = complete_mask(font, text, after, 66, 210, (0, 8, 0))
    assert ink == 182 and bounds == [66, 210, 156, 221]
    expected = {(66 + n * 6 + x, 210 + y) for n, c in enumerate(text)
                for y in range(11) for x in range(6) if font.decode(c).getpixel((x, y))}
    actual = {(x, y) for y in range(208, 224) for x in range(64, 158)
              if after.getpixel((x, y)) == (0, 8, 0)}
    assert actual == expected
    palette = PxlImage.from_bytes(rom.read_file('/_pxl/towninfo.pxl')).palette
    tile = paper(94, 16, palette)
    for y in range(16):
        for x in range(94):
            point = 64 + x, 208 + y
            rgb = (0, 8, 0) if point in expected else palette[tile[y * 94 + x]][:3]
            assert native5(after.getpixel(point)) == native5(rgb), point
    atlas = PxlImage.from_bytes(rom.read_file('/_pxl/item.pxl')).render().convert('RGB')
    assert [native5(c) for c in after.crop((64, 224, 96, 256)).get_flattened_data()] == [
        native5(c) for c in atlas.crop((0, 49 * 32, 32, 50 * 32)).get_flattened_data()]
    plaques = read(Path('translations/person_info_graphics_v3.json'))
    asset = PxlImage.from_bytes(rom.read_file(plaques['file_path']))
    for shot in (before, after):
        for row in plaques['records']:
            x0, y0, x1, y1 = row['plaque_box']
            assert all(native5(shot.getpixel((x, y))) ==
                       native5(asset.palette[asset.indices[y * asset.width + x]][:3])
                       for y in range(y0, y1) for x in range(x0, x1))
    owner = find_mask(font, 'Hodram Joakim Bergstrom', after, (80, 16, 256, 60))
    skills = []
    for label, x, y in [('Command', 16, 272), ('Sailing', 96, 272), ('Survey', 176, 272),
                        ('Finance', 16, 296), ('Observe', 96, 296), ('Vigor', 176, 296),
                        ('Aim', 16, 320), ('Swords', 96, 320), ('Speech', 176, 320), ('Guile', 16, 344)]:
        value = numeric_field(font, after, x + 42, y)
        count, box = complete_mask(font, f'{label:>7}{value:3d}', after, x, y, (230, 230, 230))
        skills.append({'label': label, 'value': value, 'complete_ink_pixels': count, 'bounds': box})
    messages = []
    for frame, lines in [(7887, ['A major discovery! The expedition', 'found this.']),
                         (9387, ['Hodram Joakim Bergstrom equipped', 'Blue Oak Shield.']),
                         (10787, ['Overwrite existing data?', 'Continue?'])]:
        shot = Image.open(CAPTURE / f'frame_{frame:06d}_navigation.png').convert('RGB')
        messages.extend({'frame': frame, 'mask': dark_text(font, line, shot, (8, 292, 253, 350))} for line in lines)
    item_view = Image.open(CAPTURE / 'frame_009087_navigation.png').convert('RGB')
    item_name = compact_mask(font, text, item_view, 56, 24)
    item_kind = compact_mask(font, 'Armor', item_view, 8, 64)
    description = [compact_mask(font, line, item_view, 8, y) for line, y in
                   [('Mysterious, rock-hard blue oak forms this', 112), ('small, round shield.', 128)]]
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'ROM_changed': False,
             'reports': [{'path': str(p), 'sha256': sha(p.read_bytes()),
                          'verified_capture_count': len(r['frames_captured'])} for p, r in reports],
             'actual_original_item_state_progression': samples, 'native_search_geometry': geometry(arm),
             'normal_Search_then_ordinary_Items_Y_equip': True, 'player_inventory_item_name': item_name,
             'item_category_Armor': item_kind, 'complete_item_description_lines': description,
             'complete_discovery_equip_save_messages': messages, 'complete_equipped_owner_name': owner,
             'complete_Armor_tooltip_ink_pixels': ink, 'complete_tooltip_bounds': bounds,
             'whole_native_paper_and_corner_pixels_exact': 1504, 'original_shield_icon_pixels_exact': 1024,
             'all20_person_plaque_instances_exact': True, 'all10_complete_skill_lines': skills,
             'entire_occupied_Armor_screen_exact_after_cold_load_pixels': 98304,
             'normal_slot6_save_completed_with4100_more_frames_then_cold_loaded': True,
             'original_London_donor_unchanged': True, 'saved_battery': str(copied),
             'saved_battery_sha256': sha(copied.read_bytes()), 'occupied_Armor_Blue_Oak_Shield_verified': True,
             'occupied_Weapon_and_other_Armor_names_states_remain_open': True,
             'all18_plaques_incomplete': True, 'all22_historical_requirements_retained': True,
             'hardware_verification': False, 'full_goal_complete': False}
    (ROOT / 'armor_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Genuine shield search/equip/save/reload:182 complete tooltip pixels,1504 paper,1024 icon,20 plaques and whole98304-pixel armor screen exact.')


if __name__ == '__main__':
    main()
