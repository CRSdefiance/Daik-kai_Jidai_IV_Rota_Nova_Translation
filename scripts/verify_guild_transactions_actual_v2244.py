"""Current full Guild foregrounds, distinct YesNo parent, paid state and ordinary returns."""
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

ROOT=Path('work/analysis/guild_transactions_verification_v2244')
RUN=Path('work/analysis/guild_transactions_actual_v2237')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/guild_transactions_actual_v2237_V2171')
NATIVE=Path('work/analysis/guild_actual_continuations_v2243/actual_snapshot_native_font_continuations.json')
ROM=Path('out/all_routes_combined_v2171_candidate.nds')
EXPECTED={1071:(7200,8400,10000),1073:(8000,9200),1074:(9600,),1085:(11600,12800),1086:(12400,13600),1096:(14000,)}

def snapshots(report):
    result={}
    for row in report.get('read_only_capture_RAM_snapshots',[])+report.get('read_only_pause_RAM_snapshots',[]):
        if row['frame']in result:assert result[row['frame']]['sha256']==row['sha256']
        result[row['frame']]=row
    return result

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    rom=NdsImage.open(ROM);arm,common,kanji=[rom.read_file(p)for p in('/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT')];entries=current_entries(common,arm)
    plan,terminal,report,obs,native=[read(p)for p in(RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',CAP/'common_observer/requests.json',NATIVE)]
    assert terminal['terminal']and terminal['all_observer_host_slots_restored']
    assert report['frames']==15601 and report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
    assert not any(v for k,v in report.items()if k.startswith('synthetic_'))
    assert not obs['errors']and not obs['mismatches']and obs['all_host_slots_restored_and_core_file_exact']
    assert report['ROM_sha256']==plan['candidate_sha256']==sha(ROM.read_bytes())
    assert sha(Path(plan['original_genuine_save']).read_bytes())==plan['donor_sha256']=='942c74828a7b7396f7567ca2d405ddc4cdd329e4837f591777d35ee458794b0f'
    prior=read(plan['prior_report']);assert sha(Path(plan['prior_report']).read_bytes())==plan['prior_report_sha256']
    assert report['scripted_input_schedule']==prior['scripted_input_schedule']and report['core_options']==prior['core_options']
    assert native['ARM9_sha256']==sha(arm)and len(native['cases'])==6
    assert all(c['complete_native_return']and c['SP_preserved']and c['callee_registers_preserved']and not c['faults']and not c['error']for c in native['cases'])
    selected=[r for r in obs['rows']if r['source_request']['ID']in EXPECTED]
    assert len(selected)==6 and {r['source_request']['ID']for r in selected}==set(EXPECTED)
    frames={r['frame']:r for r in report['frames_captured']};raster,_,_=font_tools(rom);holds=[]
    for row in selected:
        n=row['source_request']['ID'];full=next(c for c in native['cases']if c['message_ID']==n)
        assert row['bounds']==[0,0,228,48]and full['text_hex']==row['text_hex']
        raw=Path(row['snapshots']['WRAM']['path']).read_bytes();assert sha(raw)==row['snapshots']['WRAM']['sha256']
        p=struct.unpack_from('<I',arm,0x5444C)[0]-0x02000000;printf=raw[p:p+512].split(bytes(1))[0]
        match=re.fullmatch(b'(.*?)'.join(re.escape(p)for p in entries[n].text.split(b'%s')),printf);assert match
        if n==1073:assert match.groups()==('７７００'.encode('cp932'),)
        if n==1086:assert match.groups()==('６１６０'.encode('cp932'),)
        text=bytes.fromhex(row['text_hex']);lines=[s.strip().decode('cp932')for s in text.split(b'\n')];assert b' '.join(text.split())==b' '.join(printf.split())
        events=[];plane=raster(arm,text,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000,glyph_events=events)
        assert plane==independent_font(arm,kanji,lines)
        assert [r['code']for r in events if r['code']!=32]==[r['code']for r in full['glyph_events']if r['code']!=32]==glyph_codes(text)
        assert sorted({r['y']for r in full['glyph_events']})==list(range(0,12*len(lines),12))
        pixels={(16+i%228,296+i//228)for i,v in enumerate(plane)if v==1}
        for f in EXPECTED[n]:
            capture=frames[f];assert sha(Path(capture['path']).read_bytes())==capture['PNG_sha256'];image=Image.open(capture['path']).convert('RGB')
            actual={(x,y)for y in range(294,360)for x in range(16,244)if image.getpixel((x,y))==(0,8,0)}
            assert actual==pixels,(n,f,len(actual-pixels),len(pixels-actual))
            holds.append(dict(message_ID=n,font_frame=row['frame'],hold_frame=f,arguments_hex=[v.hex()for v in match.groups()],lines=lines,capture=capture['path'],capture_sha256=capture['PNG_sha256'],complete_native_independent_and_visible_foreground_equal=True))
    assert len(holds)==11
    current_ram,old_ram=snapshots(report),snapshots(prior);old_arm=NdsImage.open(prior['ROM']).read_file('/__arm9__.bin');paired=[]
    for f,cash in((3200,38816),(8000,38816),(8400,38816),(9600,38816),(10000,31116),(12400,31116),(12800,31116),(14000,31116),(14400,37276),(15600,37276)):
        raw,previous=[Path(m[f]['path']).read_bytes()for m in(current_ram,old_ram)]
        assert sha(raw)==current_ram[f]['sha256']and sha(previous)==old_ram[f]['sha256']
        s,m,objects,t=state(arm,raw),models(arm,raw),persistent_objects(arm,raw),tasks(arm,raw)
        assert s==state(old_arm,previous)and s['cash']==cash
        assert m==models(old_arm,previous)and objects==persistent_objects(old_arm,previous)and t==tasks(old_arm,previous)
        paired.append(dict(frame=f,state=s,models=m,persistent_objects=objects,task_sha256=sha(t),current_RAM_sha256=sha(raw),reference_RAM_sha256=sha(previous),state_company_fleet_ship_persistent_and_task_objects_equal_historical_same_inputs=True))
    assert all({k:v for k,v in r['models'].items()if k!='company'}=={k:v for k,v in paired[0]['models'].items()if k!='company'}for r in paired)
    assert paired[0]['persistent_objects']==paired[-1]['persistent_objects']
    controls=[dict(frame=f,capture=frames[f]['path'],capture_sha256=frames[f]['PNG_sha256'])for f in(7600,10400,10800,13200,14400,14800,15200,15600)]
    for r in controls:assert sha(Path(r['capture']).read_bytes())==r['capture_sha256']
    sheets=[]
    for name,records,key in(('eleven_current_Guild_holds',holds,'hold_frame'),('eight_current_Guild_menu_returns',controls,'frame')):
        sheet=Image.new('RGB',(1024,410*((len(records)+3)//4)),'#263238');draw=ImageDraw.Draw(sheet)
        for i,r in enumerate(records):
            x,y=i%4*256,i//4*410;draw.text((x+3,y+3),f"CURRENT ID{r.get('message_ID','context')} f{r[key]}",fill='white');sheet.paste(Image.open(r['capture']).convert('RGB'),(x,y+22))
        path=ROOT/(name+'.png');sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),scope='actual-current-fixture-free-Seoul-Guild'))
    save(ROOT/'current_Guild_full_foreground_state_transitions.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),source_plan=str(RUN/'run_plan.json'),source_plan_sha256=sha((RUN/'run_plan.json').read_bytes()),source_report=str(CAP/'capture_report.json'),source_report_sha256=sha((CAP/'capture_report.json').read_bytes()),source_observer=str(CAP/'common_observer/requests.json'),source_observer_sha256=sha((CAP/'common_observer/requests.json').read_bytes()),native_continuation=str(NATIVE),native_continuation_sha256=sha(NATIVE.read_bytes()),actual_holds=holds,transition_frames=controls,paired_native_state_model_task_controls=paired,source_purchase_price=7700,source_sale_price=6160,cash_before=38816,cash_after_purchase=31116,cash_after_sale=37276,declined_purchase_and_sale_preserve_cash=True,all6_selected_native_font_returns_complete=True,all11_full_foregrounds_equal_native_and_independent=True,only1071_1073_1074_1085_1086_1096_new_current79_visits=True,other3_observer_rows_context_only_not_source_attribution_or_editorial_credit=True,duplicate62_attribution_not_assumed_for_direct_item_description=True,current_fleet_ships_and_final_persistent_objects_unchanged=True,paid_company_cash_compared_to_corresponding_source_run_not_required_unchanged=True,no_fixture_or_savestate_or_original_save_mutation=True,source_save_history_inherited_not_reearned=True,production_logical_view=[228,48],production_metrics=[6,12],physical16pitch_oracle_not_logical_capacity=True,original_harness_core_and_host_slots_restored=True,review_sheets=sheets,visual_review_pending=True,no_full_route_or_hardware_claim=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(current_holds=11,current_IDs=sorted(EXPECTED),paired_controls=10,purchase=7700,sale=6160,cash=37276),flush=True)
