"""Original slot-six reload and source-guarded location fixture; no message/outcome injection."""
import sys
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.run_activity_special_live_v988 import GrowingCommands
from scripts import native_battle_fixture_v620 as dispatch
from scripts.native_ranged_staffing_v1050b import apply_fixture
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/reinforcement_sniping_v1051')
ROM=Path('out/all_routes_combined_v1034_candidate.nds')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/reinforcement_sniping_v1051_1034_regional')
HARNESS='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'


def main():
    assert not ROOT.exists() and not CAP.exists();ROOT.mkdir(parents=True)
    assert sha(ROM.read_bytes())==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    assert sha(Path(harness.__file__).read_bytes())==HARNESS
    source=Path('work/analysis/regional_fleet_v615/formed_Manuel_regional_copy.dsv')
    digest=sha(source.read_bytes());assert digest=='2bec91a13ba69361c5c79ff52dcc3c8a3d5cf2ccbe2fc4b614bac8d12ab4cee1'
    donor=ROOT/'disposable_regional.dsv';copy2(source,donor)
    inputs=ROOT/'original_load_inputs.json'
    schedule=read('work/analysis/regional_fleet_v616/policy_replay_inputs.json')
    schedule=[r for r in schedule if r['start']<=2801];assert len(schedule)==4
    save(inputs,schedule)
    journal=ROOT/'navigation.jsonl'
    import json
    commands=[json.loads(s) for s in Path('work/analysis/reinforcement_sniping_v1039/navigation.jsonl').read_text(encoding='utf-8').splitlines() if s]
    commands=[c for c in commands if not c.get('stop')]
    assert [c['until'] for c in commands]==[3800,4200,4600,4800,5000,5100,5110,5210,5310,5410,5510]
    commands += [{'until':5511,'duration':1,'battle_fixture':{'reinforcement_context':'staffForRangedBattle'}},
                 {'until':5610,'buttons':['A'],'duration':8}]
    journal.write_text(''.join(json.dumps(c)+'\n' for c in commands),encoding='utf-8')
    save(ROOT/'run_plan.json',{'ROM':str(ROM),'ROM_sha256':sha(ROM.read_bytes()),
        'source_donor':str(source),'source_donor_sha256':digest,'disposable_donor':str(donor),
        'source_formation_manifest':'work/analysis/regional_fleet_v615/formed_fixture_manifest.json',
        'inputs':str(inputs),'inputs_sha256':sha(inputs.read_bytes()),'append_only_navigation':str(journal),
        'harness_sha256':HARNESS,'runner_sha256':sha(Path(__file__).read_bytes()),
        'no_numeric_message_or_battle_outcome_injection':True, 'location_fixture':'scripts/native_ranged_staffing_v1050b.py', 'location_fixture_sha256':sha(Path('scripts/native_ranged_staffing_v1050b.py').read_bytes()),'no_earned_progression_or_actual_event_credit':True})
    stream=GrowingCommands(journal);old=sys.stdin;sys.stdin=stream
    old_dispatch=dispatch.apply_fixture;dispatch.apply_fixture=apply_fixture
    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','100000',
        '--inputs-json',str(inputs),'--touchscreen','--capture-every','999999','--capture-at','3400',
        '--battery-save',str(donor),'--pause-at','3400','--dump-capture-ram','--dump-pause-ram','--dump-ram','--allow-battle-fixtures']
    try:harness.main()
    finally:sys.stdin=old;dispatch.apply_fixture=old_dispatch;stream.close()
    assert sha(source.read_bytes())==sha(donor.read_bytes())==digest
    save(ROOT/'terminal_preservation.json',{'source_and_disposable_donors_unchanged':True,
        'source_donor_sha256':digest,'navigation_sha256':sha(journal.read_bytes()),
        'actual_event_credit_requires_separate_proof':True})
    print('V1051 terminal;original and disposable donor preserved.',flush=True)


if __name__=='__main__':main()
