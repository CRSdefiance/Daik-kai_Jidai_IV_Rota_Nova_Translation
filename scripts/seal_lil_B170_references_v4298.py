"""Seal all33 B170 reviews with exact relocation and scoped gameplay evidence."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B170_research_v4283 import ROM, PARENT, PLAN
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B170_reference_approval_v4298')
INPUT = Path('translations/lil_B170_editorial_manuscript_v5.json')
OUTPUT = Path('translations/lil_B170_editorial_manuscript_v6.json')
MAP = Path('translations/lil_B170_editorial_relocation_map_v1.json')
CENSUS = Path('work/analysis/lil_B170_reference_census_v4286/all45_commands_zero_relative_sites_and_shipped_entry_census.json')
CONTROL = Path('work/analysis/lil_B170_relocated_controls_v4288/all33_progressive_dispatches_C200_pause_and12_leaves.json')
STORED = Path('work/analysis/lil_B170_stored_v4282/all33_final_stored_targets132_macro_cases_and_complete_planes.json')
ENDS = Path('work/analysis/lil_B170_ends_v4287/four_declared_end_decodes_and_zero_relative_sites.json')
ACTUAL = Path('work/analysis/lil_B170_actual_v4293/actual_all33_pause_resources_A000_C200_and_first_end.json')
FIXTURE = Path('work/analysis/lil_B170_display_fixture_v4291/complete_effect_preserving_B22_fixtures.json')
VISUAL = Path('work/analysis/lil_B170_transition_review_v4297/all6_sheets_figure_pause_effect_C200_and_paired_return_review.json')
REPEAT = Path('work/analysis/lil_B170_repeat_verification_v4296d/post_B170_actor_captain_and_same_ROM_repeat_comparison.json')

if __name__ == '__main__':
    assert not any(path.exists() for path in [ROOT, MAP, OUTPUT])
    doc = deepcopy(read(INPUT))
    plan, census, control, stored, ends, actual, fixture, visual, repeat = map(read, [PLAN, CENSUS, CONTROL, STORED, ENDS, ACTUAL, FIXTURE, VISUAL, REPEAT])
    parent, image = NdsImage.open(PARENT), NdsImage.open(ROM)
    assert sha(PARENT.read_bytes()) == doc['current_ROM_sha256'] == plan['candidate_sha256']
    assert sha(ROM.read_bytes()) == census['research_ROM_sha256'] == control['research_ROM_sha256'] == ends['research_ROM_sha256']
    assert sha(INPUT.read_bytes()) == plan['manuscript_sha256'] == stored['manuscript_sha256'] == control['manuscript_sha256']
    assert census['all45_clean_current_target_commands_and_zero_relative_sites_reexecuted']
    assert census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert len(control['relocated_dispatch_cases']) == 33 and not control['relocated_predicate_pairs']
    assert len(control['all12_source_current_target_nonrelative_nonspeech_leaves']) == 12
    assert len(control['relocated_C200_pairs']) == 1 and control['original_C200_queue_and_all_unowned4MiB_preserved_at_relocated_cursor']
    assert control['source_A000_hex'] == '00a0ffff19100120'
    assert stored['current_final_stored_macro_alignment_cases'] == 132 and len(stored['final_target_parity_cases']) == 33
    assert stored['all33_final_targets_complete_native_planes_equal_reviewed_planes']
    assert ends['all4_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases']) == 4
    assert actual['fresh_actual_unique_speech_panels'] == actual['complete_matching_observations'] == 33
    assert not actual['failures'] and not actual['paired_region_differences'] and not actual['offline_only_display_IDs']
    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope']
    assert visual['no_open_translation_specific_display_or_control_finding']
    assert len(visual['all6_actual_sheets_viewed']) == 6 and len(visual['English_full_screen_views']) == 4
    assert len(visual['Japanese_full_screen_views']) == 3 and len(visual['paired_source_English_whole_RGB_pause_and_returns']) == 2
    assert visual['first_end1852_actual_second_end1856_stored_and_native_decoder_only']
    assert fixture['source_B170_later_A000_hex1019_2001_resources_presentations_pause_C200_and_both_ends_retained']
    assert all(not row['explicitly_excluded_original_commands'] for row in fixture['fixtures'])
    assert repeat['paired_post_B170_town11290_whole1A04_actor_models_and_captain2_equal']
    assert repeat['cross_language_command_order_results_and_first_end_equal']
    assert len(repeat['cross_language_speech_timing_differences']) == 22
    assert not any(repeat['same_ROM_later_differing_frames'].values())
    assert all(all(row['component_equality'].values()) for row in repeat['paired_native_persistent_state_and_PRNG_samples'] if row['frame'] <= 16090)
    native = read(doc['native_font_proof'])
    assert native['all33_current_native_speech_planes_pass'] and native['current_original_macro_alignment_calls'] == 264
    ids = [row['id'] for row in actual['actual_panels']]
    assert set(ids) == {row['id'] for row in doc['records']}
    ROOT.mkdir(parents=True)
    paths = [INPUT, PLAN, CENSUS, CONTROL, STORED, ENDS, ACTUAL, FIXTURE, VISUAL, REPEAT, Path(__file__)]
    evidence = {str(path): sha(path.read_bytes()) for path in paths}
    sample = ROOT / 'representative_display_control_and_transition_reconciliation.json'
    save(sample, dict(candidate=str(PARENT), candidate_sha256=sha(PARENT.read_bytes()), research_ROM=str(ROM), research_ROM_sha256=sha(ROM.read_bytes()),
        evidence=evidence, viewed_actual_sheets=visual['all6_actual_sheets_viewed'], actual_two_disclosed_content_cold_boots_pass=True,
        two_additional_focused_repeats_postscene_state_and_PRNG_checked=True,
        actual_selected_B170_source_events=[], actual_sampled_display_IDs=ids, offline_only_display_IDs=[], represented_reviewed_display_IDs=ids,
        actual33_progressive_panels_figure_pause_resources_A000_C200_first_end_and_normal_town_return_pass=True,
        original45_commands_and_both_declared_endwords_preserved=True, no_B170_source_command_omitted=True,
        first_end1852_actual_second1856_native_decoder_only=True,
        original_B22_four_A000_initialization_commands_retained=True, no_open_translation_specific_display_or_control_finding=True,
        later67_SeaView_differences_preserved_with_explicit_inference_and_state_scope=True,
        source_A000_packed_semantics_or_earned_recruitment_not_inferred=True,
        new_emulator_runs=4, registered_release_and_current_startup_pending=True, full_goal_complete=False))
    block = deepcopy(plan['blocks'][0])
    checked = census['blocks'][0]
    assert block['block'] == checked['block'] == 170
    block['target_block_sha256'] = block.pop('research_block_sha256')
    block.update(external_references_complete=True, entry_point_offset=8, mapped_native_commands=checked['mapped_commands'],
        external_entry_and_actual_revised_paths_approval_pending=False, individual_naturally_selected_source_scene_unobserved=True)
    assert len(block['command_map']) == 45 and not block['relative_skip_fixups'] and not block['target_native_skip_cases']
    assert len(block['text_records']) == 33 and not block['choice_commands'] and not block['actor_style_commands']
    assert block['original2000_pause_and_resume_maps'] == [dict(old_offset=36, new_offset=32, source_resume=38, target_resume=34, source_two_byte_pause_and_mapped_resumption_boundary_exact=True)]
    assert [end['source_offset'] for end in block['original_declared_end_word_maps']] == [1852, 1856]
    assert [end['target_offset'] for end in block['original_declared_end_word_maps']] == [1742, 1746]
    mapping = dict(format='dk4-lil-B170-source-relocation-map-v1', required_runtime_ARM9_sha256=sha(parent.read_file('/__arm9__.bin')),
        source_SC2_sha256=plan['source_SC2_sha256'], target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8, preserve_record_parity=True, external_references_complete=True, blocks=[block],
        all45_commands_zero_relative_sites_zero_predicates_verified=True, all33_active_speech_targets_preserved=True,
        all12_leaves_two_resources_pause_A000_C200_and_both_ends_exact=True,
        both_consecutive_declared_endwords_preserved=True, no_FE_consumers_and_FI1_FO1_preserved=True,
        no_source2100_4100_or_dynamic_objects=True, representative_shared_rules_approved=True,
        source_A000_hex='00a0ffff19100120', source_A000_raw_hex_words=['1019', '2001'], source_packed_semantics_not_inferred=True,
        representative_proof=str(sample), source_plan=str(PLAN), source_census=str(CENSUS), final_padding_proof=str(STORED),
        relocated_control_proof=str(CONTROL), termination_decode_proof=str(ENDS), focused_repeat_proof=str(REPEAT),
        evidence={**evidence, str(sample): sha(sample.read_bytes())}, actual_selected_B170_source_events=[], full_goal_complete=False)
    save(MAP, mapping)
    doc.update(previous_manuscript=str(INPUT), previous_manuscript_sha256=sha(INPUT.read_bytes()), reference_map_pending=False,
        registered_integration_pending=True, status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for key, path in [('reference_map', MAP), ('representative_proof', sample), ('final_padding_proof', STORED),
                      ('relocated_control_proof', CONTROL), ('termination_decode_proof', ENDS), ('focused_repeat_proof', REPEAT)]:
        doc[key], doc[key + '_sha256'] = str(path), sha(path.read_bytes())
    for row in doc['records']:
        assert row['kind'] == 'progressive'
        row.update(status=doc['status'], current_text_hex=row['current_hex'], native_display_consumer='original_progressive_54020',
            actual_B22_display_fixture_observed=True, offline_only_native_display_checked=False,
            individual_actual_source_event_activation_not_claimed=True)
    assert [row['english'] for row in doc['records']] == [row['english'] for row in read(INPUT)['records']]
    validate_natural_dialogue_batch(doc)
    save(OUTPUT, doc)
    save(ROOT / 'approval_receipt.json', dict(manuscripts={str(OUTPUT): sha(OUTPUT.read_bytes())}, reference_map=str(MAP),
        reference_map_sha256=sha(MAP.read_bytes()), evidence={**evidence, str(MAP): sha(MAP.read_bytes()), str(sample): sha(sample.read_bytes())},
        all33_source_native_reference_and_representative_rules_approved=True, source_prose_English_unchanged=True,
        actual_sampled_display_IDs=ids, offline_only_display_IDs=[], new_emulator_runs=4,
        registered_release_and_current_startup_pending=True, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print('All33 B170 approvals sealed:45commands,12leaves,132storedcases,figure/pause/A000/C200/firstend/town return. Four boots;later sailing differences explicitly scoped. Registered integration pending.')
