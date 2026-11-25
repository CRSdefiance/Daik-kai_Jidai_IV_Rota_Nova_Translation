"""Capture own-current Maria NewGame from the exact established ordinary input prefix."""
import os,sys
from pathlib import Path
from scripts import headless_desmume_v193 as harness
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_route_run_v7671')
if __name__=='__main__':
    assert not ROOT.exists();v=read('work/analysis/editorial_handoff_verification_v7667/verified_handoff.json');rom=Path(v['candidate'])
    assert sha(rom.read_bytes())==v['candidate_sha256'] and read(rom.with_suffix('.manifest.json'))['profile']=='all-routes-unified-v7660'
    source=Path('work/analysis/maria_opening_context_v2035/ordinary_existing_Maria_inputs.json');prefix=[r for r in read(source) if r['start']<=3601]
    assert [r['start'] for r in prefix]==[1601,2001,2401,2801,3001,3201,3401,3601] and sum(r['buttons']==['RIGHT'] for r in prefix)==3
    ROOT.mkdir(parents=True);inputs=ROOT/'ordinary_Maria_NewGame_prefix.json';save(inputs,prefix)
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/Maria_B207_own_V7660_v7671');assert not cap.exists()
    pp=ROOT/'run_plan.json';save(pp,dict(candidate=str(rom),candidate_sha256=v['candidate_sha256'],profile=v['profile'],PID=os.getpid(),frames=4001,captures=[1,180,3200,3400,4000],source_inputs=str(source),source_inputs_sha256=sha(source.read_bytes()),inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),prefix_truncated_after_existing_Maria_confirmation_not_controller_retimed=True,route=3,route_identity='Maria',expected_original_captain_ID=3,capture_folder=str(cap),no_battery_savestate_ROM_RAM_roles_roster_funds_RNG_event_orresult_fixture=True,no_optional_B207_orfull_route_coverage_claim=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    sys.argv=['headless_desmume_v193.py','--rom',str(rom),'--out',str(cap),'--frames','4001','--inputs-json',str(inputs),'--touchscreen','--capture-every','999999','--capture-at','1','180','3200','3400','4000','--dump-capture-ram','--dump-ram']
    harness.main();rp=cap/'capture_report.json';r=read(rp)
    assert r['frames']==4001 and r['cold_boot'] and not r['savestate_loaded'] and not r.get('battery_save_preloaded') and not r['callback_errors'] and not any(v for k,v in r.items() if k.startswith('synthetic_'))
    save(ROOT/'terminal.json',dict(terminal=True,candidate_sha256=v['candidate_sha256'],report=str(rp),report_sha256=sha(rp.read_bytes()),run_plan=str(pp),run_plan_sha256=sha(pp.read_bytes()),frames=4001,actual_captain3_strict_payload_binding_pending=True,no_optional_scene_ornew_editorial_credit=True,full_goal_complete=False))
    print('Own-current Maria ordinary NewGame capture terminal;actual captain3/native/payload binding pending.',flush=True)
