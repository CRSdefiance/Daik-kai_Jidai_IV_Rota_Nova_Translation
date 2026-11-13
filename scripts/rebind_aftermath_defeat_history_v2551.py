"""Four historical original paired reports and original defeat/Game Over/title."""
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
BASE=0x02000000;ROOT=Path('work/analysis/aftermath_defeat_history_v2551')
ROM=Path('out/all_routes_combined_v2284_candidate.nds');OLDROM=Path('out/all_routes_combined_v1266_candidate.nds');IDS=[*range(2016,2022),*range(2138,2146)]
if __name__=='__main__':
 assert not ROOT.exists()
 rom,oldrom=map(NdsImage.open,(ROM,OLDROM));arm=rom.read_file('/__arm9__.bin');oldarm=oldrom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');oldcommon=oldrom.read_file('/COMMON/MESFILE.DK4')
 entries=current_entries(common,arm);prior=old_entries(oldcommon,oldarm);assert all(entries[n].text==prior[n].text for n in IDS)
 hpath=Path('work/analysis/aftermath_defeat_verified_v1276/actual_abandonment_and_flagship_defeat.json');historical=read(hpath);reportpath=Path(historical['report']);report=read(reportpath)
 assert sha(reportpath.read_bytes())==historical['report_sha256']and sha(OLDROM.read_bytes())==historical['candidate_sha256']==report['ROM_sha256']
 assert report['frames']==7802 and report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
 assert historical['source_and_disposable_saves_unchanged']and len(historical['all31_fixture_replays'])==31 and historical['last_fixture5770_before_duel5772']and historical['no_during_or_post_combat_health_ability_equipment_location_or_result_changes']
 auditpath=Path(historical['effective_fixture_and_input_audit']);assert sha(auditpath.read_bytes())==historical['effective_fixture_and_input_audit_sha256']
 spans=((0xE8CC,0x11000),(0xD458,0xD540),(0x717F8,0x718D4),(0x72368,0x723C4),(0x7DF58,0x7E1A4),(0x7E750,0x7E788),(0x7E944,0x7E950),(0x519D4,0x51A28),(0xD9824,0xD9868))
 assert all(arm[a:b]==oldarm[a:b]for a,b in spans)
 fp=read('work/analysis/aftermath_defeat_fonts_v2550/native_font_proof.json');cases={r['message_ID']:r for r in fp['cases']};planes={}
 for n in(2016,2138):
  p=Path(cases[n]['preview']);assert sha(p.read_bytes())==cases[n]['preview_sha256'];planes[n]=Image.open(p).convert('L');assert planes[n].size==(228,64)
 historicalblocks=IlnkContainer.parse(oldcommon).blocks
 owner,wrapped=[struct.unpack_from('<I',arm,at)[0]for at in(0x552A0,0x54450)]
 assert owner==struct.unpack_from('<I',oldarm,0x552A0)[0]and wrapped==struct.unpack_from('<I',oldarm,0x54450)[0]
 snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']};images={r['frame']:r for r in report['frames_captured']}
 def source_raw(frame):
  item=snapshots[frame];raw=Path(item['path']).read_bytes();assert len(raw)==0x400000 and sha(raw)==item['sha256'];return raw
 def verify(n,frame,raw_override=None,image_override=None):
  raw=source_raw(frame)if raw_override is None else raw_override
  item=images[frame];picture=Path(item['path']);assert sha(picture.read_bytes())==item['PNG_sha256']
  image=Image.open(picture).convert('RGB')if image_override is None else image_override.convert('RGB')
  cpu,get=get_machine(arm,raw);fleet,actors=get(0xCB1A8),get(0xCB184);identity=get(0x82478,fleet+0x2090,1)
  actor=actors+0x19E4 if identity==get(0x7F244)else actors+4+identity*32;table=0x02117760 if n==2016 else0x02117F00
  assert identity==18 and get(0x7EE08,actor)==18 and get(0x53F4C,actor,table)==n
  assert raw[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0]==entries[n].text
  assert raw[wrapped-BASE:wrapped-BASE+512].split(b'\0')[0].hex()==cases[n]['native_formatted_hex']
  assert raw.count(historicalblocks[prior[n].block])==1
  expected={(16+x,296+y)for y in range(64)for x in range(228)if planes[n].getpixel((x,y))==0}
  actual={(x,y)for y in range(294,366)for x in range(16,244)if image.getpixel((x,y))==(0,8,0)}
  assert actual==expected
  return dict(message_ID=n,message_id=n,frame=frame,source_role_selector=1,source_actor_ID=18,original_voice_table=table,lines=cases[n]['lines'],
   current_payload_and_formatted_bytes_and_complete228x64_current_native_font_RGB_ink_blank_mask_equal=True,missing_or_unexpected_foreground_pixels=0,matching_foreground_pixels=len(expected),historical_block_unique_and_current_selected_payload_exact=True,uniform_margins_complete_first_final_letters_words_and_bounds_pass=True,
   RAM=str(snapshots[frame]['path']),RAM_sha256=sha(raw),capture=str(picture),capture_sha256=sha(picture.read_bytes()),historical_only_not_current_emulator_visit=True)
 holds=[verify(n,frame)for n,frames in((2016,(7042,7052)),(2138,(7162,7172)))for frame in frames]
 journalpath=reportpath.parent/'navigation_command_journal.json';journal=read(journalpath);assert all(r['validation_passed']for r in journal['commands_received'])
 schedule=read('work/analysis/aftermath_defeat_v1275/original_load_inputs.json')
 for row in journal['commands_received']:
  command=row['command']
  if command.get('stop'):continue
  assert command['until']in snapshots and command['until']>row['frame']
  if row['frame']>=5772:assert'battle_fixture'not in command
  if command.get('buttons')or command.get('touch')is not None:
   event=dict(start=row['frame']+1,duration=command.get('duration',12),buttons=command.get('buttons',[]))
   if command.get('touch')is not None:event['touch']=command['touch']
   schedule.append(event)
 assert schedule==report['scripted_input_schedule']and not any(5773<=e['start']<=6922 for e in schedule)
 controls=[]
 def rejected(action):
  try:action()
  except AssertionError:return True
  raise AssertionError('Corrupted paired defeat report accepted')
 for n,frame in((2016,7042),(2138,7162)):
  raw=source_raw(frame);image=Image.open(images[frame]['path']).convert('RGB');lines=cases[n]['lines'];first=lines[0].split()[0].encode()
  for at,label in((owner+0x2030+entries[n].text.index(first),'corrupt-resident-leading-letter'),(wrapped+bytes.fromhex(cases[n]['native_formatted_hex']).index(first),'corrupt-wrapped-leading-letter')):
   bad=bytearray(raw);bad[at-BASE]^=1;controls.append(dict(message_ID=n,negative=label,rejected=rejected(lambda:verify(n,frame,raw_override=bytes(bad)))))
  cells=[(0,0,'erase-complete-leading-letter'),(len(lines)-1,len(lines[-1])-1,'erase-final-exclamation'),(0,lines[0].index('killed')+1 if n==2016 else lines[0].index('flagship')+1,'erase-interior-key-word-letter'),(1,0,'erase-evacuation-continuation-G')if n==2016 else(0,lines[0].index("We've"),'erase-defeat-announcement-W')]
  for line,column,label in cells:
   bad=image.copy();x,y=22+column*6,296+line*16;bad.paste('white',(x,y,x+6,y+11));controls.append(dict(message_ID=n,negative=label,rejected=rejected(lambda:verify(n,frame,image_override=bad))))
  bad=image.copy();bad.putpixel((16,296),(0,8,0));controls.append(dict(message_ID=n,negative='stray-ink-in-left-paper-margin',rejected=rejected(lambda:verify(n,frame,image_override=bad))))
 assert len(controls)==14 and all(r['rejected']for r in controls)
 states=[]
 for state in historical['original_natural_HP_evolution']:
  data=source_raw(state['frame']);assert sha(data)==state['RAM_sha256'];cpu,get=get_machine(arm,data);actors=get(0xCB184)
  assert[get(0x7E19C,p)for p in(actors+0x19E4,actors+4+32*32)]==state['own_enemy_HP'];states.append(state)
 preserved=[]
 for hold in historical['complete_actual_holds']:
  if hold['message_ID']==1973:
   assert sha(source_raw(hold['frame']))==hold['RAM_sha256']and sha(Path(hold['capture']).read_bytes())==hold['capture_sha256'];preserved.append(hold)
 flow=[]
 for frame,label in((7042,'original crew-abandonment report'),(7162,'original following flagship-loss report'),(7382,'original Game Over after normal A'),(7802,'original title return')):
  p=Path(images[frame]['path']);assert sha(p.read_bytes())==images[frame]['PNG_sha256'];flow.append(dict(frame=frame,visually_reviewed_state=label,RAM=str(snapshots[frame]['path']),RAM_sha256=sha(source_raw(frame)),capture=str(p),capture_sha256=sha(p.read_bytes()),historical_only_not_current_startup_or_whole_route_approval=True))
 reference=Path(historical['final_title_whole_screen_exact_to_prior_original_return']);assert sha(reference.read_bytes())==historical['reference_sha256']and Image.open(flow[-1]['capture']).tobytes()==Image.open(reference).tobytes()
 ROOT.mkdir(parents=True);sheet=Image.new('RGB',(512,820),'#263238');draw=ImageDraw.Draw(sheet)
 for i,r in enumerate(holds):
  x,y=i//2*256,i%2*410;draw.text((x+4,y+3),'Historical V1266 ID'+str(r['message_ID'])+' frame'+str(r['frame']),fill='white');sheet.paste(Image.open(r['capture']),(x,y+24))
 a=ROOT/'four_historical_complete_abandonment_loss_holds.png';sheet.save(a)
 sheet=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(sheet)
 for i,r in enumerate(flow):draw.text((i*256+4,3),str(r['frame'])+' historical defeat flow',fill='white');sheet.paste(Image.open(r['capture']),(i*256,24))
 b=ROOT/'historical_abandonment_loss_GameOver_title.png';sheet.save(b)
 save(ROOT/'historical_aftermath_defeat_current_binding.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),historical_candidate=str(OLDROM),historical_candidate_sha256=sha(OLDROM.read_bytes()),historical_proof=str(hpath),historical_proof_sha256=sha(hpath.read_bytes()),historical_report=str(reportpath),historical_report_sha256=sha(reportpath.read_bytes()),historical_holds=holds,historical_IDs=[2016,2138],
  scoped_historical_cancellation_and_battle_transitions_freshly_rechecked=flow,fourteen_negative_controls_current_binding_on_offline_clones=controls,exact_historical_input_journal=str(journalpath),exact_historical_input_journal_sha256=sha(journalpath.read_bytes()),all_accepted_input_events_reconstructed_at_pause_frame_plus1=True,no_inputs5773_through6922=True,
  source_combat_paired_result_role_selection_and_RNG_current_historical_equal=[dict(start=a,end=b,sha256=sha(arm[a:b]))for a,b in spans],natural_combat_HP_states=states,original31_pre_duel_fixture_audits_hash_bound_not_needlessly_repeated=True,effective_original_fixture_input_audit=str(auditpath),effective_original_fixture_input_audit_sha256=sha(auditpath.read_bytes()),
  all14_current_historical_payloads_and_font_planes_equal=True,only2016_and2138_have_individual_historical_activation_other12_use_family_sample=True,no_new_current_battle_emulator_runs_or_family_visits=True,preserved1973_escape_holds_context_only_no_duplicate_credit=preserved,
  review_sheets=[dict(path=str(p),sha256=sha(p.read_bytes()))for p in(a,b)],scope='Historical V1266 original Charles18 role1 abandonment then flagship loss after natural duel defeat.31 health/contact/attribute/equipment prerequisites precede duel5772,last5770;none during/post combat. Four whole-report ink/blank-paper masks bind current text/fonts. Native positive startingHP31 and shield inventory are disclosed testing prerequisites,not earned state. Exact accepted input schedule leads via normal A to loss,Game Over and title;two old1973 holds are preserved context only. Other12 use current offline checks and representative family coverage. No current startup,earned progression or hardware proof.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('Four historical paired reports,14 corruption controls,exact inputs,natural HP and original loss/Game Over/title flow pass.')
