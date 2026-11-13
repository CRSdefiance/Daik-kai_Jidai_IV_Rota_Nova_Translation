"""Actual original history-dispatch samples:full months,glyphs,consumption,returns."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import inn_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts.native_inn_history_fixture_v804 import set_condition
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/inn_history_v804')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def main():
    plan=read(ROOT/'input_preflight.json');rom=NdsImage.open(plan['candidate']);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    assert sha(Path(plan['candidate']).read_bytes())==plan['candidate_sha256']
    entries=owned.current_entries(common,arm);blocks=IlnkContainer.parse(common).blocks
    rows={r['message_id']:r for r in read('translations/inn_editorial_manuscript_v3.json')['records']}
    source=(owned.ROOT/'effective_format_case.py').read_text(encoding='utf-8')
    env={**original.__dict__};exec(compile(source,str(owned.ROOT/'effective_format_case.py'),'exec'),env)
    owner,wrapped=[struct.unpack_from('<I',arm,n)[0] for n in (0x552A0,0x54450)]
    cases=[];controls=[];reference={}
    for item in plan['cases']:
        label=item['label'];path=CAP/('inn_v804_'+label)/'capture_report.json';report=read(path)
        assert report['frames']==6400 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['ROM_sha256']==plan['candidate_sha256']
        donor=report['battery_save_preloaded'];assert donor['source']!=donor['destination'] and donor['copied_byte_exact_before_cold_boot']
        assert sha(Path(donor['source']).read_bytes())==donor['source_sha256']=='d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
        for p,h in report['Inn_history_fixture_adapter_v804']['source_hashes'].items():assert sha(Path(p).read_bytes())==h,p
        receipt,=report['synthetic_condition_fixtures'];assert receipt['frame']==3200 and receipt['request']==item['request']
        assert receipt['no_code_text_dialogue_selection_menu_flags_or_result_replacement']
        frames={r['frame']:r for r in report['frames_captured']}
        for f in frames.values():assert sha(Path(f['path']).read_bytes())==f['PNG_sha256']
        ram={}
        for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
            raw=Path(r['path']).read_bytes();assert len(raw)==0x400000 and sha(raw)==r['sha256'] and r['read_only_export']
            if r['frame'] in ram:assert ram[r['frame']]==raw
            ram[r['frame']]=raw
        initial,replayed=set_condition(arm,ram[3200],item['request'])
        assert replayed=={k:v for k,v in receipt.items() if k!='frame'}
        assert receipt['original_dispatcher_preflight']==item['proof']['original_dispatcher_preflight']
        raw=ram[5600];n=receipt['original_dispatcher_preflight'][0]['message']
        assert cstring(raw,owner+0x2030)==entries[n].text and raw.count(blocks[entries[n].block])==1
        u=machine(arm);u.mem_write(BASE,raw)
        def get(fn,args=()):call(u,fn,args);return u.reg_read(UC_ARM_REG_R0)
        def ptr(at):return struct.unpack('<I',u.mem_read(at,4))[0]
        def text(p):return bytes(u.mem_read(p,256)).split(b'\0')[0]
        def name(ob):return text(get(ptr(ptr(ob)+8)-BASE,(ob,)))
        record=receipt['history_record'];data=bytes.fromhex(receipt['fixture_history_hex'])
        assert bytes(u.mem_read(record,12))==data and get(0x3A074,(record,))==receipt['original_history_type']
        company_root=get(0xCB160);town_root=get(0xCB178)
        now=get(0xCCA44,(get(0xCB1B4),));month=text(get(0x5CA8C,(0,record,now)))
        if item['request']['event']=='fleet':values=(month,name(company_root+4+data[4]*76),name(company_root+4+data[5]*76))
        elif item['request']['event']=='raid':values=(month,name(company_root+4+data[4]*76),name(town_root+4+data[6]*108))
        else:values=(month,name(town_root+4+data[6]*108),name(company_root+4+data[5]*76))
        assert [v.hex() for v in values]==receipt['original_dispatcher_preflight'][0]['values_hex']
        case=env['format_case'](prepared(arm),rows[n],values)
        assert not case['findings'] and cstring(raw,wrapped).hex()==case['formatted_hex']
        plane=raster(arm,bytes.fromhex(case['formatted_hex']),0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
        assert plane==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),case['lines'])
        image=Image.open(frames[5600]['path']).convert('RGB')
        expected={(16+i%228,296+i//228) for i,v in enumerate(plane) if v==1}
        actual={(x,y) for y in range(294,366) for x in range(16,244) if image.getpixel((x,y))==(0,8,0)}
        assert expected==actual,(label,len(expected-actual),len(actual-expected))
        end=ram[6400][record-BASE:record-BASE+12]
        assert end==data[:4]+b'\x15'+data[5:]
        def finance(raw):
            machine_copy=machine(arm);machine_copy.mem_write(BASE,raw);call(machine_copy,0xCB1B4,());cal=machine_copy.reg_read(UC_ARM_REG_R0)
            return state(arm,raw)['cash'],struct.unpack('<I',machine_copy.mem_read(cal+8,4))[0]
        before_cash,before_tick=finance(initial);after_cash,after_tick=finance(ram[6400])
        assert before_cash-after_cash==1 and after_tick-before_tick==48
        for f in (6000,6400):
            pixels=Image.open(frames[f]['path']).convert('RGB').tobytes()
            if f not in reference:reference[f]=pixels
            assert pixels==reference[f],(label,f)
            controls.append(dict(scenario=label,frame=f,capture=frames[f],whole_screen_equal_all_six_history_cases=True))
        cases.append(dict(label=label,request=item['request'],report=str(path),report_sha256=sha(path.read_bytes()),
            message_id=n,hold=frames[5600],lines=case['lines'],source_values_hex=[v.hex() for v in values],
            original_type=receipt['original_history_type'],fixture_changes=receipt['changes'],exact_fixture_replay_and_only_owned_inputs=True,
            complete_independent_font_and_all_blank_paper_ink_exact=True,complete_month_first_last_letters_and_consistent_left_margin=True,
            original_history_consumer_sets_only_consumed_company_byte=True,
            cash_before=before_cash,cash_after=after_cash,calendar_tick_delta=48,menu_return_frame=6000,town_return_frame=6400,
            donor_source_unchanged=True,natural_battle_victory_or_campaign_progress_not_claimed=True))
    assert {r['message_id'] for r in cases}=={1195,1196,1197,1198}
    save(ROOT/'history_gameplay_verification.json',dict(candidate=plan['candidate'],candidate_sha256=plan['candidate_sha256'],
        cases=cases,control_frames=controls,actual_native_history_types=[0,1,2],all_four_rumor_IDs_and_both_outcomes_per_type_verified=True,
        complete_relative_month_cases=['This month','Last month','２ months ago','３ months ago','１０ months ago','１１ months ago'],
        source_logic_text_code_and_originalsaves_unchanged=True,actual_early_departure1199_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Six actual history holds:all three original types/both outcomes,four IDs,complete months/fonts,12 identical return controls,consumption and1coin/48tick stays pass.',flush=True)


if __name__=='__main__':main()
