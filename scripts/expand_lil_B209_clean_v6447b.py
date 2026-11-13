"""Read every stored actor-style alternative in the clean letter exchange before old English."""
import struct
from copy import deepcopy
from pathlib import Path
from unicorn.arm_const import UC_ARM_REG_R0
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save
SOURCE=Path('work/analysis/lil_B209_clean_inventory_v6446/all_clean_B209_speeches_before_predecessor_comparison.json')
ROOT=Path('work/analysis/lil_B209_complete_clean_v6447b')
if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);rom=Path(d['source_ROM']);assert sha(rom.read_bytes())==d['source_ROM_sha256']
    arm=NdsImage.open(rom).read_file('/__arm9__.bin');block=bytes.fromhex(d['clean_block_hex']);objects=[];alternatives=[]
    for c in d['commands']:
        if c['word']!=0x4100:continue
        at=c['offset'];value=bytes.fromhex(c['whole_command_hex']);assert block[at:at+len(value)]==value and value[:2]==b'\0A' and value[18]==0
        offsets=struct.unpack_from('<8H',value,2);prefix=value[19];slots=[]
        cpu=machine(arm);STREAM,OWNER=0x02660000,0x02662000
        cpu.mem_write(STREAM-16,b'\xa5'*(len(value)+32));cpu.mem_write(STREAM,value)
        cpu.mem_write(OWNER-16,b'\xa5'*64);cpu.mem_write(OWNER,struct.pack('<4I',0,STREAM,0,0));guard=bytes(cpu.mem_read(OWNER-16,64));main=bytes(cpu.mem_read(0x02000000,0x400000))
        for style,offset in enumerate(offsets):
            call(cpu,0x2A154,(OWNER,style));pointer=cpu.reg_read(UC_ARM_REG_R0);relative=20+offset
            assert pointer==STREAM+relative and relative<len(value)
            end=value.index(0,relative);text=value[relative:end];assert text
            assert bytes(cpu.mem_read(STREAM,len(value)))==value and bytes(cpu.mem_read(OWNER-16,64))==guard and bytes(cpu.mem_read(0x02000000,0x400000))==main
            assert bytes(cpu.mem_read(STREAM-16,16))==bytes(cpu.mem_read(STREAM+len(value),16))==b'\xa5'*16
            slots.append(dict(style_index=style,relative_offset=relative,offset=at+relative,hex=text.hex(),Japanese=text.decode('cp932'),original_getter_pointer_and_all4MiB_owner_stream_guards_exact=True))
        rows=[]
        for relative in sorted({s['relative_offset'] for s in slots}):
            s=next(s for s in slots if s['relative_offset']==relative)
            r=dict(id=f'DK4_VOICE_B209_C{at}_T{relative}',file_path='/data/SC2.DK4',block=209,kind='typed-4100-actor-style-alternative',command_offset=at,source_selector=prefix,source_reference=dict(block=209,offset=s['offset'],bytes=len(bytes.fromhex(s['hex'])),command_offset=at),source_hex=s['hex'],source_Japanese=s['Japanese'],style_indices=[s['style_index'] for s in slots if s['relative_offset']==relative],source_legacy_NUL_ID=f'DK4_MES_B209_R{block[:s["offset"]].count(bytes([0])):04d}')
            rows.append(r);alternatives.append(r)
        objects.append(dict(command=deepcopy(c),source_selector=prefix,source_offsets=list(offsets),source_style_slots=slots,source_complete_header_hex=value[:20].hex(),records=rows,not_a_player_choice=True))
    speeches=[]
    for r in d['records']:
        r=deepcopy(r);r.update(id=f'DK4_MES_B209_R{r["source_record_index"]:04d}',file_path='/data/SC2.DK4',block=209,kind='progressive',source_Japanese=r['Japanese'],source_reference=dict(block=209,offset=r['offset'],bytes=r['bytes'],record_index=r['source_record_index'],header_offset=r['header_offset']));speeches.append(r)
    assert len(objects)==2 and sum(len(o['source_style_slots']) for o in objects)==16
    assert len(alternatives)==15 and len(speeches)==5 and [len(o['records']) for o in objects]==[7,8]
    assert [o['source_selector'] for o in objects]==[208,208] and objects[0]['source_offsets'][2]==objects[0]['source_offsets'][7]
    logical=8+struct.unpack_from('<H',block,4)[0];assert (len(block),logical,block[logical:])==(1148,1148,b'')
    ROOT.mkdir(parents=True);save(ROOT/'all20_clean_objects_five_speeches15_stored_alternatives16_slots.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),source_ROM=d['source_ROM'],source_ROM_sha256=d['source_ROM_sha256'],source_block_sha256=sha(block),source_stored_bytes=len(block),source_logical_end=logical,source_tail_bytes=0,commands=d['commands'],records=speeches,typed_actor_style_records=alternatives,actor_style_objects=objects,total_editorial_objects=20,original_inline_getter_cases=16,complete_source_only_context_gloss_before_old_English_pending=True,prior_English_unread=True,no_current_prose_consulted=True,current_actor_selectorD0_role_voices_whole4100_consumer_conditions_and_relocation_pending=True,new_review_credit=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(__file__)]},full_goal_complete=False))
    for o in objects:
        for r in o['records']:print(r['id'],r['style_indices'],r['source_Japanese'].replace('\n',' / '))
    for r in speeches:print(r['id'],r['source_Japanese'].replace('\n',' / '))
    print('20 physical objects:15 stored actor-style alternatives/16 slots plus5 speeches;not two choice menus. Old English unread.')
