"""Disclosed Inn input fixtures; original eligibility, dialogue and outcomes run."""

import struct
from types import FunctionType

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import native_strategist_fixture_v624 as strategist
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.verify_village_wrap_v608 import read


def set_condition(arm,raw,request):
    cfg=read('translations/inn_editorial_release_v1.json')
    assert sha(arm)==cfg['target_arm9_sha256'] and len(raw)==0x400000
    modes=('Inn-market-buyout','Inn-market-crash','Inn-strategist','Inn-no-funds')
    assert set(request)=={'mode'} and request['mode'] in modes
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=((0x5CC70,0x5D3F8),(0x39620,0x39634),(0x3CC80,0x3CCC8))
    assert all(arm[lo:hi]==clean[lo:hi] for lo,hi in spans)
    mode=request['mode'];parts=[]
    if mode!='Inn-no-funds':
        run=FunctionType(strategist.assign.__code__,{**strategist.__dict__,**{k:sha(arm) for k in ('ARM','TARGET','CONTEXT','QUEUED')}})
        after,part=run(arm,raw,True);parts.append(part)
    else:after=raw
    u=machine(arm);u.mem_write(BASE,after)
    def get(fn,args=()):
        call(u,fn,args);return u.reg_read(UC_ARM_REG_R0)
    def ptr(at):return struct.unpack('<I',u.mem_read(at,4))[0]
    output=bytearray(after);event=None;qualification=None
    if mode in ('Inn-market-buyout','Inn-market-crash'):
        town=get(0xB6618);town_id=get(0xB65E4);region=get(0xB2B48,(town,))
        assert town_id==22 and region==1
        offset=struct.unpack_from('<I',arm,0x5CE90)[0]
        record=get(0xCB160)+offset+region*8
        valid=ptr(ptr(record)+16)
        assert valid==BASE+0x39620 and get(valid-BASE,(record,))==0
        original=bytes(u.mem_read(record,8))
        assert original[4]==21
        # Original5CC70 consumes these four typed event fields. Preserve vptr.
        payload=bytes([0,int(mode=='Inn-market-buyout'),town_id,0])
        output[record-BASE+4:record-BASE+8]=payload
        u.mem_write(record+4,payload)
        assert get(valid-BASE,(record,))==1
        event=dict(record=record,region=region,source_vtable=ptr(record),original_validity_method=valid,
            before_hex=original.hex(),after_hex=(original[:4]+payload).hex(),
            affected_company_ID=0,town_ID=town_id,goods_ID=0,event_type=payload[1],
            original_pending_event_valid_after_input=True,consumed_sentinel_expected_from_original_handler=21)
    elif mode=='Inn-no-funds':
        root=get(0xCB160);company_id=get(0x397D8,(root,));company=root+4+company_id*76
        before=get(0x3CCC8,(company,))
        get(0x3CC80,(company,(-before)&0xffffffff))
        assert get(0x3CCC8,(company,))==0
        output[company-BASE+12:company-BASE+16]=bytes(u.mem_read(company+12,4))
        qualification=dict(original_cash_method=BASE+0x3CC80,company_ID=company_id,before_cash=before,after_cash=0)
    result=bytes(output)
    changes=[dict(address=BASE+i,before=a,after=b) for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b]
    allowed={r['address'] for p in parts for r in p['changes']}
    if event:allowed.update(range(event['record']+4,event['record']+8))
    if qualification:allowed.update(range(company+12,company+16))
    assert all(c['address'] in allowed for c in changes)
    return result,dict(synthetic_Inn_input_fixture=True,mode=mode,ARM9_sha256=sha(arm),
        original_strategist_assignment_components=parts,market_event=event,cash_fixture=qualification,
        changes=changes,all_other4MiB_RAM_bytes_exact=True,
        no_text_code_dialogue_selection_menu_flags_or_outcome_replacement=True,
        earned_assignment_market_event_money_or_campaign_progress_not_claimed=True,
        before_RAM_sha256=sha(raw),after_RAM_sha256=sha(result))
