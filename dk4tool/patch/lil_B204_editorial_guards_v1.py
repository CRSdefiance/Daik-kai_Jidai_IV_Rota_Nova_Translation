"""Read-only source-specific B204 guards used before the inherited atomic assembler."""
import json
from pathlib import Path
from collections import Counter
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
def load(p):return json.loads(Path(p).read_bytes())
def require(value,message):
    if not value:raise ValueError('Lil B204 '+message)
def validate(doc,mapping,seal,conf,source,arm,japanese):
    keys=['native_font_proof','final_padding_proof','relocated_control_proof','representative_proof','termination_decode_proof','source_nameplate_consumer_proof']
    native,stored,controls,sample,ends,names=[load(doc[k]) for k in keys]
    state=load(doc['postscene_native_state_proof']);actual=load(doc['actual_proof']);approval=load(conf['native_approval']);fields=load(doc['actor_terminology_reconciliation']);terms=load(doc['contextual_reconciliation']);voices=load(doc['actor_voice_contract'])
    require(len(native['cases'])==20 and native['current_original_macro_alignment_calls']==160 and native['new_native_alignment_calls']==40 and native['exact_input_byte_identical_reused_native_alignment_cases']==120 and native['complete_progressive_planes']==16 and native['complete_FE_logical_and_physical_planes']==4 and len(native['negative_controls'])==24 and all(r['rejected'] for r in native['negative_controls']),'complete native consumers required')
    require(approval['all20_five_gates_approved'] and len(approval['formatter_negative_controls'])==28 and len(approval['twelve_individual_rowcount_reasons'])==12,'formatter and rowcount approvals required')
    require(len(stored['final_target_parity_cases'])==20 and stored['current_final_stored_macro_alignment_cases']==80 and stored['new_parity_macro_alignment_cases']==40 and stored['exact_byte_identical_reused_macro_alignment_cases']==40 and stored['all20_final_targets_complete_native_planes_equal_reviewed_planes'],'final stored proof required')
    require(len(controls['relocated_dispatch_cases'])==20 and len(controls['all6_source_current_target_control_leaves'])==6 and len(controls['picture_and_short47xx_pairs'])==2 and controls['all16_progressive_and_four_FE_objects_preserved'] and controls['no_FI_FA_FO_source_macros'],'complete relocated controls required')
    loader=load(doc['loader_proof']);census=load(doc['source_census'])
    require(loader['all336_whole_blocks_and672_modes_each_pass'] and loader['original_parent_both_modes_start_at_loaded_payload_plus8'] and loader['SDK_IO_bridges_only_no_loader_or_cache_success_stub'] and [r['ROM_sha256'] for r in loader['versions']]==[doc['current_ROM_sha256'],conf['reference_ROM_sha256']],'both exact whole-ROM loader proofs required')
    require(census['all26_clean_current_target_commands_and_no_relative_sites_reexecuted'] and census['research_ROM_sha256']==conf['reference_ROM_sha256'] and census['blocks'][0]['mapped_commands']==mapping['blocks'][0]['mapped_native_commands'],'exact complete source/current/target entry census required')
    for version in loader['versions']:
        require(version['whole_SC2_loads_and_cache_hits']==336 and version['original_parent_modes']==672,'complete loader/cache/parent cases required')
        for key in ['load','parent']:require(sha(Path(version[key+'_proof']).read_bytes())==version[key+'_sha256'],'loader proof changed')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',1308),('research',1340)],'complete guarded end required')
    require(names['progressive_nameplate_values']=={'2':'Lil Argot','11':'Jam Ludwyan','124':'Guard','130':'Daimyo','145':'Innkeeper'} and names['full_catalogue_values']=={'2':'Lil Argot','11':'Jam Jack Ludwyan','124':'Guard','130':'Daimyo','145':'Innkeeper'},'five distinct source name consumers required')
    require(len(names['native_ten_consumer_cases']['rows'])==10 and [[f.get('Japanese') for f in r['fields']] for r in fields['source_name_fields']]==[['リル','アーゴット',None],['ジャム','ルドワイヤン','ジャック'],['衛兵','日本',None],['大名','日本',None],['宿屋のおばさん','日本',None]] and fields['no_name_asset_or_runtime_change'] and fields['no_global_207_name_closure_or_new_name_completion_credit'],'exact clean name fields and no invented relationships or ranks required')
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh5_actor_names']['rows']}=={2:3,11:4,124:0,130:0,145:0},'five source voice classes required')
    current=load(doc['current_actor_name_preservation']);require(doc['current_actor_name_preservation_sha256']==sha(Path(doc['current_actor_name_preservation']).read_bytes()) and current['candidate_sha256']==doc['current_ROM_sha256'] and current['all621_actor_name_pointer_fields_equal_V6050'] and current['all_referenced_staged_name_strings_equal_V6050'],'historical name proof must bind unchanged current consumers')
    require(terms['all20_Japanese_objects_four_FE_letter_parts_and_full_signature_viewed'] and terms['all207_names_review_and_all_other_editorial_scope_remain_open'],'complete clean whole-exchange review required')
    require(not actual['failures'] and actual['actual_unique_speech_panels']==actual['complete_matching_observations']==20 and actual['complete_matching_holds']==77 and actual['offline_only_display_IDs']==[],'all20 actual panels and77 native holds required')
    require(len(actual['actual_panels'])==20 and [p['id'] for p in actual['actual_panels']]==mapping['actual_sampled_display_IDs'] and sum(len(p['holds']) for p in actual['actual_panels'])==77,'individual actual panels required')
    for panel,row in zip(actual['actual_panels'],doc['records'],strict=True):
        require(panel['id']==row['id'] and panel['prefix']==row['source_selector'] and panel['holds'] and panel['native_plane_sha256']==row['native_font_case']['whole_native_plane_sha256'],'actual panel identity/native plane differs')
        for hold in panel['holds']:require(hold['complete_ink_and_gray_masks_equal_native_plane'] and sha(Path(hold['capture']).read_bytes())==hold['capture_sha256'],'complete actual capture required')
    require([len(v['command_pairs']) for v in actual['versions']]==[35,35,35] and [v['exit_frame'] for v in actual['versions']]==[7894,7895,7896] and [v['frames'] for v in actual['versions']]==[13001,8420,13001],'three distinct actual-source scopes required')
    shape=lambda v:[(r['source_offset'],r['word'],r['native_result']) for r in v['command_pairs']]
    require(shape(actual['versions'][0])==shape(actual['versions'][1])==shape(actual['versions'][2]),'original command paths/results differ')
    expected_ids=[(r['id'],r['source_record_index'],r['source_selector']) for r in doc['records']];expected_offsets=[None]*9+[r['old_offset'] for r in mapping['blocks'][0]['command_map']]
    for version in actual['versions']:
        require([(r['id'],r['source_record_index'],r['prefix']) for r in version['selected_intervals']]==expected_ids and [r['source_offset'] for r in version['command_pairs']]==expected_offsets,'complete actual source identities differ')
        report=load(version['capture_report']);require(report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and report['frames']==version['frames'],'actual cold-boot scope differs')
        for photo in report['frames_captured']:require(sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'],'sampled capture changed')
    timing=actual['source_English_command_timing_differences'];rng=actual['source_English_command_RNG_differences']
    for label,version in zip(['earlier-full-Japanese-V6050','current-Japanese-V6110-prefix-before-menu'],actual['versions'][:2],strict=True):
        timed=[dict(source=a,English=b) for a,b in zip(version['command_pairs'],actual['versions'][2]['command_pairs'],strict=True) if (a['start'],a['returned'])!=(b['start'],b['returned'])]
        random=[dict(source=a,English=b) for a,b in zip(version['command_pairs'],actual['versions'][2]['command_pairs'],strict=True) if (a['before_RNG'],a['after_RNG'])!=(b['before_RNG'],b['after_RNG'])]
        require(timing[label]==timed and rng[label]==random,'measured timing/RNG witnesses differ')
    require([len(x) for x in timing.values()]==[16,20] and [len(x) for x in rng.values()]==[9,13],'source-specific timing/RNG counts differ')
    require(state['actual_proof_sha256']==sample['actual_proof_sha256']==sha(Path(doc['actual_proof']).read_bytes()) and state['command_start_return_differences']==timing and state['within_scene_RNG_differences']==rng,'measured proof bindings differ')
    require(state['native_final_component_equality']==dict(state=True,models=True,persistent_objects=True,tasks=True,calendar=True) and state['whole_actor_and_captain_equal'] and not state['final_PRNG_equal'] and state['actual_old_source_and_English_ARM9_hashes_differ'] and state['no_whole_state_equivalence_claim_from_cross_build_getter_comparison'],'honest cross-build native state limits required')
    require(len(state['later_source_English_RGB_differences'])==16 and all(r['difference_bbox'] in [[224,360,240,376],[224,370,240,376]] and r['upper_portrait_name_item_region_equal'] for r in state['later_source_English_RGB_differences']) and state['all16_later_differences_bounded_to_advance_prompt'],'all later prompt differences required')
    prefix=actual['same_frame_comparisons']['current-Japanese-V6110-prefix-before-menu'];require(len(prefix)==7 and all(r['upper_portrait_name_item_region_equal'] for r in prefix) and next(r for r in prefix if r['frame']==5530)['whole_RGB_equal'],'same-code current card/name/notice comparisons required')
    require(len(actual['older_source_nontext_differences_retained_without_filtering_native_text_holds'])==19 and actual['source_current_item_name_Orca_to_Shachihoko_and_ARM9_COMMON_differences_not_hidden'] and actual['current_Japanese_same_ARM9_COMMON_prefix_reused_before_manual_menu_inputs_at8000'],'source-baseline limitations must remain explicit')
    require(sample['no_open_translation_specific_display_control_or_return_finding'] and sample['current_Shachihoko_notice5530_whole_frame_equal_to_current_source'] and sample['representative_shared_rules_approved'] and not sample['visual_review_pending'] and sample['no_natural_event_original_location_earned_inventory_full_effects_routes_or_hardware_claim'] and actual['observed_English_follows_B120'],'complete representative scope required')
    require(len(sample['viewed_sheets'])==6 and all(r['viewed'] and r['viewed_after_image_return'] and r['original_detail'] and sha(Path(r['path']).read_bytes())==r['sha256'] for r in sample['viewed_sheets']),'viewed actual and paired screens required')
    require(not any(p.get('full_goal_complete') for p in [doc,mapping,seal,native,stored,controls,sample,state,approval]),'full editorial objective remains incomplete')
    rows=doc['records'];ids=[r['id'] for r in rows]
    require(len(rows)==len(set(ids))==20 and {r['source_selector'] for r in rows}=={2,11,124,130,145,254} and Counter(r['kind'] for r in rows)=={'progressive':16,'system-FE':4} and Counter(r['editorial_decision'] for r in rows)=={'revise':12,'retain-wording':8},'exact20 decisions/consumers required')
    require(all([r['id'] for r in v['selected_intervals']]==ids for v in actual['versions']) and [r['id'] for r in actual['actual_panels']]==ids and mapping['actual_sampled_display_IDs']==ids and sample['offline_only_display_IDs']==mapping['offline_only_display_IDs']==[],'all20 actual IDs required')
    dispatch=load(doc['control_contract']);catalog=load(dispatch['registered_catalog_binding'])
    require(catalog['all467_rows_complete_keys_targets_route_masks_and_current_calls_verified'] and len(catalog['records'])==467 and all(c['registered_catalog_match'] is None for c in dispatch['speech_dispatch_cases']),'complete current name catalogue binding required')
    require(len(mapping['blocks'])==1 and mapping['blocks'][0]['block']==204,'one exact block required');spec=mapping['blocks'][0];old_blocks=list(IlnkContainer.parse(source).blocks);block=old_blocks[204];original=IlnkContainer.parse(japanese).blocks[204]
    require(len(old_blocks)==336 and sha(block)==spec['source_block_sha256'] and block[:4]==b'CS\0\1','source block differs')
    require(spec['source_bytes']==len(block)==1312 and spec['source_logical_end']==1312 and spec['research_bytes']==1344 and spec['research_logical_end']==1344 and spec['source_alignment_tail_bytes']==spec['target_alignment_tail_bytes']==0,'source/target extent metadata differs')
    require([{k:r[k] for k in ['word','old_offset','new_offset']}|{'old_extent':r['old_native_extent'],'new_extent':r['new_native_extent']} for r in spec['mapped_native_commands']]==spec['command_map'],'both complete command maps must agree')
    return native,stored,controls,sample,ends,names,fields,terms,voices,state,approval,actual,rows,ids,spec,old_blocks,block,original
