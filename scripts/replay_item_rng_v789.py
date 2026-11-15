"""Identical existing schedule plus the explicit post-acknowledgment seed input."""

import argparse,json,subprocess,sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--version',type=int,choices=(783,788),required=True)
    args=parser.parse_args()
    root=Path('work/analysis/item_transactions_v789');cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
    original=cap/'item_roles_v789_live';report=read(original/'capture_report.json')
    commands=[r['command'] for r in read(original/'navigation_command_journal.json')['commands_received']]
    target=next(c for c in commands if c.get('until')==19200)
    assert 'condition_fixture' not in target
    target['condition_fixture']={'mode':'synchronize-post-acknowledgment-RNG'}
    stdin='\n'.join(json.dumps(c) for c in commands)+'\n'
    snapshots=report.get('read_only_capture_RAM_snapshots',[])+report.get('read_only_pause_RAM_snapshots',[])
    frames=sorted({r['frame'] for r in snapshots}|{r['frame'] for r in report['frames_captured']})
    destination=cap/f'item_roles_v789_seeded_{args.version}'
    assert not destination.exists()
    command=[sys.executable,'scripts/run_item_rng_v789.py','--rom',f'out/all_routes_combined_v{args.version}_candidate.nds',
        '--out',str(destination),'--frames','20000','--inputs-json',str(root/'qualified_initial_inputs.json'),
        '--battery-save',report['battery_save_preloaded']['source'],'--touchscreen','--capture-every','99999',
        '--capture-at',*map(str,frames),'--pause-at','3200','--dump-capture-ram','--dump-pause-ram','--dump-ram','--allow-condition-fixtures']
    save(root/f'controlled_RNG_{args.version}_plan.json',{'command':command,'stdin_commands':commands,
        'reference_report_sha256':sha((original/'capture_report.json').read_bytes()),'plan_not_completion':True})
    with (root/f'controlled_RNG_{args.version}.log').open('w',encoding='utf-8') as log:
        result=subprocess.run(command,input=stdin,text=True,encoding='utf-8',stdout=log,stderr=subprocess.STDOUT)
    assert result.returncode==0
    done=read(destination/'capture_report.json');assert done['frames']==20000
    assert done['scripted_input_schedule']==report['scripted_input_schedule']
    print(f'Original schedule plus explicit same-seed control complete for V{args.version}.',flush=True)


if __name__=='__main__':main()
