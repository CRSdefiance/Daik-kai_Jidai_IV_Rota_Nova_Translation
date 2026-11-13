"""Bound original Market call sites and investment/price decision fragments."""

import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R8,
    UC_ARM_REG_R10,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, machine
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/market_replies_v753')
CALLS={747:(0xBC980,0xBC988),748:(0xBC938,0xBC93C),749:(0xC2B6C,0xC2B70),753:(0xBC22C,0xBC234),
    762:(0xBC920,0xBC928),763:(0xBC910,0xBC918),764:(0xBB084,0xBB088),765:(0xBBC24,0xBBC28),766:(0xBBC30,0xBBC34)}
SPANS=((0xBC894,0xBCA4C),(0xBB02C,0xBB098),(0xBBBF0,0xBBC40),(0xC2B20,0xC2B9C),(0xBC220,0xBC244))


def selections(arm):
    cases=[]
    for mode,start,regs,expected,terminal in (
        *[('investment_share',0xBC908,{UC_ARM_REG_R10:share,UC_ARM_REG_R5:0x02450000},[763 if share>0 else 762],BASE+0x53FE4) for share in (-1,0,1)],
        *[('investment_funds',0xBC92C,{UC_ARM_REG_R8:cash,UC_ARM_REG_R4:100,UC_ARM_REG_R5:0x02450000},[748] if cash<100 else [],BASE+(0x53FE4 if cash<100 else 0xBC948)) for cash in (99,100,101)],
        *[('investment_entry_result',0xBC968,{UC_ARM_REG_R0:amount,UC_ARM_REG_R5:0x02450000},[747] if amount else [746],BASE+0x53FE4) for amount in (0,500)],
        *[('report_funds',0xBB050,{UC_ARM_REG_R0:cash,UC_ARM_REG_R4:100,UC_ARM_REG_R5:0x02450000},[764] if cash<100 else [],BASE+(0x53FE4 if cash<100 else 0xBB058)) for cash in (99,100,101)]):
        cpu=machine(arm);events=[]
        def stop(u,address,size,unused,events=events,terminal=terminal):
            if address==BASE+0x53FE4:
                events.append(u.reg_read(UC_ARM_REG_R1))
            if address==terminal:u.emu_stop()
        hook=cpu.hook_add(UC_HOOK_CODE,stop)
        try:
            cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,0x027E0000)
            for reg,value in regs.items():cpu.reg_write(reg,value&0xffffffff)
            cpu.emu_start(BASE+start,0x027E0000,count=1000)
        finally:cpu.hook_del(hook)
        assert cpu.reg_read(UC_ARM_REG_PC)==terminal and events==expected,(mode,regs,events)
        cases.append({'mode':mode,'start':BASE+start,'supplied_registers':{str(k):v for k,v in regs.items()},'message_IDs':events,'stop':terminal})
    return cases


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    current=NdsImage.open('out/all_routes_combined_v752_candidate.nds').read_file('/__arm9__.bin')
    assert all(clean[a:b]==current[a:b] for a,b in SPANS)
    cs=Cs(CS_ARCH_ARM,CS_MODE_ARM);cs.detail=True
    bindings=[]
    for number,(start,end) in CALLS.items():
        instructions=list(cs.disasm(clean[start:end+4],BASE+start));first,last=instructions[0],instructions[-1]
        assert last.mnemonic=='bl' and last.op_str=='#0x2053fe4'
        literal=None
        if first.mnemonic=='mov':assert first.operands[1].imm==number
        else:
            assert first.mnemonic=='ldr' and first.op_str.startswith('r1, [pc,')
            literal=first.address+8+first.operands[1].mem.disp-BASE
            assert struct.unpack_from('<I',clean,literal)[0]==number
        bindings.append({'message_id':number,'load':BASE+start,'call':BASE+end,'literal':BASE+literal if literal else None,'original_parent_return':0x02054014})
    a,b=selections(clean),selections(current);assert a==b
    save(ROOT/'native_context.json',{'source_spans':[{'start':a,'end':b,'sha256':sha(clean[a:b])} for a,b in SPANS],
        'nine_original_direct_portrait_bindings':bindings,'eleven_decision_fragments_each_clean_and_current':a,
        'supplied_states_and_input_amount_no_whole_transaction_or_earned_progress_claim':True,
        'source755_760_voice_family_and761_city_question_not_in_this_batch':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Nine original Market call bindings and11 clean/current decision fragments pass.',flush=True)


if __name__=='__main__':main()
