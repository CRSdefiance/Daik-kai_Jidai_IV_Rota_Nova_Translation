"""Reuse observed V2171 capacity prompt; bind historical samples without new-visit claims."""
from pathlib import Path
import re,struct
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save
from scripts.primary_town_native_font_v2102 import font_tools,glyph_codes
from scripts.verify_shipyard_gameplay_v760 import independent_font

ROOT=Path('work/analysis/shared_context_actual_v2231')
ROM=Path('out/all_routes_combined_v2171_candidate.nds')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/recruitment_actual_v2202_V2171')
CURRENT=Path('work/analysis/recruitment_actual_verification_v2208/ordinary_recruitment_foreground_state_transitions.json')
NATIVE=Path('work/analysis/recruitment_actual_continuations_v2206/actual_snapshot_native_font_continuations.json')
HISTORICAL=Path('work/analysis/shared_metadata_v783/shared_batch_gameplay_verification.json')

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    rom=NdsImage.open(ROM);arm,common,kanji=[rom.read_file(p)for p in('/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT')]
    entries=current_entries(common,arm)
    current,report,obs,native=[read(p)for p in(CURRENT,CAP/'capture_report.json',CAP/'common_observer/requests.json',NATIVE)]
    assert current['candidate_sha256']==report['ROM_sha256']==sha(ROM.read_bytes())
    assert current['no_savestate_or_any_synthetic_fixture']and report['frames']==8801 and report['cold_boot']and not report['savestate_loaded']
    assert not report['callback_errors']and not obs['errors']and not obs['mismatches']and obs['all_host_slots_restored_and_core_file_exact']
    assert len(current['paired_native_state_model_controls'])==8 and current['source_quoted_cost']==1573 and current['gathered_before_assignment']==34
    assert native['ARM9_sha256']==sha(arm)and len(native['cases'])==7
    row,=[r for r in obs['rows']if r['source_request']['ID']==1042]
    full,=[r for r in native['cases']if r['message_ID']==1042]
    assert full['complete_native_return']and full['SP_preserved']and full['callee_registers_preserved']and not full['faults']and not full['error']
    assert full['text_hex']==row['text_hex']and row['bounds']==[0,0,228,48]
    raw=Path(row['snapshots']['WRAM']['path']).read_bytes();assert sha(raw)==row['snapshots']['WRAM']['sha256']
    p=struct.unpack_from('<I',arm,0x5444C)[0]-0x02000000;printf=raw[p:p+512].split(bytes(1))[0]
    match=re.fullmatch(b'(.*?)'.join(re.escape(p)for p in entries[1042].text.split(b'%s')),printf)
    assert match and match.groups()==('５１'.encode('cp932'),)
    text=bytes.fromhex(row['text_hex']);lines=[s.strip().decode('cp932')for s in text.split(b'\n')]
    assert b' '.join(text.split())==b' '.join(printf.split())
    raster,_,_=font_tools(rom);events=[]
    plane=raster(arm,text,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000,glyph_events=events)
    assert plane==independent_font(arm,kanji,lines)
    assert [r['code']for r in events if r['code']!=32]==[r['code']for r in full['glyph_events']if r['code']!=32]==glyph_codes(text)
    assert sorted({r['y']for r in full['glyph_events']})==list(range(0,12*len(lines),12))
    pixels={(16+i%228,296+i//228)for i,v in enumerate(plane)if v==1}
    frames={r['frame']:r for r in report['frames_captured']};holds=[]
    for f in(6600,7000):
        capture=frames[f];assert sha(Path(capture['path']).read_bytes())==capture['PNG_sha256'];image=Image.open(capture['path']).convert('RGB')
        actual={(x,y)for y in range(294,360)for x in range(16,244)if image.getpixel((x,y))==(0,8,0)}
        assert actual==pixels,(f,len(actual-pixels),len(pixels-actual))
        holds.append(dict(message_ID=1042,font_frame=row['frame'],hold_frame=f,lines=lines,arguments_hex=[v.hex()for v in match.groups()],capture=capture['path'],capture_sha256=capture['PNG_sha256'],complete_current_native_independent_and_visible_foreground_equal=True,reused_existing_V2171_capture_not_a_new_emulator_run=True))
    controls=[dict(frame=f,capture=frames[f]['path'],capture_sha256=frames[f]['PNG_sha256'])for f in(7400,7800,8200,8600,8800)]
    for r in controls:assert sha(Path(r['capture']).read_bytes())==r['capture_sha256']
    old=read(HISTORICAL);assert old['all_required_consumer_families_sampled']and old['actual_complete_holds']==17
    assert old['actual_IDs']==[1020,1022,1028,1029,1032,1034,1035,1042,1065]
    historical_holds=[];source_proofs=[];sampled_roms={}
    for item in old['scenario_proofs']:
        path=Path(item['path']);assert sha(path.read_bytes())==item['sha256'];proof=read(path)
        assert proof['candidate_sha256']==old['candidate_sha256']
        for report_path in proof['capture_reports']:
            prior=read(report_path)
            if prior['ROM_sha256']!=old['candidate_sha256']:continue
            rom_path=Path(prior['ROM']);assert sha(rom_path.read_bytes())==prior['ROM_sha256']
            sampled_roms[str(rom_path)]=prior['ROM_sha256']
        for h in proof['holds']:
            capture=h['capture'];assert sha(Path(capture['path']).read_bytes())==capture['PNG_sha256']
            assert h['complete_independent_font_and_blank_paper_exact']and h['all_other_pixels_exact']
            historical_holds.append(dict(message_ID=h['message_id'],frame=h['frame'],capture=capture['path'],capture_sha256=capture['PNG_sha256'],source_proof=str(path),source_proof_sha256=item['sha256'],historical_V782_V783_not_a_current_visit=True))
        source_proofs.append(dict(path=str(path),sha256=item['sha256']))
    assert len(historical_holds)==17 and sampled_roms
    for path,digest in sampled_roms.items():
        prior=NdsImage.open(path);old_entries=common_message_entries(prior.read_file('/COMMON/MESFILE.DK4'),prior.read_file('/__arm9__.bin'),clean=False)
        assert all(old_entries[n].text==entries[n].text for n in range(1020,1070))
    sheets=[]
    groups=[('current_V2171_1042_holds',holds,'hold_frame','current-reused-fixture-free-capture'),('current_V2171_AssignSailors_returns',controls,'frame','current-reused-fixture-free-capture')]
    groups.extend((f'historical_V782_V783_shared_holds_{i//12:02d}',historical_holds[i:i+12],'frame','historical-only;not-a-current-visit')for i in range(0,len(historical_holds),12))
    for name,records,key,scope in groups:
        sheet=Image.new('RGB',(1024,410*((len(records)+3)//4)),'#263238');draw=ImageDraw.Draw(sheet)
        for i,r in enumerate(records):
            x,y=i%4*256,i//4*410;prefix='OLD V782/783'if name.startswith('historical')else'CURRENT V2171'
            draw.text((x+3,y+3),f"{prefix} ID{r.get('message_ID','context')} f{r[key]}",fill='white');sheet.paste(Image.open(r['capture']).convert('RGB'),(x,y+22))
        path=ROOT/(name+'.png');sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),scope=scope))
    save(ROOT/'current1042_and_historical_shared_family_evidence.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),source_current_proof=str(CURRENT),source_current_proof_sha256=sha(CURRENT.read_bytes()),source_report=str(CAP/'capture_report.json'),source_report_sha256=sha((CAP/'capture_report.json').read_bytes()),source_observer=str(CAP/'common_observer/requests.json'),source_observer_sha256=sha((CAP/'common_observer/requests.json').read_bytes()),native_continuation=str(NATIVE),native_continuation_sha256=sha(NATIVE.read_bytes()),current_actual_holds=holds,current_transition_frames=controls,current_eight_paired_state_model_controls_inherited_from_exact_capture_proof=True,current_original_51_spare_capacity_after34_gathered_and1573_charge=True,current1042_role1_native_fallback_Charles_not_Barkeep=True,current_no_fixture_or_savestate=True,current50_recorded_actual_IDs=[1042],no_new_emulator_run_or_new_conditional_visits=True,historical_family_proof=str(HISTORICAL),historical_family_proof_sha256=sha(HISTORICAL.read_bytes()),historical_scenario_proofs=source_proofs,historical_holds=historical_holds,historical_sampled_ROMs=sampled_roms,historical_all50_complete_encoded_paragraphs_identical_to_current=True,historical_17holds_for9_IDs_eight_scenarios_not_new_V2171_visits=True,historical_405_paired_states_410_screen_controls_2_blink_controls_inherited_not_rerun=True,historical_declared_condition_identity_inventory_fixtures_not_earned_unlock_or_gift_claim=True,current_original_filters_and_consumers_freshly_replayed=True,current857_layouts83_full_fonts_supply_current_dispatch_and_font_proof=True,other49_current_entries_offline_or_historical_not_new_current_visits=True,review_sheets=sheets,visual_review_pending=True,no_exhaustive_conditional_full_route_or_hardware_claim=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(current1042_holds=2,current_recorded_IDs=[1042],new_emulator_runs=0,historical_holds=17,historical_IDs=9,all50_old_current_bytes_equal=True),flush=True)
