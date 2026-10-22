"""Original53F0C voice selection -> loader -> printf -> macro -> corrected wrap.

CPU research: file open/read and portrait object construction are explicit
boundaries. Actor objects, voice lookup, source tables and COMMON messages are
unchanged. No numeric message is injected into an emulator.
"""
from pathlib import Path
from types import FunctionType,SimpleNamespace
import struct
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.duel_editorial import current_entries
from scripts.probe_common_single_cache_v862 import Loader
from scripts.probe_button_prompt_native import BASE,STACK,STOP
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/escape_direct_source_v1186')
RAW=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_escape_v1179_1166_compassAttack8/frame_006902_arm9_ram.bin')
PLAN=Path('work/analysis/escape_direct_runtime_v1184c/runtime_plan.json')


def machine(arm,common,raw,plan):
    cpu,get=get_machine(arm,raw)
    for row in plan['patches']:
        at=row['address'];data=bytes.fromhex(row['target_hex'])
        assert bytes(cpu.mem_read(at,len(data))).hex()==row['source_hex']
        cpu.mem_write(at,data)
    owner=struct.unpack_from('<I',arm,0x552A0)[0]
    provider=SimpleNamespace(owner=owner,output=owner+0x2030,common=common,opens=[],reads=[],executed=set())
    io=FunctionType(Loader.code.__code__,{**Loader.code.__globals__,'STACK':STACK})
    def boundary(u,pc,size,data):
        if pc==BASE+0xD0170 and u.reg_read(UC_ARM_REG_R2)==owner+0x2230:
            assert (u.reg_read(UC_ARM_REG_R0),u.reg_read(UC_ARM_REG_R1),u.reg_read(UC_ARM_REG_R3))==(owner,8,168)
            u.mem_write(owner+0x2230,common[8:176]);provider.reads.append((8,owner+0x2230,168))
            u.reg_write(UC_ARM_REG_R0,168);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
        else:io(provider,u,pc,size,data)
    for pc in (0xD0398,0xD0170):cpu.hook_add(UC_HOOK_CODE,boundary,begin=BASE+pc,end=BASE+pc)
    cpu.mem_write(owner+8,bytes(4));cpu.mem_write(owner+0x2C,b'\xff')
    return cpu,get,provider


def main():
    assert not ROOT.exists()
    plan=read(PLAN);arm=Path(plan['research_ARM9']).read_bytes()
    assert sha(arm)==plan['target_ARM9_sha256']
    rom=NdsImage.open('out/all_routes_combined_v1166_candidate.nds');common=rom.read_file('/COMMON/MESFILE.DK4')
    entries=current_entries(common,arm);raw=RAW.read_bytes()
    cpu,get,provider=machine(arm,common,raw,plan)
    root=get(0xCB184); actors=[root+4+i*32 for i in range(207)]+[root+0x19E4]
    selected={};voices=[]
    for table in (0x02117500,0x02117620):
        for i,actor in enumerate(actors):
            n=get(0x53F4C,actor,table)
            voices.append({'slot':i,'actor':actor,'table':table,'message_ID':n})
            selected.setdefault(n,(actor,table))
    expected={*range(1951,1957),*range(1973,1980)}
    assert set(selected)==expected,(sorted(selected),sorted(expected))
    reference=read('work/analysis/escape_direct_fonts_v1185/native_direct_escape_fonts.json')
    captain=root+0x19E4;vtable=struct.unpack('<I',cpu.mem_read(captain,4))[0]
    nameptr=get(struct.unpack('<I',cpu.mem_read(vtable+0x20,4))[0]-BASE,captain)
    name=bytes(cpu.mem_read(nameptr,64)).split(b'\0')[0]
    ROOT.mkdir(parents=True);results=[]
    for n,(actor,table) in sorted(selected.items()):
        cpu,get,provider=machine(arm,common,raw,plan);seen={}
        def observe(u,pc,size,data):
            if pc==BASE+0x5408C:
                u.reg_write(UC_ARM_REG_PC,BASE+0x54144)
            elif pc==0x01FFCF3C:
                sp=u.reg_read(UC_ARM_REG_SP)
                seen.update(parent=struct.unpack('<I',u.mem_read(sp+0x264,4))[0],
                    table=struct.unpack('<I',u.mem_read(sp+0x274,4))[0],
                    input_hex=bytes(u.mem_read(u.reg_read(UC_ARM_REG_R1),256)).split(b'\0')[0].hex(),
                    output=u.reg_read(UC_ARM_REG_R0))
            else:
                seen['formatted_hex']=bytes(u.mem_read(seen['output'],256)).split(b'\0')[0].hex()
                u.emu_stop()
        for pc in (BASE+0x5408C,0x01FFCF3C,BASE+0x54164):cpu.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
        cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP)
        for reg,value in ((UC_ARM_REG_R0,actor),(UC_ARM_REG_R1,table),(UC_ARM_REG_R2,nameptr),(UC_ARM_REG_R3,0)):cpu.reg_write(reg,value)
        cpu.emu_start(BASE+0x53F0C,STOP,count=3000000)
        assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0x54164
        assert seen['parent']==0x02053F40 and seen['table']==table
        expanded=entries[n].text.replace(b'%s',name)
        assert seen['input_hex']==expanded.hex()
        candidates=[r for r in reference['cases'] if r['message_ID']==n and (not r['variant'] or r['variant']['name_hex']==name.hex())]
        assert candidates and all(r['formatted_hex']==seen['formatted_hex'] for r in candidates)
        assert b'\n' in bytes.fromhex(seen['formatted_hex'])
        results.append({'message_ID':n,'source_voice_actor':actor,'source_table':table,
            'actual_captain_compact_name_hex':name.hex(),**seen,'file_reads':provider.reads,'file_opens':provider.opens,
            'original53F0C_selection_loader_printf_macro_wrap_execute':True,'CPU_UI_construction_bridge_only_not_gameplay':True})
        print(n,'original direct pipeline passes',flush=True)
    save(ROOT/'original_direct_pipeline.json',{'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),
        'snapshot':str(RAW),'snapshot_sha256':sha(raw),'all416_source_voice_choices':voices,'all13_direct_pipeline_cases':results,
        'boundaries':['host successful file open/read','portrait object construction bypass'],
        'source_actor_objects_tables_and_native_selection_unchanged':True,
        'all13_match_corrected_complete_native_font_case_output':True,'actual_gameplay_still_pending':True,
        'no_ROM_or_completion_credit':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})


if __name__=='__main__':main()
