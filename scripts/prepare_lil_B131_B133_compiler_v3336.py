"""Derive the narrow source00-aware registered compiler; retain earlier tools."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('dk4tool/patch/lil_B122_B127_editorial_v2.py');new=Path('dk4tool/patch/lil_B131_B133_editorial_v1.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={
      'Source/runtime-locked155 speeches,two two-option menus andtwo source pauses.':'Source/runtime-locked61 speeches including18 actor00 andone two-option menu.',
      'lil_B122_B127_layout_v2':'lil_B131_B133_layout_v2','lil_B122_B127_profile_v2':'lil_B131_B133_profile',
      'lil_B122_B127_editorial_release_v1':'lil_B131_B133_editorial_release_v1',
      'list(range(122,128))':'[131,133]','Lil B122-B127 ':'Lil B131/B133 ',
      'dk4-lil-B122-B127':'dk4-lil-B131-B133',
      'all312_physical_nested_command_boundaries_and64_relative_sites_verified':'all112_physical_nested_command_boundaries_and24_relative_sites_verified',
      'all320_relocated_relative_skip_cases_preserve_original_targets':'all120_relocated_relative_skip_cases_preserve_original_targets',
      'all14_relocated_predicate_pairs_preserve_source_operands_results_and_unowned_RAM':'all5_relocated_predicate_pairs_preserve_source_operands_results_and_unowned_RAM',
      'all155_active_speech_targets_preserved':'all61_active_speech_targets_preserved',
      'two2100_objects_four_labels_and_source_indices_0_1_cancel_verified':'one2100_object_two_labels_and_source_indices_0_1_cancel_verified',
      'two_original2000_pause_words_and_mapped_resume_boundaries_verified':'no_source2000_pause_commands',
      'trade_choice0_tutorial_choice1_already_know_branch_and_return0_both_VM_modes_verified':'all18_source00_prefixes_and_nonempty_bodies_verified',
      'individual_selected_B122_B127_visits_not_required_for_reusable_rules':'individual_selected_B131_B133_visits_not_required_for_reusable_rules',
      'two2100_menus_source_order_indices_geometry_complete_planes_and_selection_cancel_bound':'one2100_menu_source_order_indices_geometry_complete_planes_and_selection_cancel_bound',
      "        and representative.get('both_mapped_pause_resumption_boundaries_exact') is True\n        and representative.get('trade_tutorial_and_already_know_branch_native_paths_and_both_return_modes_bound') is True":"        and representative.get('source00_full_typed_body_and_static_Rafael_Lil_context_macros_bound') is True",
      'actual_selected_B122_B127_IDs':'actual_selected_B131_B133_IDs',
      "len(FE['cases'])==10":"len(FE['cases'])==1",'all10_one_native_page_consumes_complete_target':'all1_one_native_page_consumes_complete_target',
      'all10_complete_native_independent_planes_all_glyphs_and_canaries_equal':'all1_complete_native_independent_planes_all_glyphs_and_canaries_equal',
      "len(FE['source_leading_vertical_staging_cases'])==7 and len(FE['source_FI_null_actor_cases'])==3":"len(FE['source_leading_vertical_staging_cases'])==0 and len(FE['source_FI_null_actor_cases'])==0",
      'all14_predicate_current_relocated_results_and_source_operands_equal':'all5_predicate_current_relocated_results_and_source_operands_equal',
      'all10_FE_preserve_original_null_actor_before_dynamic_fallback':'all1_FE_preserves_original_null_actor_before_dynamic_fallback',
      'all155_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text':'all61_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text',
      "len(controls['relocated_predicate_pairs'])==14":"len(controls['relocated_predicate_pairs'])==5",
      "menu_native['complete_current_and_reviewed_style_label_planes']==16":"menu_native['complete_current_and_reviewed_style_label_planes']==8",
      "menu_native['native_selection_cancel_cases']==12":"menu_native['native_selection_cancel_cases']==6",
      "len(menu_targets)==2":"len(menu_targets)==1",'two approved two-option objects required':'one approved two-option object required',
      '==155':'==61','155speech':'61speech','155complete':'61complete',
      "})==4,'four choice labels required'":"})==2,'two choice labels required'",
      "'six exact blocks required'":"'two exact blocks required'",'==312':'==112',
      '{2,6,9,20,26,92,95,151,254}':'{0,2,5,9,20,254}',
      '==159':'==63','only_SC2_selected_six_blocks_changed':'only_SC2_selected_two_blocks_changed',
      'all330_other_SC2_blocks_unchanged':'all334_other_SC2_blocks_unchanged',
      'all155_speeches_four_choice_labels64_relative_operands_verified':'all61_speeches_two_choice_labels24_relative_operands_verified',
      'both2000_pause_resume_boundaries_and_trade_return0_verified=True':'all18_source00_prefixes_nonempty_bodies_and_no_source2000_verified=True',
      'both2100_menu_counts_indices01_cancel_and_native_planes_verified':'one2100_menu_count_indices01_cancel_and_native_planes_verified',
    }
    for a,b in sorted(changes.items(),key=lambda kv:-len(kv[0])):assert a in t,a;t=t.replace(a,b)
    a=t.index("    branch=load(doc['conditional_return_proof'])");z=t.index("    menu_native=",a)
    t=t[:a]+"""    typed=load(doc['whole_typed_speech_proof']);native=load(doc['native_font_proof'])
    _require(sha(Path(doc['whole_typed_speech_proof']).read_bytes())==doc['whole_typed_speech_proof_sha256']
        and len(typed['cases'])==366 and typed['all108_source00_cases_forward_nonempty_body_after_selector_to_original_display'],
        'whole source00 speech-body proof required')
    _require(len(native['source_consumer_negative_controls'])==22 and all(c['rejected'] for c in native['source_consumer_negative_controls'])
        and any(c['case']=='shared-encoder-still-rejects-source00' for c in native['source_consumer_negative_controls']),
        'strict shared encoder and source00 negative controls required')
    _require(sum(r['source_selector']==0 for r in doc['records'])==18
        and controls['all18_final_source00_speeches_are_static_Rafael0_without_role_assignment'],
        'eighteen source00 static Rafael records required')
"""+t[z:]
    a=t.index("        _require(len(spec['original2000_pause_and_resume_maps'])");z=t.index("        _require(sha(target)",a)
    t=t[:a]+"        _require(spec['original2000_pause_and_resume_maps']==[],'unexpected source pause')\n"+t[z:]
    anchor='    return encoded.encoded\n'
    assert anchor in t
    t=t.replace(anchor,"""    _require(encoded.encoded and encoded.encoded[0]==raw[0] and b'\\0' not in encoded.encoded[1:]
        and encoded.encoded.count(b'\\0')==int(raw[0]==0), 'source-owned leading selector/body NUL contract differs:'+row['id'])
    return encoded.encoded
""")
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    root=Path('work/analysis/lil_B131_B133_compiler_tools_v3336');root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),shared_encoder_unchanged=True,only_proven_source00_prefix_permitted=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
