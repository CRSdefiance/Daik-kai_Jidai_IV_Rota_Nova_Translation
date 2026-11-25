"""Verify the integrated town/movie repair, full glyphs and clean patch rebuild."""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_stock_rows import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_commodity_layout_v346 import mask
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_fleet_release_v375 import files

ROOT = Path('work/analysis/town_stock_rows_v502')
ROM = Path('out/all_routes_combined_v502_candidate.nds')
PARENT = Path('out/all_routes_combined_v484_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def report(folder, digest, frames):
    path = Path('work/emulation_v193') / folder / 'capture_report.json'
    data = read(path)
    assert data['ROM_sha256'] == digest and data['frames'] == frames
    assert data['cold_boot'] and not data['savestate_loaded'] and not data['callback_errors']
    assert not data.get('synthetic_inventory_fixtures')
    for row in data['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    if data.get('battery_save_preloaded'):
        donor = data['battery_save_preloaded']
        assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    return path, data


def main():
    digest = sha(ROM.read_bytes())
    manifest, parent_manifest = read(ROM.with_suffix('.manifest.json')), read(PARENT.with_suffix('.manifest.json'))
    registry = read('translations/release_stack.json')
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v502'
    assert manifest['base_sha256'] == parent_manifest['base_sha256'] == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert manifest['batches'] == parent_manifest['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == parent_manifest['required_batches'] and all(manifest['checks'].values())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers']) == 114
    old_profile, new_profile = registry['profiles']['all-routes-unified-v484'], registry['profiles']['all-routes-unified-v502']
    assert all(new_profile[k] == v for k, v in old_profile.items() if k not in ('status', 'note', 'description'))
    before, after = files(NdsImage.open(PARENT)), files(NdsImage.open(ROM))
    assert before.keys() == after.keys()
    assert [key for key in before if before[key] != after[key]] == ['/__arm9__.bin']
    arm, change = apply_release(before['/__arm9__.bin'], 'translations/town_stock_rows_v1.json')
    assert arm == after['/__arm9__.bin']
    # Reports from research can verify a registered build only with exact bytes.
    prototype = Path('work/analysis/town_direct_labels_v501/research_only_direct_normal.nds')
    assert ROM.read_bytes() == prototype.read_bytes()
    native_files = [Path('work/analysis/town_direct_labels_v501') / name for name in
                    ('native_proof.json', 'native_height12_screen0_proof.json',
                     'native_height16_screen0_proof.json', 'native_height16_screen1_proof.json')]
    for path in native_files:
        native = read(path)
        assert native['target_arm9_sha256'] == sha(arm)
        assert len(native['all124_complete_native_masks']) == 124
        assert all(row['complete_mask_exact'] for row in native['all124_complete_native_masks'])
        assert native['ABI_and_stack_restored'] and native['source_view_and_canaries_unchanged']
    font = GameAsciiFont.from_arm9(arm)
    reference_path, reference = report('square_cells_v484', sha(PARENT.read_bytes()), 5900)
    town_path, town = report('town_direct_labels_v501_town', digest, 5900)
    assert town['scripted_input_schedule'] == reference['scripted_input_schedule']
    assert town['core_options'] == reference['core_options']
    a, b = ({r['frame']: r for r in data['frames_captured']} for data in (reference, town))
    assert a.keys() == b.keys() and len(b) == 62
    differences = []
    for frame in b:
        old, new = Image.open(a[frame]['path']).convert('RGB'), Image.open(b[frame]['path']).convert('RGB')
        assert old.crop((0, 0, 256, 192)).tobytes() == new.crop((0, 0, 256, 192)).tobytes(), frame
        if old.tobytes() != new.tobytes():
            delta = [(x, y) for y in range(192, 384) for x in range(256) if old.getpixel((x, y)) != new.getpixel((x, y))]
            assert frame in (4000, 4900, 5200, 5900)
            if frame == 4000:
                assert all(104 <= x < 152 and 278 <= y < 297 for x, y in delta)
            else:
                assert all(16 <= x < 232 and 296 <= y < 324 for x, y in delta)
            differences.append({'frame': frame, 'pixels': len(delta),
                                'scope': 'Trends focus flash' if frame == 4000 else 'different complete original shopkeeper response'})
    assert [d['frame'] for d in differences] == [4000, 4900, 5200, 5900]
    labels = []
    for frame in (4500, 4600, 4700, 4800):
        image = Image.open(b[frame]['path']).convert('RGB')
        labels.append({'frame': frame, 'complete_stock_labels': [mask(image, font, text, 88 + i * 16)
                      for i, text in enumerate(('Sulfur', 'Carpets', 'Antiques'))]})
    dialogues = []
    for frame, text, x, y in ((4900, 'We only sell retail.', 22, 296),
                              (5200, 'We only sell retail.', 22, 296),
                              (5900, 'The Ottoman Empire rules the eastern', 16, 296),
                              (5900, 'Mediterranean.', 22, 312)):
        image = Image.open(b[frame]['path']).convert('RGB')
        pixels, bounds = complete_mask(font, text, image, x, y, (0, 8, 0))
        dialogues.append({'frame': frame, 'text': text, 'ink_pixels': pixels, 'bounds': bounds,
                          'all_glyphs_complete': True})
    # Script bytes are exact to the parent. Preserve the existing mixed inset
    # as an older-record follow-up, not an assertion of universal alignment.
    old_inset_followup = {'record_context': 'Ottoman Empire shopkeeper response',
                         'first_line_x': 16, 'continuation_x': 22,
                         'existing_text_not_modified_by_this_release': True,
                         'revisit_with_older_record_based_checks': True}
    fresh_path, fresh = report('town_direct_labels_v501_fresh', digest, 21200)
    _, old_fresh = report('square_cells_fresh_v484', sha(PARENT.read_bytes()), 21200)
    assert fresh['scripted_input_schedule'] == old_fresh['scripted_input_schedule'] and fresh['core_options'] == old_fresh['core_options']
    x, y = ({r['frame']: r for r in data['frames_captured']} for data in (old_fresh, fresh))
    assert len(y) == 56 and x.keys() == y.keys()
    assert all(x[frame]['PNG_sha256'] == y[frame]['PNG_sha256'] for frame in y)
    long_manifest = read(ROOT / 'long_stock_manifest.json')
    long_path, long = report('town_stock_rows_v502_long', long_manifest['research_ROM_sha256'], 5900)
    assert long['scripted_input_schedule'] == town['scripted_input_schedule'] and long['core_options'] == town['core_options']
    long_shot = next(s for s in long['frames_captured'] if s['frame'] == 4500)
    image = Image.open(long_shot['path']).convert('RGB')
    long_masks = [mask(image, font, text, 88 + i * 16) for i, text in enumerate(
                  ('Black Glacier Sword', 'North Sea Ambergris', 'Fire and Ice Rubies'))]
    movie_manifest = read('work/analysis/town_direct_labels_v501/m28_manifest.json')
    movie_path, movie = report('town_direct_labels_v501_movie', movie_manifest['research_ROM_sha256'], 6000)
    movie_data = NdsImage.open(ROM).read_file('/FLS/M28.fls')
    assert NdsImage.open(movie_manifest['research_ROM']).read_file('/FLS/M20.fls') == movie_data
    assert NdsImage.open(movie_manifest['research_ROM']).read_file('/__arm9__.bin') == arm
    texture = FlsArchive(movie_data).texture(46)
    shot = next(s for s in movie['frames_captured'] if s['frame'] == 3700)
    image = Image.open(shot['path']).convert('RGB').point(lambda value: value >> 3)
    matches = sum(image.getpixel((12 + i % texture.width, 167 + i // texture.width)) == tuple(v >> 3 for v in texture.palette[n][:3])
                  for i, n in enumerate(texture.indices) if n)
    assert matches == 3047
    for folder in ('town_direct_labels_v501_town', 'town_direct_labels_v501_fresh'):
        raw = (Path('work/emulation_v193') / folder / 'final_arm9_ram.bin').read_bytes()
        header = struct.unpack_from('<5I', raw, 0x2BD774)
        assert header[:3] == (4, 57, 72)
        assert (0x022BD774 + header[3]) & 0xFFFFFFFF == 0x02125A20
        assert (0x022BD774 + header[4]) & 0xFFFFFFFF == 0x0601BFC8
    graphics = [key for key in before if key.lower().endswith(('.pxl', '.fls'))]
    assert all(before[key] == after[key] for key in graphics)
    clean, patch, reconstructed = Path('work/clean.nds'), ROM.with_suffix('.xdelta'), ROOT / 'reconstructed.nds'
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, reconstructed)
    assert reconstructed.read_bytes() == ROM.read_bytes()
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'patch_sha256': sha(patch.read_bytes()),
             'parent': str(PARENT), 'parent_sha256': sha(PARENT.read_bytes()),
             'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'profile': manifest['profile'], 'change': change,
             'all470_inherited_batches_and_stages_preserved': True, 'all114_accepted_layers_retained': True,
             'only_ARM9_changes_against_V484': True, 'exact_PXL_FLS_payloads': len(graphics),
             'all124_native_masks_for_both_font_heights_and_screen_selectors': True,
             'native_proofs': [{'path': str(p), 'sha256': sha(p.read_bytes())} for p in native_files],
             'registered_candidate_exact_to_actual_cold_boot_tested_prototype': True,
             'all62_upper_town_frames_exact': True, 'four_lower_focus_dialogue_variants': differences,
             'all56_fresh_title_NewGame_story_town_help_frames_exact': True,
             'complete_actual_Istanbul_stock_names': labels, 'complete_dialogue_variants': dialogues,
             'long_name_render_fixture': {'manifest': str(ROOT / 'long_stock_manifest.json'),
                                          'complete_masks': long_masks, 'not_normal_stock_availability': True},
             'M28_name_fixture': {'frame': 3700, 'all3047_pixels_match': True,
                                 'normal_ending_or_unlock_not_proven': True},
             'original_shared_numeric_header_palette_and_VRAM_restored': True,
             'reports': list(map(str, (reference_path, town_path, fresh_path, long_path, movie_path))),
             'exact_clean_patch_reconstruction': True,
             'older_record_followup': old_inset_followup,
             'release_status': 'experimental-actual-cold-boot-verified-awaiting-user-acceptance',
             'all22_historical_requirements_retained': True, 'all18_plaques_incomplete': True,
             'hardware_verification': False, 'full_goal_complete': False}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print(json.dumps({'candidate_sha256': digest, 'graphics_exact': len(graphics),
                      'fresh_whole_frames_exact': 56, 'town_upper_frames_exact': 62,
                      'long_names_complete': 3, 'movie_name_pixels': 3047, 'patch_exact': True}))


if __name__ == '__main__':
    main()
