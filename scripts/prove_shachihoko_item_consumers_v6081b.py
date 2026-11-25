"""Execute current parent/target item getters and both source virtual callers on real snapshots."""
import struct
from pathlib import Path
from unicorn.arm_const import UC_ARM_REG_R4,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_SP,UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shachihoko_item_name_data_v1 import transform
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.probe_button_prompt_native import BASE,STACK
from scripts.verify_name_catalog_glyphs_v278 import raster
from scripts.lil_current_font_oracles_v5918 import _expected
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_item_consumers_v6081b')
RESEARCH=Path('work/analysis/shachihoko_item_name_research_v6079/research_image_receipt.json')
DOC=RESEARCH.parent/'provisional_item116_manuscript.json'
TERMINAL=Path('work/analysis/shachihoko_runs_v6080/newgame_terminal.json')

def consumers(arm,common,raw,plan):
    cpu,get,provider=machine(arm,common,raw,plan);root=get(0xCB190);initial=bytes(cpu.mem_read(BASE,0x400000));rows=[]
    for ident in range(218):
        actor=root+4+ident*20;vtable=struct.unpack('<I',cpu.mem_read(actor,4))[0];getter=struct.unpack('<I',cpu.mem_read(vtable+8,4))[0]
        assert vtable==BASE+0x13C38C and getter==BASE+0x4A53C
        pointer=get(getter-BASE,actor);data=bytes(cpu.mem_read(pointer,256)).split(b'\0',1)[0]
        static=get(0xCDAFC,ident,0);assert static==BASE+0x11E210+ident*24
        static_pointer=struct.unpack('<I',cpu.mem_read(static,4))[0];static_data=bytes(cpu.mem_read(static_pointer,256)).split(b'\0',1)[0]
        callers=[]
        for start,end,index_reg,result_reg in [(0x1C7CC,0x1C7EC,UC_ARM_REG_R4,UC_ARM_REG_R4),(0x1C91C,0x1C93C,UC_ARM_REG_R6,UC_ARM_REG_R7)]:
            cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(index_reg,ident);cpu.emu_start(BASE+start,BASE+end,count=1000)
            assert cpu.reg_read(UC_ARM_REG_PC)==BASE+end and cpu.reg_read(UC_ARM_REG_SP)==STACK and cpu.reg_read(result_reg)==pointer
            callers.append(dict(start=BASE+start,end=BASE+end,selected_pointer=pointer,selected_hex=data.hex()))
        assert bytes(cpu.mem_read(BASE,0x400000))==initial
        rows.append(dict(item_ID=ident,actor_object=actor,vtable=vtable,getter=getter,pointer=pointer,text_hex=data.hex(),static_entry=static,static_pointer=static_pointer,static_text_hex=static_data.hex(),original_virtual_callers=callers,all4MiB_models_RNG_and_owned_name_storage_unchanged=True))
    assert len(rows)==218
    return dict(rows=rows,current_executed_instruction_addresses=len(provider.executed_current),original_initialized_runtime_item_objects_no_synthetic_inventory=True)

if __name__=='__main__':
    assert not ROOT.exists();receipt,doc,terminal=map(read,[RESEARCH,DOC,TERMINAL]);assert terminal['terminal']
    report_path=Path(terminal['report']);report=read(report_path);rom=NdsImage.open(receipt['research_ROM']);arm=rom.read_file('/__arm9__.bin')
    assert sha(Path(receipt['research_ROM']).read_bytes())==receipt['research_ROM_sha256']==report['ROM_sha256'] and sha(report_path.read_bytes())==terminal['report_sha256']
    before=NdsImage.open(receipt['parent']);clean=NdsImage.open('work/clean.nds');target,proof=transform(before.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin'),doc['records'][0]);assert target==arm and proof==receipt['data_plan']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and not report.get('battery_save_preloaded')
    snap=next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame']==4000);assert snap['read_only_export'] and sha(Path(snap['path']).read_bytes())==snap['sha256']
    ROOT.mkdir(parents=True);context=ROOT/'target_capture_context.json';config=read('translations/shop657_full_width_reflow_release_v1.json')
    save(context,dict(capture_report=str(report_path),capture_report_sha256=sha(report_path.read_bytes()),frame=4000,snapshot_sha256=snap['sha256'],directory_sha256=config['directory_sha256']))
    inp=ROOT/'target_native_input.json';save(inp,dict(current_ROM=receipt['research_ROM'],current_ROM_sha256=receipt['research_ROM_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(rom.read_file('/COMMON/MESFILE.DK4')),native_context_proof=str(context)))
    versions=[]
    for label,path in [('parent','work/analysis/lil_B204_voices_v6063/current_native_input.json'),('target',inp)]:
        ctx=CurrentContext(path,'unused-no-historical-ROM',ROOT/(label+'_current_context'))
        for a,b in [(0x4A53C,0x4A58C),(0xCDAFC,0xCDB48),(0x1C7CC,0x1C7EC),(0x1C91C,0x1C93C)]:assert ctx.arm[a:b]==clean.read_file('/__arm9__.bin')[a:b]
        result=ctx.execute(consumers);ctx.machines.pop();assert not ctx.machines
        versions.append(dict(case=label,result=result,context_plan=str(ctx.proof_path),context_plan_sha256=sha(ctx.proof_path.read_bytes())))
    changed=[]
    for a,b in zip(versions[0]['result']['rows'],versions[1]['result']['rows'],strict=True):
        assert a['item_ID']==b['item_ID'] and a['getter']==b['getter'] and a['vtable']==b['vtable'] and a['pointer']==b['pointer'] and a['static_entry']==b['static_entry'] and a['static_pointer']==b['static_pointer']
        if a['text_hex']!=b['text_hex'] or a['static_text_hex']!=b['static_text_hex']:
            assert a['item_ID']==116 and bytes.fromhex(a['text_hex'])==bytes.fromhex(a['static_text_hex'])==b'Orca Figurehead' and bytes.fromhex(b['text_hex'])==bytes.fromhex(b['static_text_hex'])==b'Shachihoko';changed.append(dict(parent=a,target=b))
        else:assert a['text_hex']==b['text_hex'] and a['static_text_hex']==b['static_text_hex']
    assert len(changed)==1
    pixels,events,font=raster(arm,b'Shachihoko');expected=_expected(arm,font,events);assert pixels==expected and [e['code'] for e in events]==list(b'Shachihoko') and len({e['y'] for e in events})==1 and max(e['x']+6 for e in events)<=216
    save(ROOT/'all218_item_getters_two_original_callers_and_complete_native_title_plane.json',dict(
        parent=receipt['parent'],target=receipt['research_ROM'],target_ARM9_sha256=sha(arm),data_only_source_preservation_plan=proof,
        versions=versions,changed_cases=changed,all218_parent_and218_target_original_virtual_and_static_getters_pass=True,
        all436_parent_and436_target_original_virtual_name_callers_pass=True,only_item116_native_and_static_title_outputs_change=True,
        all217_other_item_names_and_late_runtime_names_exact=True,actual_initialized_runtime_pointers_not_recreated_or_equipment_forced=True,
        complete_native_title_plane=dict(title='Shachihoko',events=events,whole_plane_sha256=sha(pixels),first_and_final_glyphs_complete=True,single_row_bounds_and_canaries_pass=True),
        independent_current_y_plus_one_glyph_oracle_reused_after_exact_name_data_only_inverse=True,
        actual_item_card_list_acquisition_panels_and_registered_release_pending=True,no_actual_inventory_menu_or_earned_ownership_claim=True,
        actual_snapshot_from_data_only_research_New_Game=True,no_initialized_RAM_overlay_or_historical_runtime=True,
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [RESEARCH,DOC,TERMINAL,report_path,Path(__file__),Path('scripts/lil_current_font_oracles_v5918.py')]}))
    print('218parent+218target virtual/static getters and436+436 original callers pass;only item116 changes. Complete title glyph plane passes;actual item panels/release remain pending.')
