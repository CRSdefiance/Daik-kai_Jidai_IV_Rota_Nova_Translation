"""Fixture-free current complete Hodram opening context; original controls unchanged."""
import ctypes as ct
import json
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

ROOT=Path('work/analysis/hodram_opening_context_v2018')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/hodram_opening_context_v2018_V2013')
ROM=Path('out/all_routes_combined_v2013_candidate.nds')

if __name__=='__main__':
    assert not ROOT.exists()and not CAP.exists()
    digest=sha(ROM.read_bytes());assert digest==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    assert read('work/analysis/lil_Stockholm_context_run_v1851/terminal.json')['frame']==62850
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin');contract=Path('work/analysis/script_sources_v733/source_contract.json')
    for target in read(contract)['targets']:
        assert struct.unpack_from('<I',arm,target['PC']-0x02000000)[0]==target['word']
    ROOT.mkdir(parents=True);(ROOT/'source_contract.json').write_bytes(contract.read_bytes())
    prior=read('work/analysis/lil_lessons_revised_v1741/run_plan.json')
    commands=[r for r in read(prior['inputs'])if r['start']<=2200 and r['start']!=1600]
    assert [r['start']for r in commands]==[1000,1200,1450,1800,2200]
    assert commands[2]['buttons']==['RIGHT']
    inputs=ROOT/'ordinary_Hodram_NewGame_inputs.json';save(inputs,commands)
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
    class Proxy:
        def __getattr__(self,name):return getattr(ct,name)
        def CDLL(self,path,*args,**kwargs):
            core=ct.CDLL(path,*args,**kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                observer=Observer(core,CAP/'observer');observer.install();observers.append(observer)
                old=core.retro_run;old.restype=None
                def run():observer.next_frame();old()
                core.retro_run=run
            return core
    save(ROOT/'run_plan.json',{'candidate':str(ROM),'candidate_sha256':digest,'inputs':str(inputs),
        'inputs_sha256':sha(inputs.read_bytes()),'journal':str(journal),'initial_pause':4000,
        'ordinary_NewGame_one_RIGHT_selects_Hodram':True,'no_save_savestate_or_fixtures':True,
        'observer_sha256':sha(Path(original.__file__).read_bytes()),'harness_sha256':sha(Path(harness.__file__).read_bytes()),
        'runner_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    stream=Commands(journal);old_stdin=sys.stdin;sys.stdin=stream;old_ct=harness.ct;harness.ct=Proxy()
    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','100000',
        '--inputs-json',str(inputs),'--capture-every','999999','--capture-at','4000','--pause-at','4000',
        '--dump-capture-ram','--dump-pause-ram','--dump-ram','--touchscreen']
    try:harness.main()
    finally:
        sys.stdin=old_stdin;harness.ct=old_ct;stream.close()
        for observer in observers:observer.close()
    for observer in observers:observer.save()
    save(ROOT/'terminal.json',{'terminal':True,'candidate_sha256':digest,'frame':read(CAP/'capture_report.json')['frames'],
        'observer_host_slots_restored':True,'no_save_savestate_or_fixtures':True,'full_goal_complete':False})
