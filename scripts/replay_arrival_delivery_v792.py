"""Exact prior arrival journal and ordinary New Game controls on registered V792."""

import json
import subprocess
import sys
from pathlib import Path

from dk4tool.patch.arrival_notices_editorial import ROOT
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def main():
    parent=CAP/'letter_delivery_v791_recovered';rep=read(parent/'capture_report.json')
    journal=read(parent/'navigation_command_journal.json')['commands_received']
    assert rep['frames']==20000 and journal[-1]['command']=={'stop':True} and all(r['validation_passed'] for r in journal)
    out=CAP/'arrival_v792_delivery';assert not out.exists()
    frames=sorted({r['frame'] for r in rep['frames_captured']})
    cmd=[sys.executable,'scripts/run_arrival_delivery_v792.py','--rom','out/all_routes_combined_v792_candidate.nds',
        '--out',str(out),'--frames','56000','--inputs-json','work/analysis/letter_delivery_v791/initial_inputs.json',
        '--battery-save',rep['battery_save_preloaded']['source'],'--touchscreen','--capture-every','99999',
        '--capture-at',*map(str,frames),'--dump-capture-ram','--dump-pause-ram','--dump-ram','--pause-at','3200','--allow-condition-fixtures']
    stdin='\n'.join(json.dumps(r['command']) for r in journal)+'\n'
    save(ROOT/'delivery_replay_plan.json',{'source_report_sha256':sha((parent/'capture_report.json').read_bytes()),'command':cmd,
        'stdin_commands':stdin,'not_completion_evidence':True})
    with (ROOT/'delivery_replay.log').open('w',encoding='utf-8') as log:
        done=subprocess.run(cmd,input=stdin,text=True,encoding='utf-8',stdout=log,stderr=subprocess.STDOUT)
    assert done.returncode==0 and read(out/'capture_report.json')['frames']==20000
    print('Revised arrival sequence terminal at20000 frames.',flush=True)
    old=read(CAP/'item_v788_newgame/capture_report.json');out=CAP/'arrival_v792_newgame';assert not out.exists()
    inputs=ROOT/'newgame_inputs.json';save(inputs,old['scripted_input_schedule'])
    cmd=[sys.executable,'scripts/headless_desmume_v193.py','--rom','out/all_routes_combined_v792_candidate.nds',
        '--out',str(out),'--frames','4000','--inputs-json',str(inputs),'--capture-every','99999','--capture-at','1600','2000','3200','4000']
    with (ROOT/'newgame.log').open('w',encoding='utf-8') as log:done=subprocess.run(cmd,text=True,encoding='utf-8',stdout=log,stderr=subprocess.STDOUT)
    assert done.returncode==0 and read(out/'capture_report.json')['frames']==4000
    print('Ordinary fresh New Game control terminal at4000 frames.',flush=True)


if __name__=='__main__':main()
