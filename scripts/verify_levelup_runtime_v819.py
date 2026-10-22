"""Private adapter contracts; source caller, every stat combination, native font.

The alternate-header test declares its external I/O boundaries. It proves the
repacked instruction block, not native widget construction or COMMON97 wording.
The font tests are native CPU rasters, not GPU or gameplay approval.
"""

import itertools
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,
    UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,
    UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,
    UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.levelup_format_runtime_v819 import BASE,START,END,HOOK,ROOT,COPY_OFFSET,assembled,apply
from scripts.native_call_abi_v764 import call
from dk4tool.patch.ceremony_editorial import current_entries
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

REGS=(UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,
      UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,
      UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,
      UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR)
STACK=0x02470000


def header_contract(old,new):
    machines=[prepared(a) for a in (old,new)]
    vectors=list(itertools.product((-1,0,1,255,256),repeat=4))
    bounds=(-1024,-1,0,1,255,256,511,-2147483648,2147483647)
    vectors += list(zip(bounds,bounds[::-1],bounds[2:]+bounds[:2],bounds[4:]+bounds[:4]))
    table,obj,method,template,text,result=0x02410000,0x02410100,0x027E1000,0x02410200,0x02410300,0x02410400
    cases=[]
    for index,vector in enumerate(vectors):
        outputs=[]
        for cpu in machines:
            cpu.reg_write(UC_ARM_REG_CPSR,0xA0000010)
            for n,reg in enumerate(REGS):cpu.reg_write(reg,0x5A000000+n*0x123+index)
            cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_R6,obj)
            cpu.mem_write(STACK-16,b'\xA5'*128)
            cpu.mem_write(obj,struct.pack('<I',table));cpu.mem_write(table+32,struct.pack('<I',method))
            cpu.mem_write(template,b'%s\x81\x41\x82k\x82\x96\x82t\x82o\x81I\0');cpu.mem_write(text,b'Hodram\0')
            visited=[];observed=[]

            def boundary(u,pc,size,unused):
                args=tuple(u.reg_read(r) for r in REGS[:4])
                if pc==BASE+0x3F0F8:
                    visited.append('manager');u.reg_write(UC_ARM_REG_R0,0x02123400)
                elif pc==BASE+0x90698:
                    assert args[:2]==(STACK+40,0x02123400)
                    visited.append('bounds');u.mem_write(args[0],struct.pack('<4i',*vector))
                elif pc==BASE+0x5528C:
                    assert args[0]==97
                    visited.append('COMMON97');u.reg_write(UC_ARM_REG_R0,template)
                elif pc==method:
                    assert args[0]==obj
                    visited.append('actor-name-virtual');u.reg_write(UC_ARM_REG_R0,text)
                elif pc==BASE+0xABFCC:
                    assert args[1:3]==(template,text)
                    visited.append('printf');observed.append(args[:3]);u.reg_write(UC_ARM_REG_R0,result)
                else:raise AssertionError(hex(pc))
                u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))

            handles=[cpu.hook_add(UC_HOOK_CODE,boundary,begin=p,end=p)
                     for p in (BASE+0x3F0F8,BASE+0x90698,BASE+0x5528C,method,BASE+0xABFCC)]
            try:cpu.emu_start(START,END,count=300)
            finally:
                for h in handles:cpu.hook_del(h)
            assert cpu.reg_read(UC_ARM_REG_PC)==END and not cpu.reg_read(UC_ARM_REG_CPSR)&32
            assert visited==['manager','bounds','COMMON97','actor-name-virtual','printf']
            # Original final ARM BL at END supplies the same callsite/LR.
            outputs.append(dict(call_args=[cpu.reg_read(r) for r in REGS[:4]],
                stack=bytes(cpu.mem_read(STACK-16,128)).hex(),
                live_saved=[cpu.reg_read(r) for r in REGS[5:12]],SP=cpu.reg_read(UC_ARM_REG_SP),printf=observed))
        assert outputs[0]==outputs[1],(vector,outputs)
        cases.append(dict(input_rectangle=vector,original_final_call_args_stack_SP_R5_R11_and_printf_exact=True))
    assert len(cases)==634
    save(ROOT/'header_contracts.json',dict(count=len(cases),cases=cases,
        source_ARM9_sha256=sha(old),research_ARM9_sha256=sha(new),
        explicit_IO_boundaries=['manager return','rectangle return','COMMON97 getter','actor virtual name','printf'],
        R4_dead_after_printf_reused_for_ARM_tail_target=True,
        R3_IP_flags_and_intermediate_LR_not_asserted_identical=True,
        COMMON97_translation_and_actual_widget_still_unapproved=True))
    print('634 alternate-header instruction/rectangle/call-argument contracts pass.',flush=True)


def font_plane(arm,kanji,lines):
    # Reuse the pinned independent4-row model in page-sized chunks.
    planes=[independent_font(arm,kanji,lines[n:n+4]) for n in range(0,len(lines),4)]
    return b''.join(p[:228*16*min(4,len(lines)-n*4)] for n,p in enumerate(planes))


def compound_contract(arm,rom):
    cpu=prepared(arm);helper=assembled()[1];buffer=STACK+0x38
    names=read('work/analysis/levelup_format_v818/source_growth_catalog.json')['names']['current']
    received=[]

    def print_boundary(u,pc,size,unused):
        ptr=u.reg_read(UC_ARM_REG_R0);assert ptr==buffer+COPY_OFFSET
        received.append(bytes(u.mem_read(ptr,256)).split(b'\0')[0])
        u.reg_write(UC_ARM_REG_R0,0x5A5A);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))

    hook=cpu.hook_add(UC_HOOK_CODE,print_boundary,begin=BASE+0x5473C,end=BASE+0x5473C)
    cases=[];fonts=[];pages=[];largest_raw=largest_output=0
    try:
        for amounts in itertools.product(range(4),repeat=6):
            if not any(amounts):continue
            lines=[f'{name} increased by {chr(0xFF10+amount)}!' for name,amount in zip(names,amounts,strict=True) if amount]
            raw='\n'.join(lines).encode('cp932')+b'\n'
            expected=b' '+b'\n  '.join(line.encode('cp932') for line in lines)
            cpu.mem_write(STACK-64,b'\xA5'*(0x440));cpu.mem_write(buffer,raw+b'\0');received.clear()
            cpu.reg_write(UC_ARM_REG_CPSR,0xA0000010)
            values={reg:0xA5A51000+n for n,reg in enumerate(REGS[4:12])}
            values[UC_ARM_REG_R5]=1
            for reg,value in values.items():cpu.reg_write(reg,value)
            cpu.reg_write(UC_ARM_REG_SP,STACK)
            rng=bytes(cpu.mem_read(0x02168EB8,4))
            cpu.emu_start(BASE+0x7E554,BASE+0x7E570,count=10000)
            assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0x7E570 and not cpu.reg_read(UC_ARM_REG_CPSR)&32
            assert cpu.reg_read(UC_ARM_REG_SP)==STACK and all(cpu.reg_read(r)==v for r,v in values.items())
            assert received==[expected] and cpu.reg_read(UC_ARM_REG_R0)==0x5A5A
            assert bytes(cpu.mem_read(buffer,len(raw)+1))==raw+b'\0'
            assert bytes(cpu.mem_read(buffer+len(raw)+1,COPY_OFFSET-len(raw)-1))==b'\xA5'*(COPY_OFFSET-len(raw)-1)
            end=COPY_OFFSET+len(expected)+1;assert end<=768
            assert bytes(cpu.mem_read(buffer+end,768-end))==b'\xA5'*(768-end)
            # The call's push frames occupy SP-20..SP-1; they are intentionally owned stack.
            assert bytes(cpu.mem_read(STACK-64,40))==b'\xA5'*40
            assert bytes(cpu.mem_read(buffer+768,64))==b'\xA5'*64
            assert bytes(cpu.mem_read(0x02168EB8,4))==rng
            largest_raw=max(largest_raw,len(raw));largest_output=max(largest_output,len(expected))
            cases.append(dict(amounts=amounts,original_tail_print_once=True,
                all_names_numbers_words_order_and_raw_input_exact=True,
                ABI_RNG_768_byte_ownership_and_canaries_pass=True,rows=len(lines),formatted_hex=expected.hex()))
            if all(n in (0,3) for n in amounts):
                height=max(64,16*len(lines))
                plane=raster(arm,expected,0x01FFCE40-BASE,size=(228,height),instruction_limit=1000000)
                target=font_plane(arm,rom.read_file('/GRP/KANJI.FNT'),lines)
                target += bytes(228*(height-len(lines)*16))
                assert plane==target,amounts
                fonts.append(dict(amounts=amounts,rows=len(lines),native_complete_font_and_blank_plane_exact=True))
                if len(lines)>4:
                    first,consumed=raster(arm,expected,0x01FFCE40-BASE,size=(228,64),complete=False,instruction_limit=1000000)
                    assert first==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),lines[:4])
                    assert 0<consumed<len(expected)
                    remainder=expected[consumed:]
                    second=raster(arm,remainder,0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
                    assert second==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),lines[4:])
                    pages.append(dict(amounts=amounts,first_page_exact=True,native_consumed_bytes=consumed,
                        remainder_hex=remainder.hex(),second_complete_native_font_and_blank_plane_exact=True,
                        no_third_or_blank_page_bytes=True,actual_modal_page_resume_pending=True))
        for flag,raw in ((0,b'Stamina increased by \x82P!\n'),(0,b''),(1,b'')):
            received.clear();cpu.mem_write(STACK-64,b'\xA5'*0x440);cpu.mem_write(buffer,raw+b'\0')
            cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_R5,flag);cpu.reg_write(UC_ARM_REG_CPSR,0x10)
            cpu.emu_start(BASE+0x7E554,BASE+0x7E570,count=100)
            assert not received and cpu.reg_read(UC_ARM_REG_PC)==BASE+0x7E570
            assert bytes(cpu.mem_read(buffer,len(raw)+1))==raw+b'\0'
    finally:cpu.hook_del(hook)
    assert len(cases)==4095 and len(fonts)==63
    save(ROOT/'compound_contracts.json',dict(count=len(cases),cases=cases,full_native_fonts=fonts,
        maximum_source_bytes=largest_raw,maximum_output_bytes=largest_output,copy_offset=COPY_OFFSET,
        original_local_buffer_capacity=768,empty_and_disabled_original_tail_controls=3,
        native_first_page_cases=pages,actual_modal_pagination_GPU_and_full_parent_pending=True,
        research_ARM9_sha256=sha(arm),producer_sha256=sha(Path(__file__).read_bytes())))
    print(f'4095 original tail calls,3 empty/disabled controls,63 complete native font planes pass; max{largest_raw}/{largest_output} bytes. Actual modal pagination pending.',flush=True)


def full_parent(old,new,rom):
    ram_path=Path('E:/Rota Nova translations/Generated/work/emulation_v193/ceremony_v809_temple_preparations/frame_006600_arm9_ram.bin')
    ram=ram_path.read_bytes();patch_map=assembled()[0]
    entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),old)
    rows=[];max_rows=0
    for mode,seed in itertools.product((0,1,2),range(16)):
        outputs=[]
        for arm in (old,new):
            u=prepared(arm);u.mem_write(BASE,ram)
            if arm==new:
                for at,code in patch_map.items():u.mem_write(at,code)
            call(u,0xCB184,());actor=u.reg_read(UC_ARM_REG_R0)+36
            call(u,0x3F0F8,());manager=u.reg_read(UC_ARM_REG_R0)
            u.mem_write(manager+8,struct.pack('<I',1 if mode==1 else 0))
            u.mem_write(0x02168EB8,struct.pack('<I',seed))
            ids=0x02420000;u.mem_write(ids,struct.pack('<6I',*range(6)))
            template=ids+64;u.mem_write(template,entries[97].text+b'\0')
            notices=[];headers=[]

            def boundary(cpu,pc,size,unused):
                args=[cpu.reg_read(r) for r in REGS[:4]]
                if pc==BASE+0x5528C:
                    if args[0]!=97:return
                    cpu.reg_write(UC_ARM_REG_R0,template)
                elif pc==BASE+0x5473C:
                    notices.append(bytes(cpu.mem_read(args[0],256)).split(b'\0')[0])
                    cpu.reg_write(UC_ARM_REG_R0,0)
                elif pc==BASE+0x546B8:
                    assert args[0]==335
                    headers.append(('modal335',bytes(cpu.mem_read(args[1],64)).split(b'\0')[0]))
                    cpu.reg_write(UC_ARM_REG_R0,0)
                elif pc==BASE+0x05E4C:
                    headers.append(('popup97',bytes(cpu.mem_read(args[0],128)).split(b'\0')[0]))
                    cpu.reg_write(UC_ARM_REG_R0,0)
                else:
                    assert pc==0x021096F8
                    cpu.reg_write(UC_ARM_REG_R0,0)
                cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))

            handles=[u.hook_add(UC_HOOK_CODE,boundary,begin=p,end=p) for p in
                     (BASE+0x5528C,BASE+0x5473C,BASE+0x546B8,BASE+0x05E4C,0x021096F8)]
            try:call(u,0x7E2E8,(actor,ids,6,int(mode!=0)),instruction_limit=1000000)
            finally:
                for h in handles:u.hook_del(h)
            outputs.append(dict(notices=notices,headers=headers,R0=u.reg_read(UC_ARM_REG_R0),
                RAM=bytes(u.mem_read(BASE,0x800000)),actor=actor))
        a,b=outputs
        assert a['headers']==b['headers'] and a['R0']==b['R0']
        assert len(a['notices'])==len(b['notices'])==int(mode==1)
        if a['notices']:
            source=a['notices'][0];expected=b' '+b'\n  '.join(source.rstrip(b'\n').split(b'\n'))
            assert b['notices']==[expected]
            max_rows=max(max_rows,len(expected.split(b'\n')))
        restored=bytearray(b['RAM'])
        for at,code in patch_map.items():restored[at-BASE:at-BASE+len(code)]=a['RAM'][at-BASE:at-BASE+len(code)]
        # The source routine owns this full stack frame and callees' scratch.
        # Compare all remaining8MiB, including every persistent object and PRNG.
        lo,hi=0x027EE000-BASE,0x027F0000-BASE
        restored[lo:hi]=a['RAM'][lo:hi]
        assert bytes(restored)==a['RAM'],(mode,seed,'memory beyond owned code/stack differs')
        rows.append(dict(mode=mode,seed=seed,full_original_CActor_builder_completed=True,
            complete8MiB_except_owned_code_and_function_stack_exact=True,
            original_growth_amounts_actor_changes_and_PRNG_exact=True,
            original_header_output_and_all_saved_registers_exact=True,
            guarded_notice_hex=b['notices'][0].hex() if b['notices'] else None))
    assert len(rows)==48 and max_rows==6
    save(ROOT/'full_parent_contracts.json',dict(count=len(rows),cases=rows,maximum_actual_native_builder_rows=max_rows,
        source_RAM=str(ram_path),source_RAM_sha256=sha(ram),
        synthetic_inputs='Six native attribute IDs (both source EXP groups), seed0..15, original manager header selector0/1 and show0/1.',
        IO_boundaries='Blocking modal335/raw notice, popup97, sound; only COMMON97 getter supplied because resident dump contains block4.',
        real_class_growth_RNG_stat_setters_names_fullwidth_number_printf_strcat_and_post_growth_effects_executed=True,
        no_claim_of_earned_six_stat_growth_or_actual_GPU_pagination=True,
        source_ARM9_sha256=sha(old),research_ARM9_sha256=sha(new)))
    print('48 full original CActor builder/ABI/whole8MiB contracts pass; genuine six-row source output covered.',flush=True)


def main():
    rom=NdsImage.open('out/all_routes_combined_v809_candidate.nds');old=rom.read_file('/__arm9__.bin')
    arm=(ROOT/'ARM9_RESEARCH_ONLY.bin').read_bytes();assert arm==apply(old)
    header_contract(old,arm)
    compound_contract(arm,rom)
    full_parent(old,arm,rom)


if __name__=='__main__':main()
