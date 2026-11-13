"""Current V627 actual plaque review packet, preserving the original18 open gates."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw, ImageFont

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_source_plaque_bevels_v546 import hint
from scripts.verify_source_plaque_grain_v542 import masks
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/plaque_review_v632')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/plaque_review_v632_current')
ROM = Path('out/all_routes_combined_v627_candidate.nds')
SOURCE = Path('E:/Rota Nova translations/Generated/work/emulation_v193/plaque_compare_v574_original')
OLD = Path('work/analysis/plaque_current_v574/native_review_proof.json')


def report(folder, digest):
    r = read(folder / 'capture_report.json')
    assert r['frames'] == 7100 and r['ROM_sha256'] == digest
    assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
    assert not any(v for k, v in r.items() if k.startswith('synthetic_'))
    donor = r['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot']
    assert donor['source_sha256'] == '958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb'
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    shots = {}
    for shot in r['frames_captured']:
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        shots[shot['frame']] = shot
    return r, shots


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    clean, current = NdsImage.open('work/clean.nds'), NdsImage.open(ROM)
    current_digest = sha(ROM.read_bytes())
    assert current_digest == '0a03862a0a0a75c748e2f806016d2316f881eb9799907590715c41d251bf2a09'
    original, source_shots = report(SOURCE, sha(clean.source.read_bytes()))
    run, current_shots = report(CAP, current_digest)
    assert run['scripted_input_schedule'] == original['scripted_input_schedule']
    assert run['core_options'] == original['core_options']
    old = read(OLD)
    arm = current.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    groups = read('translations/source_plaque_grain_v1.json')['files']
    config = {r['id']: r for g in groups for r in g['records']}
    static_fonts, assets = [], {}
    for group in groups:
        asset = PxlImage.from_bytes(current.read_file(group['file_path']))
        original_asset = PxlImage.from_bytes(clean.read_file(group['file_path']))
        assert asset.source == NdsImage.open('out/all_routes_combined_v555_candidate.nds').read_file(group['file_path'])
        assert asset.source[:asset.pixels_offset] == original_asset.source[:original_asset.pixels_offset]
        static_fonts.extend(masks(asset, group['records'], font))
        assets[group['file_path']] = asset
    rows = []
    for old_row in old['all18_native_comparison_entries']:
        frame = old_row['frame']
        left, top, right, bottom = old_row['bounds']
        source_image = Image.open(source_shots[frame]['path']).convert('RGB')
        current_image = Image.open(current_shots[frame]['path']).convert('RGB')
        if old_row['number'] <= 17:
            record = config[old_row['id']]
            assert record['english'] == old_row['English'] and record['source_japanese'] == old_row['Japanese']
            asset = assets[old_row['source_asset']]
            for y in range(top, bottom):
                for x in range(left, right):
                    assert native5(current_image.getpixel((x, y))) == native5(asset.palette[asset.indices[y * asset.width + x]])
        source_path = ROOT / f"{old_row['number']:02d}_ORIGINAL_NATIVE.png"
        current_path = ROOT / f"{old_row['number']:02d}_V627_NATIVE.png"
        source_image.crop((left, top, right, bottom)).save(source_path)
        current_image.crop((left, top, right, bottom)).save(current_path)
        rows.append({'number': old_row['number'], 'id': old_row['id'], 'English': old_row['English'],
                     'Japanese': old_row['Japanese'], 'bounds': old_row['bounds'], 'frame': frame,
                     'source_crop': str(source_path), 'source_crop_sha256': sha(source_path.read_bytes()),
                     'current_crop': str(current_path), 'current_crop_sha256': sha(current_path.read_bytes()),
                     'source_PNG': source_shots[frame], 'current_PNG': current_shots[frame],
                     'source_runtime_label_included': old_row['original_label_drawn_at_runtime'],
                     'full_native_material_frame_letter_pixels_checked': (right - left) * (bottom - top),
                     'fully_completed': False, 'user_visual_review_pending': True})
    plan = read('work/analysis/direct_equipment_v270/runtime_plan.json')
    pool = bytes(MainCodeFile(arm, BASE).sections[3].data)
    tile_at = plan['tile_pointer'] - POOL
    tile = pool[tile_at:tile_at + 1408]
    previous_pool = bytes(MainCodeFile(NdsImage.open('out/all_routes_combined_v581_candidate.nds').read_file('/__arm9__.bin'), BASE).sections[3].data)
    assert tile == previous_pool[tile_at:tile_at + 1408]
    assert len(tile) == 1408 and struct.unpack_from('<H', tile)[0]
    hint_cases = []
    for text, frame, slot in (('Equipped Items', 6300, 208), ('Weapon', 6700, 16), ('Blue Oak Shield', 7100, 64)):
        im = Image.open(current_shots[frame]['path']).convert('RGB')
        hint_cases.append({'frame': frame, **hint(font, tile, im, text, slot)})
    assert len(rows) == 18 and len(static_fonts) == 17
    title_font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 22)
    body_font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 17)
    jp_font = ImageFont.truetype('C:/Windows/Fonts/msgothic.ttc', 20)
    sheets = []
    for label, subset in (('Assign_Sailors', rows[:7]), ('Sailor_Info', rows[7:])):
        sheet = Image.new('RGB', (940, 108 + len(subset) * 124), '#263238')
        draw = ImageDraw.Draw(sheet)
        draw.text((16, 10), label.replace('_', ' ') + ' — current V627 review', font=title_font, fill='white')
        draw.text((16, 44), 'Original Japanese screen', font=body_font, fill='#c5d1d6')
        draw.text((490, 44), 'Current English screen', font=body_font, fill='#c5d1d6')
        draw.text((16, 72), 'All entries remain open. Enlarged 4× with no smoothing.', font=body_font, fill='#e7d9aa')
        for index, row in enumerate(subset):
            y = 108 + index * 124
            draw.text((16, y), f"{row['number']:02d} {row['English']}", font=body_font, fill='#e7d9aa')
            draw.text((260, y), row['Japanese'], font=jp_font, fill='#e7d9aa')
            for x, key in ((16, 'source_crop'), (490, 'current_crop')):
                crop = Image.open(row[key])
                sheet.paste(crop.resize((crop.width * 4, crop.height * 4), Image.Resampling.NEAREST), (x, y + 30))
        path = ROOT / f'{label}_V627_SOURCE_REVIEW_4x.png'
        sheet.save(path)
        sheets.append({'path': str(path), 'sha256': sha(path.read_bytes())})
    save(ROOT / 'current_plaque_review_proof.json', {
        'candidate': str(ROM), 'candidate_sha256': current_digest,
        'new_current_capture_report': str(CAP / 'capture_report.json'),
        'new_current_capture_report_sha256': sha((CAP / 'capture_report.json').read_bytes()),
        'historical_clean_capture_report': str(SOURCE / 'capture_report.json'),
        'historical_clean_capture_report_sha256': sha((SOURCE / 'capture_report.json').read_bytes()),
        'same_14_action_schedule_core_options_and_byte_exact_donor': True,
        'ordinary_UI_controls_no_synthetic_RAM_ROM_or_inventory_fixtures': True,
        'all17_independent_complete_font_masks': static_fonts, 'all18_current_native_review_entries': rows,
        'static_plaque_files_exact_V555_and_equipment_tile_exact_V581': True,
        'current_native_static_pixels': sum(r['full_native_material_frame_letter_pixels_checked'] for r in rows[:17]),
        'current_complete_hint_cases': hint_cases, 'sheets': sheets,
        'all18_original_plaque_entries_fully_completed_false': True,
        'all22_historical_requirements_remain_in_scope': True,
        'source_grain_hidden_by_original_letters_is_reconstruction_not_recovered_pixels': True,
        'user_visual_review_pending_not_inferred_from_pixel_tests': True,
        'no_ROM_patch_or_registry_changed': True, 'full_goal_complete': False, 'canonical_promoted': False,
        'script_sha256': sha(Path(__file__).read_bytes())})
    print('V632:all18 current/source native plaque entries;17 complete glyph masks;3 full material hints;user review remains open.')


if __name__ == '__main__':
    main()
