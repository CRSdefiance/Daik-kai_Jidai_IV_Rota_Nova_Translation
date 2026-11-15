"""Current alert/follow-up fonts and original deferred fire cleanup in preserved gameplay."""
from pathlib import Path
from types import FunctionType
import struct
from PIL import Image,ImageDraw
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.powder_fire_editorial import current_entries as old_entries
from dk4tool.rom.nds import NdsImage
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
BASE=0x02000000;ROOT=Path('work/analysis/powder_fire_history_v2575')
ROM=Path('out/all_routes_combined_v2284_candidate.nds');OLDROM=Path('out/all_routes_combined_v1316_candidate.nds')
if __name__=='__main__':
 assert not ROOT.exists()
 rom,oldrom=map(NdsImage.open,(ROM,OLDROM));arm=rom.read_file('/__arm9__.bin');oldarm=oldrom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');oldcommon=oldrom.read_file('/COMMON/MESFILE.DK4')
 entries=current_entries(common,arm);prior=old_entries(oldcommon,oldarm);assert all(entries[n].text==prior[n].text for n in range(2052,2058))
 assert entries[585].text==entries[586].text==prior[585].text==prior[586].text
 hpath=Path('work/analysis/powder_fire_verified_v1322b/actual_powder_fire_verification.json');h=read(hpath);reportpath=Path(h['report']);report=read(reportpath)
 assert sha(reportpath.read_bytes())==h['report_sha256'] and sha(OLDROM.read_bytes())==h['candidate_sha256']==report['ROM_sha256']
 assert report['frames']==7590 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
 assert h['source_and_disposable_donors_unchanged'] and h['no_actor_ID_RNG_eligibility_fire_flag_result_or_numeric_message_injection'] and h['no_during_or_post_battle_fixtures']
 fixture=h['sole_prebattle_fixture_entire4MiB_replayed'];assert report['synthetic_battle_recovery_proximity_fixtures']==[{**fixture,'frame':5000}]
 assert len(fixture['owned_bytes'])==24 and len(fixture['changes'])==16 and fixture['all_actor_objects_IDs_abilities_health_towns_defenses_shares_diplomacy_RNG_events_and_other4MiB_bytes_exact']
 spans=[tuple(r) for r in h['source_unforced_powder_fire_and_gun_position_actor_code_exact_clean']]+[(0x2D778,0x2D810),(0x2DEBC,0x2DEC0),(0x1185E0,0x118600)]
 cleanarm=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');assert all(arm[a:b]==oldarm[a:b]==cleanarm[a:b] for a,b in spans)
 assert struct.unpack_from('<I',arm,0x2DEBC)[0]==0x021185E0 and list(struct.unpack_from('<8i',arm,0x1185E0))==list(range(585,593))
 instructions=[dict(address=i.address,bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(arm[0x2D778:0x2D810],BASE+0x2D778)]
 assert [(i['address'],i['mnemonic']) for i in instructions if i['address'] in(0x0202D790,0x0202D7E0,0x0202D804,0x0202D808,0x0202D80C)]==[(0x0202D790,'bl'),(0x0202D7E0,'bl'),(0x0202D804,'ldrb'),(0x0202D808,'bic'),(0x0202D80C,'strb')]
 fp=read('work/analysis/powder_fire_fonts_v2574/native_font_proof.json');case=next(r for r in fp['cases'] if r['source_voice']==1);assert case['message_ID']==2053
 p=Path(case['preview']);assert sha(p.read_bytes())==case['preview_sha256'];plane=Image.open(p).convert('L');alert_mask=bytes(1 if v==0 else 0 for v in plane.tobytes());assert plane.size==(228,64)
 historicalblocks=IlnkContainer.parse(oldcommon).blocks;owner,wrapped=[struct.unpack_from('<I',arm,at)[0] for at in(0x552A0,0x54450)]
 assert owner==struct.unpack_from('<I',oldarm,0x552A0)[0] and wrapped==struct.unpack_from('<I',oldarm,0x54450)[0]
 class CurrentFont:
  @staticmethod
  def open(path):
   assert str(path)=='out/all_routes_combined_v255_candidate.nds'
   return rom
 raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
 snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']};images={r['frame']:r for r in report['frames_captured']}
 def source_raw(frame):
  item=snapshots[frame];raw=Path(item['path']).read_bytes();assert len(raw)==0x400000 and sha(raw)==item['sha256'];return raw
 assert sha(source_raw(5000))==fixture['before_RAM_sha256']
 def verify(frame,raw_override=None,image_override=None):
  raw=source_raw(frame) if raw_override is None else raw_override
  item=images[frame];picture=Path(item['path']);assert sha(picture.read_bytes())==item['PNG_sha256']
  image=Image.open(picture).convert('RGB') if image_override is None else image_override.convert('RGB')
  cpu,get=get_machine(arm,raw);fleet,actors=get(0xCB1A8),get(0xCB184);mobile=get(0x36C70,fleet+4+132+12)
  template=raw[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0];formatted=raw[wrapped-BASE:wrapped-BASE+512].split(b'\0')[0]
  if frame in(7210,7250):
   actor=get(0x82428,fleet+0x2090,9);assert actor==actors+4+16*32 and get(0x7EE08,actor)==16 and actor in[get(0x55DC4,mobile,i) for i in range(4)] and get(0x53F4C,actor,0x02117980)==2053
   assert template==entries[2053].text and formatted.hex()==case['native_formatted_hex'];mask=alert_mask;lines=case['lines'];selected=[2053];n=2053
  else:
   assert frame in(7350,7390) and template==entries[585].text==entries[586].text
   selected=[585,586];n=None;lines=[line.strip().decode('ascii') for line in formatted.split(b'\n')];assert lines==['Fire extinguished!']
   mask=raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000);assert mask==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),lines)
  assert raw.count(historicalblocks[prior[selected[0]].block])==1
  expected={(16+x,296+y) for y in range(64) for x in range(228) if mask[y*228+x]}
  actual={(x,y) for y in range(294,366) for x in range(16,244) if image.getpixel((x,y))==(0,8,0)}
  assert actual==expected and len(expected)==(472 if n==2053 else 200)
  return dict(message_ID=n,message_id=n,matching_cached_template_ID_candidates=selected,frame=frame,selected_alert=n==2053,actual_source_gunner_ID=16 if n==2053 else None,original_entry=0x02053F0C if n==2053 else None,original_parent=0x02053F40 if n==2053 else None,original_table_stack_offset=0x274 if n==2053 else None,lines=lines,
   current_payload_wrapped_bytes_and_complete228x64_current_native_font_RGB_ink_blank_mask_equal=True,missing_or_unexpected_foreground_pixels=0,matching_foreground_pixels=len(expected),historical_block_unique_and_current_selected_payload_exact=True,uniform_margins_complete_first_final_letters_words_and_bounds_pass=True,followup_individual_ID_not_claimed=n is None,
   RAM=str(snapshots[frame]['path']),RAM_sha256=sha(raw),capture=str(picture),capture_sha256=sha(picture.read_bytes()),historical_only_not_current_emulator_visit=True)
 holds=[verify(frame) for frame in(7210,7250)];followups=[verify(frame) for frame in(7350,7390)]
 journalpath=reportpath.parent/'navigation_command_journal.json';journal=read(journalpath);assert all(r['validation_passed'] for r in journal['commands_received'])
 schedule=read('work/analysis/powder_fire_scene_v1320/original_load_inputs.json')
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
 def state_verify(expected,raw_override=None):
  raw=source_raw(expected['frame']) if raw_override is None else raw_override
  cpu,get=get_machine(arm,raw);fleet,world,towns=get(0xCB1A8),get(0xCB19C),get(0xCB178);mobile=get(0x36C70,fleet+4+132+12)
  actual=dict(frame=expected['frame'],mode8_12_16=list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12))),town_ID=struct.unpack('<I',cpu.mem_read(world+0x1360,4))[0],town_defenses=get(0xB3FD4,towns+4+73*108,1),own_Hull_Crew=[get(0x5543C,mobile),get(0x55444,mobile)],original_mobile_flag0E=bytes(cpu.mem_read(mobile+14,1))[0])
  assert actual==expected
  return dict(actual,RAM_sha256=sha(raw))
 states=[state_verify(s) for s in h['original_fire_and_followup_states']];assert len(states)==8
 assert all(s['original_mobile_flag0E']&1 for s in states if s['frame'] in(7210,7250,7350,7390)) and all(not s['original_mobile_flag0E']&1 for s in states if s['frame'] in(7490,7590))
 controls=[]
 def rejected(action):
  try:action()
  except AssertionError:return True
  raise AssertionError('Corrupted alert/follow-up or early cleanup accepted')
 raw=source_raw(7210);image=Image.open(images[7210]['path']).convert('RGB');lines=case['lines']
 for at,label in((owner+0x2030+entries[2053].text.index(b'The'),'corrupt-resident-leading-T'),(wrapped+bytes.fromhex(case['native_formatted_hex']).index(b'The'),'corrupt-wrapped-leading-T')):
  bad=bytearray(raw);bad[at-BASE]^=1;controls.append(dict(negative=label,rejected=rejected(lambda:verify(7210,raw_override=bytes(bad)))))
 for line,column,label in((0,0,'erase-complete-leading-T'),(1,len(lines[1])-1,'erase-final-exclamation'),(1,0,'erase-caught-fire-continuation-c')):
  bad=image.copy();x,y=22+column*6,296+line*16;bad.paste('white',(x,y,x+6,y+11));controls.append(dict(negative=label,rejected=rejected(lambda:verify(7210,image_override=bad))))
 bad=image.copy();bad.putpixel((16,296),(0,8,0));controls.append(dict(negative='stray-alert-margin-ink',rejected=rejected(lambda:verify(7210,image_override=bad))))
 image=Image.open(images[7350]['path']).convert('RGB')
 for column,label in((0,'erase-followup-leading-F'),(len('Fire extinguished!')-1,'erase-followup-final-exclamation')):
  bad=image.copy();x,y=22+column*6,296;bad.paste('white',(x,y,x+6,y+11));controls.append(dict(negative=label,rejected=rejected(lambda:verify(7350,image_override=bad))))
 bad=bytearray(source_raw(7350));u,g=get_machine(arm,bytes(bad));mobile=g(0x36C70,g(0xCB1A8)+4+132+12);bad[mobile-BASE+14]&=0xFE;expected=next(s for s in h['original_fire_and_followup_states'] if s['frame']==7350)
 controls.append(dict(negative='premature-fire-bit-clear-while-followup-visible',rejected=rejected(lambda:state_verify(expected,raw_override=bytes(bad)))))
 assert len(controls)==9 and all(r['rejected'] for r in controls)
 sourcefolder=Path(h['source_header_reference']).parent;sourcereportpath=sourcefolder/'capture_report.json';sourcereport=read(sourcereportpath);sourceROM=Path('out/all_routes_combined_v1266_candidate.nds');assert sourcereport['ROM_sha256']==sha(sourceROM.read_bytes())
 sourcearm=NdsImage.open(sourceROM).read_file('/__arm9__.bin');assert all(sourcearm[a:b]==arm[a:b] for a,b in spans)
 sourcesnaps={r['frame']:r for r in sourcereport['read_only_capture_RAM_snapshots']+sourcereport['read_only_pause_RAM_snapshots']};sourcecleanup=[]
 for s in h['original_source_cleanup_phase_states']:
  item=sourcesnaps[s['frame']];raw=Path(item['path']).read_bytes();assert sha(raw)==item['sha256'];u,g=get_machine(arm,raw);mobile=g(0x36C70,g(0xCB1A8)+4+132+12)
  assert bytes(u.mem_read(mobile+14,1))[0]==s['flag0E'] and [g(0x5543C,mobile),g(0x55444,mobile)]==s['Hull_Crew'];sourcecleanup.append(dict(s,RAM=item['path'],RAM_sha256=sha(raw)))
 assert [s['flag0E'] for s in sourcecleanup]==[5,5,4] and sourcecleanup[-1]['Hull_Crew']==states[-1]['own_Hull_Crew']==[56,112]
 headerref=Path(h['source_header_reference']);assert sha(headerref.read_bytes())==h['source_header_reference_sha256'] and Image.open(holds[0]['capture']).convert('RGB').crop((0,0,256,294)).tobytes()==Image.open(headerref).convert('RGB').crop((0,0,256,294)).tobytes()
 flow=[]
 for frame,label in((7250,'complete original gunner fire alert'),(7390,'original Fire extinguished follow-up;fire bit still set'),(7490,'follow-up dismissed;original fire bit now clear'),(7590,'original sea battle continues')):
  p=Path(images[frame]['path']);assert sha(p.read_bytes())==images[frame]['PNG_sha256'];flow.append(dict(frame=frame,visually_reviewed_state=label,RAM=str(snapshots[frame]['path']),RAM_sha256=sha(source_raw(frame)),capture=str(p),capture_sha256=sha(p.read_bytes()),historical_only_not_current_startup_or_battle_outcome_approval=True))
 ROOT.mkdir(parents=True);sheet=Image.new('RGB',(512,820),'#263238');draw=ImageDraw.Draw(sheet)
 for i,r in enumerate(holds+followups):
  x,y=i//2*256,i%2*410;draw.text((x+4,y+3),'Historical V1316 '+('2053' if r['selected_alert'] else '585/586 ambiguous')+' '+str(r['frame']),fill='white');sheet.paste(Image.open(r['capture']),(x,y+24))
 a=ROOT/'four_historical_alert_and_extinguished_holds.png';sheet.save(a)
 sheet=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(sheet)
 for i,r in enumerate(flow):draw.text((i*256+4,3),str(r['frame'])+' original fire flow',fill='white');sheet.paste(Image.open(r['capture']),(i*256,24))
 b=ROOT/'historical_fire_followup_deferred_cleanup_battle_return.png';sheet.save(b)
 save(ROOT/'historical_powder_fire_current_binding.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),historical_candidate=str(OLDROM),historical_candidate_sha256=sha(OLDROM.read_bytes()),historical_proof=str(hpath),historical_proof_sha256=sha(hpath.read_bytes()),historical_report=str(reportpath),historical_report_sha256=sha(reportpath.read_bytes()),historical_holds=holds,historical_IDs=[2053],context_only_extinguished_followup_holds=followups,followup585_586_individual_ID_ambiguous_no_extra_credit=True,
  scoped_historical_cancellation_and_battle_transitions_freshly_rechecked=flow,nine_negative_controls_current_binding_on_offline_clones=controls,exact_historical_input_journal=str(journalpath),exact_historical_input_journal_sha256=sha(journalpath.read_bytes()),all_accepted_input_events_reconstructed_at_pause_frame_plus1=True,
  source_ignition_gun_position_and_deferred_cleanup_code_current_clean_historical_equal=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],original_followup_return_before_bit_clear_instructions=instructions,eight_original_fire_followup_and_return_states=states,source1266_cleanup_states_freshly_rechecked=sourcecleanup,source1266_report=str(sourcereportpath),source1266_report_sha256=sha(sourcereportpath.read_bytes()),
  sole_prebattle_fixture_at5000_whole4MiB_audit_hash_bound_not_needlessly_repeated=True,sole_fixture_disclosure=fixture,all6_current_historical_payloads_and_all8_voice_font_planes_equal=True,only2053_has_individual_alert_activation_other5_use_family_sample=True,no_new_current_battle_emulator_runs_or_family_visits=True,original_fire_cleanup_deferred_until_followup_dismissal_in_both_versions=True,prior1322_premature_cleanup_expectation_preserved_not_repeated=True,
  review_sheets=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in(a,b)],scope='Historical V1316 unforced own-ship powder fire with original gun-position speaker Gerhard16. One frame5000 location/existing Gunnery assignment/native sailor-capacity fixture changes16 of24 owned bytes;its full4MiB audit is bound without needless replay. No actorID,RNG,eligibility,fire flag,result or message injection and no later fixture. Two complete2053 and two context-only extinguished holds bind current text/fonts. Original follow-up bytes match both585/586;no individual ID is chosen. Exact inputs,natural Hull/Crew and mode states,and original cleanup after follow-up dismissal are freshly checked against corrected1322b and source1266. Other five alerts use current offline checks and family coverage. No current startup,earned prerequisites,ship loss,battle result or hardware proof.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('Two full historical2053 alerts,two ambiguous-ID follow-ups,9 corruptions,8 native states and original deferred cleanup/battle return pass.')
