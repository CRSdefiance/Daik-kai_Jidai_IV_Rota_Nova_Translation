"""Two historical V1266 complete reports and original return to ordinary sailing."""
from pathlib import Path
import struct
from PIL import Image,ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.battle_aftermath_editorial import current_entries as old_entries
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
BASE=0x02000000;ROOT=Path('work/analysis/aftermath_fled_history_v2543')
ROM=Path('out/all_routes_combined_v2284_candidate.nds');OLDROM=Path('out/all_routes_combined_v1266_candidate.nds')
if __name__=='__main__':
 assert not ROOT.exists()
 rom,oldrom=map(NdsImage.open,(ROM,OLDROM));arm=rom.read_file('/__arm9__.bin');oldarm=oldrom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');oldcommon=oldrom.read_file('/COMMON/MESFILE.DK4')
 entries=current_entries(common,arm);prior=old_entries(oldcommon,oldarm);assert all(entries[n].text==prior[n].text for n in range(2046,2052))
 hpath=Path('work/analysis/aftermath_victory_verified_v1271/actual_fled_victory_verification.json');historical=read(hpath);reportpath=Path(historical['report']);report=read(reportpath)
 assert sha(reportpath.read_bytes())==historical['report_sha256']and sha(OLDROM.read_bytes())==historical['candidate_sha256']==report['ROM_sha256']
 assert report['frames']==11782 and report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
 assert historical['source_and_disposable_saves_unchanged']and len(historical['all31_fixture_replays'])==31 and historical['all_fixtures_before_duel5772_last5770']and historical['no_during_or_post_duel_fixtures']
 assert historical['no_actor_ID_numeric_message_RNG_eligibility_flag_or_result_injection']
 spans=[tuple(r)for r in historical['source_fled_result_code_matches_clean_Japanese_ARM9']];assert all(arm[a:b]==oldarm[a:b]for a,b in spans)
 fp=read('work/analysis/aftermath_fled_fonts_v2542b/native_font_proof.json');case=next(r for r in fp['cases']if r['message_ID']==2046)
 preview=Path(case['preview']);assert sha(preview.read_bytes())==case['preview_sha256'];plane=Image.open(preview).convert('L');assert plane.size==(228,64)
 historicalblock=IlnkContainer.parse(oldcommon).blocks[prior[2046].block]
 owner,wrapped=[struct.unpack_from('<I',arm,at)[0]for at in(0x552A0,0x54450)]
 assert owner==struct.unpack_from('<I',oldarm,0x552A0)[0]and wrapped==struct.unpack_from('<I',oldarm,0x54450)[0]
 snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']};images={r['frame']:r for r in report['frames_captured']}
 def source_raw(frame):
  item=snapshots[frame];raw=Path(item['path']).read_bytes();assert len(raw)==0x400000 and sha(raw)==item['sha256'];return raw
 def verify(frame,raw_override=None,image_override=None):
  raw=source_raw(frame)if raw_override is None else raw_override
  item=images[frame];picture=Path(item['path']);assert sha(picture.read_bytes())==item['PNG_sha256']
  image=Image.open(picture).convert('RGB')if image_override is None else image_override.convert('RGB')
  cpu,get=get_machine(arm,raw);fleet,actors=get(0xCB1A8),get(0xCB184);identity=get(0x82478,fleet+0x2090,1)
  actor=actors+0x19E4 if identity==get(0x7F244)else actors+4+identity*32
  assert identity==18 and get(0x7EE08,actor)==18 and get(0x53F4C,actor,0x02117900)==2046
  assert raw[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0]==entries[2046].text
  assert raw[wrapped-BASE:wrapped-BASE+512].split(b'\0')[0].hex()==case['native_formatted_hex']
  assert raw.count(historicalblock)==1
  expected={(16+x,296+y)for y in range(64)for x in range(228)if plane.getpixel((x,y))==0}
  actual={(x,y)for y in range(294,366)for x in range(16,244)if image.getpixel((x,y))==(0,8,0)}
  assert actual==expected
  return dict(message_ID=2046,message_id=2046,frame=frame,source_role_selector=1,source_actor_ID=18,original_voice_table=0x02117900,lines=case['lines'],
   current_payload_and_formatted_bytes_and_complete228x64_current_native_font_RGB_ink_blank_mask_equal=True,missing_or_unexpected_foreground_pixels=0,matching_foreground_pixels=len(expected),
   historical_block_unique_and_current_selected_payload_exact=True,uniform_margins_complete_first_final_letters_words_and_bounds_pass=True,
   RAM=str(snapshots[frame]['path']),RAM_sha256=sha(raw),capture=str(picture),capture_sha256=sha(picture.read_bytes()),historical_only_not_current_emulator_visit=True)
 holds=[verify(frame)for frame in(10942,10982)]
 journalpath=reportpath.parent/'navigation_command_journal.json';journal=read(journalpath);assert all(r['validation_passed']for r in journal['commands_received'])
 schedule=read('work/analysis/aftermath_victory_v1270/original_load_inputs.json')
 for row in journal['commands_received']:
  command=row['command']
  if command.get('stop'):continue
  assert command['until']in snapshots and command['until']>row['frame']
  if row['frame']>=5772:assert'battle_fixture'not in command
  if command.get('buttons')or command.get('touch')is not None:
   event=dict(start=row['frame']+1,duration=command.get('duration',12),buttons=command.get('buttons',[]))
   if command.get('touch')is not None:event['touch']=command['touch']
   schedule.append(event)
 assert schedule==report['scripted_input_schedule']and not any(5773<=e['start']<=10982 for e in schedule)
 controls=[]
 def rejected(action):
  try:action()
  except AssertionError:return True
  raise AssertionError('Corrupted flee/victory report accepted')
 raw=source_raw(10942);image=Image.open(holds[0]['capture']).convert('RGB')
 for at,label in((owner+0x2030+entries[2046].text.index(b'The'),'corrupt-resident-leading-T'),(wrapped+bytes.fromhex(case['native_formatted_hex']).index(b'The'),'corrupt-wrapped-leading-T')):
  bad=bytearray(raw);bad[at-BASE]^=1;controls.append(dict(negative=label,rejected=rejected(lambda:verify(10942,raw_override=bytes(bad)))))
 line=case['lines'][0]
 for column,label in((0,'erase-complete-leading-T'),(len(line)-1,'erase-final-exclamation'),(line.index('won')+1,'erase-interior-victory-word-letter')):
  bad=image.copy();x,y=22+column*6,296;bad.paste('white',(x,y,x+6,y+11));controls.append(dict(negative=label,rejected=rejected(lambda:verify(10942,image_override=bad))))
 bad=image.copy();bad.putpixel((16,296),(0,8,0));controls.append(dict(negative='stray-ink-in-left-paper-margin',rejected=rejected(lambda:verify(10942,image_override=bad))))
 assert len(controls)==6 and all(r['rejected']for r in controls)
 states=[]
 for state in historical['original_natural_combat_outcome_and_dismissal_states']:
  data=source_raw(state['frame']);assert sha(data)==state['RAM_sha256'];cpu,get=get_machine(arm,data);actors=get(0xCB184)
  assert[get(0x7E19C,p)for p in(actors+0x19E4,actors+4+32*32)]==state['own_enemy_HP']
  assert list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))==state['original_battle_mode_fields8_12_16'];states.append(state)
 assert [r['frame']for r in states]==[5782,8622,10982,11782]and states[-1]['original_battle_mode_fields8_12_16']==[0,0,0]
 assert historical['normal_A_dismissal_returns_to_source_mode0_and_ordinary_sailing_without_extra_page']
 flow=[]
 for frame,label in((10982,'complete original flight/victory report before normal A dismissal'),(11782,'ordinary sailing after original A dismissal;source mode0,no extra page')):
  picture=Path(images[frame]['path']);assert sha(picture.read_bytes())==images[frame]['PNG_sha256'];flow.append(dict(frame=frame,visually_reviewed_state=label,RAM=str(snapshots[frame]['path']),RAM_sha256=sha(source_raw(frame)),capture=str(picture),capture_sha256=sha(picture.read_bytes()),historical_only_not_current_startup_or_whole_route_approval=True))
 reference=Path(historical['final_whole_screen_exact_to_prior_original_return']);assert sha(reference.read_bytes())==historical['reference_sha256']and Image.open(flow[-1]['capture']).tobytes()==Image.open(reference).tobytes()
 ROOT.mkdir(parents=True);sheet=Image.new('RGB',(512,410),'#263238');draw=ImageDraw.Draw(sheet)
 for i,r in enumerate(holds):draw.text((i*256+4,3),'Historical V1266 ID2046 frame'+str(r['frame']),fill='white');sheet.paste(Image.open(r['capture']),(i*256,24))
 a=ROOT/'two_historical_complete_flight_victory_holds.png';sheet.save(a)
 sheet=Image.new('RGB',(512,410),'#263238');draw=ImageDraw.Draw(sheet)
 for i,r in enumerate(flow):draw.text((i*256+4,3),str(r['frame'])+' historical return',fill='white');sheet.paste(Image.open(r['capture']),(i*256,24))
 b=ROOT/'historical_report_to_ordinary_sailing_return.png';sheet.save(b)
 save(ROOT/'historical_aftermath_fled_current_binding.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),historical_candidate=str(OLDROM),historical_candidate_sha256=sha(OLDROM.read_bytes()),
  historical_proof=str(hpath),historical_proof_sha256=sha(hpath.read_bytes()),historical_report=str(reportpath),historical_report_sha256=sha(reportpath.read_bytes()),historical_holds=holds,historical_IDs=[2046],
  scoped_historical_cancellation_and_battle_transitions_freshly_rechecked=flow,six_negative_controls_current_binding_on_offline_clones=controls,
  exact_historical_input_journal=str(journalpath),exact_historical_input_journal_sha256=sha(journalpath.read_bytes()),all_accepted_input_events_reconstructed_at_pause_frame_plus1=True,no_inputs5773_through10982=True,
  source_combat_result_role_selection_and_RNG_current_historical_equal=[dict(start=a,end=b,sha256=sha(arm[a:b]))for a,b in spans],
  natural_combat_outcome_and_original_dismissal_states=states,original31_pre_duel_fixture_audits_hash_bound_not_needlessly_repeated=True,
  all6_current_historical_payloads_and_font_planes_equal=True,only2046_has_individual_historical_activation_other5_use_family_sample=True,no_new_current_battle_emulator_runs_or_family_visits=True,
  review_sheets=[dict(path=str(p),sha256=sha(p.read_bytes()))for p in(a,b)],
  scope='Historical V1266 original role1 fallbackCharles18 flight/victory after natural duel victory,with31 disclosed health/contact/attribute/equipment fixtures before duel5772,last5770. No during/post-duel fixtures or actorID,message,RNG,result injection. Two whole report ink/blank-paper masks bind current text/fonts;ordinary A returns to original mode0 and sailing without extra page. Other five are offline/current-font and family-sample coverage,not individual visits. No current startup,earned progression or hardware proof.',
  producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('Two complete historical flight/victory holds,6 corruptions,exact inputs and original A return to mode0/sailing pass.')
