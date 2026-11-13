"""Cold replay of the original unforced battle outcome under V1266."""
import json
import sys
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.run_activity_special_live_v988 import GrowingCommands
from scripts import native_battle_fixture_v620 as dispatch
from scripts.native_aftermath_battle_fixture_v1269 import ROM,apply_fixture
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/aftermath_victory_v1270')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/aftermath_victory_v1270_1266')
HARNESS = 'd5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'


def main():
    assert not ROOT.exists() and not CAP.exists()
    digest = sha(ROM.read_bytes())
    assert digest == read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    assert sha(Path(harness.__file__).read_bytes()) == HARNESS
    source = Path('work/analysis/regional_fleet_v615/formed_Manuel_regional_copy.dsv')
    save_sha = sha(source.read_bytes())
    assert save_sha == '2bec91a13ba69361c5c79ff52dcc3c8a3d5cf2ccbe2fc4b614bac8d12ab4cee1'
    previous = Path('work/analysis/duel_long_live_v1243/navigation.jsonl')
    commands = [json.loads(line) for line in previous.read_text(encoding='utf-8').splitlines() if line]
    assert commands[-1] == {'stop':True}
    assert max(c['until'] for c in commands if 'battle_fixture' in c) == 5772
    assert not any(c.get('buttons') or c.get('touch') for c in commands if 5772 < c.get('until',0) < 10982)
    ROOT.mkdir(parents=True)
    donor = ROOT/'disposable_regional.dsv'
    copy2(source,donor)
    journal = ROOT/'navigation.jsonl'
    journal.write_text(''.join(json.dumps(c)+'\n' for c in commands),encoding='utf-8')
    inputs = ROOT/'original_load_inputs.json'
    copy2(Path('work/analysis/duel_long_live_v1243/original_load_inputs.json'),inputs)
    save(ROOT/'run_plan.json',{'candidate':str(ROM),'candidate_sha256':digest,'capture_folder':str(CAP),
        'source_donor':str(source),'source_donor_sha256':save_sha,'disposable_donor':str(donor),
        'source_navigation':str(previous),'source_navigation_sha256':sha(previous.read_bytes()),
        'append_only_navigation':str(journal),'navigation_identical_to_prior_audited_original_run':True,
        'inputs':str(inputs),'inputs_sha256':sha(inputs.read_bytes()),
        'fixture_module':'scripts/native_aftermath_battle_fixture_v1269.py',
        'fixture_module_sha256':sha(Path('scripts/native_aftermath_battle_fixture_v1269.py').read_bytes()),
        'harness_sha256':HARNESS,'runner_sha256':sha(Path(__file__).read_bytes()),
        'all_fixture_requests_before_duel_no_actor_ID_RNG_numeric_message_or_result_override':True,
        'no_during_or_post_duel_healing_revival_ability_equipment_or_location_changes':True,
        'actual_result_and_translation_credit_require_separate_verification':True})
    stream = GrowingCommands(journal)
    old = sys.stdin
    prior = dispatch.apply_fixture
    sys.stdin,dispatch.apply_fixture = stream,apply_fixture
    sys.argv = ['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','100000',
        '--inputs-json',str(inputs),'--touchscreen','--capture-every','999999','--capture-at','3400',
        '--battery-save',str(donor),'--pause-at','3400','--dump-capture-ram','--dump-pause-ram','--dump-ram',
        '--allow-battle-fixtures']
    try:
        harness.main()
    finally:
        sys.stdin,dispatch.apply_fixture = old,prior
        stream.close()
    assert sha(source.read_bytes()) == sha(donor.read_bytes()) == save_sha
    save(ROOT/'terminal_preservation.json',{'source_and_disposable_donors_unchanged':True,
        'source_donor_sha256':save_sha,'navigation_sha256':sha(journal.read_bytes()),
        'original_gameplay_outcome_and_text_must_be_inspected_separately':True})
    print('Original battle replay terminal;source and disposable donors preserved.',flush=True)


if __name__ == '__main__':
    main()
