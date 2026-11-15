"""Current Bribe glyphs, original deferred arrangement/fee, bounded fixture and state."""
from pathlib import Path
import re
import struct
from PIL import Image, ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from scripts.verify_village_wrap_v608 import read, save
from scripts.primary_town_native_font_v2102 import font_tools, glyph_codes
from scripts.verify_shipyard_gameplay_v760 import independent_font, models
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.native_scheme_context_fixture_v2204 import assign_expert

ROOT=Path('work/analysis/scheme_bribe_actual_verification_v2210')
RUN=Path('work/analysis/scheme_bribe_actual_v2207')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/scheme_bribe_actual_v2207_V2171')
NATIVE=Path('work/analysis/scheme_bribe_actual_continuations_v2209/actual_snapshot_native_font_continuations.json')
ROM=Path('out/all_routes_combined_v2171_candidate.nds')
EXPECTED={909:(6000,6400),915:(8000,8400),973:(9600,10000),979:(10800,11200),965:(11600,12000)}

def snapshots(report):
    result={}
    for row in report.get('read_only_capture_RAM_snapshots',[])+report.get('read_only_pause_RAM_snapshots',[]):
        if row['frame'] in result:
            assert result[row['frame']]['sha256']==row['sha256']
        result[row['frame']]=row
    return result

if __name__=='__main__':
    assert not ROOT.exists()
    ROOT.mkdir(parents=True)
    rom=NdsImage.open(ROM)
    arm,common,kanji=[rom.read_file(p)for p in('/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT')]
    entries=current_entries(common,arm)
    plan,terminal,report,obs,native=[read(p)for p in(RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',CAP/'common_observer/requests.json',NATIVE)]
    assert terminal['terminal']and terminal['all_observer_host_slots_restored']and terminal['declared_fixture_only']
    assert report['frames']==13200 and report['cold_boot']and not report['savestate_loaded']
    assert not report['callback_errors']and not report['hardware_device_verification']
    assert not obs['errors']and not obs['mismatches']and obs['all_host_slots_restored_and_core_file_exact']
    assert report['ROM_sha256']==plan['candidate_sha256']==sha(ROM.read_bytes())
    assert sha(Path(plan['battery_donor']).read_bytes())==plan['donor_sha256']=='05fa512b078fd01a8f6bee605254e9f72bfe3453c0ea098d977c87d86b6b693e'
    previous=read(plan['prior_report'])
    assert sha(Path(plan['prior_report']).read_bytes())==plan['prior_report_sha256']
    # A pause-only empty-button command adds no pad/touch input to the full recorded schedule.
    assert report['scripted_input_schedule']==previous['scripted_input_schedule']and report['core_options']==previous['core_options']
    fixture,=report['synthetic_strategist_room_assignment_fixtures']
    assert not any(v for k,v in report.items()if k.startswith('synthetic_')and k!='synthetic_strategist_room_assignment_fixtures')
    current_snapshots,old_snapshots=snapshots(report),snapshots(previous)
    before=Path(current_snapshots[3200]['path']).read_bytes()
    after,replayed=assign_expert(arm,before,True)
    assert fixture=={**replayed,'frame':3200}
    assert len(fixture['changes'])<=11 and fixture['all_other4MiB_bytes_exact']and fixture['only_three_assignment_bytes_one_XP_word_one_calendar_word_owned']
    assert {i+0x02000000 for i,(a,b)in enumerate(zip(before,after,strict=True))if a!=b}=={r['address']for r in fixture['changes']}
    assert native['ARM9_sha256']==sha(arm)and len(native['cases'])==len(obs['rows'])==6
    frames={r['frame']:r for r in report['frames_captured']}
    raster,_,_=font_tools(rom)
    holds=[]
    for row in obs['rows']:
        n=row['source_request']['ID']
        full=next(r for r in native['cases']if r['message_ID']==n and r['text_hex']==row['text_hex'])
        assert full['complete_native_return']and full['SP_preserved']and full['callee_registers_preserved']and not full['faults']and not full['error']
        if n not in EXPECTED:continue
        assert row['bounds']==[0,0,228,48]and row['font_input_offset']in(0,2)
        raw=Path(row['snapshots']['WRAM']['path']).read_bytes()
        assert sha(raw)==row['snapshots']['WRAM']['sha256']
        p=struct.unpack_from('<I',arm,0x5444C)[0]-0x02000000
        printf=raw[p:p+512].split(bytes(1))[0]
        match=re.fullmatch(b'(.*?)'.join(re.escape(p)for p in entries[n].text.split(b'%s')),printf)
        assert match is not None
        if n==979:assert match.groups()==(b'London',b'Clifford')
        text=bytes.fromhex(row['text_hex'])
        assert b' '.join(text.split())==b' '.join(printf.split())
        lines=[s.strip().decode('cp932')for s in text.split(b'\n')]
        events=[]
        plane=raster(arm,text,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000,glyph_events=events)
        assert plane==independent_font(arm,kanji,lines)
        assert[r['code']for r in events if r['code']!=32]==glyph_codes(text)
        assert[r['code']for r in full['glyph_events']if r['code']!=32]==glyph_codes(text)
        assert sorted({r['y']for r in full['glyph_events']})==list(range(0,12*len(lines),12))
        pixels={(16+i%228,296+i//228)for i,v in enumerate(plane)if v==1}
        for f in EXPECTED[n]:
            capture=frames[f]
            assert sha(Path(capture['path']).read_bytes())==capture['PNG_sha256']
            image=Image.open(capture['path']).convert('RGB')
            actual={(x,y)for y in range(294,360)for x in range(16,244)if image.getpixel((x,y))==(0,8,0)}
            assert actual==pixels,(n,f,len(actual-pixels),len(pixels-actual))
            holds.append(dict(message_ID=n,font_frame=row['frame'],hold_frame=f,lines=lines,arguments_hex=[v.hex()for v in match.groups()],formatted_hex=text.hex(),capture=capture['path'],capture_sha256=capture['PNG_sha256'],complete_native_actual_independent_foreground_equal=True))
    assert len(holds)==10 and {r['message_ID']for r in holds}==set(EXPECTED)
    old_arm=NdsImage.open(previous['ROM']).read_file('/__arm9__.bin')
    paired=[]
    for f in(3200,6000,10000,11200,12400,13200):
        raw,old_raw=[Path(q[f]['path']).read_bytes()for q in(current_snapshots,old_snapshots)]
        assert sha(raw)==current_snapshots[f]['sha256']and sha(old_raw)==old_snapshots[f]['sha256']
        current_state,old_state=state(arm,raw),state(old_arm,old_raw)
        current_models,old_models=models(arm,raw),models(old_arm,old_raw)
        assert current_state==old_state,(f,'state',current_state,old_state)
        assert current_models==old_models,(f,'models')
        assert persistent_objects(arm,raw)==persistent_objects(old_arm,old_raw),(f,'persistent')
        current_tasks,old_tasks=tasks(arm,raw),tasks(old_arm,old_raw)
        assert current_tasks==old_tasks,(f,'deferred-task-bytes')
        paired.append(dict(frame=f,state=current_state,models=current_models,deferred_task_sha256=sha(current_tasks),current_RAM_sha256=sha(raw),reference_RAM_sha256=sha(old_raw),native_state_company_fleet_ship_persistent_and_task_objects_equal_historical_same_inputs=True))
    assert paired[0]['state']['cash']==paired[3]['state']['cash']
    assert paired[0]['state']['cash']-paired[4]['state']['cash']==1000
    assert paired[4]['state']['cash']==paired[5]['state']['cash']
    controls=[]
    for f in(6800,8800,10400,12400,12800,13200):
        capture=frames[f]
        assert sha(Path(capture['path']).read_bytes())==capture['PNG_sha256']
        controls.append(dict(frame=f,capture=capture['path'],capture_sha256=capture['PNG_sha256'],scope='actual scheme/faction/town menus or ordinary return after declared fixture; visual review pending'))
    sheets=[]
    for name,rows,key in(('ten_scheme_bribe_holds',holds,'hold_frame'),('six_scheme_bribe_transitions',controls,'frame')):
        sheet=Image.new('RGB',(1024,410*((len(rows)+3)//4)),'#263238');draw=ImageDraw.Draw(sheet)
        for i,r in enumerate(rows):
            x,y=i%4*256,i//4*410
            draw.text((x+4,y+4),f"ID{r.get('message_ID','context')} frame{r[key]}",fill='white')
            sheet.paste(Image.open(r['capture']).convert('RGB'),(x,y+22))
        path=ROOT/(name+'.png');sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'scheme_bribe_foreground_fixture_state_transitions.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),source_plan=str(RUN/'run_plan.json'),source_plan_sha256=sha((RUN/'run_plan.json').read_bytes()),source_report=str(CAP/'capture_report.json'),source_report_sha256=sha((CAP/'capture_report.json').read_bytes()),source_observer=str(CAP/'common_observer/requests.json'),source_observer_sha256=sha((CAP/'common_observer/requests.json').read_bytes()),native_continuation=str(NATIVE),native_continuation_sha256=sha(NATIVE.read_bytes()),fixture=fixture,fixture_replayed_exactly_against_preinteraction_RAM=True,actual_holds=holds,transition_frames=controls,paired_native_state_model_task_controls=paired,source_cost_and_actual_charge=1000,cash_before=paired[0]['state']['cash'],cash_after=paired[4]['state']['cash'],arrangements_are_before_charge_and_deferred_outcome_not_guaranteed_success=True,all6_native_font_returns_complete=True,all10_full_foregrounds_equal_native_and_independent=True,only909_915_973_979_965_current106_actual_visits_claimed=True,no_savestate=True,room_assignment_XP_and11days_synthetic_not_earned_progress=True,all_other_4MiB_fixture_bytes_exact=True,no_money_inventory_attributes_health_location_code_menu_or_RNG_fixture=True,production_logical_view=[228,48],production_metrics=[6,12],physical16pixel_oracle_not_logical_capacity=True,original_donor_harness_core_unchanged_and_host_slots_restored=True,review_sheets=sheets,visual_review_pending=True,not_full_route_or_hardware_verification=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(holds=len(holds),paired_controls=len(paired),fee=1000,fixture_changes=len(fixture['changes'])),flush=True)
