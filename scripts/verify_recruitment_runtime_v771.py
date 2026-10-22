"""Scope,original saved argument slot,and whole8MiB typed-field contracts."""

import inspect
import struct
from pathlib import Path
from types import SimpleNamespace

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_R0,UC_ARM_REG_R1,
    UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_SP)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_editorial import LITERAL
from dk4tool.rom.nds import NdsImage
from scripts import recruitment_runtime_research_v771 as runtime
from scripts.context_tavern_recruitment_v771 import CURRENT,RAM_REPORT,ROOT
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE,STACK,STOP,SAVED
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_tavern_runtime_v769 import scope_cases as previous_scope
from scripts.verify_village_wrap_v608 import read,save


def make(arm,changed=False,raw=None):
    u=machine(arm)
    if raw is not None:u.mem_write(BASE,raw)
    if changed:runtime.load(u)
    return u


def scopes(arm):
    source=inspect.getsource(previous_scope)
    a=source.index('        expected=(');b=source.index('        if expected:',a)
    source=source[:a]+'''        expected=(parent==0x02054014 and n in (905,906,907)
            or parent==0x02053D24 and queue==0x02118380
            or parent==0x02053DB8 and queue in (0x02118360,0x021183A0)
            or parent==0x02053E38 and queue==904)
'''+source[b:]
    source=source.replace("if expected:assert new_result['target']==LITERAL", "if expected:assert new_result['target']==(runtime.STATUS if parent==0x02054014 and n in(905,906) else LITERAL)")
    source=source.replace('targets=(LITERAL,rt.COORD,0x01FFCF40)','targets=(LITERAL,rt.COORD,0x01FFCF40,runtime.STATUS)')
    source=source.replace('(0x02118400,0x02118460,0x021184C0),range(3668)', '(0x02118360,0x02118380,0x021183A0,0x02118400,0x02118460,0x021184C0),range(3668)')
    marker='    save(ROOT/\'dispatch_matrix.json\''
    assert source.count(marker)==1
    source=source.replace(marker,"    for selected_ID,unrelated in product(range(3668),(0,904,905,3667,0xFFFFFFFF)):\n        check(0x02053E38,unrelated,queue=selected_ID)\n"+marker)
    source=source.replace("'only_direct851_882_queue53D24_table118400_and_round_gift_tables_are_new'", "'only_direct905_907_three_role_voice_tables_and_role_direct904_are_new'")
    namespace=dict(previous_scope.__globals__)
    namespace.update({'make':make,'ROOT':ROOT,'runtime':runtime,'rt':SimpleNamespace(COORD=0x02147A78)})
    exec(compile(source,str(Path(__file__)),'exec'),namespace)
    count=namespace['scope_cases'](arm)
    save(ROOT/'dispatch_adapter.json',{'frozen_source':str(Path(inspect.getfile(previous_scope))),
        'source_sha256':sha(Path(inspect.getfile(previous_scope)).read_bytes()),'effective_program_sha256':sha(source.encode()),
        'paired_scope_and_register_contracts':count,'explicit_new_memberships_only':True,'no_owned_storage_or_ROM_claim':True})
    return count


def direct_slot(arm,raw):
    u=make(arm,False,raw);seen=[]
    def loader(c,pc,size,unused):
        c.reg_write(UC_ARM_REG_R0,0x02479000);c.reg_write(UC_ARM_REG_PC,c.reg_read(UC_ARM_REG_LR))
    def prologue(c,pc,size,unused):
        # Both original core prologue instructions have executed at54060.
        at=c.reg_read(UC_ARM_REG_SP);saved=struct.unpack('<I',c.mem_read(at+0x27C,4))[0]
        seen.append({'SP_after_original_prologue':at,'saved_R3_status_pointer_at_27C':saved,
            'original_parent_return':c.reg_read(UC_ARM_REG_LR)});c.emu_stop()
    u.mem_write(0x02479000,b' Native template.\0')
    hs=[u.hook_add(UC_HOOK_CODE,loader,begin=BASE+0x5528C,end=BASE+0x5528C),
        u.hook_add(UC_HOOK_CODE,prologue,begin=BASE+0x54060,end=BASE+0x54060)]
    try:
        for n in(905,906):
            u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_LR,STOP)
            for r,v in((UC_ARM_REG_R0,0x02478000),(UC_ARM_REG_R1,n),(UC_ARM_REG_R2,0x02478100),(UC_ARM_REG_R3,0x02478200)):
                u.reg_write(r,v)
            u.emu_start(BASE+0x53FE4,STOP,count=1000)
            assert seen[-1]['SP_after_original_prologue']==STACK-24-0x268
            assert seen[-1]['saved_R3_status_pointer_at_27C']==0x02478200
            assert seen[-1]['original_parent_return']==0x02054014
    finally:
        for h in hs:u.hook_del(h)
    return seen


def field_contracts(arm):
    context=read(ROOT/'native_context.json')
    labels=[r['current_UI_label'].encode() for r in context['all13_source_status_names_and_UI_labels']]
    towns=(b'Oslo',b'Rio de Janeiro',b'Santo Domingo',b'North TEST Town',b'ABCDEFGHIJKLMNOPQRSTUVW')
    templates=(b' I hear %s has been experiencing %s lately.',b" Word is, %s's been going through %s lately.")
    cases=[]
    for template in templates:
        for town in towns:
            for index,label in enumerate(labels+[b'Unknown Test Label']):
                u=make(arm,True)
                output=0x02430000
                status=struct.unpack('<13I',u.mem_read(0x02156430,52))[index] if index<13 else 0x02431000
                if index==13:u.mem_write(status,label+b'\0')
                assert bytes(u.mem_read(status,len(label)+1))==label+b'\0'
                text=template.replace(b'%s',town,1).replace(b'%s',label,1)
                phrase=runtime.STATUS_PHRASES[index].encode() if index<12 else label
                expected=template.replace(b'%s',town,1).replace(b'%s',phrase,1)
                assert max(len(text),len(expected))<236
                u.mem_write(output-16,b'\xA5'*288);u.mem_write(output,text+b'\0')
                u.mem_write(STACK+0x27C,struct.pack('<I',status));u.mem_write(STACK-64,b'\x77'*64)
                regs={r:0xA5A50000+i for i,r in enumerate(SAVED)}
                for r,v in regs.items():u.reg_write(r,v)
                for r,v in((UC_ARM_REG_R0,0x02432000),(UC_ARM_REG_R1,output),(UC_ARM_REG_R2,0x1357),(UC_ARM_REG_R3,0x2468),
                        (UC_ARM_REG_LR,STOP),(UC_ARM_REG_SP,STACK)):u.reg_write(r,v)
                before=bytes(u.mem_read(BASE,0x800000))
                h=u.hook_add(UC_HOOK_CODE,lambda c,p,s,d:c.emu_stop(),begin=LITERAL,end=LITERAL)
                u.emu_start(runtime.STATUS,STOP,count=10000);u.hook_del(h)
                assert u.reg_read(UC_ARM_REG_PC)==LITERAL and u.reg_read(UC_ARM_REG_SP)==STACK and u.reg_read(UC_ARM_REG_LR)==STOP
                assert all(u.reg_read(r)==v for r,v in regs.items())
                assert [u.reg_read(r) for r in(UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3)]==[0x02432000,output,0x1357,0x2468]
                after=bytearray(u.mem_read(BASE,0x800000))
                assert bytes(after[output-BASE:output-BASE+len(expected)+1])==expected+b'\0'
                # Only the printed final field/suffix and32 saved stack bytes may differ.
                start=output-BASE+len(text)-len(label)-len(runtime.STATUS_SUFFIX)
                end=output-BASE+max(len(text),len(expected))+1
                after[start:end]=before[start:end]
                after[STACK-BASE-32:STACK-BASE]=before[STACK-BASE-32:STACK-BASE]
                assert bytes(after)==before
                assert bytes(u.mem_read(status,len(label)+1))==label+b'\0'
                cases.append({'template':template.decode(),'town':town.decode(),'original_UI_label':label.decode(),
                    'original_status_pointer':status,'localized_phrase':phrase.decode(),
                    'source_ineligible_Normal_or_unknown_pointer_falls_through':index>=12,
                    'entire8MiB_and_registers_preserved_except_typed_field_suffix_and32_stack_bytes':True})
    return cases


def main():
    arm=NdsImage.open(CURRENT).read_file('/__arm9__.bin');raw=snapshot(read(RAM_REPORT),3200)
    count=scopes(arm);print(f'{count} paired native scope/ABI cases pass.',flush=True)
    slots=direct_slot(arm,raw);contracts=field_contracts(arm)
    save(ROOT/'typed_status_contracts.json',{'count':len(contracts),'cases':contracts,
        'two_original_wrapper_core_prologue_status_slots':slots,
        'typed_phrase_expansion_after_original_printf_original_status_UI_and_town_names_preserved':True,
        'prototype_code_hex':{hex(a):b.hex() for a,b in runtime.code().items()},
        'source_ROM_sha256':sha(CURRENT.read_bytes()),'runtime_source_sha256':sha(Path(runtime.__file__).read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'production_storage_integration_gameplay_pending':True,'full_goal_complete':False})
    print(f'{len(contracts)} whole8MiB/register contracts and original direct-wrapper/prologue field slots pass.',flush=True)


if __name__=='__main__':main()
