"""Record the shared filter repair without closing the remaining graphics scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.run_navigator_filter_v692 import CAP, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V692 Navigator Captain filter')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V692 UI and opening')
DOC = Path('docs/navigator_filter_v692_checkpoint.md')
KEY = 'actual_navigator_Captain_filter_source_slot14_complete_rows89_ordinary_pairs_v692'
POINTER = 'latest_compiled_experimental_candidate_with_inherited_native_gap'
SOURCES = ('dk4tool/patch/navigator_captain_filter.py', 'scripts/build_integrated_release.py',
    'scripts/trace_deck_gender_v692.py', 'scripts/register_navigator_filter_v692.py',
    'scripts/run_navigator_filter_v692.py', 'scripts/run_filter_choices_v692.py',
    'scripts/verify_navigator_filter_v692.py', 'scripts/finish_navigator_filter_v692.py',
    'scripts/record_navigator_filter_v692.py', 'scripts/verify_navigator_filter_archive_v692.py',
    'scripts/headless_desmume_v193.py', 'scripts/observe_file_requests_v681.py',
    'scripts/check_file_requests_v681.py', 'AGENTS.md', 'docs/build_continuity_protocol.md')


def main():
    proof, static = read(ROOT / 'proof.json'), read(ROOT / 'static_release_proof.json')
    pre = read(ROOT / 'build_preflight.json')
    assert proof['candidate_sha256'] == static['candidate_sha256'] == sha(ROM.read_bytes())
    assert proof['verifier_sha256'] == sha(Path('scripts/finish_navigator_filter_v692.py').read_bytes())
    assert len(proof['all14_complete_Captain_rows_both_saved_routes']) == 14
    assert proof['ordinary_full_RGB_baseline_pairs'] == 89
    assert static['registry_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    save(ROOT / 'visual_review.json', {'actual_before_after_Maria_and_return_cycle_sheet_opened': proof['review_sheet'],
        'sheet_sha256': proof['review_sheet_sha256'], 'complete_Captain_no_Japanese_residue_or_new_caption_clipping': True,
        'representative_ordinary_selection_story_market_frames_opened': [1600, 9000, 24100],
        'two_original_cursor_appearances_retained_same_frame_timing_not_cleared': True,
        'gender_second_parent_all18_plaques_and_broader_graphics_goal_remain_open': True})
    entry = {'documentation': str(DOC), 'proof': str(ROOT / 'proof.json'),
        'proof_sha256': sha((ROOT / 'proof.json').read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': static['candidate_sha256'],
        'original_shared_Japanese_Captain_caption_repaired_in_original8_byte_slot': True,
        'all14_complete_rows_first_final_letters_blank_cells_and_original_popup_preserved': True,
        'actual_Hodram_Maria_normal_input_return_cycle_89_ordinary_whole_pairs_and_RAM_verified': True,
        'two_distinct_original_cursor_appearances_not_same_frame_phase_proof_menu147_RAM_differences_retained': True,
        'all470_batches114_accepted_layers675_whole_graphics_and_other_components_retained': True,
        'exact_clean_patch_reconstruction_and_final_source_material_contracts_pass': True,
        'initial_observer_bypass_failure_and_popup_reset_schedule_assumption_retained': True,
        'actual_second_gender_consumer_embedded_copy_and_other_contexts_still_open': True,
        'all18_plaques_incomplete22_original_requirements_exact': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data == pre['all_original_audits_before'][name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        latest = dict(data[POINTER])
        latest.update(candidate=str(ROM), sha256=static['candidate_sha256'], profile=pre['profile'])
        data[POINTER], data[KEY], data['current_goal_turn_classification'] = latest, entry, 'progress'
        save(path, data)
        copy(path, ARCHIVE / 'audits' / name)
    heading = '## V692: shared Captain filter caption and retained gender-context gap'
    addition = (
        'Actual Deck navigator Sort/Filter revealed untranslated 艦長 between '
        'Unassigned and All. Captain fills the original eight-byte source slot '
        '(seven changed bytes); pointers/code/geometry/gameplay stay exact. '
        'Full registered V692 preserves470 batches,114 accepted layers,675 '
        'whole graphics files and every other component/ARM9 byte;clean patch '
        'reconstruction and final material/story contracts pass. Three final '
        '15200-frame saved-game runs verify14 complete caption rows across '
        'Hodram/Maria and the normal choice/return cycle. Unchanged outer labels '
        'independently determine Captain placement;all blank cells and first/final '
        'letters pass. Two cursor appearances differ from same-frame source '
        '(87/1446 non-caption pixels),each matching retained original appearances; '
        'same-frame timing and147 menu-terminal RAM differences are explicitly '
        'retained,not waived as full equality. Ordinary24100-frame New Game '
        'matches89 whole V685 captures and full RAM after only the caption-slot '
        'replacement. Twelve exploratory runs did not capture the second gender '
        'helper;an original return bypass exposed an observer assumption. Failed '
        'observer/static/live verifier and initial popup-reset schedule evidence '
        'is retained. Second gender/embedded,controls,cards,comics/legacy/material '
        'review,older record checks and final acceptance remain open. All18 '
        'plaques incomplete and22 original requirements exact. Experimental '
        'pointer advances to V692;canonical and historical V610 pointers unchanged. '
        'Evidence and ordinary guide candidates on E,no guide approval,commit or '
        'push. See [V692 checkpoint](navigator_filter_v692_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for path in (*map(Path, SOURCES), DOC, Path('translations/navigator_captain_filter_v1.json'),
                 Path('translations/release_stack.json')):
        copy(path, ARCHIVE / 'sources' / path)
    for path in ROOT.rglob('*'):
        if path.is_file() and path.suffix.lower() != '.nds':
            copy(path, ARCHIVE / 'analysis' / path.relative_to(ROOT))
    for path in (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta')):
        copy(path, ARCHIVE / 'release' / path.name)
    external = {}
    # These files already live in the user's requested E-drive destination.
    # Preserve exact hashes/references instead of duplicating all RAM snapshots.
    for folder in (*CAP.glob('deck_gender_v692_*'), *CAP.glob('navigator_filter_v692_*')):
        for path in folder.rglob('*'):
            if path.is_file():
                external[str(path)] = sha(path.read_bytes())
    baseline = CAP / 'story_percent_v685_ordinary/capture_report.json'
    original = read(baseline)
    for path in (baseline, *(Path(r['path']) for r in original['frames_captured']),
                 CAP / 'story_percent_v685_ordinary/final_arm9_ram.bin'):
        external[str(path)] = sha(path.read_bytes())
    reconstruction = ROOT / 'V692_exact_patch_reconstruction.nds'
    external[str(reconstruction.resolve())] = sha(reconstruction.read_bytes())
    report = CAP / 'navigator_filter_v692_ordinary/capture_report.json'
    guide_files = {}
    for frame, name in ((1600, 'Captain selection.png'), (9000, 'Opening dialogue.png'),
                        (24100, 'Lisbon trading.png')):
        source = CAP / f'navigator_filter_v692_ordinary/frame_{frame:06d}_cold_boot.png'
        destination = GUIDE / name
        copy(source, destination)
        guide_files[str(destination)] = {'sha256': sha(source.read_bytes()), 'source_frame': frame}
    copy(report, GUIDE / 'capture_report.json')
    guide_files[str(GUIDE / 'capture_report.json')] = {'sha256': sha(report.read_bytes())}
    save(GUIDE / 'provenance.json', {'ROM_sha256': static['candidate_sha256'], 'files': guide_files,
        'ordinary_cold_boot_no_donor_fixture_or_observer': True, 'targeted_emulator_not_full_playthrough': True,
        'guide_candidates_not_publication_approved': True})
    save(ARCHIVE / 'provenance.json', {'scripts': {p: sha(Path(p).read_bytes()) for p in SOURCES},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'external_E_drive_evidence': external, 'guide_provenance': str(GUIDE / 'provenance.json'),
        'guide_provenance_sha256': sha((GUIDE / 'provenance.json').read_bytes()),
        'fixture_or_duty_test_screens_not_guide_approved': True, 'full_goal_complete': False})
    print('V692 registered repair,full scope,evidence references and ordinary guide candidates recorded on E.', flush=True)


if __name__ == '__main__':
    main()
