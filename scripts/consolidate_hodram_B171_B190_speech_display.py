"""Join exact native proofs and directly viewed final pages without replaying them."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B171_B190_formatting_20261102')
MANUSCRIPT = ROOT / 'formatting_input.json'
INITIAL = ROOT / 'initial/automatic_plans.json'
GUARDED = ROOT / 'FE_guarded_rows_20261104/automatic_plans.json'
REPLACEMENTS = ROOT / 'visual_all11_v4_20261104/automatic_plans.json'
FIRST_NATIVE = Path('work/analysis/Hodram_B171_B190_native_20261102/initial/B171_checked.json')
REMAINING_NATIVE = Path('work/analysis/Hodram_B171_B190_native_20261104/remaining/compiled_native_pages.json')
REPLACEMENT_NATIVE = Path('work/analysis/Hodram_B171_B190_native_20261104/visual_replacements/compiled_native_pages.json')


if __name__ == '__main__':
    output = ROOT / 'speech_display_approved_20261104'
    assert not output.exists()
    doc, initial, guarded, replacements, first, remaining, refreshed = map(load, [
        MANUSCRIPT, INITIAL, GUARDED, REPLACEMENTS, FIRST_NATIVE, REMAINING_NATIVE, REPLACEMENT_NATIVE])
    assert remaining['runtime'] == refreshed['runtime']
    assert len(first['records']) == 27 and len(remaining['records']) == 406 and len(refreshed['records']) == 11
    assert remaining['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert refreshed['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    plan_by = {r['id']: r for r in guarded['records']}
    plan_by.update({r['id']: r for r in replacements['records']})
    initial_by = {r['id']: r for r in initial['records']}
    native_by = {r['id']: r for r in first['records'] + remaining['records']}
    native_by.update({r['id']: r for r in refreshed['records']})
    speech = [r for r in doc['records'] if r['kind'] != 'typed-choice-label']
    assert {r['id'] for r in speech} == set(plan_by) == set(native_by) and len(speech) == 433
    changed = [r['id'] for r in speech if plan_by[r['id']]['encoded_hex'] != initial_by[r['id']]['encoded_hex']]
    assert len(changed) == 15
    pages = 0
    for row in speech:
        plan, native = plan_by[row['id']], native_by[row['id']]
        assert plan['logical_English'] == native['logical_English'] == row['english']
        assert plan['encoded_hex'] == native['compiled_hex']
        assert row['source_reference'] == native['source_reference'] and row['current_reference'] == native['current_reference']
        assert not any(i['severity'] in ['warning', 'error'] for i in plan['base_QA']['issues'])
        display = native['complete_native_English_display']
        if row['kind'] == 'system-FE':
            assert display['planned_native_row_comparison']['complete_glyph_row_membership_exact']
            samples = [display]
        else:
            samples = display['pages']
        assert len(samples) == plan['expected_native_pages']
        for sample in samples:
            for path_key, digest_key in [('native_plane', 'native_plane_sha256'), ('preview', 'preview_sha256')]:
                assert sha(Path(sample[path_key]).read_bytes()) == sample[digest_key]
        pages += len(samples)
    assert pages == 439
    reviews = [ROOT / 'B171_B174_direct_visual_review_20261104.json', ROOT / 'B175_B190_direct_visual_review_20261104.json']
    earlier_sheets = [s for p in reviews for s in load(p)['review_sheets']]
    assert len(earlier_sheets) == 46
    for sheet in earlier_sheets + refreshed['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    assert len(refreshed['review_sheets']) == 5
    output.mkdir()
    final_plan = deepcopy(guarded)
    final_plan.update(manuscript=str(MANUSCRIPT), manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
        records=[plan_by[r['id']] for r in speech], failures=[], actual_layout_corrections=changed,
        FE_row_corrections=4, visual_phrase_orpage_corrections=11,
        no_prose_changed=True, direct_visual_review_pending=False)
    plan_path = output / 'all433_compiled_plans.json'
    save(plan_path, final_plan)
    final_native = deepcopy(remaining)
    final_native.update(manuscript=str(MANUSCRIPT), manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
        plan=str(plan_path), plan_sha256=sha(plan_path.read_bytes()), records=[native_by[r['id']] for r in speech],
        pages=439, fresh_compiled_alignments_in_final_record_set=1732, additional_refreshed_alignments=44,
        review_sheets=earlier_sheets + refreshed['review_sheets'], direct_visual_review_pending=False,
        excluded_typed_choice_IDs_separately_pending=[r['id'] for r in doc['records'] if r['kind'] == 'typed-choice-label'],
        exact_B171_partial_job_proof_reused=dict(path=str(FIRST_NATIVE), sha256=sha(FIRST_NATIVE.read_bytes()),
            original_session=56647, original_session_terminal_exit=1, successful_block_dispatch_saved_before_later_B172_failure=True,
            original_release=remaining['runtime']['release_proof'], original_startup=remaining['runtime']['startup_proof'],
            identical_original_invocation_runtime_andcomplete_compiled_B171_bytes=True),
        all439_final_pages_directly_viewed=True, actual_gameplay=False, formatting_gates_still_false=True,
        caption_name_stored_gameplay_andregistered_release_gates_pending=True,
        evidence={str(p): sha(p.read_bytes()) for p in [MANUSCRIPT, INITIAL, GUARDED, REPLACEMENTS,
            FIRST_NATIVE, REMAINING_NATIVE, REPLACEMENT_NATIVE, *reviews, Path(__file__)]})
    native_path = output / 'all433_native_pages.json'
    save(native_path, final_native)
    save(output / 'visual_approval.json', dict(native=str(native_path), native_sha256=sha(native_path.read_bytes()),
        reviewed_initial_sheets=earlier_sheets, directly_viewed_replacement_sheets=refreshed['review_sheets'],
        final_pages=439, speech_objects=433, initial_pages_viewed=440, replacement_pages_viewed=17,
        all439_final_pages_visually_approved=True, all15_individual_layout_findings_resolved=True,
        corrections=changed, FE_row_drift_fixed=4, phrase_andpage_findings_fixed=11,
        no_prose_shortening_ordinary_authored_breaks_font_viewport_orengine_changes=True,
        original_name_spelling_preserved_with_King_Muryeong_together=True,
        complete_first_internal_final_characters_consistent_native_font_andphrase_continuity_pass=True,
        guide_photos=False, actual_gameplay=False, new_credit=0))
    caption_doc = deepcopy(doc)
    caption_doc.update(records=[deepcopy(r) for r in doc['records'] if r['kind'] == 'typed-choice-label'], blocks=[171],
        physical_speech_objects=0, ordinary_speech_objects=0, typed_choice_objects=2, typed_choice_commands=1,
        total_editorial_objects=2, subset_of=str(MANUSCRIPT), subset_of_sha256=sha(MANUSCRIPT.read_bytes()))
    for row in caption_doc['records']:
        row['original_exact_source_reference'] = deepcopy(row['source_reference'])
        row['source_reference'].update(command_offset=row['source_command_offset'], source_index=row['source_index'])
    save(output / 'caption_native_input.json', caption_doc)
    save(output / 'checkpoint.json', dict(speech_objects=433, native_andvisually_approved_final_pages=439,
        layout_corrections=15, four_prose_gate_reviews=435, overall_fifth_gates_still_false=True,
        plan=str(plan_path), native=str(native_path), no_new_credit_orROM=True, guide_photos=False, full_goal_complete=False))
    print('PASS 433 speeches / 439 final native and directly viewed pages; 15 layout fixes, prose unchanged. Caption/name/stored/gameplay/release gates pending.')
