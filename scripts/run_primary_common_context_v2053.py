"""Ordinary Maria/primary town-service replay with source-bound COMMON requests."""
import ctypes as ct
import sys
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import observe_primary_common_v2053 as observed
from scripts.verify_village_wrap_v608 import read,save

ROOT=observed.ROOT
ROM=observed.ROM
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_services_actual_v2053_V2047')
PRIOR=Path('E:/Rota Nova translations/Generated/work/emulation_v193/maria_opening_context_v2035_V2030/capture_report.json')
if __name__=='__main__':
    assert not ROOT.exists()and not CAP.exists();observed.prepare_contract()
    report=read(PRIOR);old=read('work/analysis/maria_opening_context_v2035/run_plan.json');donor=Path(old['existing_isolated_system_unlock_save'])
    assert sha(donor.read_bytes())==old['save_sha256'];digest=sha(ROM.read_bytes());assert digest==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    fixture=read(old['fixture_manifest']);assert fixture['only_system_low_four_bits_and_original_checksum_changed']and not fixture['earned_unlock_verified']
    fixture.update(production_ROM=str(ROM),production_ROM_sha256=digest,current_test_scope='Ordinary Maria New Game andprimary town-service context;existing systemunlock notearned,no story/location/outcome fixture.')
    manifest=ROOT/'existing_system_unlock_manifest.json';save(manifest,fixture);inputs=ROOT/'ordinary_context_inputs.json';save(inputs,report['scripted_input_schedule'])
    frames=sorted({r['frame']for r in report['frames_captured']});assert report['frames']==38500
    save(ROOT/'run_plan.json',dict(candidate=str(ROM),candidate_sha256=digest,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),frames=38500,
        captures=frames,existing_isolated_system_unlock=str(donor),donor_sha256=sha(donor.read_bytes()),fixture_manifest=str(manifest),
        fixture_manifest_sha256=sha(manifest.read_bytes()),earned_unlock_verified=False,no_savestate_story_location_RNG_funds_outcome_fixture=True,
        prior_report=str(PRIOR),prior_report_sha256=sha(PRIOR.read_bytes()),observer_sha256=sha(Path(observed.__file__).read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    class Proxy:
        def __getattr__(self,name):return getattr(ct,name)
        def CDLL(self,path,*args,**kwargs):
            core=ct.CDLL(path,*args,**kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                observer=observed.Observer(core,CAP/'common_observer');observers.append(observer);observer.install();old_run=core.retro_run;old_run.restype=None
                def run():observer.next_frame();old_run()
                core.retro_run=run
            return core
    observers=[];previous=harness.ct;harness.ct=Proxy()
    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','38500','--inputs-json',str(inputs),
        '--battery-save',str(donor),'--allow-gallery-fixtures','--gallery-save-fixture-manifest',str(manifest),'--touchscreen',
        '--capture-every','999999','--capture-at',*map(str,frames),'--dump-capture-ram','--dump-ram']
    try:harness.main()
    finally:
        harness.ct=previous
        for observer in observers:observer.close()
    for observer in observers:observer.save()
    assert sha(donor.read_bytes())==old['save_sha256']
    save(ROOT/'terminal.json',dict(terminal=True,frames=38500,candidate_sha256=digest,all_observer_host_slots_restored=True,
        original_system_unlock_donor_unchanged=True,earned_unlock_verified=False,full_goal_complete=False))
