"""Source-lock final Maria five-gate approval to its actual evidence andmeasured limits."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_approval_tools_v7712')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/approve_papal_trade_native_v7655.py','scripts/approve_Maria_B207_native_v7712.py',{
        'Approve36 individual formatting gates':'Approve18 individual Maria formatting gates',
        'papal_trade_profile_v1':'maria_B207_profile_v1',
        'scripts.papal_trade_final_paths_v7655':'scripts.Maria_B207_final_paths_v7712',
        "actual['total_actual_speech_occurrences']==72":"actual['total_actual_speech_occurrences']==36",
        "view['all72_complete_source_English_speech_panes_individually_viewed']":"view['all36_complete_source_English_speech_panes_individually_viewed']",
        "policy['positive_count']==36 and policy['negative_count']==174 and stored['stored_alignment_cases']==144 and stored['zero_ink_parity_tail_count']==16":"policy['positive_count']==18 and policy['negative_count']==89 and stored['stored_alignment_cases']==72 and stored['zero_ink_parity_tail_count']==7",
        "view['later_RGB_differences_by_route']==[3,53] and [g['later_sample_count'] for g in later['groups']]==[133,133]":"view['later_RGB_differences']==104 and view['later_samples']==123 and [g['later_sample_count'] for g in later['groups']]==[123]",
        '{0:63,1:70}[route]':'{3:74}[route]',
        'guarded Raphael/Hodram profile':'guarded Maria profile',
        'Only exact R33 article-the continuation isclassified tokeep Papal States whole;all base QA andindividual row reasons remain.':'Seven individual row-count infos andall unmodified base QA remain;there areno warnings orwaivers.',
        'R5 keeps':'R4 keeps',
        'Fixtures prove neither original optional activation/location/earned progress norfull effects/routes/hardware.':'Fixtures explicitly useonlythe existing audited system unlock,earned=false;they prove neither original optional activation/location/earned progress norfull effects/routes/hardware.',
        'all36_individual_five_gates_approved=True,revision_count=26,retention_count=10,actual_pages=36,paired_source_English_speech_occurrences=72,all72_panes17_sheets_viewed=True':'all18_individual_five_gates_approved=True,revision_count=13,retention_count=5,actual_pages=18,paired_source_English_speech_occurrences=36,all36_panes9_sheets_viewed=True',
        '36 individual five-gate decisions approved:26 revisions/10 retentions':'18 individual Maria five-gate decisions approved:13 revisions/5 retentions',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_Maria_native_approval.json',dict(tool=tool,all_native_high_constants_andmultiplicity_preserved=True,no_English_source_control_orcredit_change=True,new_credit=0,full_goal_complete=False))
