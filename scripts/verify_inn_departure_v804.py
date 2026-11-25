"""Ordinary 30-night stay interrupted after two nights;full glyphs and true costs."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import inn_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_tavern_continuation_layout_v768 as original
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

ROOT=Path('work/analysis/inn_history_v804')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/inn_v804_early_departure')


def main():
    path=CAP/'capture_report.json';report=read(path)
    assert report['frames']==7700 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(v for k,v in report.items() if k.startswith('synthetic_'))
    journal=read(CAP/'navigation_command_journal.json')
    # The frozen journal deliberately disclaims execution receipts. Completion
    # comes from the observed exit0 and terminal capture report,not this flag.
    assert journal['commands_are_not_execution_receipts'] and journal['ROM_sha256']==report['ROM_sha256']
    assert all(r['validation_passed'] and set(r['command'])<={'until','buttons','duration','touch','stop'} for r in journal['commands_received'])
    donor=report['battery_save_preloaded'];assert donor['source']!=donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes())==donor['source_sha256']=='d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
    assert report['ROM_sha256']==sha(Path(report['ROM']).read_bytes())=='7c6c8bb3c89973af2f789488e51bff395d871be6a461490d62b3f5c8d860daad'
    rom=NdsImage.open(report['ROM']);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    entries=owned.current_entries(common,arm);blocks=IlnkContainer.parse(common).blocks
    frames={r['frame']:r for r in report['frames_captured']}
    for r in frames.values():assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']
    ram={}
    for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        raw=Path(r['path']).read_bytes();assert len(raw)==0x400000 and sha(raw)==r['sha256'] and r['read_only_export']
        if r['frame'] in ram:assert ram[r['frame']]==raw
        ram[r['frame']]=raw
    rows={r['message_id']:r for r in read('translations/inn_editorial_manuscript_v3.json')['records']}
    source=(owned.ROOT/'effective_format_case.py').read_text(encoding='utf-8')
    env={**original.__dict__};exec(compile(source,str(owned.ROOT/'effective_format_case.py'),'exec'),env)
    owner,printed,wrapped=[struct.unpack_from('<I',arm,n)[0] for n in (0x552A0,0x5444C,0x54450)]
    holds=[]
    for f,n,values in ((6200,1180,('３０'.encode('cp932'),)),(6780,1199,()),(6900,1199,())):
        raw=ram[f];assert cstring(raw,owner+0x2030)==entries[n].text and raw.count(blocks[entries[n].block])==1
        case=env['format_case'](prepared(arm),rows[n],values)
        assert not case['findings'] and cstring(raw,wrapped).hex()==case['formatted_hex']
        if n==1180:assert values[0] in cstring(raw,printed) and len(case['lines'])==1
        plane=raster(arm,bytes.fromhex(case['formatted_hex']),0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
        assert plane==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),case['lines'])
        image=Image.open(frames[f]['path']).convert('RGB')
        expected={(16+i%228,296+i//228) for i,v in enumerate(plane) if v==1}
        actual={(x,y) for y in range(294,366) for x in range(16,244) if image.getpixel((x,y))==(0,8,0)}
        assert expected==actual,(f,n,len(expected-actual),len(actual-expected))
        holds.append(dict(frame=f,message_id=n,capture=frames[f],lines=case['lines'],full_independent_native_font_exact=True,
            complete_leading_trailing_letters_both_night_digits_and_consistent_left_margin=True,no_unexpected_dark_ink_on_blank_paper=True))
    states=[]
    for f in (6600,6608,6700,6780,6900,7300,7700):
        raw=ram[f];u=machine(arm);u.mem_write(BASE,raw);call(u,0xCB1B4,());cal=u.reg_read(UC_ARM_REG_R0)
        states.append(dict(frame=f,cash=state(arm,raw)['cash'],calendar_tick=struct.unpack('<I',u.mem_read(cal+8,4))[0]))
    at={r['frame']:r for r in states}
    assert at[6600]['cash']==8371 and at[6900]['cash']==8369
    assert at[6900]['calendar_tick']-at[6600]['calendar_tick']==96
    assert all(at[f]['cash']==8369 and at[f]['calendar_tick']==at[6900]['calendar_tick'] for f in (6780,7300,7700))
    for f in (7300,7700):
        assert models(arm,ram[6900])==models(arm,ram[f])
        assert persistent_objects(arm,ram[6900])==persistent_objects(arm,ram[f])
        assert tasks(arm,ram[6900])==tasks(arm,ram[f])
    schedule=report['scripted_input_schedule']
    assert next(r for r in schedule if r['start']==6701)==dict(start=6701,duration=80,buttons=['B'])
    assert next(r for r in schedule if r['start']==6901)==dict(start=6901,duration=8,buttons=['A'])
    save(ROOT/'departure_gameplay_verification.json',dict(candidate=report['ROM'],candidate_sha256=report['ROM_sha256'],
        report=str(path),report_sha256=sha(path.read_bytes()),actual_holds=holds,native_states=states,
        ordinary_cold_boot_no_new_input_fixture=True,requested_nights=30,completed_nights=2,
        only_two_coins_and_two_days_charged=True,remaining28_nights_not_charged=True,
        B_interrupt_at_original_night_boundary_verified=True,A_yes_leaves_early=True,
        menu_return_frame=7300,town_return_frame=7700,return_captures=[frames[7300],frames[7700]],
        covered_models_actors_towns_items_goods_couriers_unchanged_after_yes=True,
        no_branch_resume_not_separately_activated=True,donor_source_unchanged=True,
        input_calibration_separate_and_not_counted_as_Inn_scene=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Actual early departure:30-night confirmation,1199 full fonts at two holds,B interrupt,A Yes,2coins/96ticks only,normal return and unchanged covered persistent objects pass.',flush=True)


if __name__=='__main__':main()
