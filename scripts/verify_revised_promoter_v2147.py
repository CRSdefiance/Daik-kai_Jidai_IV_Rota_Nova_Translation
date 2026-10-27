"""Bind actual four-line RGB to unchanged logical compact control and separate physical oracle."""
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.verify_village_wrap_v608 import read,save
from scripts.primary_town_native_font_v2102 import font_tools,glyph_codes
from scripts.verify_shipyard_gameplay_v760 import independent_font
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/square_revised_actual_v2147');RUN=Path('work/analysis/promoter_context_actual_v2144');CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/promoter_context_live_v2144_V2143')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 plan,terminal,report,obs=[read(p)for p in(RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',CAP/'common_observer/requests.json')]
 assert terminal['terminal']and terminal['all_observer_host_slots_restored']and report['frames']==6501 and report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']and not obs['errors']and not obs['mismatches']and obs['all_host_slots_restored_and_core_file_exact']
 assert sha(Path(plan['candidate']).read_bytes())==plan['candidate_sha256']==report['ROM_sha256'];assert sha(Path(plan['original_genuine_save']).read_bytes())==plan['donor_sha256']
 rom=NdsImage.open(plan['candidate']);arm=rom.read_file('/__arm9__.bin');kanji=rom.read_file('/GRP/KANJI.FNT');raster,_,_=font_tools(rom);frames={r['frame']:r for r in report['frames_captured']};holds=[]
 continuations=read('work/analysis/square_revised_continuations_v2147/actual_snapshot_native_font_continuations.json')
 for row,f in zip(obs['rows'],(3800,4200,4600,5000),strict=True):
  n=row['source_request']['ID'];assert row['bounds']==[0,0,228,48] and row['font_input_offset']in(0,2)
  native=next(r for r in continuations['cases']if r['message_ID']==n);assert native['complete_native_return']and native['SP_preserved']and native['callee_registers_preserved']and not native['faults']and not native['error']
  text=bytes.fromhex(row['text_hex']);events=[];plane=raster(arm,text,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000,glyph_events=events)
  lines=[s.strip().decode('cp932')for s in text.split(b'\n')];assert plane==independent_font(arm,kanji,lines)and[e['code']for e in events if e['code']!=32]==glyph_codes(text)
  image=Image.open(frames[f]['path']).convert('RGB');assert sha(Path(frames[f]['path']).read_bytes())==frames[f]['PNG_sha256']
  expected={(16+j%228,296+j//228)for j,v in enumerate(plane)if v==1};actual={(x,y)for y in range(294,360)for x in range(16,244)if image.getpixel((x,y))==(0,8,0)};assert expected==actual,(n,f,len(expected-actual),len(actual-expected))
  holds.append(dict(message_ID=n,font_frame=row['frame'],hold_frame=f,text_hex=row['text_hex'],capture=frames[f]['path'],capture_sha256=frames[f]['PNG_sha256'],lines=lines,logical_native_row_origins=sorted({e['y']for e in native['glyph_events']}),physical_oracle_row_origins=sorted({e['y']for e in events}),every_actual_foreground_pixel_equal=True,physical_oracle_64_plane_not_logical_view_size=True))
 assert [r['message_ID']for r in holds]==[675,676,739,740]and len(holds[2]['lines'])==4
 oldcap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/promoter_context_live_v2136_V2097');oldreport=read(oldcap/'capture_report.json');oldframes={r['frame']:r for r in oldreport['frames_captured']};controls=[]
 for f,r in frames.items():
  old=Image.open(oldframes[f]['path']).convert('RGB');new=Image.open(r['path']).convert('RGB');assert sha(Path(oldframes[f]['path']).read_bytes())==oldframes[f]['PNG_sha256']
  if f<4826:assert new.tobytes()==old.tobytes();scope='whole-frame'
  else:
   a,b=old.copy(),new.copy();a.paste((255,0,255),(16,294,244,360));b.paste((255,0,255),(16,294,244,360));assert a.tobytes()==b.tobytes();scope='every-pixel-outside-revised-body'
  controls.append(dict(frame=f,scope=scope,exact_to_V2097=True,current_capture_sha256=r['PNG_sha256'],prior_capture_sha256=oldframes[f]['PNG_sha256']))
 from scripts.verify_market_gameplay_v753 import state
 from scripts.verify_shipyard_gameplay_v760 import models
 from scripts.verify_personal_gameplay_v841 import get_machine
 import struct
 states=[]
 def snapshots(r):
  q={x['frame']:x for x in r['read_only_capture_RAM_snapshots']};q.update({x['frame']:x for x in r['read_only_pause_RAM_snapshots']});return q
 current_snaps,prior_snaps=snapshots(report),snapshots(oldreport)
 for f in(3200,5000,6501):
  a,b=[Path(q[f]['path']).read_bytes()for q in(current_snaps,prior_snaps)]
  assert sha(a)==current_snaps[f]['sha256']and sha(b)==prior_snaps[f]['sha256'];current_state,old_state=state(arm,a),state(arm,b);current_models,old_models=models(arm,a),models(arm,b);assert current_state==old_state and current_models==old_models
  cpu,get=get_machine(arm,a);player=get(0xCB184);flag=struct.unpack_from('<I',a,player+0x1A4C-0x02000000)[0];assert bool(flag&4)==(f!=3200)
  states.append(dict(frame=f,state=current_state,models=current_models,promoter_travel_flag=flag,exact_to_V2097=True,current_RAM_sha256=sha(a),prior_RAM_sha256=sha(b)))
 assert len(report['synthetic_promoter_travel_fixtures'])==1 and len(report['synthetic_promoter_travel_fixtures'][0]['changes'])==4
 journal=read(CAP/'navigation_command_journal.json');assert journal['commands_received'][-1]['command']=={'stop':True}
 sheet=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(sheet)
 for i,r in enumerate(holds):draw.text((i*256+4,4),f"ID{r['message_ID']} frame{r['hold_frame']}",fill='white');sheet.paste(Image.open(r['capture']).convert('RGB'),(i*256,22))
 p=ROOT/'four_actual_compact_holds.png';sheet.save(p)
 save(ROOT/'revised_promoter_and_preservation.json',dict(candidate=plan['candidate'],candidate_sha256=plan['candidate_sha256'],actual_holds=holds,frames=6501,frame_controls=controls,native_state_model_controls=states,complete_acceptance_flag_and_UI_transitions=True,production_logical_view=[228,48],production_font_metrics=[6,12],physical_pixel_oracle_pitch=16,geometry_word_02118ACC_unchanged_48=True,native_continuation_receipt='work/analysis/square_revised_continuations_v2147/actual_snapshot_native_font_continuations.json',four_byte_promoter_fixture_declared_not_naturally_earned=True,original_genuine_save_unchanged=True,all_host_slots_restored=True,actual_revised_740_full_hold=True,not_full_playthrough_or_hardware_verification=True,physical_64_oracle_is_not_a_capacity_rule=True,geometry_research_2128_not_approved_for_release=True,pagination_2115_2103b_2125b_scope_correction='16-metric linear 48-plane modeled three rows;production12-metric48-logical-view consumes four.307 corrected cases all single native page.',review_sheet=str(p),review_sheet_sha256=sha(p.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(holds=len(holds),four_line_739_complete=True,logical_geometry_unchanged=True,sheet=str(p)))
