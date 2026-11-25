"""Save completed prose/display research without adding release completion credit."""
import gzip
import json
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT = Path('work/analysis/Hodram_B131_B150_editorial_20261102')
MANUSCRIPT = Path('translations/hodram_B131_B150_editorial_manuscript_v2.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/editorial_hodram_B131_B150_display_20261102.md')


def main():
    checkpoint = ROOT / 'prose_display_checkpoint_v1.json'
    assert not checkpoint.exists()
    doc = load(MANUSCRIPT)
    assert len(doc['records']) == 329 and doc['revised'] == 180 and doc['retained'] == 149
    assert all(not row['review']['formatting'] for row in doc['records'])
    native_path = ROOT / 'native_v3/compiled_native_pages.json'
    native = load(native_path)
    assert len(native['records']) == 319 and native['pages'] == 328
    assert len(native['changed_layout_ids']) == 23 and len(native['reused_record_ids']) == 296
    initial_path = ROOT / 'visual_review_progress_v6.json'
    initial = load(initial_path)
    assert initial['all_initial_pages_directly_viewed'] and len(initial['findings']) == 23
    plans_path = ROOT / 'plans_v3/automatic_plans.json'
    plans = load(plans_path)
    planned = {r['id']: r for r in plans['records']}
    assert len(planned) == 319 and not plans['failures']
    assert not any(i['severity'] in ['error', 'warning'] for r in plans['records'] for i in r['base_QA']['issues'])
    preferences_path = ROOT / 'visual_formatting_preferences_v3.json'
    preferences = load(preferences_path)['records']
    assert {r['id'] for r in initial['findings']} == set(preferences) == set(native['changed_layout_ids'])
    sheets = native['review_sheets']
    assert len(sheets) == 9 and sum(s['pages'] for s in sheets) == 32
    for sheet in sheets:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    findings = []
    for finding in initial['findings']:
        record_id = finding['id']
        findings.append(dict(**{k: v for k, v in finding.items() if k != 'resolved'},
                             resolved=True, final_lines=planned[record_id]['lines'],
                             exact_source_bound_preference=preferences[record_id]))
    visual_path = ROOT / 'visual_review_progress_v7.json'
    save(visual_path, dict(native=str(native_path), native_sha256=sha(native_path.read_bytes()),
                          previous_review=str(initial_path), previous_review_sha256=sha(initial_path.read_bytes()),
                          directly_viewed_sheet_indices=list(range(9)), directly_viewed_sheets=sheets,
                          newly_directly_viewed_pages=32, unchanged_exact_native_pages_reused=296,
                          total_final_speech_pages=328, all_final_speech_pages_approved=True,
                          findings=findings, unresolved_speech_layout_findings=0,
                          initial_329_pages_already_directly_viewed=True,
                          justified_layout_retentions=initial['justified_layout_retentions'],
                          ordinary_grammar_retention=preferences['DK4_MES_B142_R0159']['QA_line_ending_retention'],
                          overall_formatting_gates_still_false=True, actual_gameplay=False, new_credit=0))
    menu_path = ROOT / 'menus_v1/complete_choice_objects.json'
    menus = load(menu_path)
    assert len(menus['objects']) == 5 and menus['all_checks_pass']
    menu_sheets = [o['review_sheet'] for o in menus['objects']]
    for sheet in menu_sheets:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    assert menu_sheets[1]['sha256'] == menu_sheets[2]['sha256']
    menu_visual_path = ROOT / 'menus_v1/caption_visual_review.json'
    save(menu_visual_path, dict(menu_receipt=str(menu_path), menu_receipt_sha256=sha(menu_path.read_bytes()),
                               review_sheets=menu_sheets, all_ten_reviewed_captions_visually_approved=True,
                               B135_sheet_exactly_identical_to_directly_viewed_B134=True,
                               whole_glyphs_centering_and_native_font_consistent=True,
                               actual_controller_and_stored_integration_still_pending=True,
                               actual_gameplay=False, new_credit=0))
    style_path = ROOT / 'style_v1/compiled_style_objects.json'
    style = load(style_path)
    assert len(style['objects']) == 1 and style['native_target_slot_cases'] == 8 and style['physical_alternatives'] == 8
    fe_path = ROOT / 'FE_native_row_membership_v1.json'
    fe = load(fe_path)
    assert len(fe['records']) == 23 and fe['all_pass'] and fe['original_installed_inside_word_wrap_rejected']
    registry = Path('translations/release_stack.json')
    assert sha(registry.read_bytes()) == 'd3cf0000ad4d1a3e4f9df5c0880a001f7449744e5251ced6f613a05d438d076a'
    reviews = [Path(p) for p in [
        'translations/hodram_B131_contextual_prose_review_v2.json',
        'translations/hodram_B132_contextual_prose_review_v2.json',
        'translations/hodram_B133_B140_and_choices_contextual_prose_review_v1.json',
        'translations/hodram_B141_B143_contextual_prose_review_v1.json',
        'translations/hodram_B144_B150_contextual_prose_review_v1.json']]
    evidence = [MANUSCRIPT, plans_path, native_path, visual_path, fe_path, style_path, menu_path,
                menu_visual_path, preferences_path, *reviews, registry,
                Path('work/analysis/Hodram_B131_B150_clean_20261102/complete_clean_meanings_checkpoint.json'),
                Path('work/analysis/Hodram_B131_B150_clean_20261102/clean_English_draft_checkpoint.json')]
    state = dict(total_batch_objects=329, ordinary_speeches=311, style_bodies=8, two_choice_labels=10,
                 prose_objects_contextually_compared=329, revisions=180, justified_retentions=149,
                 remaining_prose_comparisons=0, four_individual_prose_gates_pass=True,
                 clean_meanings_anddrafts_preceded_current_English=True,
                 manuscript=str(MANUSCRIPT), manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
                 final_speech_objects=319, final_speech_pages=328,
                 initial_speech_pages_directly_viewed=329, replacement_pages_directly_viewed=32,
                 exact_unchanged_native_proofs_reused=296,
                 resolved_layout_findings=23, unresolved_speech_layout_findings=0,
                 FE_native_row_membership_checks=23, original_inside_word_wrap_regression_rejected=True,
                 native_macro_alignment_cases=1276, new_alignment_cases=92,
                 compiled_personality_objects=1, personality_target_pointer_cases=8,
                 checked_choice_objects=5, checked_caption_records=10,
                 choice_provider_alignment_cases=30, bridged_modal_returns=90, caption_style_planes=40,
                 offline_native_display_checks=True, actual_new_gameplay=False,
                 terminal_native_jobs={'62939': 'exit1; completed83 proofs preserved',
                                       '94264': 'exit0; completed319 combined native proofs',
                                       '72149': 'exit0;23 changed layouts,32 pages,296 exact reuses'},
                 all_overall_formatting_gates_still_false=True,
                 pending=[
                     'Scoped speaker/role/mentioned-name editorial decisions and two katakana de fields: qualify exclusive ownership/native glyph consumers before changing fields.',
                     'Rebuild and verify stored scene commands, offsets/relative branches, archive loads and complete consumption with these compiled mixed objects.',
                     'Representative English gameplay/focused tests for new B133 dynamic role, B136 cargo/X behavior, B142 embedded heading/pagination, B143 actor0 transition, choices and returns; existing runtime proofs are reusable.',
                     'Registered cumulative release qualification, exact clean-input patch and candidate-own startup; no main promotion without user acceptance.'],
                 source2000_label_free_controls_preserved_pending_stored_flow_check=True,
                 B137_previously_completed_excluded=True,
                 no_guide_photos=True, new_ROMs=0, new_emulator_runs=0, new_credit=0,
                 completed_records_unchanged=8527,
                 current_registered_candidate='out/all_routes_combined_hodram_b111_b130_names_20261102_candidate.nds',
                 current_registered_candidate_sha256='f2f0bf2fd904ead5d539b25d516d53fa70a0175af145be27751e8d9f6f2ccde2',
                 main_unchanged=True, full_goal_complete=False,
                 graphics_artwork_and_later_older_record_technical_reaudit_separate=True,
                 evidence={str(p): sha(p.read_bytes()) for p in evidence})
    save(checkpoint, state)
    note = '''B131–B150 now has all 329 contextual prose decisions: 180 revisions and 149 justified retentions. All four per-record prose gates pass; final completion credit remains pending.

All 329 initial speech pages were directly reviewed. The 23 resulting findings are resolved without changing or shortening prose: nine page-boundary fixes, one unnecessary second page, twelve phrase/early-wrap fixes and the FE wrap inside “installed.” The 23 changed objects produced 32 directly viewed replacement pages; 296 unchanged native proofs are reused. Final speech coverage is 319 objects / 328 pages. All 23 FE objects now pass actual glyph-row membership checks; that check rejects the original “installe” / “d!” defect. One mechanical weak-ending warning has a precise retention: “with no one to turn to...” completes a phrasal construction before a separate question. Its original QA and reason are preserved.

The full B133 personality object passes eight native target-pointer cases and nine compiler rejection cases. Five two-choice objects / ten captions pass 30 provider alignments, 90 bridged modal returns and 40 complete caption style planes; reviewed captions were visually approved. These are offline native checks, not new gameplay. B135’s caption sheet is byte-identical to the directly viewed B134 sheet. Native jobs 62939 (exit1; first83 proofs retained), 94264 (exit0) and 72149 (exit0) are terminal. Do not replay them or the completed source/prose/visual passes.

Continue with scoped names/role labels and the two remaining katakana デ fields, then stored mixed-object/branch/archive checks, representative English gameplay and registered cumulative integration with an exact clean-input patch and candidate-own startup. The B136 X/cargo behavior, B142 embedded Foreign Girl heading, B143 Rafael transition and choices need appropriate representative evidence; exhaustive conditional playthroughs are unnecessary. Preserve label-free 2000 commands, existing runtime/name corrections and the ASCII right-bound repair. The broader Proof terminology question remains separate open editorial scope.

No new ROM, emulator run, promotion or completion credit. Completed coverage remains 8,527; registered candidate f2f0bf2f and main remain unchanged. All ROMs, translations and evidence remain preserved. No guide photo collection: only necessary QA previews/focused gameplay. Every storyline and other prose family remains in scope; graphics artwork and the later older-record technical re-audit stay separate. Full goal active.
'''
    detailed = '''# Hodram B131–B150: completed prose and offline display review

''' + note + '''
Use `work/analysis/Hodram_B131_B150_editorial_20261102/prose_display_checkpoint_v1.json` as the current machine checkpoint. It hashes the five individual comparison packets, manuscript v2, plans v3, native v3, visual review v7, FE row proof, complete style object and menu receipts. Every prose decision retains exact clean/current references and an individual finding or retention reason. The prior 75-comparison checkpoint is historical.

- Manuscript: `translations/hodram_B131_B150_editorial_manuscript_v2.json`.
- Final speech plan: `work/analysis/Hodram_B131_B150_editorial_20261102/plans_v3/automatic_plans.json`; automatic planner v18 and byte-bound `visual_formatting_preferences_v3.json`. The 13 source-qualified structural/dramatic layouts remain unchanged.
- Native pages: `work/analysis/Hodram_B131_B150_editorial_20261102/native_v3/compiled_native_pages.json`; fresh changed pages in `native_v3/fresh/`. All final speech pages are visually approved through exact unchanged reuse plus directly viewed replacements.
- Visual findings/resolutions: `work/analysis/Hodram_B131_B150_editorial_20261102/visual_review_progress_v7.json`.
- FE row comparisons/regression: `work/analysis/Hodram_B131_B150_editorial_20261102/FE_native_row_membership_v1.json`.
- Style: `work/analysis/Hodram_B131_B150_editorial_20261102/style_v1/compiled_style_objects.json`.
- Menus: `work/analysis/Hodram_B131_B150_editorial_20261102/menus_v1/complete_choice_objects.json` and `caption_visual_review.json`.

Formatting gates remain false in the manuscript until the pending names, stored-content and representative behavior checks are reconciled. This is not a registered B131–B150 release or an assertion that every conditional scene has been visited. Preserve failed planner v17/v18 attempts and all earlier plans as diagnostics; current automatic v7/final v3 passes without errors or unreviewed warnings.
'''
    assert not DOC.exists()
    updates = {DOC: detailed}
    handoff = Path('docs/editorial_handoff_current.md')
    old = handoff.read_text(encoding='utf-8')
    updates[handoff] = '# Current editorial handoff - 2026-11-02: B131–B150 prose/display checked\n\n' + note + '\nContinue from [the exact current checkpoint](editorial_hodram_B131_B150_display_20261102.md).\n\n# Historical checkpoint - 75 comparisons\n\n' + old.split('\n', 1)[1]
    workflow = Path('docs/editorial_efficiency_workflow.md')
    first, remainder = workflow.read_text(encoding='utf-8').split('\n', 1)
    updates[workflow] = first + '\n\nCurrent checkpoint: all329 B131–B150 prose decisions (180 revisions/149 retentions),319 speech objects/328 final offline native pages andall23 layout findings resolved. All final speech pages andten menu captions are visually approved. One complete eight-body personality object andfive choice objects pass compiler/native checks. Reuse completed source/prose andunchanged native/visual proofs;do not restart the obsolete75-comparison checkpoint. Scoped names,two de fields,stored integration,representative English gameplay andregistered release remain. No new completion credit orROM;8527 completed,current f2f0bf2f/main unchanged. No guide photos. See [current evidence](editorial_hodram_B131_B150_display_20261102.md).\n\nEarlier checkpoint notes below are historical.\n' + remainder
    for filename in ['known_issues.md', 'todo.md', 'translation_progress.md']:
        path = Path('docs') / filename
        title = 'B131–B150: 329 prose decisions; 23 layout findings resolved; integration pending'
        updates[path] = '## 2026-11-02: ' + title + '\n\n' + note + '\nSee [current exact evidence and remaining work](editorial_hodram_B131_B150_display_20261102.md). Earlier entries below are historical.\n\n' + path.read_text(encoding='utf-8')
    old_prose_doc = Path('docs/editorial_hodram_B131_B150_prose_20261102.md')
    updates[old_prose_doc] = 'Current: all329 comparisons andoffline display review are now complete;continue from [the newer checkpoint](editorial_hodram_B131_B150_display_20261102.md). This earlier75-comparison snapshot is historical.\n\n' + old_prose_doc.read_text(encoding='utf-8')
    backup = ROOT / 'display_checkpoint_mutation_v1'
    assert not backup.exists()
    backup.mkdir()
    before = LEDGER.read_bytes()
    prior = json.loads(before)
    ledger = deepcopy(prior)
    key = 'Hodram_B131_B150_prose_and_display_20261102'
    assert key not in ledger
    ledger[key] = dict(**state, checkpoint=str(checkpoint), checkpoint_sha256=sha(checkpoint.read_bytes()))
    old_key = 'Hodram_B131_B150_source_drafts_20261102'
    ledger[old_key]['historical_checkpoint_superseded_by'] = str(checkpoint)
    ledger[old_key]['historical_checkpoint_superseded_by_sha256'] = sha(checkpoint.read_bytes())
    assert all(ledger[k] == v for k, v in prior.items() if k != old_key)
    assert ledger['completed_editorial_record_counts_by_file'] == prior['completed_editorial_record_counts_by_file']
    (backup / 'ledger.before.json.gz').write_bytes(gzip.compress(before, compresslevel=1, mtime=0))
    staged_ledger = encode_ledger(ledger)
    assert json.loads(staged_ledger) == ledger
    mutations = []
    for index, (path, text) in enumerate(updates.items()):
        data = path.read_bytes() if path.exists() else None
        if data is not None:
            (backup / f'{index}.before').write_bytes(data)
        mutations.append(dict(path=str(path), before_sha256=sha(data) if data is not None else None,
                              after_sha256=sha(text.encode('utf-8'))))
    save(backup / 'mutation_plan.json', dict(ledger_before_sha256=sha(before),
         ledger_after_sha256=sha(staged_ledger), documentation=mutations,
         release_registry_before_sha256=sha(registry.read_bytes()), completed_keys_unchanged=True))
    assert LEDGER.read_bytes() == before
    for entry, (path, text) in zip(mutations, updates.items()):
        assert (sha(path.read_bytes()) if path.exists() else None) == entry['before_sha256']
        path.write_text(text, encoding='utf-8', newline='\n')
        assert sha(path.read_bytes()) == entry['after_sha256']
    LEDGER.write_bytes(staged_ledger)
    assert sha(LEDGER.read_bytes()) == sha(staged_ledger)
    assert sha(registry.read_bytes()) == 'd3cf0000ad4d1a3e4f9df5c0880a001f7449744e5251ced6f613a05d438d076a'
    save(backup / 'verified_mutations.json', dict(all_document_hashes_pass=True,
         ledger_sha256=sha(staged_ledger), prior_completed_values_and_all_other_ledger_entries_preserved=True,
         release_registry_unchanged=True, no_completion_credit=True, full_goal_complete=False))
    print(dict(prose=329, revised=180, retained=149, final_native_pages=328,
               resolved_layout_findings=23, menus=5, new_credit=0, checkpoint=str(checkpoint)))


if __name__ == '__main__':
    main()
