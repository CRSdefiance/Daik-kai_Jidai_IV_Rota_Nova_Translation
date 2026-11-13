"""Current actual five maximum hints, whole papers, icons and static plaques."""

from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts.native_inventory_fixture_v481 import transfer
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.run_long_hints_v730 import CAP, FRAMES, ITEMS, ROM, ROOT, support
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_equipment_join_v581 import source_tile
from scripts.verify_equipment_long_names_v536 import CASES
from scripts.verify_occupied_weapon_v477 import item_state
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_short_equipment_release_v252 import numeric_field
from scripts.verify_source_plaque_bevels_v546 import hint
from scripts.verify_source_plaque_grain_v542 import masks
from scripts.verify_village_wrap_v608 import read, save

SKILLS = [('Command', 16, 272), ('Sailing', 96, 272), ('Survey', 176, 272),
          ('Finance', 16, 296), ('Observe', 96, 296), ('Vigor', 176, 296),
          ('Aim', 16, 320), ('Swords', 96, 320), ('Speech', 176, 320), ('Guile', 16, 344)]


def main():
    pre = read(ROOT / 'preflight.json')
    assert pre['runner_sha256'] == sha(Path('scripts/run_long_hints_v730.py').read_bytes())
    assert pre['shared_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
    assert pre['compatibility'] == support()
    for key in ('original_donor', 'test_copy'):
        assert sha(Path(pre[key]).read_bytes()) == pre[key + '_sha256']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    report_path = CAP / 'capture_report.json'
    report = read(report_path)
    assert report['ROM_sha256'] == pre['candidate_sha256']
    assert report['frames'] == 15600 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and report['core_DLL_sha256'] == pre['core_sha256']
    assert report['scripted_input_schedule'] == read(pre['inputs'])
    assert report['battery_save_preloaded']['source'] == pre['test_copy']
    assert report['battery_save_preloaded']['source_sha256'] == pre['test_copy_sha256']
    assert not report['normal_acquisition_verified']
    shots, images = {}, {}
    for row in report['frames_captured']:
        path = Path(row['path'])
        assert sha(path.read_bytes()) == row['PNG_sha256']
        if row['frame'] in FRAMES:
            shots.setdefault(row['frame'], row)
            images.setdefault(row['frame'], Image.open(path).convert('RGB'))
    assert set(shots) == set(FRAMES)
    ram_rows = {r['frame']: r for r in report['read_only_capture_RAM_snapshots']}
    assert set(ram_rows) == set(FRAMES)
    for row in ram_rows.values():
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    before = Path(ram_rows[3000]['path']).read_bytes()
    _, replay = transfer(arm, before, ITEMS)
    assert report['synthetic_inventory_fixtures'] == [dict(replay, frame=3000)]
    assert len(replay['changes']) == 11
    font = GameAsciiFont.from_arm9(arm)
    plan = read('work/analysis/direct_equipment_v270/runtime_plan.json')
    pool = bytes(MainCodeFile(arm, 0x02000000).sections[3].data)
    at = plan['tile_pointer'] - POOL
    tile = pool[at:at + 1408]
    clean = NdsImage.open('work/clean.nds')
    donor = PxlImage.from_bytes(clean.read_file('/_pxl/towninfo.pxl'))
    assert tile == source_tile(donor, True)
    prior = read('work/analysis/equipment_material_v580/v581_release_proof.json')
    assert len(prior['five_longest_native_cases']) == 5
    # A current catalogue prevents historical maximum-width claims silently
    # surviving a later name edit. These are getters, not103 GPU displays.
    u = machine(arm)
    u.mem_write(BASE, before)
    call(u, 0xCB190, ())
    store = u.reg_read(UC_ARM_REG_R0)
    catalogue = {2: [], 3: [], 4: []}
    for index in range(218):
        record = store + 4 + index * 20
        call(u, 0x4A448, (record,))
        category = u.reg_read(UC_ARM_REG_R0)
        if category not in catalogue:
            continue
        call(u, 0x4A53C, (record,))
        name = bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 128)).split(b'\0')[0].decode('cp932')
        assert name.isascii()
        catalogue[category].append({'id': index, 'name': name, 'width': len(name) * 6 + 4})
    assert [len(catalogue[c]) for c in (2, 3, 4)] == [28, 26, 49]
    assert {str(k): v for k, v in catalogue.items()} == prior['all103_equipment_names_native_catalog']
    assert bytes(u.mem_read(BASE, len(before))) == before
    for index, name, _, _ in CASES:
        category = next(c for c in catalogue if any(r['id'] == index for r in catalogue[c]))
        assert len(name) * 6 + 4 == max(r['width'] for r in catalogue[category])
    atlas = PxlImage.from_bytes(rom.read_file('/_pxl/item.pxl')).render().convert('RGB')
    occupied, empty, plaques, skill_rows, status_rows = [], [], [], [], []
    definitions = []
    for group in read('translations/source_plaque_grain_v1.json')['files']:
        if group['file_path'] != '/_pxl/personinfo.pxl':
            continue
        asset = PxlImage.from_bytes(rom.read_file(group['file_path']))
        masks(asset, group['records'], font)
        definitions += [(asset, row) for row in group['records']]
    assert len(definitions) == 10
    for item, name, frame, slot in CASES:
        image = images[frame]
        paper = hint(font, tile, image, name, slot)
        width, left = len(name) * 6 + 4, min(slot, 224 - (len(name) * 6 + 4))
        assert 0 <= left < left + width <= 224
        state = item_state(arm, Path(ram_rows[frame]['path']), item)
        assert state['name'] == name and state['owner_descriptor_type'] == 2
        assert state['owner_index_or_city_if_type2_or4'] == 3
        assert [native5(p) for p in image.crop((slot, 224, slot + 32, 256)).get_flattened_data()] == [
            native5(p) for p in atlas.crop((0, item * 32, 32, (item + 1) * 32)).get_flattened_data()]
        occupied.append({'item': item, 'frame': frame, 'source_case_V581': next(
            r['frame'] for r in prior['five_longest_native_cases'] if r['item'] == item),
            'native_owner': state, 'hint': paper, 'whole_paper_bounds': [left, 208, left + width, 224],
            'complete_original_icon_pixels': 1024, 'screenshot': shots[frame]})
        for asset, row in definitions:
            l, t, r, b = row['plaque_box']
            assert all(native5(image.getpixel((x, y))) == native5(asset.palette[asset.indices[y * asset.width + x]])
                for y in range(t, b) for x in range(l, r)), (name, row['id'])
            plaques.append({'frame': frame, 'id': row['id'], 'text': row['english'],
                'whole_letter_bevel_border_and_material_pixels': (r - l) * (b - t)})
        for label, x, y in SKILLS:
            value = numeric_field(font, image, x + 42, y)
            ink, bounds = complete_mask(font, f'{label:>7}{value:3d}', image, x, y, (230, 230, 230))
            skill_rows.append({'frame': frame, 'label': label, 'observed_value': value,
                'complete_font_pixels': ink, 'bounds': bounds, 'mechanics_not_inferred': True})
        for text, y in (('Healthy', 108), ('Relaxed', 128)):
            ink, bounds = complete_mask(font, text, image, 56, y, (230, 230, 230))
            status_rows.append({'frame': frame, 'text': text, 'ink': ink, 'bounds': bounds})
    for name, frame, slot in (('Weapon', 6200, 16), ('Armor', 7000, 64), ('Equipped Items', 12000, 208)):
        empty.append({'frame': frame, **hint(font, tile, images[frame], name, slot)})
    assert len(occupied) == 5 and len(empty) == 3 and len(plaques) == len(skill_rows) == 50
    # The sheet contains complete actual screen data and clearly marked enlarged
    # original PNG crops, not a reconstructed screenshot.
    sheet = Image.new('RGB', (1412, 816), '#263238')
    draw = ImageDraw.Draw(sheet)
    draw.text((12, 10), 'V712 current combined ROM / declared inventory fixture', fill='white')
    sheet.paste(images[15600].resize((512, 768), Image.Resampling.NEAREST), (12, 36))
    for n, (item, name, frame, slot) in enumerate(CASES):
        y = 42 + n * 150
        draw.text((548, y), f'{name} / actual frame {frame}', fill='white')
        sheet.paste(images[frame].crop((8, 200, 224, 232)).resize((864, 128), Image.Resampling.NEAREST), (536, y + 20))
    sheet_path = ROOT / 'current_five_long_hints_review.png'
    sheet.save(sheet_path)
    proof = {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
        'preflight': str(ROOT / 'preflight.json'),
        'preflight_sha256': sha((ROOT / 'preflight.json').read_bytes()),
        'runner_sha256': pre['runner_sha256'], 'verifier_sha256': sha(Path(__file__).read_bytes()),
        'one_terminal15600_frame_current_cold_boot': True,
        'native_transfer11_byte_fixture_replayed_exact': replay,
        'all103_current_native_equipment_names_and_widths': catalogue,
        'five_tested_hints_still_category_maxima': True,
        'five_category_maximum_hints_and5120_icon_pixels': occupied,
        'three_complete_current_empty_hints': empty,
        'all50_current_full_static_Info_plaques': plaques,
        'all50_full_skill_labels_and_observed_numeric_fields': skill_rows,
        'all10_natural_condition_label_masks': status_rows,
        'current1408_byte_paper_exact_original_donor_join': sha(tile),
        'prior_V581_proof': 'work/analysis/equipment_material_v580/v581_release_proof.json',
        'prior_V581_proof_sha256': sha(Path('work/analysis/equipment_material_v580/v581_release_proof.json').read_bytes()),
        'review_sheet': str(sheet_path), 'review_sheet_sha256': sha(sheet_path.read_bytes()),
        'normal_acquisition_or_every_actor_state_verified': False,
        'original18_overall_objects_remain_open': True,
        'ROM_modified': False, 'release_hashes_unchanged': pre['release_hashes'], 'full_goal_complete': False}
    save(ROOT / 'proof.json', proof)
    print('V730 current5 maximum/3 empty hints,5120 icon pixels,50 whole plaques,50 observed skill rows and10 status labels pass.')


if __name__ == '__main__':
    main()
