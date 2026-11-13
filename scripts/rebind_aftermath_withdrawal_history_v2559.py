"""Two preserved town-withdrawal reports and exact normal-A sailing return."""
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
BASE=0x02000000;ROOT=Path('work/analysis/aftermath_withdrawal_history_v2559')
ROM=Path('out/all_routes_combined_v2284_candidate.nds');OLDROM=Path('out/all_routes_combined_v1266_candidate.nds')
if __name__=='__main__':
 assert not ROOT.exists()
 rom,oldrom=map(NdsImage.open,(ROM,OLDROM));arm=rom.read_file('/__arm9__.bin');oldarm=oldrom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');oldcommon=oldrom.read_file('/COMMON/MESFILE.DK4')
 entries=current_entries(common,arm);prior=old_entries(oldcommon,oldarm);assert all(entries[n].text==prior[n].text for n in range(2114,2122))
 hpath=Path('work/analysis/aftermath_withdrawal_verified_v1293/actual_withdrawal_verification.json');h=read(hpath);reportpath=Path(h['report']);report=read(reportpath)
 assert sha(reportpath.read_bytes())==h['report_sha256'] and sha(OLDROM.read_bytes())==h['candidate_sha256']==report['ROM_sha256']
 assert report['frames']==7510 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
 assert h['source_and_disposable_donors_unchanged'] and h['no_actor_ID_RNG_eligibility_battle_state_result_or_message_injection']
 fixture=h['sole_prebattle_fixture_full4MiB_replay'];assert report['synthetic_battle_recovery_proximity_fixtures']==[{**fixture,'frame':5000}]
 assert len(fixture['owned_bytes'])==18 and len(fixture['changes'])==12 and fixture['all_actor_objects_IDs_health_towns_defenses_shares_diplomacy_RNG_and_events_exact']
 spans=[tuple(r) for r in h['original_town_battle_distance_and_withdrawal_code_equal_clean']];assert all(arm[a:b]==oldarm[a:b] for a,b in spans)
 fp=read('work/analysis/aftermath_withdrawal_fonts_v2558/native_font_proof.json');case=next(r for r in fp['cases'] if r['message_ID']==2114)
 p=Path(case['preview']);assert sha(p.read_bytes())==case['preview_sha256'];plane=Image.open(p).convert('L');assert plane.size==(228,64)
 historicalblock=IlnkContainer.parse(oldcommon).blocks[prior[2114].block]
 owner,wrapped=[struct.unpack_from('<I',arm,at)[0] for at in(0x552A0,0x54450)]
 assert owner==struct.unpack_from('<I',oldarm,0x552A0)[0] and wrapped==struct.unpack_from('<I',oldarm,0x54450)[0]
 snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']};images={r['frame']:r for r in report['frames_captured']}
 def source_raw(frame):
  item=snapshots[frame];raw=Path(item['path']).read_bytes();assert len(raw)==0x400000 and sha(raw)==item['sha256'];return raw
 assert sha(source_raw(5000))==fixture['before_RAM_sha256']
 def verify(frame,raw_override=None,image_override=None):
  raw=source_raw(frame) if raw_override is None else raw_override
  item=images[frame];picture=Path(item['path']);assert sha(picture.read_bytes())==item['PNG_sha256']
  image=Image.open(picture).convert('RGB') if image_override is None else image_override.convert('RGB')
  cpu,get=get_machine(arm,raw);fleet,actors=get(0xCB1A8),get(0xCB184);duty=fleet+0x2090;identity=get(0x82478,duty,1);actor=get(0x82428,duty,1)
  assert identity==18 and actor==actors+4+18*32 and get(0x7EE08,actor)==18 and get(0x53F4C,actor,0x02117D00)==2114
  assert raw[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0]==entries[2114].text
  assert raw[wrapped-BASE:wrapped-BASE+512].split(b'\0')[0].hex()==case['native_formatted_hex'] and raw.count(historicalblock)==1
  expected={(16+x,296+y) for y in range(64) for x in range(228) if plane.getpixel((x,y))==0}
  actual={(x,y) for y in range(294,366) for x in range(16,244) if image.getpixel((x,y))==(0,8,0)}
  assert actual==expected and len(expected)==296
  return dict(message_ID=2114,message_id=2114,frame=frame,source_role_selector=1,source_actor_ID=18,assigned_original_First_Mate_actor=True,original_voice_table=0x02117D00,original_parent=0x02053DB8,lines=case['lines'],
   current_payload_and_formatted_bytes_and_complete228x64_current_native_font_RGB_ink_blank_mask_equal=True,missing_or_unexpected_foreground_pixels=0,matching_foreground_pixels=len(expected),historical_block_unique_and_current_selected_payload_exact=True,uniform_margins_complete_first_final_letters_words_and_bounds_pass=True,
   RAM=str(snapshots[frame]['path']),RAM_sha256=sha(raw),capture=str(picture),capture_sha256=sha(picture.read_bytes()),historical_only_not_current_emulator_visit=True)
 holds=[verify(frame) for frame in(7110,7310)]
 journalpath=reportpath.parent/'navigation_command_journal.json';journal=read(journalpath);assert all(r['validation_passed'] for r in journal['commands_received'])
 schedule=read('work/analysis/aftermath_town_v1291/original_load_inputs.json')
 for row in journal['commands_received']:
  command=row['command']
  if command.get('stop'):continue
  assert command['until'] in snapshots and command['until']>row['frame']
  if row['frame']>5000:assert 'battle_fixture' not in command
  if command.get('buttons') or command.get('touch') is not None:
   event=dict(start=row['frame']+1,duration=command.get('duration',12),buttons=command.get('buttons',[]))
   if command.get('touch') is not None:event['touch']=command['touch']
   schedule.append(event)
 assert schedule==report['scripted_input_schedule'] and not any(5910<=e['start']<=7310 for e in schedule)
 controls=[]
 def rejected(action):
  try:action()
  except AssertionError:return True
  raise AssertionError('Corrupted withdrawal report accepted')
 raw=source_raw(7110);image=Image.open(images[7110]['path']).convert('RGB');line=case['lines'][0]
 for at,label in((owner+0x2030+entries[2114].text.index(b'Admiral'),'corrupt-resident-leading-Admiral'),(wrapped+bytes.fromhex(case['native_formatted_hex']).index(b'Admiral'),'corrupt-wrapped-leading-Admiral')):
  bad=bytearray(raw);bad[at-BASE]^=1;controls.append(dict(negative=label,rejected=rejected(lambda:verify(7110,raw_override=bytes(bad)))))
 for column,label in((0,'erase-complete-leading-Admiral-A'),(len(line)-1,'erase-final-exclamation'),(line.index('withdrawing')+2,'erase-interior-withdrawal-word-letter')):
  bad=image.copy();x,y=22+column*6,296;bad.paste('white',(x,y,x+6,y+11));controls.append(dict(negative=label,rejected=rejected(lambda:verify(7110,image_override=bad))))
 bad=image.copy();bad.putpixel((16,296),(0,8,0));controls.append(dict(negative='stray-ink-in-left-paper-margin',rejected=rejected(lambda:verify(7110,image_override=bad))))
 assert len(controls)==6 and all(r['rejected'] for r in controls)
 states=[];context=read('work/analysis/aftermath_withdrawal_context_v2554/source_context_packet.json');distances={r['frame']:r for r in context['current_original513D0_on9_historical_town_ship_positions']}
 for s in h['original_town_battle_movement_withdrawal_and_return_states']:
  raw=source_raw(s['frame']);assert sha(raw)==s['RAM_sha256'];cpu,get=get_machine(arm,raw);fleet,world,towns=get(0xCB1A8),get(0xCB19C),get(0xCB178)
  town=towns+4+73*108;mobile=get(0x36C70,fleet+4+132+12)
  assert list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))==s['mode8_12_16']
  assert struct.unpack('<I',cpu.mem_read(world+0x1360,4))[0]==s['town_battle_ID']
  assert [get(0x5543C,mobile),get(0x55444,mobile)]==s['own_live_Hull_Crew'] and get(0xB3FD4,town,1)==s['town_defenses']==100
  get(0x36A24,0x02470010,mobile);vt=struct.unpack('<I',cpu.mem_read(town,4))[0];get(struct.unpack('<I',cpu.mem_read(vt+0x20,4))[0]-BASE,0x02470000,town)
  assert list(struct.unpack('<2i',cpu.mem_read(0x02470000,8)))==s['native_town_center'] and list(struct.unpack('<2i',cpu.mem_read(0x02470010,8)))==s['own_live_map_point']
  assert get(0x513D0,0x02470000,0x02470010,0)==s['original513D0_distance_result']==distances[s['frame']]['current_original513D0_result']
  states.append(s)
 assert len(states)==9 and h['normal_A_dismissal_clears_battle_and_town_ID_and_returns_to_ordinary_sailing']
 flow=[]
 for frame,label in((7310,'original withdrawal report at distance2'),(7410,'first normal A return clears battle and town ID'),(7510,'ordinary sailing continues without an extra page')):
  p=Path(images[frame]['path']);assert sha(p.read_bytes())==images[frame]['PNG_sha256'];flow.append(dict(frame=frame,visually_reviewed_state=label,RAM=str(snapshots[frame]['path']),RAM_sha256=sha(source_raw(frame)),capture=str(p),capture_sha256=sha(p.read_bytes()),historical_only_not_current_startup_or_whole_route_approval=True))
 assert all(s['mode8_12_16']==[0,0,0] and s['town_battle_ID']==115 for s in states if s['frame'] in(7410,7510))
 ROOT.mkdir(parents=True);sheet=Image.new('RGB',(512,410),'#263238');draw=ImageDraw.Draw(sheet)
 for i,r in enumerate(holds):draw.text((i*256+4,3),'Historical V1266 ID2114 frame'+str(r['frame']),fill='white');sheet.paste(Image.open(r['capture']),(i*256,24))
 a=ROOT/'two_historical_complete_withdrawal_holds.png';sheet.save(a)
 sheet=Image.new('RGB',(768,410),'#263238');draw=ImageDraw.Draw(sheet)
 for i,r in enumerate(flow):draw.text((i*256+4,3),str(r['frame'])+' historical withdrawal flow',fill='white');sheet.paste(Image.open(r['capture']),(i*256,24))
 b=ROOT/'historical_withdrawal_normal_A_and_sailing_return.png';sheet.save(b)
 save(ROOT/'historical_aftermath_withdrawal_current_binding.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),historical_candidate=str(OLDROM),historical_candidate_sha256=sha(OLDROM.read_bytes()),historical_proof=str(hpath),historical_proof_sha256=sha(hpath.read_bytes()),historical_report=str(reportpath),historical_report_sha256=sha(reportpath.read_bytes()),historical_holds=holds,historical_IDs=[2114],
  scoped_historical_cancellation_and_battle_transitions_freshly_rechecked=flow,six_negative_controls_current_binding_on_offline_clones=controls,exact_historical_input_journal=str(journalpath),exact_historical_input_journal_sha256=sha(journalpath.read_bytes()),all_accepted_input_events_reconstructed_at_pause_frame_plus1=True,no_inputs_or_fixtures5910_through7310=True,
  source_town_battle_distance_withdrawal_and_duty_code_current_historical_equal=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],nine_original_town_movement_withdrawal_and_return_states=states,
  sole_prebattle_fixture_at5000_whole4MiB_audit_hash_bound_not_needlessly_repeated=True,sole_fixture_disclosure=fixture,all8_current_historical_payloads_and_font_planes_equal=True,only2114_has_individual_historical_activation_other7_use_family_sample=True,no_new_current_battle_emulator_runs_or_family_visits=True,
  review_sheets=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in(a,b)],scope='Historical V1266 town attack and original distance withdrawal at Sao Tome73 with assigned Charles18. A sole frame5000 fixture changes12 of18 owned bytes for location and existing First Mate assignment;all other4MiB bytes,identity,health,towns,defenses,shares,diplomacy,RNG/events are exact. No later fixture,forced battle state,message or outcome. Two complete2114 ink/blank masks bind current text/fonts;source distance0/1/2,natural Hull/Crew60/39 to59/33,defenses100 and normal A clearing battle/town IDs are freshly checked. Other seven have current offline checks and family-sample coverage. No earned travel/assignment,current startup or hardware proof.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('Two complete historical withdrawal holds,6 corruption controls,exact inputs,9 native states and3 normal-A/sailing transitions pass.')
