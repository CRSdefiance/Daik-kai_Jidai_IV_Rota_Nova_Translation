"""Observe the actual current Maria opening prelude with the exact existing system-only unlock."""
import argparse,ctypes as ct,os,struct,sys
from pathlib import Path
from scripts.maria_existing_unlock_contract_v7680 import validate_fixture,validate_capture
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import observe_script_sources_v733 as original
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_original_initializer_v7701')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--route',type=int,choices=[3],required=True);route=ap.parse_args().route
    folder=ROOT/f'route{route}';cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'Maria_B207_original_initializer_route{route}_v7701'
    assert not folder.exists() and not cap.exists()
    verified=Path('work/analysis/editorial_handoff_verification_v7693b/verified_handoff.json');v=read(verified);rom=Path(v['candidate'])
    assert sha(rom.read_bytes())==v['candidate_sha256'] and read(rom.with_suffix('.manifest.json'))['profile']=='all-routes-unified-v7660'
    contract=Path('work/analysis/script_sources_v733/source_contract.json');arm=NdsImage.open(rom).read_file('/__arm9__.bin')
    for target in read(contract)['targets']:assert struct.unpack_from('<I',arm,target['PC']-0x02000000)[0]==target['word']
    inp=Path('work/analysis/maria_B207_route_run_v7680/ordinary_Maria_NewGame_prefix.json');fp=Path('work/analysis/maria_B207_route_run_v7680/existing_system_unlock_manifest.json');fixture=validate_fixture(fp)
    assert sum(r['buttons']==['RIGHT'] for r in read(inp))==route
    folder.mkdir(parents=True);(folder/'source_contract.json').write_bytes(contract.read_bytes())
    env={**original.__dict__,'ROM':rom,'ROOT':folder}
    class Observer(original.Observer):
        __init__=FunctionType(original.Observer.__init__.__code__,env,argdefs=original.Observer.__init__.__defaults__)
        save=FunctionType(original.Observer.save.__code__,env,argdefs=original.Observer.save.__defaults__)
    observers=[]
    class Proxy:
        def __getattr__(self,name):return getattr(ct,name)
        def CDLL(self,path,*args,**kwargs):
            core=ct.CDLL(path,*args,**kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                observer=Observer(core,cap/'observer');observer.install();observers.append(observer)
                old=core.retro_run;old.restype=None
                def run():observer.next_frame();old()
                core.retro_run=run
            return core
    plan=folder/'run_plan.json'
    save(plan,dict(candidate=str(rom),candidate_sha256=v['candidate_sha256'],route=route,route_identity={3:'Maria'}[route],frames=6001,PID=os.getpid(),capture_folder=str(cap),inputs=str(inp),inputs_sha256=sha(inp.read_bytes()),observer=str(Path(original.__file__)),observer_sha256=sha(Path(original.__file__).read_bytes()),source_contract_sha256=sha(contract.read_bytes()),existing_system_only_unlock_manifest=str(fp),existing_system_only_unlock_manifest_sha256=sha(fp.read_bytes()),earned_unlock_verified=False,no_savestate_ROM_RAM_roster_role_funds_RNG_event_orresult_fixture=True,purpose='Bind actual original captain-specific opening initializer commands before any disclosed optional-scene fixture; earlier no-observer NewGames supplied no command trace.',not_optional_event_activation_orfull_route_coverage=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    oldct=harness.ct;harness.ct=Proxy();sys.argv=['headless_desmume_v193.py','--rom',str(rom),'--out',str(cap),'--frames','6001','--inputs-json',str(inp),'--battery-save',fixture['fixture_save'],'--allow-gallery-fixtures','--gallery-save-fixture-manifest',str(fp),'--touchscreen','--capture-every','999999','--capture-at','4000','5000','6000']
    try:harness.main()
    finally:
        harness.ct=oldct
        for o in observers:o.close()
    for o in observers:o.save()
    report=cap/'capture_report.json';r=read(report)
    assert r['frames']==6001;validate_capture(r)
    assert len(observers)==1 and not observers[0].errors and not observers[0].header[3]
    save(folder/'terminal.json',dict(terminal=True,candidate_sha256=v['candidate_sha256'],route=route,frames=6001,report=str(report),report_sha256=sha(report.read_bytes()),run_plan=str(plan),run_plan_sha256=sha(plan.read_bytes()),observer_host_slots_restored=True,complete_original_initializer_trace_analysis_pending=True,no_optional_papal_scene_ornew_editorial_credit=True,full_goal_complete=False))
    print(f'route{route}: ordinary current NewGame initializer trace terminal;host callbacks restored. Exact prelude analysis pending.',flush=True)
