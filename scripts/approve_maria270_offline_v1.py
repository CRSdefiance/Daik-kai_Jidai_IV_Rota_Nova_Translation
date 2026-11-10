"""Select every directly viewed final native page, retaining the better original sparse lead-in."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B37_B50_clean_20261109')
SCOPE=ROOT/'complete_B37_B49_projection_v1'

def page_list(row):
    result=row['complete_native_English_display']
    return result['pages'] if row['kind']=='progressive' else [result]

def main():
    approval=ROOT/'offline270_display_approval_v1.json';out=ROOT/'final270_native_v1';plan_out=ROOT/'final270_plan_v1'
    assert not any(p.exists() for p in [approval,out,plan_out])
    doc_path=SCOPE/'formatting_input.json';initial_path=SCOPE/'initial_native_qualified.json'
    refined_path=ROOT/'refined270_native_v1/compiled_native_pages.json'
    fresh_path=ROOT/'refined270_native_v1/fresh/compiled_native_pages.json'
    plan_path=SCOPE/'automatic_plans.json';initial_plan_path=SCOPE/'initial_selected_plans.json'
    doc,initial,refined,fresh,plan,old_plan=map(load,[doc_path,initial_path,refined_path,fresh_path,plan_path,initial_plan_path])
    assert len(doc['records'])==270 and len(refined['records'])==len(initial['records'])==266
    assert refined['pages']==272 and fresh['pages']==32 and len(fresh['records'])==27
    assert initial['runtime']==refined['runtime']==fresh['runtime']
    assert initial['font_sha256']==refined['font_sha256']==fresh['font_sha256']
    assert refined['manuscript_sha256']==plan['manuscript_sha256']==digest(doc_path)
    original={r['id']:r for r in initial['records']};revised={r['id']:r for r in refined['records']}
    prior_plans={r['id']:r for r in old_plan['records']}
    retain='DK4_MES_B48_R0083'
    assert retain in refined['changed_layout_ids']
    assert prior_plans[retain]['lines'][0]=='I had no idea'
    trial=next(r for r in plan['records'] if r['id']==retain)
    assert trial['lines'][0]=='I had no'
    final_plan=deepcopy(plan);final_plan['records']=[deepcopy(prior_plans[r['id']] if r['id']==retain else r) for r in plan['records']]
    final_plan.update(layout_selection_only_no_prose_orcontrol_changes=True,
        retained_initial_plan_ids=[retain],initial_plan=str(initial_plan_path),initial_plan_sha256=digest(initial_plan_path),
        refined_parent_plan=str(plan_path),refined_parent_plan_sha256=digest(plan_path),failures=[])
    all_seen={};leaves={}
    for receipt,path in [(initial,initial_path),(fresh,fresh_path)]:
        for row in receipt['records']:
            leaves[(row['id'],row['compiled_hex'])]=(row,path)
            for number,page in enumerate(page_list(row),1):
                assert digest(page['preview'])==page['preview_sha256'] and digest(page['native_plane'])==page['native_plane_sha256']
                all_seen[(row['id'],number,page['preview_sha256'],page['native_plane_sha256'])]=str(path)
    selected=[];rows=[];comparisons=[]
    source={r['id']:r for r in doc['records']}
    for p in final_plan['records']:
        row,path=leaves[(p['id'],p['encoded_hex'])]
        assert row['logical_English']==source[p['id']]['english']
        assert row['source_reference']==source[p['id']]['source_reference'] and row['current_reference']==source[p['id']]['current_reference']
        assert len(page_list(row))==p['expected_native_pages']
        for number,page in enumerate(page_list(row),1):
            assert (row['id'],number,page['preview_sha256'],page['native_plane_sha256']) in all_seen
            selected.append(dict(id=row['id'],page=number,preview=page['preview'],preview_sha256=page['preview_sha256'],
                native_plane_sha256=page['native_plane_sha256'],native_receipt=str(path),native_receipt_sha256=digest(path)))
        rows.append(deepcopy(row))
        if p['encoded_hex']!=prior_plans[p['id']]['encoded_hex']:
            comparisons.append(dict(id=p['id'],source_reference=source[p['id']]['source_reference'],
                current_reference=source[p['id']]['current_reference'],before_lines=prior_plans[p['id']]['lines'],
                after_lines=p['lines'],pages_before=prior_plans[p['id']]['expected_native_pages'],pages_after=p['expected_native_pages'],
                prose_andnative_tokens_unchanged=True))
    assert len(rows)==266 and len(selected)==272 and len(comparisons)==26
    assert sum(r['pages_before']-r['pages_after'] for r in comparisons)==4
    names_path=ROOT/'name_planes_v1/native_name_planes.json';menus_path=ROOT/'menu_planes_v1/group_verification.json'
    names,menus=map(load,[names_path,menus_path])
    assert names['runtime']==initial['runtime'] and (names['actors'],names['distinct_current_strings'])==(28,42)
    assert all(p['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass'] for p in names['planes'])
    assert menus['menus']==2 and menus['captions']==4 and menus['source_current_target_VM_alignments']==12
    assert menus['bridged_modal_returns']==36 and menus['compiler_negative_cases_rejected']==14
    assert menus['all_reviewed_captions_normal_andhighlight_complete_glyphs_centering_bounds_guards_pass']
    for item in menus['objects']:
        assert digest(item['receipt'])==item['receipt_sha256'] and digest(item['review_sheet']['path'])==item['review_sheet']['sha256']
    sheets=load(ROOT/'refined270_native_v1/global_review_v1/contact_sheet_manifest.json')['review_sheets']
    assert sum(s['pages'] for s in sheets)==32
    for sheet in [*sheets,*names['review_sheets']]:assert digest(sheet['path'])==sheet['sha256']
    plan_out.mkdir();plan_final_path=plan_out/'automatic_plans.json';save(plan_final_path,final_plan)
    out.mkdir();native_final_path=out/'compiled_native_pages.json'
    save(native_final_path,dict(manuscript=str(doc_path),manuscript_sha256=digest(doc_path),
        plan=str(plan_final_path),plan_sha256=digest(plan_final_path),runtime=initial['runtime'],font_sha256=initial['font_sha256'],
        records=rows,pages=272,all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass=True,
        complete_consumption_andpagination_exact=True,all_records_native_checked_once_or_exact_compiled_dependency_reuse=True,
        previous_native=str(initial_path),previous_native_sha256=digest(initial_path),fresh_native=str(fresh_path),fresh_native_sha256=digest(fresh_path),
        fresh_compiled_alignments=108,reused_compiled_alignments=960,selected_changed_records=26,selected_reused_records=240,
        rejected_new_layout_retained_as_evidence=retain,review_sheets=sheets,previous_direct_view_sheets=initial['review_sheets'],
        directly_reviewed_selected_page_receipts=selected,direct_visual_review_pending=False,formatting_gates_still_false=True,
        actual_gameplay=False,stored_andrepresentative_checks_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [doc_path,initial_path,refined_path,fresh_path,plan_path,initial_plan_path,Path(__file__)]}))
    retentions=load(ROOT/'layout_candidate_selection_v1.json')['layout_retentions']
    retentions.append(dict(id=retain,reason='Retain the original I had no idea lead-in: the proposed forced pair made it the sparser I had no. Both are native-safe; the original best conveys Rafael’s stunned compliment without a new authored break.'))
    save(approval,dict(records=270,complete_exchanges=13,dialogue_revisions=161,dialogue_retentions=109,
        body_records=266,final_body_pages=272,all272_selected_body_pages_directly_viewed=True,
        all42_name_strings_andboth_menu_sheets_directly_viewed=True,
        glyph_target_records=16,no_global_font_orname_catalogue_UI_approval=True,
        accepted_layout_changes=comparisons,accepted_layout_changes_count=26,layout_retentions=retentions,
        pages_reclaimed_without_shortening_prose=4,new_prose_revisions_from_layout_work=0,
        final_plan=str(plan_final_path),final_plan_sha256=digest(plan_final_path),final_native=str(native_final_path),final_native_sha256=digest(native_final_path),
        names=str(names_path),names_sha256=digest(names_path),menus=str(menus_path),menus_sha256=digest(menus_path),
        all_formatted_body_macro_alignments_checked=True,stored_script_allocation_andrepresentative_gameplay_pending=True,
        all_fifth_review_gates_still_false=True,withheld_complete_exchange=50,withheld_records=16,
        B50_full_source_prose_andnative_failure_preserved=True,no_ROM_changes_ornew_completion_credit=True,new_credit=0,
        evidence={str(p):digest(p) for p in [doc_path,initial_path,fresh_path,names_path,menus_path,Path(__file__)]}))
    print('Approvedoffline270:266 bodies/272 viewed pages,26 wrap improvements/six retentions,four pages reclaimed;28 names/42 strings/four captions. Stored/gameplay/release pending.')

if __name__=='__main__':main()
