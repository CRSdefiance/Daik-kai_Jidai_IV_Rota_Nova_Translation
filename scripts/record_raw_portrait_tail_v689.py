"""Archive actual chooser evidence and preserve all original graphics scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.trace_raw_portrait_tail_v689 import FOLDER, ROOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V689 Raw portrait tails')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V685 New Game')
DOC = Path('docs/raw_portrait_tail_v689_checkpoint.md')
KEY = 'actual_four_raw_portrait_reads_unconsumed_native_tails_four_PXL_views21_baseline_pairs_v689'
SCRIPTS = tuple('scripts/' + p for p in (
    'trace_raw_portrait_tail_v689.py', 'replay_raw_portrait_tail_v689.py',
    'verify_raw_portrait_tail_v689.py', 'record_raw_portrait_tail_v689.py',
    'verify_raw_portrait_tail_archive_v689.py'))


def main():
    pre = read(ROOT / 'preflight.json')
    pp = ROOT / 'proof.json'
    proof = read(pp)
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_raw_portrait_tail_v689.py').read_bytes())
    assert proof['producer_sha256'] == pre['producer_sha256']
    assert proof['replay_sha256'] == sha(Path('scripts/replay_raw_portrait_tail_v689.py').read_bytes())
    assert proof['21_complete_current_baseline_two_screen_pairs_and_retained_terminal_RAM_exact']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'visual_review.json', {
        'opened_actual_title_biography_and_confirmation_sheet': proof['review_sheet'],
        'sheet_sha256': proof['review_sheet_sha256'],
        'no_new_visual_defect_identified_in_these_selected_ordinary_frames': True,
        'no_raw_portrait_or_comic_display_credit_from_PXL_views': True,
        'three_unmodified_ordinary_screenshots_saved_as_guide_candidates_not_publication_approved': True})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'one_actual4000_frame_cold_boot_no_save_or_live_fixture9_preserving_callbacks': True,
        'all_four14144_byte_source_payloads_loaded_and_native_following_CPU_CPSR_RAM_DTCM_exact': True,
        'four_tail_segments_no_raw_buffer_reads_build_separate_personbustup_PXL_views': True,
        'four_counterfactual_payload_controls_and_positive_native_read_detector_pass': True,
        '21_complete_current_RGB_baseline_pairs_and_retained_version_bound_terminal_RAM_exact': True,
        'last17_after_loop_and_other_readers_not_globally_excluded_raw_display_still_open': True,
        'Sea_cow_wordplay_review_revalidated_existing_decision_no_translation_change': True,
        'all18_plaques_incomplete22_original_requirements_exact_other_graphics_open': True,
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
    heading = '## V689: actual raw portrait reads and unconsumed chooser tails'
    addition = (
        'A fresh ordinary4000-frame V685 cold boot records four actual raw '
        'SLACK14–17 reads/returns and the loop boundary with9 preserving callbacks. '
        'All56576 source bytes match. Four original-native tails reproduce every '
        'next register,CPSR,4MiB RAM and16KiB DTCM exactly,with zero raw-buffer '
        'reads/writes. Four isolated payload replacements leave only their '
        'explicit14144-byte input region changed. Native read calibration passes. '
        'Actual constructed views bind personbustup00–03.PXL,not the raw payloads. '
        '21 whole current baseline pairs and version-bound retained terminal RAM '
        'match. This resolves the loop association,not later block17 use,global '
        'nonuse or raw-art display. Sea cow remains the documented bullfighter '
        'comic adaptation after context review. Three ordinary guide-candidate '
        'screens saved on E,no publication approval. ROM/patch/registry/pointers '
        'unchanged;all18 plaques incomplete,22 original scopes exact and broader '
        'graphics remain open. See '
        '[V689 checkpoint](raw_portrait_tail_v689_checkpoint.md).\n')
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
    for p in FOLDER.rglob('*'):
        if p.is_file():
            copy(p, ARCHIVE / 'run' / p.relative_to(FOLDER))
    baseline = read(pre['baseline_report'])
    copy(pre['baseline_report'], ARCHIVE / 'retained_baseline/capture_report.json')
    for s in baseline['frames_captured']:
        if s['frame'] in pre['capture_frames']:
            copy(s['path'], ARCHIVE / 'retained_baseline' / Path(s['path']).name)
    old = Path(pre['older_4000_frame_baseline'])
    copy(old, ARCHIVE / 'retained_terminal/capture_report.json')
    copy(old.parent / 'final_arm9_ram.bin', ARCHIVE / 'retained_terminal/final_arm9_ram.bin')
    source = read(ROOT / 'source_contract.json')['CPSR_source']
    copy(source, ARCHIVE / 'core_source' / Path(source).name)
    report = read(FOLDER / 'capture_report.json')
    shots = {s['frame']: s for s in report['frames_captured']}
    guide_files = {}
    for frame, label in ((1200, 'Title'), (1500, 'Captain biography'), (2000, 'Name confirmation')):
        p = Path(shots[frame]['path'])
        target = GUIDE / f'V685 {label}.png'
        copy(p, target)
        guide_files[str(target)] = sha(p.read_bytes())
    copy(FOLDER / 'capture_report.json', GUIDE / 'capture_report.json')
    copy(ROOT / 'inputs.json', GUIDE / 'inputs.json')
    save(GUIDE / 'provenance.json', {'candidate_sha256': pre['candidate_sha256'],
        'unmodified_ordinary_screenshots': guide_files, 'no_save_savestate_or_live_fixture': True,
        'publication_approved': False, 'source_report_sha256': sha((FOLDER / 'capture_report.json').read_bytes())})
    save(ARCHIVE / 'provenance.json', {
        'scripts': {p: sha(Path(p).read_bytes()) for p in SCRIPTS},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'guide_files': guide_files, 'full_goal_complete': False})
    print('V689 actual/raw-tail evidence and three ordinary guide candidates archived on E.', flush=True)


if __name__ == '__main__':
    main()
