"""Bound Market share or wallet display fixtures, using original native getters."""

import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_village_wrap_v608 import read


def assign(arm,raw,request):
    config=read('translations/market_replies_editorial_release_v1.json')
    assert sha(arm) in (config['source_arm9_sha256'],config['target_arm9_sha256'])
    assert request in ({'mode':'share'},{'mode':'low_funds'}) and len(raw)==4194304
    cpu=machine(arm);cpu.mem_write(BASE,raw)
    def get(fn,args=()):
        call(cpu,fn,args);return cpu.reg_read(UC_ARM_REG_R0)
    town=get(0xB6618);assert get(0xB65E4)==22
    root=get(0xCB160);company=get(0x397D8,(root,));assert company==2
    entity=root+4+company*0x4c
    cash=get(0x3CCC8,(entity,));share=get(0xB4AA8,(town,company));minimum=get(0xB3FA4,(town,0))
    assert cash==8371 and share==0 and minimum==2684
    if request['mode']=='share':
        address=town+0x12;assert bytes(cpu.mem_read(address,2))==bytes((21,0))
        values=[(address,bytes((company,1)),'original unused town company/share pair')]
    else:
        assert arm[0x3CCC8:0x3CCD0]==bytes.fromhex('0c0090e51eff2fe1')
        address=entity+12;assert bytes(cpu.mem_read(address,4))==struct.pack('<I',cash)
        values=[(address,bytes(4),'original current-company wallet')]
    after=bytearray(raw);changes=[]
    for address,data,field in values:
        for n,value in enumerate(data):
            at=address+n-BASE
            if after[at]!=value:
                changes.append({'address':BASE+at,'before':after[at],'after':value,'field':field});after[at]=value
    assert len(changes)==2 and sum(a!=b for a,b in zip(raw,after,strict=True))==2
    cpu.mem_write(BASE,bytes(after))
    assert get(0xB4AA8,(town,company))==(1 if request['mode']=='share' else 0)
    assert get(0x3CCC8,(entity,))==(cash if request['mode']=='share' else 0)
    return bytes(after),{'synthetic_market_display_fixture':True,'mode':request['mode'],'changes':changes,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(after),'ARM9_sha256':sha(arm),
        'original_town':22,'original_company':company,'before_share':share,'before_cash':cash,'native_minimum':minimum,
        'all_other_RAM_code_inventory_growth_stock_flags_and_location_bytes_unchanged':True,
        'earned_share_money_trade_or_investment_not_claimed':True,'fixture_source_sha256':sha(Path(__file__).read_bytes())}
