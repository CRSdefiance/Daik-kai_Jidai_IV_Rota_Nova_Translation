"""Current ordinary fallback sample plus explicitly historical six-family samples."""
from pathlib import Path
import re,struct
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save
from scripts.primary_town_native_font_v2102 import font_tools,glyph_codes
from scripts.verify_shipyard_gameplay_v760 import independent_font,models
from scripts.verify_market_gameplay_v753 import state
from scripts.aggregate_barmaid_gameplay_v780 import actual_state

ROOT=Path('work/analysis/barmaid_context_actual_v2220')
RUN=Path('work/analysis/barmaid_intro_actual_v2216')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/barmaid_intro_actual_v2216_V2171')
NATIVE=Path('work/analysis/barmaid_actual_continuations_v2219/actual_snapshot_native_font_continuations.json')
HISTORICAL=Path('work/analysis/barmaid_integration_v780/gameplay_verification.json')
ROM=Path('out/all_routes_combined_v2171_candidate.nds')

if __name__=='__main__':
    assert not ROOT.exists()
    ROOT.mkdir(parents=True)
    rom=NdsImage.open(ROM);arm,common,kanji=[rom.read_file(p)for p in('/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT')]
    entries=current_entries(common,arm)
    plan,terminal,report,obs,native=[read(p)for p in(RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',CAP/'common_observer/requests.json',NATIVE)]
    assert terminal['terminal']and terminal['all_observer_host_slots_restored']
    assert report['frames']==9201 and report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
    assert not any(v for k,v in report.items()if k.startswith('synthetic_'))
    assert not obs['errors']and not obs['mismatches']and obs['all_host_slots_restored_and_core_file_exact']
    assert report['ROM_sha256']==plan['candidate_sha256']==sha(ROM.read_bytes())
    assert sha(Path(plan['original_genuine_save']).read_bytes())==plan['donor_sha256']=='05fa512b078fd01a8f6bee605254e9f72bfe3453c0ea098d977c87d86b6b693e'
    assert plan['schedule_reference_donor_differs_from_current_London_donor']and plan['inherited_battery_provenance_not_reearned']
    assert native['ARM9_sha256']==sha(arm)and len(native['cases'])==len(obs['rows'])==9
    assert all(c['complete_native_return']and c['SP_preserved']and c['callee_registers_preserved']and not c['faults']and not c['error']for c in native['cases'])
    assert not any(989<=r['source_request']['ID']<=1019 for r in obs['rows'])
    row,=[r for r in obs['rows']if r['source_request']['ID']==827]
    raw=Path(row['snapshots']['WRAM']['path']).read_bytes();assert sha(raw)==row['snapshots']['WRAM']['sha256']
    p=struct.unpack_from('<I',arm,0x5444C)[0]-0x02000000
    printf=raw[p:p+512].split(bytes(1))[0]
    match=re.fullmatch(b'(.*?)'.join(re.escape(p)for p in entries[827].text.split(b'%s')),printf)
    assert match and match.groups()==(b'Hodram',)
    text=bytes.fromhex(row['text_hex']);lines=[s.strip().decode('cp932')for s in text.split(b'\n')]
    assert b' '.join(text.split())==b' '.join(printf.split())and row['bounds']==[0,0,228,48]
    raster,_,_=font_tools(rom);events=[]
    plane=raster(arm,text,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000,glyph_events=events)
    assert plane==independent_font(arm,kanji,lines)and[r['code']for r in events if r['code']!=32]==glyph_codes(text)
    pixels={(16+i%228,296+i//228)for i,v in enumerate(plane)if v==1}
    frames={r['frame']:r for r in report['frames_captured']};holds=[]
    for f in(7000,7200):
        capture=frames[f];assert sha(Path(capture['path']).read_bytes())==capture['PNG_sha256']
        image=Image.open(capture['path']).convert('RGB')
        actual={(x,y)for y in range(294,360)for x in range(16,244)if image.getpixel((x,y))==(0,8,0)}
        assert actual==pixels,(f,len(actual-pixels),len(pixels-actual))
        holds.append(dict(message_ID=827,font_frame=row['frame'],hold_frame=f,lines=lines,arguments_hex=[b'Hodram'.hex()],capture=capture['path'],capture_sha256=capture['PNG_sha256'],complete_current_native_independent_and_visible_foreground_equal=True,current31_editorial_visit_credit=False))
    snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']};states=[]
    for f,cash,stage in((3200,40659,0),(5000,40654,0),(7000,40644,0),(8000,40644,1),(9200,40639,1)):
        raw=Path(snapshots[f]['path']).read_bytes();assert sha(raw)==snapshots[f]['sha256']
        s,m,b=state(arm,raw),models(arm,raw),actual_state(arm,raw,0)
        assert s['cash']==cash and b['original_relationship_stage']==stage
        assert b['actor_ID']==187 and b['gift_item_ID']==128 and b['original_gift_owner_kind']==4 and b['original_gift_owner_detail']==2 and b['gift_availability_mask']==0
        states.append(dict(frame=f,state=s,models=m,original_barmaid_state=b,RAM_sha256=sha(raw)))
    assert all({k:v for k,v in r['models'].items()if k!='company'}=={k:v for k,v in states[0]['models'].items()if k!='company'}for r in states)
    assert all({k:v for k,v in r['state'].items()if k!='cash'}=={k:v for k,v in states[0]['state'].items()if k!='cash'}for r in states)
    controls=[dict(frame=f,capture=frames[f]['path'],capture_sha256=frames[f]['PNG_sha256'])for f in(5400,5800,6200,6600,7600,8800,9000,9200)]
    old=read(HISTORICAL)
    assert old['actual_IDs']==[989,990,991,999,1000,1014]and old['actual_complete_holds']==12 and old['only_declared_location_and_inventory_fixtures']
    source_proofs=[];historical_holds=[];old_entries=None
    for item in old['scenario_proofs']:
        path=Path(item['path']);assert sha(path.read_bytes())==item['sha256'];proof=read(path)
        assert proof['candidate_sha256']==old['candidate_sha256']
        for report_path in proof['capture_reports']:
            previous=read(report_path)
            assert sha(Path(previous['ROM']).read_bytes())==previous['ROM_sha256']
            if previous['ROM_sha256']==old['candidate_sha256']:
                previous_rom=NdsImage.open(previous['ROM'])
                old_entries=common_message_entries(previous_rom.read_file('/COMMON/MESFILE.DK4'),previous_rom.read_file('/__arm9__.bin'),clean=False)
        for h in proof['holds']:
            capture=h['capture'];assert sha(Path(capture['path']).read_bytes())==capture['PNG_sha256']
            assert h['complete_independent_font_and_blank_paper_exact']and h['all_other_pixels_exact']
            historical_holds.append(dict(message_ID=h['message_id'],frame=h['frame'],capture=capture['path'],capture_sha256=capture['PNG_sha256'],historical_V780_not_a_current_visit=True,source_proof=str(path),source_proof_sha256=item['sha256']))
        source_proofs.append(dict(path=str(path),sha256=item['sha256']))
    assert len(historical_holds)==12 and old_entries is not None
    assert all(old_entries[n].text==entries[n].text for n in range(989,1020))
    sheets=[]
    for name,records,key in(('current_fallback827_holds',holds,'hold_frame'),('current_London_transition_frames',controls,'frame'),('historical_V780_barmaid_family_holds',historical_holds,'frame')):
        sheet=Image.new('RGB',(1024,410*((len(records)+3)//4)),'#263238');draw=ImageDraw.Draw(sheet)
        for i,r in enumerate(records):
            x,y=i%4*256,i//4*410
            prefix='OLD V780'if 'historical' in name else'CURRENT V2171'
            draw.text((x+3,y+3),f"{prefix} ID{r.get('message_ID','context')} f{r[key]}",fill='white')
            sheet.paste(Image.open(r['capture']).convert('RGB'),(x,y+22))
        path=ROOT/(name+'.png');sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),scope='historical-V780-only'if 'historical'in name else'current-fallback827-context;no-new31-visit'))
    save(ROOT/'current_fallback_and_historical_family_evidence.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),source_plan=str(RUN/'run_plan.json'),source_plan_sha256=sha((RUN/'run_plan.json').read_bytes()),source_report=str(CAP/'capture_report.json'),source_report_sha256=sha((CAP/'capture_report.json').read_bytes()),source_observer=str(CAP/'common_observer/requests.json'),source_observer_sha256=sha((CAP/'common_observer/requests.json').read_bytes()),native_continuation=str(NATIVE),native_continuation_sha256=sha(NATIVE.read_bytes()),current_actual_holds=holds,current_transition_frames=controls,current_native_state_controls=states,current_all9_unstubbed_font_returns_complete=True,current_cash_sequence=[40659,40654,40644,40644,40639],ordinary_total_drink_cost=20,current_original_relationship_stage0_to1=True,current_gift_owner_and_availability_unchanged=True,current_fleet_and_ships_unchanged=True,current_company_hash_includes_paid_cash=True,current_state_is_within_run_not_paired_to_Istanbul_schedule_donor=True,current_no_fixture_or_savestate=True,current_ordinary_London_uses_source_fallback827_not989=True,current31_new_actual_ID_visits=[],historical_family_proof=str(HISTORICAL),historical_family_proof_sha256=sha(HISTORICAL.read_bytes()),historical_scenario_proofs=source_proofs,historical_holds=historical_holds,historical_all31_complete_encoded_paragraphs_identical_to_current=True,historical_12holds_for6consumer_families_not_new_V2171_visits=True,historical_location_inventory_fixtures_not_earned_travel_or_gifts=True,new_current_native273_layouts_and52_full_fonts_supply_current_dispatch_font_proof=True,latent996_no_normal_activation_claim=True,review_sheets=sheets,visual_review_pending=True,no_exhaustive_condition_full_route_or_hardware_claim=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(current_fallback827_holds=2,new_current31_visits=0,historical_family_holds=12,historical_families=6,all31_old_current_bytes_equal=True),flush=True)
