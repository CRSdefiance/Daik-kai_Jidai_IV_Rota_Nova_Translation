"""Seal 235 source/current/target references and representative rule approval."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Shrines_Temples_reference_approval_v3199')
MAP=Path('translations/lil_shrines_temples_editorial_relocation_map_v1.json')
INPUTS=[Path('translations/lil_shrines_temples_editorial_manuscript_v7.json'),
        Path('translations/lil_shrines_temples_actor_style_manuscript_v5.json'),
        Path('translations/lil_shrines_temples_choice_manuscript_v4.json')]
OUTPUTS=[Path('translations/lil_shrines_temples_editorial_manuscript_v8.json'),
         Path('translations/lil_shrines_temples_actor_style_manuscript_v6.json'),
         Path('translations/lil_shrines_temples_choice_manuscript_v5.json')]
PLAN=Path('work/analysis/lil_Shrines_Temples_relocation_v3193/nested_source_relocation_research.json')
CENSUS=Path('work/analysis/lil_Shrines_Temples_reference_census_v3196/all421_commands114_relative_sites_and_shipped_entry_census.json')
SAMPLE=Path('work/analysis/lil_Shrines_Temples_sampling_v3198/relocated_predicates_and_representative_rule_reconciliation.json')
PADDING=Path('work/analysis/lil_Shrines_Temples_research_v3194/research_image_receipt.json')
CONTROL=Path('work/analysis/lil_Shrines_Temples_relocated_controls_v3197/all220_dispatch16_style_commands3312_getters21_predicate_pairs.json')

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,MAP,*OUTPUTS])
    plan,census,sample,padding,control=map(read,[PLAN,CENSUS,SAMPLE,PADDING,CONTROL])
    docs=[deepcopy(read(p)) for p in INPUTS]
    assert census['all421_clean_current_target_commands_and114_relative_sites_reexecuted']
    assert census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert sample['no_open_translation_specific_display_or_control_finding']
    assert sample['actual_selected_Shrines_Temples_IDs']==[] and sample['actual_three_option_menu_gameplay_coverage']==[]
    assert padding['all220_final_targets_complete_native_planes_equal_reviewed_planes']
    assert padding['current_final_padded_macro_alignment_cases']==880
    assert control['all21_current_relocated_predicate_results_and_source_operands_equal']
    assert control['all3312_pointer_cases_and_all_source_alias_groups_preserved']
    historical_review=Path('work/analysis/lil_Seville_reference_approval_v2722/representative_sheet_review.json')
    prior_current_review=Path('work/analysis/lil_Crew_Items_completion_v3148/current_six_frame_visual_review.json')
    for p in [historical_review,prior_current_review]:
        review=read(p)
        assert review['viewed'] and sha(Path(review['sheet']).read_bytes())==review['sha256']
    blocks=[]
    for original,checked in zip(plan['blocks'],census['blocks'],strict=True):
        assert original['block']==checked['block'] and checked['entry_point_offset']==8
        spec=deepcopy(original);spec['target_block_sha256']=spec.pop('research_block_sha256')
        spec.update(external_references_complete=True,entry_point_offset=8,
            mapped_native_commands=checked['mapped_commands'],external_entry_and_actual_revised_paths_approval_pending=False,
            individual_selected_Shrines_Temples_gameplay_unobserved=True)
        blocks.append(spec)
    image=NdsImage.open(plan['candidate'])
    mapping=dict(format='dk4-lil-shrines-temples-source-relocation-map-v1',
        required_runtime_ARM9_sha256=sha(image.read_file('/__arm9__.bin')),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=blocks,
        all421_nested_command_boundaries_and114_relative_sites_verified=True,
        all570_relocated_relative_skip_cases_preserve_original_targets=True,
        all21_relocated_predicate_pairs_preserve_source_operands_and_results=True,original_event_queries=[],
        all8_actor_style_objects64_slots56_strings_aliases_and_virtual_D0_storage_verified=True,
        all5_three_option_menu_objects15_labels_preserve_source_indices012_and_cancel=True,
        representative_shared_rules_approved=True,representative_proof=str(SAMPLE),
        historical_representative_sheet_review=str(historical_review),prior_current_sheet_review=str(prior_current_review),
        source_plan=str(PLAN),source_census=str(CENSUS),final_padding_proof=str(PADDING),
        relocated_control_proof=str(CONTROL),actual_selected_Shrines_Temples_IDs=[],
        actual_three_option_menu_gameplay_coverage=[],individual_conditional_visits_not_required_under_user_policy=True,
        full_goal_complete=False)
    ROOT.mkdir(parents=True);save(MAP,mapping)
    for doc,old,new in zip(docs,INPUTS,OUTPUTS,strict=True):
        doc.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()),
            reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
            representative_proof=str(SAMPLE),representative_proof_sha256=sha(SAMPLE.read_bytes()),
            historical_representative_sheet_review=str(historical_review),prior_current_sheet_review=str(prior_current_review),
            prose_companions=[str(p) for p in OUTPUTS if p!=new],
            final_padding_proof=str(PADDING),final_padding_proof_sha256=sha(PADDING.read_bytes()),
            relocated_control_proof=str(CONTROL),relocated_control_proof_sha256=sha(CONTROL.read_bytes()),
            reference_map_pending=False,registered_integration_pending=True,
            status='source-prose-native-references-representative-approved;registered-release-startup-pending')
        for row in doc['records']:
            row.update(status=doc['status'],current_text_hex=row['current_hex'])
            if row['kind']=='typed-4100-actor-style-alternative':
                row['native_display_consumer']='original4100_actor_voice_selection_then2425C_progressive54020'
            elif row['kind']!='typed-choice-label':
                row['native_display_consumer']='original_FE_modal_5473C_mode1' if row['kind']=='system-FE' else 'original_progressive_54020'
        assert [r['english'] for r in doc['records']]==[r['english'] for r in read(old)['records']]
    docs[0].update(actor_style_companion=str(OUTPUTS[1]),actor_styles=str(OUTPUTS[1]),
        typed_choice_companion=str(OUTPUTS[2]),choice_companion=str(OUTPUTS[2]),choices=str(OUTPUTS[2]),
        native_FE_font_proof=docs[0]['native_FE_proof'],
        native_FE_font_proof_sha256=sha(Path(docs[0]['native_FE_proof']).read_bytes()))
    for doc,new in zip(docs,OUTPUTS,strict=True):
        validate_natural_dialogue_batch(doc);save(new,doc)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(OUTPUTS[0]),actor_styles=str(OUTPUTS[1]),
        choices=str(OUTPUTS[2]),reference_map=str(MAP),
        hashes={str(p):sha(p.read_bytes()) for p in [*OUTPUTS,MAP,*INPUTS,PLAN,CENSUS,SAMPLE,PADDING,CONTROL,
            historical_review,prior_current_review]},
        source_prose_English_unchanged=True,all235_source_native_reference_and_representative_rules_approved=True,
        actual_selected_Shrines_Temples_IDs=[],actual_three_option_menu_gameplay_coverage=[],new_emulator_runs=0,
        registered_release_and_current_startup_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Sealed235 source/native/reference/representative approvals:421commands/114spans/570cases,21predicate pairs,8aliasedactor-styleobjects/5three-optionmenus,880finaltarget macro cases. Registeredrelease/startup pending.')
