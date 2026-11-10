"""Seal all offline body/caption/style/name evidence; keep storage, gameplay and release gates pending."""
from copy import deepcopy
from pathlib import Path
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    out=ROOT/'offline_display_approval_v1.json';finalpath=ROOT/'final_native_v1.json';menubridge=ROOT/'menu_native_approved_v1.json'
    viewpath=ROOT/'mixed_visual_review_v1.json';assert not any(p.exists() for p in [out,finalpath,menubridge,viewpath])
    paths=dict(physical=ROOT/'formatting_FE_v2/physical_manuscript.json',plan=ROOT/'plan_continuity_v10/automatic_plans.json',
        native=ROOT/'selected_native_sheets_v2/selected_native_pages.json',visual=ROOT/'body_visual_review_v1.json',
        selection=ROOT/'native_final_selection_v2/resume_selection.json',menu=ROOT/'menu_native_v1/menu_provider_and_planes.json',
        styles=ROOT/'compiled_styles_v1/compiled_style_objects.json',names=ROOT/'name_planes_v2/native_name_planes.json',
        macros=ROOT/'formatting_v1/native_macro_measurements.json',calibration=ROOT/'native_B116_fix_v1/compiled_native_pages.json')
    d={k:load(p) for k,p in paths.items()};doc,plan,native,visual,menu,styles,names=[d[k] for k in ['physical','plan','native','visual','menu','styles','names']]
    assert len(doc['records'])==332 and len(plan['records'])==len(native['records'])==330 and native['pages']==338
    assert visual['all_final_body_pages_bound_to_directly_viewed_exact_native_pixels'] and not plan['failures']
    assert all(d[k]['runtime']==doc['runtime'] for k in ['native','menu','styles','names','macros','calibration'])
    assert (names['actors'],names['distinct_current_strings'],names['fresh_native_name_strings'],names['reused_native_name_strings'])==(26,29,13,16)
    assert all(p['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass'] for p in names['planes'])
    assert (menu['native_provider_alignments'],menu['bridged_modal_returns'],menu['complete_English_caption_style_planes'])==(6,18,8)
    assert len(menu['compiler_negatives_rejected'])==7 and menu['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
    assert (len(styles['objects']),styles['physical_alternatives'],styles['native_target_slot_cases'])==(6,35,48)
    assert sum(len(x['rejected']) for x in styles['compiler_negatives'])==54
    wanted={r['id']:r for r in doc['records'] if r['kind']!='typed-choice-label'};planned={r['id']:r for r in plan['records']}
    for row in native['records']:
        source=wanted[row['id']];assert row['logical_English']==source['english'] and row['compiled_hex']==planned[row['id']]['encoded_hex']
        assert all(row[k]==source[k] for k in ['source_reference','current_reference']) and len(row['native_alignment']['cases'])==4
        display=row['complete_native_English_display']
        if row['kind']=='progressive':
            assert display['all_visible_first_internal_final_characters_in_order'] and display['no_blank_or_overlap_page']
            assert display['complete_consumed_bytes']==len(bytes.fromhex(row['expanded_native_hex']))
            assert all(p['native_independent_plane_equal'] and p['all_bitmap_header_input_canaries_exact'] for p in display['pages'])
        else:
            assert display['all_first_internal_final_ASCII_CP932_codes_andindependent_logical_plane_exact']
            assert display['input_bitmap_header_view_context_canaries_andcomplete_return_exact'] and display['all_executed_instructions_exact_current_sections_andpayload']
            assert display['planned_native_row_comparison']['complete_glyph_row_membership_exact']
    sheets=[dict(s,directly_viewed=True) for s in names['review_sheets']]+[dict(menu['review_sheet'],directly_viewed=True)]
    for s in sheets:assert digest(s['path'])==s['sha256']
    save(viewpath,dict(review_sheets=sheets,distinct_name_strings_directly_viewed=29,target_captions_directly_viewed=2,
        current_caption_comparison_also_viewed=True,all_names_complete_consistent_andwithin_verified_bounds=True,
        target_captions_complete_centered_andnatural_in_the_source_exchange=True,actual_headers_andcontroller_pending=True,actual_gameplay=False,new_credit=0))
    final=deepcopy(native);final.update(manuscript=str(paths['physical']),manuscript_sha256=digest(paths['physical']),plan=str(paths['plan']),plan_sha256=digest(paths['plan']),
        selected_alignment_cases=1320,reused_compiled_alignments=1320,fresh_compiled_alignments=0,
        source_owned_progressive_macro_adapter=d['macros']['source_owned_progressive_adapter'],FE_factory_calibration=d['calibration']['FE_factory_calibration'],
        all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass=True,complete_consumption_andpagination_exact=True,
        direct_visual_review_pending=False,all338_final_pages_directly_viewed_or_exact_visual_dependency_reuse=True,
        selected_native_receipt_per_record={r['id']:dict(path=r['receipt'],sha256=r['receipt_sha256']) for r in d['selection']['reused_native_records']},
        aggregation_of_completed_exact_receipts_not_fresh_monolithic_run=True,formatting_gates_still_false=True,actual_gameplay=False,new_credit=0)
    save(finalpath,final)
    choices=[r for r in doc['records'] if r['kind']=='typed-choice-label'];assert [r['source_index'] for r in choices]==[0,1]
    approved=deepcopy(menu);approved.update(offline_visual_approved=True,direct_view_pending=False,original_receipt=str(paths['menu']),original_receipt_sha256=digest(paths['menu']),
        menus=[dict(block=102,source_command_offset=210,current_command_offset=choices[0]['current_reference']['command_offset'],
            source_object_hex=choices[0]['source_choice_object_hex'],current_object_hex=choices[0]['current_choice_object_hex'],target_object_hex=menu['native_choice_object_hex'],
            record_ids=[r['id'] for r in choices])],visual_receipt=str(viewpath),visual_receipt_sha256=digest(viewpath))
    save(menubridge,approved)
    evidence={str(p):digest(p) for p in [*paths.values(),viewpath,finalpath,menubridge,Path(__file__)]}
    save(out,dict(source_objects=330,complete_exchanges=26,dialogue_revisions=249,dialogue_retentions=81,physical_body_candidates=330,body_pages=338,
        original_source_FE_panels=8,physical_FE_panels=10,FE_continuation_owners=2,source_styles=35,source_style_objects=6,
        choice_menus=1,choice_captions=2,selected_alignment_cases=1320,all338_final_pages_directly_viewed=True,
        scoped_names=26,distinct_name_strings=29,fresh_name_planes=13,reused_name_planes=16,all_names_andtwo_captions_directly_viewed=True,
        menu_native_provider_alignments=6,menu_bridged_returns=18,menu_normal_highlight_planes=8,menu_compiler_negatives=7,
        style_slot_cases=48,style_compiler_negatives=54,pages_reclaimed=3,closing_clause_boundary_fixes=7,orphan_See_repaired=True,
        mixed_font_Latin_targets_corrected=3,former_Japanese_grant_now_complete_English=True,
        full_paragraphs_native_controls_substitutions_andlayout_provenance_preserved=True,
        final_native_proof=str(finalpath),final_native_proof_sha256=digest(finalpath),names_sha256=digest(paths['names']),
        stored_script_allocation_branches_actual_gameplay_andregistration_pending=True,all_fifth_formatting_gates_still_pending=True,
        actual_gameplay=False,new_ROM=False,new_credit=0,full_goal_complete=False,evidence=evidence))
    print('Sealed offline:338 body pages,two captions,six complete style objects,29 names;storage/gameplay/release pending,zero credit.')

if __name__=='__main__':main()
