"""Terminal ordinary market capture: exact templates, complete ink and real state changes."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
from scripts.primary_town_native_font_v2102 import font_tools,glyph_codes
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/market_context_actual_verification_v2118')
RUN=Path('work/analysis/market_context_actual_v2112')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/market_context_live_v2112_V2097')
PRIOR=Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_services_font_actual_v2098_V2097/capture_report.json')
BODY=(16,294,244,346)
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 plan,terminal,report,obs=[read(p)for p in(RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',CAP/'common_observer/requests.json')]
 assert terminal['terminal'] and terminal['all_observer_host_slots_restored'] and report['frames']==terminal['frames'] and report['frames']<60000
 assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and not obs['errors'] and not obs['mismatches'] and obs['all_host_slots_restored_and_core_file_exact']
 assert report['ROM_sha256']==plan['candidate_sha256']==sha(Path(plan['candidate']).read_bytes())
 assert sha(Path(plan['existing_isolated_system_unlock']).read_bytes())==plan['donor_sha256']
 assert len(report['synthetic_gallery_fixtures'])==1 and not report['synthetic_gallery_fixtures'][0]['earned_unlock_verified']
 assert all(k=='synthetic_gallery_fixtures' or not v for k,v in report.items()if k.startswith('synthetic_'))
 prefix_inputs=read(plan['inputs']);assert report['scripted_input_schedule'][:len(prefix_inputs)]==prefix_inputs
 journal=read(CAP/'navigation_command_journal.json');assert journal['commands_are_not_execution_receipts'] and journal['commands_received'][-1]['command']=={'stop':True}
 assert all(set(r['command'])<= {'until','buttons','touch','duration','stop'}for r in journal['commands_received'])
 rom=NdsImage.open(plan['candidate']);arm=rom.read_file('/__arm9__.bin');kanji=rom.read_file('/GRP/KANJI.FNT');raster,independent,meta=font_tools(rom)
 pages=read('work/analysis/market_context_pages_v2115/all18_market_native_pages.json');scoped={r['message_ID']for r in pages['cases']}
 frames={r['frame']:r for r in report['frames_captured']};prior={r['frame']:r for r in read(PRIOR)['frames_captured']};controls=[]
 for f in (31000,31400,34100,34500,34900):
  assert ImageChops.difference(Image.open(frames[f]['path']).convert('RGB'),Image.open(prior[f]['path']).convert('RGB')).getbbox()is None
  controls.append(dict(frame=f,whole_frame_byte_pixels_exact_to_verified_V2097_ordinary_prefix=True))
 for r in frames.values():assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']
 holds=[]
 for i,row in enumerate(obs['rows']):
  n=row['source_request']['ID']
  if n not in scoped:continue
  assert row['bounds']==[0,0,228,48] and row['font_input_offset']==2 and row['CPU_WRAM_DTCM_ITCM_configuration_exact']
  for s in row['snapshots'].values():assert sha(Path(s['path']).read_bytes())==s['sha256']
  matches=[p for p in pages['cases']if p['message_ID']==n and p['formatted_hex']==row['text_hex']];assert len(matches)==1 and matches[0]['page_count']==1
  end=obs['rows'][i+1]['frame']if i+1<len(obs['rows'])else report['frames']+1
  f=next(f for f in sorted(frames)if row['frame']<f<end)
  text=bytes.fromhex(row['text_hex']);events=[];plane=raster(arm,text,0x01FFCE40-0x02000000,size=(228,48),instruction_limit=2000000,glyph_events=events)
  lines=[s.strip().decode('cp932')for s in text.split(b'\n')];assert plane==independent(arm,kanji,lines) and [e['code']for e in events if e['code']!=32]==glyph_codes(text)
  photo=Image.open(frames[f]['path']).convert('RGB');expected={(16+j%228,296+j//228)for j,v in enumerate(plane)if v==1};actual={(x,y)for y in range(BODY[1],BODY[3])for x in range(BODY[0],BODY[2])if photo.getpixel((x,y))==(0,8,0)};assert expected==actual,(n,f,len(expected-actual),len(actual-expected))
  holds.append(dict(message_ID=n,font_frame=row['frame'],hold_frame=f,text_hex=row['text_hex'],lines=lines,capture=frames[f]['path'],capture_sha256=frames[f]['PNG_sha256'],exact_registered_native_template=True,every_actual_foreground_pixel_matches_full_native_independent_plane=True,all_leading_trailing_letters_bounds_and_input_bytes_complete=True))
 assert {746,747,748,763,764}.issubset({r['message_ID']for r in holds})
 snaps={r['frame']:r for r in report['read_only_pause_RAM_snapshots']};states=[]
 for f in (34900,36900,38700,40900,42700,44000,45300,45700,46500,47300,47700,48500):
  r=snaps[f];raw=Path(r['path']).read_bytes();assert sha(raw)==r['sha256'];states.append(dict(frame=f,state=state(arm,raw),snapshot=r))
 s={r['frame']:r['state']for r in states};assert s[34900]==s[36900]
 for f,cash,share,invest in((38700,38200,21,1800),(40900,2200,41,37800),(42700,400,42,39600),(44000,400,42,39600),(45700,200,42,39600),(46500,0,42,39600),(47300,0,42,39600),(47700,0,42,39600),(48500,0,42,39600)):
  assert s[f]['cash']==cash and s[f]['share']==share and s[f]['investment_accumulator']==invest
 sheet=Image.new('RGB',(256*len(holds),410),'#263238');draw=ImageDraw.Draw(sheet)
 for i,r in enumerate(holds):draw.text((i*256+4,4),f"ID{r['message_ID']} frame{r['hold_frame']}",fill='white');sheet.paste(Image.open(r['capture']).convert('RGB'),(i*256,22))
 path=ROOT/'actual_market_holds.png';sheet.save(path)
 save(ROOT/'ordinary_market_actual_verification.json',dict(candidate=plan['candidate'],candidate_sha256=plan['candidate_sha256'],frames=report['frames'],actual_holds=holds,ordinary_prefix_controls=controls,native_state_controls=states,run_plan=str(RUN/'run_plan.json'),terminal=str(RUN/'terminal.json'),capture_report=str(CAP/'capture_report.json'),source_observer=str(CAP/'common_observer/requests.json'),observer_sha256=sha((CAP/'common_observer/requests.json').read_bytes()),font_model=meta,original_donor_unchanged=True,observer_closed_original_host_slots_restored=True,existing_isolated_system_unlock_not_earned=True,no_savestate_story_location_RNG_funds_outcome_fixture=True,navigation_journal_is_not_execution_proof=True,rejected_commands_applied_no_inputs=True,no_full_playthrough_or_all_conditional_visit_or_hardware_claim=True,review_sheet=str(path),review_sheet_sha256=sha(path.read_bytes()),visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(actual_holds=len(holds),IDs=[r['message_ID']for r in holds],executed_frames=report['frames'],state_controls=len(states),prefix_controls=len(controls),sheet=str(path)))
