"""Prepare actual-changing B227 corruptions,including allthree controls andexact QA scope."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B227_challenge_tools_v7322')
if __name__=='__main__':
    assert not ROOT.exists()
    extra="""    r15=next(i for i,r in enumerate(d['records']) if r['source_record_index']==15)
    row('lost-only-reviewed-warning','exact_reviewed_base_warnings',[],r15)
    row('lost-only-warning-reason','qa_waiver_reason','',r15)
    row('broadened-only-warning','qa_waivers',['weak-line-ending','encoding'],r15)
    row('warning-on-another-record','exact_reviewed_base_warnings',[dict(severity='warning',code='weak-line-ending',message='unreviewed boundary')],0)
    add('changed-reviewed-warning-message',doc,lambda v:v['records'][r15]['exact_reviewed_base_warnings'][0].update(message='different line orword'))
    row('wrong-source-voice','source_voice_class',7,0)
    ap=read(a);runplan=next(Path(p) for p in ap['evidence'] if Path(p).name=='run_plan.json');fixture=Path(ap['fixture'])
    root('B227-explicit-entry-scope-lost',runplan,'source_event227_not_naturally_selected',False)
    root('B227-displayed-block-misidentified',runplan,'displayed_original_source_block',226)
    add('B227-fixture-block-misidentified',fixture,lambda v:v['fixtures'][0].update(source_block=226))
    root('B227-fixture-scope-lost',fixture,'initialized_Amsterdam_B22_not_natural_event227_location_or_earned_progress',False)
    for i in range(3):
        add('A000-map-target-'+str(i),mapfile,lambda v,i=i:v['blocks'][0]['original_A000_map'][i].update(target_offset=680+i*8))
        add('A000-map-operand-'+str(i),mapfile,lambda v,i=i:v['blocks'][0]['original_A000_map'][i].update(source_hex='00a0ffff00000000'))
        add('A000-consumer-location-'+str(i),paths['relocated_control_proof'],lambda v,i=i:v['three_source_andrelocated_A000_cases'][i].update(target_offset=680+i*8))
        add('A000-consumer-command-'+str(i),paths['relocated_control_proof'],lambda v,i=i:v['three_source_andrelocated_A000_cases'][i]['source'].update(source_command_hex='00a0ffff00000000'))
        add('A000-consumer-native-rows-'+str(i),paths['relocated_control_proof'],lambda v,i=i:v['three_source_andrelocated_A000_cases'][i]['relocated']['rows'].clear())
"""
    changes={'B226':'B227','lil_B226_editorial_v1':'lil_B227_editorial_v3','atomic_v7275b':'atomic_v7322','atomic_v7274':'atomic_v7321c',"('actual_objects',19),('actual_pages',19),('actual_complete_body_holds',78),('actual_complete_name_holds',78)":"('actual_objects',8),('actual_pages',8),('actual_complete_body_holds',34),('actual_complete_name_holds',34)",'familiar_ojisan_not_uncle_or_kinship':'quoted_teacher_not_family_naval_rank_orpresent_actor','King Manuel':'Captain Yifa','target_offset=1174':'target_offset=704','all20_single_original_four_row_pages':'all9_single_original_four_row_pages','all20_complete_prose_paragraphs':'all9_complete_prose_paragraphs','only_original_static_selectors2_23':'only_original_static_selectors2_25',"'negative_count',73":"'negative_count',49",'all_base_QA_diagnostics_preserved_zero_warning_waivers':'all_base_QA_diagnostics_preserved_one_exact_R15_phrasal_verb_classification','King Attila':'Master Yifa','all20_single_original_native_pages_verified':'all9_single_original_native_pages_verified','all20_complete_preambles_voices_andzero_macro_bodies_bound':'all9_complete_preambles_voices_andzero_macro_bodies_bound','original_normal_end1172_four_bytes_andtarget_no_tail_preserved':'original_normal_end702_four_bytes_andtarget_tail2_preserved','all22_commands_no_predicate_relative_typed_style_orpicture_assumptions':'all13_commands_no_predicate_relative_typed_style_orpicture_assumptions','positive_records=20':'positive_records=9','all20_actual20_pages79_body79_headers_bound':'all9_actual9_pages35_body35_headers_bound','original_A00025_ends_and_explicit_comparison_limits_bound':'three_original_A00025_ends_both_tails_and_explicit_comparison_limits_bound',"    assert len(tests)==len({t[0] for t in tests})":extra+"    assert len(tests)==len({t[0] for t in tests})"}
    r=derive('scripts/challenge_lil_B226_atomic_v7275b.py','scripts/challenge_lil_B227_atomic_v7322.py',changes);ROOT.mkdir(parents=True);save(ROOT/'source_locked_B227_semantic_challenges.json',dict(tool=r,all_changed_cases_must_reject_before_archive_write=True,file_digests_bypassed_andapproved_records_mirrored_to_reach_deep_semantics=True,new_credit=0,full_goal_complete=False))
