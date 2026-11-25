"""Retain the full pixel/timing/world audit while binding B214's distinct typed and conditional scope."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B214_English_audit_tools_v6724')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/audit_lil_B213_English_v6679.py').read_text('utf8')
    oldroute=next(line for line in source.splitlines() if line.startswith('    assert predicate_value in [0,1];expected='));suffix=oldroute.split('diffs={',1)[1]
    newroute="    assert predicate_values==[0,0];expected=next(r['offsets'] for r in control['four_structural_route_models'] if r['predicate_Boolean_values']==predicate_values);assert [p['source_offset'] for p in pairs if p['source_offset'] is not None]==expected and len(pairs)==30 and len(panels)==9 and not failures and pairs[-1]['source_offset']==1310 and pairs[-1]['native_result']==[0,0];signature=next(p for p in panels if p['source_record_index']==68);assert signature['native_pages']==1;diffs={"+suffix
    changes={
        'B213':'B214','English_actual_v6679':'English_actual_v6724','English_run_v6678':'English_run_v6723','English_fixture_v6677':'English_fixture_v6722',
        'source_actual_v6666/all18_source_speeches_complete_Japanese_name_masks35_commands_and_normal_return':'source_actual_v6709b/eight_speeches_one_selected_style_complete_source_masks30_commands_and_return',
        'stored_v6672/all18_final_stored_targets72_alignments_and19_complete_pages':'stored_v6717/all17_stored_targets68_alignments_seventeen_complete_pages',
        'name_planes_v6660b/three_actors_six_getters_nine_name_component_planes36_alignments':'name_planes_v6710/four_actors_eight_getters_eleven_name_planes44_alignments',
        'controls_v6658/two_unforced_predicates_six_structural_cases50_seeded_ends_two_branch_models':'controls_v6708/four_unforced_predicates_ten_structural_cases50_seeded_ends_four_route_models',
        "name_forms={r['actor_ID']:r['text'] for r in names['distinct_native_getter_values'] if r['consumer']=='progressive-nameplate'}":"name_forms={r['actor_ID']:r['progressive'] for r in read(names['source_name_binding'])['source_name_fields']}",
        'last=0;predicate_value=None':'last=0;predicate_values=[]',
        "command['relocated_block_offset']":"command['fixture_offset']-48",
        "r['last_result']==last":"r['previous_value']==last",
        "case['native_extent']":"case['extent']",
        "if word==0x8000:assert row['result_words'][0]==2 and row['result_words'][1] in [0,1];last=predicate_value=row['result_words'][1]":"if word==0x8000:assert row['result_words'][0]==2 and row['result_words'][1] in [0,1];last=row['result_words'][1];predicate_values.append(last)",
        'if at not in refs:continue':"if at not in refs and word!=0x4100:continue",
        "ref=refs[at];record=stored_rows[ref['id']]":"ref=refs[at] if at in refs else dict(id='DK4_VOICE_B214_C8_T170',source_record_index=None,source_selector=208);record=stored_rows[ref['id']]",
        "name_forms[ref['source_selector']]":"name_forms[151 if ref['source_selector']==208 else ref['source_selector']]",
        oldroute:newroute,
        "transition_frames=[page['selected_complete_capture']['frame'] for page in long['pages']]+[post,16001]":"transition_frames=[panels[0]['selected_complete_capture']['frame'],signature['selected_complete_capture']['frame'],post,16001]",
        'R42_both_pages_normal_port_and_final.png':'crew_signature_normal_port_and_final.png',
        'English_complete_pages_original_controls_normal_return_and_honest_later_scope.json':'nine_English_objects_complete_pages_controls_return_and_later_scope.json',
        'actual_progressive_objects=len(panels)':'actual_unique_objects=len(panels),actual_progressive_objects=sum(p[\'source_selector\']!=208 for p in panels),actual_automatic_style_objects=sum(p[\'source_selector\']==208 for p in panels)',
        'offline_only_speech_IDs=offline':"offline_only_object_IDs=offline,offline_only_speech_IDs=[v for v in offline if v.startswith('DK4_MES_')]",
        'actual_predicate_type2_Boolean=predicate_value':'actual_predicate_type2_Boolean_values=predicate_values',
        'normal_end_result=[0,predicate_value]':'normal_end_result=[0,predicate_values[-1]]',
        'R42_two_complete_native_pages_in_order_with_original_ordinary_A_input=True,R42_page2_whole_instruction_first_glyph_and_original_guard_match=True':'all_nine_actual_objects_original_single_pages_with_ordinary_A_input=True,Janus_Pasar_signature_complete_native_black_gray_and_name_masks_match=True',
        'natural_event213':'natural_event214',
        'actual_speeches=len(panels)':'actual_objects=len(panels)',
        'predicate=predicate_value':'predicates=predicate_values'
    }
    checked_text(source,changes)
    proof=derive('scripts/audit_lil_B213_English_v6679.py','scripts/audit_lil_B214_English_v6724.py',changes)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_full_English_audit.json',dict(derivation=proof,all_original_native_numbers_current_mask_guards_and_full_later_difference_audit_preserved=True,nine_selected_objects_eight_speeches_one_style4_body_not_all17=True,two_original_predicates_conditional_Manuel_lines_and_other_six_styles_explicit=True,complete_Janus_Pasar_signature_and_letter_staging_required=True,no_new_run_ROM_or_credit=True,full_goal_complete=False))
