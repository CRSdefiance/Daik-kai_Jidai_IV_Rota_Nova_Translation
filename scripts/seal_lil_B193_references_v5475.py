"""Seal all fifteen source/native/reference and viewed actual B193 objects."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B193_research_v5463 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B193_reference_approval_v5475')
INPUT=Path('translations/lil_B193_editorial_manuscript_v3.json')
OUTPUT=Path('translations/lil_B193_editorial_manuscript_v4.json')
MAP=Path('translations/lil_B193_editorial_relocation_map_v1.json')
CENSUS=Path('work/analysis/lil_B193_reference_census_v5466/all18_commands_no_relative_sites_and_shipped_entry_census.json')
CONTROL=Path('work/analysis/lil_B193_relocated_controls_v5468/all15_progressive_FE_dispatches_A000_C200_pairs_and3_leaves.json')
STORED=Path('work/analysis/lil_B193_stored_v5462/all15_final_stored_targets60_macro_cases_and_complete_planes.json')
ENDS=Path('work/analysis/lil_B193_ends_v5467/two_declared_tail_end_decodes_no_relative_sites.json')
ACTUAL=Path('work/analysis/lil_B193_actual_v5472/actual_all15_progressive_FE_A000_C200_and_single_end.json')
FIXTURE=Path('work/analysis/lil_B193_display_fixture_v5469/complete_B193_B22_fixtures.json')
VISUAL=Path('work/analysis/lil_B193_actual_review_v5473/all15_panels12_fullscreens_three_Ladies_return_and_measured_differences.json')
FLAGS=['all18_structural_commands_verified','all15_active_speech_targets_preserved','all3_leaves_one_A000_C200_and_single_end_exact',
    'single_declared_tail_endword_preserved','progressive14_impersonal_FE1_and_FI0_FA0_FO0_preserved',
    'no_source_relative_sites_predicates_pause_resources_presentations_or_typed_objects',
    'source_A000_raw_operand_bytes_preserved_without_inferred_semantics','single_end662_actual_target672_offline','representative_shared_rules_approved']

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,OUTPUT,MAP]);doc=deepcopy(read(INPUT))
    plan,census,control,stored,ends,actual,fixture,visual=map(read,[PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL])
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']
    assert sha(ROM.read_bytes())==census['research_ROM_sha256']==control['research_ROM_sha256']==ends['research_ROM_sha256']
    assert sha(INPUT.read_bytes())==plan['manuscript_sha256']==stored['manuscript_sha256']==control['manuscript_sha256']
    assert census['all18_clean_current_target_commands_and_no_relative_sites_reexecuted'] and census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert len(control['relocated_dispatch_cases'])==15 and len(control['all3_source_current_target_nonrelative_nonspeech_leaves'])==3
    assert len(control['relocated_C200_pairs'])==len(control['relocated_A000_structural_pairs'])==1
    assert stored['current_final_stored_macro_alignment_cases']==60 and stored['all15_final_targets_complete_native_planes_equal_reviewed_planes']
    assert (stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(32,28)
    assert ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
    assert actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==15 and not actual['failures'] and not actual['paired_region_differences']
    assert [len(v['selected_B22_command_pairs']) for v in actual['versions']]==[27,27]
    assert [v['fixture_exit_frame'] for v in actual['versions']]==[6457,6457]
    assert fixture['source_all18_commands_preserved_without_omission_or_flattening']
    assert all(not f['explicitly_excluded_original_commands'] and len(f['all27_stored_fixture_commands'])==27 for f in fixture['fixtures'])
    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and visual['no_open_translation_specific_display_or_control_finding']
    assert len(visual['all_actual_consumer_sheets_viewed'])==3 and len(visual['paired_full_screen_views'])==3
    assert all(s['viewed_after_image_return'] for s in visual['all_actual_consumer_sheets_viewed']+visual['paired_full_screen_views'])
    assert visual['nontext_equal_samples']==115 and visual['exact_timing_difference_counts']==dict(total=10,speech=10,control_or_end=0)
    assert not visual['sampled_postscene_whole_RGB_differences_unmasked'] and visual['all_sampled_postscene_whole_RGB_equal']
    assert visual['ten_speech_timing_differences_retained_without_masking_retiming_or_equivalence_claim'] and visual['three_distinct_original_Lady_portraits_and_four_row_explanation_cooking_offer_and_friendship_observed']
    assert visual['whole_RGB_final9001_equal'] and all(visual['postscene9001_native_component_equality'].values())
    assert visual['PRNG_equality'] and visual['postscene9001_whole1A04_actor_models_and_captain2_equal'] and visual['postscene9001_PRNG_seeds']==[463267532,463267532]
    ids=[r['id'] for r in actual['actual_panels']];assert ids==[r['id'] for r in doc['records']] and len(set(ids))==15
    for p,h in visual['evidence'].items():assert sha(Path(p).read_bytes())==h
    for s in visual['all_actual_consumer_sheets_viewed']+visual['paired_full_screen_views']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    paths=[INPUT,PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL,Path('work/analysis/lil_B193_relocation_tools_v5461/viewed_layout_retention_reasons_v2.json'),Path(__file__)];evidence={str(p):sha(p.read_bytes()) for p in paths}
    ROOT.mkdir(parents=True);sample=ROOT/'representative_display_control_and_transition_reconciliation.json'
    save(sample,dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),evidence=evidence,
        viewed_actual_sheets=visual['all_actual_consumer_sheets_viewed'],actual_sampled_display_IDs=ids,represented_reviewed_display_IDs=ids,offline_only_display_IDs=[],
        actual_selected_B193_source_events=[],all15_panels14_progressive1_FE_A000_C200_end_and_normal_parent_return_pass=True,
        original18_commands_and_single_declared_tail_endword_preserved=True,no_B193_source_command_omitted=True,
        original_B22_four_A000_initialization_commands_and_one_source_A000_retained=True,
        source_end662_actual_target672_offline_and_fixture_end_actual=True,
        all185_upper_portrait_name_samples_and59_native_holds_equal=True,measured_timing_differences=visual['exact_timing_difference_counts'],fixture_return_frames=visual['fixture_return_frames'],
        five_native_state_components_whole1A04_actor_and_captain2_equal=True,measured_PRNG_seeds=visual['postscene9001_PRNG_seeds'],PRNG_equality=True,
        all_sampled_postscene_and_final9001_RGB_equal=True,no_PRNG_causal_future_world_full_RAM_or_hardware_equality_claim=True,no_open_translation_specific_display_or_control_finding=True,
        new_emulator_runs=2,total_frames=18002,no_additional_focus_run_without_concrete_risk=True,
        no_natural_event_eligibility_earned_fashion_state_earlier_location_full_route_or_hardware_claim=True,
        registered_release_and_current_startup_pending=True,full_goal_complete=False))
    block=deepcopy(plan['blocks'][0]);checked=census['blocks'][0]
    assert block['block']==checked['block']==193 and len(block['command_map'])==18 and len(block['text_records'])==15
    assert not block['relative_skip_fixups'] and not block['target_native_skip_cases'] and not block['choice_commands'] and not block['actor_style_commands']
    assert [(e['source_offset'],e['target_offset']) for e in block['original_declared_end_word_maps']]==[(662,672)]
    block['target_block_sha256']=block.pop('research_block_sha256')
    block.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],
        external_entry_and_actual_revised_paths_approval_pending=False,individual_naturally_selected_source_scene_unobserved=True,actual_sampled_display_IDs=ids,offline_only_display_IDs=[])
    parent=NdsImage.open(PARENT)
    mapping=dict(format='dk4-lil-B193-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(parent.read_file('/__arm9__.bin')),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[block],**{f:True for f in FLAGS},
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[],representative_proof=str(sample),source_plan=str(PLAN),source_census=str(CENSUS),
        final_padding_proof=str(STORED),relocated_control_proof=str(CONTROL),termination_decode_proof=str(ENDS),postscene_native_state_proof=str(VISUAL),
        evidence={**evidence,str(sample):sha(sample.read_bytes())},actual_selected_B193_source_events=[],full_goal_complete=False)
    save(MAP,mapping);doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),reference_map_pending=False,
        registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for key,p in [('reference_map',MAP),('representative_proof',sample),('final_padding_proof',STORED),('relocated_control_proof',CONTROL),('termination_decode_proof',ENDS),('postscene_native_state_proof',VISUAL)]:
        doc[key],doc[key+'_sha256']=str(p),sha(p.read_bytes())
    for r in doc['records']:
        r['historical_pre_actual_display_scope']={k:r[k] for k in ['current_complete_native_display_pending','current_native_UI_body_explicit_unexecuted_boundary'] if k in r}
        r.update(status=doc['status'],current_text_hex=r['current_hex'],native_display_consumer='original_null_actor_FE_24310_then5473C' if r['kind']=='system-FE' else 'original_progressive_54020',
            actual_B22_display_fixture_observed=True,offline_only_native_display_checked=False,current_complete_native_display_pending=False,current_native_UI_body_explicit_unexecuted_boundary=False,
            individual_actual_source_event_activation_not_claimed=True)
    assert [r['english'] for r in doc['records']]==[r['english'] for r in read(INPUT)['records']]
    layout=Path('work/analysis/lil_B193_relocation_tools_v5461/viewed_layout_retention_reasons_v2.json')
    doc.update(layout_retention_review_proof=str(layout),layout_retention_review_proof_sha256=sha(layout.read_bytes()))
    reasons={r['id']:r['reason'] for r in read(layout)['retained_layouts']}
    for r in doc['records']:
        if r['id'] in reasons:r['native_layout_retention_reason']=reasons[r['id']]
    validate_natural_dialogue_batch(doc);save(OUTPUT,doc)
    save(ROOT/'approval_receipt.json',dict(manuscripts={str(OUTPUT):sha(OUTPUT.read_bytes())},reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        evidence={**evidence,str(MAP):sha(MAP.read_bytes()),str(sample):sha(sample.read_bytes())},all15_source_native_reference_and_representative_rules_approved=True,
        source_prose_English_unchanged=True,actual_sampled_display_IDs=ids,offline_only_display_IDs=[],new_emulator_runs=2,total_frames=18002,
        new_editorial_credit=0,registered_release_and_current_startup_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B193 sealed:15 objects,18 commands,59 native holds,115 pairs,normal return. Registered integration pending;zero credit.')
