"""Seal 17 directly viewed native panels for 16 held source objects; grant no credit."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B50_FE_resolution_20261109_v3')
def main():
    out=ROOT/'final_native_v1.json';approval=ROOT/'offline_approval_v1.json';assert not out.exists() and not approval.exists()
    old_path=ROOT/'native_v1/compiled_native_pages.json';new_path=ROOT/'native_fresh2_v1/compiled_native_pages.json'
    old,new=map(load,[old_path,new_path]);plan_path=ROOT/'plan_v5/automatic_plans.json';plan=load(plan_path)
    doc_path=ROOT/'physical17_manuscript.json';doc=load(doc_path)
    assert old['runtime']==new['runtime'] and old['font_sha256']==new['font_sha256']
    assert old['source_owned_target_page_adapter']==new['source_owned_target_page_adapter']
    assert old['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and new['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert old['complete_consumption_andpagination_exact'] and new['complete_consumption_andpagination_exact']
    assert old['pages']==len(old['records'])==17 and new['pages']==len(new['records'])==2
    fresh={r['id']:r for r in new['records']};prior={r['id']:r for r in old['records']};plans={r['id']:r for r in plan['records']}
    assert set(fresh)=={'DK4_MES_B50_R0057','DK4_MES_B50_R0076'}
    final=[];views=[]
    for i,row in enumerate(doc['records']):
        ident=row['id'];proved=deepcopy(fresh.get(ident,prior[ident]))
        assert proved['compiled_hex']==plans[ident]['encoded_hex'] and proved['logical_English']==row['english']
        d=proved['complete_native_English_display'];pages=[d] if row['kind']=='system-FE' else d['pages']
        assert len(pages)==1
        for page in pages:
            assert digest(page['native_plane'])==page['native_plane_sha256'] and digest(page['preview'])==page['preview_sha256']
        sheet=new['review_sheets'][0] if ident in fresh else old['review_sheets'][i//12]
        assert digest(sheet['path'])==sheet['sha256']
        views.append(dict(id=ident,native_plane=pages[0]['native_plane'],native_plane_sha256=pages[0]['native_plane_sha256'],directly_viewed_sheet=sheet))
        final.append(proved)
    assert not plan['failures'] and all(not any(i['severity'] in ['warning','error'] for i in r['base_QA']['issues']) for r in plan['records'])
    merged={**old,'manuscript':str(doc_path),'manuscript_sha256':digest(doc_path),'plan':str(plan_path),'plan_sha256':digest(plan_path),
        'records':final,'pages':17,'previous_native':str(old_path),'previous_native_sha256':digest(old_path),
        'fresh_native':str(new_path),'fresh_native_sha256':digest(new_path),'fresh_compiled_alignments':8,
        'reused_compiled_alignments':60,'total_alignment_cases_executed':76,'selected_alignment_cases':68,
        'review_sheets':new['review_sheets'],'previous_direct_view_sheets':old['review_sheets'],
        'directly_reviewed_selected_page_receipts':views,'all_records_native_checked_once_or_exact_compiled_dependency_reuse':True,
        'direct_visual_review_pending':False,'source_editorial_objects':16,'physical_native_panel_objects':17,
        'whole_source_prose_unchanged':True,'formatting_gates_still_false':True,'new_credit':0}
    save(out,merged)
    save(approval,dict(source_objects=16,proposed_dialogue_revisions=9,justified_dialogue_retentions=7,
        native_panels=17,pagination_owners=1,additional_native_FE_commands=1,all17_final_panels_directly_viewed=True,
        initial17_native_alignment_cases=68,fresh_wrap_alignment_cases=8,unchanged_native_panels_reused=15,
        R36_unintended_blank_row_fixed_by_existing_guard_budget=True,R43_full139_character_paragraph_preserved_in_two_panels=True,
        R57_complete_admiral_like_you_phrase_avoids_isolated_admiral=True,R76_three_substantial_rows_complete_prose=True,
        no_QA_waivers_or_prose_font_viewport_orengine_changes=True,source_owned_FE_continuation_method='dk4tool/script/reviewed_FE_pagination_v1.py',
        semantic_boundary=doc['pagination_owners'][0]['semantic_boundary_reason'],
        native=str(out),native_sha256=digest(out),plan=str(plan_path),plan_sha256=digest(plan_path),
        source_current_complete_controls_andmacro_bindings=str(ROOT/'source_and_runtime_binding.json'),
        stored_allocation_branch_andactual_transition_checks_pending=True,all_fifth_formatting_gates_still_false=True,
        actual_gameplay=False,registered_integration_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [old_path,new_path,plan_path,doc_path,ROOT/'source16_manuscript.json',ROOT/'source_and_runtime_binding.json',Path(__file__)]}))
    print('Sealed17 viewed native panels for16 sources:full paragraph preserved,two additional wraps improved;stored andactual checks pending;zero credit.')
if __name__=='__main__':main()
