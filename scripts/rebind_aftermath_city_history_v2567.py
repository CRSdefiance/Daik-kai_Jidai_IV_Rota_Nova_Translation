"""Two historical direct-captain city challenges and original defender battle entry."""
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
BASE=0x02000000;ROOT=Path('work/analysis/aftermath_city_history_v2567')
ROM=Path('out/all_routes_combined_v2284_candidate.nds');OLDROM=Path('out/all_routes_combined_v1266_candidate.nds')
if __name__=='__main__':
 assert not ROOT.exists()
 rom,oldrom=map(NdsImage.open,(ROM,OLDROM));arm=rom.read_file('/__arm9__.bin');oldarm=oldrom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');oldcommon=oldrom.read_file('/COMMON/MESFILE.DK4')
 entries=current_entries(common,arm);prior=old_entries(oldcommon,oldarm);assert all(entries[n].text==prior[n].text for n in range(2038,2046))
 hpath=Path('work/analysis/aftermath_city_verified_v1287/actual_city_defense_verification.json');h=read(hpath);reportpath=Path(h['report']);report=read(reportpath)
 assert sha(reportpath.read_bytes())==h['report_sha256'] and sha(OLDROM.read_bytes())==h['candidate_sha256']==report['ROM_sha256']
 assert report['frames']==6940 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
 assert h['source_and_disposable_saves_unchanged'] and h['no_diplomacy_health_actor_ID_eligibility_result_RNG_or_message_injection'] and h['original_source_event_defender_presence_share_and_unforced_one_in_three_choice']
 fixture=h['sole_fixture_full4MiB_replay_exact'];assert report['synthetic_battle_recovery_proximity_fixtures']==[{**fixture,'frame':5000}]
 assert len(fixture['owned_bytes'])==16 and len(fixture['changes'])==10 and fixture['only_own_cached_and_live_position_changed'] and fixture['diplomacy_actors_IDs_defender_defenses_shares_health_RNG_and_events_unchanged']
 spans=[tuple(r) for r in h['original_city_confirmation_defender_choice_and_RNG_code_exact_to_clean']];assert all(arm[a:b]==oldarm[a:b] for a,b in spans)
 fp=read('work/analysis/aftermath_city_fonts_v2566/native_font_proof.json');case=next(r for r in fp['cases'] if r['message_ID']==2043)
 p=Path(case['preview']);assert sha(p.read_bytes())==case['preview_sha256'];plane=Image.open(p).convert('L');assert plane.size==(228,64)
 historicalblock=IlnkContainer.parse(oldcommon).blocks[prior[2043].block]
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
  cpu,get=get_machine(arm,raw);fleet,actors=get(0xCB1A8),get(0xCB184);defender=fleet+4+22*132;actor=get(0x3697C,defender)
  assert get(0x35320,defender)==6 and actor==actors+4+46*32 and get(0x7EE08,actor)==46 and get(0x53F4C,actor,0x021178C0)==2043
  assert raw[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0]==entries[2043].text
  assert raw[wrapped-BASE:wrapped-BASE+512].split(b'\0')[0].hex()==case['native_formatted_hex'] and raw.count(historicalblock)==1
  expected={(16+x,296+y) for y in range(64) for x in range(228) if plane.getpixel((x,y))==0}
  actual={(x,y) for y in range(294,366) for x in range(16,244) if image.getpixel((x,y))==(0,8,0)}
  assert actual==expected and len(expected)==696
  return dict(message_ID=2043,message_id=2043,frame=frame,source_actor_ID=46,defender_fleet_ID=22,defender_company_ID=6,original_entry=0x02053F0C,original_parent=0x02053F40,original_table_stack_offset=0x274,original_voice_table=0x021178C0,lines=case['lines'],
   current_payload_and_formatted_bytes_and_complete228x64_current_native_font_RGB_ink_blank_mask_equal=True,missing_or_unexpected_foreground_pixels=0,matching_foreground_pixels=len(expected),historical_block_unique_and_current_selected_payload_exact=True,uniform_margins_complete_first_final_letters_words_and_bounds_pass=True,
   RAM=str(snapshots[frame]['path']),RAM_sha256=sha(raw),capture=str(picture),capture_sha256=sha(picture.read_bytes()),historical_only_not_current_emulator_visit=True)
 holds=[verify(frame) for frame in(6720,6740)]
 journalpath=reportpath.parent/'navigation_command_journal.json';journal=read(journalpath);assert all(r['validation_passed'] for r in journal['commands_received'])
 schedule=read('work/analysis/aftermath_city_v1286/original_load_inputs.json')
 for row in journal['commands_received']:
  command=row['command']
  if command.get('stop'):continue
  assert command['until'] in snapshots and command['until']>row['frame']
  if row['frame']>5000:assert 'battle_fixture' not in command
  if command.get('buttons') or command.get('touch') is not None:
   event=dict(start=row['frame']+1,duration=command.get('duration',12),buttons=command.get('buttons',[]))
   if command.get('touch') is not None:event['touch']=command['touch']
   schedule.append(event)
 assert schedule==report['scripted_input_schedule']
 controls=[]
 def rejected(action):
  try:action()
  except AssertionError:return True
  raise AssertionError('Corrupted city-defense challenge accepted')
 raw=source_raw(6720);image=Image.open(images[6720]['path']).convert('RGB');lines=case['lines']
 for at,label in((owner+0x2030+entries[2043].text.index(b'So'),'corrupt-resident-leading-S'),(wrapped+bytes.fromhex(case['native_formatted_hex']).index(b'So'),'corrupt-wrapped-leading-S')):
  bad=bytearray(raw);bad[at-BASE]^=1;controls.append(dict(negative=label,rejected=rejected(lambda:verify(6720,raw_override=bytes(bad)))))
 cells=[(0,0,'erase-complete-leading-S'),(2,len(lines[2])-1,'erase-final-exclamation'),(2,0,'erase-third-row-retaliation-y'),(1,lines[1].index('teach')+1,'erase-interior-retaliation-word-letter'),(1,lines[1].index("I'll"),'erase-complete-personal-I')]
 for line,column,label in cells:
  bad=image.copy();x,y=22+column*6,296+line*16;bad.paste('white',(x,y,x+6,y+11));controls.append(dict(negative=label,rejected=rejected(lambda:verify(6720,image_override=bad))))
 bad=image.copy();bad.putpixel((16,296),(0,8,0));controls.append(dict(negative='stray-ink-in-left-paper-margin',rejected=rejected(lambda:verify(6720,image_override=bad))))
 assert len(controls)==8 and all(r['rejected'] for r in controls)
 states=[]
 for s in h['original_mode_states']:
  raw=source_raw(s['frame']);cpu,get=get_machine(arm,raw);mode=list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)));assert mode==s['mode8_12_16'];states.append(dict(s,RAM_sha256=sha(raw)))
 assert len(states)==8 and states[-2]['mode8_12_16']==states[-1]['mode8_12_16']==[0,1,22]
 assert h['normal_A_dismissal_enters_original_defender_fleet_battle_without_extra_page'] and h['no_battle_outcome_or_town_surrender_claimed'] and h['prior_war_pilot_1283b_not_used_for_translation_completion']
 flow=[]
 for frame,label in((6740,'complete original defending-captain challenge'),(6840,'first normal A enters original defender-fleet22 battle'),(6940,'original battle continues without extra page')):
  p=Path(images[frame]['path']);assert sha(p.read_bytes())==images[frame]['PNG_sha256'];flow.append(dict(frame=frame,visually_reviewed_state=label,RAM=str(snapshots[frame]['path']),RAM_sha256=sha(source_raw(frame)),capture=str(p),capture_sha256=sha(p.read_bytes()),historical_only_not_current_startup_or_battle_outcome_approval=True))
 ROOT.mkdir(parents=True);sheet=Image.new('RGB',(512,410),'#263238');draw=ImageDraw.Draw(sheet)
 for i,r in enumerate(holds):draw.text((i*256+4,3),'Historical V1266 ID2043 frame'+str(r['frame']),fill='white');sheet.paste(Image.open(r['capture']),(i*256,24))
 a=ROOT/'two_historical_complete_city_defender_holds.png';sheet.save(a)
 sheet=Image.new('RGB',(768,410),'#263238');draw=ImageDraw.Draw(sheet)
 for i,r in enumerate(flow):draw.text((i*256+4,3),str(r['frame'])+' historical defender flow',fill='white');sheet.paste(Image.open(r['capture']),(i*256,24))
 b=ROOT/'historical_challenge_normal_A_defender_battle_entry.png';sheet.save(b)
 save(ROOT/'historical_aftermath_city_current_binding.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),historical_candidate=str(OLDROM),historical_candidate_sha256=sha(OLDROM.read_bytes()),historical_proof=str(hpath),historical_proof_sha256=sha(hpath.read_bytes()),historical_report=str(reportpath),historical_report_sha256=sha(reportpath.read_bytes()),historical_holds=holds,historical_IDs=[2043],
  scoped_historical_cancellation_and_battle_transitions_freshly_rechecked=flow,eight_negative_controls_current_binding_on_offline_clones=controls,exact_historical_input_journal=str(journalpath),exact_historical_input_journal_sha256=sha(journalpath.read_bytes()),all_accepted_input_events_reconstructed_at_pause_frame_plus1=True,
  source_city_confirmation_defender_selection_and_RNG_current_historical_equal=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],eight_original_challenge_and_battle_entry_mode_states=states,
  sole_prebattle_location_fixture_at5000_whole4MiB_audit_hash_bound_not_needlessly_repeated=True,sole_fixture_disclosure=fixture,original_presence_share_and_unforced_one_in_three_choice_preserved=True,
  all8_current_historical_payloads_and_font_planes_equal=True,only2043_has_individual_historical_activation_other7_use_family_sample=True,no_new_current_battle_emulator_runs_or_family_visits=True,older_war_pilot1283b_not_used_for_credit=True,
  review_sheets=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in(a,b)],scope='Historical V1266 Madeira original defense with captain46/fleet22/company6 and unforced one-in-three defender choice. One frame5000 location-only fixture changes10 of16 owned bytes;its full4MiB audit is bound without needless replay. Diplomacy,identity,health,defenses,shares,RNG/events and eligibility are not injected. Two complete2043 foreground/blank-paper masks bind current direct text/fonts;original A enters defender-fleet22 battle without extra page. Other seven use current offline tests and family coverage. No current startup,earned travel,combat outcome,town surrender or hardware proof. Older1283b war pilot receives no credit.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('Two complete historical defender challenges,8 corruptions,exact inputs,8 native modes and3 normal-A/battle-entry transitions pass.')
