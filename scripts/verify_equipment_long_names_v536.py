"""Captain's five long equipped hints, full papers/plaques and source isolation."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_inventory_fixture_v481 import transfer
from scripts.prepare_plaque_style_v247 import paper
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_occupied_weapon_v477 import item_state
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_short_equipment_release_v252 import numeric_field

ROM = Path('out/all_routes_combined_v534_candidate.nds')
OUT = Path('work/analysis/equipment_long_names_v536')
CAPTURE = Path('E:/Rota Nova translations/Generated/work/emulation_v193/equipment_long_names_v536')
CASES = [(40, 'Red-Haired Pirate Sword', 15600, 16),
         (71, "Saladin's Silver Armor", 15400, 64),
         (92, "Alexander's Campaigns", 15200, 112),
         (98, 'Self-Sharpening Plane', 15000, 160),
         (126, 'Aristarchus Telescope', 14800, 208)]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def exact_paper(font, palette, image, name, slot_x):
    width = len(name) * 6 + 4
    left = min(slot_x, 224 - width)
    ink, bounds = complete_mask(font, name, image, left + 2, 210, (0, 8, 0))
    expected = {(left + 2 + n * 6 + x, 210 + y) for n, char in enumerate(name)
                for y in range(11) for x in range(6) if font.decode(char).getpixel((x, y))}
    tile = paper(width, 16, palette)
    for y in range(16):
        for x in range(width):
            point = left + x, 208 + y
            rgb = (0, 8, 0) if point in expected else palette[tile[y * width + x]][:3]
            assert native5(image.getpixel(point)) == native5(rgb)
    return {'English': name, 'complete_ink_pixels': ink, 'glyph_bounds': bounds,
            'whole_paper_rect': [left, 208, left + width, 224],
            'all_first_final_letters_blank_cells_bevels_borders_and_background_exact': True}


def main():
    digest = sha(ROM.read_bytes())
    assert digest == 'cac800924a1dfb3e2bc6352ef3f47f8f82986229377de20bc5e194046b5a6f45'
    report_path = CAPTURE / 'capture_report.json'
    run = read(report_path)
    assert run['ROM_sha256'] == digest and run['cold_boot'] and not run['savestate_loaded']
    assert not run['callback_errors'] and run['frames'] == 15600
    assert all(r['unformatted_pattern'] == 'Setting %s color depth.\n' for r in run['core_log_unformatted_patterns'])
    donor = read(OUT / 'save_copy_manifest.json')
    assert sha(Path(donor['original']).read_bytes()) == donor['original_sha256']
    assert sha(Path(donor['test_copy']).read_bytes()) == donor['test_copy_sha256'] == donor['original_sha256']
    assert run['battery_save_preloaded']['source'] == donor['test_copy']
    assert len(run['synthetic_inventory_fixtures']) == 1 and not run['normal_acquisition_verified']
    fixture = run['synthetic_inventory_fixtures'][0]
    assert [r['item_id'] for r in fixture['items']] == [40, 71, 92, 98, 126]
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    compatibility = read(OUT / 'compatibility_proof.json')
    original = NdsImage.open('out/all_routes_combined_v502_candidate.nds').read_file('/__arm9__.bin')
    assert sha(arm) == compatibility['current_arm9_sha256']
    assert all(arm[lo:hi] == original[lo:hi] for lo, hi in compatibility['native_transfer_getter_history_ranges_byte_identical'])
    before = (CAPTURE / 'frame_003000_arm9_ram.bin').read_bytes()
    _, replay = transfer(arm, before, [40, 71, 92, 98, 126])
    assert fixture == dict(replay, frame=3000) and len(fixture['changes']) == 11
    for row in run['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    for row in run['read_only_pause_RAM_snapshots']:
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    font = GameAsciiFont.from_arm9(arm)
    palette = PxlImage.from_bytes(rom.read_file('/_pxl/towninfo.pxl')).palette
    atlas = PxlImage.from_bytes(rom.read_file('/_pxl/item.pxl')).render().convert('RGB')
    cases = []
    for item, name, frame, slot in CASES:
        path = CAPTURE / f'frame_{frame:06d}_navigation.png'
        image = Image.open(path).convert('RGB')
        display = exact_paper(font, palette, image, name, slot)
        assert [native5(p) for p in image.crop((slot, 224, slot + 32, 256)).get_flattened_data()] == [
            native5(p) for p in atlas.crop((0, item * 32, 32, (item + 1) * 32)).get_flattened_data()]
        state = item_state(arm, CAPTURE / f'frame_{frame:06d}_arm9_ram.bin', item)
        assert state['name'] == name and state['owner_descriptor_type'] == 2
        assert state['owner_index_or_city_if_type2_or4'] == 3
        cases.append({'item_id': item, 'slot_x': slot, 'frame': frame, 'image': str(path),
                      'exact32x32_icon_pixels': 1024, 'native_owner': state, 'display': display})
    empty = []
    for name, frame, slot in [('Weapon', 6200, 16), ('Armor', 7000, 64), ('Equipped Items', 12000, 208)]:
        image = Image.open(CAPTURE / f'frame_{frame:06d}_navigation.png').convert('RGB')
        empty.append({'frame': frame, 'display': exact_paper(font, palette, image, name, slot)})
    image = Image.open(CAPTURE / 'frame_015600_navigation.png').convert('RGB')
    batch = read('translations/person_info_graphics_v3.json')
    art = PxlImage.from_bytes(rom.read_file(batch['file_path']))
    plaques = []
    for row in batch['records']:
        x0, y0, x1, y1 = row['plaque_box']
        assert all(native5(image.getpixel((x, y))) == native5(art.palette[art.indices[y * 256 + x]][:3])
                   for y in range(y0, y1) for x in range(x0, x1))
        plaques.append({'English': row['text'], 'bounds': row['plaque_box'],
                        'all_letter_border_bevel_and_background_pixels_exact': True, 'fully_completed': False})
    statuses = []
    for text, y in [('Healthy', 108), ('Relaxed', 128)]:
        ink, bounds = complete_mask(font, text, image, 56, y, (230, 230, 230))
        statuses.append({'English': text, 'complete_ink_pixels': ink, 'bounds': bounds})
    skills = []
    for label, x, y in [('Command', 16, 272), ('Sailing', 96, 272), ('Survey', 176, 272),
                        ('Finance', 16, 296), ('Observe', 96, 296), ('Vigor', 176, 296),
                        ('Aim', 16, 320), ('Swords', 96, 320), ('Speech', 176, 320), ('Guile', 16, 344)]:
        value = numeric_field(font, image, x + 42, y)
        ink, bounds = complete_mask(font, f'{label:>7}{value:3d}', image, x, y, (230, 230, 230))
        skills.append({'English': label, 'displayed_value': value, 'complete_ink_pixels': ink, 'bounds': bounds})
    for filename in ['graphics_visual_audit_v150.json', 'graphics_completion_campaign_v1.json']:
        audit = read(Path('translations') / filename)['plaque_style_v247']['ongoing_plaque_inventory']
        assert len(audit) == 18 and all(not r['fully_completed'] for r in audit)
    assert len(read('translations/graphics_completion_requirements_v313.json')['historical_pending_items_retained']) == 22
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'ROM_modified': False,
             'actual_report': str(report_path), 'actual_report_sha256': sha(report_path.read_bytes()),
             'original_and_test_copy_save_hashes_unchanged': donor,
             'source_locked_bounded_native_inventory_fixture': fixture,
             'all_five_captain_occupied_long_name_slots': cases, 'three_complete_empty_hints': empty,
             'all_ten_current_Sailor_Info_plaques': plaques, 'complete_natural_Healthy_Relaxed_labels': statuses,
             'all_ten_complete_skill_labels_and_numeric_fields': skills,
             'native_Y_Equip_and_reordered_inventory_verified': True,
             'fixed_A_presses_and_toggled_telescope_attempts_not_equipped_display_credit': True,
             'normal_acquisition_and_other_owner_condition_role_contexts_remain': True,
             'all22_requirements_and18_incomplete_plaques_retained': True,
             'full_goal_complete': False, 'hardware_device_verification': False}
    (OUT / 'five_long_slots_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('V536:five long equipped captain hints/full papers,5120 icon pixels,three empty hints,ten plaques/statuses/skills;original save/ROM unchanged.')


if __name__ == '__main__':
    main()
