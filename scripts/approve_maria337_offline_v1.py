"""Seal exact selected body/caption/name displays without storage or gameplay credit."""
from copy import deepcopy
from pathlib import Path
from scripts.meaning_maria337_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    out=ROOT/'offline_display_approval_v1.json'; finalpath=ROOT/'final_native_v1.json'; viewpath=ROOT/'mixed_visual_review_v1.json'
    bodypath=ROOT/'body_visual_review_v1.json'; menupath=ROOT/'menu_native_approved_v1.json'; stylepath=ROOT/'compiled_styles_v1/compiled_style_objects.json'
    assert not any(p.exists() for p in [out,finalpath,viewpath,bodypath,menupath,stylepath.parent])
    paths=dict(manuscript=ROOT/'formatting_v1/formatting_input.json',plan=ROOT/'plan_visual_v5/automatic_plans.json',
        selection=ROOT/'native_final_selection_v1/resume_selection.json',initial=ROOT/'native_pages_v1/compiled_native_pages.json',
        updated=ROOT/'native_visual_pages_v1/compiled_native_pages.json',initial_view=ROOT/'initial_body_visual_review_v1.json',
        updated_view=ROOT/'updated_body_visual_review_v1.json',menu=ROOT/'menu_native_v2/menu_provider_and_planes.json',
        names=ROOT/'name_planes_v1/native_name_planes.json',macros=ROOT/'formatting_v1/native_macro_measurements.json',
        objects=ROOT/'current_objects_v1/current_objects.json')
    d={k:load(p) for k,p in paths.items()}; doc,plan,selection,initial,updated,menu,names=[d[k] for k in ['manuscript','plan','selection','initial','updated','menu','names']]
    assert len(doc['records'])==337 and len(plan['records'])==335 and not plan['failures']
    assert sum(r['expected_native_pages'] for r in plan['records'])==339
    assert not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert selection['native_selection_complete'] and (selection['reused_records'],selection['remaining_records'])==(335,0)
    assert selection['final_plan_sha256']==digest(paths['plan']) and selection['final_manuscript_sha256']==digest(paths['manuscript'])
    assert all(d[k]['runtime']==doc['runtime'] for k in ['initial','updated','initial_view','updated_view','menu','names','macros','objects'])
    assert initial['source_owned_target_page_adapter']==updated['source_owned_target_page_adapter']
    assert initial['source_owned_progressive_macro_adapter']==updated['source_owned_progressive_macro_adapter']==d['macros']['source_owned_progressive_adapter']
    assert initial['fresh_compiled_alignments']==1340 and updated['fresh_compiled_alignments']==32
    assert (names['actors'],names['distinct_current_strings'],names['fresh_native_name_strings'],names['reused_native_name_strings'])==(21,28,13,15)
    assert all(p['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass'] for p in names['planes'])
    assert (menu['native_provider_alignments'],menu['bridged_modal_returns'],menu['complete_English_caption_style_planes'])==(6,18,4)
    assert len(menu['compiler_negatives_rejected'])==7 and menu['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
    assert menu['reviewed_target_has_four_complete_ASCII_caption_style_planes'] and menu['current_font_comparison_not_approved']
    assert [r['text'].strip() for r in menu['exact_corrupt_current_provider_checked_butnot_ASCII_painted']]==['産es','札ecline']
    assert not d['objects']['style_records'] and not d['objects']['style_objects']
    visual_candidates={}
    for key in ['updated_view','initial_view']:
        review=d[key]; assert review['all_native_pages_bound_to_directly_viewed_exact_contact_sheet_tiles']
        for r in review['records']:visual_candidates.setdefault(r['id'],[]).append(r)
    originals={r['id']:r for r in doc['records'] if r['kind']!='typed-choice-label'}; plans={r['id']:r for r in plan['records']}
    selected=[]; bodyviews=[]; inputs=set()
    for binding in selection['reused_native_records']:
        assert digest(binding['receipt'])==binding['receipt_sha256']; receipt=load(binding['receipt']); row=receipt['record']
        ident=row['id']; source=originals[ident]
        assert row['compiled_hex']==binding['compiled_hex']==plans[ident]['encoded_hex'] and row['logical_English']==source['english']
        assert all(row[k]==source[k] for k in ['source_reference','current_reference']) and len(row['native_alignment']['cases'])==4
        assert receipt['four_native_alignment_cases_pass'] and receipt['all_original_native_glyph_pixels_consumption_canaries_bounds_androw_assertions_pass']
        assert digest(receipt['native_run_inputs'])==receipt['native_run_inputs_sha256']; inputs.add(receipt['native_run_inputs'])
        view=next(v for v in visual_candidates[ident] if v['compiled_hex']==row['compiled_hex'])
        display=row['complete_native_English_display']; pages=display['pages'] if row['kind']=='progressive' else [display]
        assert len(view['pages'])==len(pages)==plans[ident]['expected_native_pages']
        for checked,page in zip(view['pages'],pages,strict=True):
            assert checked['native_plane_sha256']==page['native_plane_sha256'] and checked['preview_sha256']==page['preview_sha256']
            assert digest(page['native_plane'])==page['native_plane_sha256'] and digest(page['preview'])==page['preview_sha256']
            assert digest(checked['viewed_sheet'])==checked['viewed_sheet_sha256'] and checked['exact_viewed_pixels_equal']
        if row['kind']=='system-FE':assert display['planned_native_row_comparison']['complete_glyph_row_membership_exact']
        selected.append(row); bodyviews.append(view)
    assert len(selected)==335 and sum(len(r['pages']) for r in bodyviews)==339 and len(inputs)==2
    sheets=d['initial_view']['review_sheets']+d['updated_view']['review_sheets']; assert len(sheets)==39
    save(bodypath,dict(records=bodyviews,body_records=335,body_pages=339,runtime=doc['runtime'],review_sheets=sheets,
        all_final_body_pages_bound_to_directly_viewed_exact_native_pixels=True,selected_plan=str(paths['plan']),selected_plan_sha256=digest(paths['plan']),
        selected_native_receipts=str(paths['selection']),selected_native_receipts_sha256=digest(paths['selection']),
        superseded_eight_layouts_preserved_not_reused_for_changed_pages=True,actual_gameplay=False,new_credit=0))
    mixed=[dict(s,directly_viewed=True) for s in names['review_sheets']]+[dict(menu['review_sheet'],directly_viewed=True)]
    for s in mixed:assert digest(s['path'])==s['sha256']
    save(viewpath,dict(review_sheets=mixed,distinct_name_strings_directly_viewed=28,target_captions_directly_viewed=2,
        all_names_complete_consistent_andwithin_verified_bounds=True,target_captions_complete_centered_andnatural_in_source_exchange=True,
        corrupt_current_caption_font_not_approved=True,actual_headers_andcontroller_pending=True,actual_gameplay=False,new_credit=0))
    final=deepcopy(initial); final.update(records=selected,review_sheets=sheets,manuscript=str(paths['manuscript']),manuscript_sha256=digest(paths['manuscript']),
        plan=str(paths['plan']),plan_sha256=digest(paths['plan']),selected_alignment_cases=1340,reused_compiled_alignments=1308,fresh_compiled_alignments=32,
        initial_native_proof=str(paths['initial']),initial_native_proof_sha256=digest(paths['initial']),updated_native_proof=str(paths['updated']),updated_native_proof_sha256=digest(paths['updated']),
        selected_native_receipt_per_record={r['id']:dict(path=r['receipt'],sha256=r['receipt_sha256']) for r in selection['reused_native_records']},
        aggregation_of_completed_exact_receipts_not_fresh_monolithic_run=True,direct_visual_review_pending=False,
        all339_final_pages_directly_viewed_or_exact_visual_dependency_reuse=True,formatting_gates_still_false=True,actual_gameplay=False,new_credit=0)
    save(finalpath,final)
    choices=[r for r in doc['records'] if r['kind']=='typed-choice-label']; assert [r['source_index'] for r in choices]==[0,1]
    assert {r['block'] for r in choices}=={136} and {r['source_command_offset'] for r in choices}=={356}
    approved=deepcopy(menu); approved.update(offline_visual_approved=True,direct_view_pending=False,original_receipt=str(paths['menu']),original_receipt_sha256=digest(paths['menu']),
        menus=[dict(block=136,source_command_offset=356,current_command_offset=choices[0]['current_reference']['command_offset'],
            source_object_hex=choices[0]['source_choice_object_hex'],current_object_hex=choices[0]['current_choice_object_hex'],target_object_hex=menu['native_choice_object_hex'],record_ids=[r['id'] for r in choices])],
        visual_receipt=str(viewpath),visual_receipt_sha256=digest(viewpath)); save(menupath,approved)
    stylepath.parent.mkdir(); save(stylepath,dict(runtime=doc['runtime'],manuscript=str(paths['manuscript']),manuscript_sha256=digest(paths['manuscript']),
        plan=str(paths['plan']),plan_sha256=digest(paths['plan']),objects=[],physical_alternatives=0,native_target_slot_cases=0,compiler_negatives=[],
        no_source_orcurrent_style_objects_in_this_scope=True,source_alias_equivalence_exact=True,no_empty_native_permutations_executed=True,new_credit=0))
    save(out,dict(source_objects=337,complete_exchanges=12,dialogue_revisions=224,dialogue_retentions=113,physical_body_candidates=335,body_pages=339,
        original_source_FE_panels=6,physical_FE_panels=6,FE_continuation_owners=0,source_styles=0,source_style_objects=0,choice_menus=1,choice_captions=2,
        selected_alignment_cases=1340,all339_final_pages_directly_viewed=True,scoped_names=21,distinct_name_strings=28,fresh_name_planes=13,reused_name_planes=15,
        all_names_andtwo_captions_directly_viewed=True,menu_native_provider_alignments=6,menu_bridged_returns=18,menu_normal_highlight_planes=4,menu_compiler_negatives=7,
        corrupt_current_menu_provider_proved_without_ASCII_font_approval=True,pages_reclaimed=0,tutorial_page_boundary_fixes=4,additional_phrase_wrap_fixes=8,
        mixed_font_Latin_records_corrected=2,mixed_font_I_characters_corrected=3,corrupt_choice_captions_corrected=2,body_name_spellings_reconciled=2,
        final_native_proof=str(finalpath),final_native_proof_sha256=digest(finalpath),names_sha256=digest(paths['names']),
        full_paragraphs_native_controls_substitutions_andlayout_provenance_preserved=True,
        stored_script_allocation_branches_actual_gameplay_andregistration_pending=True,all_fifth_formatting_gates_still_pending=True,
        actual_gameplay=False,new_ROM=False,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [*paths.values(),bodypath,viewpath,finalpath,menupath,stylepath,Path(__file__)]}))
    print('Sealed offline:339 body pages,two repaired captions,28 name strings;327 layouts reused/eight refreshed. Storage/gameplay/release pending.')

if __name__=='__main__':main()
