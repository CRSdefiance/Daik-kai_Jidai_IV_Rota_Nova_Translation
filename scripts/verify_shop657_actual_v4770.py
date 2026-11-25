"""Exact ordinary gameplay holds, blank paper, return and current startup proof."""
from pathlib import Path
import struct
from PIL import Image,ImageDraw

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from ndspy.code import MainCodeFile
from scripts.primary_town_native_font_v2102 import font_tools,glyph_codes
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.probe_button_prompt_native import BASE,STACK,machine
from scripts.review_early_shop_breaks_v4763e import expected_plane
from scripts.verify_market_gameplay_v753 import state,snapshot
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/shop657_actual_verification_v4770')
RUN=Path('work/analysis/shop657_actual_v4768b')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/shop657_full_width_v4768b')

if __name__=='__main__':
    assert not ROOT.exists()
    plan,terminal,report,obs=[read(p) for p in [RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',CAP/'common_observer/requests.json']]
    digest=plan['candidate_sha256'];rom=NdsImage.open(plan['candidate']);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    assert sha(Path(plan['candidate']).read_bytes())==digest
    assert terminal['terminal'] and report['frames']==terminal['frames']==9501
    assert report['ROM_sha256']==digest and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not obs['errors'] and not obs['mismatches'] and obs['all_host_slots_restored_and_core_file_exact']
    assert not any(v for k,v in report.items() if k.startswith('synthetic_'))
    assert report['scripted_input_schedule']==read(plan['inputs'])
    donor=report['battery_save_preloaded'];assert donor['copied_byte_exact_before_cold_boot']
    assert donor['source_sha256']==sha(Path(donor['source']).read_bytes())=='d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
    frames={r['frame']:r for r in report['frames_captured']}
    for r in frames.values():assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']
    conf=read('translations/shop657_full_width_reflow_release_v1.json');entries=owned_entries(common,arm,conf['directory_sha256'])
    cpu=machine(arm);cpu.mem_write(0x02387A20,bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]));cpu.mem_write(STACK+0x27C,struct.pack('<I',0x02118480))
    raster,_,_=font_tools(rom);holds=[]
    for row in obs['rows']:
        n=row['source_request']['ID']
        assert n in [656,657,658,717] and row['bounds']==[0,0,228,48]
        assert row['CPU_WRAM_DTCM_ITCM_configuration_exact'] and row['font_input_offset'] in [0,2]
        for s in row['snapshots'].values():assert sha(Path(s['path']).read_bytes())==s['sha256']
        formatted,lines=native_layout(cpu,entries[n].text,n,(),0x02054014)
        assert formatted.hex()==row['text_hex']
        next_request=min([r['frame'] for r in obs['source_requests'] if r['frame']>row['frame']]+[9502])
        f=next(f for f in sorted(frames) if row['frame']<f<next_request)
        events=[];plane=raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000,glyph_events=events)
        assert plane==expected_plane(arm,lines,1)
        assert [e['code'] for e in events if e['code']!=32]==glyph_codes(formatted)
        photo=Image.open(frames[f]['path']).convert('RGB')
        expected={(16+j%228,296+j//228) for j,v in enumerate(plane) if v==1}
        actual={(x,y) for y in range(294,356) for x in range(16,244) if photo.getpixel((x,y))==(0,8,0)}
        assert expected==actual,(n,f,len(expected-actual),len(actual-expected))
        if n==657:
            raw=Path(row['snapshots']['WRAM']['path']).read_bytes();block=IlnkContainer.parse(common).blocks[7]
            at=raw.find(block);assert at>=0
            assert len(lines)==2 and lines[0]=="You're a sailor, aren't you? For" and lines[1]=='bulk trade, try the trade house.'
        holds.append(dict(message_ID=n,font_frame=row['frame'],hold_frame=f,text_hex=formatted.hex(),lines=lines,
            capture=frames[f]['path'],capture_sha256=frames[f]['PNG_sha256'],
            all_ink_and_blank_paper_pixels_equal_independent_full_plane=True,
            complete_first_internal_last_characters_and_native_bounds=True))
    assert {r['message_ID'] for r in holds}=={656,657,658,717}
    states=[]
    for f in [3200,8000,9500]:
        raw=snapshot(report,f);states.append(dict(frame=f,state=state(arm,raw),models=models(arm,raw)))
    assert all(r['state']==states[0]['state'] and r['models']==states[0]['models'] for r in states)
    original=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x5F9B8:0x5FA60]==original[0x5F9B8:0x5FA60] and struct.unpack_from('<I',arm,0x5FA5C)[0]==657
    startup_terminal=read('work/analysis/shop657_startup_v4769/newgame_terminal.json');startup=read(startup_terminal['report'])
    assert startup_terminal['terminal'] and startup['frames']==4001 and startup['ROM_sha256']==digest
    assert startup['cold_boot'] and not startup['savestate_loaded'] and not startup['callback_errors'] and not startup.get('battery_save_preloaded')
    assert not any(v for k,v in startup.items() if k.startswith('synthetic_'))
    startup_frames={r['frame']:r for r in startup['frames_captured']}
    for r in startup_frames.values():assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']
    # Complete current-font masks for the confirmation and established opening.
    from dk4tool.dialogue.font_audit import GameAsciiFont
    from scripts.record_navigation_v327 import dark_text
    font=GameAsciiFont.from_arm9(arm);masks=[]
    for frame,text,box in [(2000,'Everything correct?',(10,320,244,365)),
        (4000,'Hee hee! I finally got my trade',(10,292,245,313)),
        (4000,"permit! Just you watch--I'm going",(10,308,250,329)),
        (4000,'to make a fortune!',(10,324,245,348))]:
        masks.append(dict(frame=frame,match=dark_text(font,text,Image.open(startup_frames[frame]['path']).convert('RGB'),box)))
    ROOT.mkdir(parents=True)
    selected=[r['capture'] for r in holds]+[frames[9500]['path']]+[startup_frames[f]['path'] for f in [1600,2000,4000]]
    sheet=Image.new('RGB',(1024,410*2),'#263238');draw=ImageDraw.Draw(sheet)
    for i,path in enumerate(selected):
        x,y=i%4*256,i//4*410
        draw.text((x+4,y+4),Path(path).stem,fill='white');sheet.paste(Image.open(path).convert('RGB'),(x,y+22))
    sheet_path=ROOT/'four_shop_holds_return_and_three_startup_screens.png';sheet.save(sheet_path)
    first=read('work/analysis/shop657_actual_v4768/terminal.json')
    save(ROOT/'ordinary_actual_and_startup_verification.json',dict(candidate=plan['candidate'],candidate_sha256=digest,
        focused_ordinary_run_frames=9501,earlier_ordinary_run_frames=first['frames'],startup_frames=4001,
        total_new_emulator_frames=9501+first['frames']+4001,actual_holds=holds,source_requests=obs['source_requests'],
        all_four_holds_full_native_and_independent_ink_blank_pixels_equal=True,
        observed657_selected_by_unchanged_original_fourway_random_branch=True,
        first6501_replay_did_not_select657_and_is_not657_coverage=True,
        genuine_inherited_battery_does_not_prove_earned_progress=True,
        no_savestate_state_fixture_script_replacement_or_random_value_write=True,
        state_projection_controls=states,company_fleet_ships_and_five_financial_fields_equal=True,
        no_full_RAM_future_world_route_hardware_or_every_conditional_coverage_claim=True,
        startup_complete_masks=masks,startup_cold_boot_without_save=True,
        report=str(CAP/'capture_report.json'),observer=str(CAP/'common_observer/requests.json'),
        report_sha256=sha((CAP/'capture_report.json').read_bytes()),observer_sha256=sha((CAP/'common_observer/requests.json').read_bytes()),
        sheet=str(sheet_path),sheet_sha256=sha(sheet_path.read_bytes()),visual_review_pending=True,
        no_added_editorial_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(actual_holds=len(holds),changed_message_hold=next(r['hold_frame'] for r in holds if r['message_ID']==657),
               total_new_frames=20003,startup_masks=len(masks),state_controls=3,sheet=str(sheet_path)),flush=True)
