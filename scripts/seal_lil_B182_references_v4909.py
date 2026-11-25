"""Source/native/actual B182 approval with original conditional outcomes disclosed."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B182_research_v4897 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B182_reference_approval_v4909')
INPUT=Path('translations/lil_B182_editorial_manuscript_v3.json')
OUTPUT=Path('translations/lil_B182_editorial_manuscript_v4.json')
MAP=Path('translations/lil_B182_editorial_relocation_map_v1.json')
CENSUS=Path('work/analysis/lil_B182_reference_census_v4900/all25_commands_ten_relative_sites_and_shipped_entry_census.json')
CONTROL=Path('work/analysis/lil_B182_relocated_controls_v4902/all8_dispatches_two_RNG_predicates_three_effects_C200_and25_mapped_paths.json')
STORED=Path('work/analysis/lil_B182_stored_v4894/all8_final_stored_targets32_macro_cases_and_complete_planes.json')
ENDS=Path('work/analysis/lil_B182_ends_v4901/two_declared_tail_end_decodes_ten_relative_sites.json')
ACTUAL=Path('work/analysis/lil_B182_actual_v4906/actual_all8_progressive_FE_RNG_effect_C200_and_single_end.json')
FIXTURE=Path('work/analysis/lil_B182_display_fixture_v4903/complete_B182_B22_fixtures.json')
VISUAL=Path('work/analysis/lil_B182_actual_review_v4907/all8_panels_48_fullscreens_conditional_return_and_measured_differences_v2.json')
FLAGS=['all25_structural_commands_verified','all8_active_speech_targets_preserved',
    'all7_nonrelative_leaves_two500_predicates_three_A000_C200_end_exact',
    'all10_relative_sites_and50_native_skip_cases_preserved','all25_mapped_structural_paths_preserve_all8_speeches',
    'progressive7_impersonal_FE1_and_FI0_FA0_FO0_preserved','single_end632_target648_preserved',
    'no_source2000_pause_2100_4100_resources_or_presentations','original_RNG_semantics_and_packed_effect_bytes_preserved',
    'representative_actual_display_controls_and_parent_return_approved']

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,OUTPUT,MAP])
    doc=deepcopy(read(INPUT));plan,census,control,stored,ends,actual,fixture,visual=map(read,[PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL])
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']
    assert sha(ROM.read_bytes())==census['research_ROM_sha256']==control['research_ROM_sha256']==ends['research_ROM_sha256']
    assert sha(INPUT.read_bytes())==plan['manuscript_sha256']==stored['manuscript_sha256']==control['evidence'][str(INPUT)]
    assert census['all25_clean_current_target_commands_and_ten_relative_sites_reexecuted']
    assert census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert len(control['relocated_dispatch_cases'])==8 and len(control['all7_exact_nonrelative_leaves'])==7
    assert len(control['predicate_pairs'])==2 and len(control['C200_pairs'])==1 and len(control['A000_structural_pairs'])==3
    assert len(control['all25_source_and_relocated_structural_paths_identical'])==25
    assert len(stored['final_target_parity_cases'])==8 and stored['current_final_stored_macro_alignment_cases']==32
    assert (stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(16,16)
    assert stored['all8_final_targets_complete_native_planes_equal_reviewed_planes']
    assert ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==8
    assert not actual['failures'] and not actual['paired_region_differences'] and not actual['offline_only_display_IDs']
    assert [v['fixture_exit_frame'] for v in actual['versions']]==[4776,4775]
    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and visual['no_translation_specific_glyph_bounds_pagination_portrait_or_return_finding']
    assert visual['observed_random_path_difference']['same_control_path']
    assert visual['observed_random_path_difference']['original_effects_by_case']=={'clean_Japanese':[532],'reviewed_English':[532]}
    assert visual['exact_timing_difference_counts']==dict(total=13,speech=7,control_or_end=6)
    assert len(visual['sampled_postscene_whole_RGB_differences_unmasked'])==18
    assert all(r['whole_frame_difference_bbox']==[224,360,240,376] for r in visual['sampled_postscene_whole_RGB_differences_unmasked'])
    assert visual['postscene9001_PRNG_seeds']==[3723009301,403514907] and not visual['PRNG_equality']
    assert all(visual['postscene9001_native_component_equality'].values()) and visual['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert visual['whole_RGB_final9001_equal']
    assert visual['nontext_equal_samples']==len(visual['all85_sampled_nontext_region_checks'])==115
    assert len(visual['all_actual_consumer_sheets_viewed'])==2 and len(visual['paired_full_screen_views'])==12
    assert all(s['viewed'] for s in visual['all_actual_consumer_sheets_viewed']+visual['paired_full_screen_views'])
    assert visual['total_frames']==18002 and visual['actual_new_cold_boot_runs']==2
    assert fixture['source_all25_commands_preserved_without_omission_or_flattening']
    assert all(not f['explicitly_excluded_original_commands'] and len(f['all34_stored_fixture_commands'])==34 for f in fixture['fixtures'])
    ids=[r['id'] for r in actual['actual_panels']];assert ids==[r['id'] for r in doc['records']] and len(set(ids))==8
    for p,h in visual['evidence'].items():assert sha(Path(p).read_bytes())==h
    for sheet in visual['all_actual_consumer_sheets_viewed']+visual['paired_full_screen_views']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    paths=[INPUT,PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL,Path('work/analysis/lil_B182_predicate500_v4896/all24_aligned_and_unaligned_original500_ownership_cases.json'),Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in paths};ROOT.mkdir(parents=True)
    sample=ROOT/'representative_display_control_and_transition_reconciliation.json'
    save(sample,dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        evidence=evidence,viewed_actual_sheets=visual['all_actual_consumer_sheets_viewed'],actual_sampled_display_IDs=ids,
        represented_reviewed_display_IDs=ids,offline_only_display_IDs=[],actual_selected_B182_source_events=[],
        all8_panels_seven_progressive_one_FE_selected_effect_C200_end_and_parent_return_pass=True,
        source_all25_commands_ten_branches_two_predicates_three_alternative_effects_preserved=True,
        actual_conditional_paths_verified_without_forcing_same_outcome=True,
        original_scene_RNG_outcome_equal_final_RNG_and_timing_indicator_differences_disclosed=True,
        no_open_translation_specific_display_or_control_finding=True,new_emulator_runs=2,total_frames=18002,
        no_natural_event_eligibility_earned_fashion_state_prior_location_future_world_full_RAM_or_hardware_claim=True,
        registered_release_and_current_startup_pending=True,full_goal_complete=False))
    block=deepcopy(plan['blocks'][0]);checked=census['blocks'][0]
    assert block['block']==checked['block']==182 and len(block['command_map'])==25 and len(block['text_records'])==8
    assert len(block['relative_skip_fixups'])==10 and len(block['target_native_skip_cases'])==50
    assert [(e['source_offset'],e['target_offset']) for e in block['original_declared_end_word_maps']]==[(632,648)]
    block['target_block_sha256']=block.pop('research_block_sha256')
    block.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],
        external_entry_and_actual_revised_paths_approval_pending=False,individual_naturally_selected_source_scene_unobserved=True,
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[])
    parent=NdsImage.open(PARENT)
    mapping=dict(format='dk4-lil-B182-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(parent.read_file('/__arm9__.bin')),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[block],**{f:True for f in FLAGS},
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[],representative_proof=str(sample),
        source_plan=str(PLAN),source_census=str(CENSUS),final_padding_proof=str(STORED),relocated_control_proof=str(CONTROL),
        termination_decode_proof=str(ENDS),postscene_native_state_proof=str(VISUAL),
        evidence={**evidence,str(sample):sha(sample.read_bytes())},actual_selected_B182_source_events=[],full_goal_complete=False)
    save(MAP,mapping)
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),reference_map_pending=False,
        registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for key,path in [('reference_map',MAP),('representative_proof',sample),('final_padding_proof',STORED),('relocated_control_proof',CONTROL),
        ('termination_decode_proof',ENDS),('postscene_native_state_proof',VISUAL)]:doc[key],doc[key+'_sha256']=str(path),sha(path.read_bytes())
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
        evidence={**evidence,str(MAP):sha(MAP.read_bytes()),str(sample):sha(sample.read_bytes())},
        all8_source_native_reference_and_representative_rules_approved=True,source_prose_English_unchanged=True,
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[],new_emulator_runs=2,total_frames=18002,
        new_editorial_credit=0,registered_release_and_current_startup_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B182 references sealed:8 actual panels,original conditional paths,RNG/effects,C200,end and normal return. Registered integration pending;zero credit yet.')
