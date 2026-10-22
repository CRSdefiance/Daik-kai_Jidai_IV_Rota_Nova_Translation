"""Map15 original special-move messages, including nonadjacent2146.

CPU source research only: replace the controller's actor pointer for a scope
test while leaving every actor ID unchanged. Initial animation/pose operations
are explicit boundaries. This does not activate an emulator scene.
"""
from dataclasses import asdict
from pathlib import Path
import struct
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.duel_bark_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_duel_actual_holds_v1171 import actual_widget
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.probe_button_prompt_native import STACK,STOP
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_special_context_v1215')
ROM=Path('out/all_routes_combined_v1206_candidate.nds')
RAW=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_bark_v1207_1206/frame_006113_arm9_ram.bin')
IDS=(*range(1980,1994),2146)
# Actor IDs are the original objects' IDs. These are independently checked by
# executing101EC's original jump table and the original message selectors.
CASES=((1,0xF114,1990),(3,0xFD98,1981),(6,0xEED8,2146),(7,0xF444,1982),
       (9,0xF7EC,1985),(10,0xFB70,1992),(12,0xF444,1983),(14,0xED74,1991),
       (15,0xF2D4,1987),(16,0xF7EC,1984),(17,0xF114,1989),(20,0xF2D4,1988),
       (21,0xF7EC,1986),(22,0xFD98,1980),(25,0xF968,1993))
BRIDGES={0xED80:0xEDD0,0xF304:0xF358,0xF484:0xF488,0xF4BC:0xF5B8,0xF838:0xF89C}


def main():
    assert not ROOT.exists()
    clean,current,accepted=map(NdsImage.open,('work/clean.nds',ROM,'out/raphael_natural_v2_accepted_base.nds'))
    source,arm=clean.read_file('/__arm9__.bin'),current.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes())=='3ab79feca6d89fbb3cb4495b378f0a8d70cdeb15ecaf3085713940fc799dcd57'
    assert arm[0xD458:0xD540]==source[0xD458:0xD540] and arm[0xED74:0x11000]==source[0xED74:0x11000]
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
    canonical=common_message_entries(accepted.read_file('/COMMON/MESFILE.DK4'),accepted.read_file('/__arm9__.bin'),clean=False)
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),arm)
    raw=RAW.read_bytes();widget,nested,header,h=actual_widget(raw);controller=nested-0x40
    cpu,get=get_machine(arm,raw);actors=get(0xCB184)
    names={};objects={}
    for slot in range(208):
        actor=actors+4+slot*32 if slot<207 else actors+0x19E4
        number=get(0x7EE08,actor);vt=struct.unpack('<I',cpu.mem_read(actor,4))[0]
        getter=struct.unpack('<I',cpu.mem_read(vt+0x20,4))[0]
        name=bytes(cpu.mem_read(get(getter-0x02000000,actor),64)).split(b'\0')[0].decode('cp932')
        names.setdefault(number,name);objects.setdefault(number,actor)
    expected={actor:method for actor,method,n in CASES};methods=set(expected.values());dispatch=[]
    for slot in range(208):
        cpu,get=get_machine(arm,raw);actor=actors+4+slot*32 if slot<207 else actors+0x19E4
        actor_id=get(0x7EE08,actor);cpu.mem_write(controller+0x4C4,struct.pack('<I',actor));seen=[]
        def observe(u,pc,size,data):
            if pc==0x0200FFA4:u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
            else:seen.append(pc-0x02000000);u.emu_stop()
        cpu.hook_add(UC_HOOK_CODE,observe,begin=0x0200FFA4,end=0x0200FFA4)
        for method in methods:cpu.hook_add(UC_HOOK_CODE,observe,begin=0x02000000+method,end=0x02000000+method)
        cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP);cpu.reg_write(UC_ARM_REG_R0,controller)
        cpu.emu_start(0x020101EC,STOP,count=20000)
        wanted=expected.get(actor_id)
        assert seen==([wanted] if wanted else []),(slot,actor_id,seen,wanted)
        if not wanted:assert cpu.reg_read(UC_ARM_REG_PC)==STOP
        dispatch.append({'slot':slot,'unchanged_actor_ID':actor_id,'name':names[actor_id],'selected_original_method':wanted,
            'native_jump_table_executed':True,'initial_animation_reset_bridged_CPU_only':True})
    selections=[]
    for actor_id,method,number in CASES:
        cpu,get=get_machine(arm,raw);actor=objects[actor_id]
        cpu.mem_write(controller+0x4C4,struct.pack('<I',actor));seen=[];bridged=[]
        def observe(u,pc,size,data):
            if pc==0x0200D4D0:
                values=[u.reg_read(r) for r in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3)]
                seen.append({'context':values[0],'side':values[1],'duration':values[2],'message_ID':values[3],
                    'original_source_return':u.reg_read(UC_ARM_REG_LR)})
                u.emu_stop()
            else:
                bridged.append([pc,0x02000000+BRIDGES[pc-0x02000000]])
                u.reg_write(UC_ARM_REG_PC,0x02000000+BRIDGES[pc-0x02000000])
        cpu.hook_add(UC_HOOK_CODE,observe,begin=0x0200D4D0,end=0x0200D4D0)
        for start,end in BRIDGES.items():cpu.hook_add(UC_HOOK_CODE,observe,begin=0x02000000+start,end=0x02000000+start)
        cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP);cpu.reg_write(UC_ARM_REG_R0,controller)
        cpu.emu_start(0x02000000+method,STOP,count=20000)
        assert len(seen)==1 and seen[0]['message_ID']==number
        assert (seen[0]['context'],seen[0]['side'],seen[0]['duration'])==(nested,0,120)
        assert get(0x7EE08,actor)==actor_id
        selections.append({'actor_ID':actor_id,'actor_object':actor,'name':names[actor_id],
            'source_method':0x02000000+method,**seen[0],'explicit_UI_pose_animation_CPU_bridges':bridged,
            'no_emulator_or_actual_animation_activation_claim':True})
    assert {r['message_ID'] for r in selections}==set(IDS)
    ref=lambda r:{k:v for k,v in asdict(r).items() if k!='text'}
    records=[]
    for n in IDS:
        selected=[r for r in selections if r['message_ID']==n]
        assert len(selected)==1 and jp[n].text.count(b'%s')==0
        records.append({'message_ID':n,'source_reference':ref(jp[n]),'source_hex':jp[n].text.hex(),
            'source_Japanese':jp[n].text.decode('cp932'),'canonical_source_hex':canonical[n].text.hex(),
            'current_reference':ref(en[n]),'current_hex':en[n].text.hex(),'current_English':en[n].text.decode('cp932'),
            'source_actor_ID':selected[0]['actor_ID'],'source_speaker_name':selected[0]['name'],
            'source_method':selected[0]['source_method'],'source_call_return':selected[0]['original_source_return'],
            'native_argument_count':0,'source_native_macros':[],
            'context':'Independent special-move call selected by the original active duelist ID. Original101EC dispatch and method-specific selection reach D4D0 with side0/duration120. Rendering uses the static duel widget after original printf/macro expansion;these are not sequential conversation alternatives.'})
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    code=[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str}
        for start,end in ((0x101EC,0x10308),(0xED74,0xFFAC)) for at in range(start,end,4)
        for i in decoder.disasm(source[at:at+4],0x02000000+at)]
    ROOT.mkdir(parents=True)
    save(ROOT/'source_context_packet.json',{'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'current_COMMON_sha256':sha(current.read_file('/COMMON/MESFILE.DK4')),'current_ARM9_sha256':sha(arm),
        'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'records':records,
        'all208_original_native_special_method_selections':dispatch,'all15_original_message_call_bindings':selections,
        'original_source_instructions':code,'actual_snapshot':str(RAW),'actual_snapshot_sha256':sha(raw),
        'source_actor_IDs_not_mutated_CPU_controller_pointer_rebound_only':True,
        'CPU_pose_animation_boundaries_explicit_not_actual_gameplay':True,
        'COMMON2146_is_an_additional_confirmed_special_move_not_in_prior14_inventory':True,
        'source2146_Julio_not_Generic_town_context':True,
        'White_Tree_school_kanji_is_separate_from_verified_Shiraki_katakana_surname':True,
        'no_new_prose_or_completion_credit':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('15 special calls mapped:208 original dispatches,15 source ID bindings including2146;no prose credit.',flush=True)


if __name__=='__main__':main()
