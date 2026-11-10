"""Seal the complete source-bound B208 manuscript and reversible reference map."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.create_lil_B208_reference_v6424 import PARENT,ROM,PLAN
from scripts.review_lil_B208_actual_v6433 import ACTUAL,LATER
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B208_reference_approval_v6434');INPUT=Path('translations/lil_B208_editorial_manuscript_v6.json');OUTPUT=Path('translations/lil_B208_editorial_manuscript_v7.json');MAP=Path('translations/lil_B208_editorial_relocation_map_v1.json')
PROOFS={
 'source_census':'work/analysis/lil_B208_reference_census_v6426/all29_commands_no_relative_sites_and_shipped_entry_census.json',
 'loader_proof':'work/analysis/lil_B208_loader_v6425/whole_SC2_and_B208_initial_entry_proof.json',
 'final_padding_proof':'work/analysis/lil_B208_stored_v6423b/all24_final_stored_targets96_macro_cases_and_complete_planes.json',
 'relocated_control_proof':'work/analysis/lil_B208_relocated_controls_v6428/all24_dispatches_four_structural_effects_and10_guarded_ends.json',
 'termination_decode_proof':'work/analysis/lil_B208_ends_v6427/two_declared_tail_end_decodes_no_relative_sites.json',
 'actual_proof':str(ACTUAL),'postscene_native_state_proof':str(LATER),
 'representative_proof':'work/analysis/lil_B208_actual_review_v6433/viewed24_panels95_holds_thought_FE_and_honest_broader_later_scope.json',
 'native_approval':'work/analysis/lil_B208_native_approval_v6421/all24_source_prose_current_native_approval.json',
 'speaker_name_approval':'work/analysis/lil_B208_name_approval_v6406/two_name_retentions91_headers_no_asset_change.json'}
FLAGS=['all29_commands24_preambles_five_opaque_leaves_no_relative_menu_macro',
 'all1188_predecessor_bytes_inverse_source1186_tail2_target1194_tail2',
 'all24_actual_panels95_native_holds_thought_named_FE_and_town_sailing_return',
 'Cristina_Erneco_Mysterious_Old_Man_contextual_name_retentions_style11_no_asset_change',
 'same_current_ARM9_COMMON_all_components_and_ordinary_inputs_source_baseline_bound',
 'all16_timing18_RNG44_broader_RGB_eight_duration_and_different_final_states_retained',
 'state_tasks_equal_other_queried_groups_actor_calendar_and_PRNG_differ_no_world_equivalence',
 'source_face_presence_conjecture_hearsay_limited_commitment_thought_and_Charm_plus1_preserved',
 'proven_exact_phase_reservation_one_it_during_boundary_four_rowcount_reasons_no_blanket_waiver',
 'natural_activation_original_location_earned_progress_full_effects_routes_hardware_unclaimed']
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,OUTPUT,MAP]);doc,plan=read(INPUT),read(PLAN);proofs={k:read(p) for k,p in PROOFS.items()}
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256'] and plan['manuscript_sha256']==sha(INPUT.read_bytes())
    a,v,n,s=[proofs[k] for k in ['actual_proof','representative_proof','native_approval','postscene_native_state_proof']]
    assert a['actual_unique_speech_panels']==24 and a['complete_native_text_and_nameplate_holds']==95 and not a['failures'] and not a['offline_only_display_IDs']
    assert n['all24_five_gates_approved'] and n['source_and_formatter_negative_controls']==30 and len(n['four_individual_source_target_rowcount_reasons'])==4 and n['covered_native_alignment_cases']==192 and n['additional_phase_native_alignment_cases']==12
    assert not v['visual_review_pending'] and len(v['viewed_sheets'])==6 and v['no_open_translation_specific_display_control_or_return_finding']
    for r in v['viewed_sheets']:assert r['viewed'] and r['viewed_after_image_return'] and sha(Path(r['path']).read_bytes())==r['sha256']
    assert [len(a[k]) for k in ['command_timing_differences','command_RNG_differences','later_whole_RGB_differences']]==[16,18,44]
    assert s['five_native_component_equality']==dict(state=True,models=False,persistent_objects=False,tasks=True,calendar=False) and not s['whole_actor_and_captain_equal'] and not s['final_PRNG_equal']
    ids=[r['id'] for r in doc['records']];assert ids==[r['id'] for r in a['actual_panels']];b=deepcopy(plan['blocks'][0]);census=proofs['source_census']['blocks'][0]
    assert (b['block'],b['source_bytes'],b['source_logical_end'],b['research_bytes'],b['research_logical_end'])==(208,1188,1186,1196,1194)
    assert len(b['command_map'])==29 and len(b['text_records'])==24 and not any(b[k] for k in ['relative_skip_fixups','target_native_skip_cases','choice_commands','actor_style_commands','original2000_pause_and_resume_maps'])
    assert b['inverse_plus_original_two_tailzeros_recovers_every_stored_source_byte'];b['target_block_sha256']=b.pop('research_block_sha256');b.update(mapped_native_commands=census['mapped_commands'],external_references_complete=True,entry_point_offset=8,external_entry_and_actual_revised_paths_approval_pending=False,actual_sampled_display_IDs=ids,offline_only_display_IDs=[],source_alignment_tail_bytes=2,target_alignment_tail_bytes=2)
    for k in ['source_census','relocated_control_proof','termination_decode_proof']:assert proofs[k]['research_ROM_sha256']==sha(ROM.read_bytes())
    evidence={str(p):sha(Path(p).read_bytes()) for p in [INPUT,PLAN,*PROOFS.values(),Path(__file__)]}
    mapping=dict(format='dk4-lil-B208-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(NdsImage.open(PARENT).read_file('/__arm9__.bin')),source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[b],actual_sampled_display_IDs=ids,offline_only_display_IDs=[],source_plan=str(PLAN),**PROOFS,**{f:True for f in FLAGS},evidence=evidence,full_goal_complete=False);save(MAP,mapping)
    doc=deepcopy(doc);doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),reference_map_pending=False,registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for k,p in PROOFS.items():doc[k],doc[k+'_sha256']=p,sha(Path(p).read_bytes())
    for r in doc['records']:
        r['historical_pre_actual_display_scope']={k:r[k] for k in ['current_native_UI_body_explicit_unexecuted_boundary','native_plane_verified_not_actual_English_gameplay','current_complete_native_display_pending'] if k in r};r.update(status=doc['status'],current_text_hex=r['current_hex'],actual_B22_display_fixture_observed=True,offline_only_native_display_checked=False,current_complete_native_display_pending=False,individual_actual_source_event_activation_not_claimed=True,native_plane_verified_not_actual_English_gameplay=False,native_display_consumer='original_null_actor_FE_24310_then5473C' if r['kind']=='system-FE' else 'original_progressive_54020',current_native_UI_body_explicit_unexecuted_boundary=False,previous_registered_catalog_entry=None,registered_runtime_catalog_entry=None)
    assert [r['english'] for r in doc['records']]==[r['english'] for r in read(INPUT)['records']];validate_natural_dialogue_batch(doc);save(OUTPUT,doc);ROOT.mkdir(parents=True)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),all24_source_native_reference_and_representative_rules_approved=True,source_prose_English_and_compiled_targets_unchanged=True,actual_sampled_display_IDs=ids,offline_only_display_IDs=[],revised=15,retained=9,all_measured_timing_RNG_state_and_RGB_scopes_preserved=True,registered_release_and_current_startup_pending=True,evidence=evidence,new_editorial_credit=0,full_goal_complete=False));print('B208 sealed24 records:15 revisions/9 justified retentions;95 actual holds and all38 commands. Registered integration next;all broader state limits retained.')
