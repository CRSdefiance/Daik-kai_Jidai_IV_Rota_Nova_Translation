"""Seal B200 references with complete observed dialogue and honest later-sailing limits."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B200_reference_tools_v5850 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B200_reference_approval_v5865')
INPUT=Path('translations/lil_B200_editorial_manuscript_v4.json')
OUTPUT=Path('translations/lil_B200_editorial_manuscript_v5.json')
MAP=Path('translations/lil_B200_editorial_relocation_map_v1.json')
CENSUS=Path('work/analysis/lil_B200_reference_census_v5855/all31_commands_no_relative_sites_and_shipped_entry_census.json')
CONTROL=Path('work/analysis/lil_B200_relocated_controls_v5857/all19_dispatches_one_picture_one47xx_pair_and12_exact_leaves.json')
STORED=Path('work/analysis/lil_B200_stored_v5852/all19_final_stored_targets76_macro_cases_and_complete_planes.json')
ENDS=Path('work/analysis/lil_B200_ends_v5856/two_declared_tail_end_decodes_no_relative_sites.json')
ACTUAL=Path('work/analysis/lil_B200_actual_v5861/nineteen_actual_panels_source_matched_controls_and_complete_native_holds.json')
SCREENS=Path('work/analysis/lil_B200_screen_review_v5864/paired_scene_return_and_measured_sailing_difference_sheets.json')
STATE=Path('work/analysis/lil_B200_timing_state_v5862/measured_command_durations_screen_bounds_and_native_final_components.json')
NATIVE=Path('work/analysis/lil_B200_native_approval_v5849/all19_source_prose_current_native_approval.json')
PIXELS=Path('work/analysis/lil_B200_postscene_difference_v5863/unmodified_final_difference_pixel_inventory.json')
FLAGS=['all31_source_commands_no2000_pause_verified','all19_source_targets_and12_control_leaves_preserved',
    'seventeen_progressive_two_distinct_null_actor_FE_zero_macros_preserved','all932_predecessor_bytes_inverse_source_two_tailzeros_target_zero',
    'all19_actual_panels73_holds_and_no_offline_only_scope','opaque_control_durations_and_results_preserved',
    'eight_duration_changes19_shifted_pairs16_later_prompt_sky_and_PRNG_differences_explicit',
    'queried_final_components_equal_no_future_world_equivalence_claim','representative_shared_rules_approved',
    'Stranger_target_not_applied_no_global_name_completion_credit']
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,OUTPUT,MAP]);doc=deepcopy(read(INPUT))
    plan,census,control,stored,ends,actual,screens,state,native,pixels=map(read,[PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,SCREENS,STATE,NATIVE,PIXELS])
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']
    assert sha(ROM.read_bytes())==census['research_ROM_sha256']==control['research_ROM_sha256']==ends['research_ROM_sha256']
    assert plan['manuscript_sha256']==control['manuscript_sha256']==stored['manuscript_sha256']==native['manuscript_sha256']==sha(INPUT.read_bytes())
    assert not actual['failures'] and not actual['paired_region_differences']
    assert actual['actual_unique_speech_panels']==actual['complete_matching_observations']==19 and actual['complete_matching_holds']==73
    assert len(actual['actual_timing_differences'])==19 and len(actual['later_whole_RGB_differences'])==16
    assert screens['sampled_nontext_frames']==182 and screens['nontext_equal_samples']==172
    assert screens['following_sailing_sky_difference_samples']==10 and screens['source_and_English_return_frames']==[7676,7677]
    assert state['actual_proof_sha256']==screens['actual_proof_sha256']==sha(ACTUAL.read_bytes()) and all(state['native_final_component_equality'].values())
    assert state['all_duration_changes_are_speeches'] and len(state['actual_command_duration_changes'])==8 and state['maximum_absolute_command_duration_delta']==5
    assert [r['duration_delta'] for r in state['actual_command_duration_changes']]==[-1,4,-1,-1,-4,5,-4,3]
    assert state['no_pixels_masked_retimed_or_edited'] and not state['later_differences_bounded_to_16x16_advance_prompt_region']
    assert len(screens['advance_prompt_region_differences'])==6 and len(screens['following_sailing_sky_region_differences'])==10
    assert pixels['difference_bbox']==[137,192,191,243] and len(pixels['difference_pixels'])==1037
    assert state['final_13001_PRNG_seeds']==screens['final_13001_PRNG_seeds'] and len(set(state['final_13001_PRNG_seeds']))==2
    assert not screens['final_13001_PRNG_equal'] and not state['final_PRNG_seeds_equal']
    assert len(control['relocated_dispatch_cases'])==19 and len(control['all12_source_current_target_control_leaves'])==12 and len(control['picture_and_short47xx_pairs'])==2
    assert len(ends['cases'])==2 and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',926),('research',824)]
    ids=[r['id'] for r in actual['actual_panels']];assert ids==[r['id'] for r in doc['records']] and actual['offline_only_source_indices']==[]
    viewed=[]
    for label,rows,count in [('actual-consumer',actual['review_sheets'],4),('paired-full-screen',screens['paired_full_screen_sheets'],6)]:
        assert len(rows)==count
        for s in rows:
            assert sha(Path(s['path']).read_bytes())==s['sha256'];viewed.append(dict(**s,kind=label,viewed_in_full_current_turn=True,viewed_after_image_return=True,original_detail=True))
    assert len(native['reviewed_sheets'])==3
    for s in native['reviewed_sheets']:assert s['viewed_in_full_current_turn'] and sha(Path(s['path']).read_bytes())==s['sha256']
    paths=[INPUT,PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,SCREENS,STATE,NATIVE,PIXELS,Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in paths};ROOT.mkdir(parents=True);sample=ROOT/'representative_display_control_and_transition_reconciliation.json'
    save(sample,dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),actual_sampled_display_IDs=ids,offline_only_display_IDs=[],actual_selected_B200_source_events=[],
        all31_source_commands_plus9_initializers_stored_and40_observed_without_omission=True,
        all19_actual_native_panels73_complete_holds_and_changed_scene_source_regions_match=True,
        seventeen_progressive_two_null_actor_FE_sound_and_stat_zero_macros_preserved=True,
        original_inn_transition_picture47xx6003_two_A000_final4640_and_complete_end_results_preserved=True,
        source_matched_name_portrait_item_and_background_visibility_during_changed_scene_preserved=True,
        sampled_nontext_frames=182,nontext_equal_samples=172,following_sailing_cloud_difference_samples=10,
        command_start_or_return_difference_count=19,speech_duration_difference_count=8,all_nonspeech_control_durations_equal=True,
        maximum_absolute_speech_duration_delta_frames=5,source_and_English_return_frames=[7676,7677],return_delta_frames=1,
        later_sampled_whole_RGB_difference_count=16,six_prompt_blink_samples_and_ten_following_sailing_cloud_samples_visually_reviewed=True,
        prompt_difference_bounds=[224,360,240,376],following_sailing_difference_bounds=[137,192,191,243],
        final_difference_pixels=1037,following_sailing_cloud_position_difference_not_masked_or_retimed=True,
        native_cloud_object_and_complete_RNG_timing_cause_not_traced=True,
        final_13001_PRNG_seeds=state['final_13001_PRNG_seeds'],PRNG_seeds_differ=True,complete_RNG_timing_cause_not_traced=True,
        final_native_component_equality=state['native_final_component_equality'],
        original_native_getters_verify_cash_company_fleet_ship_actor_town_item_goods_task_and_calendar_scope=True,
        no_broad_world_effect_full_RAM_future_random_sequence_or_simulation_equivalence_claim=True,
        no_natural_event_activation_original_location_full_route_or_hardware_claim=True,
        no_open_translation_specific_display_or_control_finding=True,representative_shared_rules_approved=True,
        four_actual_and_six_paired_sheets_viewed=viewed,three_native_sheets_from_current_native_approval=native['reviewed_sheets'],
        final13001_and12490_following_sailing_screens_prompt_sample_and_unmodified_sky_crop_viewed=True,
        following_B120_adds_no_editorial_credit=True,Stranger_label_target_not_applied_and_name_review_still_open=True,
        new_English_runs=1,new_English_frames=13001,reused_Japanese_runs=1,total_successful_frames=26002,
        registered_release_and_current_startup_pending=True,evidence=evidence,full_goal_complete=False))
    block=deepcopy(plan['blocks'][0]);checked=census['blocks'][0]
    assert block['block']==checked['block']==200 and len(block['command_map'])==31 and len(block['text_records'])==19
    assert (block['source_bytes'],block['source_logical_end'],block['research_bytes'],block['research_logical_end'])==(932,930,828,828)
    assert not any(block[k] for k in ['relative_skip_fixups','target_native_skip_cases','choice_commands','actor_style_commands','original2000_pause_and_resume_maps'])
    assert block['inverse_plus_original_two_tailzeros_recovers_every_stored_source_byte'];block['target_block_sha256']=block.pop('research_block_sha256')
    block.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],external_entry_and_actual_revised_paths_approval_pending=False,
        individual_naturally_selected_source_scene_unobserved=True,actual_sampled_display_IDs=ids,offline_only_display_IDs=[])
    mapping=dict(format='dk4-lil-B200-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(NdsImage.open(PARENT).read_file('/__arm9__.bin')),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[block],**{f:True for f in FLAGS},
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[],representative_proof=str(sample),source_plan=str(PLAN),source_census=str(CENSUS),final_padding_proof=str(STORED),
        relocated_control_proof=str(CONTROL),termination_decode_proof=str(ENDS),postscene_native_state_proof=str(STATE),
        evidence={**evidence,str(sample):sha(sample.read_bytes())},actual_selected_B200_source_events=[],full_goal_complete=False)
    save(MAP,mapping);doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),reference_map_pending=False,
        registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-and-name-target-pending')
    for key,p in [('reference_map',MAP),('representative_proof',sample),('final_padding_proof',STORED),('relocated_control_proof',CONTROL),('termination_decode_proof',ENDS),('postscene_native_state_proof',STATE)]:
        doc[key],doc[key+'_sha256']=str(p),sha(p.read_bytes())
    for r in doc['records']:
        r.update(status=doc['status'],current_text_hex=r['current_hex'],actual_B22_display_fixture_observed=True,offline_only_native_display_checked=False,
            current_complete_native_display_pending=False,individual_actual_source_event_activation_not_claimed=True,current_native_UI_body_explicit_unexecuted_boundary=False,
            native_display_consumer='original_null_actor_FE_24310_then5473C' if r['kind']=='system-FE' else 'original_progressive_54020')
    assert all(all(r['review'].values()) for r in doc['records']);validate_natural_dialogue_batch(doc);save(OUTPUT,doc)
    save(ROOT/'reference_approval.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        all19_source_native_reference_and_representative_rules_approved=True,source_prose_English_and_compiled_targets_unchanged=True,
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[],native_approved_revisions=13,native_approved_retentions=6,
        all_prior_evidence_and_measured_timing_prompt_cloud_PRNG_differences_preserved=True,
        Stranger_name_target_unapplied_and_207_name_queue_open=True,registered_release_and_current_startup_pending=True,evidence=evidence,new_editorial_credit=0,full_goal_complete=False))
    print('B200 sealed19 objects:13 revisions/six retentions;19 actual panels/73 holds. Eight speech-duration changes,19 shifted pairs,six prompt and ten later cloud samples differ;native components agree,PRNG differs. Atomic compiler/release next;name targets open.')
