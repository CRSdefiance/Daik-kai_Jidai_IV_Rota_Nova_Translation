"""Current special text/font binding to six preserved V1224 holds and flow."""
from pathlib import Path
import struct
from PIL import Image,ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.duel_special_editorial import current_entries as old_entries
from dk4tool.rom.nds import NdsImage
from scripts.duel_special_dispatch_v1217 import IDS,helper,front
from scripts.verify_duel_actual_holds_v1171 import actual_widget
from scripts.probe_duel_compiled_fonts_v1136c import expected_plane
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_special_history_v2535')
ROM=Path('out/all_routes_combined_v2284_candidate.nds')
OLDROM=Path('out/all_routes_combined_v1224_candidate.nds')
if __name__=='__main__':
 assert not ROOT.exists()
 rom,oldrom=map(NdsImage.open,(ROM,OLDROM));arm=rom.read_file('/__arm9__.bin');oldarm=oldrom.read_file('/__arm9__.bin')
 entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm);prior=old_entries(oldrom.read_file('/COMMON/MESFILE.DK4'),oldarm)
 assert all(entries[n].text==prior[n].text for n in IDS)
 assert arm[0x535E8:0x53628]==oldarm[0x535E8:0x53628]==helper()[0]
 assert arm[0xDAF0:0xDB5C]==oldarm[0xDAF0:0xDB5C]==front(1480)[0]
 fontproofpath=Path('work/analysis/duel_special_fonts_v2534/native_font_proof.json');fontproof=read(fontproofpath)
 fonts={r['message_ID']:r for r in fontproof['cases']};font=GameAsciiFont.from_arm9(arm);kanji=rom.read_file('/GRP/KANJI.FNT')
 hpath=Path('work/analysis/duel_long_terminal_v1245b/terminal_gameplay_verification.json');historical=read(hpath)
 reportpath=Path(historical['report']);report=read(reportpath);folder=reportpath.parent
 assert sha(OLDROM.read_bytes())==historical['candidate_sha256']==report['ROM_sha256']and sha(reportpath.read_bytes())==historical['report_sha256']
 assert report['frames']==11782 and report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
 assert historical['source_and_disposable_saves_unchanged']and historical['all_fixtures_before_duel5772_last5770']and len(historical['all31_fixture_replays'])==31
 assert historical['original_random_chance10_percent_not_forced']and historical['no_numeric_message_actor_ID_RNG_seed_eligibility_flag_or_result_injection']
 assert historical['no_healing_revival_relocation_or_ability_changes_during_or_after_duel']
 spans=[tuple(r)for r in historical['all_original_duel_and_attribute_HP_RNG_source_spans_exact']]
 assert all(arm[a:b]==oldarm[a:b]for a,b in spans)
 context=read('work/analysis/duel_special_context_v2530/source_context_packet.json')
 binding=next(r for r in context['all15_original_message_call_bindings']if r['message_ID']==1990)
 assert binding['actor_ID']==1 and binding['source_method']==0x0200F114 and binding['original_source_return']==0x0200F164
 assert binding['side']==0 and binding['duration']==120
 snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']}
 screenshots={r['frame']:r for r in report['frames_captured']}
 def source_raw(frame):
  item=snapshots[frame];raw=Path(item['path']).read_bytes();assert len(raw)==0x400000 and sha(raw)==item['sha256'];return raw
 def verify(frame,raw_override=None,image_override=None):
  raw=source_raw(frame)if raw_override is None else raw_override
  picture=Path(screenshots[frame]['path']);assert sha(picture.read_bytes())==screenshots[frame]['PNG_sha256']
  image=Image.open(picture).convert('RGB')if image_override is None else image_override.convert('RGB')
  widget,controller,header,h=actual_widget(raw);assert h[:3]==(4,52,36)and h[4]==40
  cpu,get=get_machine(arm,raw);objects=list(struct.unpack('<2I',cpu.mem_read(controller+0x34,8)))
  assert[get(0x7EE08,obj)for obj in objects]==[1,32]
  active=struct.unpack_from('<I',raw,controller-0x40-0x02000000+0x4C4)[0]
  assert active==objects[0]and get(0x7EE08,active)==1 and get(0x7E944,active,5)==100
  assert struct.unpack_from('<I',raw,controller-0x40-0x02000000+0x4EC)[0]==1
  assert sha(raw[0x28E70C:0x28E70C+1480])==fontproof['component_sha256']
  assert raw[0x28E6DC+0x2C]==21
  packed=raw[header-0x02000000+40:header-0x02000000+40+3744]
  pixels=bytes((v>>shift)&15 for v in packed for shift in(0,4))
  expected,letters=expected_plane(arm,kanji,font,fonts[1990]['lines'])
  assert pixels==bytes(expected)and sha(pixels)==fonts[1990]['source_208x36_4bit_SHA256']
  for row in range(3):
   for y in range(12):
    for x in range(144):assert image.getpixel((56+x,212+row*20+y))==((0,8,0)if pixels[(row*12+y)*208+x]else(255,255,255))
  assert sum(bool(v)for v in pixels)==sum(bool(pixels[y*208+x])for y in range(36)for x in range(144))
  return dict(message_id=1990,message_ID=1990,frame=frame,source_actor_IDs=[1,32],source_speaker_side=0,source_entry='D4D0',duration=120,
   original_special_source_binding=binding,lines=fonts[1990]['lines'],source_bitmap_header=header,source_widget=widget,source_controller=controller,
   whole208x36_current_font_and_all_three144x12_actual_RGB_ink_blank_masks_equal=True,current_identical_PIC_resident=True,
   RAM=str(snapshots[frame]['path']),RAM_sha256=sha(raw),capture=str(picture),capture_sha256=sha(picture.read_bytes()),
   historical_capture_candidate_sha256=historical['candidate_sha256'],current_payload_font_binding_only_not_current_emulator_visit=True)
 holds=[verify(r['frame'])for r in historical['actual_special_holds']]
 assert[r['frame']for r in holds]==[7622,7662,7702,7742,7782,7822]
 journalpath=folder/'navigation_command_journal.json';journal=read(journalpath)
 assert all(r['validation_passed']for r in journal['commands_received'])
 schedule=read('work/analysis/duel_long_live_v1243/original_load_inputs.json')
 for item in journal['commands_received']:
  command=item['command']
  if command.get('stop'):continue
  assert command['until']in snapshots and command.get('duration',12)<=command['until']-item['frame']
  if command.get('buttons')or command.get('touch')is not None:
   event=dict(start=item['frame']+1,duration=command.get('duration',12),buttons=command.get('buttons',[]))
   if command.get('touch')is not None:event['touch']=command['touch']
   schedule.append(event)
  if item['frame']>=5772:assert'battle_fixture'not in command
 assert schedule==report['scripted_input_schedule']and not any(5773<=r['start']<=10982 for r in schedule)
 controls=[]
 def reject(action):
  try:action()
  except AssertionError:return True
  raise AssertionError('Corrupted special hold accepted')
 hold=holds[0];frame=hold['frame'];raw=source_raw(frame);image=Image.open(hold['capture']).convert('RGB');at=hold['source_bitmap_header']-0x02000000
 bad=bytearray(raw);struct.pack_into('<I',bad,at,5)
 controls.append(dict(negative='wrong-native-format-header',rejected=reject(lambda:verify(frame,raw_override=bytes(bad)))))
 for column,label in ((0,'delete-complete-leading-Y'),(len(hold['lines'][0])-1,'delete-final-exclamation'),(hold['lines'][0].index('done')+1,'delete-interior-word-letter')):
  bad=image.copy();x,y=56+column*6,232;bad.paste('white',(x,y,x+6,y+12))
  controls.append(dict(negative=label,rejected=reject(lambda:verify(frame,image_override=bad))))
 bad=bytearray(raw)
 for y in range(12,24):pos=at+40+y*104;bad[pos:pos+3]=bytes(3)
 controls.append(dict(negative='delete-native-leading-Y',rejected=reject(lambda:verify(frame,raw_override=bytes(bad)))))
 bad=image.copy();point=next((56+x,212+r*20+y)for r in range(3)for y in range(12)for x in range(144)if image.getpixel((56+x,212+r*20+y))==(255,255,255));bad.putpixel(point,(0,8,0))
 controls.append(dict(negative='stray-ink-in-crop-blank-plane',rejected=reject(lambda:verify(frame,image_override=bad))))
 assert len(controls)==6 and all(r['rejected']for r in controls)
 for state in historical['natural_HP_evolution']:
  raw=source_raw(state['frame']);cpu,get=get_machine(arm,raw);root=get(0xCB184)
  assert[get(0x7E19C,p)for p in(root+0x19E4,root+4+32*32)]==state['own_enemy_HP']
 flow=[]
 for item in historical['natural_special_to_combat_and_original_victory_aftermath']:
  assert sha(source_raw(item['frame']))==item['RAM_sha256']and sha(Path(item['capture']).read_bytes())==item['capture_sha256']
  flow.append(dict(item,historical_only_not_current_aftermath_or_startup_translation_approval=True))
 assert[r['frame']for r in flow]==[8022,8622,10982,11782]
 ROOT.mkdir(parents=True);sheet=Image.new('RGB',(768,820),'#263238');draw=ImageDraw.Draw(sheet)
 for i,hold in enumerate(holds):
  x,y=i%3*256,i//3*410;draw.text((x+4,y+3),'Historical V1224 ID1990 frame'+str(hold['frame']),fill='white');sheet.paste(Image.open(hold['capture']),(x,y+24))
 a=ROOT/'six_historical_complete_special_holds.png';sheet.save(a)
 sheet=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(sheet)
 for i,item in enumerate(flow):draw.text((i*256+4,3),str(item['frame'])+' historical flow',fill='white');sheet.paste(Image.open(item['capture']),(i*256,24))
 b=ROOT/'four_historical_combat_victory_aftermath_transitions.png';sheet.save(b)
 save(ROOT/'historical_duel_special_current_binding.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(rom.read_file('/COMMON/MESFILE.DK4')),
  historical_candidate=str(OLDROM),historical_candidate_sha256=sha(OLDROM.read_bytes()),historical_proof=str(hpath),historical_proof_sha256=sha(hpath.read_bytes()),
  historical_report=str(reportpath),historical_report_sha256=sha(reportpath.read_bytes()),historical_holds=holds,historical_IDs=[1990],
  scoped_historical_cancellation_and_battle_transitions_freshly_rechecked=flow,six_negative_controls_current_binding_on_offline_clones=controls,
  exact_historical_input_journal=str(journalpath),exact_historical_input_journal_sha256=sha(journalpath.read_bytes()),
  all_accepted_input_events_reconstructed_at_pause_frame_plus1=True,no_inputs5773_through10982=True,
  original31_pre_duel_fixture_audits_hash_bound_not_needlessly_repeated=True,native_prerequisites=historical['native_prerequisites'],
  original_luck100_gives_unforced10_percent_special_chance=True,no_during_or_after_duel_HP_actor_RNG_message_or_outcome_injection=True,
  natural_HP_evolution=historical['natural_HP_evolution'],
  source_special_combat_selector_HP_RNG_and_outcome_code_current_old_exact=[dict(start=x,end=y,sha256=sha(arm[x:y]))for x,y in spans],
  no_new_current_battle_emulator_runs_or_family_visits=True,all15_current_historical_payloads_equal=True,
  only1990_has_individual_actual_special_activation_other14_family_sample=True,
  review_sheets=[dict(path=str(p),sha256=sha(p.read_bytes()))for p in(a,b)],
  scope='Historical V1224 original Hodram special and natural duel result after31 disclosed positive-health/contact/diplomatic fixtures before combat. Six side0 duration120 holds bind current full fonts and RGB. No inputs5773..10982;natural HP includes enemy4 at8502 and0 at8622. No current gameplay or earned progression claim. Four combat/victory/aftermath captures are historical only.',
  producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('Six historical Hodram special holds,exact input schedule,6 corruptions and4 historical combat/victory/aftermath transitions pass.')
