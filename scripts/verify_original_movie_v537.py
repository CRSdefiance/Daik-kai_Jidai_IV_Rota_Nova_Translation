"""Original startup movie and bounded original ending-state display evidence."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_ending_fixture_v537 import request_ending
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_m28_progressive_v503 import full_match, points
from scripts.verify_movie_gpu_fixtures_v336 import quantized

ROM = Path('out/all_routes_combined_v534_candidate.nds')
OUT = Path('work/analysis/ending_caller_v537')
CAPTURES = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def captures(folder, digest):
    report_path = folder / 'capture_report.json'
    report = read(report_path)
    assert report['ROM_sha256'] == digest and report['cold_boot']
    assert not report['savestate_loaded'] and not report['callback_errors']
    for shot in report['frames_captured']:
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
    return report, {'path': str(report_path), 'sha256': sha(report_path.read_bytes())}


def main():
    digest = sha(ROM.read_bytes())
    assert digest == 'cac800924a1dfb3e2bc6352ef3f47f8f82986229377de20bc5e194046b5a6f45'
    parent = NdsImage.open(ROM)
    arm = parent.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds')
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == digest and len(manifest['batches']) == 470
    save_rows = [read(OUT / 'fixture_manifest.json'), *read(OUT / 'additional_save_copies.json')]
    for row in save_rows:
        assert sha(Path(row['source_save']).read_bytes()) == row['source_save_sha256']
        assert sha(Path(row['test_save']).read_bytes()) == row['test_save_sha256']
    font = GameAsciiFont.from_arm9(arm)
    ending_cases = []
    for captain, label, suffix in [(0, 'rafael', 'rafael'), (1, 'hodram', 'hodram_complete'),
                                    (2, 'lil', 'lil_town'), (3, 'maria', 'maria')]:
        folder = CAPTURES / f'ending_caller_v537_{suffix}'
        report, provenance = captures(folder, digest)
        fixtures = report['synthetic_ending_fixtures']
        assert len(fixtures) == 1 and not report['earned_completion_verified']
        fixture = fixtures[0]
        assert fixture['active_captain_id'] == captain
        raw = (folder / f"frame_{fixture['frame']:06d}_arm9_ram.bin").read_bytes()
        _, replay = request_ending(arm, raw, captain)
        assert replay == {k: v for k, v in fixture.items() if k != 'frame'}
        movie = f'/FLS/M{29 + captain:02d}.fls'
        data = parent.read_file(movie)
        assert data == clean.read_file(movie)
        archive = FlsArchive(data)
        references = {i: quantized(archive.texture(i).render().crop((0, 0, 256, 192))).tobytes()
                      for i in range(1, archive.count)
                      if archive.texture(i).width >= 256 and archive.texture(i).height >= 192}
        matches, prompts = [], []
        for shot in report['frames_captured']:
            if shot['frame'] <= fixture['frame']:
                continue
            image = Image.open(shot['path']).convert('RGB')
            actual = quantized(image.crop((0, 0, 256, 192))).tobytes()
            for index, expected in references.items():
                if actual == expected:
                    matches.append({'frame': shot['frame'], 'texture': index,
                                    'whole_upper_screen_exact_pixels': 49152, 'capture': shot})
            try:
                ink, bounds = complete_mask(font, 'Save the ending data?', image, 16, 296, (0, 8, 0))
            except ValueError:
                continue
            prompts.append({'frame': shot['frame'], 'complete_ink_pixels': ink,
                            'bounds': bounds, 'capture': shot})
        assert matches, f'No original ending image observed for {label}'
        assert prompts, f'No complete ending save prompt observed for {label}'
        ending_cases.append({'captain': label, 'captain_id': captain, 'movie': movie,
                             'movie_sha256': sha(data), 'unchanged_original_movie_bytes': True,
                             'report': provenance, 'fixture': fixture, 'full_source_scene_matches': matches,
                             'distinct_exact_textures': sorted({r['texture'] for r in matches}),
                             'complete_save_prompts': prompts,
                             'all_transitions_or_normal_earned_completion_verified': False})

    folder = CAPTURES / 'original_m28_v537'
    report, provenance = captures(folder, digest)
    assert not report['scripted_input_schedule'] and report['frames'] == 10000
    assert not any(k.startswith('synthetic_') for k in report)
    assert not report.get('battery_save_preloaded')
    archive = FlsArchive(parent.read_file('/FLS/M28.fls'))
    original = FlsArchive(clean.read_file('/FLS/M28.fls'))
    edited = [i for i in range(archive.count) if archive.texture(i).indices != original.texture(i).indices
              or archive.texture(i).palette != original.texture(i).palette]
    assert edited == [4, 5, *range(27, 47)]
    groups = []
    for index in range(27, 47):
        pixels = points(archive.texture(index))
        same = next((g for g in groups if g['pixels'] == pixels), None)
        if same:
            same['textures'].append(index)
        else:
            groups.append({'textures': [index], 'pixels': pixels, 'captures': []})
    groups.sort(key=lambda g: len(g['pixels']))
    captions = [{'texture': i, 'origin': origin, 'pixels': points(archive.texture(i)), 'captures': []}
                for i, origin in [(4, [0, 48]), (5, [0, 82])]]
    order = []
    for shot in report['frames_captured']:
        image = quantized(Image.open(shot['path']).crop((0, 0, 256, 192)))
        for caption in captions:
            if full_match(image, caption['pixels'], caption['origin']):
                caption['captures'].append(shot)
        matched = [n for n, g in enumerate(groups) if full_match(image, g['pixels'], (12, 167))]
        if matched:
            n = max(matched)
            groups[n]['captures'].append(shot)
            if not order or order[-1] != n:
                order.append(n)
    assert order == list(range(19)) * 2, ('Missing original startup visual states', order)
    assert all(c['captures'] for c in captions)
    for group in [*groups, *captions]:
        group['full_ink_and_shadow_pixels'] = len(group.pop('pixels'))
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'ROM_modified': False,
             'original_startup_movie': {'movie': '/FLS/M28.fls', 'report': provenance,
                                        'no_inputs_save_cheats_or_file_substitution': True,
                                        'complete_title_and_gold_logo_planes': captions,
                                        'all19_distinct_progressive_states_in_original_order': groups,
                                        'two_complete_observed_reveal_cycles': True,
                                        'texture30_31_equivalence_not_direct_binding_trace': True},
             'ending_cases': ending_cases, 'all_source_saves_and_test_copy_sources_unchanged': True,
             'synthetic_ending_state_does_not_establish_earned_completion': True,
             'all22_requirements_and18_incomplete_plaques_retained': True,
             'legacy_raw_consumers_restoration_other_contexts_remain_open': True,
             'hardware_device_verification': False, 'full_goal_complete': False}
    assert len(read('translations/graphics_completion_requirements_v313.json')['historical_pending_items_retained']) == 22
    assert all(not r['fully_completed'] for r in read('translations/graphics_completion_campaign_v1.json')
               ['plaque_style_v247']['ongoing_plaque_inventory'])
    (OUT / 'native_movie_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Original startup:22 edited textures/19 reveal states; four original ending callers and exact scenes verified. Earned endings unclaimed.')


if __name__ == '__main__':
    main()
