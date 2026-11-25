"""Fresh V893 cold boot through retained original tutorial encounter;no mode edit."""

import io
import json
import sys
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import native_battle_fixture_v620 as dispatch
from scripts.native_battle_proximity_v894 import apply_fixture,ROM
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_personal_v894')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/battle_personal_v894_893_encounter')


def main():
    assert not CAP.exists();ROOT.mkdir(parents=True,exist_ok=True)
    assert sha(ROM.read_bytes())==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    pre=read('work/analysis/full_fleet_victory_v654/replay_preflight.json')
    source=Path(pre['donor']);donor=ROOT/'disposable_encounter.dsv';assert not donor.exists()
    digest=sha(source.read_bytes());assert digest==pre['donor_sha256']
    copy2(source,donor);assert sha(donor.read_bytes())==digest
    old_commands=read(pre['commands'])
    commands=[{k:v for k,v in r.items() if k!='export_native_state'} for r in old_commands if r.get('until',999999)<=13200]
    assert commands[-1]['until']==13200
    commands.append({'stop':True})
    commands_path=ROOT/'original_encounter_commands.json';save(commands_path,commands)
    inputs=Path(pre['inputs'])
    plan={'ROM':str(ROM),'ROM_sha256':sha(ROM.read_bytes()),'source_donor':str(source),'source_donor_sha256':digest,
        'disposable_donor':str(donor),'folder':str(CAP),'input_path':str(inputs),'input_sha256':sha(inputs.read_bytes()),
        'commands':str(commands_path),'commands_sha256':sha(commands_path.read_bytes()),
        'source_original_schedule':pre['commands'],'source_original_schedule_sha256':sha(Path(pre['commands']).read_bytes()),
        'only_existing_controller_inputs_and_two_declared_coordinate_fixtures_before13200':True,
        'no_global_battle_predicate_actor_text_code_enemy_stats_or_outcome_assignment':True,
        'not_yet_a_revised_Cabin_body_display_test':True}
    save(ROOT/'encounter_run_plan.json',plan)
    previous_dispatch,previous_stdin=dispatch.apply_fixture,sys.stdin
    dispatch.apply_fixture=apply_fixture
    sys.stdin=io.StringIO('\n'.join(json.dumps(r) for r in commands)+'\n')
    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','13200',
        '--inputs-json',str(inputs),'--touchscreen','--capture-every','999999','--capture-at','4800',
        '--battery-save',str(donor),'--pause-at','4800','--dump-capture-ram','--dump-pause-ram','--dump-ram','--allow-battle-fixtures']
    try:harness.main()
    finally:dispatch.apply_fixture,sys.stdin=previous_dispatch,previous_stdin
    assert sha(source.read_bytes())==sha(donor.read_bytes())==digest
    save(ROOT/'encounter_terminal_source_preservation.json',{'source_donor_sha256':digest,
        'source_and_disposable_donors_unchanged':True,'runner_sha256':sha(Path(__file__).read_bytes()),
        'actual_revised_Cabin_body_and_normal_return_still_pending':True})
    print('V894 original tutorial encounter terminal;battle predicate/body verification still required.',flush=True)


if __name__=='__main__':main()
