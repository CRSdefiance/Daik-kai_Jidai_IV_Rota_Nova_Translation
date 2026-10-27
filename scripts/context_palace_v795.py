"""Original Palace speaker,argument,letter-state and monthly-price contracts."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,
    UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,
    UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_PC,
    UC_ARM_REG_SP,UC_ARM_REG_LR)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE,STACK,STOP
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/palace_editorial_v795')
ROM=Path('out/all_routes_combined_v792_candidate.nds')
RAM=Path('E:/Rota Nova translations/Generated/work/emulation_v193/palace_v794_context/frame_004800_arm9_ram.bin')
IDS=tuple(range(1146,1177))


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin');source=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=((0x5D644,0x5E1FC),(0x53CB0,0x54058),(0x82F18,0x82F84),(0xB508C,0xB50B8),(0xB521C,0xB5240),
        (0x3CD2C,0x3CD54),(0x4A410,0x4A44C),(0xB2CD8,0xB2D58))
    assert all(source[lo:hi]==arm[lo:hi] for lo,hi in spans)
    raw=RAM.read_bytes();cpu=machine(arm);cpu.mem_write(BASE,raw)
    def get(fn,args=()):call(cpu,fn,args,instruction_limit=200000);return cpu.reg_read(UC_ARM_REG_R0)
    def word(p):return struct.unpack('<I',cpu.mem_read(p,4))[0]
    def text(p):return bytes(cpu.mem_read(p,512)).split(b'\0')[0]
    def name(obj,slot):return text(get(word(word(obj)+slot)-BASE,(obj,)))
    town,actors,companies,items=get(0xB6618),get(0xCB184),get(0xCB160),get(0xCB190)
    ruler,minister=get(0xB2CD8,(town,6)),get(0xB2CD8,(town,11))
    assert (ruler-actors-4)//32==127 and (minister-actors-4)//32==121
    admiral=actors+0x19E4
    names=[{'actor_index':i,'address_form_hex':name(actors+4+i*32,0x24).hex()} for i in range(4)]
    player_address=name(admiral,0x24)
    peers=[]
    for n in range(20):
        company=companies+4+n*76
        if get(0x3A3B4,(company,))<=0:continue
        boss=get(0x3CD2C,(company,))
        peers.append({'company_index':n,'leader_address_hex':name(boss,0x24).hex()})
    letters=[]
    for mode in (0,1,2):
        before=bytes(cpu.mem_read(BASE,0x800000));old=word(admiral+0x68)
        get(0x82F18,(admiral,mode));new=word(admiral+0x68)
        assert get(0x82F60,(admiral,))==mode and old&~3==new&~3
        after=bytes(cpu.mem_read(BASE,0x800000));fixed=bytearray(after)
        fixed[admiral+0x68-BASE:admiral+0x6C-BASE]=before[admiral+0x68-BASE:admiral+0x6C-BASE]
        assert bytes(fixed)==before
        letters.append({'mode':mode,'meaning':('Market introduction letter','Market recommendation letter','no letter')[mode],
            'field':admiral+0x68,'old':old,'new':new,'original_getter_returns':mode,'only_two_flag_bits_change_whole8MiB_exact':True})
    # Restore the exact donor status before fragment observations.
    cpu.mem_write(admiral+0x68,raw[admiral+0x68-BASE:admiral+0x6C-BASE])
    observed=[];cases=[]
    def hook(c,pc,size,data):
        key=c.reg_read(UC_ARM_REG_R1);assert key in IDS,(hex(pc),key)
        argc=1 if key in (1147,1149,1151,1154,1156,1166) else 0
        argument=text(c.reg_read(UC_ARM_REG_R2)) if argc else b''
        observed.append({'wrapper':pc,'speaker':c.reg_read(UC_ARM_REG_R0),'id':key,'argument_hex':argument.hex()})
        c.emu_stop()
    hooks=[cpu.hook_add(UC_HOOK_CODE,hook,begin=BASE+n,end=BASE+n) for n in (0x53FE4,0x53F9C)]
    registers=(UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,
        UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12)
    def run(start,n,values=(),stack=()):
        observed.clear()
        for reg in registers:cpu.reg_write(reg,0)
        cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP)
        for reg,v in values:cpu.reg_write(reg,v)
        for at,v in stack:cpu.mem_write(STACK+at,struct.pack('<I',v))
        cpu.emu_start(BASE+start,STOP,count=200000)
        assert len(observed)==1 and observed[0]['id']==n,(hex(start),n,observed)
        row={'source_fragment':BASE+start,**observed[0]}
        assert row['speaker'] in (ruler,minister),(hex(start),row,hex(ruler),hex(minister),hex(word(BASE+0x5DC90)),word(word(BASE+0x5DC90)+0x10))
        cases.append(row);return row
    try:
        for start,n,reg,speaker in ((0x5DF78,1146,UC_ARM_REG_R0,minister),(0x5DFF0,1148,UC_ARM_REG_R4,minister),
            (0x5E080,1162,UC_ARM_REG_R4,minister),(0x5E0AC,1157,UC_ARM_REG_R5,ruler),
            (0x5E0F0,1158,UC_ARM_REG_R5,ruler),(0x5DDB4,1158,UC_ARM_REG_R6,ruler),
            (0x5DDC8,1160,UC_ARM_REG_R6,ruler),(0x5DECC,1161,UC_ARM_REG_R6,ruler),
            (0x5DE10,1173,UC_ARM_REG_R6,ruler),(0x5DA60,1170,UC_ARM_REG_R5,ruler),
            (0x5DA6C,1171,UC_ARM_REG_R5,ruler),(0x5DA94,1172,UC_ARM_REG_R5,ruler),
            (0x5DBF0,1165,UC_ARM_REG_R10,ruler),(0x5DC24,1167,UC_ARM_REG_R10,ruler)):
            run(start,n,((reg,speaker),))
        for start,n,slot in ((0x5D798,1150,0x10),(0x5D7D4,1152,0x14),(0x5D7FC,1153,0x10),
            (0x5D80C,1155,0x10),(0x5D828,1174,0x10),(0x5D84C,1175,0x10),(0x5D8FC,1176,0x10)):
            run(start,n,stack=((slot,minister if slot==0x14 else ruler),))
        for start,n in ((0x5DB08,1164),(0x5D974,1169)):run(start,n)
        for share,n in ((0,1151),(1,1154)):
            r=run(0x5DCEC,n,((UC_ARM_REG_R5,share),(UC_ARM_REG_R6,ruler)))
            assert bytes.fromhex(r['argument_hex'])==player_address
        for peer in peers:
            r=run(0x5DFA8,1147,((UC_ARM_REG_R5,peer['company_index']),(UC_ARM_REG_R4,minister)))
            assert r['argument_hex']==peer['leader_address_hex']
        prices=[]
        factor=struct.unpack_from('<I',source,0x5DCA4)[0]
        assert factor==0x51EB851F
        # Each supplied item is a real native record;ownership/loan eligibility is
        # not inferred from this complete numeric provider matrix.
        for n in range(218):
            item=items+4+n*20;price=get(0x4A410,(item,))
            r=run(0x5DBFC,1166,((UC_ARM_REG_R8,price),(UC_ARM_REG_R10,ruler)))
            monthly=(price*factor)>>36
            expected=text(get(0xABF50,(monthly,)))
            assert bytes.fromhex(r['argument_hex'])==expected,(n,price,monthly,r['argument_hex'],expected.hex())
            assert r['wrapper']==BASE+0x53F9C
            prices.append({'item_index':n,'native_item_price':price,'native_monthly_amount':monthly,'source_unsigned_multiply_literal':factor,'source_right_shift':36,'formatted_amount_hex':expected.hex()})
        for n in (1,2842,999999999):
            for start,key in ((0x5E068,1149),(0x5E094,1156)):
                r=run(start,key,((UC_ARM_REG_R6,n),(UC_ARM_REG_R5,ruler)))
                assert bytes.fromhex(r['argument_hex'])==text(get(0xABF50,(n,)))
        #1168's source constant is set at5DB40..5DB44,then used at5DC38.
        cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.emu_start(BASE+0x5DB40,BASE+0x5DB48,count=10)
        assert word(STACK+8)==1168
        run(0x5DC38,1168,((UC_ARM_REG_R10,ruler),),((8,1168),))
        # Source city flag accessor selects ordinary permission or forgiveness.
        original=bytes(cpu.mem_read(town+8,2))
        for flag,key in ((0,1159),(1,1163)):
            get(0xB508C,(town,flag));assert bool(get(0xB50AC,(town,)))==bool(flag)
            run(0x5E104,key,((UC_ARM_REG_R7,town),(UC_ARM_REG_R5,ruler)))
        cpu.mem_write(town+8,original)
    finally:
        for h in hooks:cpu.hook_del(h)
    assert {r['id'] for r in cases}==set(IDS)
    save(ROOT/'native_context.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'RAM_source':str(RAM),'RAM_sha256':sha(raw),
        'all31_original_message_call_fragments':cases,'native_argument_order_bound':True,
        'ruler_role6_actor127':ruler,'minister_role11_actor121':minister,'native_player_address_hex':player_address.hex(),
        'V794_context_erratum':'Earlier role4/actor92 lookup was an assumed ruler mapping. Original complete1164/1169 prefixes read actual building role6 and resolve actor127. Earlier1156/1157/1158 and blank-page captures remain valid.',
        'four_hero_address_forms':names,'active_faction_leader_address_forms':peers,'three_native_Market_letter_states':letters,
        'letter_branch_binding':{'mode0':1155,'mode1':1153,'already_monopolized':1152,'additional_restriction_for_mode0':1174,
            'existing_share_permission':1175,'new_trade_permission':1176},
        'all218_native_item_monthly_price_providers':prices,
        'source_code_spans_exact_to_clean':[[BASE+lo,BASE+hi] for lo,hi in spans],
        'declared_fragment_registers_flags_and_numeric_sizes_are_CPU_inputs_not_actual_eligibility':True,
        'stopped_before_original_dialogue_wrapper_UI_and_no_new_prose_or_ROM':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print(f'All31 Palace messages,actual ruler/minister,name arguments,three letter states and218 monthly fee providers bound;research only.',flush=True)


if __name__=='__main__':main()
