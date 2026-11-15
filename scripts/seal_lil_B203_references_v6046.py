"""Seal B203 source relocation and complete representative English evidence."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B203_references_v6034 import PARENT,ROM,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B203_reference_approval_v6046')
INPUT=Path('translations/lil_B203_editorial_manuscript_v4.json')
OUTPUT=Path('translations/lil_B203_editorial_manuscript_v5.json')
MAP=Path('translations/lil_B203_editorial_relocation_map_v1.json')
PROOFS={
 'source_census':'work/analysis/lil_B203_reference_census_v6039/all31_commands_no_relative_sites_and_shipped_entry_census.json',
 'loader_proof':'work/analysis/lil_B203_loader_v6038/whole_SC2_and_B203_initial_entry_proof.json',
 'final_padding_proof':'work/analysis/lil_B203_stored_v6036/all22_final_stored_targets88_macro_cases_and_complete_planes.json',
 'relocated_control_proof':'work/analysis/lil_B203_relocated_controls_v6041/all22_dispatches_one_picture_one47xx_pair_and9_exact_leaves.json',
 'termination_decode_proof':'work/analysis/lil_B203_ends_v6040/two_declared_tail_end_decodes_no_relative_sites.json',
 'actual_proof':'work/analysis/lil_B203_actual_v6044/twenty_two_actual_panels_source_matched_controls_and_complete_native_holds.json',
 'representative_proof':'work/analysis/lil_B203_actual_review_v6045/viewed22_panels_complete_return_and_honest_measured_scope.json',
 'postscene_native_state_proof':'work/analysis/lil_B203_actual_review_v6045/paired_transitions_timing_RNG_and_native_state.json',
 'native_approval':'work/analysis/lil_B203_native_approval_v6031/all22_source_prose_current_native_approval.json'}
FLAGS=['all31_commands22_preambles9_opaque_leaves_complete_no_relative_or_menu',
 'all816_predecessor_bytes_inverse_source814_target768_logical768_stored_source2_target0_alignment_tail',
 'all22_actual_panels86_complete_native_holds_match_source_regions',
 'three_original_actors_voices_one_FE_one_FI_zero_FA_FO_preserved',
 'Lil_Mikhail_progressive_catalogue_middle_field_and_source_Mysterious_Old_Man_bound',
 'unspoken_book_title_not_inserted_clean_item18_widget_not_full_effect_approval',
 'one_speech_duration23_start_return_zero_interval_RNG18_prompt_differences_preserved',
 'queried_native_groups_and_PRNG_agree_no_broad_world_equivalence',
 'following_B43_source_item_Local_Product_leads_uncredited_and_open',
 'representative_shared_rules_approved_natural_activation_and_hardware_unclaimed']
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,OUTPUT,MAP]);doc,plan=map(read,[INPUT,PLAN]);proofs={k:read(p) for k,p in PROOFS.items()}
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256'] and plan['manuscript_sha256']==sha(INPUT.read_bytes())
    actual,view,state,native=[proofs[k] for k in ['actual_proof','representative_proof','postscene_native_state_proof','native_approval']]
    assert actual['actual_unique_speech_panels']==actual['complete_matching_observations']==22 and actual['complete_matching_holds']==86 and not actual['failures'] and not actual['paired_region_differences'] and not actual['offline_only_source_indices']
    assert native['all22_five_gates_approved'] and len(native['formatter_negatives'])==28 and len(native['six_individual_rowcount_reasons'])==6
    assert len(actual['actual_timing_differences'])==23 and len(actual['later_whole_RGB_differences'])==18
    assert not view['visual_review_pending'] and view['no_open_translation_specific_display_control_or_return_finding'] and view['generated_item_acquired_notice_same_frame_whole_RGB_equal_at8350']
    assert state['actual_command_duration_changes']==[dict(source_offset=208,word=0x4000,source_duration=241,English_duration=240,delta=-1)] and not state['within_scene_RNG_differences'] and all(state['native_final_component_equality'].values()) and state['final_PRNG_equal']
    assert state['source_English_exit_frames']==[8374,8373] and state['whole_actor_and_captain_equal'] and state['no_causal_explanation_full_RAM_future_RNG_or_broad_simulation_equivalence_claim']
    assert all(s['viewed_after_image_return'] and s['viewed'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in view['viewed_sheets'])
    ids=[r['id'] for r in doc['records']];assert ids==[r['id'] for r in actual['actual_panels']]
    block=deepcopy(plan['blocks'][0]);census=proofs['source_census']['blocks'][0]
    assert (block['block'],block['source_bytes'],block['source_logical_end'],block['research_bytes'],block['research_logical_end'])==(203,816,814,768,768)
    assert len(block['command_map'])==31 and len(block['text_records'])==22 and not any(block[k] for k in ['relative_skip_fixups','target_native_skip_cases','choice_commands','actor_style_commands','original2000_pause_and_resume_maps'])
    assert block['inverse_plus_original_two_tailzeros_recovers_every_stored_source_byte'];block['target_block_sha256']=block.pop('research_block_sha256')
    block.update(mapped_native_commands=census['mapped_commands'],external_references_complete=True,entry_point_offset=8,external_entry_and_actual_revised_paths_approval_pending=False,actual_sampled_display_IDs=ids,offline_only_display_IDs=[],source_alignment_tail_bytes=2,target_alignment_tail_bytes=0)
    for k in ['source_census','relocated_control_proof','termination_decode_proof']:assert proofs[k]['research_ROM_sha256']==sha(ROM.read_bytes())
    evidence={str(p):sha(Path(p).read_bytes()) for p in [INPUT,PLAN,*PROOFS.values(),Path(__file__)]}
    mapping=dict(format='dk4-lil-B203-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(NdsImage.open(PARENT).read_file('/__arm9__.bin')),source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[block],actual_sampled_display_IDs=ids,offline_only_display_IDs=[],source_plan=str(PLAN),**PROOFS,**{f:True for f in FLAGS},evidence=evidence,full_goal_complete=False);save(MAP,mapping)
    doc=deepcopy(doc);doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),reference_map_pending=False,registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for k,p in PROOFS.items():doc[k],doc[k+'_sha256']=p,sha(Path(p).read_bytes())
    for r in doc['records']:
        r['record_index']=r['current_record_index']
        r['historical_pre_actual_display_scope']={k:r[k] for k in ['current_native_UI_body_explicit_unexecuted_boundary','native_plane_verified_not_actual_English_gameplay','current_complete_native_display_pending'] if k in r}
        r.update(status=doc['status'],current_text_hex=r['current_hex'],actual_B22_display_fixture_observed=True,offline_only_native_display_checked=False,current_complete_native_display_pending=False,individual_actual_source_event_activation_not_claimed=True,native_plane_verified_not_actual_English_gameplay=False,native_display_consumer='original_null_actor_FE_24310_then5473C' if r['kind']=='system-FE' else 'original_progressive_54020',current_native_UI_body_explicit_unexecuted_boundary=False)
    assert [r['english'] for r in doc['records']]==[r['english'] for r in read(INPUT)['records']];validate_natural_dialogue_batch(doc);save(OUTPUT,doc);ROOT.mkdir(parents=True)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),all22_source_native_reference_and_representative_rules_approved=True,source_prose_English_and_compiled_targets_unchanged=True,actual_sampled_display_IDs=ids,offline_only_display_IDs=[],revised=9,retained=13,all_measured_timing_RNG_state_and_prompt_differences_preserved=True,registered_release_and_current_startup_pending=True,evidence=evidence,new_editorial_credit=0,full_goal_complete=False))
    print('B203 sealed22 objects:nine revisions/13 retentions;22 actual panels/86 complete holds. Exact controls and measured differences preserved;registered integration next.')
