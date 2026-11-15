"""Archive tested two-record release while retaining every graphics audit gate."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_wedding_dialogue_v678 import BATCH, ROOT
from scripts.record_regional_ui_v616 import checked_copy
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save
from scripts.verify_wedding_dialogue_v678 import ROM

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V678 Wedding dialogue')
DOC = Path('docs/wedding_dialogue_v678_checkpoint.md')
KEY = 'two_canonical_source_Lil_wedding_dialogue_repairs_complete_ROM_and_cold_boot_v678'
SCRIPTS = ('scripts/prepare_wedding_dialogue_v678.py', 'scripts/register_wedding_dialogue_v678.py',
    'scripts/verify_wedding_dialogue_v678.py', 'scripts/run_wedding_dialogue_v678.py',
    'scripts/finish_wedding_dialogue_v678.py', 'scripts/record_wedding_dialogue_v678.py',
    'scripts/verify_wedding_dialogue_archive_v678.py', 'scripts/native_wedding_fixture_v677.py',
    'scripts/observe_wedding_runtime_v676.py', 'scripts/observe_graphic_paints_v669.py',
    'scripts/build_integrated_release.py', 'dk4tool/patch/wedding_dialogue_cleanup.py')


def copy(source, target):
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, target)


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/finish_wedding_dialogue_v678.py').read_bytes())
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert proof['ordinary89_whole_title_selection_story_town_frames_exact_V666']
    assert proof['observer_common_fixture_baseline_whole_screen_pairs'] == 73
    assert proof['wedding_capture_records_per_run'] == 74
    assert proof['cold_boot_verification_pending'] is False
    save(ROOT / 'visual_review.json', {
        'both_QA_previews_individual_changed_runtime_boxes11_transition_and8_ordinary_phases_opened': True,
        'leading_trailing_letters_line_breaks_portraits_and_next_scene_reviewed': True,
        'new_texture_art_or_ROM_edits_after_review': False,
        'review_sheets': {str(path): sha(path.read_bytes()) for path in
            (ROOT / 'actual_dialogue_and_transition_review.png', ROOT / 'ordinary_phase_review.png')},
        'user_acceptance_or_guide_approval': False})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
        'status': 'two_source_faithful_paragraphs_integrated_and_targeted_cold_boot_verified_experimental',
        'canonical_source_natural_v2_allocation_and_speaker09_preserved': True,
        'four_complete_text_holds_first_final_letters_empty_rows_and_original_next_scene_verified': True,
        '73_whole_observer_baseline_pairs89_ordinary_regression_frames_exact': True,
        'only_two_SC2_spans_all_graphics_ARM9_and_other_files_exact_V666': True,
        'clean_patch_reconstruction470_batches114_accepted_layers_and_prior_profiles_preserved': True,
        'isolated_chapter_loader_argument_fixture_not_earned_wedding': True,
        'all18_plaques_incomplete22_historical_scopes_exact_other_gates_open': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    pointer_key = 'latest_compiled_experimental_candidate_with_inherited_native_gap'
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data == pre['all_original_audits_before'][name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        pointer = data[pointer_key]
        assert pointer['candidate'].endswith('all_routes_combined_v666_candidate.nds')
        pointer.update(candidate=str(ROM), sha256=proof['candidate_sha256'], profile='all-routes-unified-v678',
                       two_wedding_dialogue_followups_actual_verified=True)
        save(path, data)
    heading = '## V678: two source-faithful wedding paragraphs and verified combined ROM'
    addition = ('Two clean-Japanese/canonical natural-dialogue-v2 records replace the orphaned '
        'promise ending and false dress reading with natural English. Original speaker09, '
        '64/69-byte allocations, offsets and4906 movie command remain. Only two SC2 spans '
        'differ from V666; all graphics,ARM9,other files,470 batches,114 accepted layers '
        'and older profiles remain. Exact clean patch reconstruction passes. Two16000-frame '
        'wedding cold boots use the disclosed one-byte ARM9 R1 chapter fixture;73 distinct whole '
        'observer/baseline pairs match. Four complete text holds include edge letters and '
        'blank rows;ten full resident chapter snapshots and original14489 M26 request pass. '
        'All89 ordinary title/selection/story/town frames match V666. Both previews and '
        'runtime/transition/ordinary sheets visually reviewed. Latest compiled experimental '
        'pointer advances to V678; canonical/user acceptance unchanged. All18 plaques remain '
        'incomplete and22 original requirements exact; controls,cards,legacy/comics,older '
        'checks and final acceptance remain open. ROM,patch and evidence on E; no fixture '
        'guide promotion. See [V678 checkpoint](wedding_dialogue_v678_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        value = path.read_text(encoding='utf-8')
        assert heading not in value
        path.write_text(value.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    for mode in ('wedding', 'baseline', 'ordinary'):
        folder = CAP / ('wedding_dialogue_v678_' + mode)
        for source in folder.rglob('*'):
            if source.is_file():
                copy(source, ARCHIVE / 'runs' / folder.name / source.relative_to(folder))
    for source in (DOC, BATCH, Path('translations/wedding_dialogue_cleanup_v1.json'),
                   Path('translations/release_stack.json'), ROM.with_suffix('.manifest.json'), *map(Path, SCRIPTS)):
        copy(source, ARCHIVE / 'sources' / source.name)
    for source in ROOT.rglob('*'):
        if source.is_file() and source.suffix.lower() != '.nds':
            copy(source, ARCHIVE / 'analysis' / source.relative_to(ROOT))
    for name in frozen:
        copy(Path('translations') / name, ARCHIVE / 'audits' / name)
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        copy(Path('docs') / name, ARCHIVE / 'docs' / name)
    save(ARCHIVE / 'provenance.json', {
        'candidate': str(ROM.resolve()), 'candidate_sha256': proof['candidate_sha256'],
        'patch': str(ROM.with_suffix('.xdelta').resolve()), 'patch_sha256': proof['patch_sha256'],
        'source_scripts': {p: sha(Path(p).read_bytes()) for p in SCRIPTS},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'all_three_runs_terminal_no_guide_or_canonical_promotion': True, 'full_goal_complete': False})
    print('V678 release/evidence on E; three audits/four documents updated with full graphics scope retained.', flush=True)


if __name__ == '__main__':
    main()
