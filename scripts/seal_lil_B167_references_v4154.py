"""Seal 29 reviews with exact relocation and explicitly scoped representative coverage."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B167_research_v4141 import ROM, PARENT, PLAN
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B167_reference_approval_v4154')
INPUTS = [Path('translations/lil_B167_editorial_manuscript_v12.json'),Path('translations/lil_B167_choice_manuscript_v2.json')]
OUTPUTS = [Path('translations/lil_B167_editorial_manuscript_v13.json'),Path('translations/lil_B167_choice_manuscript_v3.json')]
MAP = Path('translations/lil_B167_editorial_relocation_map_v1.json')
CENSUS = Path('work/analysis/lil_B167_reference_census_v4144/all46_commands12_relative_sites_and_shipped_entry_census.json')
CONTROL = Path('work/analysis/lil_B167_relocated_controls_v4146/all27_dispatches_two_Cesare_predicates6_leaves_and_two_choice_getters.json')
STORED = Path('work/analysis/lil_B167_stored_v4140/all27_final_stored_targets108_macro_cases_and_complete_planes.json')
ENDS = Path('work/analysis/lil_B167_ends_v4145/four_declared_end_decodes_and_all12_in_block_relative_destinations.json')
ACTUAL = Path('work/analysis/lil_B167_actual_v4151/actual_both_choices_conditional_panels_and_distinct_returns.json')
FIXTURE = Path('work/analysis/lil_B167_display_fixture_v4147/complete_choice_preserving_B22_fixtures.json')
VISUAL = Path('work/analysis/lil_B167_transition_review_v4152/both_choices_all5_sheets_static_names_and_distinct_returns_review.json')
MENU = Path('work/analysis/lil_B167_choices_v4133/B167_C152/original_choice_decoder_VM_geometry_and_native_pixels.json')

if __name__ == '__main__':
    assert not any(p.exists() for p in [ROOT,MAP,*OUTPUTS])
    docs = [deepcopy(read(p)) for p in INPUTS]
    doc = docs[0]
    plan,census,control,stored,ends,actual,fixture,visual,menu = map(read,[PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL,MENU])
    parent,image = NdsImage.open(PARENT),NdsImage.open(ROM)
    assert sha(PARENT.read_bytes()) == doc['current_ROM_sha256'] == plan['candidate_sha256']
    assert sha(ROM.read_bytes()) == census['research_ROM_sha256'] == control['research_ROM_sha256'] == ends['research_ROM_sha256']
    assert sha(INPUTS[0].read_bytes()) == plan['manuscript_sha256'] == stored['manuscript_sha256'] == control['manuscript_sha256']
    assert sha(INPUTS[1].read_bytes()) == plan['choices_sha256']
    assert census['all46_clean_current_target_commands_and12_relative_sites_reexecuted']
    assert census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert len(control['relocated_dispatch_cases']) == 27 and len(control['relocated_predicate_pairs']) == 2
    assert len(control['all6_source_current_target_nonrelative_nonspeech_nonchoice_leaves']) == 6
    assert len(control['relocated_choice_getter_phases']) == 2 and control['both_unforced_Cesare_results_match_source_without_roster_fixture']
    assert stored['current_final_stored_macro_alignment_cases'] == 108 and len(stored['final_target_parity_cases']) == 27
    assert stored['all27_final_targets_complete_native_planes_equal_reviewed_planes']
    assert ends['all4_declared_end_decodes_return_type0_extent4_without_post_payload_read']
    assert ends['B167_first_end_precedes_second_end_and_declared_logical_end'] and len(ends['cases']) == 4
    assert actual['fresh_actual_unique_speech_panels'] == 25 and actual['complete_matching_observations'] == 28
    assert not actual['failures'] and actual['actual_new_cold_boot_runs'] == 4
    assert actual['both_real_choice_values_and_distinct_source_endwords_observed']
    assert visual['actual_proof_sha256'] == sha(ACTUAL.read_bytes())
    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope']
    assert len(visual['all5_actual_sheets_viewed']) == 5 and len(visual['English_full_screen_views']) == 8
    assert len(visual['Japanese_full_screen_views']) == 3 and len(visual['paired_source_English_whole_RGB_returns']) == 2
    assert menu['six_original_VM_selection_and_cancel_cases_pass'] and menu['eight_complete_native_style_label_planes_pass']
    assert fixture['all_original_choice_relative_containers_resources_and_both_ends_preserved']
    assert fixture['no_source_B167_A000_effect_to_omit']
    for path in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/data/EV2.DK4','/GRP/KANJI.FNT']:
        assert parent.read_file(path) == image.read_file(path)
    for sheet in visual['all5_actual_sheets_viewed'] + visual['English_full_screen_views'] + visual['Japanese_full_screen_views']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256'] and sheet['review'].startswith('Viewed')
    native = read(doc['native_font_proof'])
    assert native['all27_current_native_speech_planes_pass'] and native['current_original_macro_alignment_calls'] == 216
    ids = [r['id'] for r in actual['actual_panels']]
    offline = actual['offline_only_display_IDs']
    choiceids = [r['id'] for r in docs[1]['records']]
    assert offline == ['DK4_MES_B167_R0045','DK4_MES_B167_R0131'] and not set(ids) & set(offline)
    assert set(ids+offline) == {r['id'] for r in doc['records']} and len(choiceids) == 2
    ROOT.mkdir(parents=True)
    paths = [*INPUTS,PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL,MENU,Path(__file__)]
    evidence = {str(p):sha(p.read_bytes()) for p in paths}
    sample = ROOT / 'representative_display_control_and_transition_reconciliation.json'
    save(sample,dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),
        research_ROM_sha256=sha(ROM.read_bytes()),evidence=evidence,viewed_actual_sheets=visual['all5_actual_sheets_viewed'],
        actual_Shipwright109_Lil2_Janus4_Manuel23_original_names_and_portraits_observed=True,
        actual_four_disclosed_cold_boots_pass=True,actual_selected_B167_source_events=[],actual_sampled_display_IDs=ids,
        actual_sampled_choice_IDs=choiceids,offline_only_display_IDs=offline,offline_only_display_cases=visual['offline_only_display_cases'],
        represented_reviewed_display_IDs=ids+offline+choiceids,
        actual25_unique_panels28_observations_both_choices_and_distinct_returns_pass=True,
        source_two_Cesare_queries12_relative_containers_choice_and_both_ends_retained_not_flattened=True,
        both_Cesare_remarks_not_actual_or_byte_identical_reuse=True,no_B167_effect_or_source_command_omitted=True,
        original_B22_four_A000_initialization_commands_retained=True,no_open_translation_specific_display_or_control_finding=True,
        individual_conditional_visits_not_required_under_user_policy=True,new_emulator_runs=4,
        registered_release_and_current_startup_pending=True,full_goal_complete=False))
    block = deepcopy(plan['blocks'][0])
    checked = census['blocks'][0]
    assert block['block'] == checked['block'] == 167
    block['target_block_sha256'] = block.pop('research_block_sha256')
    block.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],
        external_entry_and_actual_revised_paths_approval_pending=False,individual_naturally_selected_source_scene_unobserved=True)
    assert len(block['command_map']) == 46 and len(block['relative_skip_fixups']) == 12
    assert len(block['target_native_skip_cases']) == 60 and len(block['text_records']) == 27
    assert len(block['choice_commands']) == 1 and not block['actor_style_commands'] and not block['original2000_pause_and_resume_maps']
    assert [e['source_offset'] for e in block['original_declared_end_word_maps']] == [430,2172]
    mapping = dict(format='dk4-lil-B167-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(parent.read_file('/__arm9__.bin')),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[block],
        all46_commands12_relative_sites60_target_skips_verified=True,all27_active_speech_targets_preserved=True,
        one2100_object_two_labels_and_source_indices_0_1_cancel_verified=True,
        all6_opaque_leaves_two_predicates_two_resources_and_two_ends_exact=True,
        two_separate_refusal_and_lecture_endwords_preserved=True,no_source_FE_2000_C200_or_dynamic_objects=True,
        representative_shared_rules_approved=True,representative_proof=str(sample),source_plan=str(PLAN),source_census=str(CENSUS),
        final_padding_proof=str(STORED),relocated_control_proof=str(CONTROL),termination_decode_proof=str(ENDS),native_choice_proof=str(MENU),
        evidence={**evidence,str(sample):sha(sample.read_bytes())},actual_selected_B167_source_events=[],
        individual_conditional_visits_not_required_under_user_policy=True,full_goal_complete=False)
    save(MAP,mapping)
    for i,(document,old,new) in enumerate(zip(docs,INPUTS,OUTPUTS,strict=True)):
        document.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()),
            prose_companions=[str(OUTPUTS[1-i])],reference_map_pending=False,registered_integration_pending=True,
            status='source-prose-native-references-representative-approved;registered-release-startup-pending')
        for key,path in [('reference_map',MAP),('representative_proof',sample),('final_padding_proof',STORED),
                         ('relocated_control_proof',CONTROL),('termination_decode_proof',ENDS),('native_choice_proof',MENU)]:
            document[key] = str(path)
            document[key+'_sha256'] = sha(path.read_bytes())
        for row in document['records']:
            row.update(status=document['status'],current_text_hex=row['current_hex'],
                native_display_consumer='original2100_two_option_modal51FC0' if i else 'original_progressive_54020',
                actual_B22_display_fixture_observed=row['id'] in ids+choiceids,
                offline_only_native_display_checked=row['id'] in offline,
                individual_actual_source_event_activation_not_claimed=True)
        if i == 0:
            document.update(choice_companion=str(OUTPUTS[1]),choices=str(OUTPUTS[1]))
        assert [r['english'] for r in document['records']] == [r['english'] for r in read(old)['records']]
        validate_natural_dialogue_batch(document)
        save(new,document)
    save(ROOT/'approval_receipt.json',dict(manuscripts={str(p):sha(p.read_bytes()) for p in OUTPUTS},
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        evidence={**evidence,str(MAP):sha(MAP.read_bytes()),str(sample):sha(sample.read_bytes())},
        all29_source_native_reference_and_representative_rules_approved=True,source_prose_English_unchanged=True,
        actual_sampled_display_IDs=ids,actual_sampled_choice_IDs=choiceids,offline_only_display_IDs=offline,
        new_emulator_runs=4,registered_release_and_current_startup_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('29 approvals sealed:25 actual speeches/two offline Cesare remarks,both choices,46commands/12spans/60skips,108storedcases. Registered integration pending.')
