"""Exact B223 native and actual evidence gates; no archive mutation here."""
import json,struct
from pathlib import Path
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.lil_B223_profile_v1 import contract,profile_for
from dk4tool.dialogue import lil_B223_layout_v1 as codec
from scripts.seal_lil_B223_references_v7111 import FLAGS
CONFIG='translations/lil_B223_editorial_release_v1.json';PATH='/data/SC2.DK4'
def load(path):return json.loads(Path(path).read_bytes())
def require(ok,message):
    if not ok:raise ValueError('B223 '+message)
def exact(d,fields,label):
    for k,v in fields.items():require(d.get(k)==v,label+':'+k)
def observations(doc,mapping,conf):
    approved=load(doc['native_approved_manuscript'])
    require(sha(Path(doc['native_approved_manuscript']).read_bytes())==doc['native_approved_manuscript_sha256']==mapping['manuscript_sha256'] and approved['records']==doc['records'],'exact approved records')
    spec=mapping['blocks'][0];nested=spec['text_records']+[r for o in spec['actor_style_commands'] for r in o['alternative_records']]
    require(len(nested)==17 and {r['id']:r for r in nested}=={r['id']:r for r in spec['all_object_references']},'nested references')
    for k in ['native_font_proof','native_stored_proof','native_policy_validation','native_approval','speaker_name_review','actual_source_proof','actual_English_proof','actual_English_view','relocated_control_proof','later_scope_proof']:
        require(sha(Path(doc[k]).read_bytes())==(mapping['evidence'][doc[k]] if k=='native_approval' else doc[k+'_sha256']),'proof hash:'+k)
    f,s,q,n,names,a,v,c,l=[load(doc[k]) for k in ['native_font_proof','native_stored_proof','native_policy_validation','native_approval','speaker_name_review','actual_English_proof','actual_English_view','relocated_control_proof','later_scope_proof']]
    exact(f,dict(complete_native_pages=19,logical_compiled_input_alignment_cases=136,all17_objects_each_original216x64_page_is_four_rows=True,all_first_internal_final_visible_glyphs_in_order_unique_cells_and_bounds=True,each_plane_exact_independent_current_font_and_all_canaries=True,all_original_current_font_renderer_instructions_verified=True,all_source_macros_zero_no_new_substitutions=True,no_actor_role_roster_RNG_or_event_assignment=True,D0_fallback151_unchanged=True,complete_Ian_Dukov_signature_native_ink_preserved=True),'font')
    exact(s,dict(final_stored_alignment_cases=68,fresh_alignment_cases=20,exact_reused_alignment_cases=48,fresh_parity_tail_records=5,complete_pages=19,all_final_stored_targets_equal_reviewed_complete_native_ink=True,no_extra_blank_page_or_lost_leading_trailing_internal_glyph=True,all_seven_style_bodies_exclude_virtual_D0_and_have_independent_terminators=True),'stored')
    exact(q,dict(positive_paragraph_count=17,negative_count=88,complete_native_pages=19,two_exact_record_local_article_waivers_all_base_diagnostics_preserved=True),'policy')
    require(len(q['negative_cases'])==88 and all(r['rejected'] for r in q['negative_cases']) and len(q['row_count_reasons'])==6,'policy cases/reasons')
    exact(n,dict(all17_five_gates_approved=True,revision_count=16,retention_count=1,native_pages=19,logical_compiled_alignments=136,stored_alignments=68,name_alignments=44,layout_rejections=88,actual_objects=9,actual_native_pages=11,complete_body_holds=37,complete_name_holds=37,offline_only_objects=8,six_row_reasons_two_exact_weak_boundary_waivers_and_all_base_QA_preserved=True,one_original_unforced_predicate_five_structural_cases25_seeded_ends_verified=True,three_contextual_name_retentions_no_asset_or_duplicate_credit=True,all_measured_later_differences_and_unvisited_scope_retained=True),'approval')
    require(names['three_contextual_name_retentions_no_asset_or_duplicate_credit'] and names['full_catalogue_UI_unvisited'] and names['Cesare_conditional_header_unvisited'] and names['actor151_Sailor_Retainer_and_full207_review_remain_open'],'names scope')
    require([(r['actor_ID'],r['english']) for r in names['records']]==[(2,'Lil Argot'),(13,'Cesare Tony'),(21,'Ian Dukov')] and all(all(r['review'].values()) and r['new_name_or_dialogue_credit']==0 for r in names['records']),'individual names')
    require([(r['actor_ID'],r['actual_English_header_observed']) for r in names['records']]==[(2,True),(13,False),(21,True)],'names actual/offline')
    exact(a,dict(actual_unique_objects=9,actual_progressive_objects=8,actual_automatic_style_objects=1,actual_native_pages=11,complete_body_holds=37,complete_name_holds=37,incomplete_progressive_holds=0,actual_predicate_type2_Boolean_values=[0],source_exit_frame=5253,English_exit_frame=5496,normal_English_port_sample_frame=5590,normal_end_result=[0,0],all_eleven_actual_pages_two_continuations_with_ordinary_A_input=True,Ian_Dukov_signature_complete_native_black_gray_and_name_masks_match=True,no_full_RAM_future_sequence_broad_simulation_or_complete_causal_claim=True,source_and_English_runs_terminal_reaped=True,all_following_resident_payloads_verified_against_actual_SC0_to_SC3_bank=True),'actual')
    for k in ['failures','command_result_differences','command_UI_word_differences','source_command_offsets_not_observed_in_English']:require(not a[k],'actual failed:'+k)
    require(len(a['actual_panels'])==9 and len(a['command_pairs'])==27 and len(a['offline_only_object_IDs'])==8 and a['offline_only_speech_IDs']==['DK4_MES_B223_R0067','DK4_MES_B223_R0070'],'actual objects')
    require(len(a['semantic_upper_scene_portrait_pairs'])==9 and all(r['upper_scene_portrait_equal'] and r['portrait_only_equal'] for r in a['semantic_upper_scene_portrait_pairs']),'semantic portraits')
    require(sum(len(p['complete_body_holds']) for p in a['actual_panels'])==sum(len(p['complete_name_holds']) for p in a['actual_panels'])==37 and sum(p['native_pages'] for p in a['actual_panels'])==11,'actual aggregates')
    for panel in a['actual_panels']:
        expected=2 if panel['source_record_index'] in [31,40] else 1
        require(panel['native_pages']==len(panel['pages'])==expected and panel['complete_body_holds'] and panel['complete_name_holds'] and not panel['incomplete_progressive_holds'],'actual panel')
        for page in panel['pages']:require(page['complete_body_holds'],'actual complete page')
        for h in panel['complete_body_holds']:require(h['complete_independent_native_body_black_gray_all_glyphs_equal'] and sha(Path(h['capture']).read_bytes())==h['sha256'],'actual body')
        for h in panel['complete_name_holds']:require(h['complete_name_and_blank_guards_equal'] and sha(Path(h['capture']).read_bytes())==h['sha256'],'actual name')
    require([(t['id'],t['last_complete_previous_frame'],t['first_complete_next_frame'],t['original_A_inputs_in_interval'][0]['start']) for t in a['page_transitions']]==[('DK4_MES_B223_R0031',3550,3610,3560),('DK4_MES_B223_R0040',4510,4570,4520)],'two original page advances')
    require(v['all_four_sheets_individually_returned_and_viewed'] and v['all11_sheet_panes_pixel_equal_whole_frame_crops'] and v['all11_pages37_body37_name_holds_complete'] and not v['visual_review_pending'] and v['later_captain0_2_and_all_world_differences_retained'],'viewed scope')
    require([len(a[k]) for k in ['command_timing_differences','command_RNG_differences','command_duration_changes','upper_same_frame_region_differences','scene_same_frame_RGB_differences','later_same_frame_RGB_differences']]==[14,14,5,8,44,175],'all measured differences')
    require(a['captain_IDs']==l['captain_IDs']==[0,2] and a['final_PRNG_seeds']==l['final_PRNG_seeds']==[646626623,1613831355] and a['five_native_component_equality']==l['five_native_component_equality'] and not any(a['five_native_component_equality'].values()),'unequal final values retained')
    require(l['all_measured_differences_retained_for_later_older_record_technical_reaudit'] and l['no_full_RAM_future_sequence_broad_simulation_or_complete_causal_claim'] and l['source_SC0_B44_open_English_only_SC2_B120_observed'],'later scope')
    require(len(c['dispatch_cases'])==17 and len(c['all207_target_style_getters']['cases'])==207 and c['original_style2_7_alias_preserved'] and c['whole_4100_command']['resolved_actor_ID']==151 and c['whole_4100_command']['original_actor_style']==4 and len(c['eight_style_slots'])==8 and c['eight_style_slots'][2]['relative_offset']==c['eight_style_slots'][7]['relative_offset'],'typed aliases')
    require([(r['source_offset'],r['target_offset'],r['source_operand_alignment'],r['target_operand_alignment']) for r in c['relocated_predicates']]==[(1138,1178,2,2)] and c['one_same_alignment_predicate_original_owned_scratch_only_restores4MiB'],'predicate alignment')
    for r in c['relocated_predicates']:require(r['relocated']['native_result']==[2,0,0,0,0,0] and r['relocated']['sole_scratch_restore_recovers_all4MiB_exact'] and len(r['relocated']['original_unaligned_operand_read_scratch_writes'])==1,'predicate scratch')
    require(len(c['opaque_structural_cases'])==5 and len(c['target_normal_end_cases'])==25 and all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in c['target_normal_end_cases']) and c['target_end1380_state0_retains_existing_value_word_no_tail'],'structural/normal ends')
    loader,census,entry=[load(conf[k]) for k in ['loader','census','entry']]
    require(loader['all336_whole_blocks_and672_modes_each_pass'] and loader['SDK_IO_bridges_only_no_loader_or_cache_success_stub'],'loader')
    require(census['all22_clean_current_target_commands_bound'] and census['only_original24070_interpreter_call_no_literal_alias'] and census['blocks'][0]['mapped_commands']==spec['mapped_native_commands'],'census')
    require([(r['event_ID'],r['script_block'],r['action_index'],r['must_be_completed'],r['must_not_be_completed']) for r in entry['selected_B223_source_events']]==[(223,223,224,[90],[])],'event/dependency')
    return f,s,a,c
