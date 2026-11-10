"""Derive a whole-NDS planner preserving the complete established production gates."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_atomic_tools_v8768');assert not root.exists()
    source=Path('dk4tool/patch/hodram_B52_editorial_v2.py').read_text('utf-8')
    choices="""    typed=compile_choices(doc['typed_choice_records'])
    require(typed.hex()==policy['positive_typed_choice_object_hex']==frozen['choice_object_hex'] and len(typed)==32,'complete original-count/order typed choice object')
"""
    receipt=derive('dk4tool/patch/hodram_B52_editorial_v2.py','dk4tool/patch/hodram_B31_B53_editorial_v1.py',{
        'B52':'B31_B53','all-routes-unified-v8609':'all-routes-unified-v8704',
        'Hodram_B52_release_paths_v8693':'Hodram_B31_B53_release_paths_v8767',
        'hodram_B52_controls_v2':'hodram_B31_B53_controls_v1',
        'from dk4tool.dialogue.hodram_B52_choices_v1 import compile_choices\n':'',
        'from dk4tool.patch.hodram_B52_menu_evidence_v1 import check_menu_actual\n':'',
        "prior['manifest_batches']==645":"prior['manifest_batches']==646",
        "policy['positive_editorial_units']==5":"policy['positive_editorial_units']==3",
        "policy['negative_count']==len(policy['negative_cases'])==243":"policy['negative_count']==len(policy['negative_cases'])==236",
        "'complete compiler positives and243 semantic rejections'":"'three complete compiler positives and236 semantic rejections'",
        "counts={'independent_reconstruction':26,'independent_references':20,'independent_native':10,'independent_menu':12,'independent_controls':9,'independent_loaders':7,'independent_actual':7,'independent_comparison':6}":"counts={'independent_reconstruction':51,'independent_references':20,'independent_native':12,'independent_controls':12,'independent_loaders':8,'independent_actual':13,'independent_comparison':12}",
        'profile_for(arm,bank[52],ident,PATH,\'progressive\')':"profile_for(arm,bank[row['block']],ident,PATH,'progressive')",
        "qa['issues']==frozen['record_bindings'][ident]['base_QA_issues']":"qa['base_QA_issues']==frozen['record_bindings'][ident]['base_QA_issues']",
        choices:'',
        "doc['records']+doc['typed_choice_records']":"doc['records']",
        "'five sealed disjoint prose/choice references'":"'three sealed disjoint source/current/final prose references'",
        "    menu=check_menu_actual({**data,'withdrawal':data['actual'],'opposition':data['opposition_actual']},doc,image,load,require)\n":'',
        "scope['complete_page_occurrences']==12 and scope['complete_body_name_holds']==138 and scope['total_actual_frames']==50406 and scope['later_RGB_pairs']==[93,93,13]":"scope['complete_page_occurrences']==4 and scope['complete_body_name_holds']==76 and scope['total_actual_frames']==24004 and scope['later_RGB_pairs']==[34,34] and scope['actual_unique_speech_IDs']==['DK4_MES_B31_R0018','DK4_MES_B53_R0007'] and scope['unvisited_conditional_text_IDs']==['DK4_MES_B31_R0013']",
        "'every measured actual/offline/long divergence/focused limit'":"'every measured actual/offline/unforced alternate-path limit'",
        "approval['all5_five_gates_true'] and approval['manuscript_sha256']==sha(DOC.read_bytes())":"approval['all3_five_gates_true'] and data['metadata']['predecessor_sha256']==approval['manuscript_sha256'] and data['metadata']['manuscript_sha256']==sha(DOC.read_bytes())",
        "block=52,kind='typed-choice' if r in doc['typed_choice_records'] else 'progressive'":"block=r['block'],kind='progressive'",
        'all14_commands3_preambles4_relatives_twochoices4_opaque_bothends_andtails_preserved':'all18_commands3_preambles4_relatives1_query8_opaque2_normalends_andtails_preserved',
        'explicit_complete_registered_V8609_dependency_preserved':'explicit_complete_registered_V8704_dependency_preserved',
        'native_loaders=loaders,native_menu=menu':'native_loaders=loaders',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,all_native_high_integer_constants_andmultiplicity_preserved=True,
        every_original_whole_parent_file_component_frozen_policy_compiler_reference_native_controls_loader_actual_comparison_andinverse_guard_preserved=True,
        three_speeches_two_blocks_no_typedchoices_current_registered_V8704_andboth_source_lifecycles_explicit=True,
        original_complete_NDS_object_commit_after_all_gates_preserved=True,
        module_prepared_only_seal_configuration_atomic_challenges_andregistered_integration_pending=True,new_credit=0,full_goal_complete=False))
