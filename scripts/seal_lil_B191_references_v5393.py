"""Source/native/actual B191 approval with original conditional outcomes disclosed."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B191_research_v5380 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B191_reference_approval_v5393')
INPUT=Path('translations/lil_B191_editorial_manuscript_v4.json')
OUTPUT=Path('translations/lil_B191_editorial_manuscript_v5.json')
MAP=Path('translations/lil_B191_editorial_relocation_map_v1.json')
CENSUS=Path('work/analysis/lil_B191_reference_census_v5383/all38_commands_sixteen_relative_sites_and_shipped_entry_census.json')
CONTROL=Path('work/analysis/lil_B191_relocated_controls_v5385/all13_dispatches_three_RNG_predicates_four_effects_C200_and125_mapped_paths.json')
STORED=Path('work/analysis/lil_B191_stored_v5378b/all13_final_stored_targets52_macro_cases_and_complete_planes.json')
ENDS=Path('work/analysis/lil_B191_ends_v5384/two_declared_tail_end_decodes_sixteen_relative_sites.json')
ACTUAL=Path('work/analysis/lil_B191_actual_v5389/actual_all13_progressive_FE_RNG_effect_or_no_effect_C200_and_single_end.json')
FIXTURE=Path('work/analysis/lil_B191_display_fixture_v5386/complete_B191_B22_fixtures.json')
VISUAL=Path('work/analysis/lil_B191_actual_review_v5390/all13_panels_20_fullscreens_no_effect_path_return_and_measured_differences.json')
FLAGS=['all38_structural_commands_verified', 'all13_active_speech_targets_preserved', 'all9_nonrelative_leaves_three_mixed_predicates_four_A000_C200_end_exact', 'all16_relative_sites_and80_native_skip_cases_preserved', 'all125_mapped_structural_paths_preserve_all13_speeches_and_no_effect_paths', 'progressive12_impersonal_FE1_and_FI0_FA0_FO0_preserved', 'single_end730_target676_preserved', 'no_source2000_pause_2100_4100_resources_or_presentations', 'original_mixed_RNG_semantics_and_packed_effect_bytes_preserved', 'source_and_target_prefix6_to128_byte_exact', 'exact_R64_source_prose_wrap_preserved', 'representative_actual_display_controls_and_parent_return_approved']

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,OUTPUT,MAP])
    doc=deepcopy(read(INPUT));plan,census,control,stored,ends,actual,fixture,visual=map(read,[PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL])
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']
    assert sha(ROM.read_bytes())==census['research_ROM_sha256']==control['research_ROM_sha256']==ends['research_ROM_sha256']
    assert sha(INPUT.read_bytes())==plan['manuscript_sha256']==stored['manuscript_sha256']==control['evidence'][str(INPUT)]
    assert census['all38_clean_current_target_commands_and_sixteen_relative_sites_reexecuted']
    assert census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert len(control['relocated_dispatch_cases'])==13 and len(control['all9_exact_nonrelative_leaves'])==9
    assert len(control['predicate_pairs'])==3 and len(control['C200_pairs'])==1 and len(control['A000_structural_pairs'])==4
    assert len(control['all125_source_and_relocated_structural_paths_identical'])==125
    scratch=read('work/analysis/lil_B191_predicates_v5379/all36_original_mixed_predicate_ownership_cases.json')
    assert len(scratch['cases'])==36 and scratch['unforced_cases']==9 and scratch['CPU_only_boundary_fixture_cases']==27
    assert scratch['actual_emulator_seed_writes']==0 and all(r['full4MiB_difference_exactly_original_owned_RNG_and_optional_operand_scratch'] for r in scratch['cases'])
    assert sum(r['operand_pointer_unaligned'] for r in scratch['cases'])==0
    assert len(stored['final_target_parity_cases'])==13 and stored['current_final_stored_macro_alignment_cases']==52
    assert (stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(12,40)
    assert stored['all13_final_targets_complete_native_planes_equal_reviewed_planes']
    assert ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==13
    assert not actual['failures'] and not actual['paired_region_differences'] and not actual['offline_only_display_IDs']
    assert [v['fixture_exit_frame'] for v in actual['versions']]==[5977,5975]
    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and visual['no_translation_specific_glyph_bounds_pagination_portrait_or_return_finding']
    assert visual['observed_random_path_difference']['same_control_path']
    assert visual['observed_random_path_difference']['original_effects_by_case']=={'clean_Japanese':[],'reviewed_English':[]}
    assert visual['exact_timing_difference_counts']==dict(total=12,speech=10,control_or_end=2)
    assert len(visual['sampled_postscene_whole_RGB_differences_unmasked'])==4
    assert [(r['frame'],r['whole_frame_difference_bbox']) for r in visual['sampled_postscene_whole_RGB_differences_unmasked']]==[(6730,[225,371,239,376]),(6910,[225,371,239,376]),(7690,[224,360,240,376]),(7870,[224,360,240,376])]
    assert visual['postscene9001_PRNG_seeds']==[759362961,1803218166] and not visual['PRNG_equality']
    assert all(visual['postscene9001_native_component_equality'].values()) and visual['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert visual['whole_RGB_final9001_equal']
    assert visual['nontext_equal_samples']==len(visual['all115_sampled_nontext_region_checks'])==115
    assert len(visual['all_actual_consumer_sheets_viewed'])==3 and len(visual['paired_full_screen_views'])==5
    assert all(s['viewed_after_image_return'] for s in visual['all_actual_consumer_sheets_viewed']+visual['paired_full_screen_views'])
    assert visual['total_frames']==18002 and visual['actual_new_cold_boot_runs']==2
    assert fixture['source_all38_commands_preserved_without_omission_or_flattening']
    assert all(not f['explicitly_excluded_original_commands'] and len(f['all47_stored_fixture_commands'])==47 for f in fixture['fixtures'])
    ids=[r['id'] for r in actual['actual_panels']];assert ids==[r['id'] for r in doc['records']] and len(set(ids))==13
    for p,h in visual['evidence'].items():assert sha(Path(p).read_bytes())==h
    for sheet in visual['all_actual_consumer_sheets_viewed']+visual['paired_full_screen_views']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    carry=Path('work/analysis/lil_B191_carried_result_v5392/all15_C200_and15_end_prior_result_cases.json');carried=read(carry)
    assert len(carried['cases'])==15 and visual['original_carried_result2_C200_3_2_and_end_0_2_preserved']
    layout=Path('work/analysis/lil_B191_relocation_tools_v5377/viewed_layout_retention_reasons.json')
    assert read(layout)['all13_panels_on_two_native_sheets_viewed_after_image_return']
    wrap=Path(doc['source_bound_wrap_refinement_proof']);w=read(wrap)
    assert sha(wrap.read_bytes())==doc['source_bound_wrap_refinement_proof_sha256'] and w['only_changed_record_IDs']==['DK4_MES_B191_R0064']
    assert w['all13_words_controls_and_prose_unchanged'] and w['twelve_other_compiled_targets_exact'] and w['twelve_other_native_planes_exact']
    assert doc['exact_source_prose_R64_after_be_boundary_reviewed'] and not doc['no_record_specific_ordinary_boundary_exception_required']
    sourceblock=IlnkContainer.parse(NdsImage.open(PARENT).read_file('/data/SC2.DK4')).blocks[191]
    targetblock=IlnkContainer.parse(NdsImage.open(ROM).read_file('/data/SC2.DK4')).blocks[191]
    assert sourceblock[6:128]==targetblock[6:128] and len(sourceblock)==736 and len(targetblock)==680
    assert plan['blocks'][0]['research_logical_end']==680 and plan['blocks'][0]['source_logical_end']==734
    assert visual['both_actual_rolls875_988_at8_76_return2_skip700_at28_and_apply_no_source_A000']
    assert visual['four_source_effect_alternatives_native_structural_only_not_actually_executed']
    paths=[wrap,carry,layout,INPUT,PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL,Path('work/analysis/lil_B191_predicates_v5379/all36_original_mixed_predicate_ownership_cases.json'),Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in paths};ROOT.mkdir(parents=True)
    sample=ROOT/'representative_display_control_and_transition_reconciliation.json'
    save(sample,dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        evidence=evidence,viewed_actual_sheets=visual['all_actual_consumer_sheets_viewed'],actual_sampled_display_IDs=ids,
        represented_reviewed_display_IDs=ids,offline_only_display_IDs=[],actual_selected_B191_source_events=[],
        all13_panels_twelve_progressive_one_FE_original_no_effect_path_C200_end_and_parent_return_pass=True,
        source_all38_commands_16_branches_three_mixed_predicates_four_alternative_effects_and_no_effect_paths_preserved=True,
        actual_conditional_paths_verified_without_forcing_same_outcome=True,
        original_scene_two_unforced500_draws_skip700_and_no_A000_preserved=True,
        no_open_translation_specific_display_or_control_finding=True,new_emulator_runs=2,total_frames=18002,
        no_natural_event_eligibility_earned_fashion_state_prior_location_future_world_full_RAM_or_hardware_claim=True,
        registered_release_and_current_startup_pending=True,full_goal_complete=False))
    block=deepcopy(plan['blocks'][0]);checked=census['blocks'][0]
    assert block['block']==checked['block']==191 and len(block['command_map'])==38 and len(block['text_records'])==13
    assert len(block['relative_skip_fixups'])==16 and len(block['target_native_skip_cases'])==80
    assert [(e['source_offset'],e['target_offset']) for e in block['original_declared_end_word_maps']]==[(730,676)]
    block['target_block_sha256']=block.pop('research_block_sha256')
    block.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],
        external_entry_and_actual_revised_paths_approval_pending=False,individual_naturally_selected_source_scene_unobserved=True,
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[])
    parent=NdsImage.open(PARENT)
    mapping=dict(format='dk4-lil-B191-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(parent.read_file('/__arm9__.bin')),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[block],**{f:True for f in FLAGS},
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[],representative_proof=str(sample),
        source_plan=str(PLAN),source_census=str(CENSUS),final_padding_proof=str(STORED),relocated_control_proof=str(CONTROL),
        termination_decode_proof=str(ENDS),postscene_native_state_proof=str(VISUAL),
        evidence={**evidence,str(sample):sha(sample.read_bytes())},actual_selected_B191_source_events=[],full_goal_complete=False)
    save(MAP,mapping)
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),reference_map_pending=False,
        registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for key,path in [('layout_retention_review_proof',layout),('carried_result_proof',carry),('reference_map',MAP),('representative_proof',sample),('final_padding_proof',STORED),('relocated_control_proof',CONTROL),
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
        all13_source_native_reference_and_representative_rules_approved=True,source_prose_English_unchanged=True,
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[],new_emulator_runs=2,total_frames=18002,
        new_editorial_credit=0,registered_release_and_current_startup_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B191 references sealed:13 actual panels,original conditional paths,RNG/effects,C200,end and normal return. Registered integration pending;zero credit yet.')
