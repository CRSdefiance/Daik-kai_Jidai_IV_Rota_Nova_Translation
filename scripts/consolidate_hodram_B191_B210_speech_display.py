"""Join exact complete record proofs and directly viewed speech/menu sheets without replay."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B191_B210_formatting_20261104')
DOC = ROOT / 'formatting_input.json'
PLAN = ROOT / 'guard_and_opening_v4/automatic_plans.json'
INITIAL = ROOT / 'initial/automatic_plans.json'
REUSED = Path('work/analysis/Hodram_B191_B210_native_resume_inputs_20261104/287_exact_record_proofs_reused.json')
FRESH = Path('work/analysis/Hodram_B191_B210_native_20261104/remaining65/compiled_native_pages.json')
MENUS = Path('work/analysis/Hodram_B191_B210_menus_20261104/complete_choice_objects.json')


if __name__ == '__main__':
    output = ROOT / 'speech_display_approved_20261104'
    assert not output.exists()
    doc, plans, initial, reused, fresh, menus = map(load, [DOC, PLAN, INITIAL, REUSED, FRESH, MENUS])
    assert fresh['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert fresh['complete_consumption_andpagination_exact'] and len(fresh['records']) == 65
    assert len(reused['records']) == 287 and len(reused['receipts']) == 17
    assert all(sha(Path(r['path']).read_bytes()) == r['sha256'] for r in reused['receipts'])
    native_by = {r['id']: r['native_record'] for r in reused['records']}
    native_by.update({r['id']: r for r in fresh['records']})
    plan_by = {r['id']: r for r in plans['records']}
    initial_by = {r['id']: r for r in initial['records']}
    speech = [r for r in doc['records'] if r['kind'] != 'typed-choice-label']
    assert len(speech) == len(native_by) == len(plan_by) == 352
    assert {r['id'] for r in speech} == set(native_by) == set(plan_by)
    changed = [r['id'] for r in speech if plan_by[r['id']]['encoded_hex'] != initial_by[r['id']]['encoded_hex']]
    assert set(changed) == {'DK4_MES_B200_R0074', 'DK4_MES_B201_R0074', 'DK4_MES_B208_R0065', 'DK4_MES_B210_R0070'}
    pages = alignments = 0
    for row in speech:
        plan, native = plan_by[row['id']], native_by[row['id']]
        assert plan['encoded_hex'] == native['compiled_hex'] and plan['logical_English'] == native['logical_English'] == row['english']
        assert native['source_reference'] == row['source_reference'] and native['current_reference'] == row['current_reference']
        assert not any(i['severity'] in ['warning', 'error'] for i in plan['base_QA']['issues'])
        assert len(native['native_alignment']['cases']) == 4
        assert all(c['output_hex'] == native['expanded_native_hex'] for c in native['native_alignment']['cases'])
        alignments += 4
        display = native['complete_native_English_display']
        if row['kind'] == 'system-FE':
            assert display['planned_native_row_comparison']['complete_glyph_row_membership_exact']
            assert display['all_first_internal_final_ASCII_CP932_codes_andindependent_logical_plane_exact']
            samples = [display]
        else:
            assert display['complete_consumed_bytes'] == len(bytes.fromhex(native['expanded_native_hex']))
            samples = display['pages']
        assert len(samples) == plan['expected_native_pages']
        for sample in samples:
            assert sha(Path(sample['native_plane']).read_bytes()) == sample['native_plane_sha256']
            assert sha(Path(sample['preview']).read_bytes()) == sample['preview_sha256']
        pages += len(samples)
    assert pages == 355 and alignments == 1408
    earlier = Path('work/analysis/Hodram_B191_B210_native_20261104/initial_v2')
    earlier_sheets = [dict(path=str(p), sha256=sha(p.read_bytes()), directly_viewed=True,
        includes_one_superseded_B201_R74_page=p.name == 'B201_part2.png') for p in sorted(earlier.glob('B*_part*.png'))]
    assert len(earlier_sheets) == 32
    final_sheets = [dict(**s, directly_viewed=True) for s in fresh['review_sheets']]
    assert len(final_sheets) == 8
    for sheet in final_sheets:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    menu_sheets = {}
    for obj in menus['objects']:
        assert sha(Path(obj['receipt']).read_bytes()) == obj['receipt_sha256']
        assert load(obj['receipt'])['runtime'] == fresh['runtime']
        assert sha(Path(obj['compiled_path']).read_bytes()) == obj['compiled_sha256']
        for sheet in obj['review_sheets']:
            assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
            menu_sheets[sheet['path']] = dict(**sheet, directly_viewed=True)
    assert len(menu_sheets) == 4 and menus['physical_caption_records'] == 21
    output.mkdir()
    final_plan = deepcopy(plans)
    final_plan.update(actual_layout_corrections=changed, no_prose_changed=True, direct_visual_review_pending=False)
    plan_path = output / 'all352_compiled_plans.json'
    save(plan_path, final_plan)
    final_native = deepcopy(fresh)
    final_native.update(manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), plan=str(plan_path), plan_sha256=sha(plan_path.read_bytes()),
        records=[native_by[r['id']] for r in speech], pages=355, fresh_compiled_alignments_in_final_record_set=1408,
        exact_prior_complete_record_proofs_reused=287, final_resume_records_fresh=65,
        review_sheets=earlier_sheets + final_sheets, direct_visual_review_pending=False,
        excluded_typed_choice_IDs_separately_pending=[r['id'] for r in doc['records'] if r['kind'] == 'typed-choice-label'],
        earlier_complete_record_receipts_reused=str(REUSED), earlier_complete_record_receipts_reused_sha256=sha(REUSED.read_bytes()),
        all355_final_pages_directly_viewed=True, formatting_gates_still_false=True,
        name_stored_gameplay_andregistered_release_still_pending=True,
        evidence={str(p): sha(p.read_bytes()) for p in [DOC, PLAN, INITIAL, REUSED, FRESH, MENUS, Path(__file__)]})
    native_path = output / 'all352_native_pages.json'
    save(native_path, final_native)
    save(output / 'visual_approval.json', dict(native=str(native_path), native_sha256=sha(native_path.read_bytes()),
        final_pages=355, speech_objects=352, speech_review_sheets=earlier_sheets + final_sheets,
        initial_andreplacement_page_images_viewed=356, final_speech_pages_visually_approved=True,
        one_old_B201_R74_image_superseded_not_final=True, menu_review_sheets=list(menu_sheets.values()),
        all21_caption_visual_checks_pass=True, distinct_native_menu_objects=4, exact_repeated_menus_reused=6,
        menu_native_receipt=str(MENUS), menu_native_receipt_sha256=sha(MENUS.read_bytes()),
        layout_corrections=changed, FE_guard_fix=1, page_phrase_fixes=2, premature_opening_fix=1,
        no_prose_shortening_authored_breaks_waived_QA_font_viewport_orengine_changes=True,
        current_glyph_cases=['ASCII I in Istanbul', 'ASCII I in Ian', 'ASCII 50000 digits', 'full Jam Jack Ludwyan signature'],
        representative_actual_gameplay_andscoped_name_display_still_pending=True,
        actual_gameplay=False, new_credit=0, guide_photos=False))
    print('All 352 speeches/355 final pages and 21 captions visually approved; four layout fixes; no waived QA or prose changes. Stored/name/gameplay/release pending.')
