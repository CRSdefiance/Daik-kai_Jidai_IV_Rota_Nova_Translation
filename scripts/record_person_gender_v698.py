"""Record bounded Sailor Info display coverage without clearing retained gaps."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.run_person_gender_v698 import CAP, ROOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V698 Sailor Info gender exception')
KEY = 'actual_Sailor_Info_Arcadius_both_flag_states42_pairs80_whole_plaque_crops_v698'
DOC = Path('docs/person_gender_v698_checkpoint.md')
SOURCES = ('scripts/run_person_gender_v698.py', 'scripts/replay_person_gender_v698.py',
    'scripts/verify_person_gender_v698.py', 'scripts/record_person_gender_v698.py',
    'scripts/verify_person_gender_archive_v698.py', 'scripts/run_gender_exception_v697.py',
    'scripts/observe_file_requests_v681.py', 'scripts/check_file_requests_v681.py',
    'scripts/replay_room_gender_v694.py', 'scripts/verify_room_gender_v694.py')


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_person_gender_v698.py').read_bytes())
    assert proof['actual_original_Sailor_Info_Arcadius_flag9_exception_both_symbols_verified']
    assert proof['total_whole_RGB_and_capture_RAM_pairs'] == 42
    assert proof['whole_plaque_native5_pixels'] == 55200
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    save(ROOT / 'visual_review.json', {
        'actual_both_flag_states_next_officer_and_return_sheet_opened': proof['review_sheet'],
        'sheet_sha256': proof['review_sheet_sha256'],
        'both_complete_symbols_and_ten_static_plaques_visible_in_sampled_Info_states': True,
        'labelled_symbol_insets_separate_from_uncovered_complete_screens': True,
        'restored_return_retains_Arcadius_portrait_cache_beside_Hodram_name_fixture_artifact': True,
        'no_ordinary_return_profile_or_earned_recruitment_or_guide_claim': True,
        'texture_restoration_all18_plaque_signoffs_and_native_replay_gaps_remain_open': True})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'actual_original_Info_identity8_flag9_both_symbols_and_R_L_return_verified': True,
        'eight_complete_symbols2048_pixels24_negative_controls_pass': True,
        'all42_whole_RGB_capture_RAM_pairs_and_two_terminal_RAM_pairs_exact': True,
        'all80_complete_static_plaque_crops55200_native5_pixels_exact': True,
        'only25_source_predicted_symbol_pixels_change_in_three_held_full_screens': True,
        'only_declared_lookup_and_flag_inputs_changed_and_restored_in_all_four_runs': True,
        'return_portrait_cache_is_fixture_artifact_not_ordinary_profile_credit': True,
        'original_update_prefix_replay_failed_020E31E4_no_equivalence_claim': True,
        'V694_suffix_memory_gap_embedded_consumers_and_broader_graphics_open': True,
        'all18_plaques_incomplete22_historical_requirements_preserved': True,
        'ROM_manifest_patch_registry_donor_canonical_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data == pre['all_original_audits_before'][name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        copy(path, ARCHIVE / 'audits' / name)
    heading = '## V698: Sailor Info story-controlled symbol and complete plaque crops'
    addition = (
        'Previous status-only goal turn made no progress. Four terminal 7800-frame '
        'cold boots verify the separate original Sailor Info parent with disclosed '
        'selected-actor8/flag9 fixtures. Both original getters return 0/512 and '
        'selectors 0/1; eight complete symbol cells2048 native5 pixels and24 '
        'negative controls pass. All42 whole RGB/capture-RAM pairs, two terminal '
        'RAM pairs and declared install/restore memories match. Three Arcadius '
        'holds differ at only25 independently predicted source pixels; next-officer '
        'and restored screens match across flag states. All80 whole static plaque '
        'crops55200 pixels match the current V671-reviewed asset. Actual sheet '
        'opened; restored roster keeps the fixture portrait cached beside the '
        'original name, explicitly not normal profile/guide credit. Full update '
        'prefix replay fails at020E31E4 after actor_ready; no prefix equivalence '
        'or V694 suffix-gap clearance claimed. Earlier navigation/filter/hash/'
        'cross-frame-pointer assumptions retained and corrected. All18 plaques '
        'incomplete,22 historical scopes exact and broader graphics/restoration/'
        'older checks/acceptance remain open. V692 ROM/patch/registry/pointers and '
        'donor unchanged; evidence on E,no commit/push/guide promotion. Full goal '
        'active. See [V698 checkpoint](person_gender_v698_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        content = path.read_text(encoding='utf-8')
        assert heading not in content
        path.write_text(content.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for path in (*map(Path, SOURCES), DOC):
        copy(path, ARCHIVE / 'sources' / path)
    analysis = ROOT.parent.parent
    for path in analysis.rglob('*'):
        if path.is_file():
            copy(path, ARCHIVE / 'analysis' / path.relative_to(analysis))
    external = {}
    for folder in CAP.glob('person_gender_v698_*'):
        for path in folder.rglob('*'):
            if path.is_file():
                external[str(path)] = sha(path.read_bytes())
    save(ARCHIVE / 'provenance.json', {'scripts': {p: sha(Path(p).read_bytes()) for p in SOURCES},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'external_E_drive_evidence': external,
        'earlier_aborted_navigation_and_partial_filter_pilots_retained_not_final_display_credit': True,
        'isolated_UI_fixture_no_earned_story_or_guide_promotion': True, 'full_goal_complete': False})
    print('V698 actual Sailor Info symbols and80 plaque contexts recorded; both native replay gaps remain open.', flush=True)


if __name__ == '__main__':
    main()
