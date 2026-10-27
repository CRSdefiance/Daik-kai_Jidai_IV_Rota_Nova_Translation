"""Archive the actual all-village evidence while retaining every historical gate."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.run_village_visits_v664 import ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/village_visits_v664_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V664 Village visits')
KEY = 'all24_actual_village_arrivals_docking97_menu_labels_and_chief_requests_with_original_Ezo_story_control_v664'


def copy(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, destination)


def main():
    proof_path = ROOT / 'proof.json'
    proof, pre = read(proof_path), read(ROOT / 'preflight.json')
    assert len(proof['reports']) == 29
    assert len(proof['all24_complete_source_name_arrival_fields']) == 24
    assert proof['complete_initial_menu_and_chief_request_villages'] == list(range(24))
    assert sum(len(c['initial_menu']['complete_menu_labels'])
               for c in proof['all24_complete_source_name_arrival_fields']) == 97
    assert sum(len(c['discovery']['complete_name_first_final_letter_deletion_controls'])
               for c in proof['all24_complete_source_name_arrival_fields']) == 48
    assert len(proof['original_Japanese_Ezo_same_fixture_control']['original_upper_screen_comparisons']) == 12
    for path, digest in proof['scripts'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scopes in frozen.items():
        data, before = read(Path('translations') / name), pre['all_original_audits_before'][name]
        assert set(data) <= set(before) | {KEY, 'current_goal_turn_classification'}
        assert all(data[k] == v for k, v in before.items() if k not in (KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scopes['historical_pending_items_retained']
        inventory = data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory')
        assert inventory == scopes['ongoing_plaque_inventory']
        if inventory is not None:
            assert len(inventory) == 18 and all(x['fully_completed'] is False for x in inventory)
    for path in (DOC, Path(__file__), *(Path(p) for p in proof['scripts'])):
        copy(path, ARCHIVE / 'Reproduction' / path.name)
    for path in ROOT.rglob('*'):
        if path.is_file():
            copy(path, ARCHIVE / 'Analysis' / path.relative_to(ROOT))
    captures = []
    for label, info in proof['reports'].items():
        report_path = Path(info['path'])
        assert sha(report_path.read_bytes()) == info['sha256']
        report = read(report_path)
        for path in report_path.parent.rglob('*'):
            if path.is_file():
                copy(path, ARCHIVE / label / path.relative_to(report_path.parent))
        for shot in report['frames_captured']:
            captures.append({'run': label, 'frame': shot['frame'], 'source': shot['path'],
                'PNG_sha256': shot['PNG_sha256'], 'coordinate_fixtures': len(report['synthetic_location_fixtures']),
                'original_Japanese_control': label == 'Ezo_Japanese_control',
                'unmodified_original_capture': True, 'normal_long_distance_travel_verified': False,
                'publication_approved': False})
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'all24_actual_complete_arrival_names_paired_docking_frames_initial_menus_and_chief_requests': True,
        'all97_complete_menu_labels_follow_original24_native_modulo_filters': True,
        'all24_actual_name_models_discovery_bit_masks_and_undeveloped_final_states': True,
        'complete224x48_dialogue_and96x120_menu_foreground_fields_blank_cells_and48_name_edge_negatives': True,
        'all_location_fixtures_replayed_only8_ship_coordinate_bytes_no_story_scene_or_resource_flags': True,
        'first_Ezo_approach_miss_retained_second_approach_and_original_story_then_menu_verified': True,
        'original_Japanese_same_fixture12_whole_black_upper_screens589824_pixels_match_current': True,
        'sampled_eight_white_card_file_absence_not_global_unused_proof_or_complete_development_coverage': True,
        'all_eight_white_card_ordinary_display_contexts_and_other_graphics_gates_remain_open': True,
        'all18_original_plaques_incomplete22_historical_scopes_exact': True,
        'ROM_patch_manifest_registry_canonical_and_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'guide_candidates': [], 'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        data = read(path)
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        before = pre['all_original_audits_before'][name]
        assert set(data) == set(before) | {KEY, 'current_goal_turn_classification'}
        assert all(data[k] == v for k, v in before.items() if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V664: all 24 initial village menus and original Ezo story context'
    text = ('All 24 complete arrival names, paired docking-prompt frames, 97 menu labels and chief requests pass '
        'independent whole-field font checks, including 48 actual first/final name-letter deletion controls. '
        'Original village getters, discovery bit masks and undeveloped final town states bind every location. '
        'Fixtures change only eight ship coordinate bytes; no story, scene, menu, development or resource flags '
        'are injected. Ezo\'s missed first approach is retained; a second approach triggers its original villager '
        'story before the real five-row menu and chief request. Twelve whole upper screens match the original '
        'Japanese control, including its black upper screen. No new ROM defect is established. Eight white '
        'village-card ordinary triggers remain open; sampled file absence is not global non-use. Evidence '
        'and derived comparison sheets are on E, with no guide promotion. V653/patch/registry/pointers unchanged; '
        'all18 plaques incomplete and22 historical scopes exact. Full goal remains active. See '
        '[V664 checkpoint](village_visits_v664_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        before = path.read_text(encoding='utf-8')
        if heading not in before:
            path.write_text(before.rstrip() + '\n\n' + heading + '\n\n' + text, encoding='utf-8')
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'captures': captures, 'guide_candidates': [],
        'scripts': {str(p): sha(Path(p).read_bytes()) for p in [str(Path(__file__)), *proof['scripts']]},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}, 'full_goal_complete': False})
    print(f'V664 archived {len(captures)} capture records from29 terminal runs;24 complete village branches; full goal active.')


if __name__ == '__main__':
    main()
