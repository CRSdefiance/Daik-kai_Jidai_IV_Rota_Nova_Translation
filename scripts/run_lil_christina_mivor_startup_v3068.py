"""Isolated current Lil New Game and inherited ordinary-town cold boots."""
import argparse,os,sys
from pathlib import Path
from shutil import copy2
from scripts import headless_desmume_v193 as harness
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_Christina_Mivor_runs_v3068')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',choices=['newgame','town'],required=True);case=p.parse_args().case
    ROOT.mkdir(parents=True,exist_ok=True);planpath=ROOT/(case+'_plan.json');assert not planpath.exists()
    version=3066;rom=Path(f'out/all_routes_combined_v{version}_candidate.nds')
    digest=sha(rom.read_bytes());manifest=read(rom.with_suffix('.manifest.json'));assert manifest['candidate_sha256']==digest
    cap=CAP/f'lil_Christina_Mivor_v3068_{case}_V{version}';assert not cap.exists()
    donor=None;source=None;battery=[]
    if case=='town':
        priorpath=Path('work/analysis/surrender_advice_runs_v2676/town_plan.json');prior=read(priorpath)
        sourceinputs=Path(prior['inputs']);frames=prior['frames'];captures=prior['captures']
        source=Path(prior['source_donor']);sourcehash=sha(source.read_bytes());assert sourcehash==prior['source_donor_sha256']
        donor=ROOT/'town_disposable.dsv';assert not donor.exists();copy2(source,donor);battery=['--battery-save',str(donor)]
    else:
        priorpath=Path('work/analysis/lil_opening_trace_v1706/run_plan.json');prior=read(priorpath)
        sourceinputs=Path(prior['original_inputs']);frames=4001;captures=[1,60,180,1600,2000,2400,3200,4000]
        assert sha(sourceinputs.read_bytes())==prior['inputs_sha256']
    schedule=read(sourceinputs);inputs=ROOT/(case+'_inputs.json');save(inputs,schedule)
    save(planpath,dict(candidate=str(rom),candidate_sha256=digest,profile=manifest['profile'],case=case,PID=os.getpid(),
        frames=frames,captures=captures,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),
        source_schedule=str(sourceinputs),source_schedule_sha256=sha(sourceinputs.read_bytes()),
        prior_plan=str(priorpath),prior_plan_sha256=sha(priorpath.read_bytes()),
        source_donor=str(source) if source else None,source_donor_sha256=sourcehash if source else None,
        disposable_donor=str(donor) if donor else None,inherited_five_ship_test_battery_not_earned_progress=case=='town',
        no_new_RAM_code_gameplay_fixture_observer_or_savestate=True,not_a_selected_Christina_Mivor_activation=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    sys.argv=['headless_desmume_v193.py','--rom',str(rom),'--out',str(cap),'--frames',str(frames),
        '--inputs-json',str(inputs),*battery,'--touchscreen','--capture-every','999999','--capture-at',*map(str,captures),
        '--dump-capture-ram','--dump-ram']
    harness.main()
    if source:assert sha(source.read_bytes())==sha(donor.read_bytes())==sourcehash
    report=read(cap/'capture_report.json')
    assert report['frames']==frames and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    save(ROOT/(case+'_terminal.json'),dict(terminal=True,frames=frames,candidate_sha256=digest,
        report=str(cap/'capture_report.json'),report_sha256=sha((cap/'capture_report.json').read_bytes()),
        source_and_disposable_donor_unchanged=True,no_new_RAM_code_gameplay_fixture_or_observer=True,full_goal_complete=False))
    print(case+' cold boot terminal;isolated frame/RAM evidence retained;no selectedChristina-Mivor activation.',flush=True)
