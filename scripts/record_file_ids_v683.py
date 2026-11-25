"""Archive numeric-ID/direct-range evidence and preserve every original audit gate."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.run_village_visits_v664 import CAP
from scripts.trace_file_ids_v683 import ROOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V683 Numeric file IDs')
DOC = Path('docs/file_ids_v683_checkpoint.md')
KEY = 'actual247_numeric_file_IDs8_direct_ranges_DTCM_policy193_baseline_pairs_v683'
SCRIPTS = ('scripts/trace_file_ids_v683.py', 'scripts/verify_file_ids_v683.py',
    'scripts/record_file_ids_v683.py', 'scripts/verify_file_ids_archive_v683.py',
    'scripts/observe_file_requests_v681.py', 'scripts/check_file_requests_v681.py')


def main():
    pp = ROOT / 'proof.json'
    pre, proof = read(ROOT / 'preflight.json'), read(pp)
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_file_ids_v683.py').read_bytes())
    assert proof['producer_sha256'] == sha(Path('scripts/trace_file_ids_v683.py').read_bytes())
    assert proof['all193_whole_screen_pairs_and_two_terminal_RAM_pairs_match_retained_unmodified_baselines']
    assert sum(c['entry_counts']['numeric_ID'] for c in proof['cases']) == 247
    assert sum(c['entry_counts']['direct_range'] for c in proof['cases']) == 8
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'visual_review.json', {'four_actual_current_frames_opened': True,
        'title_opening_initial_logo_and_final_Maria_Gallery_selection_reviewed': True,
        'no_new_defect_identified_in_selected_views': True,
        'Gallery_fixture_access_not_earned_all18_plaques_incomplete_no_guide_promotion': True})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'status': 'numeric_ID_and_range_gaps_typed_for_New_Game_Gallery_other_graphics_contexts_open',
        'two_corrected_terminal_cold_boots193_full_RGB_pairs_and_terminal_RAM_exact_to_retained_baselines': True,
        'all489_callbacks_CPU_WRAM_DTCM_configuration_unchanged_all_slots_restored': True,
        'all234_filename_entries_repeat_V681_and_have_exact_matching_numeric_file_IDs': True,
        'only13_extra_numeric_IDs_are_overlay0_or_sound_data_not_additional_graphics_in_these_sequences': True,
        'all8_direct_ranges_are_complete_ROM_FNT_FAT_or_overlay_tables': True,
        'all714_ROM_FAT_entries_equal_actual_file_bytes_overlay0_identity_bound_to_original_table': True,
        'all8_range_fifth_arguments_FFFFFFFF_from_actual_DTCM_28_DTCM461_main_fiber_stack_entries': True,
        '15_grouped_host_prefix8_mirror10_DTCM_precedence_boundary_controls_pass': True,
        'initial_wrong_DTCM_mapping_and_rejected_all_DTCM_verifier_retained': True,
        'entry_requests_not_successful_returns_global_nonuse_or_new_unknown_scene_credit': True,
        'all18_plaques_incomplete22_original_requirements_exact_other_gates_open': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
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
    heading = '## V683: numeric file IDs, direct byte ranges and actual stack memory'
    addition = ('Two corrected cold boots finish4000/38600 frames and match193 full RGB '
        'two-screen pairs plus both terminal RAM states against pinned retained V681 '
        'unmodified baselines. All489 actual SDK entries preserve CPU/WRAM/DTCM/base. '
        'All234 filename opens have exact matching numeric IDs;the13 extra ID opens '
        'are overlay0 code or sound_data.sdat. All8 direct ranges are exact original '
        'FNT/FAT/overlay tables.15 grouped prefixes,8 mirror and10 DTCM precedence '
        'controls pass. Initial main-RAM-only stack reads were wrong for DTCM;source '
        'and both initial runs retained. Corrected mapping verifies all8 fifth '
        'arguments FFFFFFFF from full actual DTCM. A rejected all-stacks-in-DTCM '
        'verifier is retained:actual entries use28 DTCM and461 main-RAM fiber '
        'stacks. No game bytes changed. This closes an interface question in these '
        'two schedules,not global artwork non-use or actual missing scene contexts. '
        'V678/patch/registry/pointers unchanged;all18 plaques incomplete,22 scopes '
        'exact;controls/cards/comics/legacy/material/older checks/acceptance remain '
        'open. Archive on E,no guide promotion,full goal active. See '
        '[V683 checkpoint](file_ids_v683_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    for case in ('ordinary', 'gallery'):
        folders = (CAP / f'file_ids_v683_{case}', CAP / f'file_ids_v683_v2_{case}',
                   CAP / f'file_requests_v681_{case}_baseline')
        for folder in folders:
            for source in folder.rglob('*'):
                if source.is_file():
                    copy(source, ARCHIVE / 'runs' / folder.name / source.relative_to(folder))
    for source in (DOC, *map(Path, SCRIPTS)):
        copy(source, ARCHIVE / 'sources' / source.name)
    policy = read(ROOT / 'source_contract.json')['ARM9_CPU_read_policy']
    for name in ('MMU_header', 'SFORMAT_source'):
        copy(policy[name], ARCHIVE / 'core_source' / Path(policy[name]).name)
    for source in ROOT.rglob('*'):
        if source.is_file():
            copy(source, ARCHIVE / 'analysis' / source.relative_to(ROOT))
    for name in frozen:
        copy(Path('translations') / name, ARCHIVE / 'audits' / name)
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        copy(Path('docs') / name, ARCHIVE / 'docs' / name)
    save(ARCHIVE / 'provenance.json', {'source_scripts': {p: sha(Path(p).read_bytes()) for p in SCRIPTS},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
            if p.is_file() and p.name != 'provenance.json'}, 'candidate_sha256': pre['candidate_sha256'],
        'bounded_numeric_range_interfaces_not_global_graphics_nonuse': True, 'full_goal_complete': False})
    print('V683 ID/range/DTCM evidence archived; six terminal runs include two retained baselines.', flush=True)


if __name__ == '__main__':
    main()
