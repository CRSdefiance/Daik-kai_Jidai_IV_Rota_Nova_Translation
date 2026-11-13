"""Also verify Charles1547 before the ordinary occupied-room preview."""
from pathlib import Path
from copy import deepcopy
from types import FunctionType
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.finish_refit_display_v712 import load
from scripts.gunnery_deck_layout_v887 import compiled,layout
from scripts.verify_personal_gameplay_v841 import hold as original_hold,model_state
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/gunnery_current_verification_v2376b');OLD=Path('work/analysis/gunnery_current_verification_v2376/ordinary_current_Gunnery_actual.json')
if __name__=='__main__':
 assert not ROOT.exists();d=read(OLD);rom=NdsImage.open(d['candidate']);assert sha(Path(d['candidate']).read_bytes())==d['candidate_sha256'];arm=rom.read_file('/__arm9__.bin');report,shots,receipt=load(Path('E:/Rota Nova translations/Generated/work/emulation_v193/gunnery_current_v2375_V2284'),d['candidate_sha256'],5401);r=next(s for s in report['read_only_capture_RAM_snapshots']if s['frame']==4400);raw=Path(r['path']).read_bytes();assert sha(raw)==r['sha256']and r['read_only_export'];row=next(r for r in read('translations/gunnery_deck_contextual_editorial_manuscript_v1.json')['records']if r['message_id']==1547);row={**row,'actor_ID':18};hold=FunctionType(original_hold.__code__,{**original_hold.__globals__,'layout':layout},'current_Charles_gunnery_hold');case=hold(rom,raw,shots[4400],row,9);assert case['source_role_type']==8 and case['original_parent_activity_state']==0;case.update(frame=4400,current_V2284_original_Charles_assignment_before_preview=True);state=model_state(arm,raw);assert state==d['four_scoped_state_checkpoints'][0]['state'];merged=deepcopy(d);merged['actual_complete_holds']=[case,*d['actual_complete_holds']];merged['current_message_IDs']=[1547,1548];merged['native_actor_IDs']=[18,16];merged['occupied_room_transition_focus_actor_ID']=merged.pop('native_actor_ID');merged.pop('other23_new_current_visits_not_claimed');merged['other22_new_current_visits_not_claimed']=True;merged.update(additional_4400_state_equal_to_initial_3800=state,current_Charles_then_Gerhard_occupied_room_preview_and_cancel_complete=True,original_two_Gerhard_holds_and_four_state_controls_preserved=str(OLD),original_proof_sha256=sha(OLD.read_bytes()),no_new_capture_or_emulator_run=True,extension_producer_sha256=sha(Path(__file__).read_bytes()))
 ROOT.mkdir(parents=True);save(ROOT/'ordinary_current_Gunnery_actual.json',merged);print(dict(current_IDs=[1547,1548],actual_complete_holds=3,Charles_initial_and_Gerhard_preview_verified=True,new_emulator_runs=0))
