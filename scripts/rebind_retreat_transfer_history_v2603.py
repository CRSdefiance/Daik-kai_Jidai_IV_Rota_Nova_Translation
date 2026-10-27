"""Three complete original retreat holds and defeat/transfer/sailing transitions."""
from pathlib import Path
import struct
from PIL import Image,ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.retreat_transfer_editorial import current_entries as old_entries
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_stronger_fleet_survey_v1476 import observe
from scripts.verify_village_wrap_v608 import read,save
BASE=0x02000000;ROOT=Path('work/analysis/retreat_transfer_history_v2603');ROM=Path('out/all_routes_combined_v2284_candidate.nds');OLDROM=Path('out/all_routes_combined_v1520_candidate.nds')
if __name__=='__main__':
 assert not ROOT.exists()
 rom,oldrom=map(NdsImage.open,(ROM,OLDROM));arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');oldarm=oldrom.read_file('/__arm9__.bin');oldcommon=oldrom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm);prior=old_entries(oldcommon,oldarm);assert all(entries[n].text==prior[n].text for n in range(2683,2690))
 hp=Path('work/analysis/retreat_transfer_actual_fonts_v1526c/actual_retreat_font_and_transition_verification.json');h=read(hp);ap=Path(h['complete_original_event_audit']);audit=read(ap);rp=Path(h['report']);report=read(rp);assert sha(ap.read_bytes())==h['complete_original_event_audit_sha256']and sha(rp.read_bytes())==h['report_sha256']==audit['terminal_report_sha256']and sha(OLDROM.read_bytes())==h['candidate_sha256']==report['ROM_sha256']and report['frames']==9200 and report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
 assert audit['entire4MiB_sole_prebattle40_owned_byte_fixture_and_all_validated_input_schedule_audited']and audit['no_further_battle_or_duel_fixture_health_equipment_position_ability_actor_ID_RNG_or_result_edit']and audit['source_and_disposable_donor_unchanged']and not audit['rejected_before_any_input_or_fixture_commands']
 context=read('work/analysis/retreat_transfer_context_v2600/source_context_packet.json');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');spans=[(r['start'],r['end'])for r in context['original_source_code']]+[tuple(r)for r in audit['original_clean_code_spans']]
 for a,b in spans:assert arm[a:b]==oldarm[a:b]==clean[a:b]
 fp=read('work/analysis/retreat_transfer_fonts_v2602/native_font_proof.json');case=next(c for c in fp['cases']if c['source_voice']==1 and c['variant']==0);assert case['message_ID']==2684 and case['name']=='Latina';preview=Path(case['preview']);assert sha(preview.read_bytes())==case['preview_sha256'];plane=Image.open(preview).convert('L');assert plane.size==(228,64)
 snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']};images={r['frame']:r for r in report['frames_captured']};owner,wrapped=[struct.unpack_from('<I',arm,p)[0]for p in(0x552A0,0x54450)];block=IlnkContainer.parse(oldcommon).blocks[prior[2684].block]
 def raw(frame):
  r=snapshots[frame];data=Path(r['path']).read_bytes();assert sha(data)==r['sha256']and len(data)==0x400000;return data
 def picture(frame):
  r=images[frame];p=Path(r['path']);assert sha(p.read_bytes())==r['PNG_sha256'];return Image.open(p).convert('RGB')
 def verify(frame,data=None,screen=None):
  data=raw(frame)if data is None else data;screen=picture(frame)if screen is None else screen;cpu,get=get_machine(arm,data);fleets,actors=get(0xCB1A8),get(0xCB184);identity=get(0x82478,fleets+0x2090,1);actor=actors+4+identity*32
  assert identity==get(0x7EE08,actor)==16 and get(0x7E988,actor)==1 and get(0x53F4C,actor,0x02117080)==2684
  model=get(0x36C94,fleets+4+132+12);assert model==context['replacement_model']and model!=context['original_previous_flagship_model'];vt=struct.unpack('<I',cpu.mem_read(model,4))[0];getter=struct.unpack('<I',cpu.mem_read(vt+4,4))[0];ptr=get(getter-BASE,model);name=bytes(cpu.mem_read(ptr,64)).split(b'\0')[0];assert name==b'Latina'
  assert data[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0]==entries[2684].text==entries[2687].text
  assert data[wrapped-BASE:wrapped-BASE+512].split(b'\0')[0].hex()==case['native_pipeline']['formatted_hex']and data.count(block)==1
  expected={(16+x,296+y)for y in range(64)for x in range(228)if plane.getpixel((x,y))==0};actual={(x,y)for y in range(294,366)for x in range(16,244)if screen.getpixel((x,y))==(0,8,0)};assert actual==expected
  return dict(message_ID=2684,message_id=2684,frame=frame,source_role_selector=1,source_actor_ID=16,source_voice=1,original_voice_table=0x02117080,source_logical_accessor=0x02082478,physical_FirstMate_object=get(0x82428,fleets+0x2090,1),identical2684_2687_templates_disambiguated_by_role_voice_selection=True,replacement_name='Latina',replacement_model=model,lines=case['lines'],current_template_expanded_wrapped_bytes_and_full228x64_native_RGB_ink_and_blank_mask_equal=True,matching_foreground_pixels=len(expected),missing_or_unexpected_foreground_pixels=0,RAM=snapshots[frame]['path'],RAM_sha256=sha(data),capture=images[frame]['path'],capture_sha256=images[frame]['PNG_sha256'],historical_only_not_current_emulator_visit=True)
 holds=[verify(n)for n in(8750,8800,8850)];assert all(h['matching_foreground_pixels']==550 for h in holds)
 jp=rp.parent/'navigation_command_journal.json';journal=read(jp);schedule=read('work/analysis/retreat_transfer_replay_v1524/original_departure_inputs.json')
 for r in journal['commands_received']:
  assert r['validation_passed'];c=r['command']
  if c.get('stop'):continue
  assert c['until']in snapshots and c['until']>r['frame']
  if r['frame']>4800:assert'battle_fixture'not in c
  if c.get('buttons')or c.get('touch')is not None:
   event=dict(start=r['frame']+1,duration=c.get('duration',12),buttons=c.get('buttons',[]))
   if c.get('touch')is not None:event['touch']=c['touch']
   schedule.append(event)
 assert schedule==report['scripted_input_schedule']
 controls=[]
 def reject(action):
  try:action()
  except AssertionError:return True
  raise AssertionError('Corrupted retreat hold accepted')
 data=raw(8800);screen=picture(8800)
 for at,label in((owner+0x2030+entries[2684].text.index(b'Our'),'resident-leading-O'),(wrapped+bytes.fromhex(case['native_pipeline']['formatted_hex']).index(b'Our'),'wrapped-leading-O')):
  bad=bytearray(data);bad[at-BASE]^=1;controls.append(dict(negative=label,rejected=reject(lambda:verify(8800,data=bytes(bad)))))
 for row,col,label in((0,0,'erase-leading-O'),(1,len(case['lines'][1])-1,'erase-final-exclamation'),(1,0,'erase-Get-aboard-G'),(1,case['lines'][1].index('Latina'),'erase-complete-replacement-name-L')):
  bad=screen.copy();x,y=22+col*6,296+row*16;bad.paste('white',(x,y,x+6,y+11));controls.append(dict(negative=label,rejected=reject(lambda:verify(8800,screen=bad))))
 bad=screen.copy();bad.putpixel((16,296),(0,8,0));controls.append(dict(negative='stray-margin-ink',rejected=reject(lambda:verify(8800,screen=bad))));assert len(controls)==7
 states=[]
 for expected in audit['actual_native_observations']:
  n=expected['frame'];raw(n);state=observe(arm,snapshots[n]);assert state==expected;states.append(state)
 assert len(states)==14 and states[-1]['frame']==9200 and states[-1]['mode']==[0,0,0]and[s['Hull_Crew']for s in states[-1]['fleets'][0]['ships']]==[[25,19],[25,11],[24,6],[21,8]]
 flow=[]
 for frame,label in((8200,'preceding evacuation after original auto-duel defeat;context only'),(8400,'abandonment notice;context only'),(8600,'own flagship defeat;context only'),(8800,'replacement-ship retreat report before normal A'),(9000,'ordinary sailing after original transfer/A'),(9200,'continued sailing with four surviving ships;source mode0')):
  picture(frame);flow.append(dict(frame=frame,visually_reviewed_state=label,RAM=snapshots[frame]['path'],RAM_sha256=sha(raw(frame)),capture=images[frame]['path'],capture_sha256=images[frame]['PNG_sha256'],historical_only_not_current_startup_or_unreviewed_prose_credit=True))
 pixelpath=Path('work/analysis/retreat_transfer_actual_pixels_v1526d/all_changed_pixels_explained.json');pixelproof=read(pixelpath);assert pixelproof['actual_font_proof_sha256']==sha(hp.read_bytes())and pixelproof['remaining42_complete_frames_exact_to_V1492']and len(pixelproof['all3_whole_screen_text_changes'])==3 and all(r['whole256x384_changed_RGB_pixels']==278 and r['every_changed_pixel_exactly_the_old_new_native_glyph_symmetric_difference']for r in pixelproof['all3_whole_screen_text_changes'])
 ROOT.mkdir(parents=True);sheet=Image.new('RGB',(768,410),'#263238');draw=ImageDraw.Draw(sheet)
 for i,h in enumerate(holds):draw.text((i*256+4,3),'Historical V1520 ID2684 '+str(h['frame']),fill='white');sheet.paste(Image.open(h['capture']),(i*256,24))
 a=ROOT/'three_historical_complete_retreat_holds.png';sheet.save(a);sheet=Image.new('RGB',(768,820),'#263238');draw=ImageDraw.Draw(sheet)
 for i,r in enumerate(flow):
  x,y=i%3*256,i//3*410;draw.text((x+4,y+3),str(r['frame'])+' historical transfer context',fill='white');sheet.paste(Image.open(r['capture']),(x,y+24))
 b=ROOT/'historical_defeat_retreat_transfer_and_sailing.png';sheet.save(b)
 save(ROOT/'historical_retreat_transfer_current_binding.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),historical_candidate=str(OLDROM),historical_candidate_sha256=sha(OLDROM.read_bytes()),historical_proof=str(hp),historical_proof_sha256=sha(hp.read_bytes()),historical_report=str(rp),historical_report_sha256=sha(rp.read_bytes()),complete_event_audit=str(ap),complete_event_audit_sha256=sha(ap.read_bytes()),historical_holds=holds,historical_IDs=[2684],scoped_historical_cancellation_and_battle_transitions_freshly_rechecked=flow,seven_negative_controls_current_binding_on_offline_clones=controls,exact_historical_input_journal=str(jp),exact_historical_input_journal_sha256=sha(jp.read_bytes()),all_accepted_input_events_reconstructed_at_pause_frame_plus1=True,no_fixtures_after4800=True,source_combat_result_role_selection_and_RNG_current_historical_equal=[dict(start=a,end=b,sha256=sha(arm[a:b]))for a,b in spans],natural_combat_outcome_and_original_dismissal_states=states,original_sole40_position_byte_fixture_audit_hash_bound_not_needlessly_repeated=True,sole_fixture=audit['sole_fixture'],all7_current_historical_payloads_and_all8_voice_font_planes_equal=True,only2684_has_individual_historical_activation_other6_and_voice3_fallback_use_family_sample=True,no_new_current_battle_emulator_runs_or_family_visits=True,old_new_three_screen278_glyph_differences_and42_other_whole_frames_proof=str(pixelpath),old_new_three_screen278_glyph_differences_and42_other_whole_frames_proof_sha256=sha(pixelpath.read_bytes()),review_sheets=[dict(path=str(p),sha256=sha(p.read_bytes()))for p in(a,b)],scope='Historical V1520 original auto-duel loss/evacuation/flagship defeat/replacement-ship transfer/A dismissal and four-ship sailing return. Three full2684 RGB ink/blank masks freshly bind current native text and literal Latina name. Original logical Gerhard16/voice1 disambiguates identical2684/2687 templates;no physical-room substitution. Sole40-owned-byte prebattle position fixture,whole4MiB/input audit and existing278-glyph-difference/42-whole-frame controls remain hash-bound without unnecessary replay. No later actor,health,crew,ability,RNG,result or membership edits. Only2684 individually activated;other six and voice3 fallback use current native/offline and representative-family coverage. No new current startup/emulator run,earned travel,sinking/death,full route or hardware proof. Context messages add zero prose credit.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('Three complete historical2684 holds,7 corruptions,14 original states and6 defeat/transfer/sailing transitions pass.')
