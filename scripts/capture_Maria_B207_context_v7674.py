"""Capture own-current Maria through the verified current New Game menu and three ordinary RIGHT presses."""
import os,sys
from pathlib import Path
from scripts import headless_desmume_v193 as harness
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_route_run_v7674')
if __name__=='__main__':
    assert not ROOT.exists();v=read('work/analysis/editorial_handoff_verification_v7667/verified_handoff.json');rom=Path(v['candidate'])
    assert sha(rom.read_bytes())==v['candidate_sha256'] and read(rom.with_suffix('.manifest.json'))['profile']=='all-routes-unified-v7660'
    source=Path('work/analysis/papal_trade_route_runs_v7625/route0/ordinary_NewGame_inputs.json');base=read(source);assert [r['start'] for r in base]==[1000,1200,1800,2200];prefix=sorted(base+[dict(start=f,duration=12,buttons=['RIGHT']) for f in [1400,1500,1600]],key=lambda r:r['start'])
    assert [r['start'] for r in prefix]==[1000,1200,1400,1500,1600,1800,2200] and sum(r['buttons']==['RIGHT'] for r in prefix)==3
    ROOT.mkdir(parents=True);inputs=ROOT/'ordinary_Maria_NewGame_prefix.json';save(inputs,prefix)
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/Maria_B207_own_V7660_v7674');assert not cap.exists()
    pp=ROOT/'run_plan.json';save(pp,dict(candidate=str(rom),candidate_sha256=v['candidate_sha256'],profile=v['profile'],PID=os.getpid(),frames=4001,captures=[1,180,1700,1900,3200,3400,4000],source_inputs=str(source),source_inputs_sha256=sha(source.read_bytes()),inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),current_verified_Rafael_NewGame_menu_then_three_ordinary_RIGHT_presses=True,preserved_failed_older_schedule_capture="work/analysis/maria_B207_route_run_v7671/terminal.json",route=3,route_identity='Maria',expected_original_captain_ID=3,capture_folder=str(cap),no_battery_savestate_ROM_RAM_roles_roster_funds_RNG_event_orresult_fixture=True,no_optional_B207_orfull_route_coverage_claim=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    sys.argv=['headless_desmume_v193.py','--rom',str(rom),'--out',str(cap),'--frames','4001','--inputs-json',str(inputs),'--touchscreen','--capture-every','999999','--capture-at','1','180','1700','1900','3200','3400','4000','--dump-capture-ram','--dump-ram']
    harness.main();rp=cap/'capture_report.json';r=read(rp)
    assert r['frames']==4001 and r['cold_boot'] and not r['savestate_loaded'] and not r.get('battery_save_preloaded') and not r['callback_errors'] and not any(v for k,v in r.items() if k.startswith('synthetic_'))
    save(ROOT/'terminal.json',dict(terminal=True,candidate_sha256=v['candidate_sha256'],report=str(rp),report_sha256=sha(rp.read_bytes()),run_plan=str(pp),run_plan_sha256=sha(pp.read_bytes()),frames=4001,actual_captain3_strict_payload_binding_pending=True,no_optional_scene_ornew_editorial_credit=True,full_goal_complete=False))
    print('Own-current Maria ordinary NewGame capture terminal;actual captain3/native/payload binding pending.',flush=True)
