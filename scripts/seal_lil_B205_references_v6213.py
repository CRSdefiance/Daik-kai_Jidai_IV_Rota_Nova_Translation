"""Seal complete B205 relocation and actual source/revised observations before registration."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B205_references_v6200 import PARENT,ROM,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B205_reference_approval_v6213');INPUT=Path('translations/lil_B205_editorial_manuscript_v6.json');OUTPUT=Path('translations/lil_B205_editorial_manuscript_v7.json');MAP=Path('translations/lil_B205_editorial_relocation_map_v1.json')
PROOFS={
 'source_census':'work/analysis/lil_B205_reference_census_v6206/all25_commands_no_relative_sites_and_shipped_entry_census.json',
 'loader_proof':'work/analysis/lil_B205_loader_v6205/whole_SC2_and_B205_initial_entry_proof.json',
 'final_padding_proof':'work/analysis/lil_B205_stored_v6202/all17_final_stored_targets68_macro_cases_and_complete_planes.json',
 'relocated_control_proof':'work/analysis/lil_B205_relocated_controls_v6208/all17_dispatches_one_picture_one47xx_pair_and8_exact_leaves.json',
 'termination_decode_proof':'work/analysis/lil_B205_ends_v6207/two_declared_tail_end_decodes_no_relative_sites.json',
 'actual_proof':'work/analysis/lil_B205_actual_v6211/all17_actual_English_panels_complete_native_holds_source_comparison_and_return.json',
 'representative_proof':'work/analysis/lil_B205_actual_review_v6212/viewed17_panels_five_echoes_two_sounds_complete_return_and_honest_scope.json',
 'postscene_native_state_proof':'work/analysis/lil_B205_actual_review_v6212/source_scoped_transitions_timing_RNG_and_native_state.json',
 'native_approval':'work/analysis/lil_B205_native_approval_v6196/all17_source_prose_current_native_approval.json',
 'source_nameplate_consumer_proof':'work/analysis/lil_B205_names_v6174/four_original_progressive_and_catalogue_name_consumers.json',
 'actor_voice_contract':'work/analysis/lil_B205_voices_v6173/current207_catalog_eight_voices_and_two_source_selectors.json',
 'current_actor_name_preservation':'work/analysis/lil_B205_source_view_v6184/complete_source_scenes_and_return_visual_review.json',
 'contextual_reconciliation':'work/analysis/lil_B205_source_view_v6184/complete_source_scenes_and_return_visual_review.json',
 'source_effect_and_predicate_contract':'work/analysis/lil_B205_controls_v6179/eight_exact_leaves_picture147_47xx_two63xx_three_A000_and_guarded_end.json',
}
FLAGS=['all25_commands17_preambles8_leaves_complete_no_relative_or_menu',
 'all620_predecessor_bytes_inverse_source620_target580_logical578_target_tail2',
 'all17_actual_panels63_complete_native_holds_five_echoes_two_sounds',
 'two_source_actors_voices10_progressive7_FE_no_FI_FA_FO_preserved',
 'five_word_exact_echo_pairs_and_complete_capture_joke_preserved',
 'Rainbow_Parrot_item_card_and7150_acquired_notice_retained_without_duplicate_credit',
 'same_current_ARM9_COMMON_all_components_and_ordinary_inputs_source_baseline_bound',
 'all34_command_timings_and_interval_RNG_equal_98_later_whole_RGB_samples_equal',
 'queried_native_groups_actor_and_PRNG_equal_no_broad_world_equivalence',
 'representative_shared_rules_approved_natural_activation_original_location_full_effects_and_hardware_unclaimed']
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,OUTPUT,MAP]);doc,plan=map(read,[INPUT,PLAN]);proofs={k:read(p) for k,p in PROOFS.items()}
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256'] and plan['manuscript_sha256']==sha(INPUT.read_bytes())
    a,v,s,n=[proofs[k] for k in ['actual_proof','representative_proof','postscene_native_state_proof','native_approval']]
    assert a['actual_unique_speech_panels']==a['complete_matching_observations']==17 and a['complete_matching_holds']==63 and not a['failures'] and not a['offline_only_display_IDs']
    assert n['all17_five_gates_approved'] and len(n['formatter_negative_controls'])==28 and len(n['three_individual_rowcount_reasons'])==3
    assert not v['visual_review_pending'] and v['no_open_translation_specific_display_control_or_return_finding'] and len(v['viewed_sheets'])==5
    for r in v['viewed_sheets']:assert r['viewed'] and r['viewed_after_image_return'] and sha(Path(r['path']).read_bytes())==r['sha256']
    assert not a['source_English_command_timing_differences'] and not a['source_English_command_RNG_differences'] and not a['nontext_differences_retained_without_filtering_native_text_holds']
    assert s['source_exit_frame']==s['English_exit_frame']==7175 and s['later_whole_RGB_equal_samples']==98 and not s['later_source_English_RGB_differences'] and s['generated_Rainbow_Parrot_notice_same_frame_whole_RGB_equal_at7150']
    assert all(s['native_final_component_equality'].values()) and s['whole_actor_and_captain_equal'] and s['final_PRNG_equal'] and s['no_whole_state_or_future_sequence_equivalence_claim']
    ids=[r['id'] for r in doc['records']];assert ids==[r['id'] for r in a['actual_panels']];b=deepcopy(plan['blocks'][0]);census=proofs['source_census']['blocks'][0]
    assert (b['block'],b['source_bytes'],b['source_logical_end'],b['research_bytes'],b['research_logical_end'])==(205,620,620,580,578)
    assert len(b['command_map'])==25 and len(b['text_records'])==17 and not any(b[k] for k in ['relative_skip_fixups','target_native_skip_cases','choice_commands','actor_style_commands','original2000_pause_and_resume_maps'])
    assert b['inverse_plus_original_zero_tailbytes_recovers_every_stored_source_byte'];b['target_block_sha256']=b.pop('research_block_sha256');b.update(mapped_native_commands=census['mapped_commands'],external_references_complete=True,entry_point_offset=8,external_entry_and_actual_revised_paths_approval_pending=False,actual_sampled_display_IDs=ids,offline_only_display_IDs=[],source_alignment_tail_bytes=0,target_alignment_tail_bytes=2)
    for k in ['source_census','relocated_control_proof','termination_decode_proof']:assert proofs[k]['research_ROM_sha256']==sha(ROM.read_bytes())
    assert proofs['current_actor_name_preservation']['current_screenshot_pair_names'][0]['current_catalog_name']=='Man' and proofs['current_actor_name_preservation']['current_screenshot_pair_names'][1]['current_catalog_name']=='Woman'
    evidence={str(p):sha(Path(p).read_bytes()) for p in [INPUT,PLAN,*PROOFS.values(),Path(__file__)]}
    mapping=dict(format='dk4-lil-B205-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(NdsImage.open(PARENT).read_file('/__arm9__.bin')),source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[b],actual_sampled_display_IDs=ids,offline_only_display_IDs=[],source_plan=str(PLAN),**PROOFS,**{f:True for f in FLAGS},evidence=evidence,full_goal_complete=False);save(MAP,mapping)
    doc=deepcopy(doc);doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),reference_map_pending=False,registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for k,p in PROOFS.items():doc[k],doc[k+'_sha256']=p,sha(Path(p).read_bytes())
    for r in doc['records']:
        r['record_index']=r['current_record_index'];r['historical_pre_actual_display_scope']={k:r[k] for k in ['current_native_UI_body_explicit_unexecuted_boundary','native_plane_verified_not_actual_English_gameplay','current_complete_native_display_pending'] if k in r};r.update(status=doc['status'],current_text_hex=r['current_hex'],actual_B22_display_fixture_observed=True,offline_only_native_display_checked=False,current_complete_native_display_pending=False,individual_actual_source_event_activation_not_claimed=True,native_plane_verified_not_actual_English_gameplay=False,native_display_consumer='original_null_actor_FE_24310_then5473C' if r['kind']=='system-FE' else 'original_progressive_54020',current_native_UI_body_explicit_unexecuted_boundary=False,previous_registered_catalog_entry=None,registered_runtime_catalog_entry=None)
    assert [r['english'] for r in doc['records']]==[r['english'] for r in read(INPUT)['records']];validate_natural_dialogue_batch(doc);save(OUTPUT,doc);ROOT.mkdir(parents=True);save(ROOT/'approval_receipt.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),all17_source_native_reference_and_representative_rules_approved=True,source_prose_English_and_compiled_targets_unchanged=True,actual_sampled_display_IDs=ids,offline_only_display_IDs=[],revised=8,retained=9,all_measured_timing_RNG_state_and_RGB_scopes_preserved=True,registered_release_and_current_startup_pending=True,evidence=evidence,new_editorial_credit=0,full_goal_complete=False));print('B205 sealed17 objects:8 revisions/9 retentions;63 actual native holds,25 commands/eight leaves,end616-to574 and target tail2. Registered integration next.')
