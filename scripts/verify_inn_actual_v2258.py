"""Current complete Inn foregrounds, native font returns, nightly charges and transitions."""
from pathlib import Path
import re,struct
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from scripts.verify_village_wrap_v608 import read,save
from scripts.primary_town_native_font_v2102 import font_tools,glyph_codes
from scripts.verify_shipyard_gameplay_v760 import independent_font,models
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_guild_transactions_actual_v2244 import snapshots
from scripts.verify_personal_gameplay_v841 import get_machine
ROOT=Path('work/analysis/inn_actual_verification_v2258');RUN=Path('work/analysis/inn_actual_v2253')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/inn_actual_v2253_V2171')
NATIVE=Path('work/analysis/inn_actual_continuations_v2257/actual_snapshot_native_font_continuations.json')
ROM=Path('out/all_routes_combined_v2171_candidate.nds');EXPECTED={1177:(4800,),1178:(5200,),1179:(6200,),1180:(7000,),1181:(7400,)}
def clock(arm,raw):
    u,get=get_machine(arm,raw);p=get(0xCB1B4);return struct.unpack('<I',u.mem_read(p+8,4))[0]
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True);rom=NdsImage.open(ROM);arm,common,kanji=[rom.read_file(p)for p in('/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT')];entries=current_entries(common,arm)
    plan,terminal,report,obs,native=[read(p)for p in(RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',CAP/'common_observer/requests.json',NATIVE)]
    assert terminal['terminal']and terminal['all_observer_host_slots_restored']and report['frames']==8601 and report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']and not any(v for k,v in report.items()if k.startswith('synthetic_'))
    assert not obs['errors']and not obs['mismatches']and obs['all_host_slots_restored_and_core_file_exact']and report['ROM_sha256']==plan['candidate_sha256']==sha(ROM.read_bytes())
    assert sha(Path(plan['original_genuine_save']).read_bytes())==plan['donor_sha256']=='d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
    prior=read(plan['prior_report']);assert sha(Path(plan['prior_report']).read_bytes())==plan['prior_report_sha256']and report['scripted_input_schedule']==prior['scripted_input_schedule']and report['core_options']==prior['core_options']
    assert native['ARM9_sha256']==sha(arm)and len(native['cases'])==5 and all(c['complete_native_return']and c['SP_preserved']and c['callee_registers_preserved']and not c['faults']and not c['error']for c in native['cases'])
    selected=[r for r in obs['rows']if r['source_request']['ID']in EXPECTED];assert len(selected)==5
    frames={r['frame']:r for r in report['frames_captured']};raster,_,_=font_tools(rom);holds=[]
    for row in selected:
        n=row['source_request']['ID'];full=next(c for c in native['cases']if c['message_ID']==n);assert row['bounds']==[0,0,228,48]and full['text_hex']==row['text_hex']
        raw=Path(row['snapshots']['WRAM']['path']).read_bytes();assert sha(raw)==row['snapshots']['WRAM']['sha256'];p=struct.unpack_from('<I',arm,0x5444C)[0]-0x02000000;printf=raw[p:p+512].split(bytes(1))[0]
        match=re.fullmatch(b'(.*?)'.join(re.escape(p)for p in entries[n].text.split(b'%s')),printf);assert match
        if n==1180:assert match.groups()==('３'.encode('cp932'),)
        text=bytes.fromhex(row['text_hex']);lines=[s.strip().decode('cp932')for s in text.split(b'\n')];assert b' '.join(text.split())==b' '.join(printf.split());events=[];plane=raster(arm,text,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000,glyph_events=events)
        assert plane==independent_font(arm,kanji,lines)and [r['code']for r in events if r['code']!=32]==[r['code']for r in full['glyph_events']if r['code']!=32]==glyph_codes(text)
        assert sorted({r['y']for r in full['glyph_events']})==list(range(0,12*len(lines),12));pixels={(16+i%228,296+i//228)for i,v in enumerate(plane)if v==1}
        for f in EXPECTED[n]:
            c=frames[f];assert sha(Path(c['path']).read_bytes())==c['PNG_sha256'];im=Image.open(c['path']).convert('RGB');actual={(x,y)for y in range(294,360)for x in range(16,244)if im.getpixel((x,y))==(0,8,0)};assert actual==pixels
            holds.append(dict(message_ID=n,font_frame=row['frame'],hold_frame=f,arguments_hex=[v.hex()for v in match.groups()],lines=lines,capture=c['path'],capture_sha256=c['PNG_sha256'],complete_native_independent_and_visible_foreground_equal=True))
    cr,pr=snapshots(report),snapshots(prior);oldarm=NdsImage.open(prior['ROM']).read_file('/__arm9__.bin');paired=[];random_diffs=[]
    for f in(3200,4400,5200,5600,6200,7000,7400,7800,8200,8600):
        raw,old=[Path(m[f]['path']).read_bytes()for m in(cr,pr)];assert sha(raw)==cr[f]['sha256']and sha(old)==pr[f]['sha256'];s,m,c=state(arm,raw),models(arm,raw),clock(arm,raw)
        assert s==state(oldarm,old)and m==models(oldarm,old)and c==clock(oldarm,old)
        objects_equal=persistent_objects(arm,raw)==persistent_objects(oldarm,old);tasks_equal=tasks(arm,raw)==tasks(oldarm,old)
        if not(objects_equal and tasks_equal):random_diffs.append(dict(frame=f,persistent_objects_equal=objects_equal,tasks_equal=tasks_equal,not_globally_approved=True))
        paired.append(dict(frame=f,state=s,models=m,clock=c,current_RAM_sha256=sha(raw),historical_RAM_sha256=sha(old),source_state_company_fleet_ship_and_clock_equal=True,persistent_objects_equal=objects_equal,tasks_equal=tasks_equal))
    assert paired[0]['state']['cash']-paired[-1]['state']['cash']==4 and paired[-1]['clock']-paired[0]['clock']==192
    assert all({k:v for k,v in r['models'].items()if k!='company'}=={k:v for k,v in paired[0]['models'].items()if k!='company'}for r in paired)
    controls=[dict(frame=f,capture=frames[f]['path'],capture_sha256=frames[f]['PNG_sha256'])for f in(4000,4400,5600,5800,6600,7800,8200,8600)]
    sheets=[]
    for name,rows,key in(('five_current_Inn_holds',holds,'hold_frame'),('eight_current_Inn_transitions',controls,'frame')):
        sheet=Image.new('RGB',(1024,410*((len(rows)+3)//4)),'#263238');draw=ImageDraw.Draw(sheet)
        for i,r in enumerate(rows):
            assert sha(Path(r['capture']).read_bytes())==r['capture_sha256'];x,y=i%4*256,i//4*410;draw.text((x+3,y+3),f"CURRENT ID{r.get('message_ID','context')} f{r[key]}",fill='white');sheet.paste(Image.open(r['capture']).convert('RGB'),(x,y+22))
        p=ROOT/(name+'.png');sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes()),scope='actual-current-fixture-free-Inn-stays'))
    save(ROOT/'current_Inn_foreground_state_transitions.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),source_plan=str(RUN/'run_plan.json'),source_plan_sha256=sha((RUN/'run_plan.json').read_bytes()),source_report=str(CAP/'capture_report.json'),source_report_sha256=sha((CAP/'capture_report.json').read_bytes()),source_observer=str(CAP/'common_observer/requests.json'),source_observer_sha256=sha((CAP/'common_observer/requests.json').read_bytes()),native_continuation=str(NATIVE),native_continuation_sha256=sha(NATIVE.read_bytes()),actual_holds=holds,transition_frames=controls,paired_native_state_model_clock_controls=paired,unapproved_random_daily_object_differences=random_diffs,one_night_then_three_nights_charge4_and_advance192ticks=True,only1177_to1181_current54_visits=True,greeting63_context_only_no_extra_credit=True,all5_native_font_returns_complete=True,no_fixture_savestate_or_original_save_mutation=True,inherited_battery_history_not_reearned=True,production_logical_view=[228,48],production_metrics=[6,12],physical16pitch_separate=True,review_sheets=sheets,visual_review_pending=True,no_full_route_or_hardware_claim=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(current_holds=5,paired_state_model_clock_controls=10,charge=4,ticks=192,unapproved_random_daily_differences=len(random_diffs)))
