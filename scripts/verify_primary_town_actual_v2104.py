"""Actual revised town holds: source text, full native ink and unchanged controls."""
from pathlib import Path
import struct
from PIL import Image,ImageChops,ImageDraw
from scripts.primary_town_native_font_v2102 import font_tools,glyph_codes
from scripts.verify_market_gameplay_v753 import snapshot,state
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/town_services_actual_v2104')
RUN=Path('work/analysis/town_services_font_actual_v2098')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_services_font_actual_v2098_V2097')
OLD=Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_services_font_actual_v2060_V2047')
BODY=(16,294,244,346)
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 plan,terminal,report,obs=[read(p)for p in(RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',CAP/'common_observer/requests.json')];old_report=read(OLD/'capture_report.json')
 assert terminal['terminal']and terminal['all_observer_host_slots_restored']and report['frames']==38500 and report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
 assert report['ROM_sha256']==plan['candidate_sha256']==sha(Path(plan['candidate']).read_bytes())and report['scripted_input_schedule']==read(plan['inputs'])==old_report['scripted_input_schedule']
 assert len(report['synthetic_gallery_fixtures'])==1 and not report['synthetic_gallery_fixtures'][0]['earned_unlock_verified']and all(k=='synthetic_gallery_fixtures'or not v for k,v in report.items()if k.startswith('synthetic_'))
 assert sha(Path(plan['existing_isolated_system_unlock']).read_bytes())==plan['donor_sha256']and not obs['errors']and not obs['mismatches']and obs['all_host_slots_restored_and_core_file_exact']
 assert [r['source_request']['ID']for r in obs['rows']]==[49,8,51,53,55,56,59,61]
 rom=NdsImage.open(plan['candidate']);arm=rom.read_file('/__arm9__.bin');old_arm=NdsImage.open('out/all_routes_combined_v2047_candidate.nds').read_file('/__arm9__.bin');raster,independent,meta=font_tools(rom);kanji=rom.read_file('/GRP/KANJI.FNT')
 routes=read('work/analysis/town_services_research_routes_v2083/research_runtime_all84_original_BL_routes.json');frames={r['frame']:r for r in report['frames_captured']};previous={r['frame']:r for r in old_report['frames_captured']};controls=[];states=[]
 for frame,row in frames.items():
  assert sha(Path(row['path']).read_bytes())==row['PNG_sha256'];current=Image.open(row['path']).convert('RGB');prior=Image.open(previous[frame]['path']).convert('RGB');difference=ImageChops.difference(current,prior)
  if frame>=31000:difference.paste((0,0,0),BODY)
  assert difference.getbbox()is None,(frame,difference.getbbox())
  controls.append(dict(frame=frame,all_outside_text_paper_pixels_exact_to_V2047=True,whole_screen_exact=frame<31000,capture=row['path']))
  if frame>=31000:
   a,b=snapshot(old_report,frame),snapshot(report,frame);assert state(old_arm,a)==state(arm,b)and models(old_arm,a)==models(arm,b),(frame,'native models')
   states.append(dict(frame=frame,native_town_company_fleet_ship_models_and_state_exact=True))
 cases=[];sheet=Image.new('RGB',(1024,820),'#263238');draw=ImageDraw.Draw(sheet)
 for index,row in enumerate(obs['rows']):
  n=row['source_request']['ID'];assert row['CPU_WRAM_DTCM_ITCM_configuration_exact']and row['bounds']==[0,0,228,48]
  for snap in row['snapshots'].values():assert sha(Path(snap['path']).read_bytes())==snap['sha256']
  text=bytes.fromhex(row['text_hex']);arguments=['６００']if n==49 else['Mihwa']if n==55 else[];matches=[r for r in routes['cases']if r['message_ID']==n and r['supplied_arguments']==arguments];assert matches and all(r['research_output_hex']==text.hex()for r in matches)
  following=obs['rows'][index+1]['frame']if index+1<len(obs['rows'])else38501;frame=next(f for f in sorted(frames)if row['frame']<=f<following);photo=Image.open(frames[frame]['path']).convert('RGB');events=[]
  plane=raster(arm,text,0x01FFCE40-0x02000000,size=(228,48),instruction_limit=2000000,glyph_events=events);lines=[s.strip().decode('cp932')for s in text.split(b'\n')];assert plane==independent(arm,kanji,lines)
  assert [e['code']for e in events if e['code']!=32]==glyph_codes(text)
  expected={(16+i%228,296+i//228)for i,v in enumerate(plane)if v==1};actual={(x,y)for y in range(BODY[1],BODY[3])for x in range(BODY[0],BODY[2])if photo.getpixel((x,y))==(0,8,0)};assert actual==expected,(n,frame,len(actual-expected),len(expected-actual))
  cases.append(dict(message_ID=n,font_frame=row['frame'],hold_frame=frame,source_request=row['source_request'],actual_text_hex=text.hex(),lines=lines,supplied_arguments=arguments,full_native_independent_plane_and_every_visible_foreground_pixel_exact=True,first_final_letters_complete_and_paper_bounds_clear=True,plane_sha256=sha(plane),capture=frames[frame]['path'],capture_sha256=frames[frame]['PNG_sha256']))
  x,y=index%4*256,index//4*410;draw.text((x+4,y+4),f'ID{n} frame{frame}',fill='white');sheet.paste(photo,(x,y+22))
 path=ROOT/'eight_revised_town_holds.png';sheet.save(path)
 save(ROOT/'eight_actual_full_ink_holds_and_transitions.json',dict(candidate=plan['candidate'],candidate_sha256=plan['candidate_sha256'],ARM9_sha256=sha(arm),COMMON_sha256=sha(rom.read_file('/COMMON/MESFILE.DK4')),actual_holds=cases,full_controls=controls,native_state_controls=states,font_model=meta,source_observer=str(CAP/'common_observer/requests.json'),source_observer_sha256=sha((CAP/'common_observer/requests.json').read_bytes()),existing_unlock_isolated_not_earned=True,no_savestate_story_location_RNG_funds_outcome_fixture=True,original_donor_and_core_unchanged=True,actual38500frame_replay_complete=True,actual_income_events_and_other_conditional_lines_not_claimed=True,review_sheet=str(path),review_sheet_sha256=sha(path.read_bytes()),visual_review_pending=True,corrected_pagination_proof_and_registered_proof_successor_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(actual_full_pixel_holds=len(cases),frame_controls=len(controls),native_model_controls=len(states),sheet=str(path)))
