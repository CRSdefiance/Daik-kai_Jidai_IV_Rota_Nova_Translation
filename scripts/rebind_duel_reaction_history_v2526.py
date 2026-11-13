"""Four V1206 timed-reaction holds bound to current fonts and exact historical inputs."""
from pathlib import Path
import struct
from PIL import Image,ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.duel_bark_editorial import current_entries as old_entries
from dk4tool.rom.nds import NdsImage
from scripts.verify_duel_actual_holds_v1171 import actual_widget
from scripts.probe_duel_compiled_fonts_v1136c import expected_plane
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_reaction_history_v2526')
ROM=Path('out/all_routes_combined_v2284_candidate.nds')
OLDROM=Path('out/all_routes_combined_v1206_candidate.nds')
if __name__=='__main__':
 assert not ROOT.exists()
 rom,oldrom=map(NdsImage.open,(ROM,OLDROM));arm=rom.read_file('/__arm9__.bin');oldarm=oldrom.read_file('/__arm9__.bin')
 entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm);prior=old_entries(oldrom.read_file('/COMMON/MESFILE.DK4'),oldarm)
 assert all(entries[n].text==prior[n].text for n in range(1957,1973))
 fontproofpath=Path('work/analysis/duel_reaction_fonts_v2525/native_font_proof.json');fontproof=read(fontproofpath)
 fonts={r['message_ID']:r for r in fontproof['cases']};font=GameAsciiFont.from_arm9(arm);kanji=rom.read_file('/GRP/KANJI.FNT')
 hpath=Path('work/analysis/duel_bark_terminal_v1211/terminal_gameplay_verification.json');historical=read(hpath)
 reportpath=Path(historical['terminal_report']);report=read(reportpath);folder=reportpath.parent
 assert sha(OLDROM.read_bytes())==historical['candidate_sha256']==report['ROM_sha256']and sha(reportpath.read_bytes())==historical['terminal_report_sha256']
 assert report['frames']==8203 and report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
 assert historical['source_and_disposable_saves_unchanged']and historical['last_fixture_frame5770_before_duel5772']and len(historical['all31_fixture_replays'])==31
 spans=[tuple(r)for r in historical['all_original_combat_input_outcome_and_RNG_source_spans_exact']]
 assert all(arm[a:b]==oldarm[a:b]for a,b in spans)
 snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']}
 screenshots={r['frame']:r for r in report['frames_captured']}
 def source_raw(frame):
  item=snapshots[frame];raw=Path(item['path']).read_bytes();assert len(raw)==0x400000 and sha(raw)==item['sha256'];return raw
 def verify(n,frame,raw_override=None,image_override=None):
  raw=source_raw(frame)if raw_override is None else raw_override
  picture=Path(screenshots[frame]['path']);assert sha(picture.read_bytes())==screenshots[frame]['PNG_sha256']
  image=Image.open(picture).convert('RGB')if image_override is None else image_override.convert('RGB')
  widget,controller,header,h=actual_widget(raw);assert h[:3]==(4,52,36)and h[4]==40
  cpu,get=get_machine(arm,raw);objects=list(struct.unpack('<2I',cpu.mem_read(controller+0x34,8)))
  assert[get(0x7EE08,obj)for obj in objects]==[1,32]
  table=0x02117560 if n<1965 else 0x021175C0
  assert get(0x53F4C,objects[0],table)==n
  packed=raw[header-0x02000000+40:header-0x02000000+40+3744]
  pixels=bytes((v>>shift)&15 for v in packed for shift in(0,4))
  expected,letters=expected_plane(arm,kanji,font,fonts[n]['lines'])
  assert pixels==bytes(expected)and sha(pixels)==fonts[n]['source_208x36_4bit_SHA256']
  for row in range(3):
   for y in range(12):
    for x in range(144):assert image.getpixel((56+x,212+row*20+y))==((0,8,0)if pixels[(row*12+y)*208+x]else(255,255,255))
  assert sum(bool(v)for v in pixels)==sum(bool(pixels[y*208+x])for y in range(36)for x in range(144))
  return dict(message_id=n,message_ID=n,frame=frame,source_actor_IDs=[1,32],source_speaker_side=0,source_table=table,
   lines=fonts[n]['lines'],source_bitmap_header=header,source_widget=widget,source_controller=controller,
   whole208x36_current_font_and_all_three144x12_actual_RGB_ink_blank_masks_equal=True,
   RAM=str(snapshots[frame]['path']),RAM_sha256=sha(raw),capture=str(picture),capture_sha256=sha(picture.read_bytes()),
   historical_capture_candidate_sha256=historical['candidate_sha256'],current_payload_font_binding_only_not_current_emulator_visit=True)
 holds=[verify(n,frame)for n,frames in((1958,(6093,6113)),(1966,(5953,5973)))for frame in frames]
 journalpath=folder/'navigation_command_journal.json';journal=read(journalpath)
 rejected_commands=[r for r in journal['commands_received']if not r['validation_passed']]
 assert[(r['frame'],r['command']['until'],r['rejected_before_any_input_or_fixture'])for r in rejected_commands]==[(6032,6033,'Invalid duration'),(6892,6893,'Invalid duration')]
 schedule=read('work/analysis/duel_bark_live_v1207/original_load_inputs.json')
 for item in journal['commands_received']:
  if not item['validation_passed']:continue
  command=item['command']
  if command.get('stop'):continue
  assert command['until']in snapshots and command.get('duration',12)<=command['until']-item['frame']
  if command.get('buttons')or command.get('touch')is not None:
   event=dict(start=item['frame']+1,duration=command.get('duration',12),buttons=command.get('buttons',[]))
   if command.get('touch')is not None:event['touch']=command['touch']
   schedule.append(event)
  if item['frame']>=5772:assert'battle_fixture'not in command
 assert schedule==report['scripted_input_schedule']and not any(r['start']in(6033,6893)for r in schedule)
 controls=[]
 def reject(action):
  try:action()
  except AssertionError:return True
  raise AssertionError('Corrupted timed reaction accepted')
 for hold in holds[::2]:
  n,frame=hold['message_id'],hold['frame'];raw=source_raw(frame);image=Image.open(hold['capture']).convert('RGB');at=hold['source_bitmap_header']-0x02000000
  bad=bytearray(raw);struct.pack_into('<I',bad,at,5)
  controls.append(dict(message_ID=n,negative='wrong-native-format-header',rejected=reject(lambda:verify(n,frame,raw_override=bytes(bad)))))
  lines=hold['lines'];base_y=12 if len(lines)==1 else 0
  cells=[(0,0,'delete-leading-glyph'),(len(lines)-1,len(lines[-1])-1,'delete-final-glyph'),(0,3,'delete-complete-personal-I')if n==1958 else(1,0,'delete-complete-personal-I')]
  for line,column,label in cells:
   bad=image.copy();x,y=56+column*6,212+(base_y//12+line)*20;bad.paste('white',(x,y,x+6,y+12))
   controls.append(dict(message_ID=n,negative=label,rejected=reject(lambda:verify(n,frame,image_override=bad))))
  line,column=(0,lines[0].index('coming')+1)if n==1958 else(1,lines[1].index('guard')+1)
  bad=bytearray(raw)
  for y in range(base_y+line*12,base_y+line*12+12):pos=at+40+y*104+column*3;bad[pos:pos+3]=bytes(3)
  controls.append(dict(message_ID=n,negative='delete-interior-native-word-glyph',rejected=reject(lambda:verify(n,frame,raw_override=bytes(bad)))))
  bad=image.copy();point=next((56+x,212+r*20+y)for r in range(3)for y in range(12)for x in range(144)if image.getpixel((56+x,212+r*20+y))==(255,255,255));bad.putpixel(point,(0,8,0))
  controls.append(dict(message_ID=n,negative='stray-ink-in-crop-blank-plane',rejected=reject(lambda:verify(n,frame,image_override=bad))))
 assert len(controls)==12 and all(r['rejected']for r in controls)
 for state in historical['natural_HP_evolution']:
  raw=source_raw(state['frame']);cpu,get=get_machine(arm,raw);root=get(0xCB184)
  assert[get(0x7E19C,p)for p in(root+0x19E4,root+4+32*32)]==state['own_enemy_captain_HP']
 flow=[]
 for item in historical['normal_A_defeat_GameOver_title_flow']:
  assert sha(source_raw(item['frame']))==item['RAM_sha256']and sha(Path(item['capture']).read_bytes())==item['capture_sha256']
  flow.append(dict(item,historical_only_not_current_aftermath_or_startup_translation_approval=True))
 assert[r['frame']for r in flow]==[7443,7563,7783,8203]
 for hold in historical['actual_preserved_escape_holds']:
  assert sha(source_raw(hold['frame']))==hold['RAM_sha256']and sha(Path(hold['capture']).read_bytes())==hold['capture_sha256']
 ROOT.mkdir(parents=True);sheet=Image.new('RGB',(512,820),'#263238');draw=ImageDraw.Draw(sheet)
 for i,hold in enumerate(holds):x,y=i//2*256,i%2*410;draw.text((x+4,y+3),'Historical V1206 ID'+str(hold['message_id']),fill='white');sheet.paste(Image.open(hold['capture']),(x,y+24))
 a=ROOT/'four_historical_complete_timed_reaction_holds.png';sheet.save(a)
 sheet=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(sheet)
 for i,item in enumerate(flow):draw.text((i*256+4,3),str(item['frame'])+' '+item['visually_reviewed_state'],fill='white');sheet.paste(Image.open(item['capture']),(i*256,24))
 b=ROOT/'four_historical_defeat_title_transitions.png';sheet.save(b)
 save(ROOT/'historical_duel_reaction_current_binding.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(rom.read_file('/COMMON/MESFILE.DK4')),
  historical_candidate=str(OLDROM),historical_candidate_sha256=sha(OLDROM.read_bytes()),historical_proof=str(hpath),historical_proof_sha256=sha(hpath.read_bytes()),
  historical_report=str(reportpath),historical_report_sha256=sha(reportpath.read_bytes()),historical_holds=holds,historical_IDs=[1958,1966],
  scoped_historical_cancellation_and_battle_transitions_freshly_rechecked=flow,twelve_negative_controls_current_binding_on_offline_clones=controls,
  exact_historical_input_journal=str(journalpath),exact_historical_input_journal_sha256=sha(journalpath.read_bytes()),
  all_accepted_input_events_reconstructed_at_pause_frame_plus1=True,two_rejected_gap_commands_apply_no_input=True,
  actual_timing_events=historical['actual_timing_controller_events'],original_A_mapping_proof=historical['original_A_bit5_mapping_read_only_proof'],
  original31_pre_duel_fixture_audits_hash_bound_not_needlessly_repeated=True,natural_HP_evolution=historical['natural_HP_evolution'],
  preserved1973_escape_holds_historical_context_only_no_duplicate_credit=historical['actual_preserved_escape_holds'],
  source_timing_combat_selector_RNG_and_outcome_code_current_old_exact=[dict(start=x,end=y,sha256=sha(arm[x:y]))for x,y in spans],
  no_new_current_battle_emulator_runs_or_family_visits=True,all16_current_historical_payloads_equal=True,
  review_sheets=[dict(path=str(p),sha256=sha(p.read_bytes()))for p in(a,b)],
  scope='Historical V1206 original timed inputs and natural duel result after31 disclosed positive-health/contact/diplomatic fixtures before combat. Four side0 reaction holds bind current complete fonts and RGB. Accepted inputs and two rejected commands are checked exactly. No during/after-duel actor,HP,RNG,message or outcome injection;no current gameplay,earned progression or hardware claim. Later defeat/title captures are historical only.',
  producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('Four historical reaction holds,exact accepted/rejected input schedule,12 negative controls and4 historical defeat/title transitions pass.')
