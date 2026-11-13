"""Current ordinary Gerhard Shipwright1387:source selector,complete pixels andcancel."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.finish_refit_display_v712 import load
from scripts.work_comments_layout_v843 import compiled,layout
from scripts.verify_personal_gameplay_v841 import hold as original_hold,model_state
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/work_current_verification_v2311');CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/work_current_v2310_V2284');ROM=Path('out/all_routes_combined_v2284_candidate.nds')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);rom=NdsImage.open(ROM);digest=sha(ROM.read_bytes());arm=rom.read_file('/__arm9__.bin');entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm);report,shots,receipt=load(CAP,digest,5401);assert read('work/analysis/work_current_run_v2310/terminal.json')['terminal']and not any(v for k,v in report.items()if k.startswith('synthetic_'));assert report['battery_save_preloaded']['source_sha256']=='febc859c5af2df6fa8023c349bb7f31b5fc15ea769fb2eea527b3a3f80521731';ram={}
 for snapshot in report['read_only_capture_RAM_snapshots']:raw=Path(snapshot['path']).read_bytes();assert sha(raw)==snapshot['sha256']and snapshot['read_only_export'];ram[snapshot['frame']]=raw
 row=next(r for r in read('translations/work_contextual_editorial_manuscript_v1.json')['records']if r['message_id']==1387);row={**row,'actor_ID':16};assert entries[1387].text==compiled(row);hold=FunctionType(original_hold.__code__,{**original_hold.__globals__,'layout':layout},'current_work_hold');holds=[]
 for frame in(4600,4800):case=hold(rom,ram[frame],shots[frame],row,13);assert case['source_role_type']==13 and case['original_parent_activity_state']==0;case.update(frame=frame,current_V2284_ordinary_assignment_no_new_fixture=True);holds.append(case)
 states=[dict(frame=f,state=model_state(arm,ram[f]))for f in(3800,4600,4800,5400)];assert states[0]['state']==states[-1]['state'];before=bytes.fromhex(states[0]['state']['all31_original_occupant_bytes']);assert before[7]==16 and before[13]==208
 for state in states[1:3]:
  assert all(state['state'][k]==states[0]['state'][k]for k in states[0]['state']if k!='all31_original_occupant_bytes');occupants=bytes.fromhex(state['state']['all31_original_occupant_bytes']);assert occupants[7]==208 and occupants[13]==16 and all(a==b for i,(a,b)in enumerate(zip(before,occupants,strict=True))if i not in(7,13))
 selected=[3200,3400,3800,4000,4400,4600,4800,5400];sheet=Image.new('RGB',(1024,824),'#263238');draw=ImageDraw.Draw(sheet)
 for i,f in enumerate(selected):x,y=i%4*256,i//4*412;draw.text((x+4,y+4),f'V2284 ordinary Shipwright {f}',fill='white');sheet.paste(shots[f],(x,y+28))
 p=ROOT/'ordinary_Gerhard_Shipwright_and_return.png';sheet.save(p);save(ROOT/'ordinary_current_Shipwright_actual.json',dict(candidate=str(ROM),candidate_sha256=digest,actual_report=receipt,actual_complete_holds=holds,current_message_IDs=[1387],native_actor_ID=16,actual_source_role13_slot13_and_original_whole12104_selector_verified=True,all252x36_native_bitmaps_and216x36_actual_RGB_foreground_blank_ink_equal=True,native_source_parent_projection_complete_first_final_letters_and_words_verified=True,ordinary_input_selection_moves_Gerhard_from_slot7_to13_only=True,all31_assignment_bytes_restored_after_cancel=True,all_other_scoped_fields_unchanged_across4_checkpoints=True,four_scoped_state_checkpoints=states,no_RAM_code_text_health_location_timing_role_or_RNG_fixture_or_savestate=True,inherited_five_ship_test_battery_no_earned_ownership_or_fleet_claim=True,other23_new_current_visits_not_claimed=True,review_sheet=str(p),review_sheet_sha256=sha(p.read_bytes()),visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(current_actual_holds=2,IDs=[1387],actor16=True,native_role13=True,ordinary_return_restores_all_roles=True,new_fixtures=0,visual_pending=True))
