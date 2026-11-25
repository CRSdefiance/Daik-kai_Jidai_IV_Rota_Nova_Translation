"""Ordinary Maria New Game with the existing isolated system-unlock save only."""
import ctypes as ct
import struct
import sys
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import observe_script_sources_v733 as original
from scripts.run_activity_special_live_v988 import GrowingCommands
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/maria_opening_context_v2035')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/maria_opening_context_v2035_V2030')
ROM=Path('out/all_routes_combined_v2030_candidate.nds')

if __name__=='__main__':
    assert not ROOT.exists()and not CAP.exists()
    digest=sha(ROM.read_bytes());assert digest==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    old=read('work/analysis/maria_intro_v684/preflight.json');donor=Path(old['donor'])
    assert sha(donor.read_bytes())==old['donor_sha256']
    fixture=read('work/analysis/maria_intro_v684/unlock_manifest.json')
    assert fixture['fixture_save_sha256']==old['donor_sha256']and fixture['all_six_route_save_slots_and_footer_unchanged']
    assert fixture['only_system_low_four_bits_and_original_checksum_changed']and fixture['earned_unlock_verified']is False
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin');contract=Path('work/analysis/script_sources_v733/source_contract.json')
    for target in read(contract)['targets']:assert struct.unpack_from('<I',arm,target['PC']-0x02000000)[0]==target['word']
    ROOT.mkdir(parents=True);(ROOT/'source_contract.json').write_bytes(contract.read_bytes())
    fixture.update(production_ROM=str(ROM),production_ROM_sha256=digest,current_test_scope='Ordinary Maria NewGame/opening and practical town visits;existing isolated system unlock,not earned. No story/location/RNG/funds/outcome fixture.')
    fixture_path=ROOT/'existing_system_unlock_manifest.json';save(fixture_path,fixture)
    prior=read('work/analysis/maria_intro_v684/run_config.json');inputs=ROOT/'ordinary_existing_Maria_inputs.json';save(inputs,read(prior['inputs']))
    journal=ROOT/'navigation.jsonl';journal.write_text('',encoding='utf-8');env={**original.__dict__,'ROM':ROM,'ROOT':ROOT}
    class Observer(original.Observer):
        __init__=FunctionType(original.Observer.__init__.__code__,env,argdefs=original.Observer.__init__.__defaults__)
        save=FunctionType(original.Observer.save.__code__,env,argdefs=original.Observer.save.__defaults__)
    observers=[]
    class Commands(GrowingCommands):
        def readline(self,*args):
            for observer in observers:save(ROOT/'live_observer_progress.json',dict(rows=observer.rows,errors=observer.errors,
                callbacks=observer.header[2],mismatches=observer.header[3],pending={str(k):v for k,v in observer.pending.items()},live_not_terminal_proof=True))
            return super().readline(*args)
    class Proxy:
        def __getattr__(self,name):return getattr(ct,name)
        def CDLL(self,path,*args,**kwargs):
            core=ct.CDLL(path,*args,**kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                observer=Observer(core,CAP/'observer');observer.install();observers.append(observer);old_run=core.retro_run;old_run.restype=None
                def run():observer.next_frame();old_run()
                core.retro_run=run
            return core
    save(ROOT/'run_plan.json',dict(candidate=str(ROM),candidate_sha256=digest,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),
        journal=str(journal),initial_pause=31000,existing_isolated_system_unlock_save=str(donor),save_sha256=sha(donor.read_bytes()),
        fixture_manifest=str(fixture_path),fixture_manifest_sha256=sha(fixture_path.read_bytes()),earned_unlock_verified=False,
        no_savestate_or_story_location_RNG_funds_outcome_fixture=True,observer_sha256=sha(Path(original.__file__).read_bytes()),
        harness_sha256=sha(Path(harness.__file__).read_bytes()),runner_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    stream=Commands(journal);old_stdin=sys.stdin;sys.stdin=stream;old_ct=harness.ct;harness.ct=Proxy()
    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','100000','--inputs-json',str(inputs),
        '--battery-save',str(donor),'--allow-gallery-fixtures','--gallery-save-fixture-manifest',str(fixture_path),
        '--capture-every','999999','--capture-at',*map(str,prior['capture_frames']),'--pause-at','31000',
        '--dump-capture-ram','--dump-pause-ram','--dump-ram','--touchscreen']
    try:harness.main()
    finally:
        sys.stdin=old_stdin;harness.ct=old_ct;stream.close()
        for observer in observers:observer.close()
    for observer in observers:observer.save()
    assert sha(donor.read_bytes())==old['donor_sha256']
    save(ROOT/'terminal.json',dict(terminal=True,candidate_sha256=digest,frame=read(CAP/'capture_report.json')['frames'],
        observer_host_slots_restored=True,existing_isolated_system_unlock_only_no_earned_unlock_claim=True,
        no_savestate_or_story_location_RNG_funds_outcome_fixture=True,full_goal_complete=False))
