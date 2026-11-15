"""Full B46 entry fixtures, ordinary choices and disjoint read-only command/caption observers."""
import argparse,ctypes as ct,inspect,os,struct,sys
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import observe_lil_B180_v4810 as original
from scripts import run_lil_B212_menu_owner_v6630 as owner_module
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_scene_runs_v7945')
FIXTURES=Path('work/analysis/Rafael_B46_scene_fixtures_v7944/two_complete_source_English_original_Rafael_prelude_fixtures.json')
MENU_SNAPSHOT_FRAMES=[4810,4870,4930]
if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--route',type=int,choices=[0],required=True)
    ap.add_argument('--version',choices=['clean_Japanese','English'],required=True)
    ap.add_argument('--choice',choices=['accept','decline'],required=True)
    ap.add_argument('--down-frame',type=int)
    args=ap.parse_args();route,version,choice=args.route,args.version,args.choice
    assert (choice=='accept' and args.down_frame is None) or (choice=='decline' and args.down_frame is not None and 4725<=args.down_frame<4960)
    selected=next(f for f in read(FIXTURES)['fixtures'] if f['route']==route and f['version']==version)
    folder=ROOT/f'route{route}_{version}_{choice}'
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'Rafael_B46_route{route}_{version}_{choice}_v7945'
    assert not folder.exists() and not cap.exists()
    rom=Path(selected['research_ROM']);assert sha(rom.read_bytes())==selected['research_ROM_sha256']
    arm=NdsImage.open(rom).read_file('/__arm9__.bin')
    contract=Path('work/analysis/script_sources_v733/source_contract.json');contract_doc=read(contract)
    for target in contract_doc['targets']:assert struct.unpack_from('<I',arm,target['PC']-0x02000000)[0]==target['word']
    menu_word=struct.unpack_from('<I',arm,0xD5340)[0];assert menu_word==0xE92D4030
    menu_index=((menu_word>>16)&0xFF0)|((menu_word>>4)&15)
    assert menu_index not in {t['instruction_index'] for t in contract_doc['targets']}
    source_inputs=Path(f'work/analysis/papal_trade_route_runs_v7625/route{route}/ordinary_NewGame_inputs.json')
    base=read(source_inputs);assert sum(r['buttons']==['RIGHT'] for r in base)==route and max(r['start'] for r in base)<=2200
    folder.mkdir(parents=True);(folder/'source_contract.json').write_bytes(contract.read_bytes())
    inputs=folder/'ordinary_inputs.json';schedule=base+[dict(start=f,duration=5,buttons=['A']) for f in range(4000,15501,240)]
    if choice=='decline':schedule.append(dict(start=args.down_frame,duration=5,buttons=['DOWN']))
    save(inputs,sorted(schedule,key=lambda r:r['start']))
    env={**original.__dict__,'ROM':rom,'ROOT':folder}
    class Observer(original.Observer):
        __init__=FunctionType(original.Observer.__init__.__code__,env,argdefs=original.Observer.__init__.__defaults__)
        save=FunctionType(original.Observer.save.__code__,env,argdefs=original.Observer.save.__defaults__)
    owner_dir=folder/'menu_owner';owner_dir.mkdir()
    labels={r['label'].encode('cp932') for r in selected['original_menu_records']}
    assert len(labels)==2
    owner_adapter=checked_text(inspect.getsource(owner_module.OwnerObserver),{
        'if frame<2900 or len(self.rows)>=40:return':'if frame<2300 or len(self.rows)>=40:return',
        "text in [b'Yes',b'No',b'Zhao Yun',b'Guan Yu',b'Zhuge Liang']":"text in MENU_LABELS",
        "text=text.decode('ascii')":"text=text.decode('cp932')",
    })
    owner_env={**owner_module.__dict__,'ROOT':owner_dir,'MENU_LABELS':labels,'__file__':__file__}
    exec(compile(owner_adapter,__file__+'::source-owned-two-label-readonly-observer','exec'),owner_env)
    observers=[];owners=[];snapshots=[]
    def snapshot(o,frame):
        cpu=ct.string_at(o.cpu,128);raw=ct.string_at(o.wram,0x400000)
        dtcm=o.image.read(o.dtcm,0x4000);itcm=o.image.read(o.itcm,0x8000);base_raw=o.image.read(o.dtcm_base,4)
        paths={}
        for key,data in [('CPU',cpu),('WRAM',raw),('DTCM',dtcm),('ITCM',itcm)]:
            p=folder/f'menu_frame{frame}_{key}.bin';assert not p.exists();p.write_bytes(data)
            paths[key]=dict(path=str(p),sha256=sha(data),bytes=len(data))
        assert ct.string_at(o.cpu,128)==cpu and ct.string_at(o.wram,0x400000)==raw
        assert o.image.read(o.dtcm,0x4000)==dtcm and o.image.read(o.itcm,0x8000)==itcm and o.image.read(o.dtcm_base,4)==base_raw
        snapshots.append(dict(frame=frame,files=paths,DTCM_base=struct.unpack('<I',base_raw)[0],all_CPU_WRAM_DTCM_ITCM_andconfiguration_exact_before_after_readonly_export=True))
    class Proxy:
        def __getattr__(self,name):return getattr(ct,name)
        def CDLL(self,path,*a,**kw):
            core=ct.CDLL(path,*a,**kw)
            if str(path).lower().endswith('desmume_libretro.dll'):
                o=Observer(core,cap/'observer');o.install();observers.append(o)
                m=owner_env['OwnerObserver'](core,arm);owners.append(m)
                assert m.slot not in {r['slot'] for r in o.slots}
                old=core.retro_run;old.restype=None
                def run():
                    o.next_frame();m.next_frame();old()
                    assert o.header[0]==m.header[0]
                    if m.header[0] in MENU_SNAPSHOT_FRAMES:snapshot(m,int(m.header[0]))
                core.retro_run=run
            return core
    captures=sorted(set(range(2350,16001,60))|{16000,*MENU_SNAPSHOT_FRAMES})
    plan=folder/'run_plan.json'
    save(plan,dict(research_ROM=str(rom),research_ROM_sha256=selected['research_ROM_sha256'],route=route,version=version,choice=choice,DOWN_frame=args.down_frame,
        capture_folder=str(cap),PID=os.getpid(),frames=16001,captures=captures,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),
        source_inputs=str(source_inputs),source_inputs_sha256=sha(source_inputs.read_bytes()),fixture_manifest=str(FIXTURES),fixture_manifest_sha256=sha(FIXTURES.read_bytes()),
        displayed_original_file=selected['source_file'],displayed_original_block=46,entry_opening_block=44,
        original_exchange_commands=37,original_exchange_stored_speeches=24,original_menu_choices=2,original_initializer_commands=10,
        primary_observer=str(Path(original.__file__)),primary_observer_sha256=sha(Path(original.__file__).read_bytes()),
        menu_observer_source=str(Path(owner_module.__file__)),menu_observer_source_sha256=sha(Path(owner_module.__file__).read_bytes()),
        menu_observer_adapter=owner_adapter,menu_filter_label_hex=sorted(t.hex() for t in labels),menu_host_dispatch_index=menu_index,
        disjoint_command_andcaption_observer_host_slots_asserted=True,readonly_menu_snapshot_frames=MENU_SNAPSHOT_FRAMES,
        disclosed_ROM_entry_fixture_not_natural_activation_ororiginal_location=True,
        no_battery_savestate_RAM_code_role_roster_funds_RNG_condition_orresult_forcing=True,
        no_controller_retiming_between_source_andEnglish=True,actual_path_body_name_menu_transition_return_andlate_analysis_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    oldct=harness.ct;harness.ct=Proxy()
    sys.argv=['headless_desmume_v193.py','--rom',str(rom),'--out',str(cap),'--frames','16001','--inputs-json',str(inputs),
        '--capture-every','999999','--capture-at',*map(str,captures),'--dump-ram']
    try:harness.main()
    finally:
        harness.ct=oldct
        for m in owners:m.close()
        for o in observers:o.close()
    for o in observers:o.save()
    for m in owners:m.save()
    rp=cap/'capture_report.json';report=read(rp);op=cap/'observer/commands.json';mp=owner_dir/'actual_caption_context_view_and_backing.json'
    assert report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
    assert len(observers)==len(owners)==1 and not observers[0].errors and not owners[0].errors and not observers[0].header[3] and not owners[0].header[3]
    assert read(op)['all_host_slots_restored_and_core_file_exact'] and read(mp)['all_host_slots_restored_and_core_file_exact']
    assert [s['frame'] for s in snapshots]==MENU_SNAPSHOT_FRAMES
    sp=folder/'readonly_menu_snapshots.json';save(sp,snapshots)
    save(folder/'terminal.json',dict(terminal=True,route=route,version=version,choice=choice,frames=16001,research_ROM_sha256=selected['research_ROM_sha256'],
        report=str(rp),report_sha256=sha(rp.read_bytes()),observer=str(op),observer_sha256=sha(op.read_bytes()),
        menu_observer=str(mp),menu_observer_sha256=sha(mp.read_bytes()),readonly_menu_snapshots=str(sp),readonly_menu_snapshots_sha256=sha(sp.read_bytes()),
        run_plan=str(plan),run_plan_sha256=sha(plan.read_bytes()),all_callbacks_readonly_andhost_slots_restored=True,
        actual_complete_path_body_header_menu_backing_highlights_transition_return_andlate_analysis_pending=True,
        not_natural_activation_location_earned_progress_full_route_orhardware_coverage=True,new_credit=0,full_goal_complete=False))
    print(f'B46 {version} {choice}:16001 frames terminal;readonly command/caption/menu snapshots captured. Actual path/display/return analysis pending.',flush=True)
