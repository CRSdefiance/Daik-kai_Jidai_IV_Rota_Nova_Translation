"""Own-ROM New Games for captains0/1/2 and preserved ordinary-town battery regression."""
import argparse,os,sys
from pathlib import Path
from shutil import copy2
from scripts import headless_desmume_v193 as harness
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_startup_runs_v7663b')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--case',choices=['route0','route1','route2','town'],required=True);case=ap.parse_args().case
    folder=ROOT/case;assert not folder.exists()
    release=read('work/analysis/papal_trade_release_v7661/registered_release_verification.json');rom=Path(release['candidate']);digest=sha(rom.read_bytes());manifest=read(rom.with_suffix('.manifest.json'))
    assert digest==release['candidate_sha256']==manifest['candidate_sha256'] and release['whole_clean_input_ROM_reconstruction_byte_exact'] and manifest['profile']=='all-routes-unified-v7660'
    if case in ['route0','route1']:
        route=int(case[-1]);priorpath=Path(f'work/analysis/papal_trade_route_runs_v7625/route{route}/run_plan.json');prior=read(priorpath);old_terminal=Path(f'work/analysis/papal_trade_route_runs_v7625/route{route}/terminal.json')
        source_inputs=Path(prior['inputs']);frames=4001;captures=[1,180,2000,4000];source=None;source_hash=None
    else:
        route=2;oldcase='newgame' if case=='route2' else 'town';priorpath=Path(f'work/analysis/lil_B234_runs_v7614/{oldcase}_plan.json');prior=read(priorpath);old_terminal=Path(f'work/analysis/lil_B234_runs_v7614/{oldcase}_terminal.json')
        source_inputs=Path(prior['inputs']);frames=4001 if case=='route2' else prior['frames'];captures=[1,180,2000,4000] if case=='route2' else prior['captures'];source=Path(prior['source_donor']) if case=='town' else None;source_hash=prior['source_donor_sha256'] if source else None
    assert sha(source_inputs.read_bytes())==prior['inputs_sha256'];folder.mkdir(parents=True);inputs=folder/'ordinary_inputs.json';save(inputs,read(source_inputs));battery=[];donor=None
    if source:
        assert sha(source.read_bytes())==source_hash;donor=folder/'town_disposable.dsv';copy2(source,donor);battery=['--battery-save',str(donor)]
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'papal_trade_V7660_{case}_v7663b';assert not cap.exists()
    pp=folder/'run_plan.json';save(pp,dict(candidate=str(rom),candidate_sha256=digest,profile=manifest['profile'],case=case,route=route,route_identity={0:'Rafael',1:'Hodram',2:'Lil'}[route],expected_original_captain_ID=route,PID=os.getpid(),frames=frames,captures=captures,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),prior_plan=str(priorpath),prior_plan_sha256=sha(priorpath.read_bytes()),prior_terminal=str(old_terminal),prior_terminal_sha256=sha(old_terminal.read_bytes()),source_donor=str(source) if source else None,source_donor_sha256=source_hash,disposable_donor=str(donor) if donor else None,capture_folder=str(cap),inherited_five_ship_test_battery_not_earned_progress=case=='town',no_RAM_code_observer_savestate_ornew_gameplay_fixture=True,no_selected_optional_papal_scene_activation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    sys.argv=['headless_desmume_v193.py','--rom',str(rom),'--out',str(cap),'--frames',str(frames),'--inputs-json',str(inputs),*battery,*(['--touchscreen'] if case in ['route2','town'] else []),'--capture-every','999999','--capture-at',*map(str,captures),'--dump-capture-ram','--dump-ram']
    harness.main()
    if source:assert sha(source.read_bytes())==sha(donor.read_bytes())==source_hash
    rp=cap/'capture_report.json';r=read(rp);assert r['frames']==frames and r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors'] and not any(v for k,v in r.items() if k.startswith('synthetic_'))
    save(folder/'terminal.json',dict(terminal=True,case=case,candidate_sha256=digest,frames=frames,report=str(rp),report_sha256=sha(rp.read_bytes()),run_plan=str(pp),run_plan_sha256=sha(pp.read_bytes()),source_and_disposable_donor_unchanged=True,source_is_own_registered_ROM_not_old_snapshot_orRAM_overlay=True,new_credit=0,full_goal_complete=False))
    print(case+' own-current cold boot terminal;comparison/native binding pending;no optional event orfull-route claim.',flush=True)
