"""Seal all31 whole-exchange references with measured timing and honest capture limits."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B199_reference_tools_v5796 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B199_reference_approval_v5809')
INPUT=Path('translations/lil_B199_editorial_manuscript_v5.json')
OUTPUT=Path('translations/lil_B199_editorial_manuscript_v6.json')
MAP=Path('translations/lil_B199_editorial_relocation_map_v1.json')
CENSUS=Path('work/analysis/lil_B199_reference_census_v5802/all47_commands_no_relative_sites_and_shipped_entry_census.json')
CONTROL=Path('work/analysis/lil_B199_relocated_controls_v5804/all31_dispatches_two_picture_two47xx_pairs_one_pause_and16_exact_leaves.json')
STORED=Path('work/analysis/lil_B199_stored_v5798/all31_final_stored_targets124_macro_cases_and_complete_planes.json')
ENDS=Path('work/analysis/lil_B199_ends_v5803/two_declared_tail_end_decodes_no_relative_sites.json')
ACTUAL=Path('work/analysis/lil_B199_actual_v5807/thirty_one_actual_panels_source_matched_controls_and_complete_native_holds.json')
SCREENS=Path('work/analysis/lil_B199_screen_review_v5808/paired_scene_and_return_sheets_with_measured_limits.json')
STATE=Path('work/analysis/lil_B199_timing_state_v5808b/six_speech_duration_changes_34_shifted_pairs_prompt_bounds_and_native_state.json')
NATIVE=Path('work/analysis/lil_B199_native_approval_v5793/all31_source_prose_current_native_approval.json')
FLAGS=['all47_source_commands_and_one_pause_verified','all31_source_targets_and16_control_leaves_preserved',
    'thirty_progressive_one_null_actor_FE_and_one_FI_preserved','all1168_predecessor_bytes_inverse_two_tailzeros',
    'all31_actual_panels120_holds_and_no_offline_only_scope','opaque_control_durations_and_results_preserved',
    'measured_speech_timing_prompt_and_PRNG_differences_explicit',
    'queried_final_components_equal_no_future_world_equivalence_claim','representative_shared_rules_approved']
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,OUTPUT,MAP])
    doc=deepcopy(read(INPUT))
    plan,census,control,stored,ends,actual,screens,state,native=map(read,[PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,SCREENS,STATE,NATIVE])
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']
    assert sha(ROM.read_bytes())==census['research_ROM_sha256']==control['research_ROM_sha256']==ends['research_ROM_sha256']
    assert plan['manuscript_sha256']==control['manuscript_sha256']==stored['manuscript_sha256']==native['manuscript_sha256']==sha(INPUT.read_bytes())
    assert not actual['failures'] and not actual['paired_region_differences']
    assert actual['actual_unique_speech_panels']==actual['complete_matching_observations']==31 and actual['complete_matching_holds']==120
    assert len(actual['actual_timing_differences'])==34 and len(actual['later_whole_RGB_differences'])==6
    assert all(r['nontext_region_difference_bbox'] is None for r in actual['all_sampled_frame_comparisons'])
    assert screens['sampled_nontext_frames']==182 and screens['source_and_English_return_frames']==[10776,10778]
    assert state['actual_proof_sha256']==screens['actual_proof_sha256']==sha(ACTUAL.read_bytes())
    assert all(state['native_final_component_equality'].values())
    assert state['all_nonspeech_pause_picture_resource_effect_and_end_durations_equal']
    assert len(state['six_actual_speech_duration_changes'])==6 and state['maximum_absolute_speech_duration_delta']==5
    assert state['later_differences_bounded_to_16x16_advance_prompt_region'] and state['no_pixels_masked_retimed_or_edited']
    assert state['final_13001_PRNG_seeds']==screens['final_13001_PRNG_seeds']==[2490278034,720570979]
    assert not screens['final_13001_PRNG_equal'] and not state['final_PRNG_seeds_equal']
    assert len(control['relocated_dispatch_cases'])==31 and len(control['all16_source_current_target_control_leaves'])==16
    assert len(control['picture_and_short47xx_pairs'])==4
    assert len(ends['cases'])==2 and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',1162),('research',1110)]
    ids=[r['id'] for r in actual['actual_panels']]
    assert ids==[r['id'] for r in doc['records']] and actual['offline_only_source_indices']==[]
    viewed=[]
    for label,rows in [('actual-consumer',actual['review_sheets']),('paired-full-screen',screens['paired_full_screen_sheets'])]:
        assert len(rows)==6
        for s in rows:
            assert sha(Path(s['path']).read_bytes())==s['sha256']
            viewed.append(dict(**s,kind=label,viewed_in_full_current_turn=True,viewed_after_image_return=True,original_detail=True))
    assert len(native['reviewed_sheets'])==4
    for s in native['reviewed_sheets']:assert s['viewed_in_full_current_turn'] and sha(Path(s['path']).read_bytes())==s['sha256']
    paths=[INPUT,PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,SCREENS,STATE,NATIVE,Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    ROOT.mkdir(parents=True);sample=ROOT/'representative_display_control_and_transition_reconciliation.json'
    save(sample,dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[],actual_selected_B199_source_events=[],
        all47_source_commands_plus9_initializers_stored_and56_observed_without_omission=True,
        all31_actual_native_panels120_complete_holds_and_all182_sampled_nontext_regions_match=True,
        thirty_progressive_one_null_actor_four_impact_FE_one_FI_and_two_private_thoughts_preserved=True,
        original_pause_two_picture_layouts_short47xx_A000_and_complete_end_results_preserved=True,
        source_matched_name_portrait_item_and_background_visibility_preserved=True,
        sampled_nontext_frames=182,command_start_or_return_difference_count=34,speech_duration_difference_count=6,
        all_nonspeech_control_durations_equal=True,maximum_absolute_speech_duration_delta_frames=5,
        source_and_English_return_frames=[10776,10778],return_delta_frames=2,
        later_sampled_whole_RGB_difference_count=6,later_difference_bounds=[224,360,240,376],
        six_later_differences_visually_confirmed_advance_prompt_blink=True,
        final_13001_PRNG_seeds=[2490278034,720570979],PRNG_seeds_differ=True,complete_RNG_timing_cause_not_traced=True,
        final_native_component_equality=state['native_final_component_equality'],
        original_native_getters_verify_cash_company_fleet_ship_actor_town_item_goods_task_and_calendar_scope=True,
        no_broad_world_effect_full_RAM_future_random_sequence_or_simulation_equivalence_claim=True,
        no_natural_event_activation_original_location_full_route_or_hardware_claim=True,
        no_open_translation_specific_display_or_control_finding=True,representative_shared_rules_approved=True,
        six_actual_and_six_paired_sheets_viewed=viewed,
        four_native_sheets_reused_from_previous_native_approval=native['reviewed_sheets'],
        final13001_following_B120_line_and_two_prompt_blink_samples_viewed=True,following_scene_adds_no_editorial_credit=True,
        new_English_runs=1,new_English_frames=13001,reused_Japanese_runs=1,total_successful_frames=26002,
        registered_release_and_current_startup_pending=True,evidence=evidence,full_goal_complete=False))
    block=deepcopy(plan['blocks'][0]);checked=census['blocks'][0]
    assert block['block']==checked['block']==199 and len(block['command_map'])==47 and len(block['text_records'])==31
    assert (block['source_bytes'],block['source_logical_end'],block['research_bytes'],block['research_logical_end'])==(1168,1166,1116,1114)
    assert not any(block[k] for k in ['relative_skip_fixups','target_native_skip_cases','choice_commands','actor_style_commands'])
    assert block['inverse_plus_original_two_tailzeros_recovers_every_stored_source_byte']
    assert block['original2000_pause_and_resume_maps']==[dict(old_offset=56,new_offset=66,source_resume=58,target_resume=68,source_two_byte_pause_and_mapped_resumption_boundary_exact=True)]
    block['target_block_sha256']=block.pop('research_block_sha256')
    block.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],
        external_entry_and_actual_revised_paths_approval_pending=False,individual_naturally_selected_source_scene_unobserved=True,
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[])
    mapping=dict(format='dk4-lil-B199-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(NdsImage.open(PARENT).read_file('/__arm9__.bin')),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[block],**{f:True for f in FLAGS},
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[],representative_proof=str(sample),source_plan=str(PLAN),source_census=str(CENSUS),
        final_padding_proof=str(STORED),relocated_control_proof=str(CONTROL),termination_decode_proof=str(ENDS),postscene_native_state_proof=str(STATE),
        evidence={**evidence,str(sample):sha(sample.read_bytes())},actual_selected_B199_source_events=[],full_goal_complete=False)
    save(MAP,mapping)
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),reference_map_pending=False,
        registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for key,p in [('reference_map',MAP),('representative_proof',sample),('final_padding_proof',STORED),('relocated_control_proof',CONTROL),
        ('termination_decode_proof',ENDS),('postscene_native_state_proof',STATE)]:doc[key],doc[key+'_sha256']=str(p),sha(p.read_bytes())
    for r in doc['records']:
        r.update(status=doc['status'],current_text_hex=r['current_hex'],actual_B22_display_fixture_observed=True,
            offline_only_native_display_checked=False,current_complete_native_display_pending=False,
            individual_actual_source_event_activation_not_claimed=True,current_native_UI_body_explicit_unexecuted_boundary=False,
            native_display_consumer='original_null_actor_FE_24310_then5473C' if r['kind']=='system-FE' else 'original_progressive_54020')
    assert all(all(r['review'].values()) for r in doc['records']);validate_natural_dialogue_batch(doc);save(OUTPUT,doc)
    save(ROOT/'reference_approval.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        all31_source_native_reference_and_representative_rules_approved=True,source_prose_English_and_compiled_targets_unchanged=True,
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[],native_approved_revisions=11,native_approved_retentions=20,
        all_prior_evidence_and_measured_timing_prompt_PRNG_differences_preserved=True,
        registered_release_and_current_startup_pending=True,evidence=evidence,new_editorial_credit=0,full_goal_complete=False))
    print('B199 sealed31 objects:11 revisions/20 retentions;31 actual panels/120 holds,182 nontext samples exact. Timing/prompt/PRNG differences explicitly bounded;queried final components equal. Atomic compiler/release next.')
