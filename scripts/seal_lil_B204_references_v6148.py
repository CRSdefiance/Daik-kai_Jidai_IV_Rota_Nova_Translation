"""Seal complete source relocation and source-scoped actual English observations."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B204_references_v6135 import PARENT,ROM,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B204_reference_approval_v6148');INPUT=Path('translations/lil_B204_editorial_manuscript_v7.json');OUTPUT=Path('translations/lil_B204_editorial_manuscript_v8.json');MAP=Path('translations/lil_B204_editorial_relocation_map_v1.json')
PROOFS={
 'source_census':'work/analysis/lil_B204_reference_census_v6141/all26_commands_no_relative_sites_and_shipped_entry_census.json',
 'loader_proof':'work/analysis/lil_B204_loader_v6140/whole_SC2_and_B204_initial_entry_proof.json',
 'final_padding_proof':'work/analysis/lil_B204_stored_v6137/all20_final_stored_targets80_macro_cases_and_complete_planes.json',
 'relocated_control_proof':'work/analysis/lil_B204_relocated_controls_v6143/all20_dispatches_one_picture_one47xx_pair_and6_exact_leaves.json',
 'termination_decode_proof':'work/analysis/lil_B204_ends_v6142/two_declared_tail_end_decodes_no_relative_sites.json',
 'actual_proof':'work/analysis/lil_B204_actual_v6146/all20_actual_English_panels_complete_native_holds_two_source_scopes_and_return.json',
 'representative_proof':'work/analysis/lil_B204_actual_review_v6147/viewed20_panels_four_letters_complete_return_and_honest_scope.json',
 'postscene_native_state_proof':'work/analysis/lil_B204_actual_review_v6147/source_scoped_transitions_timing_RNG_and_native_state.json',
 'native_approval':'work/analysis/lil_B204_native_approval_v6132/all20_source_prose_current_native_approval.json',
 'source_nameplate_consumer_proof':'work/analysis/lil_B204_names_v6064/ten_original_progressive_and_catalogue_name_consumers.json',
 'actor_voice_contract':'work/analysis/lil_B204_voices_v6063/current207_catalog_eight_voices_and_five_source_selectors.json',
 'current_actor_name_preservation':'work/analysis/current_speaker_labels_v6113/existing_Man_Woman_Stranger_labels_and_broader_name_scope.json',
 'contextual_reconciliation':'work/analysis/lil_B204_source_view_v6077/complete_source_scenes_and_return_visual_review.json',
 'source_effect_and_predicate_contract':'work/analysis/lil_B204_controls_v6139/six_exact_leaves_picture47xx_two43xx_one_A000_structural_pairs_and_guarded_end.json',
}
FLAGS=['all26_commands20_preambles6_leaves_complete_no_relative_or_menu',
 'all1312_predecessor_bytes_inverse_source1312_target1344_zero_alignment_tails',
 'all20_actual_panels77_complete_native_holds_four_FE_letters',
 'five_source_actors_voices_no_FI_FA_FO_and_full_Jam_Jack_Ludwyan_signature_preserved',
 'source_gift_claim_letter_taking_and_explicit_thief_order_tension_retained',
 'current_Shachihoko_item_card_and5530_acquired_notice_preserved_without_duplicate_credit',
 'older_full_source_and_current_same_code_prefix_baselines_explicitly_distinct',
 'timing16_and20_RNG9_and13_later16_prompt_differences_preserved',
 'queried_native_groups_equal_different_PRNG_no_broad_world_equivalence',
 'representative_shared_rules_approved_natural_activation_original_location_full_effects_and_hardware_unclaimed']
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,OUTPUT,MAP]);doc,plan=map(read,[INPUT,PLAN]);proofs={k:read(p) for k,p in PROOFS.items()}
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256'] and plan['manuscript_sha256']==sha(INPUT.read_bytes())
    a,v,s,n=[proofs[k] for k in ['actual_proof','representative_proof','postscene_native_state_proof','native_approval']]
    assert a['actual_unique_speech_panels']==a['complete_matching_observations']==20 and a['complete_matching_holds']==77 and not a['failures'] and not a['offline_only_display_IDs']
    assert n['all20_five_gates_approved'] and len(n['formatter_negative_controls'])==28 and len(n['twelve_individual_rowcount_reasons'])==12
    assert not v['visual_review_pending'] and v['no_open_translation_specific_display_control_or_return_finding'] and v['current_Shachihoko_notice5530_whole_frame_equal_to_current_source']
    assert all(x['viewed'] and x['viewed_after_image_return'] and sha(Path(x['path']).read_bytes())==x['sha256'] for x in v['viewed_sheets']) and len(v['viewed_sheets'])==6
    assert [len(x) for x in a['source_English_command_timing_differences'].values()]==[16,20] and [len(x) for x in a['source_English_command_RNG_differences'].values()]==[9,13]
    assert s['source_exit_frames']==[7894,7895] and s['English_exit_frame']==7896 and s['all16_later_differences_bounded_to_advance_prompt']
    assert all(s['native_final_component_equality'].values()) and s['whole_actor_and_captain_equal'] and not s['final_PRNG_equal'] and s['no_whole_state_equivalence_claim_from_cross_build_getter_comparison']
    ids=[r['id'] for r in doc['records']];assert ids==[r['id'] for r in a['actual_panels']]
    b=deepcopy(plan['blocks'][0]);census=proofs['source_census']['blocks'][0]
    assert (b['block'],b['source_bytes'],b['source_logical_end'],b['research_bytes'],b['research_logical_end'])==(204,1312,1312,1344,1344)
    assert len(b['command_map'])==26 and len(b['text_records'])==20 and not any(b[k] for k in ['relative_skip_fixups','target_native_skip_cases','choice_commands','actor_style_commands','original2000_pause_and_resume_maps'])
    assert b['inverse_plus_original_zero_tailbytes_recovers_every_stored_source_byte'];b['target_block_sha256']=b.pop('research_block_sha256')
    b.update(mapped_native_commands=census['mapped_commands'],external_references_complete=True,entry_point_offset=8,external_entry_and_actual_revised_paths_approval_pending=False,actual_sampled_display_IDs=ids,offline_only_display_IDs=[],source_alignment_tail_bytes=0,target_alignment_tail_bytes=0)
    for k in ['source_census','relocated_control_proof','termination_decode_proof']:assert proofs[k]['research_ROM_sha256']==sha(ROM.read_bytes())
    names=proofs['current_actor_name_preservation'];assert names['candidate_sha256']==doc['current_ROM_sha256'] and names['all621_actor_name_pointer_fields_equal_V6050'] and names['all_referenced_staged_name_strings_equal_V6050']
    evidence={str(p):sha(Path(p).read_bytes()) for p in [INPUT,PLAN,*PROOFS.values(),Path(__file__)]}
    mapping=dict(format='dk4-lil-B204-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(NdsImage.open(PARENT).read_file('/__arm9__.bin')),source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[b],actual_sampled_display_IDs=ids,offline_only_display_IDs=[],source_plan=str(PLAN),**PROOFS,**{f:True for f in FLAGS},evidence=evidence,full_goal_complete=False);save(MAP,mapping)
    doc=deepcopy(doc);doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),reference_map_pending=False,registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for k,p in PROOFS.items():doc[k],doc[k+'_sha256']=p,sha(Path(p).read_bytes())
    for r in doc['records']:
        r['record_index']=r['current_record_index'];r['historical_pre_actual_display_scope']={k:r[k] for k in ['current_native_UI_body_explicit_unexecuted_boundary','native_plane_verified_not_actual_English_gameplay','current_complete_native_display_pending'] if k in r}
        r.update(status=doc['status'],current_text_hex=r['current_hex'],actual_B22_display_fixture_observed=True,offline_only_native_display_checked=False,current_complete_native_display_pending=False,individual_actual_source_event_activation_not_claimed=True,native_plane_verified_not_actual_English_gameplay=False,native_display_consumer='original_null_actor_FE_24310_then5473C' if r['kind']=='system-FE' else 'original_progressive_54020',current_native_UI_body_explicit_unexecuted_boundary=False,previous_registered_catalog_entry=None,registered_runtime_catalog_entry=None)
    assert [r['english'] for r in doc['records']]==[r['english'] for r in read(INPUT)['records']];validate_natural_dialogue_batch(doc);save(OUTPUT,doc);ROOT.mkdir(parents=True)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),all20_source_native_reference_and_representative_rules_approved=True,source_prose_English_and_compiled_targets_unchanged=True,actual_sampled_display_IDs=ids,offline_only_display_IDs=[],revised=12,retained=8,all_measured_timing_RNG_state_and_prompt_differences_preserved=True,registered_release_and_current_startup_pending=True,evidence=evidence,new_editorial_credit=0,full_goal_complete=False));print('B204 sealed20 objects:12 revisions/8 retentions;77 actual complete native holds. References,controls,source-baseline differences and PRNG limits explicit. Registered integration next.')
