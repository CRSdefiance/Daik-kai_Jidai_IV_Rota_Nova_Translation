"""Approve 256 exact native body pages: ten refinements and245 exact reuses."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

DOC = Path('translations/rafael_B85_B100_contextual_editorial_manuscript_v2.json')
PLAN = Path('work/analysis/Rafael261_sparse_row_refinement_v4_20261105/full_plan/automatic_plans.json')
BASE = Path('work/analysis/Rafael261_native_v1_20261105/compiled_native_pages.json')
DELTA = Path('work/analysis/Rafael261_native_delta_v3_20261105/compiled_native_pages.json')
FRESH = Path('work/analysis/Rafael261_native_sparse_delta_v4_20261105/compiled_native_pages.json')
OUT = Path('work/analysis/Rafael261_native_final_v4_20261105')

if __name__ == '__main__':
    assert not OUT.exists()
    doc, plan, base, delta, fresh = map(load, [DOC, PLAN, BASE, DELTA, FRESH])
    assert plan['manuscript_sha256'] == sha(DOC.read_bytes()) and not plan['failures']
    assert base['runtime'] == delta['runtime'] == fresh['runtime']
    assert base['font_sha256'] == delta['font_sha256'] == fresh['font_sha256']
    assert (len(base['records']), base['pages'], len(delta['records']), delta['pages'], len(fresh['records'])) == (255, 256, 11, 12, 1)
    assert load(BASE.parent/'direct_visual_review_with_findings.json')['all256_native_pages_andall_readable_sheets_directly_viewed']
    for proof in [base, delta, fresh]:
        assert proof['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
        assert proof['complete_consumption_andpagination_exact']
        for sheet in proof['review_sheets']:
            assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    dictionaries = [{r['id']: r for r in proof['records']} for proof in [fresh, delta, base]]
    records, origins = [], {}
    counts = {str(p): 0 for p in [BASE, DELTA, FRESH]}
    for planned in plan['records']:
        ident = planned['id']
        matches = [(rows.get(ident), p) for rows, p in zip(dictionaries, [FRESH, DELTA, BASE], strict=True)
            if ident in rows and rows[ident]['compiled_hex'] == planned['encoded_hex']]
        assert matches, ident
        row, origin = matches[0]
        assert row['logical_English'] == planned['logical_English']
        assert len(row['native_alignment']['cases']) == 4
        assert all(c['output_hex'] == row['expanded_native_hex'] for c in row['native_alignment']['cases'])
        display = row['complete_native_English_display']
        if row['kind'] == 'system-FE':
            assert display['all_first_internal_final_ASCII_CP932_codes_andindependent_logical_plane_exact']
            assert display['planned_native_row_comparison']['complete_glyph_row_membership_exact']
            pages = [display]
        else:
            assert display['all_visible_first_internal_final_characters_in_order'] and display['no_blank_or_overlap_page']
            assert display['complete_consumed_bytes'] == len(bytes.fromhex(row['expanded_native_hex']))
            pages = display['pages']
        assert len(pages) == planned['expected_native_pages']
        for page in pages:
            assert sha(Path(page['native_plane']).read_bytes()) == page['native_plane_sha256']
            assert sha(Path(page['preview']).read_bytes()) == page['preview_sha256']
        counts[str(origin)] += 1
        records.append(deepcopy(row))
        origins[ident] = dict(native_proof=str(origin), native_proof_sha256=sha(origin.read_bytes()),
            exact_compiled_bytes_logical_prose_andcomplete_native_pages=True, direct_visual_review_reused_for_exact_page=True)
    assert counts == {str(BASE): 245, str(DELTA): 9, str(FRESH): 1}
    assert len(records) == 255 and sum(r['expected_native_pages'] for r in plan['records']) == 256
    OUT.mkdir()
    approval = OUT/'direct_visual_approval.json'
    save(approval, dict(base_native=str(BASE), base_native_sha256=sha(BASE.read_bytes()),
        all256_base_pages_andall_readable_sheets_directly_viewed=True,
        delta_native=str(DELTA), delta_native_sha256=sha(DELTA.read_bytes()), all12_delta_pages_andall_six_sheets_directly_viewed=True,
        fresh_native=str(FRESH), fresh_native_sha256=sha(FRESH.read_bytes()), one_fresh_page_andits_sheet_directly_viewed=True,
        final_approved_refinements=10, exact_original_retentions=245, final_approved_pages=256,
        original_B90_R23_retained_toavoid_sparse_middle_row=True,
        B86_R272_rejected_sparse_Just_opening_replaced_by_complete_Just_thinking_about_it_phrase=True,
        final_sentence_kept_together_across_B86_R75_page_turn=True,
        all_prose_words_controls_macros_andnative_geometry_preserved=True, offline_only_not_gameplay=True, new_credit=0))
    merged = deepcopy(base)
    merged.update(manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), plan=str(PLAN), plan_sha256=sha(PLAN.read_bytes()),
        records=records, origins=origins, pages=256, final_native_origins=counts,
        fresh_final_layout_records=10, exact_reused_records=245, all256_complete_pages_directly_viewed=True,
        direct_visual_review_pending=False, all255_body_layouts_approved=True, full261_object_batch_display_complete=False,
        typed_choice_labels_separately_pending=6, stored_actual_names_andregistered_integration_pending=True,
        formatting_gates_still_false=True, actual_gameplay=False, new_credit=0,
        evidence={str(p): sha(p.read_bytes()) for p in [DOC, PLAN, BASE, DELTA, FRESH, approval, Path(__file__)]})
    save(OUT/'compiled_native_pages.json', merged)
    print('255 speeches/256 complete native andviewed pages approved:10 layout refinements,245 exact original reuses. Six choices/stored/actual/release pending.')
