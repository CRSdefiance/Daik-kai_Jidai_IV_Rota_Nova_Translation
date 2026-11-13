"""Original Sao Tome battle with ordinary touchscreen stop; no post-entry fixtures."""
import json
import sys
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import native_battle_fixture_v620 as dispatch
from scripts.native_aftermath_town_fixture_v1290 import ROM, apply_fixture
from scripts.run_activity_special_live_v988 import GrowingCommands
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/town_hold_v1297')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_hold_v1297_1266')
HARNESS = 'd5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'


def main():
    assert not ROOT.exists() and not CAP.exists()
    digest = sha(ROM.read_bytes())
    assert digest == read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    assert sha(Path(harness.__file__).read_bytes()) == HARNESS
    source = Path('work/analysis/regional_fleet_v615/formed_Manuel_regional_copy.dsv')
    donor_sha = sha(source.read_bytes())
    assert donor_sha == '2bec91a13ba69361c5c79ff52dcc3c8a3d5cf2ccbe2fc4b614bac8d12ab4cee1'
    previous = Path('work/analysis/aftermath_town_v1291/navigation.jsonl')
    commands = [json.loads(line) for line in previous.read_text(encoding='utf-8').splitlines() if line]
    commands = [row for row in commands if row.get('until',999999) <= 5910]
    assert commands[-1]['until'] == 5910
    assert [row['battle_fixture'] for row in commands if 'battle_fixture' in row] == [{'town_context':'SaoTomeFirstMate'}]
    commands += [{'until':6010,'touch':[128,96],'duration':8}]
    ROOT.mkdir(parents=True)
    donor = ROOT/'disposable_regional.dsv'
    copy2(source,donor)
    journal = ROOT/'navigation.jsonl'
    journal.write_text(''.join(json.dumps(row)+'\n' for row in commands),encoding='utf-8')
    inputs = ROOT/'original_load_inputs.json'
    copy2(Path('work/analysis/aftermath_town_v1291/original_load_inputs.json'),inputs)
    save(ROOT/'run_plan.json',{'candidate':str(ROM),'candidate_sha256':digest,'capture_folder':str(CAP),
        'source_donor':str(source),'source_donor_sha256':donor_sha,'disposable_donor':str(donor),
        'append_only_navigation':str(journal),'original_navigation':str(previous),'original_navigation_sha256':sha(previous.read_bytes()),
        'only_fixture':{'town_context':'SaoTomeFirstMate'},'fixture_module':'scripts/native_aftermath_town_fixture_v1290.py',
        'fixture_module_sha256':sha(Path('scripts/native_aftermath_town_fixture_v1290.py').read_bytes()),
        'no_health_defense_share_actor_ID_RNG_eligibility_battle_state_result_or_message_injection':True,
        'no_fixture_after_original_town_battle_entry':True,'harness_sha256':HARNESS,'runner_sha256':sha(Path(__file__).read_bytes())})
    stream = GrowingCommands(journal)
    old,old_fixture = sys.stdin,dispatch.apply_fixture
    sys.stdin,dispatch.apply_fixture = stream,apply_fixture
    sys.argv = ['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','100000',
        '--inputs-json',str(inputs),'--touchscreen','--capture-every','999999','--capture-at','3400',
        '--battery-save',str(donor),'--pause-at','3400','--dump-capture-ram','--dump-pause-ram','--dump-ram','--allow-battle-fixtures']
    try:
        harness.main()
    finally:
        sys.stdin,dispatch.apply_fixture = old,old_fixture
        stream.close()
    assert sha(source.read_bytes()) == sha(donor.read_bytes()) == donor_sha
    save(ROOT/'terminal_preservation.json',{'source_and_disposable_donors_unchanged':True,'source_donor_sha256':donor_sha,
        'navigation_sha256':sha(journal.read_bytes()),'scene_outcome_credit_requires_separate_verification':True})
    print('Original town hold terminal;both source saves preserved.',flush=True)


if __name__ == '__main__':
    main()
