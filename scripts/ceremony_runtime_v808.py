"""Ceremony runtime packing in the already-proven384 source-owned bytes.

Research only: no production registration, COMMON change or playable ROM.
"""

import struct
from pathlib import Path

from keystone import Ks,KS_ARCH_ARM,KS_MODE_ARM,KS_MODE_THUMB
from ndspy.code import MainCodeFile

from dk4tool.patch import inn_editorial_runtime as previous
from dk4tool.patch.arrival_notices_editorial import modal_code as old_modal_code
from dk4tool.patch import captain_prompt_wrap as modal
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.shipyard_editorial import LITERAL as OLD_LITERAL
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

BASE=0x02000000
ROOT=Path('work/analysis/ceremony_runtime_v808')
ROM=Path('out/all_routes_combined_v803_candidate.nds')
SOURCE='41d4f8ef7d751dc90d40e5c29a17fea3a1080775604573d07175edd45ed2be71'
bank=previous.bank
LITERAL=previous.CONTRACTS
STATUS=LITERAL+88
CONTRACTS=OLD_LITERAL+4
TABLE_USED=174
TABLE_BYTES=174
PACKED_PHRASES=CONTRACTS+TABLE_BYTES
END=bank.STATUS+80
MODAL_FILTER=PACKED_PHRASES+24
MODAL_IDS=(289,290,291,293,294,295)


def contract_rows():
    proof=read('work/analysis/ceremony_layout_v807_name_bounds/runtime_size_measurement.json')
    assert proof['candidate_sha256']=='7c6c8bb3c89973af2f789488e51bff395d871be6a461490d62b3f5c8d860daad'
    return [(r['parent'],r['stack_field'],r['high'],tuple(r['proposed_values'])) for r in proof['seven_exact_contract_rows']]


def table():
    data=bytearray()
    for parent,offset,high,values in contract_rows():
        shift=(4 if parent==0x02053C14 else 5) if high else 0
        assert all(not n&((1<<shift)-1) for n in values)
        keys=sorted((n>>shift)-512 if high else n for n in values);ranges=[]
        for key in keys:
            if ranges and key==ranges[-1][1]+1:ranges[-1]=(ranges[-1][0],key)
            else:ranges.append((key,key))
        words=[]
        for lo,hi in ranges:
            while lo<=hi:
                end=min(lo+31,hi);assert 0<=lo<=end<2048
                words.append(lo|((end-lo)<<11));lo=end+1
        field=(offset+24-0x180)//4
        data.extend(struct.pack('<HBB',parent&65535,field|(128 if high else 0),len(words)))
        data.extend(struct.pack('<'+'H'*len(words),*words))
    assert len(data)==TABLE_USED
    return bytes(data)+bytes(TABLE_BYTES-TABLE_USED)


def literal_code():
    ka,kt=Ks(KS_ARCH_ARM,KS_MODE_ARM),Ks(KS_ARCH_ARM,KS_MODE_THUMB)
    stub=bytes(ka.asm(f'ldr ip,[pc];bx ip;.word {LITERAL+13}',LITERAL)[0])
    asm='''push {r4,lr}
mov r4,r0
blx 0x01ff9fac
sub sp,#240
mov r0,r4
ldrb r3,[r0]
cmp r3,#32
beq ready
blx 0x020ced28
mov r2,r0
mov r0,r4
cmp r2,#237
bhi ready
shift:
ldrb r3,[r0,r2]
adds r1,r2,#1
strb r3,[r0,r1]
subs r2,#1
bpl shift
movs r3,#32
strb r3,[r0]
ready:
mov r0,r4
add r1,sp,#0
ldr r3,helper
blx r3
cmp r0,#0
beq done
adds r2,r0,#1
mov r0,r4
add r1,sp,#0
blx 0x020cec74
done:
movs r0,#0
add sp,#240
pop {r4,pc}
.align 2
helper: .word 0x02147ae5
'''
    body=bytes(kt.asm(asm,LITERAL+12)[0]);assert len(stub)==12 and len(stub)+len(body)==88
    return stub+body,asm


def status_code(arm):
    old=arm[bank.STATUS-BASE:bank.STATUS-BASE+80]
    # Retain exact original UI table, article and shortage-prefix constants.
    ui,article,prefix,phrases=struct.unpack_from('<4I',old,64)
    assert ui==0x02156430 and phrases==previous.PACKED_PHRASES
    asm=f'''push {{r0-r7,lr}}
mov r4,r1
ldr r5,[sp,#0x2a0]
ldr r6,UI_table
movs r2,#0
find:
ldr r0,[r6,r2]
cmp r0,r5
beq found
adds r2,#4
cmp r2,#48
blo find
b done
found:
lsrs r6,r2,#1
mov r0,r5
blx 0x020ced28
mov r5,r0
mov r0,r4
blx 0x020ced28
adds r4,r4,r0
subs r4,#8
subs r4,r4,r5
cmp r6,#10
ldr r5,article
blo prefix_ready
ldr r5,prefix
prefix_ready:
ldr r7,phrases
b {bank.STATUS_TAIL}
done:
blx {bank.STATUS_RETURN}
.align 2
UI_table: .word {ui}
article: .word {article}
prefix: .word {prefix}
phrases: .word {PACKED_PHRASES}
'''
    code=bytes(Ks(KS_ARCH_ARM,KS_MODE_THUMB).asm(asm,STATUS)[0]);assert len(code)==80
    return code,asm


def modal_code():
    # The14-byte filter normalizes to ID289,then maps only the six source-
    # proven ceremony IDs to the already balanced ID346 path. ID292 retains
    # its original unselected path. Every other ID receives the same net
    # subtraction as the old wrapper before the321/327/346-348 tests.
    helper='''subs r3,#20
cmp r3,#6
bhi done
cmp r3,#3
beq done
movs r3,#57
done:
bx lr
'''
    filt=bytes(Ks(KS_ARCH_ARM,KS_MODE_THUMB).asm(helper,MODAL_FILTER)[0])
    assert len(filt)==14 and MODAL_FILTER+len(filt)==END
    _,asm=old_modal_code();assert asm.count('subs r3,#52')==1
    asm=asm.replace('subs r3,#52',f'bl {MODAL_FILTER}\nsubs r3,#32')
    stub=bytes(Ks(KS_ARCH_ARM,KS_MODE_ARM).asm(f'ldr ip,[pc];bx ip;.word {modal.ADDRESS+13}',modal.ADDRESS)[0])
    body=bytes(Ks(KS_ARCH_ARM,KS_MODE_THUMB).asm(asm,modal.ADDRESS+12)[0])
    assert len(stub)+len(body)==modal.SIZE==128
    return stub+body,filt,asm,helper


def patches(arm):
    assert sha(arm)==SOURCE
    assert arm[previous.CONTRACTS-BASE:previous.PACKED_PHRASES-BASE]==previous.table()
    words=arm[previous.PACKED_PHRASES-BASE:previous.END-BASE]
    assert len(words)==24
    literal,_=literal_code();status,_=status_code(arm)
    private=literal+status;assert len(private)==168 and LITERAL+len(private)==previous.END
    trampoline=bytes(Ks(KS_ARCH_ARM,KS_MODE_ARM).asm(f'b {LITERAL}',OLD_LITERAL)[0])
    wrapper,filt,_,_=modal_code()
    public=trampoline+table()+words+filt
    assert len(public)==216 and OLD_LITERAL+len(public)==END
    result={LITERAL:private,OLD_LITERAL:public}
    old=struct.pack('<I',previous.CONTRACTS)
    gate=arm[bank.GATE-BASE:bank.GATE-BASE+164];assert gate.count(old)==1
    result[bank.GATE+gate.index(old)]=struct.pack('<I',CONTRACTS)
    entry=arm[bank.STATUS_EXIT-BASE:bank.STATUS_EXIT-BASE+16]
    pointer=struct.pack('<I',bank.STATUS|1);assert entry.count(pointer)==1
    result[bank.STATUS_EXIT+entry.index(pointer)]=struct.pack('<I',STATUS|1)
    return result


def apply(arm):
    out=bytearray(arm)
    for at,raw in patches(arm).items():out[at-BASE:at-BASE+len(raw)]=raw
    # The ITCM section is stored after the main ARM9 allocation rather than at
    # its runtime address in the file. Update it through the section model.
    code=MainCodeFile(bytes(out),BASE);section=code.sections[4]
    assert section.ramAddress==0x01FFC000 and len(section.data)==4096
    off=modal.ADDRESS-section.ramAddress
    assert bytes(section.data[off:off+modal.SIZE])==old_modal_code()[0]
    section.data[off:off+modal.SIZE]=modal_code()[0]
    return bytes(code.save())


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');target=apply(arm)
    old,new=[MainCodeFile(a,BASE) for a in (arm,target)]
    geometry=lambda c:[(s.ramAddress,len(s.data),s.bssSize) for s in c.sections]
    assert geometry(old)==geometry(new) and cache_plan(arm)==cache_plan(target)
    assert all(bytes(old.sections[n].data)==bytes(new.sections[n].data) for n in (1,2,3))
    restored_itcm=bytearray(new.sections[4].data);off=modal.ADDRESS-old.sections[4].ramAddress
    restored_itcm[off:off+modal.SIZE]=old.sections[4].data[off:off+modal.SIZE]
    assert bytes(restored_itcm)==bytes(old.sections[4].data)
    assert len(new.sections[3].data)-48==123040
    assert target[bank.GATE-BASE:bank.GATE-BASE+152]==arm[bank.GATE-BASE:bank.GATE-BASE+152]
    path=ROOT/'ARM9_RESEARCH_ONLY.bin';path.write_bytes(target)
    save(ROOT/'prospective_runtime_plan.json',dict(source_ARM9_sha256=sha(arm),research_ARM9_sha256=sha(target),
        existing_owned_banks=[[previous.CONTRACTS,previous.END],[OLD_LITERAL,END]],
        new_literal=[LITERAL,STATUS],new_status=[STATUS,previous.END],
        retained_literal_entry_trampoline=[OLD_LITERAL,CONTRACTS],new_table=[CONTRACTS,CONTRACTS+TABLE_BYTES],
        new_phrase_array=[PACKED_PHRASES,PACKED_PHRASES+24],
        existing_dispatch_instructions_unchanged=True,seven_exact_parent_contracts=True,
        only_two_private_pointer_literals_redirected=True,
        complete_section_BSS_cache_and_staged123040_bytes_unchanged=True,
        ROM_modified=False,COMMON_modified=False,ownership_refresh_native_equivalence_and_production_dispatch_pending=True,
        modal_ceremony_scope_added=list(MODAL_IDS),modal_source_owned_filter=[MODAL_FILTER,END],
        existing_ITCM_wrapper=[modal.ADDRESS,modal.ADDRESS+modal.SIZE],modal_ASM=modal_code()[2],modal_filter_ASM=modal_code()[3],
        patches=[dict(address=at,size=len(raw),sha256=sha(raw)) for at,raw in patches(arm).items()],
        literal_ASM=literal_code()[1],status_ASM=status_code(arm)[1],
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(f'Prospective384-byte bank packing:88-byte literal,80-byte status,4-byte entry,174-byte table,24-byte phrases,14-byte modal filter;existing128-byte wrapper. ARM9 {sha(target)}. No ROM/COMMON change;native verification pending.',flush=True)


if __name__=='__main__':main()
