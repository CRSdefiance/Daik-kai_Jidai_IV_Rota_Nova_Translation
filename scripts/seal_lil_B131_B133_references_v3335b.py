"""Seal159 source/current/target references under representative test policy."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B131_B133_reference_approval_v3335b')
MAP=Path('translations/lil_B131_B133_editorial_relocation_map_v1.json')
INPUTS=[Path('translations/lil_B131_B133_editorial_manuscript_v4.json'),Path('translations/lil_B131_B133_choice_manuscript_v5.json')]
OUTPUTS=[Path('translations/lil_B131_B133_editorial_manuscript_v5.json'),Path('translations/lil_B131_B133_choice_manuscript_v6.json')]
PLAN=Path('work/analysis/lil_B131_B133_relocation_v3329b/nested_source_relocation_research.json')
CENSUS=Path('work/analysis/lil_B131_B133_reference_census_v3332/all112_commands24_relative_sites_and_shipped_entry_census.json')
SAMPLE=Path('work/analysis/lil_B131_B133_sampling_v3334/representative_rules_and_focused_current_native_reconciliation.json')
PADDING=Path('work/analysis/lil_B131_B133_research_v3330b/research_image_receipt.json')
CONTROL=Path('work/analysis/lil_B131_B133_relocated_controls_v3333b/all61_relocated_dispatches_source00_and5_predicate_pairs.json')
TYPED=Path('work/analysis/lil_B131_B133_typed_speech_v3323/all366_whole4000_commands_and108_source00_cases.json')
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,MAP,*OUTPUTS]);plan,census,sample,padding,control,typed=map(read,[PLAN,CENSUS,SAMPLE,PADDING,CONTROL,TYPED]);docs=[deepcopy(read(p)) for p in INPUTS]
    assert census['all112_clean_current_target_commands_and24_relative_sites_reexecuted'] and census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert sample['no_open_translation_specific_display_or_control_finding'] and not sample['actual_selected_B131_B133_IDs']
    assert padding['all61_final_targets_complete_native_planes_equal_reviewed_planes'] and padding['current_final_padded_macro_alignment_cases']==244 and padding['all1_final2100_object_two_labels_and3_selection_cancel_cases_bound'] and padding['no_source2000_pause_commands'] and padding['all18_final_source00_speech_prefixes_and_nonempty_bodies_preserved']
    assert control['all5_predicate_current_relocated_results_and_source_operands_equal'] and control['all1_FE_preserves_original_null_actor_before_dynamic_fallback'] and not control['original_event_queries']
    assert len(typed['cases'])==366 and typed['all108_source00_cases_forward_nonempty_body_after_selector_to_original_display']
    historical_review=Path('work/analysis/lil_Seville_reference_approval_v2722/representative_sheet_review.json');current_review=Path('work/analysis/lil_B122_B127_startup_v3303/current_six_frame_visual_review.json')
    for p in [historical_review,current_review]:
        r=read(p);assert r['viewed'] and sha(Path(r['sheet']).read_bytes())==r['sha256']
    blocks=[]
    for original,checked in zip(plan['blocks'],census['blocks'],strict=True):
        assert original['block']==checked['block'] and checked['entry_point_offset']==8
        spec=deepcopy(original);spec['target_block_sha256']=spec.pop('research_block_sha256');spec.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],external_entry_and_actual_revised_paths_approval_pending=False,individual_selected_B131_B133_gameplay_unobserved=True);blocks.append(spec)
    assert len(blocks)==2 and sum(len(b['command_map']) for b in blocks)==112 and sum(len(b['text_records']) for b in blocks)==61 and sum(len(b['choice_commands']) for b in blocks)==1 and not any(b['actor_style_commands'] for b in blocks)
    assert sum(len(b['original2000_pause_and_resume_maps']) for b in blocks)==0
    image=NdsImage.open(plan['candidate']);evidence={str(p):sha(p.read_bytes()) for p in [*INPUTS,PLAN,CENSUS,SAMPLE,PADDING,CONTROL,TYPED,historical_review,current_review,Path(__file__)]}
    mapping=dict(format='dk4-lil-B131-B133-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(image.read_file('/__arm9__.bin')),source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=blocks,all112_physical_nested_command_boundaries_and24_relative_sites_verified=True,all120_relocated_relative_skip_cases_preserve_original_targets=True,all5_relocated_predicate_pairs_preserve_source_operands_results_and_unowned_RAM=True,original_event_queries=[],all61_active_speech_targets_preserved=True,one2100_object_two_labels_and_source_indices_0_1_cancel_verified=True,no_source2000_pause_commands=True,all18_source00_prefixes_and_nonempty_bodies_verified=True,no_dynamic_selector_or4100_objects=True,representative_shared_rules_approved=True,representative_proof=str(SAMPLE),historical_representative_sheet_review=str(historical_review),prior_current_sheet_review=str(current_review),source_plan=str(PLAN),source_census=str(CENSUS),final_padding_proof=str(PADDING),relocated_control_proof=str(CONTROL),whole_typed_speech_proof=str(TYPED),evidence=evidence,actual_selected_B131_B133_IDs=[],individual_conditional_visits_not_required_under_user_policy=True,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(MAP,mapping)
    for doc,old,new in zip(docs,INPUTS,OUTPUTS,strict=True):
        doc.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),representative_proof=str(SAMPLE),representative_proof_sha256=sha(SAMPLE.read_bytes()),historical_representative_sheet_review=str(historical_review),prior_current_sheet_review=str(current_review),prose_companions=[str(p) for p in OUTPUTS if p!=new],final_padding_proof=str(PADDING),final_padding_proof_sha256=sha(PADDING.read_bytes()),relocated_control_proof=str(CONTROL),relocated_control_proof_sha256=sha(CONTROL.read_bytes()),whole_typed_speech_proof=str(TYPED),whole_typed_speech_proof_sha256=sha(TYPED.read_bytes()),reference_map_pending=False,registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
        for row in doc['records']:
            row.update(status=doc['status'],current_text_hex=row['current_hex'],native_display_consumer='original2100_two_option_modal51FC0' if row['kind']=='typed-choice-label' else 'original_FE_modal_5473C_mode1' if row['kind']=='system-FE' else 'original_progressive_54020')
        assert [r['english'] for r in doc['records']]==[r['english'] for r in read(old)['records']]
    docs[0].update(choice_companion=str(OUTPUTS[1]),choices=str(OUTPUTS[1]),native_FE_font_proof=docs[0]['native_FE_proof'],native_FE_font_proof_sha256=sha(Path(docs[0]['native_FE_proof']).read_bytes()))
    for doc,new in zip(docs,OUTPUTS,strict=True):validate_natural_dialogue_batch(doc);save(new,doc)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(OUTPUTS[0]),choices=str(OUTPUTS[1]),reference_map=str(MAP),hashes={str(p):sha(p.read_bytes()) for p in [*OUTPUTS,MAP,*INPUTS,PLAN,CENSUS,SAMPLE,PADDING,CONTROL,TYPED,historical_review,current_review]},source_prose_English_unchanged=True,all63_source_native_reference_and_representative_rules_approved=True,one2100_menu_and18_source00_controls_preserved=True,actual_selected_B131_B133_IDs=[],new_emulator_runs=0,registered_release_and_current_startup_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Sealed63 source/native/reference/representative approvals;registered release andstartup pending.')
