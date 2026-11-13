"""Seal 44 reviews with exact relocation and explicitly scoped representative coverage."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B166_research_v4095 import ROM, PARENT, PLAN
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B166_reference_approval_v4106')
INPUTS = [Path('translations/lil_B166_editorial_manuscript_v5.json'),Path('translations/lil_B166_choice_manuscript_v2.json')]
OUTPUTS = [Path('translations/lil_B166_editorial_manuscript_v6.json'),Path('translations/lil_B166_choice_manuscript_v3.json')]
MAP = Path('translations/lil_B166_editorial_relocation_map_v1.json')
CENSUS = Path('work/analysis/lil_B166_reference_census_v4098/all62_commands8_relative_sites_and_shipped_entry_census.json')
CONTROL = Path('work/analysis/lil_B166_relocated_controls_v4100/all42_dispatches_Fernando_predicate11_leaves_and_two_choice_getters.json')
STORED = Path('work/analysis/lil_B166_stored_v4094/all42_final_stored_targets168_macro_cases_and_complete_planes.json')
ENDS = Path('work/analysis/lil_B166_ends_v4099/two_declared_end_decodes_and_all8_in_block_relative_destinations.json')
ACTUAL = Path('work/analysis/lil_B166_actual_v4104/actual_both_choices_conditional_panels_and_single_return.json')
FIXTURE = Path('work/analysis/lil_B166_display_fixture_v4101/complete_choice_preserving_B22_fixtures.json')
VISUAL = Path('work/analysis/lil_B166_transition_review_v4105/both_choices_all7_sheets_Manuel_names_figures_and_paired_returns_review.json')
MENU = Path('work/analysis/lil_B166_choices_v4080/B166_C2152/original_choice_decoder_VM_geometry_and_native_pixels.json')

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
    assert census['all62_clean_current_target_commands_and8_relative_sites_reexecuted']
    assert census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert len(control['relocated_dispatch_cases']) == 42 and len(control['relocated_predicate_pairs']) == 1
    assert len(control['all11_source_current_target_nonrelative_nonspeech_nonchoice_leaves']) == 11
    assert len(control['relocated_choice_getter_phases']) == 2 and control['unforced_Fernando_result_matches_source_without_roster_fixture']
    assert stored['current_final_stored_macro_alignment_cases'] == 168 and len(stored['final_target_parity_cases']) == 42
    assert stored['all42_final_targets_complete_native_planes_equal_reviewed_planes']
    assert ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
    assert ends['B166_single_end_is_declared_logical_tail'] and len(ends['cases']) == 2
    assert actual['fresh_actual_unique_speech_panels'] == 41 and actual['complete_matching_observations'] == 73
    assert not actual['failures'] and actual['actual_new_cold_boot_runs'] == 4
    assert actual['both_real_choice_values_and_same_single_tail_end_observed']
    assert visual['actual_proof_sha256'] == sha(ACTUAL.read_bytes())
    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope']
    assert len(visual['all7_actual_sheets_viewed']) == 7 and len(visual['English_full_screen_views']) == 11
    assert len(visual['Japanese_full_screen_views']) == 3 and len(visual['paired_source_English_whole_RGB_returns']) == 2
    assert menu['six_original_VM_selection_and_cancel_cases_pass'] and menu['eight_complete_native_style_label_planes_pass']
    assert fixture['all_original_choice_relative_containers_presentation_resources_and_single_end_preserved']
    assert fixture['one_late_recruitment_effect_excluded_after_choice_without_changing_any_branch_span']
    for path in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/data/EV2.DK4','/GRP/KANJI.FNT']:
        assert parent.read_file(path) == image.read_file(path)
    for sheet in visual['all7_actual_sheets_viewed'] + visual['English_full_screen_views'] + visual['Japanese_full_screen_views']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256'] and sheet['review'].startswith('Viewed')
    native = read(doc['native_font_proof'])
    assert native['all42_current_native_speech_planes_pass'] and native['current_original_macro_alignment_calls'] == 336
    ids = [r['id'] for r in actual['actual_panels']]
    offline = actual['offline_only_display_IDs']
    choiceids = [r['id'] for r in docs[1]['records']]
    assert offline == ['DK4_MES_B166_R0087'] and not set(ids) & set(offline)
    assert set(ids+offline) == {r['id'] for r in doc['records']} and len(choiceids) == 2
    ROOT.mkdir(parents=True)
    paths = [*INPUTS,PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL,MENU,Path(__file__)]
    evidence = {str(p):sha(p.read_bytes()) for p in paths}
    sample = ROOT / 'representative_display_control_and_transition_reconciliation.json'
    save(sample,dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),
        research_ROM_sha256=sha(ROM.read_bytes()),evidence=evidence,viewed_actual_sheets=visual['all7_actual_sheets_viewed'],
        actual_Manuel17_original_nameplate_portrait_and_full_figure_observed=True,
        actual_four_disclosed_cold_boots_pass=True,actual_selected_B166_source_events=[],actual_sampled_display_IDs=ids,
        actual_sampled_choice_IDs=choiceids,offline_only_display_IDs=offline,offline_only_display_cases=visual['offline_only_display_cases'],
        represented_reviewed_display_IDs=ids+offline+choiceids,
        actual41_unique_panels73_observations_both_advice_results_and_normal_returns_pass=True,
        source_Fernando_query8_relative_containers_choice_and_single_end_retained_not_flattened=True,
        Fernando_remark_not_actual_or_byte_identical_reuse=True,source_recruitment_effect_excluded=True,
        original_B22_four_A000_initialization_commands_retained=True,no_open_translation_specific_display_or_control_finding=True,
        individual_conditional_visits_not_required_under_user_policy=True,new_emulator_runs=4,
        registered_release_and_current_startup_pending=True,full_goal_complete=False))
    block = deepcopy(plan['blocks'][0])
    checked = census['blocks'][0]
    assert block['block'] == checked['block'] == 166
    block['target_block_sha256'] = block.pop('research_block_sha256')
    block.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],
        external_entry_and_actual_revised_paths_approval_pending=False,individual_naturally_selected_source_scene_unobserved=True)
    assert len(block['command_map']) == 62 and len(block['relative_skip_fixups']) == 8
    assert len(block['target_native_skip_cases']) == 40 and len(block['text_records']) == 42
    assert len(block['choice_commands']) == 1 and not block['actor_style_commands'] and not block['original2000_pause_and_resume_maps']
    assert [e['source_offset'] for e in block['original_declared_end_word_maps']] == [2948]
    mapping = dict(format='dk4-lil-B166-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(parent.read_file('/__arm9__.bin')),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[block],
        all62_commands8_relative_sites40_target_skips_verified=True,all42_active_speech_targets_preserved=True,
        one2100_object_two_labels_and_source_indices_0_1_cancel_verified=True,
        all11_opaque_leaves_one_predicate_one_effect_two_resources_six_presentations_and_end_exact=True,
        single_declared_tail_end_after_advice_rejoin_preserved=True,no_source_FE_2000_C200_or_dynamic_objects=True,
        representative_shared_rules_approved=True,representative_proof=str(sample),source_plan=str(PLAN),source_census=str(CENSUS),
        final_padding_proof=str(STORED),relocated_control_proof=str(CONTROL),termination_decode_proof=str(ENDS),native_choice_proof=str(MENU),
        evidence={**evidence,str(sample):sha(sample.read_bytes())},actual_selected_B166_source_events=[],
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
        all44_source_native_reference_and_representative_rules_approved=True,source_prose_English_unchanged=True,
        actual_sampled_display_IDs=ids,actual_sampled_choice_IDs=choiceids,offline_only_display_IDs=offline,
        new_emulator_runs=4,registered_release_and_current_startup_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('44 approvals sealed:41 actual speeches/1 offline Fernando remark,both advice choices,62commands/8spans/40skips,168storedcases. Registered integration pending.')
