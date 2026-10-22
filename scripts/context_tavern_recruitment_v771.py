"""Clean-source role/amount/result and town-condition rumor contracts."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_R0,UC_ARM_REG_R1,
    UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R8,
    UC_ARM_REG_R9,UC_ARM_REG_SP)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE,STACK,STOP
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/tavern_recruitment_editorial_v771')
CURRENT=Path('out/all_routes_combined_v770_candidate.nds')
RAM_REPORT=Path('E:/Rota Nova translations/Generated/work/emulation_v193/tavern_round_v770_accept_v770/capture_report.json')
TABLES={0x021183A0:(883,-1,884,885,886,887,888,889),
    0x02118380:(890,-1,891,892,893,894,895,896),
    0x02118360:(897,-1,898,899,900,901,902,903)}


def main():
    rom=NdsImage.open(CURRENT);arm=rom.read_file('/__arm9__.bin')
    clean_rom=NdsImage.open('work/clean.nds');clean=clean_rom.read_file('/__arm9__.bin')
    for lo,hi in((0x57408,0x576C4),(0x578F4,0x57A5C),(0x53CB0,0x53E4C)):
        assert arm[lo:hi]==clean[lo:hi],hex(lo)
    raw=snapshot(read(RAM_REPORT),3200);u=machine(arm);u.mem_write(BASE,raw);j=machine(clean)
    def get(fn,args=()):call(u,fn,args);return u.reg_read(UC_ARM_REG_R0)
    def ptr(at):return struct.unpack('<I',u.mem_read(at,4))[0]
    def text(at):return bytes(u.mem_read(at,256)).split(b'\0')[0]
    def name(obj):return text(get(ptr(ptr(obj)+8)-BASE,(obj,)))
    officers,towns=get(0xCB184),get(0xCB178)
    here=get(0xB6618);npc=get(0xB2CD8,(here,13))
    actors=[]
    for table,values in TABLES.items():
        assert tuple(struct.unpack('<8i',u.mem_read(table,32)))==values
        for i in range(40):
            obj=officers+4+i*32;voice=get(0x7E988,(obj,));selected=get(0x53F4C,(obj,table))
            expected=values[voice] if values[voice]!=-1 else values[0]
            assert selected==expected
            actors.append({'table':table,'actor_index':i,'voice':voice,'selected_message_ID':selected})
        assert get(0x53F4C,(0,table))==values[0]
    status_rows=[]
    scratch=0x02476000
    for i in range(13):
        u.mem_write(scratch+0x6A,bytes([i]));get(0xB2D58,(scratch,));english=text(u.reg_read(UC_ARM_REG_R0))
        j.mem_write(scratch+0x6A,bytes([i]));call(j,0xB2D58,(scratch,))
        jp=bytes(j.mem_read(j.reg_read(UC_ARM_REG_R0),128)).split(b'\0')[0]
        status_rows.append({'index':i,'Japanese':jp.decode('cp932'),'current_UI_label':english.decode('ascii'),
            'private_dialogue_label':english.lower().decode('ascii'),'eligible_for_source_rumor':i<12})
    events=[]
    def observe(c,pc,size,unused):
        n=c.reg_read(UC_ARM_REG_R1);assert n in(905,906,907)
        args=[] if n==907 else [text(c.reg_read(UC_ARM_REG_R2)).hex(),text(c.reg_read(UC_ARM_REG_R3)).hex()]
        events.append({'message_id':n,'argument_hex':args});c.emu_stop()
    h=u.hook_add(UC_HOOK_CODE,observe,begin=BASE+0x53FE4,end=BASE+0x53FE4)
    cases=[];places=[]
    try:
        for i in range(114):
            obj=towns+4+i*108;native_name=name(obj)
            places.append({'index':i,'object':obj,'name_hex':native_name.hex(),'name_cp932':native_name.decode('cp932')})
            original=bytes(u.mem_read(obj+0x6A,1))
            try:
                for state in range(12):
                    u.mem_write(obj+0x6A,bytes([state]))
                    for formal in(0,1):
                        events.clear();u.mem_write(scratch,struct.pack('<3I',0,0,formal));u.mem_write(STACK,struct.pack('<I',scratch))
                        u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_R0,npc);u.reg_write(UC_ARM_REG_R5,obj)
                        u.emu_start(BASE+0x579D0,BASE+0x57A18,count=10000)
                        expected={'message_id':905 if formal else 906,'argument_hex':[native_name.hex(),status_rows[state]['current_UI_label'].encode().hex()]}
                        assert events==[expected],events
                        cases.append({**expected,'town_index':i,'status_index':state,'mode':formal})
            finally:u.mem_write(obj+0x6A,original)
        events.clear();u.mem_write(STACK+0x1C,struct.pack('<I',13));u.reg_write(UC_ARM_REG_SP,STACK)
        u.emu_start(BASE+0x575C0,BASE+0x575D4,count=10000)
        assert events==[{'message_id':907,'argument_hex':[]}]
        cases.append({**events[0],'context':'Original crowd acknowledgement immediately after first role1 recruitment call'})
    finally:u.hook_del(h)
    # Execute all four original role call sites up to the unchanged wrapper.
    role_calls=[]
    def role_stop(c,pc,size,unused):
        role_calls.append({'wrapper':pc,'role':c.reg_read(UC_ARM_REG_R0),'table_or_ID':c.reg_read(UC_ARM_REG_R1),
            'first_argument_pointer':c.reg_read(UC_ARM_REG_R2)});c.emu_stop()
    hooks=[u.hook_add(UC_HOOK_CODE,role_stop,begin=BASE+fn,end=BASE+fn) for fn in(0x53D44,0x53CB0,0x53DCC)]
    try:
        for lo,hi,regs,stack in((0x5745C,0x57468,(),()),
                (0x57470,0x57488,((UC_ARM_REG_R8,1573),),()),
                (0x575B4,0x575C0,(),((0x18,1),)),
                (0x575DC,0x575F4,((UC_ARM_REG_R9,35),),((0x24,1),(0x28,904)))):
            u.reg_write(UC_ARM_REG_SP,STACK)
            for r,v in regs:u.reg_write(r,v)
            for off,v in stack:u.mem_write(STACK+off,struct.pack('<I',v))
            u.emu_start(BASE+lo,BASE+hi,count=10000)
    finally:
        for h in hooks:u.hook_del(h)
    assert [(r['wrapper'],r['role'],r['table_or_ID']) for r in role_calls]==[(BASE+0x53D44,1,0x021183A0),
        (BASE+0x53CB0,1,0x02118380),(BASE+0x53D44,1,0x02118360),(BASE+0x53DCC,1,904)]
    entries=common_message_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm,clean=False)
    bindings=[]
    for row in role_calls:
        captured=[];chosen=[];wrapper=row['wrapper'];n=row['table_or_ID']
        amount=b'\x82\x50\x82\x54\x82\x56\x82\x52' if wrapper==BASE+0x53CB0 else '３５'.encode('cp932') if wrapper==BASE+0x53DCC else b''
        u.mem_write(scratch,amount+b'\0')
        def loader(c,pc,size,unused):
            selected=c.reg_read(UC_ARM_REG_R0);chosen.append(selected)
            assert 883<=selected<=904
            c.mem_write(scratch+0x100,entries[selected].text+b'\0');c.reg_write(UC_ARM_REG_R0,scratch+0x100)
            c.reg_write(UC_ARM_REG_PC,c.reg_read(UC_ARM_REG_LR))
        def core(c,pc,size,unused):
            vargs=c.reg_read(UC_ARM_REG_R3);sp=c.reg_read(UC_ARM_REG_SP)
            captured.append({'mode':c.reg_read(UC_ARM_REG_R0),'actor':c.reg_read(UC_ARM_REG_R1),'text_hex':text(c.reg_read(UC_ARM_REG_R2)).hex(),
                'va_list':vargs,'amount_hex':text(ptr(vargs)).hex() if amount else None,
                'original_saved_R1':ptr(sp+20),'parent_return':c.reg_read(UC_ARM_REG_LR),'SP':sp})
            c.emu_stop()
        hs=[u.hook_add(UC_HOOK_CODE,loader,begin=BASE+0x5528C,end=BASE+0x5528C),u.hook_add(UC_HOOK_CODE,core,begin=BASE+0x54058,end=BASE+0x54058)]
        u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_LR,STOP)
        for r,v in((UC_ARM_REG_R0,1),(UC_ARM_REG_R1,n),(UC_ARM_REG_R2,scratch)):u.reg_write(r,v)
        try:u.emu_start(wrapper,STOP,count=10000)
        finally:
            for h in hs:u.hook_del(h)
        assert len(captured)==len(chosen)==1
        result=captured[0];expected_parent={BASE+0x53CB0:BASE+0x53D24,BASE+0x53D44:BASE+0x53DB8,BASE+0x53DCC:BASE+0x53E38}[wrapper]
        assert result['parent_return']==expected_parent and result['SP']==STACK-32
        assert result['original_saved_R1']==n and result['va_list']==STACK-8
        assert result['mode']==int(wrapper==BASE+0x53CB0)
        assert result['text_hex']==entries[chosen[0]].text.hex()
        if amount:assert result['amount_hex']==amount.hex()
        bindings.append({'source_call':row,'selected_message_ID':chosen[0],'original_core_binding':result})
    save(ROOT/'native_context.json',{'source_ARM9_sha256':sha(clean),'current_ARM9_sha256':sha(arm),
        'source_executable_spans_exact':[[0x57408,0x576C4],[0x578F4,0x57A5C],[0x53CB0,0x53E4C]],
        'three_original_role_voice_tables':{hex(k):v for k,v in TABLES.items()},'all120_actor_voice_selections_plus3_null_fallbacks':actors,
        'all13_source_status_names_and_UI_labels':status_rows,'actual114_native_town_objects':places,
        'original_rumor_and_interjection_fragments':cases,'original_role_call_core_bindings':bindings,
        'source_candidate_filter':'Original578F4 requires virtual+10 eligibility (B5104:bit0 of halfword+8),same original region and status<12 before selecting905/906; Normal12 is excluded',
        '907_follows_recruiting_call_not_town_rumor':True,'904_reports_number_gathered_before_Assign_Sailors_not_a_sentence_fragment':True,
        'scope':'Original native CPU fragments and supplied status-byte cases only;not earned events or actual new gameplay',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print(f'{len(cases)} original rumor/interjection fragments,120 actor selections,3 null fallbacks and4 original role/core contracts pass.',flush=True)


if __name__=='__main__':main()
