"""Actual current system267: its own geometry, direct font call and complete foreground."""
from pathlib import Path
from PIL import Image
from scripts.verify_village_wrap_v608 import read,save
from scripts.primary_town_native_font_v2102 import font_tools,glyph_codes
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_market_gameplay_v753 import state
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/yard_modal_actual_verification_v2158');RUN=Path('work/analysis/town_yard_actual_v2156');CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_yard_live_v2156b_V2143')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);plan,terminal,report,obs=[read(p)for p in(RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',CAP/'common_observer/requests.json')]
 assert terminal['terminal']and terminal['all_observer_host_slots_restored']and report['frames']==6401 and report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']and not obs['errors']and not obs['mismatches']and obs['all_host_slots_restored_and_core_file_exact']
 assert not any(v for k,v in report.items()if k.startswith('synthetic_'))and sha(Path(plan['candidate']).read_bytes())==plan['candidate_sha256']==report['ROM_sha256']and sha(Path(plan['original_genuine_save']).read_bytes())==plan['donor_sha256']
 assert len(obs['rows'])==1;row=obs['rows'][0];assert row['source_request']['ID']==267 and row['bounds']==[0,0,228,48]and row['distinct_system_modal']and row['font_input_offset']==0
 native=read('work/analysis/yard_modal_font_v2158/actual_snapshot_native_font_continuations.json')['cases'][0];assert native['message_ID']==267 and native['complete_native_return']and native['SP_preserved']and native['callee_registers_preserved']and not native['faults']and not native['error'];text=bytes.fromhex(row['text_hex']);assert[e['code']for e in native['glyph_events']if e['code']!=32]==glyph_codes(text)and native['glyph_events'][0]['x']==0 and{e['y']for e in native['glyph_events']}=={0}
 rom=NdsImage.open(plan['candidate']);arm=rom.read_file('/__arm9__.bin');raster,_,_=font_tools(rom);events=[];plane=raster(arm,text,0xD5404,size=(228,64),instruction_limit=2000000,glyph_events=events);font=GameAsciiFont.from_arm9(arm);expected=bytearray(228*64)
 for i,ch in enumerate(text.decode('ascii')):
  glyph=font.decode(ch)
  for y in range(11):
   for x in range(6):
    if glyph.getpixel((x,y)):expected[y*228+i*6+x]=1
 assert plane==bytes(expected)and[e['code']for e in events if e['code']!=32]==glyph_codes(text)
 frames={r['frame']:r for r in report['frames_captured']};hold=frames[4600];image=Image.open(hold['path']).convert('RGB');assert sha(Path(hold['path']).read_bytes())==hold['PNG_sha256'];pixels={(16+i%228,296+i//228)for i,v in enumerate(plane)if v==1};actual={(x,y)for y in range(294,360)for x in range(16,244)if image.getpixel((x,y))==(0,8,0)};assert pixels==actual
 snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']};states=[]
 for f in(3200,4600,6400):
  s=snapshots[f];raw=Path(s['path']).read_bytes();assert sha(raw)==s['sha256'];states.append(dict(frame=f,state=state(arm,raw),models=models(arm,raw),snapshot=s))
 assert all(r['state']==states[0]['state']and r['models']==states[0]['models']for r in states)
 out=ROOT/'actual267_complete_hold.png';image.save(out)
 save(ROOT/'actual267_native_geometry_direct_font_and_foreground.json',dict(candidate=plan['candidate'],candidate_sha256=plan['candidate_sha256'],message_ID=267,frames=6401,font_frame=row['frame'],hold_frame=4600,text_hex=text.hex(),actual_bounds=row['bounds'],production_font_row_pitch=12,first_glyph_x=0,direct_native_font_entry=row['PC'],actual_font_call_return=row['LR'],complete_native_actual_continuation=True,complete_independent_physical_font_plane_and_all_actual_foreground_pixels_equal=True,all_leading_trailing_letters_and_input_complete=True,native_state_model_controls=states,no_ship_sale_or_world_state_change=True,ordinary_Yard_selection_refusal_dismissal_and_return_captured=True,no_savestate_or_any_synthetic_fixture=True,original_genuine_donor_and_core_unchanged_and_host_slots_restored=True,old240pixel_offline_canvas_does_not_establish_actual_view_width=True,no_new_geometry_or_runtime_change=True,capture=hold,review_image=str(out),review_image_sha256=sha(out.read_bytes()),source_observer=str(CAP/'common_observer/requests.json'),source_observer_sha256=sha((CAP/'common_observer/requests.json').read_bytes()),native_continuation='work/analysis/yard_modal_font_v2158/actual_snapshot_native_font_continuations.json',only267_actual_visit_claimed_other61_paths_offline_or_pending=True,not_full_playthrough_or_hardware_verification=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(actual267='complete',logical_bounds=row['bounds'],first_glyph_x=0,state_controls=3,frames=6401,review_image=str(out)))
