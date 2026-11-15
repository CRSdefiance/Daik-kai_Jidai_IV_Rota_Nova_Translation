"""Ordinary Gerhard-to-Lumber input test in current V2284; no new RAM fixture."""
import sys
from copy import deepcopy
from pathlib import Path
from scripts import headless_desmume_v193 as harness
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/work_current_run_v2310');CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/work_current_v2310_V2284');ROM=Path('out/all_routes_combined_v2284_candidate.nds')
if __name__=='__main__':
 assert not ROOT.exists()and not CAP.exists();ROOT.mkdir(parents=True);prior=Path('E:/Rota Nova translations/Generated/work/emulation_v193/personal_current_v2301_V2284/capture_report.json');p=read(prior);schedule=deepcopy(p['scripted_input_schedule']);changed=[]
 for event in schedule:
  if event['start']==3801:assert event['touch']==[192,66];event['touch']=[104,66];changed.append(3801)
  elif event['start']==4201:assert event['touch']==[66,110];event['touch']=[104,110];changed.append(4201)
 assert changed==[3801,4201];donor=Path(p['battery_save_preloaded']['source']);assert sha(donor.read_bytes())=='febc859c5af2df6fa8023c349bb7f31b5fc15ea769fb2eea527b3a3f80521731';digest=sha(ROM.read_bytes());assert read(ROM.with_suffix('.manifest.json'))['candidate_sha256']==digest;inputs=ROOT/'ordinary_inputs.json';save(inputs,schedule);captures=[1,60,180,3200,*range(3400,5401,200)]
 save(ROOT/'run_plan.json',dict(candidate=str(ROM),candidate_sha256=digest,frames=5401,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),captures=captures,prior_ordinary_schedule=str(prior),prior_sha256=sha(prior.read_bytes()),two_touch_targets_changed=[dict(frame=3801,XY=[104,66],intended='current upper-deck Survey/Gerhard room'),dict(frame=4201,XY=[104,110],intended='current Lumber room next to Cabin')],intended_ID1387_not_assumed_until_actual_source_and_pixels_verified=True,source_battery=str(donor),source_battery_sha256=sha(donor.read_bytes()),inherited_test_fleet_not_earned_progress=True,no_new_RAM_code_health_role_location_timing_text_or_RNG_fixture=True,no_savestate=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','5401','--inputs-json',str(inputs),'--battery-save',str(donor),'--touchscreen','--capture-every','999999','--capture-at',*map(str,captures),'--dump-capture-ram','--dump-ram'];harness.main();assert sha(donor.read_bytes())=='febc859c5af2df6fa8023c349bb7f31b5fc15ea769fb2eea527b3a3f80521731';save(ROOT/'terminal.json',dict(terminal=True,frames=read(CAP/'capture_report.json')['frames'],new_RAM_fixtures=0,source_donor_unchanged=True,actual_ID_source_and_pixels_pending=True,full_goal_complete=False))
