"""Ordinary no-save revised opening with original command entry/return observation."""
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
from scripts.prepare_lil_opening_research_v1704 import ROM
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_opening_trace_v1706')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_opening_trace_v1706_RESEARCH_ONLY')


if __name__=='__main__':
    assert not ROOT.exists() and not CAP.exists()
    receipt=read('work/analysis/lil_opening_research_v1704/research_image_receipt.json')
    assert sha(ROM.read_bytes())==receipt['research_ROM_sha256']
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin');source=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x24048:0x24118]==source[0x24048:0x24118]
    contract=Path('work/analysis/script_sources_v733/source_contract.json')
    cfg=read(contract)
    for target in cfg['targets']:assert struct.unpack_from('<I',arm,target['PC']-0x02000000)[0]==target['word']
    inputs=Path('work/analysis/movie_viewport_v303/lil_start_inputs.json')
    assert sha(inputs.read_bytes())=='097df0c69d30d00532373b2b8b7fe2f5969ba581a0bd35e27074c22749631541'
    ROOT.mkdir(parents=True);(ROOT/'source_contract.json').write_bytes(contract.read_bytes())
    journal=ROOT/'navigation.jsonl';journal.write_text('',encoding='utf-8')
    env={**original.__dict__,'ROM':ROM,'ROOT':ROOT}
    class Observer(original.Observer):
        __init__=FunctionType(original.Observer.__init__.__code__,env,argdefs=original.Observer.__init__.__defaults__)
        save=FunctionType(original.Observer.save.__code__,env,argdefs=original.Observer.save.__defaults__)
    observers=[]
    class Commands(GrowingCommands):
        def readline(self,*args):
            for observer in observers:
                save(ROOT/'live_observer_progress.json',{'rows':observer.rows,'errors':observer.errors,
                    'callbacks':observer.header[2],'mismatches':observer.header[3],
                    'pending':{str(k):v for k,v in observer.pending.items()},'live_not_terminal_proof':True})
            return super().readline(*args)
    class CtypesProxy:
        def __getattr__(self,name):return getattr(ct,name)
        def CDLL(self,path,*extra,**kwargs):
            core=ct.CDLL(path,*extra,**kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                observer=Observer(core,CAP/'observer');observer.install();observers.append(observer)
                old_run=core.retro_run;old_run.restype=None
                def run():observer.next_frame();old_run()
                core.retro_run=run
            return core
    save(ROOT/'run_plan.json',{'research_ROM':str(ROM),'research_ROM_sha256':sha(ROM.read_bytes()),'capture_folder':str(CAP),
        'original_inputs':str(inputs),'inputs_sha256':sha(inputs.read_bytes()),'no_save_savestate_or_gameplay_fixtures':True,
        'original_readonly_observer':str(Path(original.__file__)),'original_observer_sha256':sha(Path(original.__file__).read_bytes()),
        'source_contract_sha256':sha(contract.read_bytes()),'only_ROM_ROOT_globals_rebound_for_current_source':True,
        'runner_sha256':sha(Path(__file__).read_bytes()),'harness_sha256':sha(Path(harness.__file__).read_bytes()),
        'not_a_registered_candidate_or_user_handoff':True,'full_goal_complete':False})
    stream=Commands(journal);old_stdin=sys.stdin;sys.stdin=stream;old_ct=harness.ct;harness.ct=CtypesProxy()
    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','100000',
        '--inputs-json',str(inputs),'--capture-every','999999','--capture-at','4000','6000','--pause-at','6000',
        '--dump-capture-ram','--dump-pause-ram','--dump-ram']
    try:harness.main()
    finally:
        sys.stdin=old_stdin;harness.ct=old_ct;stream.close()
        for observer in observers:observer.close()
    for observer in observers:observer.save()
    save(ROOT/'terminal.json',{'terminal':True,'research_ROM_sha256':sha(ROM.read_bytes()),'observer_instances':len(observers),
        'observer_host_slots_restored':True,'no_gameplay_fixture_save_or_ROM_runtime_edit':True})
