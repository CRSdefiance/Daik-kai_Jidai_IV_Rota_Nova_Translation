"""Actual Inn market/report/refusal samples with disclosed original-input fixtures."""

import re
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import inn_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts.native_inn_fixture_v803 import set_condition
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_shipyard_gameplay_v760 import independent_font,models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import read,save

ROOT=owned.ROOT
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def load(folder,terminal,mode,arm):
    path=CAP/folder/'capture_report.json';report=read(path)
    assert report['frames']==terminal and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert sha(Path(report['ROM']).read_bytes())==report['ROM_sha256']
    fixture,=report['synthetic_condition_fixtures']
    assert fixture['mode']==mode and fixture['frame']==3200
    assert fixture['no_text_code_dialogue_selection_menu_flags_or_outcome_replacement']
    donor=report['battery_save_preloaded']
    assert donor['source']!=donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes())==donor['source_sha256']=='d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
    for p,h in report['Inn_fixture_adapter_v803']['source_hashes'].items():assert sha(Path(p).read_bytes())==h,p
    frames={r['frame']:r for r in report['frames_captured']}
    for r in frames.values():assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']
    ram={}
    for r in report.get('read_only_capture_RAM_snapshots',[])+report.get('read_only_pause_RAM_snapshots',[]):
        raw=Path(r['path']).read_bytes();assert len(raw)==0x400000 and sha(raw)==r['sha256'] and r['read_only_export']
        if r['frame'] in ram:assert ram[r['frame']]==raw
        ram[r['frame']]=raw
    expected,replay=set_condition(arm,ram[3200],{'mode':mode})
    assert replay=={k:v for k,v in fixture.items() if k!='frame'}
    assert sha(expected)==fixture['after_RAM_sha256']
    return path,report,fixture,frames,ram,expected


def main():
    registered=read(ROOT/'registered_verification.json');rom=NdsImage.open(registered['candidate'])
    arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    entries=owned.current_entries(common,arm);blocks=IlnkContainer.parse(common).blocks
    rows={r['message_id']:r for r in read('translations/inn_editorial_manuscript_v3.json')['records']}
    source=(ROOT/'effective_format_case.py').read_text(encoding='utf-8')
    env={**original.__dict__};exec(compile(source,str(ROOT/'effective_format_case.py'),'exec'),env)
    owner,printed,wrapped=[struct.unpack_from('<I',arm,n)[0] for n in (0x552A0,0x5444C,0x54450)]
    scenarios=[];holds=[]
    jobs=(('inn_v803_buyout',6800,'Inn-market-buyout',((5600,1184),(6000,1185)),6400),
          ('inn_v803_crash',6800,'Inn-market-crash',((5600,1182),(6000,1183)),6400),
          ('inn_v803_report_complete',6800,'Inn-strategist',((5600,1187),),6400),
          ('inn_v803_no_funds',5600,'Inn-no-funds',((4800,1194),),5200))
    for folder,terminal,mode,selected,menu_frame in jobs:
        path,report,fixture,frames,ram,initial=load(folder,terminal,mode,arm)
        assert report['ROM_sha256']==registered['candidate_sha256']
        def helpers(raw):
            u=machine(arm);u.mem_write(BASE,raw)
            def get(fn,args=()):call(u,fn,args);return u.reg_read(UC_ARM_REG_R0)
            def ptr(p):return struct.unpack('<I',u.mem_read(p,4))[0]
            def name(ob):
                p=get(ptr(ptr(ob)+8)-BASE,(ob,));return bytes(u.mem_read(p,128)).split(b'\0')[0]
            return u,get,name
        for frame,n in selected:
            raw=ram[frame];assert cstring(raw,owner+0x2030)==entries[n].text and raw.count(blocks[entries[n].block])==1
            u,get,name=helpers(raw)
            if n in (1182,1184):
                event=fixture['market_event'];values=(name(get(0xCB178)+4+event['town_ID']*108),name(get(0xCB124)+4+event['goods_ID']*16))
            elif n in (1183,1185):values=(name(get(0xCB160)+4+fixture['market_event']['affected_company_ID']*76),)
            elif n==1187:
                pattern=b'(.*?)'.join(re.escape(p) for p in entries[n].text.split(b'%s'))
                match=re.fullmatch(pattern,cstring(raw,printed));assert match
                values=match.groups();root=get(0xCB160)
                assert len(values)==1 and values[0] in {name(root+4+i*76) for i in range(20)}
                controller=get(0xCB1A8)+0x2090
                assert get(0x825E4,(controller,2))==16
                actor=get(0xCB184)+4+16*32
                assert get(0x7E988,(actor,))==1 and get(0x53F4C,(actor,0x021180E0))==1187
            else:values=()
            case=env['format_case'](prepared(arm),rows[n],values)
            assert cstring(raw,wrapped).hex()==case['formatted_hex'] and not case['findings']
            plane=raster(arm,bytes.fromhex(case['formatted_hex']),0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
            assert plane==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),case['lines'])
            image=Image.open(frames[frame]['path']).convert('RGB')
            expected={(16+i%228,296+i//228) for i,v in enumerate(plane) if v==1}
            actual={(x,y) for y in range(294,366) for x in range(16,244) if image.getpixel((x,y))==(0,8,0)}
            assert expected==actual,(mode,n,len(expected-actual),len(actual-expected))
            holds.append(dict(scenario=mode,frame=frame,message_id=n,values_hex=[v.hex() for v in values],
                capture=frames[frame],lines=case['lines'],complete_independent_font_exact=True,
                complete_first_final_letters_left_margins_bounds_and_blank_paper=True,native_complete_resident_block_exact=True))
        u,get,name=helpers(initial);cal=get(0xCB1B4)
        before_tick=struct.unpack('<I',u.mem_read(cal+8,4))[0];before_cash=state(arm,initial)['cash']
        u,get,name=helpers(ram[terminal]);cal=get(0xCB1B4)
        after_tick=struct.unpack('<I',u.mem_read(cal+8,4))[0];after_cash=state(arm,ram[terminal])['cash']
        spent=0 if mode=='Inn-no-funds' else 1
        assert before_cash-after_cash==spent and after_tick-before_tick==spent*48
        if fixture['market_event']:
            record=fixture['market_event']['record'];old=bytes.fromhex(fixture['market_event']['after_hex'])
            actual=ram[terminal][record-BASE:record-BASE+8]
            assert actual[:4]==old[:4] and actual[4]==21 and actual[5:]==old[5:]
        if mode=='Inn-no-funds':
            assert before_cash==after_cash==0
            assert models(arm,initial)==models(arm,ram[terminal])
            assert persistent_objects(arm,initial)==persistent_objects(arm,ram[terminal])
            assert tasks(arm,initial)==tasks(arm,ram[terminal])
        scenarios.append(dict(mode=mode,report=str(path),report_sha256=sha(path.read_bytes()),
            fixture_changes=fixture['changes'],source_input_fixture_replay_exact=True,
            cash_before=before_cash,cash_after=after_cash,calendar_ticks=after_tick-before_tick,
            market_event_consumed_by_original_handler=bool(fixture['market_event']),
            source_company_info_screen_after_report_frame=6000 if mode=='Inn-strategist' else None,
            menu_return_frame=menu_frame,town_return_frame=terminal,return_captures=[frames[menu_frame],frames[terminal]],
            returns_visually_reviewed=True,donor_source_unchanged=True,
            naturally_earned_assignment_market_event_or_campaign_progress_not_claimed=True))
    save(ROOT/'news_report_refusal_gameplay.json',dict(candidate=registered['candidate'],candidate_sha256=registered['candidate_sha256'],
        actual_holds=holds,scenarios=scenarios,all_six_actual_body_fonts_and_source_values_exact=True,
        original_report_company_info_window_preserved=True,report_uses_native_Strategist_role2_Gerhard_voice1=True,
        original_one_coin_day_cost_market_consumed_flags_and_no_funds_noop_verified=True,
        battle_raid_relative_month_and_early_departure_actual_samples_pending=True,
        full_Inn23_completion_credit=False,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Six actual market/report/refusal holds:complete native fonts,source values,event consumption,fees/calendar,report info window and normal returns pass.',flush=True)


if __name__=='__main__':main()
