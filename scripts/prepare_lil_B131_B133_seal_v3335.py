"""Create a source00-aware successor of the prior reference seal."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/seal_lil_B122_B127_references_v3295.py');new=Path('scripts/seal_lil_B131_B133_references_v3335b.py');assert not new.exists()
    t=old.read_text(encoding='utf-8')
    changes={
        'lil_B122_B127_reference_approval_v3295':'lil_B131_B133_reference_approval_v3335b',
        'lil_B122_B127_editorial_relocation_map_v1':'lil_B131_B133_editorial_relocation_map_v1',
        'lil_B122_B127_editorial_manuscript_v5':'lil_B131_B133_editorial_manuscript_v4',
        'lil_B122_B127_editorial_manuscript_v6':'lil_B131_B133_editorial_manuscript_v5',
        'lil_B122_B127_choice_manuscript_v4':'lil_B131_B133_choice_manuscript_v5',
        'lil_B122_B127_choice_manuscript_v5':'lil_B131_B133_choice_manuscript_v6',
        'lil_B122_B127_relocation_v3288b':'lil_B131_B133_relocation_v3329b',
        'lil_B122_B127_reference_census_v3291/all312_commands64_relative_sites_and_shipped_entry_census':'lil_B131_B133_reference_census_v3332/all112_commands24_relative_sites_and_shipped_entry_census',
        'lil_B122_B127_sampling_v3294':'lil_B131_B133_sampling_v3334',
        'lil_B122_B127_research_v3289b':'lil_B131_B133_research_v3330b',
        'lil_B122_B127_relocated_controls_v3292/all155_relocated_dispatches_and14_predicate_pairs':'lil_B131_B133_relocated_controls_v3333b/all61_relocated_dispatches_source00_and5_predicate_pairs',
        'all312_clean_current_target_commands_and64_relative_sites_reexecuted':'all112_clean_current_target_commands_and24_relative_sites_reexecuted',
        'actual_selected_B122_B127_IDs':'actual_selected_B131_B133_IDs',
        'all155_final_targets_complete_native_planes_equal_reviewed_planes':'all61_final_targets_complete_native_planes_equal_reviewed_planes',
        "padding['current_final_padded_macro_alignment_cases']==620":"padding['current_final_padded_macro_alignment_cases']==244",
        'all2_final2100_objects_four_labels_and6_selection_cancel_cases_bound':'all1_final2100_object_two_labels_and3_selection_cancel_cases_bound',
        "padding['both_original_pause_resume_words_and20_decoder_cases_bound']":"padding['no_source2000_pause_commands'] and padding['all18_final_source00_speech_prefixes_and_nonempty_bodies_preserved']",
        'all14_predicate_current_relocated_results_and_source_operands_equal':'all5_predicate_current_relocated_results_and_source_operands_equal',
        'all10_FE_preserve_original_null_actor_before_dynamic_fallback':'all1_FE_preserves_original_null_actor_before_dynamic_fallback',
        'work/analysis/lil_B111_B119_completion_v3255/current_six_frame_visual_review.json':'work/analysis/lil_B122_B127_startup_v3303/current_six_frame_visual_review.json',
        'individual_selected_B122_B127_gameplay_unobserved':'individual_selected_B131_B133_gameplay_unobserved',
        'len(blocks)==6':'len(blocks)==2',
        '==312':'==112','==155':'==61',
        "for b in blocks)==2":"for b in blocks)==1",
        "sum(len(b['original2000_pause_and_resume_maps']) for b in blocks)==2":"sum(len(b['original2000_pause_and_resume_maps']) for b in blocks)==0",
        'dk4-lil-B122-B127-source-relocation-map-v1':'dk4-lil-B131-B133-source-relocation-map-v1',
        'all312_physical_nested_command_boundaries_and64_relative_sites_verified':'all112_physical_nested_command_boundaries_and24_relative_sites_verified',
        'all320_relocated_relative_skip_cases_preserve_original_targets':'all120_relocated_relative_skip_cases_preserve_original_targets',
        'all14_relocated_predicate_pairs_preserve_source_operands_results_and_unowned_RAM':'all5_relocated_predicate_pairs_preserve_source_operands_results_and_unowned_RAM',
        'all155_active_speech_targets_preserved':'all61_active_speech_targets_preserved',
        'two2100_objects_four_labels_and_source_indices_0_1_cancel_verified':'one2100_object_two_labels_and_source_indices_0_1_cancel_verified',
        'two_original2000_pause_words_and_mapped_resume_boundaries_verified=True,trade_choice0_tutorial_choice1_already_know_branch_and_return0_both_VM_modes_verified=True,':'no_source2000_pause_commands=True,all18_source00_prefixes_and_nonempty_bodies_verified=True,',
        'all159_source_native_reference_and_representative_rules_approved':'all63_source_native_reference_and_representative_rules_approved',
        'both2000_pauses_and_two2100_menus_and_conditional_return0_preserved=True':'one2100_menu_and18_source00_controls_preserved=True',
    }
    # Longest-first avoids overlapping manuscript-name substitutions.
    for a,b in sorted(changes.items(),key=lambda kv:-len(kv[0])):
        assert a in t,a;t=t.replace(a,b)
    t=t.replace("RETURN=Path('work/analysis/lil_trade_branch_return_v3293/original_choice_control_paths_and_both_VM_return_modes.json')", "TYPED=Path('work/analysis/lil_B131_B133_typed_speech_v3323/all366_whole4000_commands_and108_source00_cases.json')")
    t=t.replace('plan,census,sample,padding,control,branch=map(read,[PLAN,CENSUS,SAMPLE,PADDING,CONTROL,RETURN])','plan,census,sample,padding,control,typed=map(read,[PLAN,CENSUS,SAMPLE,PADDING,CONTROL,TYPED])')
    t=t.replace("    assert branch['source_current_target_branch_endings_preserved'] and len(branch['original_VM_return_cases'])==12", "    assert len(typed['cases'])==366 and typed['all108_source00_cases_forward_nonempty_body_after_selector_to_original_display']")
    t=t.replace('PADDING,CONTROL,RETURN','PADDING,CONTROL,TYPED').replace(",Path(docs[0]['original2000_wait_proof'])",'')
    t=t.replace('conditional_return_proof=str(RETURN),','whole_typed_speech_proof=str(TYPED),')
    t=t.replace('conditional_return_proof_sha256=sha(RETURN.read_bytes()),','whole_typed_speech_proof_sha256=sha(TYPED.read_bytes()),')
    t=t[:t.rindex('    print(')]+"    print('Sealed63 source/native/reference/representative approvals;registered release andstartup pending.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    root=Path('work/analysis/lil_B131_B133_seal_tools_v3335');root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
