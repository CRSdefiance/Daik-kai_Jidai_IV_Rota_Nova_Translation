"""Three predeclared ordinary controller schedules for probabilistic specials.

No seed selection, numeric message injection, actor-ID edit or special/result
override. Each case cold-boots, uses the same disclosed pre-duel prerequisites,
then uses only physical A inputs and frame advances until ordinary aftermath.
"""
import argparse
import json
import sys
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import native_battle_fixture_v620 as dispatch
from scripts.run_activity_special_live_v988 import GrowingCommands
from scripts.native_duel_special_fixture_v1232 import ROM, apply_fixture
from scripts.verify_village_wrap_v608 import read, save


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--period',type=int,choices=(37,53,71),required=True)
    args=parser.parse_args()
    root=Path(f'work/analysis/duel_special_matrix_v1235_{args.period}')
    cap=Path(f'E:/Rota Nova translations/Generated/work/emulation_v193/duel_special_v1235_1224_p{args.period}')
    assert not root.exists() and not cap.exists()
    assert sha(ROM.read_bytes())==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    harness_sha='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    assert sha(Path(harness.__file__).read_bytes())==harness_sha
    source=Path('work/analysis/regional_fleet_v615/formed_Manuel_regional_copy.dsv')
    digest=sha(source.read_bytes())
    assert digest=='2bec91a13ba69361c5c79ff52dcc3c8a3d5cf2ccbe2fc4b614bac8d12ab4cee1'
    previous=Path('work/analysis/duel_contact_v1169_compassAttack8/navigation.jsonl')
    commands=[json.loads(s) for s in previous.read_text(encoding='utf-8').splitlines() if s]
    commands=[r for r in commands if r.get('until',999999)<=5772]
    assert commands[-1]['until']==5772 and max(c['until'] for c in commands if 'battle_fixture' in c)==5772
    commands += [{'until':5782,'duration':1},{'until':5902,'duration':1}]
    presses=set(range(5902,7903,args.period))
    points=sorted({*range(5942,9503,40),*presses,9502}-{5902})
    current=5902
    for target in points:
        c={'until':target,'duration':1}
        if current in presses:c['buttons']=['A']
        commands.append(c);current=target
    commands += [{'until':n,'buttons':['A'],'duration':2} for n in range(9702,11503,200)]
    commands.append({'stop':True})
    assert not any('battle_fixture' in c for c in commands if c.get('until',0)>5772)
    root.mkdir(parents=True)
    donor=root/'disposable_regional.dsv';copy2(source,donor)
    inputs=root/'original_load_inputs.json';copy2(Path('work/analysis/duel_escape_v1179_compassAttack8/original_load_inputs.json'),inputs)
    journal=root/'navigation.jsonl';journal.write_text(''.join(json.dumps(c)+'\n' for c in commands),encoding='utf-8')
    save(root/'run_plan.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'capture_folder':str(cap),'period':args.period,'all_three_periods_predeclared':[37,53,71],
        'source_donor':str(source),'source_donor_sha256':digest,'disposable_donor':str(donor),
        'inputs':str(inputs),'inputs_sha256':sha(inputs.read_bytes()),'append_only_navigation':str(journal),
        'initial_navigation_sha256':sha(journal.read_bytes()),
        'fixture_module':'scripts/native_duel_special_fixture_v1232.py',
        'fixture_module_sha256':sha(Path('scripts/native_duel_special_fixture_v1232.py').read_bytes()),
        'harness_sha256':harness_sha,'runner_sha256':sha(Path(__file__).read_bytes()),
        'original_combat_eligibility_actor_IDs_RNG_results_unchanged':True,
        'no_fixture_after_original_duel_begins':True,'actual_credit_requires_separate_evidence':True})
    stream=GrowingCommands(journal);old=sys.stdin;sys.stdin=stream
    prior=dispatch.apply_fixture;dispatch.apply_fixture=apply_fixture
    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(cap),'--frames','100000',
        '--inputs-json',str(inputs),'--touchscreen','--capture-every','999999','--capture-at','3400',
        '--battery-save',str(donor),'--pause-at','3400','--dump-capture-ram','--dump-pause-ram',
        '--dump-ram','--allow-battle-fixtures']
    try:harness.main()
    finally:sys.stdin=old;dispatch.apply_fixture=prior;stream.close()
    assert sha(source.read_bytes())==sha(donor.read_bytes())==digest
    save(root/'terminal_preservation.json',{'source_and_disposable_donors_unchanged':True,
        'source_donor_sha256':digest,'navigation_sha256':sha(journal.read_bytes()),
        'actual_credit_requires_separate_verification':True})
    print('Ordinary timed-A case',args.period,'terminal;donors exact.',flush=True)


if __name__=='__main__':main()
