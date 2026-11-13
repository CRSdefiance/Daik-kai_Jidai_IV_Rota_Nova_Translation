"""Verify existing current ordinary Survey holds;reuse the shared run without replay."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from scripts.finish_refit_display_v712 import load
from scripts.survey_lookout_layout_v875 import compiled,layout
from scripts.verify_personal_gameplay_v841 import hold as original_hold,model_state
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/survey_current_verification_v2356');CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/bridge_current_v2346_V2284');ROM=Path('out/all_routes_combined_v2284_candidate.nds')
if __name__=='__main__':
 assert not ROOT.exists();rom=NdsImage.open(ROM);digest=sha(ROM.read_bytes());arm=rom.read_file('/__arm9__.bin');entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm);report,shots,receipt=load(CAP,digest,5401);assert read('work/analysis/bridge_current_run_v2346/terminal.json')['terminal']and not any(v for k,v in report.items()if k.startswith('synthetic_'));assert report['battery_save_preloaded']['source_sha256']=='febc859c5af2df6fa8023c349bb7f31b5fc15ea769fb2eea527b3a3f80521731';ram={}
 for snapshot in report['read_only_capture_RAM_snapshots']:raw=Path(snapshot['path']).read_bytes();assert sha(raw)==snapshot['sha256']and snapshot['read_only_export'];ram[snapshot['frame']]=raw
 row=next(r for r in read('translations/survey_lookout_contextual_editorial_manuscript_v1.json')['records']if r['message_id']==1500);row={**row,'actor_ID':16};assert entries[1500].text==compiled(row);hold=FunctionType(original_hold.__code__,{**original_hold.__globals__,'layout':layout},'current_survey_hold');holds=[]
 for frame in(4000,4200):
  case=hold(rom,ram[frame],shots[frame],row,7);assert case['source_role_type']==3 and case['original_parent_activity_state']==0;case.update(frame=frame,current_V2284_ordinary_selection_no_new_fixture=True,already_owned_actor16_in_original_Survey7=True);holds.append(case)
 states=[dict(frame=f,state=model_state(arm,ram[f]))for f in(3800,4000,4200,5400)];assert all(r['state']==states[0]['state']for r in states);assert bytes.fromhex(states[0]['state']['all31_original_occupant_bytes'])[7]==16
 bridgepath=Path('work/analysis/bridge_current_verification_v2348/ordinary_current_Mate_actual.json');bridge=read(bridgepath);assert bridge['candidate_sha256']==digest and bridge['current_message_IDs']==[1476]and bridge['all31_assignment_bytes_restored_after_cancel']and bridge['all_other_scoped_fields_unchanged_across4_checkpoints']
 ROOT.mkdir(parents=True);sheet=Image.new('RGB',(1024,824),'#263238');draw=ImageDraw.Draw(sheet)
 for i,f in enumerate((3200,3400,4000,4200,4400,4600,4800,5400)):
  x,y=i%4*256,i//4*412;draw.text((x+4,y+4),f'V2284 Survey then Mate/cancel {f}',fill='white');sheet.paste(shots[f],(x,y+28))
 p=ROOT/'ordinary_Gerhard_Survey_then_Mate_and_return.png';sheet.save(p)
 save(ROOT/'ordinary_current_Survey_actual.json',dict(candidate=str(ROM),candidate_sha256=digest,actual_report=receipt,actual_complete_holds=holds,current_message_IDs=[1500],native_actor_ID=16,actual_source_role3_slot7_and_original_whole12104_selector_verified=True,all252x36_native_bitmaps_and216x36_actual_RGB_foreground_blank_ink_equal=True,native_source_parent_projection_complete_first_final_letters_and_words_verified=True,already_owned_Gerhard_original_Survey7_assignment_unchanged_during_both_holds=True,all31_assignment_bytes_restored_after_cancel=True,all_other_scoped_fields_unchanged_across4_checkpoints=True,four_scoped_state_checkpoints=states,subsequent_Mate1476_transition_and_cancel_separately_bound=str(bridgepath),subsequent_Mate_proof_sha256=sha(bridgepath.read_bytes()),subsequent_Mate_preview_changes_only_slots7_and15_then_restores_all31=True,no_RAM_code_text_health_location_timing_role_or_RNG_fixture_or_savestate=True,inherited_five_ship_test_battery_no_earned_ownership_or_fleet_claim=True,reused_current_capture_no_new_emulator_run=True,other23_new_current_visits_not_claimed=True,review_sheet=str(p),review_sheet_sha256=sha(p.read_bytes()),visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(current_actual_holds=2,IDs=[1500],ordinary_Survey7=True,new_emulator_runs=0,subsequent_Mate_cancel_separately_bound=True,visual_pending=True))
