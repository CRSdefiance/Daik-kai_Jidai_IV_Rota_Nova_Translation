"""Native equivalence and caller closure for consolidated private runtime."""

import inspect
import re
import struct
from pathlib import Path
from types import FunctionType

from capstone import CS_ARCH_ARM,CS_MODE_THUMB,Cs
from unicorn.arm_const import UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_R0,UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_editorial import QUANTITY,PRICE_RETURNS,DAY_RETURN
from dk4tool.rom.nds import NdsImage
from scripts import recruitment_owned_runtime_v772 as runtime
from scripts import verify_recruitment_runtime_v771 as prior
from scripts.context_tavern_recruitment_v771 import CURRENT,RAM_REPORT
from scripts.inventory_shipyard_storage_v760 import units
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE,STACK,SAVED
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/recruitment_owned_v772')


def make(arm,changed=False,raw=None):
    u=machine(arm)
    if raw is not None:u.mem_write(BASE,raw)
    if changed:runtime.load(u)
    return u


def quantity_closure(rom):
    external=[];aliases=[];adr=[];thumb=[]
    lo,hi=QUANTITY,QUANTITY+188
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    for name,base,raw in units(rom)+[('ARM7',rom.rom.arm7RamAddress,bytes(rom.rom.arm7))]:
        for m in re.finditer(rb'(?=(...\x02))',raw,re.DOTALL):
            target=int.from_bytes(m.group(1),'little')
            if lo<=target<hi and not lo<=base+m.start()<hi:aliases.append([name,base+m.start(),target])
        for at in range(0,len(raw)-3,4):
            word=struct.unpack_from('<I',raw,at)[0];pc=base+at
            if word&0x0E000000==0x0A000000:
                delta=word&0xffffff
                if delta&0x800000:delta-=0x1000000
                target=pc+8+delta*4
                if lo<=target<hi and not lo<=pc<hi:external.append([name,pc,target,hex(word)])
            if word&0x0E0F0000==0x020F0000 and (word>>21)&15 in(2,4):
                v,shift=word&255,((word>>8)&15)*2
                v=((v>>shift)|(v<<(32-shift)))&0xffffffff if shift else v
                target=pc+8+(v if (word>>21)&15==4 else -v)
                if lo<=target<hi and not lo<=pc<hi:adr.append([name,pc,target])
        for at in range(0,len(raw)-3,2):
            first,second=struct.unpack_from('<HH',raw,at)
            if first&0xF800!=0xF000 or second&0xF800 not in(0xE800,0xF800):continue
            inst=next(cs.disasm(raw[at:at+4],base+at),None)
            if inst is None or inst.mnemonic not in('bl','blx') or not inst.op_str.startswith('#'):continue
            target=int(inst.op_str[1:],0)&~1
            if lo<=target<hi and not lo<=base+at<hi:thumb.append([name,base+at,target])
    expected=sorted(('section0',pc-4,QUANTITY) for pc in (*PRICE_RETURNS,DAY_RETURN))
    save(ROOT/'quantity_caller_closure.json',{'exact_seven_ARM_BLs':external,'absolute_aliases':aliases,
        'external_ADR_leads':adr,'external_Thumb_BL_BLX_leads':thumb,
        'private_helper_has_no_public_unregistered_caller_contract':True})
    assert sorted((n,a,t) for n,a,t,_ in external)==expected,external
    assert all(int(word,16)>>24==0xEB for *_,word in external)
    assert not aliases and not adr and not thumb,(aliases,adr,thumb)


def quantities(arm,raw):
    cases=[]
    for caller in (*PRICE_RETURNS,DAY_RETURN):
        for amount in(0,1,2,9,10,99,100,9999,65535,999999,2147483647,0xffffffff):
            results=[]
            for changed in(False,True):
                u=make(arm,changed,raw)
                for i,reg in enumerate(SAVED):u.reg_write(reg,0xA5A50000+i)
                u.reg_write(UC_ARM_REG_R0,amount);u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_LR,caller)
                u.emu_start(QUANTITY,caller,count=100000)
                assert u.reg_read(UC_ARM_REG_PC)==caller and u.reg_read(UC_ARM_REG_SP)==STACK
                assert all(u.reg_read(reg)==0xA5A50000+i for i,reg in enumerate(SAVED))
                at=u.reg_read(UC_ARM_REG_R0);value=bytes(u.mem_read(at,128)).split(b'\0')[0]
                results.append((at,value.hex(),u.reg_read(UC_ARM_REG_LR)))
            assert results[0]==results[1],(hex(caller),amount,results)
            cases.append({'caller':caller,'supplied_amount':amount,'returned_pointer':results[0][0],
                'complete_native_result_hex':results[0][1],'callee_saved_SP_LR_exact':True})
    save(ROOT/'quantity_equivalence.json',{'count':len(cases),'cases':cases,'scope':'All seven proven source callers;synthetic numeric bounds included. No public/unregistered-call equivalence claimed.'})


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    rom=NdsImage.open(CURRENT);arm=rom.read_file('/__arm9__.bin');raw=snapshot(read(RAM_REPORT),3200)
    quantity_closure(rom);quantities(arm,raw)
    print('Exact seven-caller closure and84 native quantity equivalence cases pass.',flush=True)
    env=dict(prior.__dict__);env.update({'runtime':runtime,'ROOT':ROOT,'make':make})
    adapter=inspect.getsource(prior.scopes)
    marker='    namespace=dict(previous_scope.__globals__)'
    replacement='''    source=source.replace('for u in pair:', 'for j,u in enumerate(pair):')
    source=source.replace('for at in targets:u.hook_add', 'for at in targets:\\n                if j==0 and at==runtime.STATUS:continue\\n                u.hook_add')
'''+marker
    assert adapter.count(marker)==1;adapter=adapter.replace(marker,replacement)
    exec(compile(adapter,str(Path(__file__)),'exec'),env)
    count=env['scopes'](arm)
    print(f'{count} paired native dispatch/register cases pass.',flush=True)
    source=inspect.getsource(prior.field_contracts)
    source=source.replace('u.emu_start(runtime.STATUS,STOP','u.emu_start(runtime.STATUS|1,STOP')
    source=source.replace('STACK-BASE-32:STACK-BASE','STACK-BASE-36:STACK-BASE')
    source=source.replace('and32_stack_bytes','and36_stack_bytes')
    env['ROOT']=Path('work/analysis/tavern_recruitment_editorial_v771')
    exec(compile(source,str(Path(__file__)),'exec'),env)
    contracts=env['field_contracts'](arm)
    save(ROOT/'typed_status_contracts.json',{'count':len(contracts),'cases':contracts,
        'prototype_code_hex':{hex(a):b.hex() for a,b in runtime.assemble().items()},
        'runtime_source_sha256':sha(Path(runtime.__file__).read_bytes()),
        'quantity_source_sha256':sha(Path('scripts/recruitment_quantity_v772.py').read_bytes()),
        'source_ROM_sha256':sha(CURRENT.read_bytes()),'producer_sha256':sha(Path(__file__).read_bytes()),
        'all_storage_ownership_registered_integration_and_gameplay_pending':True,'full_goal_complete':False})
    print(f'{len(contracts)} whole8MiB status/register contracts pass;storage and integration still pending.',flush=True)


if __name__=='__main__':main()
