"""Recheck historical126 holds against current native text/font; no new GPU visits."""
from pathlib import Path
import struct
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from dk4tool.patch.levelup_stat_format import current_entries as historical_entries
from scripts.verify_ceremony_heroes_v825 import identity,cstring
from scripts.primary_town_native_font_v2102 import font_tools
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_ceremony_consumers_v808 import production_functions
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/ceremony_history_v2270');OLD=Path('translations/ceremony_editorial_final_review_v1.json')
IDS=[64,289,290,291,293,294,295,*range(1200,1245)]
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True);old=read(OLD);current=NdsImage.open('out/all_routes_combined_v2171_candidate.nds');arm,common,font=[current.read_file(p)for p in('/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT')];entries=current_entries(common,arm)
    prior=NdsImage.open(old['candidate']);oldarm,oldcommon=[prior.read_file(p)for p in('/__arm9__.bin','/COMMON/MESFILE.DK4')];previous=historical_entries(oldcommon,oldarm);assert sha(Path(old['candidate']).read_bytes())==old['candidate_sha256']
    assert all(previous[n].text==entries[n].text for n in IDS)and prior.read_file('/GRP/KANJI.FNT')==font
    for p,h in old['source_proof_sha256'].items():assert sha(Path(p).read_bytes())==h
    rows={r['message_id']:r for r in read('translations/ceremony_contextual_editorial_manuscript_v1.json')['records']};matrix=read('work/analysis/ceremony_layouts_v2268/all52_current_native_layouts.json');raster,_,_=font_tools(current);ordinary,modal,_,_=production_functions()
    reports={};roms={};holds=[];planes={};representatives=[]
    for row in old['records']:
        n=row['message_id']
        for sample in row['actual_samples']:
            capture=sample['capture'];folder=Path(capture['path']).parent;rp=folder/'capture_report.json'
            if str(rp)not in reports:
                report=read(rp);assert report['cold_boot']and not report['savestate_loaded']and not report['callback_errors'];source=NdsImage.open(report['ROM']);digest=sha(Path(report['ROM']).read_bytes());assert digest==report['ROM_sha256']and source.read_file('/COMMON/MESFILE.DK4')==oldcommon and source.read_file('/GRP/KANJI.FNT')==font
                snapshots={r['frame']:r for r in report.get('read_only_capture_RAM_snapshots',[])+report.get('read_only_pause_RAM_snapshots',[])}
                reports[str(rp)]=dict(report=report,snapshots=snapshots,sha256=sha(rp.read_bytes()));roms[report['ROM']]=dict(sha256=digest,ARM9_sha256=sha(source.read_file('/__arm9__.bin')))
            bundle=reports[str(rp)];report=bundle['report'];assert report['ROM_sha256']==sample['source_sample_ROM_sha256'];snap=bundle['snapshots'][sample['frame']];raw=Path(snap['path']).read_bytes();assert sha(raw)==snap['sha256']and snap['read_only_export'];source=NdsImage.open(report['ROM']);sourcearm=source.read_file('/__arm9__.bin');who=identity(sourcearm,raw)
            assert who['captain']==sample['actual_captain']and who['notice_name']==sample['actual_notice_name']
            values=((b'Parthenon'if who['town']==19 else b'Cappadocia'),)if n==1219 else (who['notice_name'].encode('ascii'),)if n in(290,291,293,294,295)else()
            case=next(c for c in matrix['cases']if c['message_ID']==n and c['values_hex']==[v.hex()for v in values]);encoded=bytes.fromhex(case['formatted_hex']);lines=case['lines'];assert lines==sample['lines']
            owner,wrapped=[struct.unpack_from('<I',sourcearm,p)[0]for p in(0x552A0,0x54450)];assert cstring(raw,owner+0x2030)==entries[n].text and cstring(raw,wrapped)==encoded
            assert sha(Path(capture['path']).read_bytes())==capture['PNG_sha256'];picture=Image.open(capture['path']).convert('RGB')
            if encoded not in planes:
                plane=raster(arm,encoded,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000);expected=independent_font(arm,font,lines)
                if n==64:expected=b''.join(expected[y*228+6:(y+1)*228]+bytes(6)for y in range(64))
                assert plane==expected;planes[encoded]=plane
            plane=planes[encoded];expected_ink={(16+i%228,296+i//228)for i,p in enumerate(plane)if p==1};actual_ink={(x,y)for y in range(294,366)for x in range(16,244)if picture.getpixel((x,y))==(0,8,0)};assert expected_ink==actual_ink,(n,sample['frame'],len(expected_ink-actual_ink),len(actual_ink-expected_ink))
            h=dict(message_ID=n,frame=sample['frame'],capture=capture['path'],capture_sha256=capture['PNG_sha256'],source_report=str(rp),source_report_sha256=bundle['sha256'],source_proof=sample['proof'],source_proof_sha256=old['source_proof_sha256'][sample['proof']],historical_ROM_sha256=report['ROM_sha256'],historical_captain=who['captain'],historical_notice_name=who['notice_name'],lines=lines,values_hex=[v.hex()for v in values],current_stored_paragraph_formatted_bytes_native_independent_foreground_and_all_blank_paper_equal=True,resident_complete_template_and_formatted_buffer_equal_current=True,historical_fixture_inputs_not_earned_or_current_visit=True);holds.append(h)
            if n not in{r['message_ID']for r in representatives}:representatives.append(h)
    assert len(holds)==126 and len(representatives)==52 and {h['message_ID']for h in holds}==set(IDS)
    sheets=[]
    for start in range(0,len(representatives),12):
        selected=representatives[start:start+12];sheet=Image.new('RGB',(1024,410*((len(selected)+3)//4)),'#263238');draw=ImageDraw.Draw(sheet)
        for i,r in enumerate(selected):
            x,y=i%4*256,i//4*410;draw.text((x+3,y+3),f"HISTORICAL ID{r['message_ID']} f{r['frame']} hero{r['historical_captain']}",fill='white');sheet.paste(Image.open(r['capture']).convert('RGB'),(x,y+22))
        p=ROOT/f'historical_all52_representatives_{start//12:02d}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes()),scope='historical-only;current-native-pixel-binding-not-current-GPU-visit'))
    metadata={p:dict(sha256=b['sha256'],ROM=b['report']['ROM'],ROM_sha256=b['report']['ROM_sha256'],frames=b['report']['frames'],synthetic_input_receipts={k:v for k,v in b['report'].items()if k.startswith('synthetic_')and v},original_goal_complete=b['report'].get('goal_complete'),original_hardware_verified=b['report'].get('hardware_device_verification'))for p,b in reports.items()}
    save(ROOT/'historical126_current_pixel_binding.json',dict(candidate_sha256=sha(Path('out/all_routes_combined_v2171_candidate.nds').read_bytes()),historical_final_review=str(OLD),historical_final_review_sha256=sha(OLD.read_bytes()),historical_proofs=old['source_proof_sha256'],historical_holds=holds,historical_IDs=IDS,historical_sampled_ROMs=roms,historical_reports=metadata,all52_complete_stored_paragraphs_and_KANJI_exact_current=True,all126_actual_foregrounds_and_blank_paper_rechecked_current_native_and_independent_font=True,all126_resident_templates_and_formatted_buffers_equal_current=True,source64_zero_origin_pixel_binding_distinct=True,representative_holds_viewable=representatives,review_sheets=sheets,representative52_visual_review_pending=True,new_current_emulator_runs=0,new_current_ID_visits=[],all_fixtures_originally_declared_not_earned_or_natural_campaign_progress=True,strict_random_trace_failures_remain_unapproved='docs/ceremony_random_cause_v824_checkpoint.md',no_new_every_frame_transparency_random_outcome_hardware_or_full_route_approval=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(historical_holds=126,IDs=52,current_pixel_bindings=126,sheets=5,new_current_visits=0))
