"""Seal318 directly reviewed final pages,15 wrap improvements andfive native FE repairs."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT

def pages(row):
    value=row['complete_native_English_display'];return value['pages'] if row['kind']=='progressive' else [value]

def main():
    out=ROOT/'final_native_v1.json';approval=ROOT/'offline_display_approval_v1.json'
    assert not out.exists() and not approval.exists()
    doc_path=ROOT/'formatting_v1/formatting_input.json';plan_path=ROOT/'plan_v8_complete_clauses/automatic_plans.json'
    old_path=ROOT/'initial_complete_native_v1.json';new_path=ROOT/'refined_native_v1/compiled_native_pages.json'
    fresh_path=ROOT/'refined_native_v1/fresh/compiled_native_pages.json'
    doc,plan,old,new,fresh=map(load,[doc_path,plan_path,old_path,new_path,fresh_path])
    initial_plan=load(ROOT/'plan_v1/automatic_plans.json');guard_plan=load(ROOT/'plan_v4_FE_guards/automatic_plans.json')
    assert len(doc['records'])==len(plan['records'])==len(new['records'])==310
    assert new['pages']==old['pages']==318 and (len(fresh['records']),fresh['pages'],fresh['fresh_compiled_alignments'])==(15,23,60)
    assert new['fresh_compiled_alignments']==60 and new['reused_compiled_alignments']==1180
    assert new['runtime']==old['runtime']==fresh['runtime'] and new['font_sha256']==old['font_sha256']==fresh['font_sha256']
    assert new['manuscript_sha256']==plan['manuscript_sha256']==digest(doc_path) and new['plan_sha256']==digest(plan_path)
    assert not plan['failures'] and not any(i['severity'] in ['error','warning'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert not old['direct_visual_review_pending'] and fresh['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert fresh['complete_consumption_andpagination_exact']
    seen={(r['id'],r['page'],r['preview_sha256'],r['native_plane_sha256']) for r in old['directly_reviewed_selected_page_receipts']}
    sheet_path=ROOT/'refined_visual_v1/contact_sheet_manifest.json';sheets=load(sheet_path)
    assert sheets['pages']==23 and len(sheets['review_sheets'])==2
    for sheet in sheets['review_sheets']:
        assert digest(sheet['path'])==sheet['sha256']
        seen.update((m['id'],m['page'],m['preview_sha256'],m['native_plane_sha256']) for m in sheet['members'])
    planned={r['id']:r for r in plan['records']};source={r['id']:r for r in doc['records']}
    selected=[]
    for row in new['records']:
        expected=planned[row['id']];original=source[row['id']]
        assert row['compiled_hex']==expected['encoded_hex'] and row['logical_English']==original['english']
        assert row['source_reference']==original['source_reference'] and row['current_reference']==original['current_reference']
        assert len(pages(row))==expected['expected_native_pages'] and len(row['native_alignment']['cases'])==4
        for number,page in enumerate(pages(row),1):
            assert digest(page['preview'])==page['preview_sha256'] and digest(page['native_plane'])==page['native_plane_sha256']
            assert (row['id'],number,page['preview_sha256'],page['native_plane_sha256']) in seen
            selected.append(dict(id=row['id'],page=number,preview=page['preview'],preview_sha256=page['preview_sha256'],
                native_plane_sha256=page['native_plane_sha256']))
    assert len(selected)==318
    names_path=ROOT/'name_planes_v1/native_name_planes.json';names=load(names_path)
    assert names['runtime']==new['runtime'] and (names['actors'],names['distinct_current_strings'])==(26,31)
    assert all(r['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass'] for r in names['planes'])
    for sheet in names['review_sheets']:assert digest(sheet['path'])==sheet['sha256']
    first={r['id']:r for r in initial_plan['records']};guard={r['id']:r for r in guard_plan['records']}
    changes=[];guard_fixes=[]
    for row in plan['records']:
        ident=row['id'];binding=dict(id=ident,source_reference=source[ident]['source_reference'],current_reference=source[ident]['current_reference'])
        if guard[ident]['encoded_hex']!=first[ident]['encoded_hex']:
            guard_fixes.append({**binding,'before_lines':first[ident]['lines'],'after_lines':guard[ident]['lines'],
                'original_native_row_orbounds_failure_preserved':True,'full_prose_unchanged':True})
        if row['encoded_hex']!=guard[ident]['encoded_hex']:
            changes.append({**binding,'before_lines':guard[ident]['lines'],'after_lines':row['lines'],
                'pages_before':guard[ident]['expected_native_pages'],'pages_after':row['expected_native_pages'],
                'whole_prose_andnative_controls_unchanged':True})
    assert len(changes)==15 and len(guard_fixes)==5
    for path in [ROOT/'FE_guard_probe_v1/cases.json',ROOT/'FE_guard_probe_v2/cases.json']:
        probe=load(path);assert probe['runtime']==new['runtime'] and all(not c['rejected'] for c in probe['cases'])
    assert all(c['rejected'] for c in load(ROOT/'FE_original_risk_probe_v1/cases.json')['cases'])
    final=deepcopy(new)
    for key in ['source_owned_target_page_adapter','source_owned_progressive_macro_adapter','FE_factory_calibration']:
        final[key]=old[key]
    final.update(direct_visual_review_pending=False,directly_reviewed_selected_page_receipts=selected,
        review_sheets=sheets['review_sheets'],previous_direct_view_sheets=old['review_sheets'],
        all318_final_pages_directly_viewed_or_exact_visual_dependency_reuse=True,
        selected_alignment_cases=1240,formatting_gates_still_false=True,actual_gameplay=False,new_credit=0)
    save(out,final)
    retentions=load(ROOT/'formatting_v1/preferences_v7_complete_clauses.json')['layout_retentions']
    retentions.append(dict(id='DK4_MES_B51_R0082',reason='Retain two pages after the unchanged131-character one-page trial fails the source/QA contract. The accepted second page carries the full life-stake phrase;no shortening orguard waiver.'))
    save(approval,dict(records=310,complete_exchanges=7,dialogue_revisions=184,dialogue_retentions=126,
        body_records=310,final_body_pages=318,all318_final_pages_directly_viewed_or_exact_visual_reuse=True,
        directly_viewed_initial_pages=282,byte_exact_initial_visual_reuses=36,fresh_refined_pages_directly_viewed=23,
        scoped_names=26,distinct_name_strings=31,all31_name_strings_directly_viewed=True,
        all15_nonASCII_targets_native_checked=True,corrected_mixed_width_letters=3,mixed_width_letter_records=2,
        native_FE_row_repairs=guard_fixes,native_FE_row_repairs_count=5,
        accepted_layout_changes=changes,accepted_layout_changes_count=15,justified_layout_retentions=retentions,
        pages_reclaimed=0,no_prose_shortening_no_font_viewport_orengine_change=True,
        native_FE_commands_added=0,source_utterances_equal_native_commands=True,
        final_plan=str(plan_path),final_plan_sha256=digest(plan_path),final_native=str(out),final_native_sha256=digest(out),
        names=str(names_path),names_sha256=digest(names_path),
        fresh_selected_alignment_cases=60,reused_selected_alignment_cases=1180,
        all_fifth_review_gates_still_false=True,stored_script_allocation_andrepresentative_gameplay_pending=True,
        full_catalogue_UI_andhardware_unvisited=True,no_new_batch_gameplay_orintegration_credit=True,new_credit=0,
        evidence={str(p):digest(p) for p in [doc_path,plan_path,old_path,new_path,fresh_path,sheet_path,names_path,
            ROOT/'initial_visual_findings_v1.json',ROOT/'FE_original_risk_probe_v1/cases.json',Path(__file__)]}))
    print('Approved offline310:318 viewed pages,15 wrap improvements,five FE row repairs,31 name strings;stored/gameplay/release remain.')
if __name__=='__main__':main()
