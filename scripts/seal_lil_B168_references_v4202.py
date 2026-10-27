"""Seal all54 reviews with exact relocation and scoped progressive/FE/effect coverage."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B168_research_v4192 import ROM, PARENT, PLAN
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B168_reference_approval_v4202')
INPUT = Path('translations/lil_B168_editorial_manuscript_v7.json')
OUTPUT = Path('translations/lil_B168_editorial_manuscript_v8.json')
MAP = Path('translations/lil_B168_editorial_relocation_map_v1.json')
CENSUS = Path('work/analysis/lil_B168_reference_census_v4195/all82_commands12_relative_sites_and_shipped_entry_census.json')
CONTROL = Path('work/analysis/lil_B168_relocated_controls_v4197/all54_progressive_FE_dispatches_three_predicates_and16_leaves.json')
STORED = Path('work/analysis/lil_B168_stored_v4191/all54_final_stored_targets216_macro_cases_and_complete_planes.json')
ENDS = Path('work/analysis/lil_B168_ends_v4196/four_declared_end_decodes_and_all12_in_block_relative_destinations.json')
ACTUAL = Path('work/analysis/lil_B168_actual_v4200/actual_progressive_FE_three_predicates_full_effect_and_return.json')
FIXTURE = Path('work/analysis/lil_B168_display_fixture_v4198/complete_effect_preserving_B22_fixtures.json')
VISUAL = Path('work/analysis/lil_B168_transition_review_v4201/all9_sheets_contact_FE_source_effect_and_paired_return_review.json')

if __name__ == '__main__':
    assert not any(path.exists() for path in [ROOT, MAP, OUTPUT])
    doc = deepcopy(read(INPUT))
    plan, census, control, stored, ends, actual, fixture, visual = map(read, [PLAN, CENSUS, CONTROL, STORED, ENDS, ACTUAL, FIXTURE, VISUAL])
    parent, image = NdsImage.open(PARENT), NdsImage.open(ROM)
    assert sha(PARENT.read_bytes()) == doc['current_ROM_sha256'] == plan['candidate_sha256']
    assert sha(ROM.read_bytes()) == census['research_ROM_sha256'] == control['research_ROM_sha256'] == ends['research_ROM_sha256']
    assert sha(INPUT.read_bytes()) == plan['manuscript_sha256'] == stored['manuscript_sha256'] == control['manuscript_sha256']
    assert census['all82_clean_current_target_commands_and12_relative_sites_reexecuted']
    assert census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert len(control['relocated_dispatch_cases']) == 54 and len(control['relocated_predicate_pairs']) == 3
    assert len(control['all16_source_current_target_nonrelative_nonspeech_leaves']) == 16
    assert control['all_three_unforced_predicates_match_copied_source_state_without_roster_fixture']
    assert stored['current_final_stored_macro_alignment_cases'] == 216 and len(stored['final_target_parity_cases']) == 54
    assert stored['all54_final_targets_complete_native_planes_equal_reviewed_planes']
    assert ends['all4_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases']) == 4
    assert actual['fresh_actual_unique_speech_panels'] == actual['complete_matching_observations'] == 51 and not actual['failures']
    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope']
    assert visual['no_open_translation_specific_display_or_control_finding']
    assert len(visual['all9_actual_sheets_viewed']) == 9 and len(visual['English_full_screen_views']) == 5
    assert len(visual['paired_source_English_whole_RGB_returns']) == 1
    assert fixture['source_B168_later_A000_and_all_resources_presentations_and_FE_notices_preserved']
    assert all(not row['explicitly_excluded_original_commands'] for row in fixture['fixtures'])
    native = read(doc['native_font_proof'])
    assert native['all54_current_native_speech_planes_pass'] and native['current_original_macro_alignment_calls'] == 432
    ids = [row['id'] for row in actual['actual_panels']]
    offline = actual['offline_only_display_IDs']
    assert offline == ['DK4_MES_B168_R0020', 'DK4_MES_B168_R0048', 'DK4_MES_B168_R0135']
    assert set(ids + offline) == {row['id'] for row in doc['records']}
    ROOT.mkdir(parents=True)
    paths = [INPUT, PLAN, CENSUS, CONTROL, STORED, ENDS, ACTUAL, FIXTURE, VISUAL, Path(__file__)]
    evidence = {str(path): sha(path.read_bytes()) for path in paths}
    sample = ROOT / 'representative_display_control_and_transition_reconciliation.json'
    save(sample, dict(candidate=str(PARENT), candidate_sha256=sha(PARENT.read_bytes()), research_ROM=str(ROM), research_ROM_sha256=sha(ROM.read_bytes()),
        evidence=evidence, viewed_actual_sheets=visual['all9_actual_sheets_viewed'], actual_two_disclosed_cold_boots_pass=True,
        actual_selected_B168_source_events=[], actual_sampled_display_IDs=ids, offline_only_display_IDs=offline,
        offline_only_display_cases=visual['offline_only_display_cases'], represented_reviewed_display_IDs=ids + offline,
        actual51_panels_three_FE_and_normal_return_pass=True, original_three_unforced_queries_twelve_spans_and_later_effect_preserved=True,
        three_conditional_remarks_not_actual_or_byte_identical_reuse=True, no_B168_source_command_omitted=True,
        original_B22_four_A000_initialization_commands_retained=True, no_open_translation_specific_display_or_control_finding=True,
        individual_conditional_visits_not_required_under_user_policy=True, new_emulator_runs=2,
        registered_release_and_current_startup_pending=True, full_goal_complete=False))
    block = deepcopy(plan['blocks'][0])
    checked = census['blocks'][0]
    assert block['block'] == checked['block'] == 168
    block['target_block_sha256'] = block.pop('research_block_sha256')
    block.update(external_references_complete=True, entry_point_offset=8, mapped_native_commands=checked['mapped_commands'],
        external_entry_and_actual_revised_paths_approval_pending=False, individual_naturally_selected_source_scene_unobserved=True)
    assert len(block['command_map']) == 82 and len(block['relative_skip_fixups']) == 12
    assert len(block['target_native_skip_cases']) == 60 and len(block['text_records']) == 54
    assert not block['choice_commands'] and not block['actor_style_commands'] and not block['original2000_pause_and_resume_maps']
    assert [end['source_offset'] for end in block['original_declared_end_word_maps']] == [2906, 2910]
    mapping = dict(format='dk4-lil-B168-source-relocation-map-v1', required_runtime_ARM9_sha256=sha(parent.read_file('/__arm9__.bin')),
        source_SC2_sha256=plan['source_SC2_sha256'], target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8, preserve_record_parity=True, external_references_complete=True, blocks=[block],
        all82_commands12_relative_sites60_target_skips_verified=True, all54_active_speech_targets_preserved=True,
        all16_leaves_three_predicates_four_resources_six_presentations_one_effect_and_two_ends_exact=True,
        two_consecutive_declared_endwords_preserved=True, three_FE_null_actor_consumers_and_FI7_FA1_FO1_preserved=True,
        no_source2000_2100_4100_C200_or_dynamic_objects=True, representative_shared_rules_approved=True,
        representative_proof=str(sample), source_plan=str(PLAN), source_census=str(CENSUS), final_padding_proof=str(STORED),
        relocated_control_proof=str(CONTROL), termination_decode_proof=str(ENDS), evidence={**evidence, str(sample): sha(sample.read_bytes())},
        actual_selected_B168_source_events=[], individual_conditional_visits_not_required_under_user_policy=True, full_goal_complete=False)
    save(MAP, mapping)
    doc.update(previous_manuscript=str(INPUT), previous_manuscript_sha256=sha(INPUT.read_bytes()), reference_map_pending=False,
        registered_integration_pending=True, status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for key, path in [('reference_map', MAP), ('representative_proof', sample), ('final_padding_proof', STORED),
                      ('relocated_control_proof', CONTROL), ('termination_decode_proof', ENDS)]:
        doc[key], doc[key + '_sha256'] = str(path), sha(path.read_bytes())
    for row in doc['records']:
        row.update(status=doc['status'], current_text_hex=row['current_hex'],
            native_display_consumer='original_null_actor_FE_5473C' if row['kind'] == 'system-FE' else 'original_progressive_54020',
            actual_B22_display_fixture_observed=row['id'] in ids, offline_only_native_display_checked=row['id'] in offline,
            individual_actual_source_event_activation_not_claimed=True)
    assert [row['english'] for row in doc['records']] == [row['english'] for row in read(INPUT)['records']]
    validate_natural_dialogue_batch(doc)
    save(OUTPUT, doc)
    save(ROOT / 'approval_receipt.json', dict(manuscripts={str(OUTPUT): sha(OUTPUT.read_bytes())}, reference_map=str(MAP),
        reference_map_sha256=sha(MAP.read_bytes()), evidence={**evidence, str(MAP): sha(MAP.read_bytes()), str(sample): sha(sample.read_bytes())},
        all54_source_native_reference_and_representative_rules_approved=True, source_prose_English_unchanged=True,
        actual_sampled_display_IDs=ids, offline_only_display_IDs=offline, new_emulator_runs=2,
        registered_release_and_current_startup_pending=True, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print('54 approvals sealed:51 actual/three offline remarks,three FE,82commands/12spans/60skips/216storedcases. Registered integration pending.')
