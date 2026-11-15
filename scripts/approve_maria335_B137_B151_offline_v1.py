"""Seal all333 exact body displays and scoped captions/names; no gameplay credit."""
from copy import deepcopy
from pathlib import Path
from collections import Counter
from scripts.meaning_maria335_B137_B151_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    output=ROOT/'offline_display_approval_v1.json'
    finalpath=ROOT/'final_native_v1.json'
    bodypath=ROOT/'body_visual_review_v1.json'
    mixedpath=ROOT/'mixed_visual_review_v1.json'
    menupath=ROOT/'menu_native_approved_v1.json'
    stylepath=ROOT/'compiled_styles_v1/compiled_style_objects.json'
    assert not any(p.exists() for p in [output,finalpath,bodypath,mixedpath,menupath,stylepath.parent])
    paths=dict(manuscript=ROOT/'formatting_v1/formatting_input.json',plan=ROOT/'plan_native_v4/automatic_plans.json',
        selection=ROOT/'native_final_selection_v1/resume_selection.json',latest=ROOT/'native_resume_pages_v2/compiled_native_pages.json',
        menu=ROOT/'menu_native_v1/menu_provider_and_planes.json',names=ROOT/'name_planes_v1/native_name_planes.json',
        macros=ROOT/'formatting_v1/native_macro_measurements.json',objects=ROOT/'current_objects_v1/current_objects.json')
    d={k:load(p) for k,p in paths.items()}
    doc,plan,selection,latest,menu,names,macros,objects=[d[k] for k in paths]
    assert (len(doc['records']),len(plan['records']),sum(r['expected_native_pages'] for r in plan['records']))==(335,333,333)
    assert doc['blocks']==list(range(137,152)) and not plan['failures']
    assert not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert selection['native_selection_complete'] and (selection['reused_records'],selection['remaining_records'])==(333,0)
    assert selection['final_plan_sha256']==digest(paths['plan']) and selection['final_manuscript_sha256']==digest(paths['manuscript'])
    assert all(d[k]['runtime']==doc['runtime'] for k in ['latest','menu','names','macros','objects'])
    assert latest['source_owned_progressive_macro_adapter']==macros['source_owned_progressive_adapter']
    assert latest['fresh_compiled_alignments']==332
    assert (names['actors'],names['distinct_current_strings'],names['fresh_native_name_strings'],names['reused_native_name_strings'])==(26,30,19,11)
    assert len(names['planes'])==30 and all(p['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass'] for p in names['planes'])
    assert (menu['native_provider_alignments'],menu['bridged_modal_returns'],menu['complete_English_caption_style_planes'])==(6,18,6)
    assert menu['current_valid_ASCII_option_normal_highlight_planes']==2
    assert menu['reviewed_target_has_four_complete_ASCII_caption_style_planes'] and menu['current_font_comparison_not_approved']
    assert len(menu['compiler_negatives_rejected'])==7 and menu['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
    assert len(menu['exact_corrupt_current_provider_checked_butnot_ASCII_painted'])==1
    assert menu['exact_corrupt_current_provider_checked_butnot_ASCII_painted'][0]['text'].strip()=='丑o'
    assert not objects['style_records'] and not objects['style_objects']
    visualpaths=[ROOT/name for name in ['initial_viewed52_visual_v1.json','initial_B139_46_visual_v1.json',
        'resumed_v1_141_visual_v1.json','resumed_v1_partial145_visual_v1.json','resumed_v2_83_visual_v1.json']]
    candidates={};sheets=[]
    for path in visualpaths:
        visual=load(path)
        assert visual['runtime']==doc['runtime'] and visual['font_sha256']==latest['font_sha256']
        assert visual['all_native_pages_bound_to_directly_viewed_exact_contact_sheet_tiles']
        assert digest(visual['native_proof'])==visual['native_proof_sha256']
        for row in visual['records']:candidates.setdefault(row['id'],[]).append(row)
        sheets.extend(visual['review_sheets'])
    originals={r['id']:r for r in doc['records'] if r['kind']!='typed-choice-label'}
    plans={r['id']:r for r in plan['records']}
    selected=[];bodyviews=[];runs={};used=Counter()
    for binding in selection['reused_native_records']:
        assert digest(binding['receipt'])==binding['receipt_sha256']
        proof=load(binding['receipt']);row=proof['record'];ident=row['id'];original=originals[ident]
        assert row['compiled_hex']==binding['compiled_hex']==plans[ident]['encoded_hex'] and row['logical_English']==original['english']
        assert all(row[k]==original[k] for k in ['source_reference','current_reference'])
        assert proof['four_native_alignment_cases_pass'] and proof['all_original_native_glyph_pixels_consumption_canaries_bounds_androw_assertions_pass']
        assert len(row['native_alignment']['cases'])==4
        runpath=proof['native_run_inputs'];assert digest(runpath)==proof['native_run_inputs_sha256']
        if runpath not in runs:
            run=load(runpath);runs[runpath]=run
            assert run['runtime']==doc['runtime'] and run['font_sha256']==latest['font_sha256'] and run['all_v1_native_assertions_preserved']
            assert run['macro_proof_sha256']==digest(paths['macros'])
            for field in ['source_owned_target_page_adapter','source_owned_progressive_macro_adapter']:
                assert run[field]==latest[field]
        used[runpath]+=1
        view=next(v for v in candidates[ident] if v['compiled_hex']==row['compiled_hex'])
        display=row['complete_native_English_display'];pages=display['pages'] if row['kind']=='progressive' else [display]
        assert len(view['pages'])==len(pages)==plans[ident]['expected_native_pages']==1
        for checked,page in zip(view['pages'],pages,strict=True):
            for field in ['native_plane','preview']:
                assert checked[field+'_sha256']==page[field+'_sha256']==digest(page[field])
            assert digest(checked['viewed_sheet'])==checked['viewed_sheet_sha256'] and checked['exact_viewed_pixels_equal']
        if row['kind']=='system-FE':assert display['planned_native_row_comparison']['complete_glyph_row_membership_exact']
        selected.append(row);bodyviews.append(view)
    assert len(selected)==len({r['id'] for r in selected})==333 and len(runs)==3
    assert sorted(used.values())==[83,95,155]
    assert Counter(r['kind'] for r in selected)=={'progressive':315,'system-FE':18}
    save(bodypath,dict(records=bodyviews,body_records=333,body_pages=333,runtime=doc['runtime'],review_sheets=sheets,
        all_final_body_pages_bound_to_directly_viewed_exact_native_pixels=True,selected_plan=str(paths['plan']),selected_plan_sha256=digest(paths['plan']),
        superseded_four_complete_receipts_preserved_not_reused_for_changed_pages=True,ordinary_soft_wraps_reviewed_in_complete_exchanges=True,
        ordinary_title_soft_wraps_retained_when_readable_on_consecutive_rows=True,actual_gameplay=False,new_credit=0))
    mixed=[dict(s,directly_viewed=True) for s in names['review_sheets']]+[dict(menu['review_sheet'],directly_viewed=True)]
    for sheet in mixed:assert digest(sheet['path'])==sheet['sha256']
    save(mixedpath,dict(review_sheets=mixed,distinct_name_strings_directly_viewed=30,target_captions_directly_viewed=2,
        all_names_complete_consistent_andwithin_verified_bounds=True,target_captions_complete_centered_andnatural_in_source_exchange=True,
        two_valid_current_ASCII_caption_planes_checked=True,corrupt_current_caption_font_not_approved=True,
        actual_headers_andcontroller_pending=True,actual_gameplay=False,new_credit=0))
    final=deepcopy(latest)
    final.update(records=selected,review_sheets=sheets,pages=333,manuscript=str(paths['manuscript']),manuscript_sha256=digest(paths['manuscript']),
        plan=str(paths['plan']),plan_sha256=digest(paths['plan']),selected_alignment_cases=1332,fresh_compiled_alignments=1332,
        selected_native_receipt_per_record={r['id']:dict(path=r['receipt'],sha256=r['receipt_sha256']) for r in selection['reused_native_records']},
        aggregation_of_completed_exact_receipts_not_fresh_monolithic_run=True,selected_records_by_run=dict(used),
        completed_executed_alignment_cases_including_superseded=1348,superseded_completed_alignment_cases_not_selected=16,
        failed_partial_cases_not_credited=True,direct_visual_review_pending=False,all333_final_pages_directly_viewed_or_exact_visual_dependency_reuse=True,
        formatting_gates_still_false=True,actual_gameplay=False,new_credit=0)
    save(finalpath,final)
    choices=[r for r in doc['records'] if r['kind']=='typed-choice-label']
    assert [r['source_index'] for r in choices]==[0,1] and {r['block'] for r in choices}=={138} and {r['source_command_offset'] for r in choices}=={1274}
    approved=deepcopy(menu)
    approved.update(offline_visual_approved=True,direct_view_pending=False,original_receipt=str(paths['menu']),original_receipt_sha256=digest(paths['menu']),
        menus=[dict(block=138,source_command_offset=1274,current_command_offset=choices[0]['current_reference']['command_offset'],
            source_object_hex=choices[0]['source_choice_object_hex'],current_object_hex=choices[0]['current_choice_object_hex'],
            target_object_hex=menu['native_choice_object_hex'],record_ids=[r['id'] for r in choices])],visual_receipt=str(mixedpath),visual_receipt_sha256=digest(mixedpath))
    save(menupath,approved)
    stylepath.parent.mkdir()
    save(stylepath,dict(runtime=doc['runtime'],manuscript=str(paths['manuscript']),manuscript_sha256=digest(paths['manuscript']),
        plan=str(paths['plan']),plan_sha256=digest(paths['plan']),objects=[],physical_alternatives=0,native_target_slot_cases=0,compiler_negatives=[],
        no_source_orcurrent_style_objects_in_this_scope=True,source_alias_equivalence_exact=True,no_empty_native_permutations_executed=True,new_credit=0))
    save(output,dict(source_objects=335,complete_exchanges=15,dialogue_revisions=185,dialogue_retentions=150,physical_body_candidates=333,body_pages=333,
        original_source_FE_panels=18,physical_FE_panels=18,FE_continuation_owners=0,source_styles=0,source_style_objects=0,choice_menus=1,choice_captions=2,
        selected_alignment_cases=1332,all333_final_pages_directly_viewed=True,scoped_names=26,distinct_name_strings=30,fresh_name_planes=19,reused_name_planes=11,
        all_names_andtwo_captions_directly_viewed=True,menu_native_provider_alignments=6,menu_bridged_returns=18,
        menu_normal_highlight_planes=6,target_menu_normal_highlight_planes=4,valid_current_menu_normal_highlight_planes=2,menu_compiler_negatives=7,
        corrupt_current_menu_provider_proved_without_ASCII_font_approval=True,pages_reclaimed=3,additional_phrase_wrap_fixes=4,
        scoped_FE_guard_fixes=6,concrete_failed_FE_records=['DK4_MES_B139_R0199','DK4_MES_B145_R0057'],
        final_native_proof=str(finalpath),final_native_proof_sha256=digest(finalpath),names_sha256=digest(paths['names']),
        full_paragraphs_native_controls_substitutions_andlayout_provenance_preserved=True,
        stored_script_allocation_branches_actual_gameplay_andregistration_pending=True,all_fifth_formatting_gates_still_pending=True,
        actual_gameplay=False,new_ROM=False,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [*paths.values(),*visualpaths,bodypath,mixedpath,finalpath,menupath,stylepath,Path(__file__)]}))
    print('Sealed333 body pages,30 name strings andtwo repaired captions; storage/gameplay/release pending; no new credit.')


if __name__=='__main__':main()
