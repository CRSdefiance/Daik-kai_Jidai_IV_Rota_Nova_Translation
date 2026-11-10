"""Bind measured Hodram town captain1; preserve the failed assumed-Lil plan and assertion."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_town_scope_tools_v7664c')
if __name__=='__main__':
    assert not ROOT.exists();p=read('work/analysis/papal_trade_startup_runs_v7663/town/run_plan.json');t=read('work/analysis/papal_trade_startup_runs_v7663/town/terminal.json');reports=[read(read(p['prior_terminal'])['report']),read(t['report'])]
    arm=NdsImage.open(p['candidate']).read_file('/__arm9__.bin');rows=[]
    for r in reports:
        s=next(s for s in r['read_only_capture_RAM_snapshots'] if s['frame']==3200);raw=Path(s['path']).read_bytes();assert sha(raw)==s['sha256'];_,get=get_machine(arm,raw);captain=get(0x7F244);assert captain==1
        rows.append(dict(ROM_sha256=r['ROM_sha256'],snapshot=s,actual_original_captain_ID=captain))
    assert p['route']==2 and p['route_identity']=='Lil' and sha(Path(p['source_donor']).read_bytes())==sha(Path(p['disposable_donor']).read_bytes())==p['source_donor_sha256']
    tool=derive('scripts/verify_papal_trade_startup_v7664b.py','scripts/verify_papal_trade_startup_v7664c.py',{
        'papal_trade_startup_verification_v7664b':'papal_trade_startup_verification_v7664c',
        "assert captain==plan['route']":"assert captain=={'route0':0,'route1':1,'route2':2,'town':1}[case]",
        "source_and_disposable_donor_unchanged=True,inherited_battery_not_earned_progress=case=='town'":"source_and_disposable_donor_unchanged=True,inherited_battery_not_earned_progress=case=='town',measured_original_captain_ID={'route0':0,'route1':1,'route2':2,'town':1}[case]",
        "all_three_captains0_1_2_actual_NewGames_verified=True":"all_three_captains0_1_2_actual_NewGames_verified=True,inherited_Stockholm_town_actual_Hodram_captain1_verified=True,historical_town_plan_route2_Lil_label_preserved_as_superseded_metadata=True",
    })
    binder=Path('scripts/bind_current_V7660_native_v7665.py');text=binder.read_text('utf8');old='papal_trade_startup_verification_v7664b/';assert old in text;binder.write_text(text.replace(old,'papal_trade_startup_verification_v7664c/'),'utf8')
    ROOT.mkdir(parents=True);save(ROOT/'actual_Hodram_town_captain1_source_current_binding.json',dict(tool=tool,source_current_captain_bindings=rows,historical_town_plan_route2_Lil_label_is_incorrect=True,correct_Stockholm_donor_identity='Hodram',actual_original_captain_ID=1,all_strict_source_current_actor_captain_options_inputs_andRGB_guards_preserved=True,failed_7664_and7664b_assertions_preserved_not_negative_control_orROM_failure=True,no_ROM_battery_controller_capture_orRAM_change_orreplay=True,new_credit=0,full_goal_complete=False))
