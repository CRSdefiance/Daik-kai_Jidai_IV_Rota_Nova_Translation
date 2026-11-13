"""Bind all three-option source menus,including every answer and result index."""
import struct
from pathlib import Path
from unicorn.arm_const import UC_ARM_REG_R0
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_three_option_source_v3162')
SOURCE=Path('work/analysis/lil_Shrines_Temples_source_v3159/complete220_clean_current_native_context.json')
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);paths=[Path('work/clean.nds'),Path(source['current_ROM'])];images=[NdsImage.open(p)for p in paths];arms=[i.read_file('/__arm9__.bin')for i in images];blocks=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in images];inventory,_,_=scoped_inventory()
    assert arms[0][0x2A1D8:0x2A414]==arms[1][0x2A1D8:0x2A414]
    objects=[];rows=[];calls=0
    for b in source['blocks']:
        n=b['block']
        for c,now in zip(b['all_clean_native_commands'],b['all_current_native_commands'],strict=True):
            if not 0x2000<=c['word']<0x4000:continue
            assert c['word']==now['word']==0x2200;at=c['offset'];versions=[]
            for label,arm,bb,command in zip(['clean','current'],arms,blocks,[c,now],strict=True):
                block=bb[n];value=block[at:at+command['native_extent']];cpu=machine(arm);STREAM,OBJECT=0x02660000,0x02662000
                cpu.mem_write(STREAM-16,b'\xA5'*(len(value)+32));cpu.mem_write(STREAM,value);cpu.mem_write(OBJECT-16,b'\xA5'*64);cpu.mem_write(OBJECT,struct.pack('<3I',0,0,STREAM));guard=bytes(cpu.mem_read(OBJECT-16,64));main=bytes(cpu.mem_read(0x02000000,0x400000))
                call(cpu,0x2A3B8,(OBJECT,));count=cpu.reg_read(UC_ARM_REG_R0);assert count==3;calls+=1;labels=[]
                for option in range(count):
                    relative=8+struct.unpack_from('<H',value,2+2*option)[0];call(cpu,0x2A30C,(OBJECT,option));pointer=cpu.reg_read(UC_ARM_REG_R0);assert pointer==STREAM+relative
                    text=bytes(cpu.mem_read(pointer,len(value)-relative)).split(bytes([0]))[0];assert text;calls+=1
                    labels.append(dict(option_index=option,relative_offset=relative,offset=at+relative,hex=text.hex(),text=text.decode('cp932')))
                assert bytes(cpu.mem_read(OBJECT-16,64))==guard and bytes(cpu.mem_read(STREAM,len(value)))==value and bytes(cpu.mem_read(0x02000000,0x400000))==main
                for p in [STREAM-16,STREAM+len(value)]:assert bytes(cpu.mem_read(p,16))==b'\xA5'*16
                versions.append(dict(version=label,command_offset=at,command_hex=value.hex(),count=count,text_base=8,labels=labels,original_count_pointer_ABI_all4MiB_owner_input_and_guards_exact=True))
            labels=[]
            for jp,en in zip(versions[0]['labels'],versions[1]['labels'],strict=True):
                option=jp['option_index'];assert option==en['option_index'];r=dict(id=f'DK4_CHOICE_B{n}_C{at}_O{option}',file_path='/data/SC2.DK4',block=n,command_offset=at,option_index=option,kind='typed-choice-label',source_command_word=0x2200,source_reference=dict(offset=jp['offset'],bytes=len(bytes.fromhex(jp['hex']))),current_reference=dict(offset=en['offset'],bytes=len(bytes.fromhex(en['hex']))),source_hex=jp['hex'],current_hex=en['hex'],source_Japanese=jp['text'],current_English=en['text'],source_legacy_NUL_ID=f'DK4_MES_B{n}_R{blocks[0][n][:jp["offset"]].count(bytes([0])):04d}',source_prose_or_completion_credit_added=0,original_three_result_order_preserved=True,selection_cancel_VM_and_complete_native_menu_display_pending=True)
                labels.append(r);rows.append(r)
            objects.append(dict(block=n,command_offset=at,source_command=c,current_command=now,versions=versions,records=labels))
    assert len(objects)==5 and len(rows)==15 and calls==40
    ROOT.mkdir(parents=True);save(ROOT/'all5_three_option_clean_current_native_pointer_proof.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],objects=objects,records=rows,original_native_count_and_pointer_calls=calls,all5_source_commands_are2200_with3ordered_labels=True,source_and_current_all_indices0_1_2_pointers_counts_texts_and_guards_preserved=True,source_context220_is_nonexhaustive_without_these15_choice_labels=True,first_ten_scope_including_choices=235,all_B101_B119_scope_including_choices=417,source_prose_credit_added=0,completion_credit_added=0,new_emulator_runs=0,complete_native_three_option_geometry_selection_cancel_and_release_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Five2200menus/15source-current labels,40guarded native count/getter calls. Nextscope235(first10)/417(all19);menu VM/display stillpending;zero credit.')
