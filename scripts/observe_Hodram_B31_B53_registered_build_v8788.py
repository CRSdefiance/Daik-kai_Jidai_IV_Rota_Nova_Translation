"""Record the specific live registered-builder process tree; status is scoped to observation time."""
import json,subprocess
from datetime import datetime,timezone
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_build_observation_v8788')
PLAN=Path('work/analysis/Hodram_B31_B53_build_v8778/build_plan.json')
TERMINAL=PLAN.with_name('build_terminal.json')
if __name__=='__main__':
    assert not ROOT.exists() and not TERMINAL.exists();plan=read(PLAN);wrapper=plan['PID']
    query=f"Get-CimInstance Win32_Process -Filter 'ProcessId={wrapper} OR ParentProcessId={wrapper}' | Select-Object ProcessId,ParentProcessId,CommandLine | ConvertTo-Json -Depth 3"
    result=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,encoding='utf-8',check=True)
    processes=json.loads(result.stdout.lstrip('\ufeff'));assert isinstance(processes,list)
    parent=next(p for p in processes if p['ProcessId']==wrapper)
    children=[p for p in processes if p['ParentProcessId']==wrapper and 'scripts/build_integrated_release.py' in p['CommandLine']]
    assert 'scripts.build_Hodram_B31_B53_v8778' in parent['CommandLine'] and len(children)==1
    child=children[0];assert '--profile all-routes-unified-v8778' in child['CommandLine'] and 'all_routes_combined_v8778_candidate.nds' in child['CommandLine']
    assert not TERMINAL.exists()
    ROOT.mkdir(parents=True);save(ROOT/'qualified_live_observation.json',dict(observed_UTC=datetime.now(timezone.utc).isoformat(),exec_session=90938,
        wrapper_PID=wrapper,builder_PID=child['ProcessId'],confirmed_live_at_observation=True,native_processes=processes,
        plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),terminal_absent_at_observation=True,
        native_process_tree_matches_exact_plan_wrapper_profile_andcandidate=True,
        running_claim_only_at_observation_not_future_orcompletion=True,no_restart_ornew_build=True,
        new_credit=0,full_goal_complete=False,evidence={str(p):sha(Path(p).read_bytes()) for p in [PLAN,Path(__file__)]}))
    print('Confirmed live:session90938/wrapper'+str(wrapper)+'/builder'+str(child['ProcessId'])+';terminal absent atobservation. Pollsame handle;no restart.',flush=True)
