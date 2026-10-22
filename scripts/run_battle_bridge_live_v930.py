"""Cold-boot original encounter and append-only navigation;no saved-state restore."""

import argparse
import json
import sys
import time
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_battle_fixture_v620 as dispatch
from scripts import run_battle_bridge_adapter_v930 as adapter
from scripts.native_battle_standoff_v929 import apply_fixture,ROM
from scripts.native_battle_bridge_fixture_v929 import CASES
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_bridge_v930')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')


class GrowingCommands:
    def __init__(self,path):self.stream=path.open('r',encoding='utf-8')
    def readline(self,*args):
        deadline=time.monotonic()+1200
        while time.monotonic()<deadline:
            line=self.stream.readline()
            if line:return line
            time.sleep(0.1)
        raise TimeoutError('No appended navigation command for20 minutes;run not restarted')
    def isatty(self):return False
    def close(self):self.stream.close()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--case',choices=tuple(CASES),required=True);args=parser.parse_args()
    ROOT.mkdir(parents=True,exist_ok=True);folder=CAP/f'battle_bridge_v930_928_{args.case}';assert not folder.exists()
    assert sha(ROM.read_bytes())==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    pre=read('work/analysis/full_fleet_victory_v654/replay_preflight.json');source=Path(pre['donor'])
    donor=ROOT/f'disposable_{args.case}.dsv';assert not donor.exists()
    digest=sha(source.read_bytes());assert digest==pre['donor_sha256'];copy2(source,donor)
    old_commands=read(pre['commands']);commands=[{k:v for k,v in r.items() if k!='export_native_state'} for r in old_commands if 'stop' not in r and r.get('until',999999)<=11700]
    if args.case=='ClaudioMate':commands[0]['battle_bridge_fixture']=args.case
    assert commands[-1]['until']==11700
    journal=ROOT/f'{args.case}_navigation.jsonl';assert not journal.exists()
    with journal.open('x',encoding='utf-8') as f:
        for command in commands:f.write(json.dumps(command)+'\n')
    inputs=Path(pre['inputs'])
    save(ROOT/f'{args.case}_run_plan.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'folder':str(folder),
        'source_donor':str(source),'source_donor_sha256':digest,'disposable_donor':str(donor),
        'inputs':str(inputs),'inputs_sha256':sha(inputs.read_bytes()),'append_only_navigation':str(journal),
        'initial_navigation_sha256':sha(journal.read_bytes()),'initial_last_frame':11700,
        'battle_mode_changes_only_by_original_gameplay':True,'owned_actor_room_assignment_delayed_until_observed_original_combat':args.case!='ClaudioMate','two_or_three_room_occupant_bytes_plus_two_existing_coordinate_fixtures_only':True,
        'prior_donor_has_isolated_fleet_no_earned_fleet_progression_or_recruitment_claim':True,
        'source_original_schedule':pre['commands'],'source_original_schedule_sha256':sha(Path(pre['commands']).read_bytes()),
        'runner_sha256':sha(Path(__file__).read_bytes())})
    stream=GrowingCommands(journal);previous_dispatch,previous_stdin=dispatch.apply_fixture,sys.stdin
    dispatch.apply_fixture,sys.stdin=apply_fixture,stream
    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(folder),'--frames','100000',
        '--inputs-json',str(inputs),'--touchscreen','--capture-every','999999','--capture-at','4800',
        '--battery-save',str(donor),'--pause-at','4800','--dump-capture-ram','--dump-pause-ram','--dump-ram',
        '--allow-battle-fixtures','--allow-battle-bridge-fixtures']
    try:adapter.main()
    finally:
        dispatch.apply_fixture,sys.stdin=previous_dispatch,previous_stdin;stream.close()
    assert sha(source.read_bytes())==sha(donor.read_bytes())==digest
    save(ROOT/f'{args.case}_terminal_source_preservation.json',{'source_and_disposable_donors_unchanged':True,
        'source_donor_sha256':digest,'final_navigation_sha256':sha(journal.read_bytes()),
        'runner_sha256':sha(Path(__file__).read_bytes()),'actual_body_verification_required_separately':True})
    print('V930',args.case,'terminal;donors unchanged.',flush=True)


if __name__=='__main__':main()
