"""Verify cumulative release, all ordinary region hints and exact boundary repair."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.region_name_boundaries import BASE, LABELS, apply_release, validate_names
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.probe_worldmap_overlays_v638 import color5
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/region_boundaries_v640')
ROM = Path('out/all_routes_combined_v640_candidate.nds')
PARENT = Path('out/all_routes_combined_v636_candidate.nds')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def report(name, digest, frames):
    path = CAP / name / 'capture_report.json'
    data = read(path)
    assert data['ROM_sha256'] == digest and data['frames'] == frames
    assert data['cold_boot'] and not data['savestate_loaded'] and not data['callback_errors']
    assert not data.get('battery_save_preloaded')
    assert not any(v for k, v in data.items() if k.startswith('synthetic_'))
    shots = {r['frame']: r for r in data['frames_captured']}
    for row in data['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    for row in data.get('read_only_capture_RAM_snapshots', []) + data.get('read_only_pause_RAM_snapshots', []):
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    return data, shots, {'path': str(path), 'sha256': sha(path.read_bytes())}


def main():
    rom, parent, clean = NdsImage.open(ROM), NdsImage.open(PARENT), NdsImage.open('work/clean.nds')
    digest, parent_digest = sha(ROM.read_bytes()), sha(PARENT.read_bytes())
    target, transform = apply_release(parent.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin'),
                                      'translations/region_name_boundaries_v1.json')
    assert target == rom.read_file('/__arm9__.bin')
    before = {p: b for _, p, b in parent.iter_files()} | dict(parent.iter_components())
    after = {p: b for _, p, b in rom.iter_files()} | dict(rom.iter_components())
    assert before.keys() == after.keys()
    assert {p for p in before if before[p] != after[p]} == {'/__arm9__.bin'}
    manifest, old_manifest = read(ROM.with_suffix('.manifest.json')), read(PARENT.with_suffix('.manifest.json'))
    registry = read('translations/release_stack.json')
    assert manifest['profile'] == 'all-routes-unified-v640' and manifest['candidate_sha256'] == digest
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['base_sha256'] == registry['canonical_baseline']['sha256']
    assert manifest['batches'] == old_manifest['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == old_manifest['required_batches']
    assert manifest['changed_paths'] == old_manifest['changed_paths'] and len(registry['accepted_layers']) == 114
    assert all(manifest['checks'].values())
    font = GameAsciiFont.from_arm9(target)
    market, market_shots, market_receipt = report('region_boundaries_v640_market', digest, 24100)
    baselines, regression = [], set()
    for name, frames in [('commodity_fidelity_v636_market', 24100), ('commodity_fidelity_v636_startup_636', 19700)]:
        old, shots, receipt = report(name, parent_digest, frames)
        assert market['scripted_input_schedule'] == old['scripted_input_schedule']
        for frame, shot in shots.items():
            assert Image.open(shot['path']).tobytes() == Image.open(market_shots[frame]['path']).tobytes()
            regression.add(frame)
        baselines.append(receipt)
    assert len(regression) == 32
    current, shots, current_receipt = report('region_boundaries_v640_map', digest, 39200)
    source, source_shots, source_receipt = report('region_boundaries_v640_map_source', parent_digest, 39200)
    assert current['scripted_input_schedule'] == source['scripted_input_schedule'] == read(ROOT / 'all7_area_inputs.json')
    # Current source getters must read the actual resident strings, without restaging
    # code or constructing substitute name objects in the exported RAM.
    raw_path = CAP / 'region_boundaries_v640_map/frame_037200_arm9_ram.bin'
    raw = raw_path.read_bytes()
    u = machine(target)
    u.mem_write(BASE, raw)
    live_names = []
    for row in validate_names(target):
        call(u, 0x9458C, (row['index'],))
        record = u.reg_read(UC_ARM_REG_R0)
        pointer = struct.unpack('<I', u.mem_read(record, 4))[0]
        assert pointer == row['pointer']
        value = bytes(u.mem_read(pointer, 32)).split(b'\0')[0].decode('ascii')
        assert value == row['English']
        live_names.append({'index': row['index'], 'native_record': record, 'pointer': pointer, 'complete_name': value})
    cases = []
    for case in read(ROOT / 'ordinary_region_tooltip_cases.json'):
        frame, text = case['frame'], LABELS[case['index']]
        image = Image.open(shots[frame]['path']).convert('RGB')
        old = Image.open(source_shots[frame]['path']).convert('RGB')
        x, y = case['origin']
        width, height = case['width'], case['height']
        ink, bounds = complete_mask(font, text, image, x + 2, y + 2, (0, 8, 0))
        expected_ink = set()
        for n, char in enumerate(text):
            glyph = font.decode(char)
            expected_ink.update((x + 2 + n * 6 + gx, y + 2 + gy)
                                for gy in range(11) for gx in range(6) if glyph.getpixel((gx, gy)))
        occlusion = 0
        for dy in range(height):
            for dx in range(width):
                p = (x + dx, y + dy)
                blue = old.getpixel(p) == (0, 0, 255)
                expected = (0, 0, 255) if blue else (0, 8, 0) if p in expected_ink else (255, 255, 255)
                assert image.getpixel(p) == expected, (frame, p)
                occlusion += blue
        if case['index'] != 6:
            assert image.tobytes() == old.tobytes(), frame
            only_hint_change = False
        else:
            complete_mask(font, 'AmericasMed.', old, x + 2, y + 2, (0, 8, 0))
            old_width = len('AmericasMed.') * 6 + 4
            differences = [(xx, yy) for yy in range(384) for xx in range(256)
                           if image.getpixel((xx, yy)) != old.getpixel((xx, yy))]
            assert differences and all(x <= xx < x + old_width and y <= yy < y + height for xx, yy in differences)
            # The former suffix/backing tail must restore actual underlying map pixels.
            # Its blue selected-area border is independently retained from the old control.
            header = 0x279B38
            palette = struct.unpack_from('<16H', raw, header + 20)
            packed = raw[header + 52:header + 52 + 19520]
            indices = [n for b in packed for n in (b & 15, b >> 4)]
            for yy in range(y, y + height):
                for xx in range(x + width, x + old_width):
                    expected = 0x7C00 if old.getpixel((xx, yy)) == (0, 0, 255) else palette[indices[(yy - 208) * 244 + xx - 6]] & 32767
                    assert color5(image.getpixel((xx, yy))) == expected
            only_hint_change = True
        cases.append({**case, 'complete_font_ink': ink, 'glyph_bounds': bounds,
                      'complete_current_hint_face_margin_and_blank_cells_exact': True,
                      'original_blue_area_border_occlusion_pixels': occlusion,
                      'old_AmericasMed_and_its_extra_hint_tail_corrected': only_hint_change,
                      'every_other_two_screen_pixel_exact_source_control': True,
                      'ordinary_UI_no_fixture': True})
    assert {r['index'] for r in cases} == set(range(7))
    # The current map prefix also preserves all prior opening/map compositions.
    prior = read(CAP / 'worldmap_composition_v638/capture_report.json')
    prior_shots = {r['frame']: r for r in prior['frames_captured']}
    for frame in (34800, 35200, 35600, 36000):
        assert Image.open(shots[frame]['path']).tobytes() == Image.open(prior_shots[frame]['path']).tobytes()
    patch, preservation = read(ROOT / 'patch_proof.json'), read(ROOT / 'preservation_proof.json')
    assert patch['candidate_sha256'] == preservation['candidate_sha256'] == digest
    assert patch['exact_all_byte_reconstruction'] and sha(ROM.with_suffix('.xdelta').read_bytes()) == patch['patch_sha256']
    assert preservation['current921_format_palette_extent_checks'] and preservation['all57_embedded_block_extents_exact']
    preview = read(ROOT / 'native_preview_proof.json')
    assert preview['target_arm9_sha256'] == sha(target)
    save(ROOT / 'release_proof.json', {
        'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
        'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
        'patch_sha256': patch['patch_sha256'], 'transform': transform,
        'all8_actual_resident_native_name_getters': live_names,
        'all7_ordinary_region_tooltips_and_repeat': cases,
        'Global_complete_native_bitmap_preview_only_not_an_eighth_selected_area': True,
        'all32_unique_startup_New_Game_story_town_and_Market_frames_exact_V636': sorted(regression),
        'four_current_map_prefix_whole_frames_exact_V638': [34800, 35200, 35600, 36000],
        'all_other_ROM_files_and_staged_sections_exact_V636': True,
        'all470_batches114_layers921_graphics57_embedded_extents_and_exact_patch_retained': True,
        'reports': [market_receipt, current_receipt, source_receipt], 'historical_regression_reports': baselines,
        'legacy_fixed_text_exact_capacity_census': read(ROOT / 'legacy_fixed_text_boundary_census.json'),
        'native_preview_proof_sha256': sha((ROOT / 'native_preview_proof.json').read_bytes()),
        'all18_plaque_entries_incomplete_all22_historical_scopes_retained': True,
        'canonical_promoted': False, 'full_goal_complete': False,
        'script_sha256': sha(Path(__file__).read_bytes())})
    print('V640 passes:all8 live names,all7 ordinary area hints,old AmericasMed regression,32 startup/Market frames,full integration/preservation and exact patch.')


if __name__ == '__main__':
    main()
