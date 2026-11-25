"""Bind the second actual B52 response and its source-flagged kind1/zero-value return."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_opposition_audit_tools_v8653');assert not root.exists()
    old="""                assert row['result_words']==[0,pairs[-2]['native_result'][1]];finished=True;normal=dict(frame=row['frame'],native_result=row['result_words'],complete_four_byte_end=True)"""
    new="""                ending=command['whole_command_hex'];assert ending in ['00000000','00000080']
                expected_return=[1,0] if ending=='00000080' else [0,pairs[-2]['native_result'][1]]
                assert row['result_words']==expected_return;finished=True;normal=dict(frame=row['frame'],native_result=row['result_words'],complete_four_byte_end=True,source_end_hex=ending,flagged_end_clears_carried_value=ending=='00000080')"""
    result=derive('scripts/audit_Hodram_B52_actual_v8651.py','scripts/audit_Hodram_B52_opposition_v8653.py',{
        old:new,
        'Hodram_B52_actual_v8651':'Hodram_B52_opposition_actual_v8653','Hodram_B52_scene_runs_v8649':'Hodram_B52_opposition_runs_v8652',
        'normal_return=normal':'script_return=normal',"kind='normal-return-not-observed'":"kind='script-return-not-observed'",'no_B51_FE_panel':'no_B52_FE_panel',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,original_complete_body_name_source_payload_branch_extent_readonly_andcanary_guards_preserved=True,actual_return_matches_exact_original_fourbyte_word_normal_orflagged_not_normalized=True,alternate_unvisited_withdrawal_preserved_as_case_specific_scope=True,no_capture_replay_input_retiming_orcredit=True,new_credit=0,full_goal_complete=False))
