"""Compact exact-key scheme selector prototype; no playable ROM is written."""

import struct
from pathlib import Path

from keystone import KS_ARCH_ARM,KS_MODE_ARM,KS_MODE_THUMB,Ks
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,
    UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,
    UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_SP)

from dk4tool.patch import recruitment_editorial_runtime as prior
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_editorial import LITERAL
from dk4tool.rom.nds import NdsImage
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE,STACK,STOP
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/tavern_scheme_selector_v775')
NEW_NARRATION=(0x7B40,0x82C0,0x8300,0x8320,0x8340)
NEW_CONFIRM=(0x8260,0x8280,0x82A0)
REGS=(UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,
    UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,
    UC_ARM_REG_R10,UC_ARM_REG_R11)


def contract_rows():
    rows=[]
    for parent,offset,high,ranges in prior.CONTRACT_ROWS:
        values=list(ranges)
        if parent==0x02053DB8:values.extend((n,n) for n in NEW_NARRATION)
        if parent==0x02053D24:values.extend((n,n) for n in NEW_CONFIRM)
        rows.append((parent,offset,high,tuple(sorted(values))))
    return rows


def assemble():
    table=bytearray()
    for parent,offset,high,ranges in contract_rows():
        field=(offset+24-0x180)//4
        assert 0<=field<128 and high in (0,0x0211)
        encoded=[]
        for lo,hi in ranges:
            if high:
                assert lo==hi and not(lo&15)
                encoded.append(lo>>4)
            else:
                while lo<=hi:
                    end=min(lo+15,hi)
                    assert 0<=lo<=end<4096
                    encoded.append(lo|((end-lo)<<12))
                    lo=end+1
        table.extend(struct.pack('<HBB',parent&65535,field|(128 if high else 0),len(encoded)))
        table.extend(struct.pack('<'+'H'*len(encoded),*encoded))
    assert len(table)==100
    # Every item packs a12-bit low key and4-bit interval delta. Exact pointer
    # keys are divided by16 only after rejecting every unaligned low nibble.
    assembly=f'''
ldr r3,[sp,#0x27c]
ldr r4,parent_base
subs r3,r3,r4
lsrs r5,r3,#16
bne fallback
ldr r4,contracts
movs r5,#7
parents:
ldrh r6,[r4]
cmp r3,r6
beq matched
ldrb r7,[r4,#3]
lsls r7,r7,#1
adds r4,#4
adds r4,r4,r7
subs r5,#1
bne parents
b fallback
matched:
ldrb r3,[r4,#2]
lsrs r6,r3,#7
negs r6,r6
ldr r7,field_high
ands r6,r7
lsls r3,r3,#25
lsrs r3,r3,#23
add r5,sp,#0x180
ldr r3,[r5,r3]
lsrs r7,r3,#16
cmp r6,r7
bne fallback
lsls r3,r3,#16
lsrs r3,r3,#16
ldrb r5,[r4,#3]
adds r4,#4
cmp r6,#0
beq ranges
lsls r7,r3,#28
bne fallback
lsrs r3,r3,#4
ranges:
ldrh r6,[r4]
lsls r7,r6,#20
lsrs r7,r7,#20
subs r7,r3,r7
lsrs r6,r6,#12
cmp r7,r6
bls selected
adds r4,#2
subs r5,#1
bne ranges
fallback:
blx {prior.ORIGINAL_EXIT}
selected:
ldr r4,coord_ID
subs r4,r3,r4
beq coordinate
subs r4,#63
cmp r4,#1
bls status
blx {prior.LITERAL_EXIT}
coordinate:
blx {prior.COORD_EXIT}
status:
blx {prior.STATUS_EXIT}
.align 2
parent_base: .word 0x02050000
contracts: .word {prior.CONTRACTS}
coord_ID: .word 842
field_high: .word 0x0211
'''
    code=bytes(Ks(KS_ARCH_ARM,KS_MODE_THUMB).asm(assembly,prior.GATE)[0])
    return bytes(table),code,assembly


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    rom_path=Path('out/all_routes_combined_v773_candidate.nds')
    arm=NdsImage.open(rom_path).read_file('/__arm9__.bin')
    table,code,assembly=assemble()
    # This diagnostic saves size even if a new arrangement is still required.
    save(ROOT/'prototype.json',{'source_ROM_sha256':sha(rom_path.read_bytes()),
        'table_bytes':len(table),'gate_bytes':len(code),'table_hex':table.hex(),'gate_hex':code.hex(),
        'assembly_sha256':sha(assembly.encode()),'point_keys_are_exact_not_pointer_intervals':True,
        'no_production_storage_or_integration_approval':True,'full_goal_complete':False})
    assert len(code)<=144
    u=machine(arm)
    constants=bytes(u.mem_read(prior.STATUS_CONSTANTS,24))
    packed=bytes(u.mem_read(prior.PACKED_PHRASES,24))
    u.mem_write(prior.GATE,code)
    u.mem_write(prior.CONTRACTS,table)
    assert bytes(u.mem_read(prior.STATUS_CONSTANTS,24))==constants
    assert bytes(u.mem_read(prior.PACKED_PHRASES,24))==packed
    targets=(0x01FFCF40,LITERAL,prior.COORD,prior.STATUS)
    hooks=[u.hook_add(UC_HOOK_CODE,lambda c,p,s,d:c.emu_stop(),begin=t,end=t) for t in targets]
    def check(parent,n,queue=0,gift=0):
        values={r:0xA5A50000+i for i,r in enumerate(REGS)}
        for r,v in values.items():u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,STACK)
        u.reg_write(UC_ARM_REG_LR,STOP)
        for offset,value in ((0x264,parent),(0x270,gift),(0x274,n),(0x27C,queue)):
            u.mem_write(STACK+offset,struct.pack('<I',value))
        u.emu_start(prior.ENTRY,STOP,count=10000)
        route=0x01FFCF40
        for p,off,high,ranges in contract_rows():
            value={0x274:n,0x27C:queue,0x270:gift}[off]
            if p==parent and value>>16==high and any(lo<=value&65535<=hi for lo,hi in ranges):
                low=value&65535
                route=prior.COORD if low==842 else prior.STATUS if low in (905,906) else LITERAL
        assert u.reg_read(UC_ARM_REG_PC)==route,(hex(parent),n,hex(queue),hex(gift),hex(u.reg_read(UC_ARM_REG_PC)),hex(route))
        assert u.reg_read(UC_ARM_REG_SP)==STACK
        assert u.reg_read(UC_ARM_REG_LR)==STOP
        assert all(u.reg_read(r)==v for r,v in values.items() if r!=UC_ARM_REG_R3 or route!=0x01FFCF40)
        if route==0x01FFCF40:assert u.reg_read(UC_ARM_REG_R3)==parent
    count=0
    try:
        for parent in (0x02053D24,0x02053DB8):
            for low in range(0x7B20,0x8490):
                for n in (0,908,940,3667):
                    check(parent,n,0x02110000|low)
                    count+=1
        # All numeric IDs in every unchanged parent/field contract.
        for parent in (0x02054014,0x02053FCC,0x02053C5C,0x02053E38):
            for n in range(3668):
                check(parent,n,queue=n,gift=n)
                count+=1
        for parent in (0x02053C14,0x02054014,0x02053DB8,0x02053D24,0x02053FCC,0,0xFFFFFFFF):
            for gift in (0,0x02116610,0x021166E0,0x021166F0,0x02116810,0x02118260,0x021182E0):
                for queue in (0,904,0x02118380,0x02118260,0x021182E0,0x12118260,0xFFFFFFFF):
                    check(parent,950,queue,gift)
                    count+=1
    finally:
        for h in hooks:u.hook_del(h)
    save(ROOT/'scope_proof.json',{'cases':count,'table_bytes':len(table),
        'gate_bytes':len(code),'native_production_addresses_in_CPU_only':True,
        'exact_new_five_narration_three_confirmation_tables':True,
        'unreviewed_021182E0_and_all_between_table_addresses_rejected':True,
        'registers_SP_and_original_fallback_argument_preserved':True,
        'original_status_constants_and_packed_phrase_pointers_preserved':True,
        'source_ROM_unchanged':sha(rom_path.read_bytes()),'producer_sha256':sha(Path(__file__).read_bytes()),
        'full_goal_complete':False})
    assert len(code)<=144
    print(f'{count} scope/register cases pass;table{len(table)} bytes,gate{len(code)} bytes;existing-bank sizes fit. Production ownership/integration pending.',flush=True)


if __name__=='__main__':main()
