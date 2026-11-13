"""Seal 249 individual research reviews; registered release and completion credit remain separate."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices, labels, count_and_base
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Rafael_B51_B60_checked_20261104')
INPUT = Path('work/analysis/Rafael_B51_B60_current_runtime_20261104')
REBUILT = Path('work/analysis/Rafael_B51_B60_rebuilt_20261104/reconstruction.json')
STORED = Path('work/analysis/Rafael_B51_B60_stored_native_20261104/stored_native_verification.json')
LOOKUP = Path('work/analysis/Rafael_B51_B60_stored_catalogue_20261104/all245_stored_effective_body_bindings.json')
LOADERS = Path('work/analysis/Rafael_B51_B60_loaders_20261104/verification.json')
VISUAL = Path('work/analysis/Rafael_B51_B60_formatting_20261104/body_display_approval_v4.json')
PIXELS = Path('work/analysis/Rafael_B51_B60_focused_pixels_20261104/focused_actual_pixels.json')
MENU_PIXELS = Path('work/analysis/Rafael_B60_menu_actual_pixels_20261104/menu_actual_pixels.json')
NAMES = Path('translations/rafael_B51_B60_scoped_progressive_names_final_v1.json')
FINAL = Path('translations/rafael_B51_B60_contextual_final_review_v1.json')
NAMES_FINAL = Path('translations/rafael_B51_B60_scoped_names_actual_final_v2.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not FINAL.exists() and not NAMES_FINAL.exists()
    doc, plan, native, rebuilt, stored, lookup, loaders, visual, pixels, menu_pixels, names = map(load, [
        INPUT/'formatting_input.json', INPUT/'compatible_plans.json', INPUT/'compatible_native_pages.json',
        REBUILT, STORED, LOOKUP, LOADERS, VISUAL, PIXELS, MENU_PIXELS, NAMES])
    assert len(doc['records']) == 249 and (doc['proposed_revisions'], doc['wording_retentions']) == (102, 147)
    assert visual['final_253_pages_have_exact_native_glyphs_bounds_controls_substitutions_consumption_pagination_andvisual_approval']
    assert visual['changed_layout_records'] == 38 and stored['complete_stored_pages'] == 253
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes'] and stored['fresh_relocated_native_relative_cases'] == 380
    assert stored['reconstruction_sha256'] == sha(REBUILT.read_bytes()) and native['runtime'] == stored['runtime']
    assert len(lookup['records']) == 245 and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert (loaders['fresh_whole_archive_loads_andcache_hits'], loaders['fresh_parent_cases'], loaders['exact_reused_parent_cases']) == (343, 20, 666)
    assert pixels['all_complete_native_body_andheader_planes_andblank_guards_match']
    assert (pixels['selected_utterances'], pixels['selected_pages'], pixels['complete_body_planes'], pixels['complete_header_planes']) == (27, 30, 64, 58)
    assert menu_pixels['both_two_option_menu_caption_planes_centering_first_internal_final_glyphs_andblank_guards_match']
    assert menu_pixels['first_menu_cursor_down_up_andsecond_menu_cursor_down_observed']
    assert menu_pixels['A_acceptance_followed_by_original_next_fixture_speech_observed']
    sheets = [*pixels['review_sheets'], menu_pixels['review_sheet']]
    assert len(sheets) == 6
    for sheet in sheets:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    # All six readable sheets, the individual pause at4320 and the initial
    # second-menu highlight frames5280/5400/5520 were directly viewed this turn.
    ROOT.mkdir()
    actual_visual = ROOT/'actual_visual_approval.json'
    save(actual_visual, dict(reviewed_sheets=sheets, all_six_sheets_directly_viewed=True,
        all18_scoped_headers_andall_sampled_body_pages_readable=True,
        all_four_captions_both_cursor_positions_andboth_modal_continuations_directly_viewed=True,
        FE_pause_individual_capture='work/rf51cap/frame_004320_cold_boot.png',
        FE_pause_three_original_font_period_pixels_present_at_relative_xy=[[0,9],[6,9],[12,9]],
        FE_pause_retained_as_source_intended_silence_not_missing_text=True,
        second_menu_initial_highlight_at5400_andlater_option1_at5520_directly_viewed=True,
        conditional_B60_R486_crosses_page_butkeeps_entire_mustached_bastard_noun_phrase_together=True,
        no_new_findings=True, guide_photos=False, new_credit=0))
    observed_ids = {r['id'] for r in pixels['body_pages']} | {r['id'] for r in menu_pixels['body_pages']}
    assert len(observed_ids) == 32
    actual_path = ROOT/'actual_review.json'
    actual = dict(total_frames=18662, initialized_fixture_runs=2, actual_utterances=32, actual_body_pages=35,
        offline_only_utterances=213, actual_choice_captions=4, observed_actor_IDs=sorted({r['actor_ID'] for r in pixels['headers']}),
        complete_body_planes=pixels['complete_body_planes']+len(menu_pixels['body_pages']), complete_header_planes=58,
        all_six_QA_sheets_directly_viewed=True, all_required_distinct_wrap_glyph_macro_pagination_andmenu_cases_pass=True,
        focused_pixels=str(PIXELS), focused_pixels_sha256=sha(PIXELS.read_bytes()),
        menu_pixels=str(MENU_PIXELS), menu_pixels_sha256=sha(MENU_PIXELS.read_bytes()),
        native_return_values_andoriginal_relative_branch_sites_checked_offline=True,
        live_numeric_return_register_original_menu_response_branches_andcancellation_unvisited=True,
        natural_activation=False, original_location=False, earned_chronology=False, full_route=False, hardware=False,
        disclosed_synthetic_display_sequences=True, sampled_ids=sorted(observed_ids),
        final_menu_R41_is_source_command_continuation_sentinel_not_original_branch_outcome=True,
        no_world_state_orfull_catalogue_UI_claim=True, guide_photos=False, new_credit=0)
    save(actual_path, actual)
    names_final = deepcopy(names)
    assert len(names_final['records']) == 18 and all(all(r['review'].values()) for r in names_final['records'])
    for row in names_final['records']:
        assert row['actor_ID'] in actual['observed_actor_IDs']
        row['actual_target_headers_unvisited'] = False
        row['formatting_scope'] = 'Complete original style11 name planes and58 pixel-bound actual headers in a disclosed initialized fixture; full catalogue UI remains unvisited.'
        row['actual_header_evidence'] = dict(path=str(PIXELS), sha256=sha(PIXELS.read_bytes()), actor_ID=row['actor_ID'])
    names_final.update(source_scoped_review=str(NAMES), source_scoped_review_sha256=sha(NAMES.read_bytes()),
        actual_header_evidence=str(PIXELS), actual_header_evidence_sha256=sha(PIXELS.read_bytes()),
        no_new_dialogue_credit=True, registered_deployment_pending=True, new_credit=0)
    validate_natural_dialogue_batch(names_final)
    save(NAMES_FINAL, names_final)
    final = deepcopy(doc)
    by_stored = {r['id']: r for r in stored['records']}
    by_plan = {r['id']: r for r in plan['records']}
    choice_refs = {}
    for group in rebuilt['groups']:
        for obj in group['native_objects']:
            rows = sorted([r for r in final['records'] if r['id'] in {v['id'] for v in obj['records']}], key=lambda r:r['source_index'])
            for row in rows:
                row['review']['formatting'] = True
            raw = compile_choices(bytes.fromhex(obj['source_hex']), bytes.fromhex(obj['current_hex']), rows)
            assert raw.hex() == obj['compiled_hex']
            count, base = count_and_base(raw)
            offsets = struct.unpack_from('<'+str(count)+'H', raw, 2)
            for row, offset, value in zip(rows, offsets, labels(raw), strict=True):
                choice_refs[row['id']] = dict(file_path=doc['file_path'], block=group['block'], command_offset=obj['new_offset'],
                    native_command_word=0x2100, source_index=row['source_index'], offset=obj['new_offset']+base+offset,
                    exact_stored_hex=value.hex(), exact_choice_object_hex=raw.hex(), target_archive_sha256=rebuilt['target_archive_sha256'])
    assert len(choice_refs) == 4
    for row in final['records']:
        assert all(row['review'][k] for k in ['source','context','localization','naturalness'])
        row['review']['formatting'] = True
        if row['kind'] == 'typed-choice-label':
            ref = choice_refs[row['id']]
        else:
            entry = by_stored[row['id']]
            ref = dict(file_path=doc['file_path'], block=row['block'], offset=entry['new_offset'], header_offset=entry['new_offset']-5,
                record_index=entry['new_record_index'], exact_stored_hex=entry['stored_hex'], target_archive_sha256=rebuilt['target_archive_sha256'])
            row['planned_English_markup'] = by_plan[row['id']]['formatted_markup']
        row.update(planned_integrated_reference=ref, registered_release_andcompletion_credit_pending=True,
            all_fifth_formatting_gates_still_pending=False, complete_native_preamble_andfresh_formatting_pending=False,
            fresh_formatting_native_visual_stored_andrepresentative_gameplay_pending=False,
            actual_utterance_observed_in_disclosed_fixture=row['id'] in observed_ids if row['kind'] != 'typed-choice-label' else True,
            formatting_evidence=dict(native=str(INPUT/'compatible_native_pages.json'), stored=str(STORED), loaders=str(LOADERS),
                actual=str(actual_path), visual=str(actual_visual), scope='All253 body pages/four captions offline;32 utterances/35 body pages/four captions in initialized display fixtures,213 utterances offline-only. No natural event activation.'))
    final.update(format='dk4-editorial-final-review-v1', all_five_individual_review_gates_passed=True,
        all_formatting_gates_false=False, registered_release_andcompletion_credit_pending=True, new_credit=0,
        scoped_name_review=str(NAMES_FINAL), scoped_name_review_sha256=sha(NAMES_FINAL.read_bytes()),
        formatting_evidence={str(p):sha(p.read_bytes()) for p in [REBUILT, STORED, LOOKUP, LOADERS, VISUAL, PIXELS, MENU_PIXELS,
            NAMES_FINAL, actual_path, actual_visual, INPUT/'compatible_plans.json', INPUT/'compatible_menu_objects.json',
            INPUT/'dependency_qualification.json', Path(__file__)]})
    validate_natural_dialogue_batch(final)
    save(FINAL, final)
    save(ROOT/'release_plans.json', plan)
    save(ROOT/'formatting_checkpoint.json', dict(final_review=str(FINAL), final_review_sha256=sha(FINAL.read_bytes()),
        scoped_names=str(NAMES_FINAL), scoped_names_sha256=sha(NAMES_FINAL.read_bytes()), prose_reviews=249,
        revised=102, retained=147, body_pages=253, captions=4, layout_corrections=38, ASCII_I_fixes=3,
        scoped_names_retained=17, exclusive_Fernan_name_glyph_corrections=1,
        actual_frames=18662, actual_utterances=32, actual_body_pages=35, offline_only_utterances=213,
        all_individual_five_gates_pass_in_research=True, registered_release_andcompletion_credit_pending=True,
        new_credit=0, guide_photos=False, full_goal_complete=False))
    print('249 five-gate research reviews:102 revisions/147 retentions;32 observed utterances/213 offline-only;18 scoped names. Registered integration pending,zero credit.')
