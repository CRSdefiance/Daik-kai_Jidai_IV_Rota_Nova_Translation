"""Own registered four New Games andpreserved Copenhagen town control; exact prior inputs."""
import argparse,os,sys
from pathlib import Path
from shutil import copy2
from scripts import headless_desmume_v193 as harness
from scripts.maria_existing_unlock_contract_v7680 import validate_fixture,validate_capture
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B36_startup_runs_v7823')
RELEASE=Path('work/analysis/maria_B36_release_v7822/registered_release_verification.json')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--case',choices=['route3'],required=True);case=ap.parse_args().case
    folder=ROOT/case;assert not folder.exists();release=read(RELEASE);rom=Path(release['candidate']);digest=sha(rom.read_bytes());manifest=read(rom.with_suffix('.manifest.json'))
    assert digest==release['candidate_sha256']==manifest['candidate_sha256'] and release['whole_clean_input_ROM_reconstruction_byte_exact'] and manifest['profile']=='all-routes-unified-v7821'
    if case=='route3':
        priorroot=Path('work/analysis/maria_story_startup_runs_v7781/route3');route=3
    else:
        priorroot=Path('work/analysis/papal_trade_startup_runs_v7663b' if case in ['route0','route1'] else 'work/analysis/papal_trade_startup_runs_v7663')/case
        route={'route0':0,'route1':1,'route2':2,'town':1}[case]
    priorpath=priorroot/'run_plan.json';oldterminal=priorroot/'terminal.json';prior=read(priorpath);source_inputs=Path(prior['inputs'])
    assert sha(source_inputs.read_bytes())==prior['inputs_sha256'];frames=prior['frames'];captures=prior['captures']
    folder.mkdir(parents=True);inputs=folder/'identical_ordinary_inputs.json';save(inputs,read(source_inputs));battery=[];source=donor=None;fp=None
    if case=='town':
        source=Path(prior['source_donor']);sourcehash=prior['source_donor_sha256'];assert sha(source.read_bytes())==sourcehash
        donor=folder/'town_disposable.dsv';copy2(source,donor);battery=['--battery-save',str(donor)]
    elif case=='route3':
        historical=Path(prior['existing_system_unlock_manifest']);fixture=validate_fixture(historical);fixture.update(production_ROM=str(rom),production_ROM_sha256=digest,current_test_scope='Own registered V7821 Maria NewGame/startup;existing system-only unlock,not earned or optional B36 activation.')
        fp=folder/'existing_system_unlock_manifest.json';save(fp,fixture);validate_fixture(fp);source=Path(fixture['fixture_save']);sourcehash=fixture['fixture_save_sha256'];battery=['--battery-save',str(source),'--allow-gallery-fixtures','--gallery-save-fixture-manifest',str(fp)]
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'Maria_B36_V7821_{case}_v7823';assert not cap.exists()
    pp=folder/'run_plan.json';save(pp,dict(candidate=str(rom),candidate_sha256=digest,profile=manifest['profile'],case=case,route=route,route_identity={0:'Rafael',1:'Hodram',2:'Lil',3:'Maria'}[route],expected_original_captain_ID=route,PID=os.getpid(),frames=frames,captures=captures,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),prior_plan=str(priorpath),prior_plan_sha256=sha(priorpath.read_bytes()),prior_terminal=str(oldterminal),prior_terminal_sha256=sha(oldterminal.read_bytes()),source_donor=str(source) if source else None,source_donor_sha256=sourcehash if source else None,disposable_donor=str(donor) if donor else None,existing_system_unlock_manifest=str(fp) if fp else None,existing_system_unlock_manifest_sha256=sha(fp.read_bytes()) if fp else None,earned_unlock_verified=False if fp else None,capture_folder=str(cap),inherited_five_ship_test_battery_not_earned_progress=case=='town',existing_system_only_unlock_not_earned=case=='route3',town_actual_Hodram_captain1_old_plan_labels_preserved=case=='town',no_RAM_code_observer_savestate_roles_roster_funds_RNG_orresult_forcing=True,no_optional_story_arc_activation_orfullroute_claim=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    sys.argv=['headless_desmume_v193.py','--rom',str(rom),'--out',str(cap),'--frames',str(frames),'--inputs-json',str(inputs),*battery,*(['--touchscreen'] if case in ['route2','route3','town'] else []),'--capture-every','999999','--capture-at',*map(str,captures),'--dump-capture-ram','--dump-ram']
    harness.main();rp=cap/'capture_report.json';report=read(rp)
    assert report['frames']==frames and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    if case=='route3':validate_capture(report)
    else:assert not any(v for k,v in report.items() if k.startswith('synthetic_'))
    if source:assert sha(source.read_bytes())==sourcehash
    if donor:assert sha(donor.read_bytes())==sourcehash
    save(folder/'terminal.json',dict(terminal=True,case=case,candidate_sha256=digest,frames=frames,report=str(rp),report_sha256=sha(rp.read_bytes()),run_plan=str(pp),run_plan_sha256=sha(pp.read_bytes()),source_and_disposable_donor_unchanged=True,own_registered_ROM_not_old_snapshot_orRAM_overlay=True,new_credit=0,full_goal_complete=False))
    print(case+' own V7821 startup terminal;comparison/native binding pending.No optional activation orfull-route credit.',flush=True)
