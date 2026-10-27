"""Seal159 source/current/target references under representative test policy."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B122_B127_reference_approval_v3295')
MAP=Path('translations/lil_B122_B127_editorial_relocation_map_v1.json')
INPUTS=[Path('translations/lil_B122_B127_editorial_manuscript_v5.json'),Path('translations/lil_B122_B127_choice_manuscript_v4.json')]
OUTPUTS=[Path('translations/lil_B122_B127_editorial_manuscript_v6.json'),Path('translations/lil_B122_B127_choice_manuscript_v5.json')]
PLAN=Path('work/analysis/lil_B122_B127_relocation_v3288b/nested_source_relocation_research.json')
CENSUS=Path('work/analysis/lil_B122_B127_reference_census_v3291/all312_commands64_relative_sites_and_shipped_entry_census.json')
SAMPLE=Path('work/analysis/lil_B122_B127_sampling_v3294/representative_rules_and_focused_current_native_reconciliation.json')
PADDING=Path('work/analysis/lil_B122_B127_research_v3289b/research_image_receipt.json')
CONTROL=Path('work/analysis/lil_B122_B127_relocated_controls_v3292/all155_relocated_dispatches_and14_predicate_pairs.json')
RETURN=Path('work/analysis/lil_trade_branch_return_v3293/original_choice_control_paths_and_both_VM_return_modes.json')
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,MAP,*OUTPUTS]);plan,census,sample,padding,control,branch=map(read,[PLAN,CENSUS,SAMPLE,PADDING,CONTROL,RETURN]);docs=[deepcopy(read(p)) for p in INPUTS]
    assert census['all312_clean_current_target_commands_and64_relative_sites_reexecuted'] and census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert sample['no_open_translation_specific_display_or_control_finding'] and not sample['actual_selected_B122_B127_IDs']
    assert padding['all155_final_targets_complete_native_planes_equal_reviewed_planes'] and padding['current_final_padded_macro_alignment_cases']==620 and padding['all2_final2100_objects_four_labels_and6_selection_cancel_cases_bound'] and padding['both_original_pause_resume_words_and20_decoder_cases_bound']
    assert control['all14_predicate_current_relocated_results_and_source_operands_equal'] and control['all10_FE_preserve_original_null_actor_before_dynamic_fallback'] and not control['original_event_queries']
    assert branch['source_current_target_branch_endings_preserved'] and len(branch['original_VM_return_cases'])==12
    historical_review=Path('work/analysis/lil_Seville_reference_approval_v2722/representative_sheet_review.json');current_review=Path('work/analysis/lil_B111_B119_completion_v3255/current_six_frame_visual_review.json')
    for p in [historical_review,current_review]:
        r=read(p);assert r['viewed'] and sha(Path(r['sheet']).read_bytes())==r['sha256']
    blocks=[]
    for original,checked in zip(plan['blocks'],census['blocks'],strict=True):
        assert original['block']==checked['block'] and checked['entry_point_offset']==8
        spec=deepcopy(original);spec['target_block_sha256']=spec.pop('research_block_sha256');spec.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],external_entry_and_actual_revised_paths_approval_pending=False,individual_selected_B122_B127_gameplay_unobserved=True);blocks.append(spec)
    assert len(blocks)==6 and sum(len(b['command_map']) for b in blocks)==312 and sum(len(b['text_records']) for b in blocks)==155 and sum(len(b['choice_commands']) for b in blocks)==2 and not any(b['actor_style_commands'] for b in blocks)
    assert sum(len(b['original2000_pause_and_resume_maps']) for b in blocks)==2
    image=NdsImage.open(plan['candidate']);evidence={str(p):sha(p.read_bytes()) for p in [*INPUTS,PLAN,CENSUS,SAMPLE,PADDING,CONTROL,RETURN,historical_review,current_review,Path(docs[0]['original2000_wait_proof']),Path(__file__)]}
    mapping=dict(format='dk4-lil-B122-B127-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(image.read_file('/__arm9__.bin')),source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=blocks,all312_physical_nested_command_boundaries_and64_relative_sites_verified=True,all320_relocated_relative_skip_cases_preserve_original_targets=True,all14_relocated_predicate_pairs_preserve_source_operands_results_and_unowned_RAM=True,original_event_queries=[],all155_active_speech_targets_preserved=True,two2100_objects_four_labels_and_source_indices_0_1_cancel_verified=True,two_original2000_pause_words_and_mapped_resume_boundaries_verified=True,trade_choice0_tutorial_choice1_already_know_branch_and_return0_both_VM_modes_verified=True,no_dynamic_selector_or4100_objects=True,representative_shared_rules_approved=True,representative_proof=str(SAMPLE),historical_representative_sheet_review=str(historical_review),prior_current_sheet_review=str(current_review),source_plan=str(PLAN),source_census=str(CENSUS),final_padding_proof=str(PADDING),relocated_control_proof=str(CONTROL),conditional_return_proof=str(RETURN),evidence=evidence,actual_selected_B122_B127_IDs=[],individual_conditional_visits_not_required_under_user_policy=True,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(MAP,mapping)
    for doc,old,new in zip(docs,INPUTS,OUTPUTS,strict=True):
        doc.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),representative_proof=str(SAMPLE),representative_proof_sha256=sha(SAMPLE.read_bytes()),historical_representative_sheet_review=str(historical_review),prior_current_sheet_review=str(current_review),prose_companions=[str(p) for p in OUTPUTS if p!=new],final_padding_proof=str(PADDING),final_padding_proof_sha256=sha(PADDING.read_bytes()),relocated_control_proof=str(CONTROL),relocated_control_proof_sha256=sha(CONTROL.read_bytes()),conditional_return_proof=str(RETURN),conditional_return_proof_sha256=sha(RETURN.read_bytes()),reference_map_pending=False,registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
        for row in doc['records']:
            row.update(status=doc['status'],current_text_hex=row['current_hex'],native_display_consumer='original2100_two_option_modal51FC0' if row['kind']=='typed-choice-label' else 'original_FE_modal_5473C_mode1' if row['kind']=='system-FE' else 'original_progressive_54020')
        assert [r['english'] for r in doc['records']]==[r['english'] for r in read(old)['records']]
    docs[0].update(choice_companion=str(OUTPUTS[1]),choices=str(OUTPUTS[1]),native_FE_font_proof=docs[0]['native_FE_proof'],native_FE_font_proof_sha256=sha(Path(docs[0]['native_FE_proof']).read_bytes()))
    for doc,new in zip(docs,OUTPUTS,strict=True):validate_natural_dialogue_batch(doc);save(new,doc)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(OUTPUTS[0]),choices=str(OUTPUTS[1]),reference_map=str(MAP),hashes={str(p):sha(p.read_bytes()) for p in [*OUTPUTS,MAP,*INPUTS,PLAN,CENSUS,SAMPLE,PADDING,CONTROL,RETURN,historical_review,current_review]},source_prose_English_unchanged=True,all159_source_native_reference_and_representative_rules_approved=True,both2000_pauses_and_two2100_menus_and_conditional_return0_preserved=True,actual_selected_B122_B127_IDs=[],new_emulator_runs=0,registered_release_and_current_startup_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Sealed159 source/native/reference/representative approvals:312 commands/64 spans/320 skip cases,155 dispatches/14 predicates,two menus/two pauses andconditional return. Registered release/startup pending.')
