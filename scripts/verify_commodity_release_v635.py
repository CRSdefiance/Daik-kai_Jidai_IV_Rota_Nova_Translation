"""Verify source-faithful names, actual full hints and complete cumulative release."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.commodity_fidelity import BASE, CHANGES, TABLE, apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_commodity_label_fixture_v635 import substitute
from scripts.prepare_commodity_fidelity_v635 import CONFIG, ROOT
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_regional_ui_v616 import full_cells
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v635_candidate.nds')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
PROFILE = 'all-routes-unified-v635'
RUN_PREFIX = 'commodity_fidelity_v635'


def report(name, frames, digest, *, fixture=False):
    root = CAP / name
    path = root / 'capture_report.json'
    data = read(path)
    assert data['frames'] == frames and data['ROM_sha256'] == digest
    assert data['cold_boot'] and not data['savestate_loaded'] and not data['callback_errors']
    synthetic = {k: v for k, v in data.items() if k.startswith('synthetic_') and v}
    if fixture:
        assert set(synthetic) == {'synthetic_complete_commodity_label_fixtures'}
    else:
        assert not synthetic
    donor = data.get('battery_save_preloaded')
    if donor:
        assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
        assert donor['source_sha256'] == '958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb'
    shots = {r['frame']: r for r in data['frames_captured']}
    for r in shots.values():
        assert sha(Path(r['path']).read_bytes()) == r['PNG_sha256']
    return root, data, shots, {'path': str(path), 'sha256': sha(path.read_bytes())}


def overlay_hint(im, font, text, x0, y0):
    result = im.copy()
    width = len(text) * 6 + 4
    for y in range(16):
        for x in range(width):
            result.putpixel((x0 + x, y0 + y), (255, 255, 255))
    for n, c in enumerate(text):
        mask = font.decode(c)
        for y in range(11):
            for x in range(6):
                if mask.getpixel((x, y)):
                    result.putpixel((x0 + 2 + n * 6 + x, y0 + 2 + y), (0, 8, 0))
    return result


def cached_names(arm, raw, rows):
    u = machine(arm)
    u.mem_write(BASE, raw)
    call(u, 0xCB124, ())
    objects = u.reg_read(UC_ARM_REG_R0) + 4
    results = []
    for row in rows:
        obj = objects + row['index'] * 16
        pointer = struct.unpack('<I', u.mem_read(obj + 4, 4))[0]
        value = bytes(u.mem_read(pointer, 64)).split(b'\0')[0].decode('ascii')
        assert value == row['English']
        assert pointer == struct.unpack_from('<I', arm, TABLE + row['index'] * 12)[0]
        results.append({'index': row['index'], 'complete_name': value, 'object': obj,
                        'actual_source_pointer': pointer})
    return results


def main():
    digest = sha(ROM.read_bytes())
    parent_path = Path('out/all_routes_combined_v633_candidate.nds')
    parent, current = NdsImage.open(parent_path), NdsImage.open(ROM)
    old_digest = sha(parent_path.read_bytes())
    arm, transform = apply_release(parent.read_file('/__arm9__.bin'),
                                   NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'), CONFIG)
    assert arm == current.read_file('/__arm9__.bin')
    before = {p: b for _, p, b in parent.iter_files()} | dict(parent.iter_components())
    after = {p: b for _, p, b in current.iter_files()} | dict(current.iter_components())
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {'/__arm9__.bin'}
    manifest, prior = read(ROM.with_suffix('.manifest.json')), read(parent_path.with_suffix('.manifest.json'))
    registry = read('translations/release_stack.json')
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == PROFILE
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['base_sha256'] == registry['canonical_baseline']['sha256']
    assert manifest['batches'] == prior['batches'] and len(manifest['batches']) == 470
    assert all(manifest['checks'].values()) and len(registry['accepted_layers']) == 114
    cfg = read(CONFIG)
    font = GameAsciiFont.from_arm9(arm)
    _, om, os, omr = report('ship_title_v633_market', 24100, old_digest)
    _, nm, ns, nmr = report(RUN_PREFIX + '_market', 24100, digest)
    assert om['scripted_input_schedule'] == nm['scripted_input_schedule'] and os.keys() == ns.keys() and len(ns) == 19
    assert 'battery_save_preloaded' not in nm
    for f in os:
        assert Image.open(os[f]['path']).tobytes() == Image.open(ns[f]['path']).tobytes()
    _, old, obs, obr = report('selection_contexts_v634_two_ship_baseline', 22600, old_digest)
    nr, new, nbs, nbr = report(RUN_PREFIX + '_two_ship', 22600, digest)
    assert old['scripted_input_schedule'] == new['scripted_input_schedule'] and obs.keys() == nbs.keys() and len(nbs) == 80
    changed = {4000: (48, 212), 4800: (80, 212), 18800: (48, 212),
               19000: (48, 212), 20400: (16, 266), 20600: (16, 266)}
    cases = []
    for f in obs:
        original = Image.open(obs[f]['path']).convert('RGB')
        actual = Image.open(nbs[f]['path']).convert('RGB')
        expected = overlay_hint(original, font, 'Iron Ore', *changed[f]) if f in changed else original
        assert actual.tobytes() == expected.tobytes(), f
        cases.append({'frame': f, 'whole_two_screen_pixels_exact_expected': True,
                      'only_complete_Iron_Ore_tooltip_expected_change': f in changed})
    fr, fixtures, fs, frr = report(RUN_PREFIX + '_tooltips', 17800, digest, fixture=True)
    declared = read(ROOT / 'tooltip_cases.json')
    records = fixtures['synthetic_complete_commodity_label_fixtures']
    assert len(records) == 17 and [r['selected_name_id'] for r in records] == list(CHANGES)
    initial = (fr / 'frame_004600_arm9_ram.bin').read_bytes()
    live_names = cached_names(arm, initial, cfg['records'])
    cached_names(arm, (nr / 'final_arm9_ram.bin').read_bytes(), cfg['records'])
    reference = Image.open(nbs[4800]['path']).convert('RGB')
    tooltip_cases = []
    for case, fixture in zip(declared, records, strict=True):
        i, frame = case['index'], case['frame']
        assert i == fixture['selected_name_id'] and frame == fixture['frame'] + (400 if i == 15 else 800)
        name = CHANGES[i][1]
        im = Image.open(fs[frame]['path']).convert('RGB')
        expected = overlay_hint(reference, font, name, 80, 212)
        assert im.tobytes() == expected.tobytes(), (i, name)
        glyph = full_cells(im, font, name, 82, 214, (0, 8, 0))
        field = fixture['commodity_object'] + 4
        assert all(field <= r['address'] < field + 4 for r in fixture['changes'])
        raw = (fr / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
        assert struct.unpack_from('<I', raw, field - BASE)[0] == fixture['new_name_pointer']
        assert fixture['new_name_pointer'] == struct.unpack_from('<I', arm, TABLE + i * 12)[0]
        tooltip_cases.append({'index': i, 'frame': frame, 'English': name,
                              'complete_font_mask': glyph, 'entire_hint_white_background_and_padding_exact': True,
                              'every_other_two_screen_pixel_exact_unmodified_current_control': True,
                              'only_one_label_pointer_fixture_not_stock_or_original_item_identity': True})
    invalid_fixtures = []
    for label, candidate, raw, item in (
        ('unreviewed-name', arm, initial, 93),
        ('wrong-ROM', parent.read_file('/__arm9__.bin'), initial, 90),
        ('wrong-RAM-size', arm, initial[:-1], 90)):
        try:
            substitute(candidate, raw, item)
        except ValueError as error:
            invalid_fixtures.append({'case': label, 'rejected': str(error)})
        else:
            raise AssertionError(label)
    previews = read(ROOT / 'native_preview_proof.json')
    consumers = read(ROOT / 'consumer_native_proof.json')
    assert previews['transform']['target_arm9_sha256'] == consumers['target_arm9_sha256'] == sha(arm)
    assert len(previews['all124_actual_native_getters']) == 124 and len(previews['all248_complete_town_name_rasters']) == 248
    assert len(consumers['all124_market_and_Local_cases']) == len(consumers['all124_actual_pointer_Price_Info_cases']) == 124
    expected_labels = {r['index']: r['English'] for r in cfg['records']}
    assert {r['index']: r['English'] for r in consumers['all124_market_and_Local_cases']} == expected_labels
    assert {r['index']: r['English'] for r in consumers['all124_actual_pointer_Price_Info_cases']} == expected_labels
    assert consumers['script_sha256'] == sha(Path('scripts/verify_commodity_consumers_v635.py').read_bytes())
    patch, preservation = read(ROOT / 'patch_proof.json'), read(ROOT / 'preservation_proof.json')
    assert patch['candidate_sha256'] == preservation['candidate_sha256'] == digest
    assert patch['exact_all_byte_reconstruction'] and preservation['current921_format_palette_extent_checks']
    assert preservation['all57_embedded_block_extents_exact']
    save(ROOT / 'release_proof.json', {
        'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
        'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
        'patch_sha256': patch['patch_sha256'], 'transform': transform,
        'all124_fresh_live_cached_names_before_fixture': live_names,
        'all124_fresh_ordinary_final_cached_names_exact': True,
        'all248_town_rasters124_Market_Local124_real_pointer_Price_Info_cases_pass': True,
        'all17_actual_controlled_full_name_tooltips': tooltip_cases,
        'three_invalid_fixture_contracts_rejected': invalid_fixtures,
        'all80_ordinary_two_ship_whole_screen_compositions': cases,
        'all19_no_save_no_fixture_New_Game_Market_frames_exact_V633': sorted(ns),
        'all_other_ROM_files_components_fonts_palettes_helpers_and_section_shapes_exact_V633': True,
        'all470_batches114_layers921_graphics57_embedded_extents_and_exact_patch_retained': True,
        'reports': [omr, nmr, obr, nbr, frr],
        'controlled_labels_do_not_prove_normal_stock_or_acquisition_for_other16_goods': True,
        'other107_commodity_spellings_preserved_not_newly_semantically_approved': True,
        'all18_plaques_incomplete_all22_historical_scopes_retained': True,
        'full_goal_complete': False, 'canonical_promoted': False,
        'script_sha256': sha(Path(__file__).read_bytes())})
    print(PROFILE + ':17 complete actual tooltips,124 fresh cached names,80 full compositions,19 ordinary screens and exact stack/patch pass.')


if __name__ == '__main__':
    main()
