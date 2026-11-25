"""Preserve complete whole-NDS atomic planning and all registered prefix guards for82 speeches."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_atomic_tools_v8854');assert not root.exists()
    old_scope="scope==seal['observed_scope'] and scope['complete_page_occurrences']==4 and scope['complete_body_name_holds']==76 and scope['total_actual_frames']==24004 and scope['later_RGB_pairs']==[34,34] and scope['actual_unique_speech_IDs']==['DK4_MES_B31_R0018','DK4_MES_B53_R0007'] and scope['unvisited_conditional_text_IDs']==['DK4_MES_B31_R0013']"
    new_scope="scope==seal['observed_scope'] and scope['complete_page_occurrences']==150 and scope['complete_body_name_holds']==676 and scope['total_actual_frames']==130014 and scope['later_RGB_pairs']==[22,43,56,77,65,61,11] and len(scope['actual_unique_speech_IDs'])==63 and len(scope['offline_only_text_IDs'])==19 and len(scope['unvisited_conditional_text_IDs'])==18 and not set(scope['actual_unique_speech_IDs'])&set(scope['offline_only_text_IDs']) and set(scope['actual_unique_speech_IDs'])|set(scope['offline_only_text_IDs'])=={r['id'] for r in doc['records']}"
    module=derive('dk4tool/patch/hodram_B31_B53_editorial_v2.py','dk4tool/patch/hodram_B54_B60_editorial_v1.py',{
        'B31_B53':'B54_B60','hodram_B31_B53':'hodram_B54_B60',
        'from scripts.Hodram_B31_B53_release_paths_v8767':'from scripts.Hodram_B54_B60_release_paths_v8853',
        'from dk4tool.patch.hodram_B31_B53_comparison_v1 import check_comparisons':'from dk4tool.patch.hodram_B54_B60_FE_actual_v2 import check_FE_live\nfrom dk4tool.patch.hodram_B54_B60_comparison_v1 import check_comparisons',
        'all-routes-unified-v8704':'all-routes-unified-v8778',"prior['manifest_batches']==646":"prior['manifest_batches']==647",
        'entire verified registered V8704 stack':'entire verified registered V8778 stack',
        "policy['positive_editorial_units']==3 and len(policy['positive_speech_compilers'])==3 and policy['negative_count']==len(policy['negative_cases'])==236":"policy['positive_editorial_units']==82 and len(policy['positive_speech_compilers'])==82 and policy['negative_count']==len(policy['negative_cases'])==625",
        'three complete compiler positives and236 semantic rejections':'82 complete compiler positives and625 semantic rejections',
        "{'independent_reconstruction':51,'independent_references':20,'independent_native':12,'independent_controls':12,'independent_loaders':8,'independent_actual':13,'independent_comparison':12}":"{'independent_reconstruction':161,'independent_references':25,'independent_native':12,'independent_controls':12,'independent_loaders':11,'independent_actual':16,'independent_comparison':16,'independent_FE_actual':8}",
        "ident,PATH,'progressive')":"ident,PATH,'FE-paper' if row['source_selector']==254 else 'progressive')",
        "qa['native_page_count']==1":"qa['native_page_count']==row['expected_native_pages']",
        'three sealed disjoint source/current/final prose references':'82 sealed disjoint source/current/final prose references',
        '    comparison=check_comparisons(data,image,load,require)':'    FE_actual=check_FE_live(data,image,load,require)\n    comparison=check_comparisons(data,image,load,require)',
        old_scope:new_scope,
        "approval['all3_five_gates_true']":"approval['all82_five_gates_true']",
        "['directly_viewed_dialogue_andtransition_sheets']":"['viewed_sheets']",
        "kind='progressive'":"kind=r['kind']",
        'all18_commands3_preambles4_relatives1_query8_opaque2_normalends_andtails_preserved':'all152_commands82_preambles24_relatives6_queries33_nonprose7_normalends_andtails_preserved',
        'explicit_complete_registered_V8704_dependency_preserved':'explicit_complete_registered_V8778_dependency_preserved',
        "actual_summary=actual['summary'],comparison=comparison":"actual_summary=actual['summary'],FE_actual_summary=FE_actual,comparison=comparison",
    })
    # The registered builder resolves this lowercase wrapper; the original
    # predecessor wrappers/modules/configurations remain byte-for-byte intact.
    wrapper=derive('dk4tool/patch/hodram_b31_b53_extension_v2.py','dk4tool/patch/hodram_b54_b60_extension_v1.py',{
        'B31/B53':'B54-B60','hodram_B31_B53_editorial_v2':'hodram_B54_B60_editorial_v1',
    })
    root.mkdir(parents=True);save(root/'source_locked_atomic_planner.json',dict(module=module,wrapper=wrapper,whole_parent_baseline_clean_prefix_files_components_source_refs_all82compilers_allindependentreaders_exactreference_wholeinverse_andonecommit_guards_preserved=True,FE_multipage_all14runs_andall_measured_scope_limits_required=True,no_seal_config_registry_orROM_written_no_credit=True,new_credit=0,full_goal_complete=False))
