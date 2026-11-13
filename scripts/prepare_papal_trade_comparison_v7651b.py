"""Include the harness's actual automatic16001 final capture without omitting16000."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_comparison_tools_v7651b')
if __name__=='__main__':
    assert not ROOT.exists()
    for route in [0,1]:
        for version in ['clean_Japanese','English']:
            t=read(f'work/analysis/papal_trade_scene_runs_v7649/route{route}_{version}/terminal.json');r=read(t['report']);f=sorted(p['frame'] for p in r['frames_captured'])
            assert f[-2:]==[16000,16001] and r['frames']==16001
    tool=derive('scripts/measure_papal_trade_scene_pairs_v7651.py','scripts/measure_papal_trade_scene_pairs_v7651b.py',{'papal_trade_actual_comparison_v7651':'papal_trade_actual_comparison_v7651b','frames[-1]==16000':'frames[-1]==16001'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_automatic_final_frame_correction.json',dict(tool=tool,all_four_reports_explicit16000_andautomatic16001_preserved=True,prior_7651_assertion_failure_preserved_not_negative_control_orROM_failure=True,no_ROM_trace_snapshot_getter_constant_input_schedule_orcapture_change=True,no_new_emulator_run=True,new_credit=0,full_goal_complete=False))
