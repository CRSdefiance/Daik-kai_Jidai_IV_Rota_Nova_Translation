"""Cold original duel replay; pause before ordinary timed button experiments."""
import json
import sys
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.run_activity_special_live_v988 import GrowingCommands
from scripts import native_battle_fixture_v620 as dispatch
from scripts.native_duel_bark_fixture_v1207 import ROM,apply_fixture
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_bark_live_v1207')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_bark_v1207_1206')
HARNESS='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'


def main():
    assert not ROOT.exists() and not CAP.exists()
    assert sha(ROM.read_bytes())==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    assert sha(Path(harness.__file__).read_bytes())==HARNESS
    source=Path('work/analysis/regional_fleet_v615/formed_Manuel_regional_copy.dsv');digest=sha(source.read_bytes())
    assert digest=='2bec91a13ba69361c5c79ff52dcc3c8a3d5cf2ccbe2fc4b614bac8d12ab4cee1'
    previous=Path('work/analysis/duel_contact_v1169_compassAttack8/navigation.jsonl')
    commands=[json.loads(line) for line in previous.read_text(encoding='utf8').splitlines() if line]
    commands=[r for r in commands if r.get('until',999999)<=5772]
    assert commands[-1]['until']==5772 and max(c['until'] for c in commands if 'battle_fixture' in c)==5772
    commands += [{'until':5782,'duration':1},{'until':5902,'duration':1}]
    ROOT.mkdir(parents=True);donor=ROOT/'disposable_regional.dsv';copy2(source,donor)
    journal=ROOT/'navigation.jsonl';journal.write_text(''.join(json.dumps(c)+'\n' for c in commands),encoding='utf8')
    inputs=ROOT/'original_load_inputs.json';copy2(Path('work/analysis/duel_escape_v1179_compassAttack8/original_load_inputs.json'),inputs)
    save(ROOT/'run_plan.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'capture_folder':str(CAP),
        'source_donor':str(source),'source_donor_sha256':digest,'disposable_donor':str(donor),
        'inputs':str(inputs),'inputs_sha256':sha(inputs.read_bytes()),'append_only_navigation':str(journal),
        'source_pre_duel_navigation':str(previous),'source_navigation_sha256':sha(previous.read_bytes()),
        'fixture_module':'scripts/native_duel_bark_fixture_v1207.py','fixture_module_sha256':sha(Path('scripts/native_duel_bark_fixture_v1207.py').read_bytes()),
        'harness_sha256':HARNESS,'runner_sha256':sha(Path(__file__).read_bytes()),
        'only_positive_health_ship_recovery_and_contact_before_duel':True,
        'timed_reactions_require_ordinary_physical_button_inputs_after5902':True,
        'no_actor_ID_numeric_message_RNG_or_battle_result_injection':True,'completion_requires_separate_evidence':True})
    stream=GrowingCommands(journal);old=sys.stdin;sys.stdin=stream;prior=dispatch.apply_fixture;dispatch.apply_fixture=apply_fixture
    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','100000','--inputs-json',str(inputs),
        '--touchscreen','--capture-every','999999','--capture-at','3400','--battery-save',str(donor),'--pause-at','3400',
        '--dump-capture-ram','--dump-pause-ram','--dump-ram','--allow-battle-fixtures']
    try:harness.main()
    finally:sys.stdin=old;dispatch.apply_fixture=prior;stream.close()
    assert sha(source.read_bytes())==sha(donor.read_bytes())==digest
    save(ROOT/'terminal_preservation.json',{'source_and_disposable_donors_unchanged':True,'source_donor_sha256':digest,
        'navigation_sha256':sha(journal.read_bytes()),'actual_credit_requires_separate_verification':True})
    print('Duel reaction replay terminal; source and disposable donors preserved.',flush=True)


if __name__=='__main__':main()
