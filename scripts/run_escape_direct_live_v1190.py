"""Cold replay the proven original defeat navigation; leave the notice paused."""
import json
import sys
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.run_activity_special_live_v988 import GrowingCommands
from scripts import native_battle_fixture_v620 as dispatch
from scripts.native_escape_direct_fixture_v1190 import ROM,apply_fixture
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/escape_direct_live_v1190')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/escape_direct_v1190_1189')
HARNESS='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'


def main():
    assert not ROOT.exists() and not CAP.exists()
    assert sha(ROM.read_bytes())==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    assert sha(Path(harness.__file__).read_bytes())==HARNESS
    source=Path('work/analysis/regional_fleet_v615/formed_Manuel_regional_copy.dsv');digest=sha(source.read_bytes())
    assert digest=='2bec91a13ba69361c5c79ff52dcc3c8a3d5cf2ccbe2fc4b614bac8d12ab4cee1'
    previous=Path('work/analysis/duel_escape_v1179_compassAttack8/navigation.jsonl')
    commands=[json.loads(line) for line in previous.read_text(encoding='utf8').splitlines() if line]
    assert commands[-1]=={'stop':True};commands=commands[:-1]
    assert commands[-1]['until']==6922
    assert max(c['until'] for c in commands if 'battle_fixture' in c)==5772
    ROOT.mkdir(parents=True);donor=ROOT/'disposable_regional.dsv';copy2(source,donor)
    journal=ROOT/'navigation.jsonl';journal.write_text(''.join(json.dumps(c)+'\n' for c in commands),encoding='utf8')
    inputs=ROOT/'original_load_inputs.json';copy2(Path('work/analysis/duel_escape_v1179_compassAttack8/original_load_inputs.json'),inputs)
    save(ROOT/'run_plan.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'capture_folder':str(CAP),
        'source_donor':str(source),'source_donor_sha256':digest,'disposable_donor':str(donor),
        'inputs':str(inputs),'inputs_sha256':sha(inputs.read_bytes()),'append_only_navigation':str(journal),
        'exact_prior_navigation_reference':str(previous),'prior_navigation_sha256':sha(previous.read_bytes()),
        'all_navigation_through6922_exact_except_final_stop_removed':True,'harness_sha256':HARNESS,
        'fixture_module':'scripts/native_escape_direct_fixture_v1190.py',
        'fixture_module_sha256':sha(Path('scripts/native_escape_direct_fixture_v1190.py').read_bytes()),
        'runner_sha256':sha(Path(__file__).read_bytes()),
        'pre_duel_low_positive_HP_shield_inventory_transfer_and_contact_only':True,
        'no_message_ID_RNG_actor_ID_or_outcome_injection':True,'completion_credit_requires_separate_verification':True})
    stream=GrowingCommands(journal);old=sys.stdin;sys.stdin=stream;prior=dispatch.apply_fixture;dispatch.apply_fixture=apply_fixture
    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','100000','--inputs-json',str(inputs),
        '--touchscreen','--capture-every','999999','--capture-at','3400','--battery-save',str(donor),'--pause-at','3400',
        '--dump-capture-ram','--dump-pause-ram','--dump-ram','--allow-battle-fixtures']
    try:harness.main()
    finally:sys.stdin=old;dispatch.apply_fixture=prior;stream.close()
    assert sha(source.read_bytes())==sha(donor.read_bytes())==digest
    save(ROOT/'terminal_preservation.json',{'source_and_disposable_donors_unchanged':True,'source_donor_sha256':digest,
        'navigation_sha256':sha(journal.read_bytes()),'actual_credit_requires_separate_verification':True})
    print('Original escape replay terminal; donors preserved.',flush=True)


if __name__=='__main__':main()
