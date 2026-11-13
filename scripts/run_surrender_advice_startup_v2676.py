"""Cold-boot registered2674 through existing NewGame and ordinary town schedules."""
import argparse,sys,os
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/surrender_advice_runs_v2676')
ROM=Path('out/all_routes_combined_v2674_candidate.nds')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--case',choices=['newgame','town'],required=True);case=parser.parse_args().case
    ROOT.mkdir(parents=True,exist_ok=True);planpath=ROOT/(case+'_plan.json');assert not planpath.exists()
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'surrender_advice_v2676_{case}_V2674';assert not cap.exists()
    digest=sha(ROM.read_bytes());manifest=read(ROM.with_suffix('.manifest.json'));assert manifest['candidate_sha256']==digest and manifest['profile']=='all-routes-unified-v2674'
    priorcase='newgame' if case=='newgame' else 'refit'
    priorpath=Path('work/analysis/refit_spritsail_runs_v2287')/(priorcase+'_plan.json');prior=read(priorpath)
    sourceinputs=Path(prior['inputs']);schedule=read(sourceinputs);assert sha(sourceinputs.read_bytes())==prior['inputs_sha256']
    source=None;sourcehash=None;battery=[]
    if case=='town':
        source=Path('work/analysis/refit_editorial_v831/disposable_refit_source.dsv');sourcehash=sha(source.read_bytes())
        assert sourcehash=='febc859c5af2df6fa8023c349bb7f31b5fc15ea769fb2eea527b3a3f80521731'
        donor=ROOT/'town_disposable.dsv';assert not donor.exists();copy2(source,donor);battery=['--battery-save',str(donor)]
    inputs=ROOT/(case+'_inputs.json');save(inputs,schedule)
    save(planpath,dict(candidate=str(ROM),candidate_sha256=digest,profile=manifest['profile'],case=case,PID=os.getpid(),
        frames=prior['frames'],inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),captures=prior['captures'],
        prior_schedule_plan=str(priorpath),prior_schedule_plan_sha256=sha(priorpath.read_bytes()),
        source_donor=str(source) if source else None,source_donor_sha256=sourcehash,
        disposable_donor=str(donor) if source else None,
        inherited_five_ship_test_battery_not_earned_progress=case=='town',
        no_new_RAM_code_gameplay_fixture_observer_or_savestate=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(cap),'--frames',str(prior['frames']),
        '--inputs-json',str(inputs),*battery,'--touchscreen','--capture-every','999999','--capture-at',*map(str,prior['captures']),
        '--dump-capture-ram','--dump-ram']
    harness.main()
    if source:assert sha(source.read_bytes())==sha(donor.read_bytes())==sourcehash
    report=read(cap/'capture_report.json')
    assert report['frames']==prior['frames'] and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    save(ROOT/(case+'_terminal.json'),dict(terminal=True,frames=report['frames'],candidate_sha256=digest,
        report=str(cap/'capture_report.json'),report_sha256=sha((cap/'capture_report.json').read_bytes()),
        source_and_disposable_donor_unchanged=True,no_new_RAM_code_gameplay_fixture_or_observer=True,
        full_goal_complete=False))
    print(f'{case}2674cold boot terminal;read-only frame/RAM evidence preserved;no new gameplay fixture.',flush=True)
