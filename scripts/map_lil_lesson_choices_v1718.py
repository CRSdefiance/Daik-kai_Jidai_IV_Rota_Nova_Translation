"""Execute original choice count/label accessors for both tutorial menus."""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from unicorn.arm_const import UC_ARM_REG_R0
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_lesson_choices_v1718')
PACKET=Path('work/analysis/lil_lessons_source_v1717/complete_lesson_source_context.json')
OBJECT,STREAM=0x02660000,0x02662000


if __name__=='__main__':
    assert not ROOT.exists()
    packet=read(PACKET);clean=NdsImage.open('work/clean.nds');current=NdsImage.open(packet['current_ROM'])
    arms=[r.read_file('/__arm9__.bin') for r in (clean,current)]
    assert arms[0][0x2A30C:0x2A414]==arms[1][0x2A30C:0x2A414]
    cases=[]
    for label,arm in zip(('clean','current'),arms,strict=True):
        cpu=machine(arm)
        for block in packet['blocks']:
            choice=block['choices'][0];value=bytes.fromhex(choice['source_hex' if label=='clean' else 'current_hex'])
            assert value[:4]==b'\0\x21\0\0'
            cpu.mem_write(STREAM-16,b'\xA5'*(len(value)+32));cpu.mem_write(STREAM,value)
            cpu.mem_write(OBJECT-16,b'\xA5'*64);cpu.mem_write(OBJECT,struct.pack('<3I',0,0,STREAM))
            before=bytes(cpu.mem_read(OBJECT-16,64))
            call(cpu,0x2A3B8,(OBJECT,));assert cpu.reg_read(UC_ARM_REG_R0)==2
            labels=[]
            for index in range(2):
                expected=6+struct.unpack_from('<H',value,2+index*2)[0]
                call(cpu,0x2A30C,(OBJECT,index));pointer=cpu.reg_read(UC_ARM_REG_R0)
                assert pointer==STREAM+expected
                text=bytes(cpu.mem_read(pointer,len(value)-expected)).split(b'\0')[0]
                assert text and expected+len(text)<len(value)
                labels.append({'index':index,'relative_offset':expected,'hex':text.hex(),'text':text.decode('cp932')})
            assert bytes(cpu.mem_read(OBJECT-16,64))==before
            assert bytes(cpu.mem_read(STREAM,len(value)))==value
            assert bytes(cpu.mem_read(STREAM-16,16))==bytes(cpu.mem_read(STREAM+len(value),16))==b'\xA5'*16
            cases.append({'version':label,'block':block['block'],'command_offset':choice['offset'],
                'source_word':0x2100,'native_choice_count':2,'labels':labels,
                'original_count_and_pointer_accessors_ABI_input_and_guard_bytes_exact':True})
    ROOT.mkdir(parents=True)
    save(ROOT/'native_two_choice_labels.json',{'source_context':str(PACKET),'source_context_sha256':sha(PACKET.read_bytes()),
        'original_accessors':[0x0202A3B8,0x0202A30C],'source_byte_span':[0x0202A30C,0x0202A414],
        'source_bytes_exact_current_to_clean':True,'cases':cases,
        'label_table_direct_offsets_relative_to_command_plus6':True,
        'choice_rendering_bounds_and_selected_branch_gameplay_not_verified':True,
        'no_ROM_registry_or_completion_change':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Four original two-choice objects verified:8 complete clean/current labels and exact pointer/count/ABI contracts.',flush=True)
