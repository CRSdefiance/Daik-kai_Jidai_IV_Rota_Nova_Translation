"""Current ordinary Charles Cabin holds, original selector/projection and return."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.finish_refit_display_v712 import load
from scripts.personal_chatter_layout_v837 import compiled
from scripts.verify_personal_gameplay_v841 import hold,model_state
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/personal_current_verification_v2302');CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/personal_current_v2301_V2284');ROM=Path('out/all_routes_combined_v2284_candidate.nds')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);rom=NdsImage.open(ROM);digest=sha(ROM.read_bytes());arm=rom.read_file('/__arm9__.bin');entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm);rpt,shots,receipt=load(CAP,digest,5401);assert read('work/analysis/personal_current_run_v2301/terminal.json')['terminal']and not any(v for k,v in rpt.items()if k.startswith('synthetic_'));assert rpt['battery_save_preloaded']['source_sha256']=='febc859c5af2df6fa8023c349bb7f31b5fc15ea769fb2eea527b3a3f80521731';ram={}
 for row in rpt['read_only_capture_RAM_snapshots']:
  raw=Path(row['path']).read_bytes();assert sha(raw)==row['sha256']and row['read_only_export'];ram[row['frame']]=raw
 doc=read('translations/personal_contextual_editorial_manuscript_v1.json');row=next(r for r in doc['records']if r['message_id']==1379);assert entries[1379].text==compiled(row);holds=[]
 for frame in(4600,4800):case=hold(rom,ram[frame],shots[frame],row,12);case.update(frame=frame,current_V2284_ordinary_capture=True);holds.append(case)
 states=[dict(frame=f,state=model_state(arm,ram[f]))for f in(3800,4600,4800,5400)];assert all(s['state']==states[0]['state']for s in states)
 selected=[3200,3400,3800,4000,4400,4600,4800,5400];sheet=Image.new('RGB',(1024,824),'#263238');draw=ImageDraw.Draw(sheet)
 for i,f in enumerate(selected):x,y=i%4*256,i//4*412;draw.text((x+4,y+4),f'V2284 ordinary Cabin {f}',fill='white');sheet.paste(shots[f],(x,y+28))
 p=ROOT/'ordinary_Charles_Cabin_and_return.png';sheet.save(p)
 save(ROOT/'ordinary_current_Cabin_actual.json',dict(candidate=str(ROM),candidate_sha256=digest,actual_report=receipt,actual_complete_holds=holds,current_message_IDs=[1379],native_actor_ID=18,actual_source_role_type12_and_original_whole12104_selector_verified=True,all_full252x36_bitmap_and216x36_RGB_complete_words_and_blank_pixels_equal=True,native_original_parent_projection_and_complete_first_final_glyphs_verified=True,owned_Charles_and_normal_room_selection_no_new_fixture=True,inherited_five_ship_Copenhagen_battery_not_earned_fleet_or_ownership_claim=True,four_scoped_state_checkpoints=states,all_funds_calendar31_roles_owned_companion_records_flagship_and_full_ship_models_equal=True,no_new_RAM_code_text_health_location_timing_or_role_fixture_or_savestate=True,counterfactual144x24_crop_is_CPU_only_not_actual_or_ROM_change=True,review_sheet=str(p),review_sheet_sha256=sha(p.read_bytes()),visual_review_pending=True,other24_current_visits_not_claimed=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(current_actual_holds=2,IDs=[1379],four_scoped_state_controls=True,new_fixtures=0,visual_pending=True))
