"""Replay terminal six-type navigation with the same declared prerequisites."""

import argparse,json,subprocess,sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/letter_eligibility_v790')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',default='letter_eligibility_v790_baseline')
    parser.add_argument('--phase-control',action='store_true')
    args=parser.parse_args()
    src=CAP/'letter_eligibility_v790_live';report=read(src/'capture_report.json')
    journal=read(src/'navigation_command_journal.json')['commands_received']
    assert report['frames']==24000 and journal[-1]['command'].get('stop')
    assert all(r['validation_passed'] for r in journal)
    out=CAP/args.out;assert not out.exists()
    frames=sorted({r['frame'] for r in report['frames_captured']})
    runner='scripts/run_letter_phase_v790.py' if args.phase_control else 'scripts/run_letter_eligibility_v790.py'
    command=[sys.executable,runner,'--rom','out/all_routes_combined_v783_candidate.nds',
        '--out',str(out),'--frames','24000','--inputs-json',str(ROOT/'initial_inputs.json'),
        '--battery-save',report['battery_save_preloaded']['source'],'--touchscreen','--capture-every','99999',
        '--capture-at',*map(str,frames),'--dump-capture-ram','--dump-pause-ram','--dump-ram',
        '--pause-at','3200','--allow-condition-fixtures']
    stdin='\n'.join(json.dumps(r['command']) for r in journal)+'\n'
    save(ROOT/(args.out+'_plan.json'),{'source_report_sha256':sha((src/'capture_report.json').read_bytes()),
        'command':command,'stdin_commands':stdin,'not_completion_evidence':True})
    with (ROOT/(args.out+'.log')).open('w',encoding='utf-8') as log:
        done=subprocess.run(command,input=stdin,text=True,encoding='utf-8',stdout=log,stderr=subprocess.STDOUT)
    assert done.returncode==0
    final=read(out/'capture_report.json')
    assert final['frames']==24000 and final['scripted_input_schedule']==report['scripted_input_schedule']
    print('Original-ROM exact six-type schedule replay terminal at24000 frames.',flush=True)


if __name__=='__main__':main()
