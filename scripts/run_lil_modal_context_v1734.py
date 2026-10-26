"""Repeat the terminal ordinary schedule and read actual modal layout fields."""
import ctypes as ct
import sys
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.observe_lil_modal_v1733 import Observer
from scripts.inspect_committed_gpu_v646 import CORE,CORE_SHA
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_modal_context_v1734')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_modal_context_v1734_1711')
ROM=Path('out/all_routes_combined_v1711_candidate.nds')


if __name__=='__main__':
    assert not ROOT.exists() and not CAP.exists()
    digest=sha(ROM.read_bytes());assert digest==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    previous=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_lesson_context_v1723_1711/capture_report.json')
    report=read(previous);assert report['ROM_sha256']==digest and report['frames']==29930
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin');contract=read('work/analysis/script_sources_v733/source_contract.json')
    core=CORE.read_bytes();assert sha(core)==CORE_SHA==contract['core_sha256']
    preferred=contract['interpreter_table']['source_VA']-contract['interpreter_table']['RVA']
    targets=[]
    for at,name in [(0x548A8,'modal_entry'),(0x54924,'modal_paint')]:
        word=struct.unpack_from('<I',arm,at)[0];index=((word>>16)&0xFF0)|((word>>4)&15)
        address=struct.unpack_from('<Q',core,contract['interpreter_table']['file_offset']+index*8)[0]
        targets.append({'PC':0x02000000+at,'word':word,'name':name,'instruction_index':index,'handler_RVA':address-preferred})
    contract['targets']=targets
    ROOT.mkdir(parents=True);contract_path=ROOT/'source_contract.json';save(contract_path,contract)
    inputs=ROOT/'ordinary_replay_inputs.json';save(inputs,report['scripted_input_schedule'])
    save(ROOT/'run_plan.json',{'candidate':str(ROM),'candidate_sha256':digest,'input':str(inputs),'input_sha256':sha(inputs.read_bytes()),
        'original_terminal_report':str(previous),'original_report_sha256':sha(previous.read_bytes()),
        'no_preloaded_battery_save_savestate_gameplay_fixture_or_ROM_edit':True,
        'read_only_PC_filters':targets,'source_contract':str(contract_path),'source_contract_sha256':sha(contract_path.read_bytes()),
        'harness_sha256':sha(Path(harness.__file__).read_bytes()),'runner_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    observers=[]
    class Proxy:
        def __getattr__(self,name):return getattr(ct,name)
        def CDLL(self,path,*args,**kwargs):
            lib=ct.CDLL(path,*args,**kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                observer=Observer(lib,CAP/'modal_observer',contract_path);observer.install();observers.append(observer)
                old=lib.retro_run;old.restype=None
                def run():observer.next_frame();old()
                lib.retro_run=run
            return lib
    old_ct=harness.ct;harness.ct=Proxy()
    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','29930',
        '--inputs-json',str(inputs),'--capture-every','999999','--capture-at','22930','25330','25630','27530','27830','28130','29330','29930',
        '--dump-capture-ram','--dump-ram']
    try:harness.main()
    finally:
        harness.ct=old_ct
        for observer in observers:observer.close()
    for observer in observers:observer.save()
    save(ROOT/'terminal.json',{'terminal':True,'candidate_sha256':digest,'frames':29930,'observer_instances':len(observers),
        'all_host_slots_restored_core_file_exact':True,'no_gameplay_fixture_ROM_or_save_input':True})
