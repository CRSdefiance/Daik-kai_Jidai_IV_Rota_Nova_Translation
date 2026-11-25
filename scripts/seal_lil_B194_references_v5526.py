"""Seal all11 approved objects after exact relocation and both viewed unforced actual paths."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B194_research_v5508 import ROM, PARENT, PLAN
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B194_reference_approval_v5526')
INPUT = Path('translations/lil_B194_editorial_manuscript_v3.json')
OUTPUT = Path('translations/lil_B194_editorial_manuscript_v4.json')
MAP = Path('translations/lil_B194_editorial_relocation_map_v1.json')
CENSUS = Path('work/analysis/lil_B194_reference_census_v5511/all21_commands_four_relative_sites_and_shipped_entry_census.json')
CONTROL = Path('work/analysis/lil_B194_relocated_controls_v5513/all11_dispatches_changed_predicate_alignment_resource42_two_UI_and_paths.json')
STORED = Path('work/analysis/lil_B194_stored_v5507/all11_final_stored_targets44_macro_cases_and_complete_planes.json')
ENDS = Path('work/analysis/lil_B194_ends_v5512/two_declared_tail_end_decodes_four_relative_sites.json')
VISUAL = Path('work/analysis/lil_B194_actual_views_v5525/both_unforced_paths_all11_panels24_fullscreens_and_normal_returns_viewed.json')
BINDING = Path('work/analysis/lil_B194_recruitment_binding_v5518/source_B165_Julio6_recruitment_initializer_disclosed_for_conditional_test.json')
FLAGS = ['all21_structural_commands_verified', 'all11_active_speech_targets_preserved',
         'all6_leaves_A000_predicate_resource42_two_C200_and_single_end_exact',
         'single_declared_tail_endword_preserved', 'progressive10_impersonal_FE1_and_FI1_FA0_FO0_preserved',
         'all4_relative_sites_and20_target_native_skip_cases_verified',
         'changed_predicate_alignment_has_exact_owned_scratch_restore',
         'source_A000_raw_operand_bytes_preserved_without_inferred_semantics',
         'single_end536_actual_target510_offline', 'representative_shared_rules_approved']

if __name__ == '__main__':
    assert not any(p.exists() for p in [ROOT, OUTPUT, MAP])
    doc = deepcopy(read(INPUT))
    plan, census, control, stored, ends, visual, binding = map(read, [PLAN, CENSUS, CONTROL, STORED, ENDS, VISUAL, BINDING])
    assert sha(PARENT.read_bytes()) == doc['current_ROM_sha256'] == plan['candidate_sha256']
    assert sha(ROM.read_bytes()) == census['research_ROM_sha256'] == control['research_ROM_sha256'] == ends['research_ROM_sha256']
    assert sha(INPUT.read_bytes()) == plan['manuscript_sha256'] == stored['manuscript_sha256'] == control['manuscript_sha256']
    assert census['all21_clean_current_target_commands_and_four_relative_sites_reexecuted']
    assert census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert len(control['relocated_dispatch_cases']) == 11 and len(control['all6_source_current_target_nonrelative_nonspeech_leaves']) == 6
    assert len(control['unforced_relocated_predicate_cases']) == 1
    assert control['changed_unaligned_operand_scratch_owned_and_restored']
    assert len(control['relocated_C200_prior_result_cases']) == len(control['relocated_resource42_prior_result_cases']) == 10
    assert len(control['relocated_end_prior_result_cases']) == 5
    assert [len(p['speech_record_indices']) for p in control['relocated_structural_predicate0_1_paths']] == [9, 11]
    assert stored['current_final_stored_macro_alignment_cases'] == 44
    assert stored['all11_final_targets_complete_native_planes_equal_reviewed_planes']
    assert (stored['new_parity_macro_alignment_cases'], stored['exact_byte_identical_reused_macro_alignment_cases']) == (20, 24)
    assert ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope']
    assert visual['no_open_translation_specific_display_or_control_finding'] and not visual['visual_review_pending']
    assert (visual['unique_actual_display_objects'], visual['actual_panel_observations_across_setups'], visual['total_paired_fullscreen_views']) == (11, 20, 24)
    assert visual['all_content_jobs_terminal_and_reaped'] and visual['total_frames'] == 36004
    ids = [r['id'] for r in doc['records']]
    assert visual['actual_sampled_display_IDs'] == ids and not visual['offline_only_display_IDs']
    assert binding['original_command_hex'] == '00a0ffff06100120' and binding['source_block'] == 165
    assert binding['candidate_sha256'] == doc['current_ROM_sha256']
    for v in visual['versions']:
        actual = read(v['actual_proof'])
        analysis = read(v['visual_analysis'])
        assert sha(Path(v['actual_proof']).read_bytes()) == v['actual_proof_sha256']
        assert sha(Path(v['visual_analysis']).read_bytes()) == v['visual_analysis_sha256']
        assert len(v['viewed_sheets']) == 5 and all(s['viewed_after_image_return'] for s in v['viewed_sheets'])
        assert v['timing_differences'] == dict(total=0, speech=0, control_or_end=0)
        assert v['sampled_nontext_pairs'] == 115 and v['sampled_postscene_and_final_RGB_equal']
        assert v['all_five_native_groups_and_whole1A04_actor_and_captain2_equal']
        assert v['final_PRNG_seeds'] == [3723009301, 3723009301]
        for p, h in analysis['evidence'].items():
            assert sha(Path(p).read_bytes()) == h
        for sheet in v['viewed_sheets']:
            assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
        assert not actual['failures'] and not actual['paired_region_differences']
    paths = [INPUT, PLAN, CENSUS, CONTROL, STORED, ENDS, VISUAL, BINDING, Path(__file__)]
    evidence = {str(p): sha(p.read_bytes()) for p in paths}
    ROOT.mkdir(parents=True)
    sample = ROOT / 'representative_display_control_and_transition_reconciliation.json'
    save(sample, dict(candidate=str(PARENT), candidate_sha256=sha(PARENT.read_bytes()),
        research_ROM=str(ROM), research_ROM_sha256=sha(ROM.read_bytes()), evidence=evidence,
        actual_sampled_display_IDs=ids, represented_reviewed_display_IDs=ids, offline_only_display_IDs=[],
        actual_selected_B194_source_events=[], all11_panels10_progressive1_FE_one_FI_and_normal_returns_pass=True,
        original21_commands_four_relative_sites_and_one_declared_end_preserved=True,
        default_source_availability0_and_original_recruitment_setup_availability1_observed_without_forcing=True,
        source_resource42_and_two_C200_paths_observed_in_conditional_setup=True,
        source_resource_command_executed_without_bridging_no_audible_output_claim=True,
        source_end536_target510_offline_and_both_fixture_ends_actually_reached=True,
        source_full_original_B22_initializers_and_one_B194_A000_preserved=True,
        extra_original_B165_recruitment_initializer_is_disclosed_test_setup_not_earned_progress=True,
        viewed_actual_sheets=[s for v in visual['versions'] for s in v['viewed_sheets']],
        complete_native_holds=[35, 44], paired_nontext_samples=230, fixture_return_frames=[[5017, 5017], [5737, 5737]],
        all_measured_timing_differences_zero=True, all_sampled_postscene_and_final9001_RGB_equal=True,
        five_native_state_groups_whole1A04_actor_captain2_and_measured_final_PRNG_equal_within_each_setup=True,
        default_Lil3_FI_verified_all_custom_name_lengths_unproved=True,
        no_open_translation_specific_display_or_control_finding=True,
        no_natural_event_eligibility_earned_state_earlier_location_full_route_full_RAM_future_world_or_hardware_claim=True,
        actual_new_cold_boot_runs=4, total_frames=36004, no_additional_focus_run_without_concrete_risk=True,
        registered_release_and_current_startup_pending=True, full_goal_complete=False))
    block = deepcopy(plan['blocks'][0])
    checked = census['blocks'][0]
    assert block['block'] == checked['block'] == 194 and len(block['command_map']) == 21 and len(block['text_records']) == 11
    assert len(block['relative_skip_fixups']) == 4 and len(block['target_native_skip_cases']) == 20
    assert not block['choice_commands'] and not block['actor_style_commands'] and not block['original2000_pause_and_resume_maps']
    assert [(e['source_offset'], e['target_offset']) for e in block['original_declared_end_word_maps']] == [(536, 510)]
    assert (block['source_bytes'], block['source_logical_end'], block['research_bytes'], block['research_logical_end']) == (540, 540, 516, 514)
    block['target_block_sha256'] = block.pop('research_block_sha256')
    block.update(external_references_complete=True, entry_point_offset=8, mapped_native_commands=checked['mapped_commands'],
                 external_entry_and_actual_revised_paths_approval_pending=False,
                 individual_naturally_selected_source_scene_unobserved=True, actual_sampled_display_IDs=ids, offline_only_display_IDs=[])
    parent = NdsImage.open(PARENT)
    mapping = dict(format='dk4-lil-B194-source-relocation-map-v1', required_runtime_ARM9_sha256=sha(parent.read_file('/__arm9__.bin')),
        source_SC2_sha256=plan['source_SC2_sha256'], target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8, preserve_record_parity=True, external_references_complete=True, blocks=[block],
        **{f: True for f in FLAGS}, actual_sampled_display_IDs=ids, offline_only_display_IDs=[],
        representative_proof=str(sample), source_plan=str(PLAN), source_census=str(CENSUS), final_padding_proof=str(STORED),
        relocated_control_proof=str(CONTROL), termination_decode_proof=str(ENDS), postscene_native_state_proof=str(VISUAL),
        original_recruitment_setup_binding=str(BINDING), evidence={**evidence, str(sample): sha(sample.read_bytes())},
        actual_selected_B194_source_events=[], full_goal_complete=False)
    save(MAP, mapping)
    doc.update(previous_manuscript=str(INPUT), previous_manuscript_sha256=sha(INPUT.read_bytes()), reference_map_pending=False,
               registered_integration_pending=True, status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for key, path in [('reference_map', MAP), ('representative_proof', sample), ('final_padding_proof', STORED),
                      ('relocated_control_proof', CONTROL), ('termination_decode_proof', ENDS), ('postscene_native_state_proof', VISUAL)]:
        doc[key], doc[key + '_sha256'] = str(path), sha(path.read_bytes())
    for row in doc['records']:
        row['historical_pre_actual_display_scope'] = {k: row[k] for k in ['current_complete_native_display_pending', 'current_native_UI_body_explicit_unexecuted_boundary'] if k in row}
        row.update(status=doc['status'], current_text_hex=row['current_hex'],
                   native_display_consumer='original_null_actor_FE_24310_then5473C' if row['kind'] == 'system-FE' else 'original_progressive_54020',
                   actual_B22_display_fixture_observed=True, offline_only_native_display_checked=False,
                   current_complete_native_display_pending=False, current_native_UI_body_explicit_unexecuted_boundary=False,
                   individual_actual_source_event_activation_not_claimed=True,
                   actual_conditional_setup_disclosed=(row['source_selector'] == 6))
    assert [r['english'] for r in doc['records']] == [r['english'] for r in read(INPUT)['records']]
    validate_natural_dialogue_batch(doc)
    save(OUTPUT, doc)
    save(ROOT / 'approval_receipt.json', dict(manuscripts={str(OUTPUT): sha(OUTPUT.read_bytes())},
        reference_map=str(MAP), reference_map_sha256=sha(MAP.read_bytes()),
        evidence={**evidence, str(MAP): sha(MAP.read_bytes()), str(sample): sha(sample.read_bytes())},
        all11_source_native_reference_and_representative_rules_approved=True, source_prose_English_unchanged=True,
        actual_sampled_display_IDs=ids, offline_only_display_IDs=[], actual_new_cold_boot_runs=4, total_frames=36004,
        new_editorial_credit=0, registered_release_and_current_startup_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print('B194 sealed:11 objects,21 commands,four branches,one FI,two unforced paths,79 native holds,230 pairs. Atomic compiler/registered integration remain pending;zero credit.')
