"""Bind historical battle/ordinary displays,format flags and returns to current code/text."""
from pathlib import Path
from types import FunctionType
import struct
from PIL import Image,ImageDraw
from dk4tool.patch.battle_personal_editorial import current_entries as historical_entries
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.battle_personal_actual_v898 import actual_view
from scripts.verify_personal_gameplay_v841 import hold as original_hold,get_machine,model_state
from scripts.battle_personal_layout_v892 import compiled,layout
from scripts.personal_chatter_layout_v837 import compiled as ordinary_compiled,layout as ordinary_layout
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels
from scripts.finish_refit_display_v712 import load
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/battle_personal_history_v2385');OLD=Path('work/analysis/battle_personal_v898/actual_gameplay_verification.json');BASE=0x02000000
SPECS={'Julio':(1577,14300,(14500,14700),14900,15100),'Carlo':(1590,14300,(14500,14700),14900,15100),'Joakim':(1572,17100,(17300,17500),17700,17900)}

def rejected(action):
 try:action()
 except AssertionError:return True
 raise AssertionError('Negative control was accepted')

def snap(report,frame):
 row=next(r for r in report.get('read_only_capture_RAM_snapshots',[])+report.get('read_only_pause_RAM_snapshots',[])if r['frame']==frame);raw=Path(row['path']).read_bytes();assert row['read_only_export']and sha(raw)==row['sha256'];return raw,row

if __name__=='__main__':
 assert not ROOT.exists();history=read(OLD);oldpath=Path(history['candidate']);assert sha(oldpath.read_bytes())==history['candidate_sha256'];oldrom=NdsImage.open(oldpath);rompath=Path('out/all_routes_combined_v2284_candidate.nds');rom=NdsImage.open(rompath);arm=rom.read_file('/__arm9__.bin');oldarm=oldrom.read_file('/__arm9__.bin');entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm);oldentries=historical_entries(oldrom.read_file('/COMMON/MESFILE.DK4'),oldarm);rows={r['message_id']:r for r in read('translations/battle_personal_contextual_editorial_manuscript_v1.json')['records']};assert all(entries[n].text==oldentries[n].text==compiled(r)for n,r in rows.items());assert rom.read_file('/GRP/KANJI.FNT')==oldrom.read_file('/GRP/KANJI.FNT');spans=((0x11000,0x20000),(0x3F0F8,0x3F100),(0x53914,0x53AC4),(0x7F244,0x7F268),(0x81F54,0x82E0C));assert all(arm[a:b]==oldarm[a:b]for a,b in spans)
 hold=FunctionType(original_hold.__code__,{**original_hold.__globals__,'actual_view':actual_view,'layout':layout},'current_code_on_historical_battle_RAM');holds=[];scopes=[];controls=[];returns=[];panels=[];return_panels=[];records=[]
 for label,(number,baseline,frames,first_back,end)in SPECS.items():
  receipt=next(r for r in history['terminal_capture_receipts']if Path(r['report']).parent.name.endswith('_'+label));rp=Path(receipt['report']);assert sha(rp.read_bytes())==receipt['sha256'];report,shots,verified=load(rp.parent,history['candidate_sha256'],end);assert report['cold_boot']and not report['savestate_loaded']and not report['callback_errors'];donor=report['battery_save_preloaded'];assert sha(Path(donor['source']).read_bytes())==donor['source_sha256'];fixture=report['synthetic_battle_personal_Cabin_assignment_fixtures'];approaches=report['synthetic_battle_recovery_proximity_fixtures'];assert len(fixture)==1 and len(approaches)==2;fixture=fixture[0];assert fixture['actor_ID']==rows[number]['actor_ID']and len(fixture['changes'])==(2 if label=='Joakim'else 1)and fixture['all_other4MiB_RAM_including_battle_mode_actor_captain_health_money_calendar_RNG_text_code_exact']
  for f in approaches:assert f['action']=='approach'and len(f['owned_bytes'])==8 and f['no_enemy_stats_war_outcome_reward_inventory_or_resource_flags_changed']and f['actual_battle_mode_not_assigned_by_fixture']and f['source_helpers_unchanged']and all(c['address']in f['owned_bytes']for c in f['changes'])
  before,before_receipt=snap(report,baseline);before_state=model_state(arm,before);initial,_=snap(report,4800);u,g=get_machine(arm,initial);mode=g(0x3F0F8);assert list(struct.unpack('<2I',u.mem_read(mode+8,8)))==[0,0];captain_bytes=None
  for frame in frames:
   raw,rrec=snap(report,frame);u,g=get_machine(arm,raw);mode=g(0x3F0F8);assert list(struct.unpack('<2I',u.mem_read(mode+8,8)))==[0,1]and g(0x7F244)==1;case=hold(rom,raw,shots[frame],rows[number],12);assert case['native_image_header_first_word_with_flags_preserved']==0x0E04 and model_state(arm,raw)==before_state;captain=g(0xCB184)+struct.unpack_from('<I',arm,0x1229C)[0];current=raw[captain-BASE:captain-BASE+32]
   if captain_bytes is None:captain_bytes=current
   assert current==captain_bytes;case.update(case=label,frame=frame,historical_V893_capture_current_code_text_and_pixels_bound=True,source_RAM=rrec,source_report=verified,original_battle_mode_not_injected_by_fixture=True,not_new_current_gameplay=True);holds.append(case);panel=Image.new('RGB',(256,412),'#263238');ImageDraw.Draw(panel).text((4,4),f'Historical V893 {label} {frame}',fill='white');panel.paste(shots[frame],(0,28));panels.append(panel)
  back,_=snap(report,first_back);after,arec=snap(report,end);assert model_state(arm,back)==before_state and rejected(lambda:actual_view(after));after_state=model_state(arm,after);assert after_state['funds']==before_state['funds']and after_state['all31_original_occupant_bytes']==before_state['all31_original_occupant_bytes']and after_state['calendar_tick']>before_state['calendar_tick'];returns.append(dict(case=label,first_back=first_back,return_frame=end,UI_open_and_first_back_scoped_state_equal=True,actual_captain32_bytes_equal_between_holds=True,assignments_and_funds_restored_or_unchanged_on_return=True,original_battle_time_resumes=True,world_ship_and_RNG_state_not_claimed_frozen_after_combat_resumes=True,return_RAM=arec));panel=Image.new('RGB',(256,412),'#263238');ImageDraw.Draw(panel).text((4,4),f'Historical V893 {label} return',fill='white');panel.paste(shots[end],(0,28));return_panels.append(panel)
  raw,_=snap(report,frames[0]);view,parent,res,h=actual_view(raw);bad=bytearray(raw);struct.pack_into('<I',bad,res-BASE,0x0E05);assert rejected(lambda:actual_view(bytes(bad)));controls.append(dict(case=label,negative='wrong-format-low-byte',rejected=True,offline_clone_only=True))
  if label in('Carlo','Julio'):
   x=6 if label=='Carlo'else(len(layout(rows[number]['english'])[1])-1)*6;bad=bytearray(raw);start=((res+h[4])&0xFFFFFFFF)-BASE
   for y in range(72,83):bad[start+y*126+x//2:start+y*126+x//2+3]=b'\0'*3
   assert rejected(lambda:hold(rom,bytes(bad),shots[frames[0]],rows[number],12));controls.append(dict(case=label,negative='deleted-leading-N'if label=='Carlo'else'deleted-final-exclamation',rejected=True,offline_clone_only=True))
  scopes.append(dict(case=label,report=str(rp),report_sha256=sha(rp.read_bytes()),source_battery=donor['source'],source_battery_sha256=donor['source_sha256'],historical_Cabin_occupant_fixture=fixture,historical_two8byte_source_terrain_checked_approaches=approaches,no_battle_mode_health_actor_captain_code_text_enemy_outcome_or_reward_fixture=True,not_earned_assignment_recruitment_travel_or_current_gameplay=True))
 # Locate the already-proven ordinary Carlo body by its independent bitmap,then
 # require the full current numeric/parent/RGB hold checks before accepting it.
 ordinary=history['original_ordinary1380_versus_battle1590_discriminating_actual_control'];orp=Path(ordinary['source_report']);assert sha(orp.read_bytes())==ordinary['source_report_sha256'];orpt=read(orp);oc=ordinary['actual_ordinary_hold'];orow=dict(message_id=1380,actor_ID=19,english=oc['complete_English']);assert entries[1380].text==oldentries[1380].text==ordinary_compiled(orow);lines=ordinary_layout(orow['english']);assert lines==oc['visible_lines'];events=[dict(kind='ascii',code=ord(c),style=15,x=x*6,y=60+y*12)for y,line in enumerate(lines)for x,c in enumerate(line)];pixels=expected_pixels(arm,rom.read_file('/GRP/KANJI.FNT'),events,4,background=0);expected=b''.join(pixels[y*128:y*128+126]for y in range(60,96));ordinary_hold=FunctionType(original_hold.__code__,{**original_hold.__globals__,'actual_view':actual_view,'layout':ordinary_layout},'current_ordinary_on_historical_RAM');ordinary_bound=None
 for rrec in orpt.get('read_only_capture_RAM_snapshots',[])+orpt.get('read_only_pause_RAM_snapshots',[]):
  raw=Path(rrec['path']).read_bytes();view=oc['actual_view'];res=struct.unpack_from('<I',raw,view-BASE+0x50)[0]
  if not BASE<=res<BASE+len(raw)-20:continue
  h=struct.unpack_from('<5I',raw,res-BASE);start=((res+h[4])&0xFFFFFFFF)-BASE
  if h[0]not in(4,0x1404,0x0E04)or not 0<=start< len(raw)-96*126 or raw[start+60*126:start+96*126]!=expected:continue
  assert sha(raw)==rrec['sha256']and rrec['read_only_export'];shot=next(r for r in orpt['frames_captured']if r['frame']==rrec['frame']);sp=Path(shot['path']);assert sha(sp.read_bytes())==shot['PNG_sha256'];im=Image.open(sp).convert('RGB');case=ordinary_hold(rom,raw,im,orow,12);u,g=get_machine(arm,raw);mode=g(0x3F0F8);assert list(struct.unpack('<2I',u.mem_read(mode+8,8)))!=[0,1];ordinary_bound=dict(frame=rrec['frame'],hold=case,source_RAM=rrec,source_report=str(orp),source_report_sha256=sha(orp.read_bytes()),same_source_actor19_selects_ordinary1380_not_battle1590=True,context_only_no_duplicate_credit=True);panel=Image.new('RGB',(256,412),'#263238');ImageDraw.Draw(panel).text((4,4),f'Historical ordinary Carlo {rrec["frame"]}',fill='white');panel.paste(im,(0,28));return_panels.append(panel);break
 assert ordinary_bound is not None and len(holds)==6 and {c['message_id']for c in holds}=={1572,1577,1590}and len(controls)==5 and len(returns)==3
 ROOT.mkdir(parents=True);sheet=Image.new('RGB',(768,824),'#263238')
 for i,panel in enumerate(panels):sheet.paste(panel,(i//2*256,i%2*412))
 p=ROOT/'historical_battle6_sheet.png';sheet.save(p);back=Image.new('RGB',(1024,412),'#263238')
 for i,panel in enumerate(return_panels):back.paste(panel,(i*256,0))
 b=ROOT/'historical_three_returns_and_ordinary_control.png';back.save(b)
 save(ROOT/'historical_battle_current_binding.json',dict(candidate=str(rompath),candidate_sha256=sha(rompath.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(rom.read_file('/COMMON/MESFILE.DK4')),historical_proof=str(OLD),historical_proof_sha256=sha(OLD.read_bytes()),all25_complete_payloads_exact_to_historical_V893=True,executed_selector_Deck_font_macro_and_role_code_spans_byte_exact=[dict(start=a,end=z,sha256=sha(arm[a:z]))for a,z in spans],historical_holds=holds,historical_IDs=[1572,1577,1590],all6_current_native_numeric_selector_parent_bitmap_RGB_and_complete_word_checks_on_historical_RAM_pass=True,native0E04_format_flags_preserved_low_byte4_not_rewritten=True,scoped_historical_battle_returns_freshly_rechecked=returns,historical_ordinary_Carlo_control_current_bound=ordinary_bound,five_negative_controls_current_reexecution_on_offline_clones=controls,historical_reports_and_fixture_scopes=scopes,all25_current_native_fonts_are_separate='work/analysis/battle_personal_fonts_v2384/all25_current_native_fonts.json',current_ordinary_Gunnery_shared_parent_control_not_battle_visit='work/analysis/gunnery_current_verification_v2376b/ordinary_current_Gunnery_actual.json',no_new_current_battle_emulator_runs_or_family_visits=True,no_earned_campaign_or_fleet_recruitment_or_battle_outcome_claim=True,review_sheets=[dict(path=str(p),sha256=sha(p.read_bytes())),dict(path=str(b),sha256=sha(b.read_bytes()))],visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(historical_battle_holds=6,current_bound_ordinary_control=ordinary_bound['frame'],current_rechecked_returns=3,negative_controls=5,new_current_emulator_runs=0,visual_pending=True))
