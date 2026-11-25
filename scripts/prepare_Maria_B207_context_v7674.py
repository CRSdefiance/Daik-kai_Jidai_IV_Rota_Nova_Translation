"""Preserve the Sound Setup attempt; select Maria through current ordinary New Game."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_context_tools_v7674')
if __name__=='__main__':
    assert not ROOT.exists()
    changes={
        'Capture own-current Maria NewGame from the exact established ordinary input prefix.':'Capture own-current Maria through the verified current New Game menu and three ordinary RIGHT presses.',
        'v7671':'v7674',
        "source=Path('work/analysis/maria_opening_context_v2035/ordinary_existing_Maria_inputs.json');prefix=[r for r in read(source) if r['start']<=3601]":"source=Path('work/analysis/papal_trade_route_runs_v7625/route0/ordinary_NewGame_inputs.json');base=read(source);assert [r['start'] for r in base]==[1000,1200,1800,2200];prefix=sorted(base+[dict(start=f,duration=12,buttons=['RIGHT']) for f in [1400,1500,1600]],key=lambda r:r['start'])",
        "assert [r['start'] for r in prefix]==[1601,2001,2401,2801,3001,3201,3401,3601] and sum(r['buttons']==['RIGHT'] for r in prefix)==3":"assert [r['start'] for r in prefix]==[1000,1200,1400,1500,1600,1800,2200] and sum(r['buttons']==['RIGHT'] for r in prefix)==3",
        'prefix_truncated_after_existing_Maria_confirmation_not_controller_retimed=True':'current_verified_Rafael_NewGame_menu_then_three_ordinary_RIGHT_presses=True,preserved_failed_older_schedule_capture="work/analysis/maria_B207_route_run_v7671/terminal.json"',
        'captures=[1,180,3200,3400,4000]':'captures=[1,180,1700,1900,3200,3400,4000]',
        "'1','180','3200','3400','4000'":"'1','180','1700','1900','3200','3400','4000'",
    }
    capture=derive('scripts/capture_Maria_B207_context_v7671.py','scripts/capture_Maria_B207_context_v7674.py',changes)
    binder=derive('scripts/bind_Maria_B207_context_v7672.py','scripts/bind_Maria_B207_context_v7675.py',{
        'maria_B207_native_v7672':'maria_B207_native_v7675',
        'maria_B207_route_run_v7671':'maria_B207_route_run_v7674',
        '[3200,3400,4000]':'[1700,1900,4000]',
    })
    consumers=derive('scripts/prove_Maria_B207_consumers_v7673.py','scripts/prove_Maria_B207_consumers_v7676.py',{
        'maria_B207_consumers_v7673':'maria_B207_consumers_v7676',
        'maria_B207_native_v7672':'maria_B207_native_v7675',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_ordinary_menu_successors.json',dict(capture=capture,binder=binder,consumers=consumers,strict_captain3_guard_unchanged=True,old_capture_andfailed_binder_preserved=True,new_credit=0,full_goal_complete=False))
