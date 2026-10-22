"""Source coordinate equivalence, exact call scope and bounded native stat layouts."""

import argparse
import itertools
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
    UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11,
    UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.levelup_format_runtime_v818 import ROOT,BASE,START,END,HOOK,apply,patches
from scripts.native_call_abi_v764 import call
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

REGS = (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,
        UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,
        UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,
        UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR)


def coordinate_contract(old, new):
    machines = [prepared(a) for a in (old,new)]
    stack = 0x02470000; cases = []
    bounds = (-1024,-1,0,1,255,256,511,-2147483648,2147483647)
    vectors = [(x,y,x2,y2) for x,y,x2,y2 in itertools.product((-1,0,1,255,256),repeat=4)]
    vectors += [(x,y,z,w) for x,y,z,w in zip(bounds,bounds[::-1],bounds[2:]+bounds[:2],bounds[4:]+bounds[:4])]
    for index,vector in enumerate(vectors):
        outputs = []
        for cpu in machines:
            cpu.reg_write(UC_ARM_REG_CPSR,0xA0000010)
            for n,reg in enumerate(REGS):
                cpu.reg_write(reg,(0x5A001234+n*0x123+index)&0xFFFFFFFF)
            cpu.reg_write(UC_ARM_REG_SP,stack)
            cpu.mem_write(stack,b'\xA5'*96)
            cpu.mem_write(stack+40,struct.pack('<4i',*vector))
            cpu.emu_start(START,END,count=200)
            assert cpu.reg_read(UC_ARM_REG_PC)==END and not cpu.reg_read(UC_ARM_REG_CPSR)&0x20
            outputs.append(([cpu.reg_read(reg) for reg in REGS],bytes(cpu.mem_read(BASE,0x800000))))
        for n in (0,1,2,*range(4,12),13,14):
            assert outputs[0][0][n]==outputs[1][0][n],(index,n)
        restored = bytearray(outputs[1][1])
        for at,data in patches(old).items():
            restored[at-BASE:at-BASE+len(data)] = old[at-BASE:at-BASE+len(data)]
        assert outputs[0][1]==bytes(restored),(index,'outside RECT or code differs')
        assert outputs[0][0][0]==97
        cases.append(dict(input_rectangle=vector,result_words=list(struct.unpack('<4I',machines[1].mem_read(stack+24,16))),
                          entire8MiB_except_owned_code_exact=True,SP_LR_R0_R1_R2_and_R4_R11_exact=True))
    save(ROOT/'coordinate_contracts.json',dict(cases=cases,count=len(cases),
        R3_IP_and_condition_flags_dead_before_original_single_argument_Common97_getter=True,
        no_claim_that_dead_volatiles_remain_identical=True,
        source_ARM9_sha256=sha(old),research_ARM9_sha256=sha(new)))
    print(f'{len(cases)} coordinate/whole8MiB/ARM-return contracts pass.',flush=True)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--layouts-only',action='store_true',help='Reuse exact source/target coordinate proof; do not weaken or rerun that gate.')
    args=parser.parse_args()
    rom=NdsImage.open('out/all_routes_combined_v809_candidate.nds');old=rom.read_file('/__arm9__.bin')
    new=(ROOT/'ARM9_RESEARCH_ONLY.bin').read_bytes();assert new==apply(old)
    if args.layouts_only:
        prior=read(ROOT/'coordinate_contracts.json')
        assert prior['source_ARM9_sha256']==sha(old) and prior['research_ARM9_sha256']==sha(new)
        assert prior['count']==len(prior['cases'])==634
        assert all(c['entire8MiB_except_owned_code_exact'] and c['SP_LR_R0_R1_R2_and_R4_R11_exact'] for c in prior['cases'])
    else:
        coordinate_contract(old,new)
    growth=read(ROOT/'source_growth_catalog.json');assert growth['native_computed_increment_upper_bound']==3
    names=growth['names']['current'];assert len(names)==6
    cpu=prepared(new);buffer=0x02430000;received=[]

    def print_boundary(u,pc,size,data):
        assert pc==BASE+0x5473C and u.reg_read(UC_ARM_REG_R0)==buffer
        received.append(bytes(u.mem_read(buffer,768)).split(b'\0')[0])
        u.reg_write(UC_ARM_REG_R0,0x5A5A)
        u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))

    hook=cpu.hook_add(UC_HOOK_CODE,print_boundary,begin=BASE+0x5473C,end=BASE+0x5473C)
    cases=[];fonts=[];findings=[]
    try:
        for amounts in itertools.product(range(4),repeat=6):
            if not any(amounts):continue
            parts=[f'{name} increased by {amount}!'.replace(str(amount),chr(0xFF10+amount)).encode('cp932')
                   for name,amount in zip(names,amounts,strict=True) if amount]
            raw=b'\n'.join(parts)+b'\n'
            cpu.mem_write(buffer-16,b'\xA5'*816);cpu.mem_write(buffer,raw+b'\0');received.clear()
            before_rng=bytes(cpu.mem_read(0x02168EB8,4))
            call(cpu,0x7E3F1,(buffer,),instruction_limit=3000000)
            assert len(received)==1 and cpu.reg_read(UC_ARM_REG_R0)==0x5A5A
            result=received[0];assert b' '.join(result.split())==b' '.join(raw.split())
            assert bytes(cpu.mem_read(buffer-16,16))==b'\xA5'*16
            # In-place prefix insertion shifts the old NUL by one. A shorter
            # balanced result may leave that harmless NUL beyond its new NUL.
            # Both writes must remain inside the original 768-byte buffer.
            owned_end=max(len(raw)+2,len(result)+1)
            assert owned_end<=768
            assert bytes(cpu.mem_read(buffer+owned_end,800-owned_end))==b'\xA5'*(800-owned_end)
            assert bytes(cpu.mem_read(0x02168EB8,4))==before_rng
            lines=[s.strip().decode('cp932') for s in result.split(b'\n')]
            good=result.startswith(b' ') and not result.endswith(b'\n') and len(lines)<=4 and all(s.startswith(b'  ') for s in result.split(b'\n')[1:])
            case=dict(amounts=list(amounts),raw_hex=raw.hex(),formatted_hex=result.hex(),lines=lines,
                complete_words_substituted_numbers_and_buffer_guards=True,
                original_raw_print_callee_receives_once_and_ABI_RNG_preserved=True,guarded_four_row_layout=good)
            cases.append(case)
            if not good:findings.append(case)
            if all(n in (0,3) for n in amounts):
                plane=raster(new,result,0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
                assert plane==independent_font(new,rom.read_file('/GRP/KANJI.FNT'),lines)
                fonts.append(dict(amounts=list(amounts),complete_native_and_independent_font_match=True))
    finally:
        cpu.hook_del(hook)
    assert len(cases)==4095 and len(fonts)==63
    save(ROOT/'all_stat_layouts.json',dict(cases=cases,count=len(cases),findings=findings,findings_count=len(findings),
        source_increment_domain=[0,3],native_source_maximum3_proof=str(ROOT/'source_growth_catalog.json'),
        six_original_English_names_preserved=True,native_whole_fonts=fonts,
        research_ARM9_sha256=sha(new),producer_sha256=sha(Path(__file__).read_bytes()),
        original_full_parent_empty_message_and_actual_GPU_checks_pending=True))
    print(f'4095 native compound calls and63 complete font planes;{len(findings)} layout findings. Actual caller/full-parent/GPU checks pending.',flush=True)
    assert not findings


if __name__=='__main__':
    main()
