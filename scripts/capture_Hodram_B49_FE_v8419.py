"""Focused original FE-boundary snapshots; same fixture/input prefix, no repeated whole-flow test."""
import argparse,ctypes as ct,inspect,os,struct,sys,textwrap
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import observe_lil_modal_v1733 as original
from scripts.inspect_committed_gpu_v646 import CORE,CORE_SHA
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_FE_runs_v8419')
MODELS=Path('work/analysis/Hodram_B49_models_v8408/native_models.json')
FIXTURES=Path('work/analysis/Hodram_B49_tail_v8415/bounded_tail_fixtures.json')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--version',choices=['clean_Japanese','revised_English'],required=True);version=ap.parse_args().version
    root=ROOT/version;cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'Hodram_B49_FE_geometry_{version}_v8419';assert not root.exists() and not cap.exists()
    fixture=next(f for f in read(FIXTURES)['fixtures'] if f['source_block']==49 and f['version']==version);rom=Path(fixture['research_ROM']);assert sha(rom.read_bytes())==fixture['research_ROM_sha256'];arm=NdsImage.open(rom).read_file('/__arm9__.bin')
    full=Path('work/analysis/Hodram_B49_tail_runs_v8416')/f'route1_{version}_accept';terminal=read(full/'terminal.json');fullplan=read(full/'run_plan.json');report=read(terminal['report'])
    assert terminal['terminal'] and report['frames']==10001 and report['ROM_sha256']==fixture['research_ROM_sha256']
    models=read(MODELS);body=next(m for m in models['native_models'][version] if m['source_selector']==254)['expanded_native_hex']
    contract=read('work/analysis/script_sources_v733/source_contract.json');core=CORE.read_bytes();assert sha(core)==CORE_SHA==contract['core_sha256'];preferred=contract['interpreter_table']['source_VA']-contract['interpreter_table']['RVA'];targets=[]
    for at,name in [(0x548A8,'modal_entry'),(0x54924,'modal_paint')]:
        word=struct.unpack_from('<I',arm,at)[0];index=((word>>16)&0xFF0)|((word>>4)&15);address=struct.unpack_from('<Q',core,contract['interpreter_table']['file_offset']+index*8)[0];targets.append(dict(PC=0x02000000+at,word=word,name=name,instruction_index=index,handler_RVA=address-preferred))
    contract['targets']=targets
    adapter=checked_text(textwrap.dedent(inspect.getsource(original.Observer.__init__)),{
        "    packet=read('work/analysis/lil_lessons_source_v1717/complete_lesson_source_context.json')\n    self.FE_bodies={r['current_native_macro_output_hex'] for block in packet['blocks'] if block['block']==120 for r in block['records'] if r['source_presentation_prefix_hex']=='fe'}":"    self.FE_bodies={FE_BODY_HEX}\n    self.snapshot_count=0",
        "if target['name']=='modal_paint' and body.hex() in self.FE_bodies:":"if target['name']=='modal_paint' and body.hex() in self.FE_bodies and not self.snapshot_count:\n                self.snapshot_count+=1",
    })
    env={**original.__dict__,'FE_BODY_HEX':body};exec(compile(adapter,__file__+'::source-qualified-one-FE-boundary','exec'),env)
    class Observer(original.Observer):
        __init__=env['__init__']
    root.mkdir(parents=True);contractpath=root/'source_contract.json';save(contractpath,contract);inputs=root/'same_ordinary_input_prefix.json';schedule=[e for e in report['scripted_input_schedule'] if e['start']<=4930];save(inputs,schedule)
    assert schedule==[e for e in read(fullplan['inputs']) if e['start']<=4930]
    plan=root/'run_plan.json';save(plan,dict(research_ROM=str(rom),research_ROM_sha256=fixture['research_ROM_sha256'],version=version,PID=os.getpid(),frames=4931,input=str(inputs),input_sha256=sha(inputs.read_bytes()),same_prefix_of_completed_scene_run=str(full/'run_plan.json'),same_prefix_of_completed_scene_run_sha256=sha((full/'run_plan.json').read_bytes()),
        source_owned_FE_boundary_adapter=adapter,exact_expanded_FE_body_hex=body,read_only_PC_filters=targets,observer_source=str(Path(original.__file__)),observer_source_sha256=sha(Path(original.__file__).read_bytes()),
        source_contract=str(contractpath),source_contract_sha256=sha(contractpath.read_bytes()),capture_folder=str(cap),focused_descriptor_palette_andmain_RAM_evidence_not_new_whole_exchange_orpossession_orordinary_optional_activation=True,no_savestate_RAM_conditions_roster_funds_RNG_result_orcontroller_retiming=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    observers=[]
    class Proxy:
        def __getattr__(self,name):return getattr(ct,name)
        def CDLL(self,path,*args,**kwargs):
            lib=ct.CDLL(path,*args,**kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                observer=Observer(lib,cap/'modal_observer',contractpath);observer.install();observers.append(observer);old=lib.retro_run;old.restype=None
                def run():observer.next_frame();old()
                lib.retro_run=run
            return lib
    oldct=harness.ct;harness.ct=Proxy();sys.argv=['headless_desmume_v193.py','--rom',str(rom),'--out',str(cap),'--frames','4931','--inputs-json',str(inputs),'--capture-every','999999','--capture-at','4870','4930','--dump-capture-ram','--dump-ram']
    try:harness.main()
    finally:
        harness.ct=oldct
        for observer in observers:observer.close()
    for observer in observers:observer.save()
    assert len(observers)==1 and observers[0].snapshot_count==1 and not observers[0].errors
    rp=cap/'capture_report.json';op=cap/'modal_observer/actual_modal_contexts.json';result=read(rp);observed=read(op)
    assert result['frames']==4931 and result['cold_boot'] and not result['savestate_loaded'] and not result.get('battery_save_preloaded') and not result['callback_errors'] and not any(v for k,v in result.items() if k.startswith('synthetic_'))
    assert observed['all_host_slots_restored_and_core_file_exact'] and not observed['errors'] and not observed['mismatches']
    save(root/'terminal.json',dict(terminal=True,version=version,frames=4931,report=str(rp),report_sha256=sha(rp.read_bytes()),observer=str(op),observer_sha256=sha(op.read_bytes()),run_plan=str(plan),run_plan_sha256=sha(plan.read_bytes()),exactly_one_complete_original_FE_paint_CPU_WRAM_DTCM_ITCM_snapshot=True,all_callbacks_readonly_andhost_slots_restored=True,
        original_whole_scene_runs_not_repeated=True,actual_descriptor_palette_andpixel_binding_pending=True,new_credit=0,full_goal_complete=False))
    print(version+' focused4931-frameFEboundary capture:one fullpaint snapshot/two hold RAM exports;readonly callback/core restoration pass.Binding pending.')
