"""Archive the declared live input control without broadening its display scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.trace_chooser_raw_independence_v690 import CAP, ROOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V690 Chooser raw independence')
DOC = Path('docs/chooser_raw_independence_v690_checkpoint.md')
KEY = 'actual_full_chooser_initialization_return_and_declared_final_raw_fixture21_whole_pairs_v690'
SCRIPTS = tuple('scripts/' + p for p in (
    'trace_chooser_raw_independence_v690.py', 'verify_chooser_raw_independence_v690.py',
    'record_chooser_raw_independence_v690.py', 'verify_chooser_raw_independence_archive_v690.py',
    'replay_raw_portrait_tail_v689.py', 'observe_file_requests_v681.py',
    'check_file_requests_v681.py'))


def main():
    pre, proof = read(ROOT / 'preflight.json'), read(ROOT / 'proof.json')
    pp = ROOT / 'proof.json'
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_chooser_raw_independence_v690.py').read_bytes())
    assert proof['producer_sha256'] == sha(Path(SCRIPTS[0]).read_bytes())
    assert proof['both873_instruction_original_initialization_remainders_no_raw_reads_or_writes']
    assert proof['two_terminal4000_frame_cold_boots21_whole_fixture_control_pairs21_retained_baseline_pairs_exact']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'visual_review.json', {
        'opened_actual_control_and_declared_fixture_comparison': proof['review_sheet'],
        'sheet_sha256': proof['review_sheet_sha256'],
        'title_Rafael_biography_and_confirmation_reviewed_no_new_visible_difference': True,
        'fixture_screens_not_guide_candidates': True,
        'sampled_frames_not_all_frames_or_all_captain_contexts': True})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'two_terminal4000_frame_cold_boots20_preserving_or_declared_fixture_callbacks': True,
        'both873_original_instruction_remaining_initializations_match_actual_return_CPU_CPSR_RAM_DTCM': True,
        'exact_single14144_byte_raw17_input_replacement_declared_not_production_art_change': True,
        '21_complete_fixture_control_pairs21_retained_baseline_pairs_terminal_RAM_exact': True,
        'actual_raw_buffer_not_read_by_remaining_initializer_first_sampled_Rafael_displays_independent': True,
        'not_all_intermediate_frames_all_captains_other_readers_or_global_nonuse': True,
        'all18_plaques_incomplete22_requirements_exact_broader_graphics_gates_open': True,
        'ROM_manifest_patch_registry_canonical_release_pointers_unchanged': True,
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
    heading = '## V690: complete chooser initialization return and live raw-input control'
    addition = (
        'Two4000-frame V685 cold boots observe the actual initialization return. '
        'One isolated test replaces only the guarded final14144-byte raw17 buffer; '
        'its fixture is declared and its full before/after memory retained. '
        'Both873-instruction original initialization remainders reproduce actual '
        'return registers,CPSR,saved registers,stack,all RAM and DTCM exactly '
        'without raw-buffer accesses or native bridges.21 whole case pairs and21 '
        'retained baseline pairs match;complete terminal RAM is identical. '
        'This verifies sampled initial Rafael screens,not every intermediate '
        'frame,captain update,other raw consumer or global nonuse. All-captain '
        'selection updates remain a useful distinct follow-up. No production '
        'ROM/patch/registry/pointer changes;all18 plaques incomplete,22 historical '
        'scopes exact and broader graphics remain open. Evidence on E,fixture '
        'screens not guide candidates. See '
        '[V690 checkpoint](chooser_raw_independence_v690_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for p in (DOC, *map(Path, SCRIPTS)):
        copy(p, ARCHIVE / 'sources' / p.name)
    for p in ROOT.rglob('*'):
        if p.is_file():
            copy(p, ARCHIVE / 'analysis' / p.relative_to(ROOT))
    for case in ('control', 'poison'):
        folder = CAP / ('chooser_raw_independence_v690_' + case)
        for p in folder.rglob('*'):
            if p.is_file():
                copy(p, ARCHIVE / 'runs' / case / p.relative_to(folder))
    baseline = Path(pre['baseline_report'])
    for p in baseline.parent.rglob('*'):
        if p.is_file():
            copy(p, ARCHIVE / 'retained_V689_baseline' / p.relative_to(baseline.parent))
    save(ARCHIVE / 'provenance.json', {
        'scripts': {p: sha(Path(p).read_bytes()) for p in SCRIPTS},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'fixture_screens_not_guide_candidates': True, 'full_goal_complete': False})
    print('V690 complete initialization and explicitly declared raw-buffer control archived on E.', flush=True)


if __name__ == '__main__':
    main()
