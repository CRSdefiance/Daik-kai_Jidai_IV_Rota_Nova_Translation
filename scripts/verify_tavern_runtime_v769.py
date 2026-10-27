"""Execute prospective dispatch/providers with original ARM946 semantics."""

import struct
from itertools import product
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0,
    UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
    UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R9, UC_ARM_REG_SP)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_editorial import DIRECT,YESNO,LITERAL
from dk4tool.patch.region_name_boundaries import LABELS,TABLE
from dk4tool.rom.nds import NdsImage
from scripts.context_tavern_continuation_v768 import CURRENT,RAM_REPORT,REGIONS
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE,STACK,STOP,SAVED
from scripts import tavern_continuation_runtime_v769 as rt
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/tavern_runtime_v769')


def make(arm,changed=False,raw=None):
    u=machine(arm)
    if raw is not None:u.mem_write(BASE,raw)
    if changed:rt.load_into_cpu(u,arm)
    return u


def cstring(u,at):return bytes(u.mem_read(at,256)).split(b'\0')[0]
def ptr(u,at):return struct.unpack('<I',u.mem_read(at,4))[0]


def scope_cases(arm):
    targets=(LITERAL,rt.COORD,0x01FFCF40)
    def new():
        pair=[make(arm),make(arm,True)]
        for u in pair:
            for at in targets:u.hook_add(UC_HOOK_CODE,lambda c,p,s,d:c.emu_stop(),begin=at,end=at)
        return pair
    def run(u,parent,n,queue=0x021184C0,word=0):
        u.mem_write(STACK+0x260,b'\x77'*64)
        for off,value in ((0x264,parent),(0x274,n),(0x270,word),(0x27C,queue)):
            u.mem_write(STACK+off,struct.pack('<I',value))
        u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_LR,STOP)
        for reg,value in zip((UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3),(0x02410000,0x02411000,0,0xFEED1003)):
            u.reg_write(reg,value)
        for i,reg in enumerate(SAVED):u.reg_write(reg,0xA5A51000+i)
        u.emu_start(0x01FFCF3C,STOP,count=500)
        assert u.reg_read(UC_ARM_REG_PC) in targets,hex(u.reg_read(UC_ARM_REG_PC))
        assert u.reg_read(UC_ARM_REG_SP)==STACK and u.reg_read(UC_ARM_REG_LR)==STOP
        assert all(u.reg_read(reg)==0xA5A51000+i for i,reg in enumerate(SAVED))
        assert [u.reg_read(r) for r in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2)]==[0x02410000,0x02411000,0]
        return {'target':u.reg_read(UC_ARM_REG_PC),'r3':u.reg_read(UC_ARM_REG_R3)}
    rows=[];changed=[];pair=None
    def check(parent,n,queue=0x021184C0,word=0):
        nonlocal pair
        if len(rows)%512==0:pair=new()
        old,new_result=[run(u,parent,n,queue,word) for u in pair]
        expected=(parent==0x02054014 and 851<=n<=882
            or parent==0x02053D24 and queue==0x02118400
            or parent==0x02053C14 and word in (0x021166F0,0x02116810))
        if expected:assert new_result['target']==LITERAL
        else:assert new_result==old,(hex(parent),n,hex(queue),hex(word),old,new_result)
        row={'parent':parent,'id':n,'queue':queue,'word':word,'prior':old,'prospective':new_result,'new_membership':expected}
        rows.append(row)
        if old!=new_result:changed.append(row)
    for parent,queue,n in product((0x02054014,0x02053FCC,0x02054044,0x02053D24,0x02053DB8),(0x02118400,0x02118460,0x021184C0),range(3668)):
        check(parent,n,queue)
    for parent,word,n in product((0x02053C14,0x02053C5C),
            (0,825,0x02116610,0x021166E0,0x021166F0,0x02116810,0x0211660F,0x02116611,0x021166D0,0x02116710,0x02116811,0xFFFFFFFF),
            (0,825,850,851,859,862,864,867,882,3667,0xFFFFFFFF)):
        check(parent,n,word=word)
    save(ROOT/'dispatch_matrix.json',{'count':len(rows),'cases':rows,'changed_scope_count':len(changed),
        'only_direct851_882_queue53D24_table118400_and_round_gift_tables_are_new':True,
        'all_prior_targets_r3_input_registers_callee_saved_SP_LR_preserved':True})
    return len(rows)


def providers(arm,raw):
    u=make(arm,True,raw);source=make(arm,False,raw)
    rows=[]
    for n in range(-3,260):
        call(u,rt.REGION-BASE,(n&0xFFFFFFFF,))
        at=u.reg_read(UC_ARM_REG_R0)
        if 0<=n<7:
            value=cstring(u,ptr(u,at));assert value==REGIONS[n].encode('ascii')
            rows.append({'index':n,'full_phrase':value.decode('ascii'),'record_pointer':at})
        else:
            call(source,0x945B4,(n&0xFFFFFFFF,))
            assert at==source.reg_read(UC_ARM_REG_R0)
    for i,label in enumerate(LABELS):
        field=BASE+TABLE+i*52
        assert cstring(u,ptr(u,field))==label.encode('ascii')
        assert bytes(u.mem_read(field+4,48))==bytes(source.mem_read(field+4,48))
    events=[]
    def observe(cpu,pc,size,unused):
        n=cpu.reg_read(UC_ARM_REG_R1);count={863:2,870:3,878:2}[n]
        fields=[cpu.reg_read(UC_ARM_REG_R2),cpu.reg_read(UC_ARM_REG_R3),ptr(cpu,cpu.reg_read(UC_ARM_REG_SP))]
        events.append({'id':n,'args':[cstring(cpu,p).hex() for p in fields[:count]]});cpu.emu_stop()
    handle=u.hook_add(UC_HOOK_CODE,observe,begin=BASE+0x53FE4,end=BASE+0x53FE4)
    context=read('work/analysis/tavern_continuation_v768/native_context_partial.json')
    # Paired source/prospective fragments use the same copied native objects.
    cases=[]
    try:
        for n in (863,870):
            for item in context['real_item_names_and_native_regions']:
                region=item['original_region_index']
                if not 0<=region<7:continue
                events.clear();u.reg_write(UC_ARM_REG_SP,STACK)
                if n==863:
                    for r,v in ((UC_ARM_REG_R5,region),(UC_ARM_REG_R6,item['object'])):u.reg_write(r,v)
                    lo,hi=0x59950,0x59994
                else:
                    # Native copied captain and native scene NPC are unmodified.
                    original=next(c for c in context['original_provider_fragments'] if c['id']==870 and c['item_ID']==item['index'] and c['supplied_route']==1)
                    call(u,0xB6618,());town=u.reg_read(UC_ARM_REG_R0)
                    call(u,0xB2CD8,(town,13));npc=u.reg_read(UC_ARM_REG_R0)
                    for r,v in ((UC_ARM_REG_R4,item['object']),(UC_ARM_REG_R5,npc),(UC_ARM_REG_R9,region)):u.reg_write(r,v)
                    lo,hi=0x5829C,0x582F0
                u.emu_start(BASE+lo,BASE+hi,count=10000)
                assert len(events)==1 and events[0]['id']==n
                expected=[item['name_hex'],REGIONS[region].encode().hex()]
                if n==870:expected=[original['arguments_hex'][0],*expected]
                assert events[0]['args']==expected,(n,item,events)
                cases.append(events[0])
        for company in context['real_company_names']:
            for address in (b'Sir',b"Ma'am"):
                events.clear();u.mem_write(0x02473000,address+b'\0');u.reg_write(UC_ARM_REG_SP,STACK)
                for r,v in ((UC_ARM_REG_R4,company['object']),(UC_ARM_REG_R5,0x02473100),(UC_ARM_REG_R6,0x02473000)):u.reg_write(r,v)
                u.emu_start(BASE+0x58060,BASE+0x58084,count=10000)
                assert events==[{'id':878,'args':[address.hex(),company['name_hex']]}],events
                cases.append(events[0])
    finally:u.hook_del(handle)
    save(ROOT/'provider_verification.json',{'all263_region_values_private_or_original_fallback':True,
        'private_regions':rows,'all8_UI_strings_and48byte_metadata_exact':True,
        'actual_original_caller_fragments':cases,'source_values_preserved_except_full_region_phrase_and878_exact_permutation':True,
        'no_global_region_getter_or_UI_wording_change':True})
    return len(cases)


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    rom=NdsImage.open(CURRENT);arm=rom.read_file('/__arm9__.bin')
    assert sha(arm)==rt.SOURCE
    raw=snapshot(read(RAM_REPORT),3200)
    count=scope_cases(arm);print(f'{count} complete paired dispatcher/ABI cases pass.',flush=True)
    fields=providers(arm,raw);print(f'{fields} original provider fragments and263 region cases pass.',flush=True)
    save(ROOT/'runtime_verification.json',{'source_ROM_sha256':sha(CURRENT.read_bytes()),'source_ARM9_sha256':sha(arm),
        'paired_dispatch_cases':count,'provider_fragments':fields,'module_sha256':sha(Path(rt.__file__).read_bytes()),
        'prototype_blobs':{hex(a):b.hex() for a,b in rt.assemble(arm).items()},
        'ownership_and_registered_integration_gameplay_still_pending':True,'full_goal_complete':False})


if __name__=='__main__':main()
