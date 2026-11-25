"""Match the two earlier mouse-pointer controls; preserve all original captures and guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_startup_pointer_tools_v7663b')
if __name__=='__main__':
    assert not ROOT.exists()
    for route in [0,1]:
        p=read(f'work/analysis/papal_trade_startup_runs_v7663/route{route}/run_plan.json');t=read(f'work/analysis/papal_trade_startup_runs_v7663/route{route}/terminal.json')
        a=read(read(p['prior_terminal'])['report']);b=read(t['report'])
        assert a['scripted_input_schedule']==b['scripted_input_schedule']
        changed={k:(a['core_options'].get(k),b['core_options'].get(k)) for k in set(a['core_options'])|set(b['core_options']) if a['core_options'].get(k)!=b['core_options'].get(k)}
        assert changed=={'desmume_pointer_type':('mouse','touch')}
    a=derive('scripts/run_papal_trade_startup_v7663.py','scripts/run_papal_trade_startup_v7663b.py',{'papal_trade_startup_runs_v7663':'papal_trade_startup_runs_v7663b','_v7663':'_v7663b',"""*battery,'--touchscreen','--capture-every'""":"""*battery,*(['--touchscreen'] if case in ['route2','town'] else []),'--capture-every'"""})
    b=derive('scripts/verify_papal_trade_startup_v7664.py','scripts/verify_papal_trade_startup_v7664b.py',{'papal_trade_startup_verification_v7664':'papal_trade_startup_verification_v7664b',"RUN=Path('work/analysis/papal_trade_startup_runs_v7663')":"RUN=Path('work/analysis/papal_trade_startup_runs_v7663')\ndef run_folder(case):return Path('work/analysis/papal_trade_startup_runs_v7663b')/case if case in ['route0','route1'] else RUN/case",'RUN/case':'run_folder(case)','RUN/c/':'run_folder(c)/'})
    # The binder has not been executed; select the strict successor comparison.
    binder=Path('scripts/bind_current_V7660_native_v7665.py');text=binder.read_text('utf8');old='papal_trade_startup_verification_v7664/';assert old in text;binder.write_text(text.replace(old,'papal_trade_startup_verification_v7664b/'),'utf8')
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_matching_pointer_controls.json',dict(tools=[a,b],original_failed_core_options_assertion_andall_four_original_captures_preserved=True,only_Rafael_Hodram_cases_rerun_to_match_mouse_pointer_controls=True,Lil_andtown_existing_exact_matching_options_andcaptures_reused=True,all_capture_framebuffers_already_equal_butstrict_option_guard_preserved=True,no_ROM_prose_controller_schedule_state_orresult_change=True,new_credit=0,full_goal_complete=False))
