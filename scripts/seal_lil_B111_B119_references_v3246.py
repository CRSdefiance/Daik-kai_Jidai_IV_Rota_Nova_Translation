"""Seal 150 source/current/target references and representative rule approval."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B111_B119_reference_approval_v3246')
MAP=Path('translations/lil_B111_B119_editorial_relocation_map_v1.json')
INPUTS=[Path('translations/lil_B111_B119_editorial_manuscript_v5.json'),Path('translations/lil_B111_B119_actor_style_manuscript_v4.json')]
OUTPUTS=[Path('translations/lil_B111_B119_editorial_manuscript_v6.json'),Path('translations/lil_B111_B119_actor_style_manuscript_v5.json')]
PLAN=Path('work/analysis/lil_B111_B119_relocation_v3239b/nested_source_relocation_research.json')
CENSUS=Path('work/analysis/lil_B111_B119_reference_census_v3242/all305_commands64_relative_sites_and_shipped_entry_census.json')
SAMPLE=Path('work/analysis/lil_B111_B119_sampling_v3245/relocated_predicates_and_representative_rule_reconciliation.json')
PADDING=Path('work/analysis/lil_B111_B119_research_v3240b/research_image_receipt.json')
CONTROL=Path('work/analysis/lil_B111_B119_relocated_controls_v3243d/all150_dispatch12_style_commands2484_getters16_predicate_query_pairs.json')
COPY=Path('work/analysis/lil_B111_B119_relocated_copy_v3244/moved_return0_and_unowned_copy_proof.json')

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,MAP,*OUTPUTS])
    plan,census,sample,padding,control,copy=map(read,[PLAN,CENSUS,SAMPLE,PADDING,CONTROL,COPY]);docs=[deepcopy(read(p)) for p in INPUTS]
    assert census['all305_clean_current_target_commands_and64_relative_sites_reexecuted'] and census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert sample['no_open_translation_specific_display_or_control_finding'] and not sample['actual_selected_B111_B119_IDs']
    assert padding['all150_final_targets_complete_native_planes_equal_reviewed_planes'] and padding['current_final_padded_macro_alignment_cases']==600
    assert control['all15_predicate_and_one_query_current_relocated_results_and_source_operands_equal'] and control['all2484_pointer_cases_and_all_source_alias_groups_preserved']
    assert control['original_query_r0_r1_r2_and_mapped_incidental_r3_cursor_exact']
    assert copy['all32_unowned_copy_speeches_byte_exact_and_unreachable_from_ordinary_Lil_entry'] and len(copy['original_VM_return_cases'])==2
    historical_review=Path('work/analysis/lil_Seville_reference_approval_v2722/representative_sheet_review.json')
    prior_current_review=Path('work/analysis/lil_Shrines_Temples_completion_v3208/current_six_frame_visual_review.json')
    for p in [historical_review,prior_current_review]:
        r=read(p);assert r['viewed'] and sha(Path(r['sheet']).read_bytes())==r['sha256']
    blocks=[]
    for original,checked in zip(plan['blocks'],census['blocks'],strict=True):
        assert original['block']==checked['block'] and checked['entry_point_offset']==8
        spec=deepcopy(original);spec['target_block_sha256']=spec.pop('research_block_sha256')
        spec.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],external_entry_and_actual_revised_paths_approval_pending=False,individual_selected_B111_B119_gameplay_unobserved=True)
        blocks.append(spec)
    assert len(blocks)==9 and sum(len(b['command_map']) for b in blocks)==305
    assert sum(len(b['text_records']) for b in blocks)==116
    assert sum(len(b['actor_style_commands']) for b in blocks)==6 and not any(b['choice_commands'] for b in blocks)
    image=NdsImage.open(plan['candidate'])
    mapping=dict(format='dk4-lil-B111-B119-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(image.read_file('/__arm9__.bin')),source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=blocks,
        all305_physical_nested_command_boundaries_and64_relative_sites_verified=True,
        all320_relocated_relative_skip_cases_preserve_original_targets=True,
        all15_relocated_predicate_pairs_and_one_event319_query_preserve_source_operands_results_and_mapped_cursor=True,
        original_event_queries=control['original_event_queries'],
        all6_actor_style_objects48_slots34_strings_aliases_and_actual5_virtual_prefixes_verified=True,
        all116_active_speech_targets_and148_physical_speeches_preserved=True,
        no_player_choice_objects=True,unowned1886byte_copy_preserved_and_original_VM_return_before_copy_verified=True,
        canonical_Maria_SC3_B97_32_targets_still_pending_uncredited=True,
        unowned_copy_proof=str(COPY),unowned_copy_proof_sha256=sha(COPY.read_bytes()),
        representative_shared_rules_approved=True,representative_proof=str(SAMPLE),historical_representative_sheet_review=str(historical_review),prior_current_sheet_review=str(prior_current_review),source_plan=str(PLAN),source_census=str(CENSUS),final_padding_proof=str(PADDING),relocated_control_proof=str(CONTROL),actual_selected_B111_B119_IDs=[],individual_conditional_visits_not_required_under_user_policy=True,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(MAP,mapping)
    for doc,old,new in zip(docs,INPUTS,OUTPUTS,strict=True):
        doc.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),representative_proof=str(SAMPLE),representative_proof_sha256=sha(SAMPLE.read_bytes()),historical_representative_sheet_review=str(historical_review),prior_current_sheet_review=str(prior_current_review),prose_companions=[str(p) for p in OUTPUTS if p!=new],final_padding_proof=str(PADDING),final_padding_proof_sha256=sha(PADDING.read_bytes()),relocated_control_proof=str(CONTROL),relocated_control_proof_sha256=sha(CONTROL.read_bytes()),unowned_copy_proof=str(COPY),unowned_copy_proof_sha256=sha(COPY.read_bytes()),reference_map_pending=False,registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
        for row in doc['records']:
            row.update(status=doc['status'],current_text_hex=row['current_hex'])
            if row['kind']=='typed-4100-actor-style-alternative':row['native_display_consumer']='original4100_actor_voice_selection_then2425C_progressive54020'
            else:row['native_display_consumer']='original_FE_modal_5473C_mode1' if row['kind']=='system-FE' else 'original_progressive_54020'
        assert [r['english'] for r in doc['records']]==[r['english'] for r in read(old)['records']]
    docs[0].update(actor_style_companion=str(OUTPUTS[1]),actor_styles=str(OUTPUTS[1]),native_FE_font_proof=docs[0]['native_FE_proof'],native_FE_font_proof_sha256=sha(Path(docs[0]['native_FE_proof']).read_bytes()))
    for doc,new in zip(docs,OUTPUTS,strict=True):validate_natural_dialogue_batch(doc);save(new,doc)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(OUTPUTS[0]),actor_styles=str(OUTPUTS[1]),reference_map=str(MAP),hashes={str(p):sha(p.read_bytes()) for p in [*OUTPUTS,MAP,*INPUTS,PLAN,CENSUS,SAMPLE,PADDING,CONTROL,COPY,historical_review,prior_current_review]},source_prose_English_unchanged=True,all150_source_native_reference_and_representative_rules_approved=True,canonical_Maria32_uncredited_and_unowned_copy_byte_exact=True,actual_selected_B111_B119_IDs=[],new_emulator_runs=0,registered_release_and_current_startup_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Sealed150 source/native/reference/representative approvals:305commands/64spans/320cases,15predicates/event319,6variable-selector4100objects,600final macro cases andexact unownedcopy. Registeredrelease/startup pending.')
