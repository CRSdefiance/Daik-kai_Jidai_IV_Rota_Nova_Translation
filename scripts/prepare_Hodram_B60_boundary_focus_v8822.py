"""Focused same-prefix cold boots with readonly snapshots at both measured end frames."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B60_boundary_focus_tools_v8822');assert not root.exists()
    actual=read('work/analysis/Hodram_B54_B60_actual_v8820/B60/paired_actual_dialogue_headers_flow_returns.json')
    assert [g['normal_return']['frame'] for g in actual['groups']]==[6176,6415]
    result=derive('scripts/run_Hodram_B54_B60_v8816.py','scripts/run_Hodram_B60_boundary_focus_v8822.py',{
        'Hodram_B54_B60_scene_runs_v8816':'Hodram_B60_boundary_focus_runs_v8822',
        'choices=[54,57,58,59,60]':'choices=[60]',
        'frames={54:6001,57:9001,58:16001,59:10001,60:10001}':'frames={60:7001}',
        '_v8816':'_v8822',
        "captures=sorted(set(range(2350,frames,60))|{frames-1})":"captures=sorted(set(range(2350,frames,60))|{frames-1,6176,6415})",
        "'--dump-ram']":"'--capture-native-state-at','6176','6415','--dump-ram']",
        "report['frames']==frames and report['cold_boot']":"report['frames']==frames and report['exact_requested_native_state_capture_frames']==[6176,6415] and report['cold_boot']",
    })
    for group in actual['groups']:
        old=read(group['capture_report'])['scripted_input_schedule']
        source=read('work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json')
        prefix=source+[dict(start=f,duration=5,buttons=['A']) for f in range(4000,7001-480,240)]
        assert prefix==[r for r in old if r['start']<7001-480] and prefix[-1]['start']==6400
    root.mkdir(parents=True);save(root/'source_locked_boundary_focus.json',dict(derivation=result,
        concrete_risk='Long B60 paired run has different wholeactors/persistentobjects andlater RGB;preserve that result andinspect immediately at each original normal return before making any broader claim.',
        identical_ordinary_input_prefix_through_A6400_perlanguage=True,no_language_specific_retiming=True,
        both_languages_snapshot_same_absolute_frames=[6176,6415],snapshots_are_readonly_exports_never_loaded=True,
        all_coldboot_core_contract_observer_integrity_andstate_guards_preserved=True,
        no_full_playthrough_causality_orfuture_simulation_claim=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
