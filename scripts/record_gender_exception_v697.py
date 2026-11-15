"""Record actual original exception coverage and preserve the broader audit."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.run_gender_exception_v697 import CAP, ROOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V697 Arcadius gender exception')
KEY = 'actual_Arcadius_identity8_flag9_both_symbols54_full_pairs14_native_construction_states_v697'
DOC = Path('docs/gender_exception_v697_checkpoint.md')
SOURCES = ('scripts/run_gender_exception_v697.py', 'scripts/replay_gender_exception_v697.py',
    'scripts/verify_gender_exception_v697.py', 'scripts/record_gender_exception_v697.py',
    'scripts/verify_gender_exception_archive_v697.py', 'scripts/observe_file_requests_v681.py',
    'scripts/check_file_requests_v681.py', 'scripts/replay_room_gender_v694.py',
    'scripts/verify_room_gender_v694.py', 'scripts/run_room_gender_v694.py',
    'scripts/inspect_committed_gpu_v646.py')


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_gender_exception_v697.py').read_bytes())
    assert proof['actual_Arcadius_identity8_story_flag9_exception_in_second_room_parent_verified']
    assert proof['total_whole_RGB_and_capture_RAM_pairs'] == 54
    assert proof['complete_actual_native5_symbol_pixels'] == 2048
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    save(ROOT / 'visual_review.json', {'actual_both_flag_states_and_restored_Deck_screens_opened': proof['review_sheet'],
        'sheet_sha256': proof['review_sheet_sha256'],
        'both_complete_gender_symbols_inside_boxes_original_profile_and_return_visible': True,
        'magnified_crops_separately_labelled_below_uncovered_whole_screens': True,
        'isolated_actor_lookup_flag_fixture_not_earned_recruitment_or_story_no_guide_promotion': True,
        'full_info_suffix_and_other_consumers_not_cleared': True})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'specific_V694_identity8_story_flag9_gap_closed_for_second_room_parent': True,
        'actual_raw1_identity8_flag_returns0_512_processed_selectors0_1_verified': True,
        'eight_complete_symbol_cells2048_native5_pixels_and24_negative_controls_pass': True,
        'all54_whole_RGB_capture_RAM_pairs_and_both_terminal_RAM_pairs_exact': True,
        'all4_hold_full_screens_change_at_exact25_independently_source_predicted_symbol_pixels': True,
        'all4_runs_only_declared_lookup_word_flag_bit_writes_restore_before_exit': True,
        'both_original_construction_prefixes14_R0_R14_CPSR_and_whole_RAM_DTCM_ITCM_states_exact': True,
        'V694_full_suffix_memory_gap_embedded_copy_and_other_contexts_remain_open': True,
        'all18_plaques_incomplete22_historical_scopes_and_broader_goal_open_or_exact': True,
        'ROM_manifest_patch_registry_original_donor_canonical_and_release_pointers_unchanged': True,
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
    heading = "## V697: Arcadius's original story-controlled gender symbol"
    addition = (
        'Four10800-frame cold boots use guarded isolated selected-actor8/flag9 inputs in '
        'the real Deck room. Only one roster lookup word and one story bit change;full '
        'before/after RAM and CPU/TCM guards prove install/restore,with original donor exact. '
        'The original getter returns0/512;raw gender1/identity8 produce displayed male0/'
        'female1. Eight full symbol cells2048 native5 pixels pass all edges and24 negatives. '
        'All54 observed/minimal-fixture whole RGB and capture-RAM pairs,two terminal RAM '
        'pairs and restore states match. All four held cross-state screens differ at exactly '
        '25 independently source-predicted symbol pixels;21 pre-fixture and two return '
        'screens are whole-RGB exact. Original full selection-to-gender construction '
        'prefixes match14 R0-R14/CPSR/full RAM/DTCM/ITCM checkpoints without native bridges. '
        'Actual sheet reviewed;no earned recruitment/reveal or guide claim. This closes '
        'the specific second-parent exception gap,not V694 full-suffix memory differences '
        'or embedded/other consumers. All18 plaques incomplete,22 historical scopes exact '
        'and broader graphics/older checks/acceptance remain open. V692/patch/registry/'
        'pointers unchanged;evidence on E,no commit or push. Full goal active. See '
        '[V697 checkpoint](gender_exception_v697_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        content = path.read_text(encoding='utf-8')
        assert heading not in content
        path.write_text(content.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for path in (*map(Path, SOURCES), DOC):
        copy(path, ARCHIVE / 'sources' / path)
    for path in ROOT.rglob('*'):
        if path.is_file():
            copy(path, ARCHIVE / 'analysis' / path.relative_to(ROOT))
    external = {}
    for folder in CAP.glob('gender_exception_v697_*'):
        for path in folder.rglob('*'):
            if path.is_file():
                external[str(path)] = sha(path.read_bytes())
    source = read(ROOT / 'native_input_controls.json')
    external[source['source_RAM']] = source['source_RAM_sha256']
    save(ARCHIVE / 'provenance.json', {'scripts': {p: sha(Path(p).read_bytes()) for p in SOURCES},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'external_E_drive_evidence': external,
        'isolated_UI_fixtures_not_earned_progress_no_guide_promotion': True, 'full_goal_complete': False})
    print('V697 Arcadius original exception, bounded fixtures, complete current symbols and unchanged audit scope recorded on E.', flush=True)


if __name__ == '__main__':
    main()
