"""Seal B201's two companion manuscripts and source-bound relocation map."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B201_reference_approval_v5944')
INPUT=Path('translations/lil_B201_editorial_manuscript_v6.json')
CHOICE_INPUT=Path('translations/lil_B201_choice_manuscript_v3.json')
OUTPUT=Path('translations/lil_B201_editorial_manuscript_v7.json')
CHOICE_OUTPUT=Path('translations/lil_B201_choice_manuscript_v4.json')
MAP=Path('translations/lil_B201_editorial_relocation_map_v1.json')
PARENT=Path('out/all_routes_combined_v5891_candidate.nds')
ROM=Path('out/lil_B201_reference_v5934_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B201_relocation_v5931/nested_source_relocation_research.json')
PROOFS={
 'source_census':'work/analysis/lil_B201_reference_census_v5936/all44_commands_four_relative_sites_and_shipped_entry_census.json',
 'loader_proof':'work/analysis/lil_B201_loader_v5935/whole_SC2_and_B201_initial_entry_proof.json',
 'final_padding_proof':'work/analysis/lil_B201_stored_v5932b/all24_final_stored_targets96_macro_cases_and_complete_planes.json',
 'final_typed_menu_proof':'work/analysis/lil_B201_stored_choices_v5933/one_final_typed_object_two_references_and_both_even_alignments.json',
 'relocated_control_proof':'work/analysis/lil_B201_relocated_controls_v5938/all24_dispatches_two_FI_one_picture_two47xx_menu_and15_exact_leaves.json',
 'termination_decode_proof':'work/analysis/lil_B201_ends_v5937/two_declared_tail_end_decodes_four_relative_sites.json',
 'actual_proof':'work/analysis/lil_B201_actual_v5942/two_paths_all24_complete_panels_two_options_and_source_comparisons.json',
 'representative_proof':'work/analysis/lil_B201_actual_review_v5943/viewed24_panels_both_options_returns_and_measured_state_scope.json',
 'native_approval':'work/analysis/lil_B201_native_approval_v5925/all26_source_prose_current_native_approval.json'}
FLAGS=['all44_commands24_preambles15_opaque_leaves_one2100_four_relative_sites_complete',
 'all1452_predecessor_bytes_inverse_target1222_logical1224_stored_two_tailzeros',
 'all24_actual_panels37_observations144_complete_native_holds_source_regions_equal',
 'both_actual_choice_indices_labels_and_visible_highlights_complete',
 'two_FI_three_null_FE_and_seven_prices_final100000_preserved',
 'measured54_timing30_RNG21_later_RGB_differences_preserved_no_world_equivalence',
 'Trader_contextual_retention_no_name_bytes_or_global_name_completion_credit',
 'representative_shared_rules_approved_natural_activation_earned_affordability_hardware_unclaimed']
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,OUTPUT,CHOICE_OUTPUT,MAP])
    doc,menu,plan=map(read,[INPUT,CHOICE_INPUT,PLAN]);proofs={k:read(p) for k,p in PROOFS.items()}
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==menu['current_ROM_sha256']==plan['candidate_sha256']
    assert plan['manuscript_sha256']==sha(INPUT.read_bytes()) and plan['choices_sha256']==sha(CHOICE_INPUT.read_bytes())
    actual,view,native=[proofs[k] for k in ['actual_proof','representative_proof','native_approval']]
    assert not actual['failures'] and not actual['paired_nontext_region_differences'] and not actual['command_result_differences']
    assert (actual['actual_unique_speech_panels'],actual['actual_English_speech_observations'],actual['complete_native_holds'])==(24,37,144)
    assert not view['visual_review_pending'] and view['no_open_translation_specific_display_menu_control_or_return_finding']
    assert native['all26_five_gates_approved'] and len(native['formatter_negatives'])==28 and len(native['thirteen_individual_rowcount_reasons'])==13
    assert [len(actual[k]) for k in ['command_timing_differences','command_RNG_differences','later_whole_RGB_differences']]==[54,30,21]
    assert view['actual_proof_sha256']==sha(Path(PROOFS['actual_proof']).read_bytes())
    for s in view['viewed_sheets']:assert s['viewed_after_image_return'] and s['viewed'] and sha(Path(s['path']).read_bytes())==s['sha256']
    ids=[r['id'] for r in doc['records']];assert ids==[r['id'] for r in actual['actual_panels']]
    block=deepcopy(plan['blocks'][0]);census=proofs['source_census']['blocks'][0]
    assert (block['block'],block['source_bytes'],block['source_logical_end'],block['research_bytes'],block['research_logical_end'])==(201,1452,1452,1224,1222)
    assert len(block['command_map'])==44 and len(block['relative_skip_fixups'])==4 and len(block['target_native_skip_cases'])==20
    assert len(block['choice_commands'])==1 and len(block['text_records'])==24 and block['inverse_plus_original_zero_tailzeros_recovers_every_stored_source_byte']
    block['target_block_sha256']=block.pop('research_block_sha256');block.update(mapped_native_commands=census['mapped_commands'],external_references_complete=True,entry_point_offset=8,external_entry_and_actual_revised_paths_approval_pending=False,actual_sampled_display_IDs=ids,offline_only_display_IDs=[])
    for k in ['source_census','relocated_control_proof','termination_decode_proof']:assert proofs[k]['research_ROM_sha256']==sha(ROM.read_bytes())
    evidence={str(p):sha(Path(p).read_bytes()) for p in [INPUT,CHOICE_INPUT,PLAN,*PROOFS.values(),Path(__file__)]}
    mapping=dict(format='dk4-lil-B201-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(NdsImage.open(PARENT).read_file('/__arm9__.bin')),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[block],actual_sampled_display_IDs=ids,offline_only_display_IDs=[],
        source_plan=str(PLAN),**PROOFS,**{f:True for f in FLAGS},evidence=evidence,full_goal_complete=False)
    save(MAP,mapping)
    for batch,old,out in [(menu,CHOICE_INPUT,CHOICE_OUTPUT),(doc,INPUT,OUTPUT)]:
        batch=deepcopy(batch);batch.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),reference_map_pending=False,
            registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
        for k,p in PROOFS.items():batch[k],batch[k+'_sha256']=p,sha(Path(p).read_bytes())
        for r in batch['records']:
            r['historical_pre_actual_display_scope']={k:r[k] for k in ['current_native_typed_choice_font_reference_and_outcome_binding_pending','current_native_UI_body_explicit_unexecuted_boundary','native_plane_verified_not_actual_English_gameplay','current_native_voice_macro_entry_and_context_pending'] if k in r}
            r.update(status=batch['status'],current_text_hex=r['current_hex'],actual_B22_display_fixture_observed=True,offline_only_native_display_checked=False,current_complete_native_display_pending=False,individual_actual_source_event_activation_not_claimed=True,native_plane_verified_not_actual_English_gameplay=False)
            if r['kind']=='typed-choice-label':
                r.update(native_display_consumer='original2100_two_option_modal51FC0',actual_label_visible=True,actual_choice_all_outcomes_observed=True,current_native_typed_choice_font_reference_and_outcome_binding_pending=False)
            else:r.update(native_display_consumer='original_null_actor_FE_24310_then5473C' if r['kind']=='system-FE' else 'original_progressive_54020',current_native_UI_body_explicit_unexecuted_boundary=False,current_native_voice_macro_entry_and_context_pending=False)
        if out==OUTPUT:batch.update(typed_choice_manuscript=str(CHOICE_OUTPUT),typed_choice_manuscript_sha256=sha(CHOICE_OUTPUT.read_bytes()))
        else:batch['actual_English_choice_association_and_relocated_reference_still_pending']=False
        assert [r['english'] for r in batch['records']]==[r['english'] for r in read(old)['records']]
        validate_natural_dialogue_batch({**batch,'encoder':'dialogue-relocatable-v1'} if out==CHOICE_OUTPUT else batch);save(out,batch)
    ROOT.mkdir(parents=True);save(ROOT/'approval_receipt.json',dict(manuscripts={str(p):sha(p.read_bytes()) for p in [OUTPUT,CHOICE_OUTPUT]},reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        evidence=evidence,all26_source_native_reference_and_representative_rules_approved=True,source_prose_English_and_compiled_targets_unchanged=True,actual_sampled_display_IDs=ids,offline_only_display_IDs=[],
        revised=12,retained=14,registered_release_and_current_startup_pending=True,all_measured_timing_RNG_state_and_RGB_differences_preserved=True,new_editorial_credit=0,full_goal_complete=False))
    print('B201 sealed26 objects:12 revisions/14 retentions. All24 panels/both options observed;scope and measured differences retained. Registered integration next.')
