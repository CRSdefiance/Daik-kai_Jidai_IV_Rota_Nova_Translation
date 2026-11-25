"""Capture own-current Hodram New Game through original ordinary inputs;not B49 activation."""
import argparse,os,sys
from pathlib import Path
from scripts import headless_desmume_v193 as harness
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_registered_context_runs_v8477')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--route',type=int,choices=[1],required=True);route=ap.parse_args().route
    folder=ROOT/f'route{route}';assert not folder.exists()
    verified=Path('work/analysis/Hodram_B49_release_v8476/registered_release_verification.json');v=read(verified);rom=Path(v['candidate']);manifest=read(rom.with_suffix('.manifest.json'))
    assert manifest['profile']=='all-routes-unified-v8475' and sha(rom.read_bytes())==manifest['candidate_sha256']==v['candidate_sha256']
    identity=Path('work/analysis/papal_trade_route_identity_v7624/route_identity_correction_no_ROM_prose_reference_orcredit_change.json');scope=next(r for r in read(identity)['current_scope'] if r['expected_original_captain_ID']==route)
    source=Path('work/analysis/movie_viewport_v303/rafael_start_inputs.json') if route==0 else Path('work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json')
    schedule=read(source);assert all(x['buttons'] in [['START'],['A'],['RIGHT']] for x in schedule)
    assert sum(x['buttons']==['RIGHT'] for x in schedule)==route
    folder.mkdir(parents=True);inputs=folder/'ordinary_NewGame_inputs.json';save(inputs,schedule)
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'Hodram_B49_registered_route{route}_v8477_V8475';assert not cap.exists()
    plan=folder/'run_plan.json';save(plan,dict(candidate=str(rom),candidate_sha256=v['candidate_sha256'],profile=manifest['profile'],route=route,route_identity=scope['route_identity'],expected_original_captain_ID=route,capture_folder=str(cap),PID=os.getpid(),frames=4001,captures=[1,180,2000,4000],source_inputs=str(source),source_inputs_sha256=sha(source.read_bytes()),inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),route_identity_proof=str(identity),route_identity_proof_sha256=sha(identity.read_bytes()),current_registered_ROM_only_no_ROM_or_RAM_or_savestate_fixture=True,no_battery_donor_or_observer=True,ordinary_route_selection_not_optional_B47_B48_activation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    sys.argv=['headless_desmume_v193.py','--rom',str(rom),'--out',str(cap),'--frames','4001','--inputs-json',str(inputs),'--capture-every','999999','--capture-at','1','180','2000','4000','--dump-capture-ram','--dump-ram']
    harness.main();rp=cap/'capture_report.json';report=read(rp)
    assert report['frames']==4001 and report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors'] and not any(value for key,value in report.items() if key.startswith('synthetic_'))
    save(folder/'terminal.json',dict(terminal=True,candidate_sha256=v['candidate_sha256'],report=str(rp),report_sha256=sha(rp.read_bytes()),run_plan=str(plan),run_plan_sha256=sha(plan.read_bytes()),route=route,route_identity=scope['route_identity'],frames=4001,expected_captain_anddeployed_payload_binding_pending=True,no_optional_scene_orfull_route_coverage_claim=True,full_goal_complete=False))
    print(scope['route_identity']+' own-current NewGame capture terminal;actual captain/payload/EV/native binding pending.',flush=True)
