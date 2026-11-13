"""Bind all source personality aliases andthree-choice captions on the own runtime."""
import argparse
import struct
from copy import deepcopy
from pathlib import Path
from unicorn.arm_const import UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_R1,UC_ARM_REG_SP
from dk4tool.patch.confirmed_name_message_catalog import CALLS,MACRO
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime import RegisteredRuntime

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ['current','styles','choices','out']:parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists();current,styles,choices=map(load,[args.current,args.styles,args.choices])
    assert all(r['earlier_English_unconsulted'] for d in [styles,choices] for r in d['records'])
    runtime=current['runtime'];ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof']);assert runtime==ctx.receipt()
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    ranges=[(0x29BD0,0x29D34),(0x2A154,0x2A1D8),(0x2434C,0x243A0),(0x7E988,0x7E9A0)]
    assert all(ctx.arm[a:b]==clean[a:b] for a,b in ranges)
    cpu,get,_=ctx.machine(ctx.arm,ctx.common,ctx.raw,ctx.plan)
    instruction=struct.unpack_from('<I',ctx.arm,CALLS[0])[0];assert instruction>>24==0xEB
    delta=(instruction&0xFFFFFF)<<2
    if delta&0x2000000:delta-=0x4000000
    entry=BASE+CALLS[0]+8+delta
    def effective(body):
        pointer=0x02468020;cpu.mem_write(pointer-16,b'\xa5'*(len(body)+33));cpu.mem_write(pointer,body+b'\0')
        before=bytes(cpu.mem_read(pointer-16,len(body)+33));cpu.reg_write(UC_ARM_REG_R1,pointer);cpu.reg_write(UC_ARM_REG_LR,BASE+CALLS[0]+4);cpu.reg_write(UC_ARM_REG_SP,0x027F0000)
        cpu.emu_start(entry,MACRO,count=1000000);assert cpu.reg_read(UC_ARM_REG_PC)==MACRO
        selected=cpu.reg_read(UC_ARM_REG_R1);value=bytes(cpu.mem_read(selected,1024)).split(b'\0')[0]
        assert len(value)<1024 and bytes(cpu.mem_read(pointer-16,len(body)+33))==before
        return dict(current_effective_hex=value.hex(),current_effective_text=value.decode('cp932'),current_comparison_paragraph=' '.join(value.decode('cp932').split()),current_catalogue_selected=selected!=pointer,selected_native_pointer=selected)
    groups={g['block']:g for g in current['groups']};style_rows=[];objects=[];native_cases=0
    for block,group in groups.items():
        source_commands={c['offset']:c for c in group['all_source_commands']}
        for mapped in group['command_map']:
            if mapped['word']!=0x4100:continue
            before,now=bytes.fromhex(mapped['source_hex']),bytes.fromhex(mapped['current_hex'])
            assert before[:20].hex()==next(r['source_header_hex'] for r in styles['records'] if r['block']==block and r['source_command_offset']==mapped['source_offset'])
            assert before[:2]==now[:2]==b'\0\x41' and before[18:20]==now[18:20]
            old_offsets=list(struct.unpack_from('<8H',before,2));new_offsets=list(struct.unpack_from('<8H',now,2))
            assert all((old_offsets[a]==old_offsets[b])==(new_offsets[a]==new_offsets[b]) for a in range(8) for b in range(8))
            stream,owner=0x02660000,0x02662000;cpu.mem_write(stream-16,b'\xa5'*(len(now)+32));cpu.mem_write(stream,now)
            cpu.mem_write(owner-16,b'\xa5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream,0,0));guard=bytes(cpu.mem_read(owner-16,64));slots=[]
            for style in range(8):
                main=bytes(cpu.mem_read(BASE,0x400000));pointer=get(0x2A154,owner,style);at=20+new_offsets[style]
                assert pointer==stream+at and at<len(now)
                text=now[at:now.index(0,at)];assert text and bytes(cpu.mem_read(pointer,len(text)+1))==text+b'\0'
                assert bytes(cpu.mem_read(BASE,0x400000))==main and bytes(cpu.mem_read(owner-16,64))==guard
                assert bytes(cpu.mem_read(stream,len(now)))==now and bytes(cpu.mem_read(stream-16,16))==bytes(cpu.mem_read(stream+len(now),16))==b'\xa5'*16
                slots.append(dict(style=style,relative_offset=at,hex=text.hex(),original_getter_andall_unowned4MiB_input_owner_stream_guards_exact=True));native_cases+=1
            originals=[r for r in styles['records'] if r['block']==block and r['source_command_offset']==mapped['source_offset']]
            blockraw=bytes.fromhex(group['current_block_hex'])
            for original in originals:
                indices=original['source_style_indices'];slot=slots[indices[0]]
                assert all(slots[i]['hex']==slot['hex'] and slots[i]['relative_offset']==slot['relative_offset'] for i in indices)
                raw=bytes.fromhex(slot['hex']);offset=mapped['current_offset']+slot['relative_offset']
                row=deepcopy(original);row.update(current_hex=raw.hex(),current_reference=dict(file_path=current['file_path'],block=block,command_offset=mapped['current_offset'],offset=offset,length=len(raw),physical_record_index=blockraw[:offset].count(b'\0')),
                    current_style_object_hex=now.hex(),current_style_indices=indices,current_stored_text=raw.decode('cp932'),current_style_offsets=new_offsets,
                    **effective(raw),earlier_English_unconsulted=False,current_English_now_exposed=True)
                style_rows.append(row)
            objects.append(dict(block=block,source_command_offset=mapped['source_offset'],current_command_offset=mapped['current_offset'],source_object_hex=before.hex(),current_object_hex=now.hex(),source_style_offsets=old_offsets,current_style_offsets=new_offsets,source_selector=now[19],native_slots=slots,source_alias_equivalence_exact=True))
    choice_rows=[];choice_objects=[]
    for group in groups.values():
        for mapped in group['command_map']:
            if mapped['word']!=0x2200:continue
            before,now=bytes.fromhex(mapped['source_hex']),bytes.fromhex(mapped['current_hex']);assert before[:2]==now[:2]==b'\0\x22'
            offsets=struct.unpack_from('<3H',now,2);originals=[r for r in choices['records'] if r['block']==group['block'] and r['source_command_offset']==mapped['source_offset']]
            assert len(originals)==3
            for original in originals:
                i=original['source_index'];at=8+offsets[i];end=now.index(0,at);raw=now[at:end]
                row=deepcopy(original);row.update(current_hex=raw.hex(),current_choice_object_hex=now.hex(),current_reference=dict(file_path=current['file_path'],block=group['block'],command_offset=mapped['current_offset'],source_index=i,offset=mapped['current_offset']+at,length=len(raw)),
                    current_stored_text=raw.decode('cp932'),current_comparison_paragraph=' '.join(raw.decode('cp932').split()),current_effective_text=raw.decode('cp932'),current_effective_hex=raw.hex(),current_catalogue_selected=False,
                    native_choice_provider_not_run_as_message_catalogue=True,earlier_English_unconsulted=False,current_English_now_exposed=True)
                choice_rows.append(row)
            choice_objects.append(dict(block=group['block'],source_command_offset=mapped['source_offset'],current_command_offset=mapped['current_offset'],source_hex=before.hex(),current_hex=now.hex(),count=3,source_index_order=[0,1,2]))
    assert len(style_rows)==48 and native_cases==64 and len(choice_rows)==15 and len(objects)==8 and len(choice_objects)==5
    assert bytes(cpu.mem_read(ctx.actor_root,0x1A04))==ctx.actor_bytes;ctx.calls.clear();args.out.mkdir(parents=True)
    save(args.out/'current_objects.json',dict(current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_archive_sha256=current['current_archive_sha256'],runtime=runtime,
        style_records=style_rows,choice_records=choice_rows,style_objects=objects,choice_objects=choice_objects,native_style_getter_cases=native_cases,
        clean_getter_handler_role_voice_ranges_exact=[dict(start=a,end=b,sha256=sha(ctx.arm[a:b])) for a,b in ranges],
        original_4100_selection_proof_reused='work/analysis/lil_4100_alternatives_v3156/all14_clean_current_eight_style_alternatives.json',
        current_speech_packet=str(args.current),current_speech_packet_sha256=sha(args.current.read_bytes()),source_style_meanings=str(args.styles),source_style_meanings_sha256=sha(args.styles.read_bytes()),source_choice_meanings=str(args.choices),source_choice_meanings_sha256=sha(args.choices.read_bytes()),
        source_meanings_preceded_current_comparison=True,new_localized_English_andformatting_approval_pending=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print(dict(current_style_alternatives=48,current_choice_labels=15,native_style_getter_cases=64,all_source_aliases_preserved=True,new_credit=0))

if __name__=='__main__':main()
