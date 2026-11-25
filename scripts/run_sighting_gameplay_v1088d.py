"""Cold slot-six load to Info;append audited source prerequisites after preflight."""
import argparse
import json
import sys
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.run_activity_special_live_v988 import GrowingCommands
from scripts import native_battle_fixture_v620 as dispatch
from scripts.native_sighting_context_v1087d import apply_fixture
from scripts.verify_village_wrap_v608 import read,save

ROM=Path('out/all_routes_combined_v1086_candidate.nds')
HARNESS='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--case',choices=('closeReady28','closeAttack28'),required=True)
    case=parser.parse_args().case
    root=Path('work/analysis/sighting_gameplay_v1088d_'+case)
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/sighting_v1088d_1086_'+case)
    assert not root.exists() and not cap.exists();root.mkdir(parents=True)
    assert sha(ROM.read_bytes())==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    assert sha(Path(harness.__file__).read_bytes())==HARNESS
    source=Path('work/analysis/regional_fleet_v615/formed_Manuel_regional_copy.dsv')
    digest=sha(source.read_bytes());assert digest=='2bec91a13ba69361c5c79ff52dcc3c8a3d5cf2ccbe2fc4b614bac8d12ab4cee1'
    donor=root/'disposable_regional.dsv';copy2(source,donor)
    inputs=root/'original_load_inputs.json';schedule=read('work/analysis/regional_fleet_v616/policy_replay_inputs.json')
    schedule=[r for r in schedule if r['start']<=2801];assert len(schedule)==4;save(inputs,schedule)
    commands=[json.loads(s) for s in Path('work/analysis/reinforcement_sniping_v1039/navigation.jsonl').read_text(encoding='utf8').splitlines() if s]
    commands=[c for c in commands if c.get('until',999999)<=5100]
    assert [c['until'] for c in commands]==[3800,4200,4600,4800,5000,5100]
    assert not any('battle_fixture' in c for c in commands)
    commands += [{'until':5210,'buttons':['B'],'duration':8},{'until':5310,'buttons':['B'],'duration':8},{'until':5410,'duration':1}]
    journal=root/'navigation.jsonl';journal.write_text(''.join(json.dumps(c)+'\n' for c in commands),encoding='utf8')
    save(root/'run_plan.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'case':case,'capture_folder':str(cap),
        'source_donor':str(source),'source_donor_sha256':digest,'disposable_donor':str(donor),
        'inputs':str(inputs),'inputs_sha256':sha(inputs.read_bytes()),'append_only_navigation':str(journal),
        'harness_sha256':HARNESS,'runner_sha256':sha(Path(__file__).read_bytes()),
        'fixture_module':'scripts/native_sighting_context_v1087d.py','fixture_module_sha256':sha(Path('scripts/native_sighting_context_v1087d.py').read_bytes()),
        'pause5410_after_original_Stop_requires_preflight':True,'no_numeric_message_or_outcome_injection':True,
        'no_scene_or_editorial_completion_credit_without_separate_verification':True})
    stream=GrowingCommands(journal);old=sys.stdin;sys.stdin=stream;old_dispatch=dispatch.apply_fixture;dispatch.apply_fixture=apply_fixture
    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(cap),'--frames','100000','--inputs-json',str(inputs),
        '--touchscreen','--capture-every','999999','--capture-at','3400','--battery-save',str(donor),'--pause-at','3400',
        '--dump-capture-ram','--dump-pause-ram','--dump-ram','--allow-battle-fixtures']
    try:harness.main()
    finally:sys.stdin=old;dispatch.apply_fixture=old_dispatch;stream.close()
    assert sha(source.read_bytes())==sha(donor.read_bytes())==digest
    save(root/'terminal_preservation.json',{'source_and_disposable_donors_unchanged':True,'source_donor_sha256':digest,
        'navigation_sha256':sha(journal.read_bytes()),'actual_event_credit_requires_separate_proof':True})
    print(case,'terminal;original and disposable donor preserved.',flush=True)


if __name__=='__main__':main()
