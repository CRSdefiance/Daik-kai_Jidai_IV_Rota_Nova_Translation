"""Prepare actual-changing production corruptions for the staged item,callbacks,prerequisite and display scope."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B229_challenge_tools_v7416')
if __name__=='__main__':
    assert not ROOT.exists()
    extra="""    add('item53-wrong-storage-class',item,lambda v:v['source_named_item'].update(current_storage_kind='static-current-ARM9'))
    add('item53-wrong-relative-offset',item,lambda v:v['source_named_item'].update(current_storage_offset=134))
    add('item53-current-pointer-retargeted',item,lambda v:v['source_named_item'].update(current_pointer=v['source_named_item']['source_pointer']))
    entry=Path(d['source_entry_proof']);callback=Path(d['callback_completed_review']);namefont=Path(d['native_name_proof'])
    add('source229-prerequisite-lost',entry,lambda v:v['selected_B229_source_events'][0].update(must_be_completed=[]))
    add('source229-wrong-prerequisite',entry,lambda v:v['selected_B229_source_events'][0].update(must_be_completed=[227]))
    add('source229-wrong-action',entry,lambda v:v['selected_B229_source_events'][0].update(action_index=229))
    root('entry-source-identity-lost',entry,'original_source_EV2_and_action_table_exact',False)
    root('entry-hash-changed',doc,'source_entry_proof_sha256','0'*64)
    root('callback-hash-changed',doc,'callback_completed_review_sha256','0'*64)
    add('B228-pitch-echo-corrupted',callback,lambda v:next(r for r in v['records'] if r['source_record_index']==28).update(english='Different pitch!'))
    add('B228-personal-reassurance-corrupted',callback,lambda v:next(r for r in v['records'] if r['source_record_index']==46).update(english='Different reassurance!'))
    root('name-font-reuse-count-lost',namefont,'exact_reused_native_name_font_alignment_cases',0)
    root('name-font-reuse-falsely-fresh',namefont,'fresh_native_name_font_alignment_cases',32)
    root('name-font-plane-count-lost',namefont,'complete_name_component_plane_count',7)
    root('name-font-catalogue-approval-invented',namefont,'Samwell_mixed_Japanese_catalogue_plane_is_technical_evidence_not_wording_approval',False)
    add('actual-command-comparison-erased',a,lambda v:v['command_comparison_differences'].pop())
    add('actual-duration-erased',a,lambda v:v['command_duration_changes'].pop())
    add('later-RGB-difference-erased',paths['later_scope_proof'],lambda v:v['later_sampled_RGB_differences'].pop())
"""
    changes={'B228':'B229','atomic_v7369':'atomic_v7416','atomic_v7368':'atomic_v7415',"('actual_objects',12),('actual_pages',12),('actual_complete_body_holds',50),('actual_complete_name_holds',50)":"('actual_objects',16),('actual_pages',16),('actual_complete_body_holds',66),('actual_complete_name_holds',66)",'target_offset=742':'target_offset=918','all13_single_original_four_row_pages':'all17_single_original_four_row_pages','all13_complete_prose_paragraphs':'all17_complete_prose_paragraphs',"'negative_count',61":"'negative_count',75",'all13_single_original_native_pages_verified':'all17_single_original_native_pages_verified','event228':'event229','all13_complete_preambles_voices_andzero_macro_bodies_bound':'all17_complete_preambles_voices_andzero_macro_bodies_bound','original_normal_end740_four_bytes_andtarget_no_tail_preserved':'original_normal_end916_four_bytes_andtarget_no_tail_preserved','all15_commands_no_predicate_relative_typed_style_orpicture_assumptions':'all19_commands_no_predicate_relative_typed_style_orpicture_assumptions','positive_records=13':'positive_records=17','all13_actual13_pages51_body51_headers_bound':'all17_actual17_pages67_body67_headers_bound','current_Armadillo_Hide_asset_andharder_than_iron_source_meaning_bound':'current_Giant_Tortoise_Shield_asset_andreported_iron_hard_shell_source_meaning_bound','actual-lost-command-difference':'actual-invented-command-difference','actual-lost-duration':'actual-invented-duration','later-RGB-difference-erased':'later-RGB-difference-invented',"    assert len(tests)==len({t[0] for t in tests})":extra+"    assert len(tests)==len({t[0] for t in tests})"}
    r=derive('scripts/challenge_lil_B228_atomic_v7369.py','scripts/challenge_lil_B229_atomic_v7416.py',changes);ROOT.mkdir(parents=True);save(ROOT/'source_locked_B229_semantic_challenges.json',dict(tool=r,all_cases_must_change_data_andreject_before_archive_write=True,file_digests_bypassed_andapproved_records_mirrored_to_reach_deep_semantics=True,staged_item53_offsets_andsource_prerequisite_andcallback_have_distinct_cases=True,nonempty_measured_differences_challenged_by_both_invention_anderasure=True,new_credit=0,full_goal_complete=False))
