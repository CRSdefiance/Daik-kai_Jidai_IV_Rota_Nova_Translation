"""Paired clean/revised Hodram whole-script entry fixtures;ordinary identical inputs andreadonly traces."""
import argparse,ctypes as ct,os,struct,sys
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import observe_lil_B180_v4810 as original
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B54_B60_scene_runs_v8816')
FIXTURES=Path('work/analysis/Hodram_B54_B60_fixtures_v8815/twelve_whole_scripts.json')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--route',type=int,choices=[1],required=True);ap.add_argument('--block',type=int,choices=[54,57,58,59,60],required=True);ap.add_argument('--version',choices=['clean_Japanese','revised_English'],required=True);args=ap.parse_args()
    route,version,block=args.route,args.version,args.block;frames={54:6001,57:9001,58:16001,59:10001,60:10001}[block];selected=next(f for f in read(FIXTURES)['fixtures'] if f['route']==route and f['version']==version and f['source_block']==block)
    folder=ROOT/f'route{route}_B{block}_{version}';cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'Hodram_B{block}_route{route}_{version}_v8816'
    assert not folder.exists() and not cap.exists();rom=Path(selected['research_ROM']);assert sha(rom.read_bytes())==selected['research_ROM_sha256']
    contract=Path('work/analysis/script_sources_v733/source_contract.json');arm=NdsImage.open(rom).read_file('/__arm9__.bin')
    for target in read(contract)['targets']:assert struct.unpack_from('<I',arm,target['PC']-0x02000000)[0]==target['word']
    source_inputs=Path('work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json')
    base=read(source_inputs);assert sum(r['buttons']==['RIGHT'] for r in base)==route and max(r['start'] for r in base)<=2200
    folder.mkdir(parents=True);(folder/'source_contract.json').write_bytes(contract.read_bytes());inputs=folder/'identical_ordinary_A_inputs.json'
    save(inputs,base+[dict(start=frame,duration=5,buttons=['A']) for frame in range(4000,frames-480,240)])
    env={**original.__dict__,'ROM':rom,'ROOT':folder}
    class Observer(original.Observer):
        __init__=FunctionType(original.Observer.__init__.__code__,env,argdefs=original.Observer.__init__.__defaults__)
        save=FunctionType(original.Observer.save.__code__,env,argdefs=original.Observer.save.__defaults__)
    observers=[]
    class Proxy:
        def __getattr__(self,name):return getattr(ct,name)
        def CDLL(self,path,*a,**kw):
            core=ct.CDLL(path,*a,**kw)
            if str(path).lower().endswith('desmume_libretro.dll'):
                o=Observer(core,cap/'observer');o.install();observers.append(o);old=core.retro_run;old.restype=None
                def run():o.next_frame();old()
                core.retro_run=run
            return core
    captures=sorted(set(range(2350,frames,60))|{frames-1})
    plan=folder/'run_plan.json'
    save(plan,dict(research_ROM=str(rom),research_ROM_sha256=selected['research_ROM_sha256'],route=route,version=version,capture_folder=str(cap),PID=os.getpid(),frames=frames,captures=captures,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),source_inputs=str(source_inputs),source_inputs_sha256=sha(source_inputs.read_bytes()),fixture_manifest=str(FIXTURES),fixture_manifest_sha256=sha(FIXTURES.read_bytes()),displayed_original_file=selected['source_file'],displayed_original_block=selected['source_block'],entry_opening_block=selected['fixture_block'],original_exchange_commands=len(selected['all_original_exchange_commands']),original_exchange_speeches=len(selected['original_text_records']),original_initializer_commands=len(selected['original_opening_prelude_commands']),observer=str(Path(original.__file__)),observer_sha256=sha(Path(original.__file__).read_bytes()),source_contract_sha256=sha(contract.read_bytes()),disclosed_ROM_entry_fixture_not_natural_optional_activation_ororiginal_location=True,no_battery_savestate_RAM_code_role_roster_funds_RNG_condition_orresult_forcing=True,no_controller_retiming_between_clean_Japanese_andrevised_English=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    oldct=harness.ct;harness.ct=Proxy();sys.argv=['headless_desmume_v193.py','--rom',str(rom),'--out',str(cap),'--frames',str(frames),'--inputs-json',str(inputs),'--capture-every','999999','--capture-at',*map(str,captures),'--dump-ram']
    try:harness.main()
    finally:
        harness.ct=oldct
        for o in observers:o.close()
    for o in observers:o.save()
    rp=cap/'capture_report.json';report=read(rp)
    assert report['frames']==frames and report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
    assert len(observers)==1 and not observers[0].errors and not observers[0].header[3]
    op=cap/'observer/commands.json';assert read(op)['all_host_slots_restored_and_core_file_exact']
    save(folder/'terminal.json',dict(terminal=True,route=route,source_block=block,version=version,frames=frames,research_ROM_sha256=selected['research_ROM_sha256'],report=str(rp),report_sha256=sha(rp.read_bytes()),observer=str(op),observer_sha256=sha(op.read_bytes()),run_plan=str(plan),run_plan_sha256=sha(plan.read_bytes()),all_callbacks_readonly_andhost_slots_restored=True,complete_body_header_palette_transition_return_andlate_state_analysis_pending=True,not_natural_optional_activation_location_earned_progress_full_route_orhardware_coverage=True,new_credit=0,full_goal_complete=False))
    print(f'route{route} B{block} {version}:{frames}-frame fixture capture terminal;body/header/return/transition analysis pending;zero credit.',flush=True)
