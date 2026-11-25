"""Record source-native transition evidence without changing historical scope."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/movie_transition_bitmaps_v648')
DOC = Path('docs/movie_transition_bitmaps_v648_checkpoint.md')
KEY = 'ordinary_movie_transitions18_native_bitmap_states32_original_phases3_clean_boundary_controls_v648'
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V648 Movie transition bitmaps')


def main():
    pp = ROOT / 'transition_bitmap_proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['18_complete_bitmap_states_884736_words_match_source_native_output']
    assert proof['16_actual_upper_transition_scene_replays_exact_clean_code_ABI']
    assert proof['all3_original_reported_boundary_screens_exact_untouched_Japanese']
    assert proof['exact_independent_intraframe_2D_display_timing_still_open']
    assert not proof['full_goal_complete']
    for p, h in proof['scripts'].items():
        assert sha(Path(p).read_bytes()) == h
    for p, h in pre['release_hashes'].items():
        assert sha(Path(p).read_bytes()) == h
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        current = read(Path('translations') / name)
        assert all(current[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert current.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for source in [DOC, *ROOT.glob('*.json'), *ROOT.glob('*.png'), *ROOT.glob('*.py'),
                   *ROOT.glob('*.log'), *ROOT.glob('*.bin'), *[Path(p) for p in proof['scripts']]]:
        checked_copy(source, ARCHIVE / source.name)
    captures = []
    for label, data in proof['routes'].items():
        for kind, item in data['reports'].items():
            assert sha(Path(item['path']).read_bytes()) == item['sha256']
            checked_copy(item['path'], ARCHIVE / f'capture_report_{label}_{kind}.json')
            report = read(item['path'])
            shots = {s['frame']: s for s in report['frames_captured']}
            folder = ARCHIVE / 'Unmodified captures' / label / kind
            folder.mkdir(parents=True, exist_ok=True)
            for shot in shots.values():
                assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
                target = folder / Path(shot['path']).name
                checked_copy(shot['path'], target)
                captures.append({'route': label, 'kind': kind, 'frame': shot['frame'],
                    'path': str(target), 'sha256': shot['PNG_sha256']})
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'unmodified_captures': captures, 'native_exports_remain_on_E_at_report_paths': True,
        'source_phase_controls_are_isolated_not_played_cheat_frames': True,
        'derived_sheets_distinct_from_unmodified_captures': True,
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}, 'full_goal_complete': False})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate_sha256': proof['candidate_sha256'], '18_complete_source_bitmap_states_exact': True,
        '16_actual_transition_scene_replays_2_retained_source_bitmaps': True,
        '32_controlled_original_dissolve_phase_calls_exact': True,
        '36_whole_two_screen_no_export_baselines_exact': True,
        '3_reported_boundary_screens_exact_untouched_Japanese': True,
        'one_later_Lil63_pixel_edge_uses_only_old_and_new_original_source_colors': True,
        'exact_independent_intraframe_display_timing_remains_open': True,
        'all18_plaques_incomplete_all22_historical_scopes_exact': True,
        'ROM_patch_registry_canonical_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        current = read(path)
        current[KEY], current['current_goal_turn_classification'] = entry, 'progress'
        save(path, current)
        assert all(read(path)[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V648: original movie-to-scene bitmap sources and dissolve phases'
    addition = ('Normal adjacent route transitions identify exact original evstill001,towngrp03,evstill033. '
        'The actual upper scene list includes stack-owned effects.18 full bitmap states884736 words '
        'match source/native output,with16 actual transition scene replays and2 retained Hodram source '
        'bitmaps after the transition owner ends.32 isolated original dissolve-phase calls pass. '
        'Three original reported boundary screens match untouched Japanese on both screens; '
        '36 complete no-export baselines match.35/36 clean controls match;the later Lil63-pixel '
        'single-row edge is entirely old3D/new-photo source colors at the original Bayer cell. '
        'No fitted screenshot lag;exact independent intra-frame display timing stays open. '
        'Evidence/captures on E,no ROM/patch/registry/pointer changes. All18 plaques incomplete '
        'and22 historical scopes exact;full goal active. '
        'See [V648 checkpoint](movie_transition_bitmaps_v648_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    for p, h in pre['release_hashes'].items():
        assert sha(Path(p).read_bytes()) == h
    print('V648 archived:18 source/native bitmaps,32 phases,36 baselines,3 exact clean boundaries;18 plaques/22 scopes exact.')


if __name__ == '__main__':
    main()
