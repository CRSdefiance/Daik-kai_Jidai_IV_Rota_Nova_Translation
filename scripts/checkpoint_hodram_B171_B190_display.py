"""Record completed speech/menu/name display work; storage and actual QA remain open."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.save_editorial_progress_checkpoint_v1 import checkpoint

ROOT = Path('work/analysis/Hodram_B171_B190_formatting_20261102')
APPROVED = ROOT / 'speech_display_approved_20261104'
NAMES = Path('work/analysis/Hodram_B171_B190_scoped_name_planes_20261104/native_name_planes.json')
MENUS = Path('work/analysis/Hodram_B171_B190_menu_20261104/complete_choice_objects.json')
SUMMARY = ('B171–B190: all 435 contextual prose decisions (195 revisions/240 retentions) and 49 scoped name/term retentions preserved. '
    'All 433 speech objects/439 final native pages are visually approved; 15 layout defects are corrected without changing prose. '
    'Both captions and 31 name strings pass native and visual checks. Stored reconstruction, representative English gameplay and registered integration remain. '
    'No credit or ROM added; 9498 complete, experimental 7774721f and main unchanged. Full scope/all evidence preserved; no guide photos.')


if __name__ == '__main__':
    proof, native, visual, names, menus = map(load, [APPROVED / 'checkpoint.json', APPROVED / 'all433_native_pages.json',
        APPROVED / 'visual_approval.json', NAMES, MENUS])
    assert proof['native_andvisually_approved_final_pages'] == native['pages'] == 439 and len(native['records']) == 433
    assert visual['all439_final_pages_visually_approved'] and visual['all15_individual_layout_findings_resolved']
    assert (names['actors'], names['distinct_current_strings'], names['fresh_planes'], names['exact_reused_planes']) == (32, 31, 13, 18)
    assert names['runtime'] == native['runtime'] and menus['all_checks_pass'] and len(menus['objects']) == 1
    for sheet in names['review_sheets'] + [menus['objects'][0]['review_sheet']]:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    save(NAMES.with_name('visual_review.json'), dict(native=str(NAMES), native_sha256=sha(NAMES.read_bytes()),
        directly_viewed_sheets=names['review_sheets'], all31_bound_name_strings_visually_approved=True,
        complete_first_internal_final_glyphs_native_font_andbounds_pass=True, current_getter_values=64,
        fresh_native_planes=13, exact_previous_native_planes_reused=18,
        no_new_getter_calls_orname_data_changes=True, full_catalogue_UI_not_observed=True,
        representative_English_headers_pending=True, actual_gameplay=False, new_credit=0))
    save(MENUS.with_name('visual_review.json'), dict(native=str(MENUS), native_sha256=sha(MENUS.read_bytes()),
        directly_viewed_sheet=menus['objects'][0]['review_sheet'], both_reviewed_captions_visually_approved=True,
        all_source_current_andreviewed_provider_alignments_andbridged_returns_pass=True,
        normal_andhighlight_font_planes_automatically_verified=True, actual_controller_selection_not_observed=True,
        complete_leading_trailing_characters_native_font_centering_andbounds_pass=True, actual_gameplay=False, new_credit=0))
    evidence_paths = [APPROVED / 'checkpoint.json', APPROVED / 'all433_compiled_plans.json', APPROVED / 'all433_native_pages.json',
        APPROVED / 'visual_approval.json', NAMES, NAMES.with_name('visual_review.json'), MENUS, MENUS.with_name('visual_review.json'), Path(__file__)]
    display_checkpoint = APPROVED / 'complete_display_checkpoint.json'
    save(display_checkpoint, dict(prose_reviews=435, proposed_revisions=195, justified_retentions=240,
        scoped_name_andterm_retentions=49, native_speeches=433, native_andvisually_approved_final_pages=439,
        initial_pages_viewed=440, replacement_pages_viewed=17, speech_review_sheets_viewed=51,
        layout_defects_fixed=15, FE_glyph_row_defects_fixed=4, visual_phrase_page_defects_fixed=11,
        caption_records=2, typed_menus=1, native_provider_alignments=6, bridged_returns=18, caption_style_planes=8,
        scoped_actors=32, bound_consumers=64, native_name_strings=31, fresh_name_planes=13, reused_name_planes=18,
        all_required_new_offline_display_checks_pass=True, actual_gameplay=False,
        stored_source_commands_allocation_relative_reconstruction_gameplay_andregistered_release_pending=True,
        overall435_fifth_gates_still_false=True, full_goal_complete=False, new_credit=0, guide_photos=False,
        evidence={str(p): sha(p.read_bytes()) for p in evidence_paths}))
    text = '''# Hodram B171–B190: speech, menu and name display checkpoint

All 435 complete contextual comparisons remain preserved: 195 proposed revisions and 240 justified retentions, with four prose gates on every record. The 49 scoped name/term decisions remain retentions. See the earlier prose checkpoint for the source-first chronology and individual editorial findings; do not repeat those comparisons.

All 433 speeches (405 progressive/28 FE) now pass fresh native glyph, macro, input-canary, full-character, bounds and pagination checks on the registered 7774721f runtime. All 439 final pages have been directly viewed. The 440 initial pages/46 readable sheets and 17 replacement pages/five additional sheets were reviewed. Fifteen individual layout findings are resolved with no wording changes: four real FE row defects and eleven phrase/page-boundary issues. The FE defects split the last letter of view/press onto its own row or inserted an unwanted blank row. Their corrected native glyph-row membership matches the plan exactly.

Page refinements keep complete contrast clauses, restrictions and final sentences together. One complete sailing question now occupies a single page. The paragraph that cannot fit a single native page while preserving following wind keeps the whole headwind contrast on page two. Bottom space before complete thoughts is generated by the formatter; editable prose contains no ordinary authored breaks or alignment. King Muryeong, a woman's heart, say it, realize it and since when receive scoped phrase-continuity treatment. No font, viewport or engine change was made.

The original native job 56647 is terminal/exit 1; its saved 27 B171 records/31 pages are reused unchanged. The four later FE findings that caused the failure are now closed. Session 22958 completed the remaining 406 records/409 initial pages, exit 0. Session 61396 checked only the eleven changed visual records/17 pages, exit 0. The final set binds 1732 macro alignment cases; the eleven refreshes add 44 cases. No live job remains and no failed initial run should be restarted.

The two captions in B171 command 154 pass native source/current/reviewed provider checks: six alignments, 18 bridged modal returns, eight normal/highlight caption planes and seven rejected invalid compiler cases. Listen. replaces Hear; No thanks is retained. The complete compiled object is 24 bytes. The readable caption sheet was viewed. Actual controller selection and stored relocation remain pending.

All 32 actors' 64 name-consumer values remain bound. Their 31 distinct strings pass native style-11 complete glyph/bounds tests: 13 fresh planes and 18 exact existing planes reused through the proven static-data inverse and unchanged code/font/literal dependencies. Both name sheets were viewed. These full-name literal tests do not claim visits to the catalogue UI. The six typed story terms and eleven forecast-city labels remain unchanged with exact field bindings; no new item/city widget visit is claimed. Broader name/Proofs audits remain open outside this scoped pass.

Authoritative evidence:

- `translations/hodram_B171_B190_contextual_editorial_manuscript_v1.json`: all 435 individual decisions, exact source/current references and five gates.
- `translations/hodram_B171_B190_scoped_names_andterms_v1.json`: 49 individual retentions.
- `work/analysis/Hodram_B171_B190_formatting_20261102/speech_display_approved_20261104/`: final 433 compiled plans, native proofs, direct visual approval, caption input and complete display checkpoint.
- `work/analysis/Hodram_B171_B190_menu_20261104/`: native provider/planes, compiled menu and direct visual review.
- `work/analysis/Hodram_B171_B190_scoped_name_planes_20261104/`: 31 bound name planes and direct visual review.
- `work/analysis/Hodram_B171_B190_FE_diagnostic_20261104/`: the four original native row failures; preserve them as historical diagnostics.

Next, reconstruct all twenty complete SC1 blocks with the unchanged nontext controls and original 2100 two-choice object. There are no 4100 style objects or actor0 bodies. Use the generic complete-scene workflow with this exact scope, not the B156-specific cinematic successor. Then check stored bytes, relocation/allocation, native relative cases and archive loading. Reuse all unchanged compiled/native/visual proofs. Representative English gameplay should cover the sail-lesson menu's two selections, a generated page boundary, ordinary speaker/portrait transitions and the FE behavior; include town scenes broadly as practical. These offline previews are not observed gameplay, natural conditional activation, a complete route or hardware verification. No new gameplay run has been claimed for this batch.

Once those necessary checks pass, close the individual fifth gates, register the cumulative scene layer, and use the full registered static-text pipeline while preserving every existing runtime/name/static layer and ASCII right bounds. Produce an exactly reconstructable clean-input patch and candidate-own startup proof before adding once-only credit. Do not promote main without user acceptance.

The registered experimental candidate remains `7774721fdc6da677f56a75a7350785f3cc5e90759c6784527b3c144fa77b0399`; main remains `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. No new ROM, credit, commit/push or pruning. Coverage remains 9498 completed (5809 revisions/3689 retentions); historical source/prose/draft counters remain 9501. All earlier work, ROMs, translations and evidence are preserved. The full editorial goal remains active across every storyline, shared shop/town exchange, random scene and remaining player-facing text. Graphics artwork and the later older-record technical re-audit remain separate. No guide photos.
'''
    updates = dict(source_current_contextual_comparison_and49_scoped_retentions_preserved=True,
        native_speech_records=433, final_native_andvisually_approved_pages=439, initial_speech_pages=440,
        layout_corrections=15, FE_glyph_row_corrections=4, visual_phrase_page_corrections=11,
        speech_direct_visual_sheets=51, typed_caption_native_andvisual_pass=True,
        native_provider_alignments=6, bridged_modal_returns=18, caption_style_planes=8,
        scoped_name_native_andvisual_pass=True, distinct_name_strings=31, fresh_name_planes=13, reused_name_planes=18,
        native_initial_job=dict(session=56647, terminal=True, exit_code=1, saved_block171_reused=True,
            four_later_FE_row_failures_resolved_with_fresh_checks=True),
        completed_native_jobs=[dict(session=22958, terminal=True, exit_code=0), dict(session=61396, terminal=True, exit_code=0)],
        no_live_job=True, all_final_speech_native_andvisual_checks_pass=True, actual_new_batch_gameplay=False,
        stored_reconstruction_gameplay_andregistered_release_pending=True,
        complete_display_checkpoint=str(display_checkpoint), complete_display_checkpoint_sha256=sha(display_checkpoint.read_bytes()),
        new_credit=0, full_goal_complete=False, guide_photos=False)
    protected = {'translations/release_stack.json': '7e7288fe7920fb601ab96a6bde937793c2c9873dd6a9573be796853d7924d143',
        'out/all_routes_combined_hodram_b151_b170_static_text_20261102_candidate.nds': '7774721fdc6da677f56a75a7350785f3cc5e90759c6784527b3c144fa77b0399',
        'out/raphael_natural_v2_accepted_base.nds': '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'}
    checkpoint(mutation=ROOT / 'display_checkpoint_mutation_20261104_v1', batch_key='Hodram_B171_B190_clean_next_20261102',
        batch_updates=updates, summary=SUMMARY, document='docs/editorial_hodram_B171_B190_display_20261104.md',
        document_text=text, completed=9498, protected=protected)
    print('Saved complete speech/menu/name display checkpoint. 9498 completions and all prior releases preserved; full goal active.')
