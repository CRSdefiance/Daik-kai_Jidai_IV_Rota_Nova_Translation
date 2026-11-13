"""Complete native4000 commands:one source00 selector thena nonempty body."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_PC,UC_ARM_REG_LR
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B131_B133_typed_speech_v3323')
DOC=Path('translations/lil_B131_B133_editorial_manuscript_v3.json')
BASE=0x02000000
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);source=read(doc['source_context']);arm=NdsImage.open(doc['current_ROM']).read_file('/__arm9__.bin');cases=[]
    byid={r['id']:r for r in source['records']}
    for row in doc['records']:
        original=byid[row['id']]
        for version,raw in [('clean',bytes.fromhex(original['source_hex'])),('current',bytes.fromhex(original['current_hex'])),('compiled',bytes.fromhex(row['compiled_hex']))]:
            assert raw[0]==row['source_selector'] and raw[1:] and b'\0' not in raw[1:]
            command=bytes.fromhex('0040ffff00')+raw+b'\0';command+=b'\0'*(-len(command)%2)
            for phase in [0,2]:
                cpu=machine(arm);stream,owner,result,length=0x02660000+phase,0x02662000,0x02664000,0x02664100
                cpu.mem_write(stream-16,b'\xa5'*(len(command)+32));cpu.mem_write(stream,command);cpu.mem_write(owner-16,b'\xa5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream,0,0));owned=bytes(cpu.mem_read(owner-16,64));before=bytes(cpu.mem_read(BASE,0x400000));seen=[]
                def boundary(u,pc,size,unused):
                    selector=u.reg_read(UC_ARM_REG_R0);pointer=u.reg_read(UC_ARM_REG_R1);assert selector==raw[0] and pointer==stream+6
                    value=bytes(u.mem_read(pointer,len(raw))).split(b'\0')[0];assert value==raw[1:] and value
                    seen.append(dict(selector=selector,body_pointer=pointer,complete_nonempty_body_hex=value.hex(),prefix_zero_not_treated_as_body_terminator=selector==0,original_2425C_display_body_unexecuted=True))
                    u.reg_write(UC_ARM_REG_R0,0);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
                hook=cpu.hook_add(UC_HOOK_CODE,boundary,begin=BASE+0x2425C,end=BASE+0x2425C)
                cpu.mem_write(result-16,b'\xa5'*80);cpu.mem_write(result,bytes(24));cpu.mem_write(length-16,b'\xa5'*36);cpu.mem_write(length,bytes(4))
                try:call(cpu,0x2A510,(result,owner,length,0xFFFFFFFF),instruction_limit=400000)
                finally:cpu.hook_del(hook)
                extent=struct.unpack('<I',cpu.mem_read(length,4))[0];native=struct.unpack('<6I',cpu.mem_read(result,24))
                assert len(seen)==1 and extent==len(command) and native==(3,0,0,0,0,0) and bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(owner-16,64))==owned and bytes(cpu.mem_read(stream,len(command)))==command
                for p in [stream-16,stream+len(command),result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(p,16))==b'\xa5'*16
                cases.append(dict(id=row['id'],version=version,even_input_alignment=phase,whole_native_command_hex=command.hex(),source_selector=raw[0],native_extent=extent,native_result=list(native),original_display_boundary=seen[0],ABI_all4MiB_owner_stream_result_length_and_guards_exact=True))
    assert len(cases)==366 and sum(c['source_selector']==0 for c in cases)==108
    ROOT.mkdir(parents=True);save(ROOT/'all366_whole4000_commands_and108_source00_cases.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_context=doc['source_context'],source_context_sha256=doc['source_context_sha256'],cases=cases,all61_complete_source_current_compiled_preambles_and_bodies_preserved=True,all108_source00_cases_forward_nonempty_body_after_selector_to_original_display=True,exactly_one_leading_source00_actor_byte_not_a_body_C_string_terminator=True,original_UI_display_body_bridged_and_not_actual_gameplay=True,full_native_fonts_macros_and_pagination_proved_separately=True,no_native_code_orROM_mutation=True,new_emulator_runs=0,source_prose_orcompletion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('366 complete clean/current/compiled4000 commands pass,including108 source00 cases. Original handler forwards full nonempty body after actor byte;ABI/4MiB/guards exact. UIbody explicitly bridged.')
