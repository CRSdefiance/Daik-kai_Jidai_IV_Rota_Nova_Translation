"""Current binding of four spoken holds,four literal boxes and both Inspect returns."""
from pathlib import Path
import struct
from PIL import Image,ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.inspection_status_editorial import current_entries as old_entries
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/sea_inspection_history_v2616');BASE=0x02000000;ROM=Path('out/all_routes_combined_v2284_candidate.nds');OLDROM=Path('out/all_routes_combined_v1578_candidate.nds')
if __name__=='__main__':
 assert not ROOT.exists()
 rom,oldrom=map(NdsImage.open,(ROM,OLDROM));arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');oldarm=oldrom.read_file('/__arm9__.bin');oldcommon=oldrom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm);prior=old_entries(oldcommon,oldarm);assert all(entries[n].text==prior[n].text for n in[306,307,*range(2209,2217)])
 hp=Path('work/analysis/inspection_status_actual_verified_v1583/both_original_status_paths_native_RGB_and_transitions.json');historical=read(hp);assert sha(OLDROM.read_bytes())==historical['candidate_sha256']and historical['entire4MiB_fixtures_input_primary_RAM_PNG_and_unchanged_donor_audits_pass']and historical['both_source_original_statuses_observed_without_message_injection']and historical['both_normal_Inspect_returns_proven'];context=read('work/analysis/sea_inspection_context_v2612/source_context_packet.json')
 for r in context['original_source_code']:assert sha(arm[r['start']:r['end']])==r['sha256']and arm[r['start']:r['end']]==oldarm[r['start']:r['end']]
 for r in context['status_source_spans']:assert sha(arm[r['start']:r['end']])==r['current_sha256']and arm[r['start']:r['end']]==oldarm[r['start']:r['end']]
 sea=read('work/analysis/sea_responses_fonts_v2614/native_font_proof.json');status=read('work/analysis/inspection_status_fonts_v2615/native_font_proof.json');cases={2209:next(c for c in sea['cases']if c['message_ID']==2209),**{c['message_ID']:c for c in status['cases']}};planes={}
 for n,c in cases.items():
  p=Path(c['preview']);assert sha(p.read_bytes())==c['preview_sha256'];planes[n]=Image.open(p).convert('L');assert planes[n].size==(228,64)
 runs={};journals=[];states=[]
 for path in historical['paths']:
  number=path['message_ID'];audit=path['audit'];rp=Path(audit['terminal_report']);report=read(rp);assert sha(rp.read_bytes())==audit['terminal_report_sha256']and report['ROM_sha256']==historical['candidate_sha256']and report['frames']==path['terminal_frame']and report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
  assert audit['complete_primary_RAM_and_PNG_hash_audits']and audit['source_and_disposable_donor_unchanged']and audit['no_further_battle_or_duel_fixture_health_equipment_position_ability_actor_ID_RNG_or_result_edit'];fixture=audit['sole_fixture'];assert len(fixture['owned_bytes'])==(48 if number==306 else 46)and fixture['all_other4MiB_bytes_exact']and fixture['no_RNG_value_or_combat_outcome_forced']and fixture['no_message_ID_renderer_target_type_actor_identity_or_result_injected']
  snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']};images={r['frame']:r for r in report['frames_captured']};journalpath=rp.parent/'navigation_command_journal.json';journal=read(journalpath);plan=read(audit['run_plan']);schedule=read(plan['original_load_inputs'])
  for r in journal['commands_received']:
   assert r['validation_passed'];c=r['command']
   if c.get('stop'):continue
   assert c['until']in snapshots and c['until']>r['frame']
   if r['frame']>4800:assert'battle_fixture'not in c
   if c.get('buttons')or c.get('touch')is not None:
    event=dict(start=r['frame']+1,duration=c.get('duration',12),buttons=c.get('buttons',[]))
    if c.get('touch')is not None:event['touch']=c['touch']
    schedule.append(event)
  assert schedule==report['scripted_input_schedule'];journals.append(dict(status_path=number,path=str(journalpath),sha256=sha(journalpath.read_bytes()),all_events_reconstructed_at_pause_frame_plus1=True))
  runs[number]=dict(path=path,report=report,report_path=str(rp),report_sha256=sha(rp.read_bytes()),snapshots=snapshots,images=images)
 def raw(run,frame):
  r=runs[run]['snapshots'][frame];data=Path(r['path']).read_bytes();assert sha(data)==r['sha256']and len(data)==0x400000;return data
 def picture(run,frame):
  r=runs[run]['images'][frame];p=Path(r['path']);assert sha(p.read_bytes())==r['PNG_sha256'];return Image.open(p).convert('RGB')
 owner=struct.unpack_from('<I',arm,0x552A0)[0]
 def verify(n,run,frame,data=None,screen=None):
  data=raw(run,frame)if data is None else data;screen=picture(run,frame)if screen is None else screen;cpu,get=get_machine(arm,data);duty=get(0xCB1A8)+0x2090;slot3=get(0x82BC4,duty,3);slot9=get(0x82BC4,duty,9);logical=get(0x82478,duty,7)
  assert logical==18 and(slot3,slot9)==((18,208)if run==306 else(208,18));actor=get(0xCB184)+4+logical*32;assert get(0x7E988,actor)==0
  if n==2209:assert run==306 and get(0x53F4C,actor,0x021186E0)==2209
  wrapped=struct.unpack_from('<I',arm,0x54450 if n==2209 else 0x54894)[0];assert data[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0]==entries[n].text and data[wrapped-BASE:wrapped-BASE+512].split(b'\0')[0].hex()==cases[n]['native_pipeline']['formatted_hex']
  block=IlnkContainer.parse(oldcommon).blocks[prior[n].block];assert data.count(block)==1
  plane=planes[n];expected={(16+x,296+y)for y in range(64)for x in range(228)if plane.getpixel((x,y))==0};actual={(x,y)for y in range(294,366)for x in range(16,244)if screen.getpixel((x,y))==(0,8,0)};assert expected==actual
  return dict(message_ID=n,message_id=n,status_path=run,frame=frame,source_actor_ID=18 if n==2209 else None,source_role=7 if n==2209 else None,source_voice=0 if n==2209 else None,lookout_slot3=slot3,Charles_slot9=slot9,logical_role7_fallback_ID=logical,fallback_not_confused_with_lookout_assignment=True,display_origin_x=6 if n==2209 else 0,lines=cases[n].get('lines',[entries[n].text.decode('ascii')]),current_template_formatted_bytes_complete_native_RGB_ink_and_blank_mask_exact=True,matching_foreground_pixels=len(expected),missing_or_unexpected_foreground_pixels=0,RAM=runs[run]['snapshots'][frame]['path'],RAM_sha256=sha(data),capture=runs[run]['images'][frame]['path'],capture_sha256=runs[run]['images'][frame]['PNG_sha256'],historical_only_not_current_emulator_visit=True)
 sea_holds=[verify(2209,306,n)for n in(5800,5830,5900,5930)];status_holds=[verify(n,n,f)for n,frames in((306,(6040,6100)),(307,(6600,6630)))for f in frames]
 controls={2209:[],306:[],307:[]}
 def reject(action):
  try:action()
  except AssertionError:return True
  raise AssertionError('Corrupted inspection hold accepted')
 for n,run,frame in((2209,306,5830),(306,306,6100),(307,307,6630)):
  data=raw(run,frame);screen=picture(run,frame);wrapped=struct.unpack_from('<I',arm,0x54450 if n==2209 else 0x54894)[0];formatted=bytes.fromhex(cases[n]['native_pipeline']['formatted_hex']);first=entries[n].text[:1]
  for at,label in((owner+0x2030,'resident-leading-character'),(wrapped+formatted.index(first),'formatted-leading-character')):
   bad=bytearray(data);bad[at-BASE]^=1;controls[n].append(dict(message_ID=n,negative=label,rejected=reject(lambda:verify(n,run,frame,data=bytes(bad)))))
  lines=cases[n].get('lines',[entries[n].text.decode('ascii')]);positions=[(0,0,'erase-first-glyph'),(len(lines)-1,len(lines[-1])-1,'erase-final-glyph')]
  if n==2209:positions.extend(((0,lines[0].index('no'),'erase-panicked-no-n'),(1,lines[1].index('alive'),'erase-return-alive-a')))
  else:positions.append((0,lines[0].index('information'if n==306 else'lookout'),'erase-information-or-lookout-word'))
  for row,col,label in positions:
   bad=screen.copy();x,y=16+(6 if n==2209 else 0)+6*col,296+16*row;bad.paste('white',(x,y,x+6,y+11));controls[n].append(dict(message_ID=n,negative=label,rejected=reject(lambda:verify(n,run,frame,screen=bad))))
  bad=screen.copy();bad.putpixel((16,340),(0,8,0));controls[n].append(dict(message_ID=n,negative='stray-blank-paper-ink',rejected=reject(lambda:verify(n,run,frame,screen=bad))))
 assert[len(controls[n])for n in(2209,306,307)]==[7,6,6]
 for run,frames in((306,(4800,5800,6100,6300)),(307,(4800,6600,6630,6850))):
  for frame in frames:
   data=raw(run,frame);cpu,get=get_machine(arm,data);duty=get(0xCB1A8)+0x2090;mode=list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)));assert mode==[0,0,0];state=dict(status_path=run,frame=frame,mode=mode,lookout_slot3=get(0x82BC4,duty,3),Charles_slot9=get(0x82BC4,duty,9),logical_role7_member=get(0x82478,duty,7),RAM_sha256=sha(data))
   if frame==runs[run]['path']['terminal_frame']:
    controller=data.find(struct.pack('<I',0x02147148),0x170000);assert controller>=0 and struct.unpack_from('<I',data,controller+0x74)[0]==0;state['original_Info_Mode_Inspect_controller_state']=0
   states.append(state)
 def flow(items):
  result=[]
  for run,frame,label in items:
   picture(run,frame);result.append(dict(status_path=run,frame=frame,visually_reviewed_state=label,RAM=runs[run]['snapshots'][frame]['path'],RAM_sha256=sha(raw(run,frame)),capture=runs[run]['images'][frame]['path'],capture_sha256=runs[run]['images'][frame]['PNG_sha256'],historical_only_not_current_startup_or_opposite_consumer_prose_credit=True))
  return result
 sea_flow=flow(((306,5800,'complete original creature-inspection reaction'),(306,5930,'reaction before normal A dismissal'),(306,6100,'following literal306 status;separate consumer'),(306,6300,'normal final A returns to Info Mode/Inspect,not Sea View')))
 status_flow=flow(((306,6100,'complete306 following sea reaction'),(306,6300,'normal306 dismissal returns to Inspect'),(307,6630,'complete307 with lookout3 empty,despite logical fallback18'),(307,6850,'normal307 dismissal returns to Inspect')))
 ROOT.mkdir(parents=True)
 def sheet(path,items,columns):
  im=Image.new('RGB',(columns*256,410*((len(items)+columns-1)//columns)),'#263238');draw=ImageDraw.Draw(im)
  for i,r in enumerate(items):
   x,y=i%columns*256,i//columns*410;draw.text((x+4,y+3),'Historical V1578 '+str(r.get('message_ID','flow'))+' '+str(r['frame']),fill='white');im.paste(Image.open(r['capture']),(x,y+24))
  im.save(path);return dict(path=str(path),sha256=sha(path.read_bytes()))
 commonproof=dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),historical_candidate=str(OLDROM),historical_candidate_sha256=sha(OLDROM.read_bytes()),historical_both_paths_proof=str(hp),historical_both_paths_proof_sha256=sha(hp.read_bytes()),historical_reports=[dict(status_path=n,path=r['report_path'],sha256=r['report_sha256'])for n,r in runs.items()],exact_historical_input_journals=journals,all_accepted_input_events_reconstructed_at_pause_frame_plus1=True,no_fixtures_after4800=True,eight_original_mode_lookout_and_Inspect_states=states,completed_48_and46_owned_byte_whole4MiB_registration_fixture_audits_hash_bound=True,fixture_48_and46_natural_RNG_call_not_forced_value=True,source_code_and_three_inherited_hooks_current_bound=True,original48_and46_byte_fixtures=[r['path']['audit']['sole_fixture']for r in runs.values()],both_original_Inspect_returns_not_Sea_View=True,all10_current_historical_selected_payloads_and_native_font_planes_equal=True,no_new_current_emulator_runs_or_visits=True,scope='Historical V1578 targeted cold-boot inspection replays use registration/location of existing Monster Fish,plus existing Charles18 moved9-to3 only in the48-byte positive-lookout fixture;the46-byte path keeps lookout3 empty. One original RNG initialization runs naturally;no RNG value,message ID,target type,renderer,actor identity or outcome is forced. Completed whole4MiB/input/RAM/PNG/donor audits are hash-bound without unnecessary replay. Current x6 spoken and x0 literal full native planes match complete historical RGB ink/blank masks. Only2209 among sea voices and both306/307 statuses have individual activation. Returns are Info Mode/Inspect at6300/6850. No new current startup/emulator event,earned discovery/travel/assignment,full route or hardware proof.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
 for label,holds,flows,ids,negative in(('sea',sea_holds,sea_flow,[2209],controls[2209]),('status',status_holds,status_flow,[306,307],controls[306]+controls[307])):
  sheets=[sheet(ROOT/f'{label}_complete_historical_holds.png',holds,2),sheet(ROOT/f'{label}_original_Inspect_transitions.png',flows,2)]
  save(ROOT/f'historical_{label}_inspection_current_binding.json',dict(**commonproof,historical_holds=holds,historical_IDs=ids,scoped_historical_inspection_and_return_transitions_freshly_rechecked=flows,negative_controls_current_binding_on_offline_clones=negative,only2209_individually_activated_other7_use_family_sample=label=='sea',both306_307_individually_activated=label=='status',opposite_consumer_context_only_no_extra_credit=True,review_sheets=sheets))
 print('Four spoken2209 holds,four literal306/307 holds,19 corruptions,8 source states and both normal Inspect returns pass;no new emulator run.')
