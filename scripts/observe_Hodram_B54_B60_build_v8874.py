"""Record authoritative process state; quiet output or an old state file is not a reason to restart."""
import json,subprocess
from datetime import datetime,timezone
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B54_B60_build_observation_v8874')
BUILD=Path('work/analysis/Hodram_B54_B60_build_v8865')
if __name__=='__main__':
    assert not ROOT.exists();plan=read(BUILD/'build_plan.json');pid=plan['PID']
    command="Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' -and ($_.ProcessId -eq "+str(pid)+" -or $_.ParentProcessId -eq "+str(pid)+") } | Select-Object ProcessId,ParentProcessId,CommandLine | ConvertTo-Json -Compress"
    result=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',command],capture_output=True,text=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
    values=json.loads(result.stdout) if result.stdout.strip() else [];values=values if isinstance(values,list) else [values]
    producers=[r for r in values if r['ProcessId']==pid and 'scripts.build_Hodram_B54_B60_v8865' in r['CommandLine']]
    children=[r for r in values if r['ParentProcessId']==pid and 'scripts/build_integrated_release.py' in r['CommandLine'] and '--profile all-routes-unified-v8865' in r['CommandLine']]
    terminal=BUILD/'build_terminal.json';state='live-registered-builder-andproducer' if producers and children else 'live-producer-terminal-receipt-pending' if producers else 'terminal' if terminal.exists() and read(terminal)['terminal'] else 'unresolved-repoll-same-exec-session'
    assert sha(Path('scripts/build_integrated_release.py').read_bytes())==plan['builder_sha256'] and sha(Path('translations/release_stack.json').read_bytes())==plan['registry_sha256']
    ROOT.mkdir(parents=True);save(ROOT/'authoritative_process_observation.json',dict(observed_UTC=datetime.now(timezone.utc).isoformat(),state=state,processes=values,exec_session_id=29114,producer_PID=pid,build_plan=str(BUILD/'build_plan.json'),build_plan_sha256=sha((BUILD/'build_plan.json').read_bytes()),terminal_receipt_exists=terminal.exists(),terminal_receipt=read(terminal) if terminal.exists() else None,quiet_log_not_failure_andno_relaunch=True,observation_is_not_future_liveness_repoll_specific_handle=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print(state,'exec29114',[(r['ProcessId'],r['ParentProcessId']) for r in values],flush=True)
