"""Replay the terminal arrival investigation against the preceding registered ROM."""

import json
import subprocess
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/letter_delivery_v791')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def main():
    folder=CAP/'letter_delivery_v791_recovered'
    report=read(folder/'capture_report.json')
    journal=read(folder/'navigation_command_journal.json')['commands_received']
    assert report['frames']==20000 and journal[-1]['command']=={'stop':True}
    assert all(r['validation_passed'] for r in journal)
    out=CAP/'letter_delivery_v791_baseline';assert not out.exists()
    frames=sorted({r['frame'] for r in report['frames_captured']})
    cmd=[sys.executable,'scripts/run_letter_delivery_v791.py','--rom','out/all_routes_combined_v783_candidate.nds',
         '--out',str(out),'--frames','56000','--inputs-json',str(ROOT/'initial_inputs.json'),
         '--battery-save',report['battery_save_preloaded']['source'],'--touchscreen','--capture-every','99999',
         '--capture-at',*map(str,frames),'--dump-capture-ram','--dump-pause-ram','--dump-ram',
         '--pause-at','3200','--allow-condition-fixtures']
    stdin='\n'.join(json.dumps(r['command']) for r in journal)+'\n'
    save(ROOT/'baseline_replay_plan.json',{'source_report_sha256':sha((folder/'capture_report.json').read_bytes()),
        'command':cmd,'stdin_commands':stdin,'not_completion_evidence':True})
    with (ROOT/'baseline_replay.log').open('w',encoding='utf-8') as log:
        done=subprocess.run(cmd,input=stdin,text=True,encoding='utf-8',stdout=log,stderr=subprocess.STDOUT)
    assert done.returncode==0
    final=read(out/'capture_report.json')
    assert final['frames']==20000 and final['scripted_input_schedule']==report['scripted_input_schedule']
    print('Original ROM delivery replay terminal at20000 frames.',flush=True)


if __name__=='__main__':main()
