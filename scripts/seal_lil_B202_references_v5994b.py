"""Seal B202's exact source relocation and complete representative English evidence."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B202_references_v5982 import PARENT,ROM,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B202_reference_approval_v5994b')
INPUT=Path('translations/lil_B202_editorial_manuscript_v4.json')
OUTPUT=Path('translations/lil_B202_editorial_manuscript_v6.json')
MAP=Path('translations/lil_B202_editorial_relocation_map_v2.json')
PROOFS={
 'source_census':'work/analysis/lil_B202_reference_census_v5987/all26_commands_no_relative_sites_and_shipped_entry_census.json',
 'loader_proof':'work/analysis/lil_B202_loader_v5986/whole_SC2_and_B202_initial_entry_proof.json',
 'final_padding_proof':'work/analysis/lil_B202_stored_v5984/all19_final_stored_targets76_macro_cases_and_complete_planes.json',
 'relocated_control_proof':'work/analysis/lil_B202_relocated_controls_v5989/all19_dispatches_one_picture_one47xx_pair_and7_exact_leaves.json',
 'termination_decode_proof':'work/analysis/lil_B202_ends_v5988/two_declared_tail_end_decodes_no_relative_sites.json',
 'actual_proof':'work/analysis/lil_B202_actual_v5992/nineteen_actual_panels_source_matched_controls_and_complete_native_holds.json',
 'representative_proof':'work/analysis/lil_B202_actual_review_v5993/viewed19_panels_complete_return_and_honest_measured_scope.json',
 'postscene_native_state_proof':'work/analysis/lil_B202_actual_review_v5993/paired_transitions_timing_RNG_and_native_state.json',
 'native_approval':'work/analysis/lil_B202_native_approval_v5979/all19_source_prose_current_native_approval.json'}
FLAGS=['all26_commands19_preambles7_opaque_leaves_complete_no_relative_or_menu',
 'all588_predecessor_bytes_inverse_source586_target578_logical580_stored_two_tailzeros',
 'all19_actual_panels74_complete_native_holds_match_source_regions',
 'four_original_actors_voices_zero_FE_and_zero_FI_FA_FO_preserved',
 'Sailor_progressive_alias_Retainer_catalogue_Charles_middle_field_and_Guildmaster_bound',
 'Glassmaking_Guide_spoken_title_bound_clean_item14_widget_not_full_effect_approval',
 'three_speech_duration22_start_return5_RNG21_prompt_differences_preserved',
 'queried_native_groups_agree_PRNG_differs_no_broad_world_equivalence',
 'following_B43_source_item_Local_Product_leads_uncredited_and_open',
 'representative_shared_rules_approved_natural_activation_and_hardware_unclaimed']
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,OUTPUT,MAP]);doc,plan=map(read,[INPUT,PLAN]);proofs={k:read(p) for k,p in PROOFS.items()}
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256'] and plan['manuscript_sha256']==sha(INPUT.read_bytes())
    actual,view,state,native=[proofs[k] for k in ['actual_proof','representative_proof','postscene_native_state_proof','native_approval']]
    assert actual['actual_unique_speech_panels']==actual['complete_matching_observations']==19 and actual['complete_matching_holds']==74 and not actual['failures'] and not actual['paired_region_differences'] and not actual['offline_only_source_indices']
    assert native['all19_five_gates_approved'] and len(native['formatter_negatives'])==14 and len(native['three_individual_rowcount_reasons'])==3 and len(actual['actual_timing_differences'])==22 and len(actual['later_whole_RGB_differences'])==21
    assert not view['visual_review_pending'] and view['no_open_translation_specific_display_control_or_return_finding'] and len(state['actual_command_duration_changes'])==3 and len(state['within_scene_RNG_differences'])==5 and all(state['native_final_component_equality'].values()) and not state['final_PRNG_equal']
    assert state['source_English_exit_frames']==[7657,7655] and state['whole_actor_and_captain_equal'] and state['no_causal_explanation_full_RAM_future_RNG_or_broad_simulation_equivalence_claim']
    assert all(s['viewed_after_image_return'] and s['viewed'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in view['viewed_sheets'])
    ids=[r['id'] for r in doc['records']];assert ids==[r['id'] for r in actual['actual_panels']]
    block=deepcopy(plan['blocks'][0]);census=proofs['source_census']['blocks'][0]
    assert (block['block'],block['source_bytes'],block['source_logical_end'],block['research_bytes'],block['research_logical_end'])==(202,588,586,580,578)
    assert len(block['command_map'])==26 and len(block['text_records'])==19 and not any(block[k] for k in ['relative_skip_fixups','target_native_skip_cases','choice_commands','actor_style_commands','original2000_pause_and_resume_maps'])
    assert block['inverse_plus_original_two_tailzeros_recovers_every_stored_source_byte'];block['target_block_sha256']=block.pop('research_block_sha256');block.update(mapped_native_commands=census['mapped_commands'],external_references_complete=True,entry_point_offset=8,external_entry_and_actual_revised_paths_approval_pending=False,actual_sampled_display_IDs=ids,offline_only_display_IDs=[])
    for k in ['source_census','relocated_control_proof','termination_decode_proof']:assert proofs[k]['research_ROM_sha256']==sha(ROM.read_bytes())
    evidence={str(p):sha(Path(p).read_bytes()) for p in [INPUT,PLAN,*PROOFS.values(),Path(__file__)]}
    mapping=dict(format='dk4-lil-B202-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(NdsImage.open(PARENT).read_file('/__arm9__.bin')),source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[block],actual_sampled_display_IDs=ids,offline_only_display_IDs=[],source_plan=str(PLAN),**PROOFS,**{f:True for f in FLAGS},evidence=evidence,full_goal_complete=False);save(MAP,mapping)
    doc=deepcopy(doc);doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),reference_map_pending=False,registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for k,p in PROOFS.items():doc[k],doc[k+'_sha256']=p,sha(Path(p).read_bytes())
    for r in doc['records']:
        r['record_index']=r['current_record_index']
        r['historical_pre_actual_display_scope']={k:r[k] for k in ['current_native_UI_body_explicit_unexecuted_boundary','native_plane_verified_not_actual_English_gameplay','current_complete_native_display_pending'] if k in r}
        r.update(status=doc['status'],current_text_hex=r['current_hex'],actual_B22_display_fixture_observed=True,offline_only_native_display_checked=False,current_complete_native_display_pending=False,individual_actual_source_event_activation_not_claimed=True,native_plane_verified_not_actual_English_gameplay=False,native_display_consumer='original_progressive_54020',current_native_UI_body_explicit_unexecuted_boundary=False)
    assert [r['english'] for r in doc['records']]==[r['english'] for r in read(INPUT)['records']];validate_natural_dialogue_batch(doc);save(OUTPUT,doc);ROOT.mkdir(parents=True)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),all19_source_native_reference_and_representative_rules_approved=True,source_prose_English_and_compiled_targets_unchanged=True,actual_sampled_display_IDs=ids,offline_only_display_IDs=[],revised=6,retained=13,all_measured_timing_RNG_state_and_prompt_differences_preserved=True,registered_release_and_current_startup_pending=True,evidence=evidence,new_editorial_credit=0,full_goal_complete=False));print('B202 sealed19 objects:six revisions/13 retentions;19 actual panels/74 complete holds. Exact controls and honest differences preserved;registered integration next.')
