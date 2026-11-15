"""Verify previously omitted original credit planes and current Rafael playback.

Historical V534 display evidence remains labeled historical. A separate current
V573 run exercises the original ending branch using an authorized one-byte RAM
fixture. Neither implies earned completion or all-frame hardware coverage.
"""

import argparse
import itertools
import json
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_ending_fixture_v537 import request_ending
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

ROOT = Path('work/analysis/ending_native_v578')
CAPTURE_ROOT = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
CURRENT = Path('out/all_routes_combined_v573_candidate.nds')
HISTORICAL = Path('out/all_routes_combined_v534_candidate.nds')
CASES = [(0, 'rafael', 'rafael', 6), (1, 'hodram', 'hodram_complete', 10),
         (2, 'lil', 'lil_town', 8), (3, 'maria', 'maria', 6)]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def quantized(path):
    with Image.open(path) as image:
        return image.convert('RGB').point(lambda value: value >> 3)


def source_caption(movie, index):
    archive = FlsArchive(movie)
    texture = archive.texture(index)
    record = archive.records[index]
    assert (texture.width, texture.height) == (256, 16)
    assert (record[0] >> 16, record[1] & 65535) == (256, 16)
    white, dark = [], []
    for offset, n in enumerate(texture.indices):
        rgb = tuple(value >> 3 for value in texture.palette[n][:3])
        if n == 0:
            assert rgb == (0, 0, 0)
        elif rgb == (31, 31, 31):
            white.append([offset % 256, offset // 256])
        else:
            assert rgb == (0, 0, 0)
            dark.append([offset % 256, offset // 256])
    assert len(white) == 306 and len(dark) == 961
    mask = Image.new('L', (256, 192))
    for x, y in white:
        mask.putpixel((x, y + 90), 255)
    states = {mask.point([0] + [level] * 255).convert('RGB').tobytes(): level for level in range(1, 32)}
    return texture, white, dark, states


def verify_captures(folder, rom_path, captain, index):
    rom = NdsImage.open(rom_path)
    digest = sha(rom_path.read_bytes())
    report_path = folder / 'capture_report.json'
    report = read(report_path)
    assert report['ROM_sha256'] == digest and report['cold_boot']
    assert not report['savestate_loaded'] and not report['callback_errors']
    assert not report['earned_completion_verified']
    fixtures = report['synthetic_ending_fixtures']
    assert len(fixtures) == 1
    fixture = fixtures[0]
    assert fixture['active_captain_id'] == captain
    assert fixture['native_dispatch_arguments'] == [29 + captain, 0, 0, 0]
    assert fixture['changes'] == [{'address': 0x022796BC, 'before': 1, 'after': 4}]
    raw = (folder / f"frame_{fixture['frame']:06d}_arm9_ram.bin").read_bytes()
    arm = rom.read_file('/__arm9__.bin')
    _, replay = request_ending(arm, raw, captain)
    assert replay == {k: v for k, v in fixture.items() if k != 'frame'}
    if 'battery_save_preloaded' in report:
        save = report['battery_save_preloaded']
        assert sha(Path(save['source']).read_bytes()) == save['source_sha256']
        assert save['copied_byte_exact_before_cold_boot']
    movie_path = f'/FLS/M{29 + captain}.fls'
    movie = rom.read_file(movie_path)
    texture, white, dark, states = source_caption(movie, index)
    source_tile = texture.render().convert('RGB').point(lambda value: value >> 3).tobytes()
    archive = FlsArchive(movie)
    scene_refs = {i: archive.texture(i).render().convert('RGB').crop((0, 0, 256, 192)).point(lambda value: value >> 3).tobytes()
                  for i in range(1, archive.count)
                  if archive.texture(i).width >= 256 and archive.texture(i).height >= 192}
    credits, scenes, table = [], [], {}
    for shot in report['frames_captured']:
        path = Path(shot['path'])
        assert sha(path.read_bytes()) == shot['PNG_sha256']
        table.setdefault(shot['frame'], shot)
    for frame, shot in table.items():
        if frame <= fixture['frame']:
            continue
        image = quantized(shot['path'])
        upper = image.crop((0, 0, 256, 192)).tobytes()
        if upper in states:
            level = states[upper]
            if level == 31:
                assert image.crop((0, 90, 256, 106)).tobytes() == source_tile
            credits.append({'frame': frame, 'native_gray_level': level, 'caption': shot['path'],
                            'PNG_sha256': shot['PNG_sha256'], 'complete_white_source_points': 306,
                            'full49152_upper_pixels_exact_to_uniform_credit_state': True,
                            'bounds': [0, 90, 256, 106], 'first_and_final_source_characters_included': True})
        for i, expected in scene_refs.items():
            if upper == expected:
                scenes.append({'frame': frame, 'texture': i, 'full49152_upper_pixels_exact': True,
                               'caption': shot['path'], 'PNG_sha256': shot['PNG_sha256']})
    assert credits and any(c['native_gray_level'] == 31 for c in credits)
    assert scenes
    return {'captain_id': captain, 'ROM': str(rom_path), 'ROM_sha256': digest,
            'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
            'movie': movie_path, 'movie_sha256': sha(movie), 'texture': index,
            'native_header_view': [archive.records[index][0] >> 16,
                                   archive.records[index][1] & 65535],
            'credit_wording_retained_from_original_English': 'SpecialThanks : BRIDGE Inc.',
            'white_source_points': white, 'dark_source_points': dark,
            'source_tile_sha256_5bit_RGB': sha(source_tile), 'credit_cases': credits,
            'visible_credit_gray_levels': sorted({c['native_gray_level'] for c in credits}),
            'full_scene_cases': scenes, 'distinct_complete_scene_textures': sorted({c['texture'] for c in scenes}),
            'fixture': fixture, 'earned_completion_verified': False,
            'identical_credit_pixels_do_not_disambiguate_texture_instances': True}, table


def verify_split_pans(rom, previous, tables):
    """Compare whole displayed source windows; do not invent unseen tile order."""
    results = []
    # M30 texture4 is a sparse gray streak/effect, not a photo segment.
    for captain, indexes in ((1, [1, 2, 3]), (2, [1, 2, 3])):
        case = previous[captain]
        movie = rom.read_file(case['movie'])
        archive = FlsArchive(movie)
        tiles = {i: archive.texture(i).render().convert('RGB').point(lambda value: value >> 3)
                 for i in indexes}
        assert all(tile.width == 256 for tile in tiles.values())
        source_height = sum(tile.height for tile in tiles.values())
        candidates, canvases = {}, {}
        stride = 256 * 3
        for order in itertools.permutations(indexes):
            canvas = Image.new('RGB', (256, source_height))
            y = 0
            for i in order:
                canvas.paste(tiles[i], (0, y))
                y += tiles[i].height
            raw = canvas.tobytes()
            canvases[order] = raw
            for top in range(source_height - 192 + 1):
                key = sha(raw[top * stride:(top + 192) * stride])
                candidates.setdefault(key, []).append((order, top))
        matches = []
        for frame, shot in tables[captain].items():
            if frame <= case['fixture']['frame']:
                continue
            actual = quantized(shot['path']).crop((0, 0, 256, 192)).tobytes()
            choices = candidates.get(sha(actual), [])
            if not choices:
                continue
            assert all(actual == canvases[order][top * stride:(top + 192) * stride]
                       for order, top in choices)
            matches.append({'frame': frame, 'capture': shot['path'], 'PNG_sha256': shot['PNG_sha256'],
                            'full49152_source_composite_pixels_exact': True,
                            'source_window_candidates': [{'order': list(order), 'source_y': top}
                                                         for order, top in choices]})
        assert matches
        orders = set(canvases)
        for match in matches:
            orders &= {tuple(c['order']) for c in match['source_window_candidates']}
        assert orders
        coverage = None
        if len(orders) == 1:
            order = next(iter(orders))
            observed = set()
            for match in matches:
                selected = [c['source_y'] for c in match['source_window_candidates'] if tuple(c['order']) == order]
                assert len(selected) == 1
                observed.update(range(selected[0], selected[0] + 192))
            coverage, origin = [], 0
            for i in order:
                rows = sorted(y - origin for y in observed if origin <= y < origin + tiles[i].height)
                coverage.append({'texture': i, 'height': tiles[i].height, 'observed_source_rows': rows,
                                 'unobserved_source_rows': sorted(set(range(tiles[i].height)) - set(rows))})
                origin += tiles[i].height
        results.append({'captain_id': captain, 'historical_report': case['report'], 'movie': case['movie'],
                        'source_movie_sha256': sha(movie), 'textures_considered': indexes,
                        'exact_full_upper_frame_composites': matches,
                        'orders_consistent_with_all_observed_windows': [list(order) for order in sorted(orders)],
                        'source_row_coverage_if_order_unique': coverage,
                        'source_order_is_pixel_inferred_not_a_GPU_binding_trace': True,
                        'unobserved_tiles_rows_fades_and_other_transforms_not_cleared': True,
                        'fresh_current_playback_not_claimed': True})
    return results


def main(historical_only=False):
    current, historical, clean = map(NdsImage.open, (CURRENT, HISTORICAL, Path('work/clean.nds')))
    provenance = read(ROOT / 'current_fixture_provenance.json')
    assert sha(CURRENT.read_bytes()) == provenance['candidate_sha256']
    assert sha(current.read_file('/__arm9__.bin')) == provenance['ARM9_sha256']
    for row in provenance['original_code_ranges']:
        lo, hi = row['offset']
        samples = [image.read_file('/__arm9__.bin')[lo:hi] for image in (current, historical, clean)]
        assert samples[0] == samples[1] == samples[2]
        assert sha(samples[0]) == row['sha256']
    for path, expected in provenance['original_ending_movies'].items():
        assert current.read_file(path) == historical.read_file(path) == clean.read_file(path)
        assert sha(current.read_file(path)) == expected
    for key in ('source_save', 'test_save'):
        assert sha(Path(provenance[key]).read_bytes()) == provenance[key + '_sha256']

    previous, tables = [], {}
    for captain, label, suffix, index in CASES:
        folder = CAPTURE_ROOT / f'ending_caller_v537_{suffix}'
        case, table = verify_captures(folder, HISTORICAL, captain, index)
        case['captain'] = label
        previous.append(case)
        tables[captain] = table
    pans = verify_split_pans(current, previous, tables)
    if historical_only:
        (ROOT / 'historical_credit_planes_proof.json').write_text(
            json.dumps(previous, indent=2) + '\n', encoding='utf-8')
        print('Four original credit planes:306 complete white points plus961 dark points; all4096 tile/49152 upper pixels exact.')
        return

    folder = CAPTURE_ROOT / 'ending_native_v578_rafael'
    case, table = verify_captures(folder, CURRENT, 0, 6)
    report = read(folder / 'capture_report.json')
    assert report['frames'] == 11600
    assert report['scripted_input_schedule'] == read(ROOT / 'rafael_inputs.json')
    assert len(case['credit_cases']) > 1 and len(case['visible_credit_gray_levels']) > 1
    assert case['distinct_complete_scene_textures'] == [1, 2, 3, 4, 5, 7]
    shared = []
    for frame in sorted(table.keys() & tables[0].keys()):
        if not 3000 < frame <= 11600:
            continue
        actual = quantized(table[frame]['path']).crop((0, 0, 256, 192)).tobytes()
        expected = quantized(tables[0][frame]['path']).crop((0, 0, 256, 192)).tobytes()
        assert actual == expected, ('Current/historical native ending differs', frame)
        shared.append(frame)
    assert len(shared) >= 60

    arm = current.read_file('/__arm9__.bin')
    raw = (folder / 'frame_003000_arm9_ram.bin').read_bytes()
    for bad_arm, captain in ((arm, 1), (bytes([arm[0] ^ 1]) + arm[1:], 0)):
        try:
            request_ending(bad_arm, raw, captain)
        except ValueError:
            pass
        else:
            raise ValueError('Unverified source/wrong-captain negative control accepted')
    from dk4tool.dialogue.font_audit import GameAsciiFont

    font = GameAsciiFont.from_arm9(arm)
    image = Image.open(table[11280]['path']).convert('RGB')
    prompt_ink, bounds = complete_mask(font, 'Save the ending data?', image, 16, 296, (0, 8, 0))
    effect = FlsArchive(current.read_file('/FLS/M30.fls')).texture(4)
    assert sum(bool(index) for index in effect.indices) == 46
    result = {'format': 'dk4-ending-credit-native-proof-v578', 'candidate': str(CURRENT),
              'candidate_sha256': provenance['candidate_sha256'], 'current_Rafael_playback': case,
              'current_complete_ending_save_prompt': {'frame': 11280, 'ink_pixels': prompt_ink, 'bounds': bounds},
              'historical_V534_credit_planes': previous,
              'historical_split_pan_compositions': pans,
              'separate_M30_effect_texture': {
                  'texture': 4, 'dimensions': [effect.width, effect.height],
                  'nonzero_source_points': 46, 'source_art_review': 'Small gray streak consistent with a shooting star; no Japanese text observed.',
                  'retain_original_art': True, 'not_a_photographic_pan_tile': True,
                  'actual_effect_transform_palette_and_native_pixels_not_verified': True},
              'all_four_current_movie_files_and_five_original_code_ranges_exact_source': True,
              'current_vs_historical_full_upper_shared_frames': shared,
              'native_credit_geometry': [0, 90, 256, 106],
              'current_captions_and_full_scene_pixels_exact': True,
              'uniform_gray_pixel_states_are_not_internal_GPU_alpha_measurements': True,
              'wrong_captain_and_unverified_ARM9_rejected': True,
              'one_byte_synthetic_state_change_not_earned_completion': True,
              'current_original_donor_and_all_used_fixture_sources_unchanged': True,
              'other_three_current_playbacks_not_retested': True,
              'every_intervening_frame_or_transition_not_claimed': True,
              'production_ROM_changed': False, 'all18_plaques_remain_incomplete': True,
              'full_goal_complete': False}
    (ROOT / 'native_ending_credit_proof.json').write_text(
        json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'current_Rafael_credit_frames': len(case['credit_cases']),
                      'current_Rafael_credit_levels': case['visible_credit_gray_levels'],
                      'current_complete_scene_textures': case['distinct_complete_scene_textures'],
                      'current_historical_upper_matches': len(shared),
                      'historical_credit_planes': len(previous),
                      'historical_split_pan_full_frames': [len(p['exact_full_upper_frame_composites']) for p in pans],
                      'production_changed': False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--historical-only', action='store_true')
    main(parser.parse_args().historical_only)
