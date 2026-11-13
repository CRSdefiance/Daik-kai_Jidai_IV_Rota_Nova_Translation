"""Seal all28 source-bound B206 speech/choice decisions and the complete relocation."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B206_reference_approval_v6322')
INPUT=Path('translations/lil_B206_editorial_manuscript_v7.json')
CHOICE_INPUT=Path('translations/lil_B206_choice_manuscript_v3.json')
OUTPUT=Path('translations/lil_B206_editorial_manuscript_v8.json')
CHOICE_OUTPUT=Path('translations/lil_B206_choice_manuscript_v4.json')
MAP=Path('translations/lil_B206_editorial_relocation_map_v1.json')
PARENT=Path('out/all_routes_combined_v6270_candidate.nds')
ROM=Path('out/lil_B206_reference_v6307_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B206_relocation_v6301/nested_source_relocation_research.json')
PROOFS={
 'source_census':'work/analysis/lil_B206_reference_census_v6309/all42_commands_eight_relative_sites_and_shipped_entry_census.json',
 'loader_proof':'work/analysis/lil_B206_loader_v6308/whole_SC2_and_B206_initial_entry_proof.json',
 'final_padding_proof':'work/analysis/lil_B206_stored_v6302/all24_final_stored_targets96_macro_cases_and_complete_planes.json',
 'final_typed_menu_proof':'work/analysis/lil_B206_stored_choices_v6303/two_final_typed_objects_four_label_references_and_both_even_alignments.json',
 'relocated_control_proof':'work/analysis/lil_B206_relocated_controls_v6311/all24_dispatches_picture_three47xx_three_A000_and10_guarded_ends.json',
 'termination_decode_proof':'work/analysis/lil_B206_ends_v6310/two_declared_tail_end_decodes_eight_relative_sites.json',
 'actual_proof':'work/analysis/lil_B206_actual_v6319/all24_English_panels55_observations217_native_holds_five_menus_three_same_code_paths.json',
 'representative_proof':'work/analysis/lil_B206_actual_review_v6321/viewed24_panels_four_labels_three_paths_and_measured_later_scope.json',
 'native_approval':'work/analysis/lil_B206_native_approval_v6299/all28_source_prose_current_native_approval.json'}
FLAGS=[
 'all42_commands24_preambles8_opaque_leaves_two2100_eight_relative_sites_complete',
 'all1524_predecessor_bytes_inverse_source1522_logical_tail2_target1580_no_tail',
 'all24_actual_panels55_observations217_complete_native_text_and_nameplate_holds',
 'four_labels_five_actual_menu_visits13_holds_all_three_branch_paths_bound',
 'picture138_three47xx_three_A000_zero_FE_zero_macros_and_single_end_preserved',
 'measured81_timing8_RNG114_later_RGB_differences_and_final_state_scope_preserved',
 'five_exact_source_ordinary_boundaries_ten_rowcount_reasons_no_blanket_waiver',
 'Shady_Man_integrated_Lil_Cristina_retained_all207_names_alias_queue_still_open',
 'natural_event206_earned_progress_payment_full_effects_routes_hardware_unclaimed']
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,OUTPUT,CHOICE_OUTPUT,MAP])
    doc,menu,plan=map(read,[INPUT,CHOICE_INPUT,PLAN]);proofs={k:read(p) for k,p in PROOFS.items()}
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==menu['current_ROM_sha256']==plan['candidate_sha256']
    assert plan['manuscript_sha256']==sha(INPUT.read_bytes()) and plan['choices_sha256']==sha(CHOICE_INPUT.read_bytes())
    actual,view,native=[proofs[k] for k in ['actual_proof','representative_proof','native_approval']]
    assert not any(actual[k] for k in ['failures','paired_nontext_region_differences','command_result_differences','command_UI_word_differences','offline_only_display_IDs'])
    assert (actual['actual_unique_speech_panels'],actual['actual_English_speech_observations'],actual['complete_native_text_and_nameplate_holds'])==(24,55,217)
    assert len(actual['actual_menu_cases'])==5 and sum(len(r['holds']) for r in actual['actual_menu_cases'])==13
    assert not view['visual_review_pending'] and view['no_open_translation_specific_display_menu_control_or_return_finding'] and view['all_jobs_terminal_and_reaped']
    assert native['all28_five_gates_approved'] and native['source_and_formatter_negative_controls']==41 and len(native['ten_individual_source_target_rowcount_reasons'])==10 and len(native['five_reviewed_ordinary_boundaries'])==5
    assert [len(actual[k]) for k in ['command_timing_differences','command_RNG_differences','later_whole_RGB_differences']]==[81,8,114]
    assert view['actual_proof_sha256']==sha(Path(PROOFS['actual_proof']).read_bytes())
    for s in view['viewed_sheets']+view['viewed_acquisition_frames']:
        assert s['viewed_after_image_return'] and s['viewed'] and sha(Path(s['path']).read_bytes())==s['sha256']
    assert len(view['viewed_sheets'])==9 and len(view['viewed_acquisition_frames'])==2
    ids=[r['id'] for r in doc['records']];assert len(ids)==24 and set(ids)=={r['id'] for r in actual['actual_panels']}
    assert (sum(r['editorial_decision']=='revise' for r in doc['records']),sum(r['editorial_decision']=='retain-wording' for r in doc['records']))==(14,10)
    assert len(menu['records'])==4 and [r['english'] for r in menu['records']]==['Got it','So?',"I'll take them!","That's expensive..."]
    assert (sum(r['editorial_decision']=='revise' for r in menu['records']),sum(r['editorial_decision']=='retain-wording' for r in menu['records']))==(2,2)
    block=deepcopy(plan['blocks'][0]);census=proofs['source_census']['blocks'][0]
    assert (block['block'],block['source_bytes'],block['source_logical_end'],block['research_bytes'],block['research_logical_end'])==(206,1524,1522,1580,1580)
    assert len(block['command_map'])==42 and len(block['relative_skip_fixups'])==8 and len(block['target_native_skip_cases'])==40
    assert len(block['choice_commands'])==2 and len(block['text_records'])==24 and block['inverse_plus_original_two_tailzeros_recovers_every_stored_source_byte']
    block['target_block_sha256']=block.pop('research_block_sha256');block.update(mapped_native_commands=census['mapped_commands'],external_references_complete=True,entry_point_offset=8,external_entry_and_actual_revised_paths_approval_pending=False,actual_sampled_display_IDs=ids,offline_only_display_IDs=[])
    for k in ['source_census','relocated_control_proof','termination_decode_proof']:assert proofs[k]['research_ROM_sha256']==sha(ROM.read_bytes())
    evidence={str(p):sha(Path(p).read_bytes()) for p in [INPUT,CHOICE_INPUT,PLAN,*PROOFS.values(),Path(__file__)]}
    for proof in proofs.values():
        assert not proof.get('full_goal_complete')
        for p,h in proof.get('evidence',{}).items():assert sha(Path(p).read_bytes())==h
    mapping=dict(format='dk4-lil-B206-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(NdsImage.open(PARENT).read_file('/__arm9__.bin')),
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
            pending=[k for k in r if k.endswith('_pending') or k.startswith('native_plane_verified_not_')]
            r['historical_pre_actual_display_scope']={k:r[k] for k in pending}
            for k in pending:r[k]=False
            r.update(status=batch['status'],current_text_hex=r['current_hex'],actual_B22_display_fixture_observed=True,offline_only_native_display_checked=False,current_complete_native_display_pending=False,individual_actual_source_event_activation_not_claimed=True)
            if r['kind']=='typed-choice-label':r.update(native_display_consumer='original2100_two_option_modal51FC0',actual_label_visible=True,actual_choice_all_outcomes_observed=True)
            else:r['native_display_consumer']='original_progressive_54020'
        if out==OUTPUT:batch.update(typed_choice_manuscript=str(CHOICE_OUTPUT),typed_choice_manuscript_sha256=sha(CHOICE_OUTPUT.read_bytes()),all28_five_gates_approved_English_scene_relocation_and_registered_release_pending=False,all28_source_native_reference_actual_approved_registered_release_pending=True)
        else:batch['actual_English_choice_association_and_relocated_scene_still_pending']=False
        assert [r['english'] for r in batch['records']]==[r['english'] for r in read(old)['records']]
        validate_natural_dialogue_batch({**batch,'encoder':'dialogue-relocatable-v1'} if out==CHOICE_OUTPUT else batch);save(out,batch)
    ROOT.mkdir(parents=True);save(ROOT/'approval_receipt.json',dict(manuscripts={str(p):sha(p.read_bytes()) for p in [OUTPUT,CHOICE_OUTPUT]},reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        evidence=evidence,all28_source_native_reference_and_representative_rules_approved=True,source_prose_English_and_compiled_targets_unchanged=True,actual_sampled_display_IDs=ids,offline_only_display_IDs=[],
        revised=16,retained=12,registered_release_and_current_startup_pending=True,all_measured_timing_RNG_state_and_RGB_differences_preserved=True,all207_names_alias_queue_and_full_editorial_goal_open=True,new_editorial_credit=0,full_goal_complete=False))
    print('B206 sealed28 objects:16 revisions/12 retentions. All24 panels,four labels and three paths observed;measured differences and full scope retained. Registered integration next.')
