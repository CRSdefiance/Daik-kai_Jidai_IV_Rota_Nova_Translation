"""Native exact dispatch/ABI, reference, modal and status regressions.

This writes a research ARM9 only. It does not build a ROM, approve fonts,
simulate a successful battle event, or grant editorial completion credit.
"""
import struct
from pathlib import Path
from types import FunctionType

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_R3, UC_ARM_REG_R12

from dk4tool.patch import recruitment_editorial_runtime as bank
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_editorial import LITERAL
from dk4tool.rom.nds import NdsImage
from scripts import battle_aftermath_runtime_v1253 as runtime
from scripts import escape_direct_runtime_v1183b as old_runtime
from scripts import verify_sighting_runtime_v1076 as historical
from scripts.audit_item_runtime_storage_v785 import census
from scripts.verify_escape_direct_runtime_v1184b import literal_accesses
from scripts.verify_arrival_native_v792 import prepared
from scripts.research_scheme_selector_v775 import REGS
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_aftermath_runtime_v1254')
ROM = Path('out/all_routes_combined_v1224_candidate.nds')


def scope(arm):
    cpu = prepared(arm)
    targets = (0x01FFCF40, LITERAL, bank.COORD, bank.STATUS)
    hooks = [cpu.hook_add(UC_HOOK_CODE, lambda c,p,s,d: c.emu_stop(), begin=t, end=t) for t in targets]
    records = {p: (o,h,set(v)) for p,o,h,v in runtime.contract_rows()}
    regs = {r: 0xA5A50000+i for i,r in enumerate(REGS)}
    count = 0

    def check(parent, fields, whole_memory=False):
        nonlocal count
        for reg,value in regs.items():
            cpu.reg_write(reg,value)
        cpu.reg_write(UC_ARM_REG_R12, 0xABCD1234)
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.reg_write(UC_ARM_REG_LR, STOP)
        cpu.mem_write(STACK-64, b'\x96'*128)
        for offset,value in ((0x264,parent),*fields.items()):
            cpu.mem_write(STACK+offset, struct.pack('<I',value))
        before = bytes(cpu.mem_read(BASE,0x800000)) if whole_memory else None
        cpu.emu_start(bank.ENTRY, STOP, count=10000)
        route = 0x01FFCF40
        if parent in records:
            offset,high,allowed = records[parent]
            value = fields[offset]
            if value >> 16 == high and value & 65535 in allowed:
                n = value & 65535
                route = bank.COORD if not high and n in (842,1028,1029) else bank.STATUS if not high and n in (905,906) else LITERAL
        actual = cpu.reg_read(UC_ARM_REG_PC)
        assert actual == route, (hex(parent), fields, hex(actual), hex(route))
        assert cpu.reg_read(UC_ARM_REG_SP) == STACK and cpu.reg_read(UC_ARM_REG_LR) == STOP
        assert cpu.reg_read(UC_ARM_REG_R12) == bank.GATE|1
        for reg,value in regs.items():
            expected = parent if reg == UC_ARM_REG_R3 and route == 0x01FFCF40 else value
            assert cpu.reg_read(reg) == expected, (reg,parent,fields)
        assert bytes(cpu.mem_read(STACK-64,40)) == b'\x96'*40
        assert bytes(cpu.mem_read(STACK,64)) == b'\x96'*64
        expected_stack = b''.join(struct.pack('<I',regs[r]) for r in REGS[3:8])+struct.pack('<I',STOP)
        assert bytes(cpu.mem_read(STACK-24,24)) == expected_stack
        if whole_memory:
            after = bytearray(cpu.mem_read(BASE,0x800000))
            after[STACK-24-BASE:STACK-BASE] = before[STACK-24-BASE:STACK-BASE]
            assert bytes(after) == before
        count += 1
        return targets.index(route)

    exhaustive = []
    try:
        for parent,(offset,high,allowed) in records.items():
            bitmap = bytearray()
            for low in range(65536):
                fields = {0x270:0xDEADBEEF,0x274:0xDEADBEEF,0x27C:0xDEADBEEF}
                fields[offset] = high<<16|low
                bitmap.append(check(parent,fields))
            exhaustive.append({'parent':parent,'selector_stack_offset':offset,'high_word':high,
                'cases':65536,'route_bitmap_sha256':sha(bitmap),'allowed_keys':sorted(allowed)})
            print(hex(parent)+': all65536 original-entry selector/ABI cases pass.',flush=True)
        controls = 0
        for parent,(offset,high,allowed) in records.items():
            lows = sorted(allowed | {0,1,127,128,255,256,383,384,65535,2192})
            for wrong_high in (0,1,0x0205,0x0210,0x0211,0x0212,0x1211,0xFFFF):
                for low in lows:
                    fields = {0x270:0xDEADBEEF,0x274:0xDEADBEEF,0x27C:0xDEADBEEF}
                    fields[offset] = wrong_high<<16|low
                    check(parent,fields)
                    controls += 1
            for other_parent in (0,0xFFFFFFFF,parent ^ 0x10000000,parent ^ 0x00010000,parent+1):
                for low in lows:
                    fields = {0x270:0xDEADBEEF,0x274:0xDEADBEEF,0x27C:0xDEADBEEF}
                    fields[offset] = high<<16|low
                    check(other_parent,fields)
                    controls += 1
            for low in (0,min(allowed),max(allowed),65535):
                fields = {0x270:0xDEADBEEF,0x274:0xDEADBEEF,0x27C:0xDEADBEEF}
                fields[offset] = high<<16|low
                check(parent,fields,True)
        save(ROOT/'scope_proof.json',{'exhaustive_rows':exhaustive,
            'all524288_native_low_word_cases':sum(r['cases'] for r in exhaustive),
            'additional_parent_high_word_and_selector_high_word_controls':controls,
            'whole8MiB_memory_guards':32,'total_cases':count,
            'all_exact_routes_SP_LR_saved_registers_R12_and24_stack_bytes':True,
            'only_actual_selector_field_set_other_two_fields_poisoned':True,
            'source_and_target_only13_exact_new_memberships':True,
            'CPU_only_not_actual_gameplay':True})
    finally:
        for h in hooks:
            cpu.hook_del(h)


def main():
    assert not ROOT.exists()
    rom = NdsImage.open(ROM)
    assert sha(ROM.read_bytes()) == 'cdc860e53267dbef64ac9d40a1832b00fda6a4da6adbde2b61be830345d55dbd'
    old = rom.read_file('/__arm9__.bin')
    target,plan = runtime.apply(old)
    old_rows = {p:(o,h,set(v)) for p,o,h,v in old_runtime.contract_rows()}
    added = {}
    for parent,offset,high,values in runtime.contract_rows():
        o,h,prior = old_rows[parent]
        assert (o,h) == (offset,high) and prior <= set(values)
        if set(values) != prior:
            added[hex(parent)] = sorted(set(values)-prior)
    assert sum(map(len,added.values())) == 13
    owned = read('work/analysis/recruitment_owned_v772/owned_runtime_plan.json')['private_spans']
    assert all(any(lo <= a and b <= hi for lo,hi in owned) for a,b in plan['private_spans'])
    other = NdsImage.open(ROM)
    other.rom.arm9 = target
    refs = [census(r,plan['private_spans'],plan['private_spans']) for r in (rom,other)]
    external = lambda rows: sorted(r for r in rows if not r[-1])
    assert external(refs[0]) == external(refs[1]), [external(r) for r in refs]
    accesses = [literal_accesses(r,plan['private_spans']) for r in (rom,other)]
    outside = lambda rows: sorted(r for r in rows if not any(lo <= r[2] < hi for lo,hi in plan['private_spans']))
    assert outside(accesses[0]) == outside(accesses[1])
    # Nothing external may address an old internal row or instruction/literal.
    assert all(r[3] in (runtime.CONTRACTS,runtime.GATE,runtime.GATE|1) for r in external(refs[0]))
    assert not outside(accesses[0])
    ROOT.mkdir(parents=True)
    output = ROOT/'ARM9_RUNTIME_RESEARCH_ONLY.bin'
    output.write_bytes(target)
    save(ROOT/'runtime_plan.json',{**plan,'research_ARM9':str(output),'new_memberships':added,
        'source_ROM_sha256':sha(ROM.read_bytes()),'source_owned_spans':owned,
        'source_target_absolute_branch_ADR_reference_census':refs,
        'source_target_PC_relative_load_store_census':accesses,
        'all_external_references_exact_no_internal_row_or_gate_tail_references':True,
        'runtime_module_sha256':sha(Path(runtime.__file__).read_bytes())})
    scope(target)
    for fn in (historical.modal_equivalence,historical.status):
        bound = FunctionType(fn.__code__,{**fn.__globals__,'ROOT':ROOT},argdefs=fn.__defaults__)
        bound(old,target) if fn is historical.modal_equivalence else bound(target)
    proofs = [ROOT/p for p in ('runtime_plan.json','scope_proof.json','modal_equivalence.json','status_contracts.json')]
    save(ROOT/'native_runtime_verification.json',{'source_ROM':str(ROM),'source_ROM_sha256':sha(ROM.read_bytes()),
        'source_ARM9_sha256':sha(old),'target_ARM9_sha256':sha(target),
        'proofs':{str(p):sha(p.read_bytes()) for p in proofs},
        'native_exact_dispatch_ABI_memory_and_external_reference_proven':True,
        'all3668_modal238_parent5_edge_and140_whole_memory_status_regressions_pass':True,
        'no_section_BSS_cache_ITCM_or123040_staged_growth':True,
        'no_ROM_registry_or_editorial_completion_change':True,
        'font_matrix_native_source_pipelines_and_actual_gameplay_still_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Research-only aftermath decoder, exact scope and historical regressions pass.',flush=True)


if __name__ == '__main__':
    main()
