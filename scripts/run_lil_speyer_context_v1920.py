"""Registered V1909 replay to London; append-only targeted Speyer context run."""
import ctypes as ct
import json
import struct
import sys
from pathlib import Path
from types import FunctionType
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts import observe_script_sources_v733 as original
from scripts.run_activity_special_live_v988 import GrowingCommands
from scripts import native_battle_fixture_v620 as fixture_dispatch
from scripts.native_lil_london_location_v1883 import apply_fixture
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v1909_candidate.nds')
ROOT = Path('work/analysis/lil_Speyer_context_run_v1920')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Speyer_context_run_v1920_RESEARCH_ONLY')

if __name__ == '__main__':
    assert not ROOT.exists() and not CAP.exists()
    source_run = Path('work/analysis/lil_London_revised_run_v1903')
    assert read(source_run/'terminal.json')['frame'] == 86310
    plan = read(source_run/'run_plan.json')
    digest = sha(ROM.read_bytes())
    assert digest == plan['research_ROM_sha256'] == read('work/analysis/lil_London_release_v1908b/registered_release_verification.json')['candidate_sha256']
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    contract = Path('work/analysis/script_sources_v733/source_contract.json')
    for target in read(contract)['targets']:
        assert struct.unpack_from('<I',arm,target['PC']-0x02000000)[0] == target['word']
    commands = [json.loads(line) for line in (source_run/'navigation.jsonl').read_text().splitlines() if line]
    commands = [r for r in commands if not r.get('stop') and r.get('until',999999) <= 86310]
    assert commands[-1]['until'] == 86310
    ROOT.mkdir(parents=True)
    (ROOT/'source_contract.json').write_bytes(contract.read_bytes())
    inputs = ROOT/'ordinary_replay_inputs.json'
    save(inputs,read(plan['inputs']))
    journal = ROOT/'navigation.jsonl'
    journal.write_text(''.join(json.dumps(r)+'\n' for r in commands),encoding='utf-8')
    env = {**original.__dict__,'ROM':ROM,'ROOT':ROOT}
    class Observer(original.Observer):
        __init__ = FunctionType(original.Observer.__init__.__code__,env,argdefs=original.Observer.__init__.__defaults__)
        save = FunctionType(original.Observer.save.__code__,env,argdefs=original.Observer.save.__defaults__)
    observers = []
    class Commands(GrowingCommands):
        def readline(self,*args):
            for observer in observers:
                save(ROOT/'live_observer_progress.json',dict(rows=observer.rows,errors=observer.errors,
                    callbacks=observer.header[2],mismatches=observer.header[3],
                    pending={str(k):v for k,v in observer.pending.items()},live_not_terminal_proof=True))
            return super().readline(*args)
    class Proxy:
        def __getattr__(self,name):return getattr(ct,name)
        def CDLL(self,path,*args,**kwargs):
            core = ct.CDLL(path,*args,**kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                observer = Observer(core,CAP/'observer')
                observer.install()
                observers.append(observer)
                old = core.retro_run
                old.restype = None
                def run():observer.next_frame();old()
                core.retro_run = run
            return core
    save(ROOT/'run_plan.json',dict(research_ROM=str(ROM),research_ROM_sha256=digest,registered_profile='all-routes-unified-v1909',
        inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),append_only_navigation=str(journal),
        initial_pause_frame=29930,replay_target_frame=86310,no_preloaded_save_or_savestate=True,
        inherited_three_coordinate_only_fixture_paths=plan['declared_each16_byte_location_only_fixtures'],
        future_Speyer_access_fixtures_must_be_separately_source_bound_and_disclosed=True,
        replay_source_journal=str(source_run/'navigation.jsonl'),replay_source_journal_sha256=sha((source_run/'navigation.jsonl').read_bytes()),
        observer_sha256=sha(Path(original.__file__).read_bytes()),harness_sha256=sha(Path(harness.__file__).read_bytes()),
        runner_sha256=sha(Path(__file__).read_bytes()),not_a_full_route_or_earned_travel_test=True,full_goal_complete=False))
    stream = Commands(journal)
    old_stdin,old_ct,old_fixture = sys.stdin,harness.ct,fixture_dispatch.apply_fixture
    sys.stdin,harness.ct,fixture_dispatch.apply_fixture = stream,Proxy(),apply_fixture
    sys.argv = ['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','140000',
        '--inputs-json',str(inputs),'--capture-every','999999','--capture-at','29930','--pause-at','29930',
        '--dump-capture-ram','--dump-pause-ram','--dump-ram','--touchscreen','--allow-battle-fixtures']
    try:harness.main()
    finally:
        sys.stdin,harness.ct,fixture_dispatch.apply_fixture = old_stdin,old_ct,old_fixture
        stream.close()
        for observer in observers:observer.close()
    for observer in observers:observer.save()
    save(ROOT/'terminal.json',dict(terminal=True,research_ROM_sha256=digest,
        frame=read(CAP/'capture_report.json')['frames'],observer_host_slots_restored=True,full_goal_complete=False))
