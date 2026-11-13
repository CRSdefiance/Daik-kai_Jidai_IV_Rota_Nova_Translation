"""Execute the actual captured modal contexts,not initialized surrogate metrics."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP,UC_ARM_REG_PC
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_actual_modal_replay_v1736')
OBS=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_modal_context_v1734_1711/modal_observer/actual_modal_contexts.json')


if __name__=='__main__':
    assert not ROOT.exists()
    observed=read(OBS);assert observed['errors']==[] and observed['mismatches']==0
    arm=NdsImage.open('out/all_routes_combined_v1711_candidate.nds').read_file('/__arm9__.bin')
    cases=[]
    for row in observed['rows']:
        if not row.get('complete_readonly_snapshots'):continue
        snapshots={k:Path(r['path']).read_bytes() for k,r in row['complete_readonly_snapshots'].items()}
        for k,data in snapshots.items():assert sha(data)==row['complete_readonly_snapshots'][k]['sha256']
        raw=snapshots['WRAM'];cpu=machine(arm);cpu.mem_write(0x02000000,raw)
        cpu.mem_write(0x01FF8000,snapshots['ITCM']);cpu.mem_write(row['DTCM_base'],snapshots['DTCM'])
        cpu.mem_map(0x06000000,0x800000)
        ctx=row['context'];text=row['R1'];font=row['font_metrics_object'];events=[];font_writes=[]
        assert bytes(cpu.mem_read(ctx,76)).hex()==row['context_76_hex']
        def glyph(u,address,size,_):
            sp=u.reg_read(UC_ARM_REG_SP);code,style=struct.unpack('<2I',u.mem_read(sp,8))
            events.append({'code':code,'style':style,'x':u.reg_read(UC_ARM_REG_R2),'y':u.reg_read(UC_ARM_REG_R3),
                'image':u.reg_read(UC_ARM_REG_R1),'font_metrics':list(struct.unpack('<3I',u.mem_read(font,12)))})
        def write(u,access,address,size,value,_):
            if font<=address<font+24:font_writes.append({'PC':u.reg_read(UC_ARM_REG_PC),'address':address,'size':size,'value':value})
        h=cpu.hook_add(UC_HOOK_CODE,glyph,begin=0x020D16B4,end=0x020D16B4);w=cpu.hook_add(UC_HOOK_MEM_WRITE,write)
        try:call(cpu,0x01FFCE40-0x02000000,(ctx,text),instruction_limit=1000000)
        finally:cpu.hook_del(h);cpu.hook_del(w)
        cases.append({'frame':row['frame'],'source_context':ctx,'source_bitmap':row['bitmap'],'text':row['text_CP932'],
            'glyphs':events,'visible_row_origins':sorted({e['y'] for e in events if e['code']!=32}),
            'font_object_writes':font_writes,'context_after_hex':bytes(cpu.mem_read(ctx,76)).hex(),
            'source_snapshot_sha256':row['complete_readonly_snapshots']['WRAM']['sha256'],
            'VRAM_zero_initialized_for_offline_pixel_paint_not_actual_VRAM_capture':True})
    ROOT.mkdir(parents=True)
    save(ROOT/'captured_context_native_glyph_metrics.json',{'observer':str(OBS),'observer_sha256':sha(OBS.read_bytes()),
        'cases':cases,'no_game_ROM_or_emulator_state_mutated':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print([(r['frame'],r['visible_row_origins'],r['font_object_writes']) for r in cases],flush=True)
