"""Seal both B196 companions with exact relocation and sufficient limited gameplay."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B196_research_v5618 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B196_reference_approval_v5631')
INPUT=Path('translations/lil_B196_editorial_manuscript_v3.json')
CHOICE_INPUT=Path('translations/lil_B196_choice_manuscript_v2.json')
OUTPUT=Path('translations/lil_B196_editorial_manuscript_v4.json')
CHOICE_OUTPUT=Path('translations/lil_B196_choice_manuscript_v3.json')
MAP=Path('translations/lil_B196_editorial_relocation_map_v1.json')
CENSUS=Path('work/analysis/lil_B196_reference_census_v5621/all119_commands52_relative_sites_and_shipped_entry_census.json')
CONTROL=Path('work/analysis/lil_B196_relocated_controls_v5623/all24_dispatches_seven_predicates_six_pictures_menus_and37_exact_leaves.json')
STORED=Path('work/analysis/lil_B196_stored_v5616/all24_final_stored_targets96_macro_cases_and_complete_planes.json')
STORED_MENUS=Path('work/analysis/lil_B196_stored_choices_v5617/six_final_typed_objects_twelve_references_and_both_even_alignments.json')
ENDS=Path('work/analysis/lil_B196_ends_v5622/fourteen_declared_end_decodes_and_all52_in_block_relative_destinations.json')
ACTUAL=Path('work/analysis/lil_B196_actual_v5628b/three_paired_paths_native_panels_menus_and_separate_endings.json')
FIXTURE=Path('work/analysis/lil_B196_display_fixture_v5625/complete_B196_B22_fixtures.json')
VISUAL=Path('work/analysis/lil_B196_actual_review_v5630/viewed13_panels13_menus_three_paths_and_measured_state_scope.json')
FLAGS=['all119_structural_commands_and52_relative_sites_verified','all24_speech_targets_and12_typed_labels_preserved',
       'all37_opaque_leaves_seven_predicates_six_pictures_and_seven_ends_exact',
       'progressive23_null_actor_FE1_FI1_preserved','all_six_typed_menu_counts_order_pointers_and_returns_preserved',
       'all_original_stored_source_bytes_restored_by_inverse_with_two_tailzeros',
       'thirteen_actual_speech_panels_eleven_native_offline_only_scope_explicit',
       'first_buy_deepest_buy_and_all_pass_actual_endings_verified','representative_shared_rules_approved']

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,OUTPUT,CHOICE_OUTPUT,MAP])
    doc,choice=map(lambda p:deepcopy(read(p)),[INPUT,CHOICE_INPUT])
    plan,census,control,stored,menus,ends,actual,fixture,visual=map(read,[PLAN,CENSUS,CONTROL,STORED,STORED_MENUS,ENDS,ACTUAL,FIXTURE,VISUAL])
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==choice['current_ROM_sha256']==plan['candidate_sha256']
    assert sha(ROM.read_bytes())==census['research_ROM_sha256']==control['research_ROM_sha256']==ends['research_ROM_sha256']
    assert sha(INPUT.read_bytes())==plan['manuscript_sha256']==stored['manuscript_sha256']==control['manuscript_sha256']
    assert sha(CHOICE_INPUT.read_bytes())==plan['choices_sha256']==menus['manuscript_sha256']
    assert census['all119_clean_current_target_commands_and52_relative_sites_reexecuted'] and census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert len(control['relocated_dispatch_cases'])==24 and len(control['all37_source_current_target_nonrelative_nonspeech_nonchoice_leaves'])==37
    assert len(control['relocated_unforced_predicates'])==7 and len(control['relocated_picture_boundaries'])==len(control['relocated_menu_getters'])==6
    assert stored['current_final_stored_macro_alignment_cases']==96 and stored['all24_final_targets_complete_native_planes_equal_reviewed_planes']
    assert (stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(40,56)
    assert menus['all_six_stored_objects_and_twelve_actual_offsets_record_indices_labels_and_counts_exact']
    assert ends['all14_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases'])==14
    assert not actual['failures'] and not actual['paired_nontext_region_differences']
    assert len(actual['actual_panels'])==13 and len(actual['actual_menu_cases'])==13 and len(actual['offline_only_display_IDs'])==11
    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and visual['no_open_translation_specific_display_menu_control_or_return_finding'] and not visual['visual_review_pending']
    assert visual['actual_new_cold_boot_runs']==6 and visual['total_frames']==78006
    assert fixture['source_all119_commands_preserved_without_omission_or_flattening']
    assert all(not f['explicitly_excluded_original_commands'] and len(f['all128_stored_fixture_commands'])==128 for f in fixture['fixtures'])
    views=visual['all_actual_consumer_menu_sheets_viewed']+visual['paired_full_screen_views']+[visual['first_buy_postscene_view']]
    assert all(s['viewed'] and s['viewed_after_image_return'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in views)
    for p,h in visual['evidence'].items():assert sha(Path(p).read_bytes())==h
    ids=[r['id'] for r in actual['actual_panels']];offline=actual['offline_only_display_IDs']
    assert set(ids).isdisjoint(offline) and set(ids+offline)=={r['id'] for r in doc['records']}
    paths=[INPUT,CHOICE_INPUT,PLAN,CENSUS,CONTROL,STORED,STORED_MENUS,ENDS,ACTUAL,FIXTURE,VISUAL,Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in paths};ROOT.mkdir(parents=True)
    sample=ROOT/'representative_display_control_and_transition_reconciliation.json'
    buy=sorted({r['source_menu_offset'] for r in actual['actual_menu_cases'] if r['native_result_words'][1]==0})
    passed=sorted({r['source_menu_offset'] for r in actual['actual_menu_cases'] if r['native_result_words'][1]==1})
    assert buy==[218,1588] and passed==[218,582,832,1156,1370,1588]
    save(sample,dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        actual_sampled_display_IDs=ids,offline_only_display_IDs=offline,actual_buy_menu_offsets=buy,actual_pass_menu_offsets=passed,
        all_six_label_pairs_seen_and_native_order_bound_but_not_all_six_Buy_outcomes_played=True,
        all_original_commands_stored_without_omission=True,first_buy_end364_deepest_buy_end1708_all_pass_end1810_observed=True,
        R74_four_rows_validated_offline_but_not_visited_in_gameplay=True,
        six_unforced_source_payment_amounts_and_thirty_explicit_offline_owned_funds_boundaries_separate=True,
        observed_item_presentation_and_acquisition_notice_not_full_inventory_or_Charm_model_semantics=True,
        viewed_actual_sheets=visual['all_actual_consumer_menu_sheets_viewed'],viewed_paired_full_screen_sheets=visual['paired_full_screen_views'],
        no_open_translation_specific_display_or_control_finding=True,representative_shared_rules_approved=True,
        no_natural_eligibility_earned_affordability_full_route_hardware_or_full_state_claim=True,
        new_emulator_runs=6,total_frames=78006,registered_release_and_current_startup_pending=True,evidence=evidence,full_goal_complete=False))
    block=deepcopy(plan['blocks'][0]);checked=census['blocks'][0]
    assert block['block']==checked['block']==196 and len(block['command_map'])==119 and len(block['text_records'])==24
    assert (block['source_bytes'],block['source_logical_end'],block['research_bytes'],block['research_logical_end'])==(1816,1814,1668,1668)
    assert len(block['relative_skip_fixups'])==52 and len(block['target_native_skip_cases'])==260 and len(block['choice_commands'])==6
    assert block['inverse_plus_original_two_tailzeros_recovers_every_stored_source_byte']
    block['target_block_sha256']=block.pop('research_block_sha256')
    block.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],
        external_entry_and_actual_revised_paths_approval_pending=False,individual_naturally_selected_source_scene_unobserved=True,
        actual_sampled_display_IDs=ids,offline_only_display_IDs=offline)
    mapping=dict(format='dk4-lil-B196-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(NdsImage.open(PARENT).read_file('/__arm9__.bin')),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[block],**{f:True for f in FLAGS},
        actual_sampled_display_IDs=ids,offline_only_display_IDs=offline,representative_proof=str(sample),source_plan=str(PLAN),source_census=str(CENSUS),
        final_padding_proof=str(STORED),final_choice_proof=str(STORED_MENUS),relocated_control_proof=str(CONTROL),termination_decode_proof=str(ENDS),postscene_native_state_proof=str(VISUAL),
        evidence={**evidence,str(sample):sha(sample.read_bytes())},actual_selected_B196_source_events=[],full_goal_complete=False)
    save(MAP,mapping)
    for batch,old,other,out in [(doc,INPUT,CHOICE_OUTPUT,OUTPUT),(choice,CHOICE_INPUT,OUTPUT,CHOICE_OUTPUT)]:
        batch.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()),prose_companions=[str(other)],reference_map_pending=False,
            registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
        for key,p in [('reference_map',MAP),('representative_proof',sample),('final_padding_proof',STORED),('final_choice_proof',STORED_MENUS),('relocated_control_proof',CONTROL),('termination_decode_proof',ENDS),('postscene_native_state_proof',VISUAL)]:batch[key],batch[key+'_sha256']=str(p),sha(p.read_bytes())
        for r in batch['records']:
            r['historical_pre_actual_display_scope']={k:r[k] for k in ['current_complete_native_display_pending','current_native_UI_body_explicit_unexecuted_boundary','actual_choice_selection_still_pending'] if k in r}
            speech=r['id'] in ids or r['id'] in offline;observed=r['id'] in ids if speech else True
            r.update(status=batch['status'],current_text_hex=r['current_hex'],actual_B22_display_fixture_observed=observed,offline_only_native_display_checked=not observed,
                current_complete_native_display_pending=False,individual_actual_source_event_activation_not_claimed=True)
            if speech:
                r['native_display_consumer']='original_null_actor_FE_24310_then5473C' if r['kind']=='system-FE' else 'original_progressive_54020'
                r['current_native_UI_body_explicit_unexecuted_boundary']=not observed
            else:
                r.update(native_display_consumer='original2100_two_option_modal51FC0',actual_label_visible=True,actual_choice_all_outcomes_observed=r['command_offset'] in buy,
                    actual_choice_selection_still_pending=False,choice_consumer_selection_geometry_native_display_pending=False)
        assert [r['english'] for r in batch['records']]==[r['english'] for r in read(old)['records']]
        validate_natural_dialogue_batch(batch);save(out,batch)
    save(ROOT/'approval_receipt.json',dict(manuscripts={str(p):sha(p.read_bytes()) for p in [OUTPUT,CHOICE_OUTPUT]},reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        evidence={**evidence,str(MAP):sha(MAP.read_bytes()),str(sample):sha(sample.read_bytes())},all36_source_native_reference_and_representative_rules_approved=True,
        source_prose_English_unchanged=True,actual_sampled_display_IDs=ids,offline_only_display_IDs=offline,actual_buy_menu_offsets=buy,actual_pass_menu_offsets=passed,
        new_emulator_runs=6,total_frames=78006,new_editorial_credit=0,registered_release_and_current_startup_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B196 sealed36 objects:13 speeches actual/11 native offline,all six menu label pairs,three endings. Both companions approved without prose changes;registered compiler/release/startup remain.')
