"""Record the three source waits without changing artwork or release pointers."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.run_opening_holds_v686 import CAP, ROOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V686 Original scene waits')
DOC = Path('docs/opening_holds_v686_checkpoint.md')
KEY = 'three_Maria_blank_holds_actual_source_modal_entries_returns_and24_whole_baseline_pairs_v686'
SCRIPTS = tuple('scripts/' + name for name in (
    'run_opening_holds_v686.py', 'verify_opening_holds_v686.py',
    'prepare_wait_entries_v686.py', 'observe_wait_entries_v686.py',
    'run_wait_entries_v686.py', 'verify_actual_waits_v686.py',
    'record_opening_holds_v686.py', 'verify_opening_holds_archive_v686.py',
    'observe_file_requests_v681.py', 'check_file_requests_v681.py'))


def main():
    pre = read(ROOT / 'preflight.json')
    pp, ap = ROOT / 'proof.json', ROOT / 'actual_wait_proof.json'
    component, actual = read(pp), read(ap)
    assert component['verifier_sha256'] == sha(Path('scripts/verify_opening_holds_v686.py').read_bytes())
    assert actual['verifier_sha256'] == sha(Path('scripts/verify_actual_waits_v686.py').read_bytes())
    assert actual['component_and_photo_proof_sha256'] == sha(pp.read_bytes())
    assert actual['all_three_source_and_current_blank_captures_inside_actual_original_zero_argument_modal_calls']
    assert actual['24_whole_screen_baseline_pairs_two_terminal_RAM_pairs_and_ten_native_prefix_controls_pass']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'visual_review.json', {
        'opened_script_position_matched_original_waits_sheet': component['review_sheet'],
        'sheet_sha256': component['review_sheet_sha256'],
        'all_three_source_current_blank_holds_and_continuation_controls_reviewed': True,
        'third_source_control_is_later_join_not_immediate_next_sentence': True,
        'A_indicator_differences_retained_not_whole_region_equivalence': True,
        'all18_plaques_incomplete_no_guide_promotion': True})
    entry = {
        'documentation': str(DOC), 'component_proof': str(pp),
        'component_proof_sha256': sha(pp.read_bytes()), 'actual_proof': str(ap),
        'actual_proof_sha256': sha(ap.read_bytes()), 'candidate': pre['candidate'],
        'candidate_sha256': pre['candidate_sha256'],
        'three_specific_blank_holds_are_original2000_zero_argument_waits_not_English_padding': True,
        'all_six_blank_captures_inside_actual_unbridged_modal_entry_return_intervals': True,
        '99_callbacks12_selected87_other_all_CPU_RAM_DTCM_unchanged_slots_restored': True,
        '24_complete_two_screen_baseline_pairs_and_two_terminal_RAM_pairs_exact': True,
        'source22000_matches_current21400_by_actual_script_position_not_arbitrary_lag': True,
        'A_indicator208_RGB_differences_retained_no_whole_region_or_phase_credit': True,
        'initial_eight_frame_return_assumption_rejected_failure_retained': True,
        'system_unlock_donor_not_earned_access_no_live_gameplay_fixture': True,
        'previous_status_only_goal_turn_classification': 'no progress',
        'all18_plaques_incomplete22_original_requirements_exact_other_gates_open': True,
        'ROM_patch_registry_canonical_release_pointers_unchanged': True,
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
    heading = '## V686: three Maria blank holds are original script waits'
    addition = (
        'Original Japanese and V685 opcode2000 at chapter33 offsets32/120/1708 '
        'calls02054E44(0,0). Actual read-only entry/return traces bracket all six '
        'selected blank captures;99 callbacks preserve CPU/WRAM/DTCM and restore '
        'host slots.24 complete two-screen baseline pairs and two terminal RAM '
        'pairs match. Source22000/current21400 match by VM position; same-time '
        '21400 is different dialogue.208 A-indicator RGB differences remain '
        'disclosed without whole-region or native-phase credit. The rejected '
        'eight-frame return assertion is retained; actual returns follow the '
        'first A by14–16 frames before any subsequent input. Three specific '
        'waits are resolved, not all blank pages or the full route. Existing '
        'system-unlock donor is disclosed. Previous status turn:no progress; '
        'this evidence checkpoint:progress. V685/patch/registry/pointers unchanged; '
        'all18 plaques incomplete,22 historical scopes exact and broader graphics '
        'remain open. Evidence on E,no guide promotion. See '
        '[V686 checkpoint](opening_holds_v686_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for folder_name in ('opening_holds_v686_source', 'opening_wait_entries_v686_source',
                        'opening_wait_entries_v686_current', 'story_percent_v685_maria',
                        'story_percent_v685_baseline'):
        folder = CAP / folder_name
        for source in folder.rglob('*'):
            if source.is_file():
                copy(source, ARCHIVE / 'runs' / folder.name / source.relative_to(folder))
    for source in (DOC, Path(pre['inputs']), *map(Path, SCRIPTS)):
        copy(source, ARCHIVE / 'sources' / source.name)
    for source in ROOT.rglob('*'):
        if source.is_file():
            copy(source, ARCHIVE / 'analysis' / source.relative_to(ROOT))
    for name in frozen:
        copy(Path('translations') / name, ARCHIVE / 'audits' / name)
    save(ARCHIVE / 'provenance.json', {
        'source_scripts': {p: sha(Path(p).read_bytes()) for p in SCRIPTS},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'candidate_sha256': pre['candidate_sha256'], 'full_goal_complete': False})
    print('V686 source wait evidence recorded and archived; ROM and original audit scopes unchanged.', flush=True)


if __name__ == '__main__':
    main()
