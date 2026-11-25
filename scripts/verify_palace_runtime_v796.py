"""Exact parent/ID routing and private-bank compaction, without a ROM build."""

import inspect
import struct
from pathlib import Path
from types import FunctionType

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_SP,UC_ARM_REG_LR

from dk4tool.patch import palace_editorial_runtime as new
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.shipyard_editorial import LITERAL
from dk4tool.rom.nds import NdsImage
from scripts import research_scheme_selector_v775 as old_scope
from scripts import verify_recruitment_runtime_v771 as old_status
from scripts.audit_item_runtime_storage_v785 import census
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE,STACK,STOP
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/palace_runtime_v796')
ROM = Path('out/all_routes_combined_v792_candidate.nds')


def scope(arm):
    cpu = prepared(arm)
    targets = (0x01FFCF40,LITERAL,new.bank.COORD,new.bank.STATUS)
    hooks = [cpu.hook_add(UC_HOOK_CODE,lambda c,p,s,d:c.emu_stop(),begin=t,end=t) for t in targets]
    records = {p:(off,high,set(values)) for p,off,high,values in new.contract_rows()}
    count = 0
    def check(parent,number,queue=0,gift=0):
        nonlocal count
        regs = {r:0xA5A50000+i for i,r in enumerate(old_scope.REGS)}
        for r,v in regs.items(): cpu.reg_write(r,v)
        cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP)
        fields = {0x274:number,0x27C:queue,0x270:gift}
        for off,value in ((0x264,parent),*fields.items()):
            cpu.mem_write(STACK+off,struct.pack('<I',value))
        cpu.emu_start(new.bank.ENTRY,STOP,count=10000)
        route = 0x01FFCF40
        if parent in records:
            off,high,allowed = records[parent];value = fields[off]
            if value>>16 == high and value&65535 in allowed:
                n = value&65535
                route = new.bank.COORD if not high and n in (842,1028,1029) else new.bank.STATUS if not high and n in (905,906) else LITERAL
        assert cpu.reg_read(UC_ARM_REG_PC) == route,(hex(parent),number,hex(queue),hex(gift),hex(cpu.reg_read(UC_ARM_REG_PC)),hex(route))
        assert cpu.reg_read(UC_ARM_REG_SP) == STACK and cpu.reg_read(UC_ARM_REG_LR) == STOP
        for reg,value in regs.items():
            expected = parent if reg == old_scope.UC_ARM_REG_R3 and route == 0x01FFCF40 else value
            assert cpu.reg_read(reg) == expected
        count += 1
    try:
        for parent in (0x02053D24,0x02053DB8):
            for low in range(0x7B20,0x8490):
                for number in (0,1072,1117,3667): check(parent,number,0x02110000|low)
        for parent in (0x02054014,0x02053FCC,0x02053C5C,0x02053E38):
            for number in range(3668): check(parent,number,number,number)
        for low in range(0x65F0,0x6840): check(0x02053C14,0,gift=0x02110000|low)
        for parent in (*records,0,0xffffffff,0x12053D24,0x02053EAC,0x02053EF4,0x02053F40,0x02054048):
            for high in (0,0x0211,0x1211,0xffff):
                for low in (0,842,905,1073,1117,1166,0x6610,0x66F0,0x7F60,0x80A0,0x80B0,0x8160,0xffff):
                    value=high<<16|low;check(parent,1156,value,value)
    finally:
        for h in hooks: cpu.hook_del(h)
    save(ROOT/'scope_proof.json',{'cases':count,'all_exact_parent_ID_pointer_stride_ABI_SP_LR_cases_pass':True,
        'new_ordinary_IDs':list(range(1146,1177)),'new_yes_no_IDs':[1166],
        'all_other_contract_sets_unchanged':True,'gate_instructions_byte_identical_only_table_literal_moves':True,
        'private_data_allocation_bytes':168,'table_used_bytes':130,'table_halfword_aligned':True,
        'twelve_phrase_indices_bytes':24,'complete_luxury_goods_including_NUL_bytes':13,'alignment_byte':1,
        'no_production_ROM_or_gameplay_claim':True})
    print(f'{count} exact Palace and prior selector/ABI cases pass.',flush=True)


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin')
    assert sha(arm)=='efde1eeffac95af843f489c6ff388a950cc1faabccce9f0962ce54ca32de8bc5'
    target=new.apply(arm);changes=new.patches(arm)
    owned=read('work/analysis/recruitment_owned_v772/owned_runtime_plan.json')['private_spans']
    assert all(any(lo<=at and at+len(data)<=hi for lo,hi in owned) for at,data in changes.items())
    restored=bytearray(target)
    for at,data in changes.items(): restored[at-BASE:at-BASE+len(data)] = arm[at-BASE:at-BASE+len(data)]
    assert bytes(restored)==arm
    a,b=[MainCodeFile(v,BASE) for v in (arm,target)]
    shape=lambda c:[(s.ramAddress,len(s.data),s.bssSize) for s in c.sections]
    assert shape(a)==shape(b) and bytes(a.sections[3].data)==bytes(b.sections[3].data)
    assert len(b.sections[3].data)-48==123040 and cache_plan(arm)==cache_plan(target)
    before_gate=arm[new.bank.GATE-BASE:new.bank.GATE-BASE+168]
    after_gate=target[new.bank.GATE-BASE:new.bank.GATE-BASE+168]
    assert after_gate.replace(struct.pack('<I',new.CONTRACTS),struct.pack('<I',new.bank.CONTRACTS))==before_gate
    after=NdsImage.open(ROM);after.rom.arm9=target
    span=[[new.LUXURY_GOODS,new.END]]
    before_refs,after_refs=[census(r,span,owned) for r in (rom,after)]
    external=lambda rows:sorted(r for r in rows if not r[-1])
    assert external(before_refs)==external(after_refs),(external(before_refs),external(after_refs))
    save(ROOT/'bounded_compaction.json',{'source_ROM_sha256':sha(ROM.read_bytes()),
        'source_ARM9_sha256':sha(arm),'target_ARM9_sha256':sha(target),
        'patches':[{'address':at,'source_hex':arm[at-BASE:at-BASE+len(data)].hex(),'target_hex':data.hex()} for at,data in changes.items()],
        'existing_private_spans':owned,'compacted_data_span':[new.LUXURY_GOODS,new.END],
        'before_reference_census':before_refs,'after_reference_census':after_refs,
        'external_references_exact':True,'all_changes_inside_previous_owned_allocations':True,
        'sections_BSS_cache_and_staged123040_bytes_exact':True,
        'producer_sha256':sha(Path('scripts/verify_palace_runtime_v796.py').read_bytes()),
        'runtime_sha256':sha(Path('dk4tool/patch/palace_editorial_runtime.py').read_bytes()),
        'no_ROM_build_or_gameplay_claim':True})
    (ROOT/'ARM9_RUNTIME_RESEARCH_ONLY.bin').write_bytes(target)
    scope(target)
    # Replay the existing native status-output contract after moving its packed
    # table and luxury-goods string. Keep the original function frozen.
    def make(source,changed=False,raw=None):
        cpu=prepared(source)
        if raw is not None: cpu.mem_write(BASE,raw)
        return cpu
    source=inspect.getsource(old_status.field_contracts)
    source=source.replace('u.emu_start(runtime.STATUS,STOP','u.emu_start(runtime.STATUS|1,STOP')
    source=source.replace('STACK-BASE-32:STACK-BASE','STACK-BASE-36:STACK-BASE')
    env={**old_status.__dict__,'runtime':new.bank,'make':make,
         'ROOT':Path('work/analysis/tavern_recruitment_editorial_v771')}
    exec(compile(source,__file__,'exec'),env)
    cases=env['field_contracts'](target)
    assert len(cases)==140
    save(ROOT/'status_contracts.json',{'count':len(cases),'cases':cases,
        'all_whole8MiB_guards_original_status_UI_labels_and_registers_SP_LR_exact':True,
        'effective_verifier_sha256':sha(source.encode())})
    print('140 whole8MiB status-output and ABI cases pass.',flush=True)


if __name__=='__main__':main()
