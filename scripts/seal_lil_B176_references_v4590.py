"""Seal complete B176 source/native/actual evidence for registered integration."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B176_research_v4579 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B176_reference_approval_v4590')
INPUT=Path('translations/lil_B176_editorial_manuscript_v3.json')
OUTPUT=Path('translations/lil_B176_editorial_manuscript_v4.json')
MAP=Path('translations/lil_B176_editorial_relocation_map_v1.json')
CENSUS=Path('work/analysis/lil_B176_reference_census_v4582/all13_commands_no_relative_sites_and_shipped_entry_census.json')
CONTROL=Path('work/analysis/lil_B176_relocated_controls_v4584/all10_progressive_FE_dispatches_A000_C200_pairs_and3_leaves.json')
STORED=Path('work/analysis/lil_B176_stored_v4576/all10_final_stored_targets40_macro_cases_and_complete_planes.json')
ENDS=Path('work/analysis/lil_B176_ends_v4583/two_declared_tail_end_decodes_no_relative_sites.json')
ACTUAL=Path('work/analysis/lil_B176_actual_v4588/actual_all10_progressive_FE_A000_C200_and_single_end.json')
FIXTURE=Path('work/analysis/lil_B176_display_fixture_v4585/complete_B176_B22_fixtures.json')
VISUAL=Path('work/analysis/lil_B176_actual_review_v4589/all2_actual_sheets10_planes_fullscreens_return_and_final_state.json')

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,OUTPUT,MAP])
    doc=deepcopy(read(INPUT))
    plan,census,control,stored,ends,actual,fixture,visual=map(read,[PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL])
    parent=NdsImage.open(PARENT)
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']
    assert sha(ROM.read_bytes())==census['research_ROM_sha256']==control['research_ROM_sha256']==ends['research_ROM_sha256']
    assert sha(INPUT.read_bytes())==plan['manuscript_sha256']==stored['manuscript_sha256']==control['manuscript_sha256']
    assert census['all13_clean_current_target_commands_and_no_relative_sites_reexecuted']
    assert census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert len(control['relocated_dispatch_cases'])==10 and sum(r['resolved_actor_ID'] is None for r in control['relocated_dispatch_cases'])==1
    assert len(control['all3_source_current_target_nonrelative_nonspeech_leaves'])==3
    assert len(control['relocated_C200_pairs'])==len(control['relocated_A000_structural_pairs'])==1
    assert control['all9_progressive_static_actors1_impersonal_null_actor_FE_and_no_FI_FA_FO_exact']
    assert len(stored['final_target_parity_cases'])==10 and stored['current_final_stored_macro_alignment_cases']==40
    assert (stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(16,24)
    assert stored['all10_final_targets_complete_native_planes_equal_reviewed_planes']
    assert len(ends['cases'])==2 and ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
    assert ends['B176_single_end_finishes_declared_logical_end']
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==10
    assert not actual['failures'] and not actual['paired_region_differences'] and not actual['offline_only_display_IDs']
    assert actual['frames_per_boot']==9001 and actual['actual_new_cold_boot_runs']==2
    assert all(len(v['selected_B22_command_pairs'])==22 and v['single_source_end386_actually_reached']
               and v['fixture_exit_frame']==5256 for v in actual['versions'])
    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and visual['no_open_translation_specific_display_or_control_finding']
    assert len(visual['all2_actual_sheets_viewed'])==2 and all(s['viewed'] for s in visual['all2_actual_sheets_viewed'])
    assert len(visual['paired_full_screen_views'])==2 and sum(len(s['frames'])*2 for s in visual['paired_full_screen_views'])==8
    assert all(s['viewed'] for s in visual['paired_full_screen_views'])
    assert len(visual['all115_sampled_nontext_region_checks'])==visual['nontext_equal_samples']==115
    assert not visual['nontext_difference_samples'] and not visual['actual_timing_differences']
    assert visual['all_sampled_whole_RGB_from5290_through9001_equal'] and visual['whole_RGB_final9001_equal']
    assert all(visual['postscene9001_native_component_equality'].values()) and visual['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert visual['all_content_jobs_terminal'] and visual['PRNG_equality'] and visual['postscene9001_PRNG_seeds']==[403514907,403514907]
    assert fixture['source_all13_commands_preserved_without_omission_or_flattening']
    assert all(not f['explicitly_excluded_original_commands'] and len(f['all22_stored_fixture_commands'])==22 for f in fixture['fixtures'])
    ids=[r['id'] for r in actual['actual_panels']]
    assert ids==[r['id'] for r in doc['records']] and len(set(ids))==10
    native=read(doc['native_font_proof'])
    assert native['all10_current_native_speech_planes_pass'] and native['current_original_macro_alignment_calls']==80
    paths=[INPUT,PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL,Path(__file__)]
    for path,digest in visual['evidence'].items():
        assert sha(Path(path).read_bytes())==digest,path
    for sheet in visual['all2_actual_sheets_viewed']+visual['paired_full_screen_views']:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    ROOT.mkdir(parents=True)
    sample=ROOT/'representative_display_control_and_transition_reconciliation.json'
    save(sample,dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        evidence=evidence,viewed_actual_sheets=visual['all2_actual_sheets_viewed'],actual_two_disclosed_content_cold_boots_pass=True,
        content_frames_each=9001,new_emulator_runs=2,no_additional_focus_run_without_concrete_unresolved_risk=True,
        actual_selected_B176_source_events=[],actual_sampled_display_IDs=ids,offline_only_display_IDs=[],represented_reviewed_display_IDs=ids,
        all10_panels9_progressive1_impersonal_FE_source_A000_C200_single_end_and_normal_town_return_pass=True,
        original13_commands_and_single_declared_tail_endword_preserved=True,no_B176_source_command_omitted=True,
        original_B22_four_A000_initialization_commands_and_one_source_A000_retained=True,
        source_end386_actual_target400_offline_and_fixture_end_actual=True,
        all115_nontext_samples_and_all22_command_timings_equal=True,
        complete_native_text_planes_and_paired_held_nontext_regions_equal=True,
        whole_RGB_town_return_and_final_following_tutorial_equal=True,
        five_native_state_components_whole1A04_actor_captain2_and_PRNG_equal=True,
        no_future_world_full_RAM_or_hardware_equality_claim=True,
        no_open_translation_specific_display_or_control_finding=True,
        no_natural_event_eligibility_earned_fashion_state_earlier_location_full_route_or_hardware_claim=True,
        registered_release_and_current_startup_pending=True,full_goal_complete=False))
    block=deepcopy(plan['blocks'][0]);checked=census['blocks'][0]
    assert block['block']==checked['block']==176
    block['target_block_sha256']=block.pop('research_block_sha256')
    block.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],
        external_entry_and_actual_revised_paths_approval_pending=False,individual_naturally_selected_source_scene_unobserved=True,
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[],representative_scope_does_not_mean_natural_event_eligibility=True)
    assert len(block['command_map'])==13 and len(block['text_records'])==10
    assert not any(block[k] for k in ['relative_skip_fixups','target_native_skip_cases','choice_commands','actor_style_commands'])
    assert [(e['source_offset'],e['target_offset']) for e in block['original_declared_end_word_maps']]==[(386,400)]
    flags=['all13_structural_commands_verified','all10_active_speech_targets_preserved',
        'all3_leaves_one_A000_C200_and_single_end_exact','single_declared_tail_endword_preserved',
        'progressive9_impersonal_FE1_and_FI0_FA0_FO0_preserved','no_source2100_4100_or_dynamic_objects',
        'no_source2000_pause','no_source_relative_sites_predicates_resources_or_presentations',
        'source_A000_raw_operand_bytes_preserved_without_inferred_semantics',
        'single_end386_actual_target400_offline','representative_shared_rules_approved']
    mapping=dict(format='dk4-lil-B176-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(parent.read_file('/__arm9__.bin')),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[block],**{f:True for f in flags},
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[],representative_proof=str(sample),source_plan=str(PLAN),source_census=str(CENSUS),
        final_padding_proof=str(STORED),relocated_control_proof=str(CONTROL),termination_decode_proof=str(ENDS),postscene_native_state_proof=str(VISUAL),
        evidence={**evidence,str(sample):sha(sample.read_bytes())},actual_selected_B176_source_events=[],full_goal_complete=False)
    save(MAP,mapping)
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),reference_map_pending=False,
        registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for key,path in [('reference_map',MAP),('representative_proof',sample),('final_padding_proof',STORED),('relocated_control_proof',CONTROL),
        ('termination_decode_proof',ENDS),('postscene_native_state_proof',VISUAL)]:
        doc[key],doc[key+'_sha256']=str(path),sha(path.read_bytes())
    for row in doc['records']:
        assert row['kind'] in ['progressive','system-FE']
        row['historical_pre_actual_display_scope']={k:row[k] for k in ['current_complete_native_display_pending','current_native_UI_body_explicit_unexecuted_boundary'] if k in row}
        row.update(status=doc['status'],current_text_hex=row['current_hex'],
            native_display_consumer='original_null_actor_FE_24310_then5473C' if row['kind']=='system-FE' else 'original_progressive_54020',
            actual_B22_display_fixture_observed=True,offline_only_native_display_checked=False,current_complete_native_display_pending=False,
            current_native_UI_body_explicit_unexecuted_boundary=False,individual_actual_source_event_activation_not_claimed=True)
    assert [r['english'] for r in doc['records']]==[r['english'] for r in read(INPUT)['records']]
    validate_natural_dialogue_batch(doc);save(OUTPUT,doc)
    save(ROOT/'approval_receipt.json',dict(manuscripts={str(OUTPUT):sha(OUTPUT.read_bytes())},reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        evidence={**evidence,str(MAP):sha(MAP.read_bytes()),str(sample):sha(sample.read_bytes())},all10_source_native_reference_and_representative_rules_approved=True,
        source_prose_English_unchanged=True,actual_sampled_display_IDs=ids,offline_only_display_IDs=[],single_end386_actually_reached=True,
        all115_nontext_samples_and_all22_command_timings_equal=True,new_emulator_runs=2,registered_release_and_current_startup_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B176 references sealed:all ten actual panels,13 source commands,A000,C200,single end and normal town return. Registered integration pending.')
