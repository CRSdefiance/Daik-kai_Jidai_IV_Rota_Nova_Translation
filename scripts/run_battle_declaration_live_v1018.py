"""Actual original Sea menu,append-only commands and disposable cold-boot save."""
import argparse
import json
import sys
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import native_battle_fixture_v620 as dispatch
from scripts.native_battle_declaration_lookout_v1017 import dispatch_fixture
from scripts.native_battle_declaration_standoff_v999 import ROM
from scripts.run_activity_special_live_v988 import GrowingCommands
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_declaration_v1018')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
HARNESS = 'd5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=('ObserveMenu', 'KnownJanus', 'UnknownEmilio', 'ReadyEmilio'), required=True)
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    folder = CAP/f'battle_declaration_v1018_997_{args.case}'
    assert not folder.exists()
    assert sha(Path(harness.__file__).read_bytes()) == HARNESS
    digest = sha(ROM.read_bytes())
    assert digest == read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    pre = read('work/analysis/full_fleet_victory_v654/replay_preflight.json')
    source = Path(pre['donor'])
    donor = ROOT/f'disposable_{args.case}.dsv'
    assert not donor.exists()
    donor_digest = sha(source.read_bytes())
    assert donor_digest == pre['donor_sha256']
    commands = [{k:v for k,v in r.items() if k != 'export_native_state'}
                for r in read(pre['commands']) if 'stop' not in r and r.get('until', 999999) <= 5200]
    assert [r['until'] for r in commands] == [4801, 4900, 5200]
    assert args.case in ('KnownJanus','UnknownEmilio','ReadyEmilio')
    commands += [
        {'until':5300,'touch':[130,95],'duration':8},
        {'until':5350,'battle_fixture':{'declaration_context':args.case},'duration':1},
        {'until':5450,'battle_fixture':{'declaration_context':'approachPasha'},'buttons':['Y'],'duration':8},
        {'until':5550,'buttons':['Y'],'duration':8},
        {'until':5650,'buttons':['Y'],'duration':8},
        {'until':5660,'battle_fixture':{'declaration_context':'approachVisiblePasha'},'buttons':['B'],'duration':8},
        {'until':5760,'buttons':['Y'],'duration':8},
        {'until':5860,'buttons':['Y'],'duration':8},
        {'until':5960,'buttons':['Y'],'duration':8}]
    journal = ROOT/f'{args.case}_navigation.jsonl'
    assert not journal.exists()
    with journal.open('x', encoding='utf-8') as f:
        for command in commands:
            f.write(json.dumps(command)+'\n')
    copy2(source, donor)
    inputs = Path(pre['inputs'])
    plan = ROOT/f'{args.case}_run_plan.json'
    assert not plan.exists()
    save(plan, {'candidate': str(ROM), 'candidate_sha256': digest, 'folder': str(folder),
        'source_donor': str(source), 'source_donor_sha256': donor_digest, 'disposable_donor': str(donor),
        'inputs': str(inputs), 'inputs_sha256': sha(inputs.read_bytes()),
        'append_only_navigation': str(journal), 'initial_navigation_sha256': sha(journal.read_bytes()),
        'original_harness_sha256': HARNESS, 'fixture_dispatcher': 'scripts/native_battle_declaration_standoff_v999.py',
        'fixture_dispatcher_sha256': sha(Path('scripts/native_battle_declaration_standoff_v999.py').read_bytes()),
        'no_earned_progression_or_scene_completion_claim': True, 'initial_last_frame': 5960, 'context_successor': 'scripts/native_battle_declaration_lookout_v1017.py',
        'context_successor_sha256':sha(Path('scripts/native_battle_declaration_lookout_v1017.py').read_bytes()),
        'source_runner_sha256':sha(Path('scripts/run_battle_declaration_live_v999.py').read_bytes()),
        'no_numeric_message_injection_or_battle_outcome_fixture': True,
        'runner_sha256': sha(Path(__file__).read_bytes())})
    stream = GrowingCommands(journal)
    old_dispatch, old_stdin = dispatch.apply_fixture, sys.stdin
    dispatch.apply_fixture, sys.stdin = dispatch_fixture, stream
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder), '--frames', '100000',
                '--inputs-json', str(inputs), '--touchscreen', '--capture-every', '999999', '--capture-at', '4800',
                '--battery-save', str(donor), '--pause-at', '4800', '--dump-capture-ram', '--dump-pause-ram', '--dump-ram',
                '--allow-battle-fixtures']
    try:
        harness.main()
    finally:
        dispatch.apply_fixture, sys.stdin = old_dispatch, old_stdin
        stream.close()
    assert sha(source.read_bytes()) == sha(donor.read_bytes()) == donor_digest
    report_path = folder/'capture_report.json'
    report = read(report_path)
    assert sha(Path(harness.__file__).read_bytes()) == HARNESS
    report['controlled_battle_declaration_fixture_dispatch'] = {
        'original_harness_file_unchanged': True, 'original_harness_sha256': HARNESS,
        'dispatcher_sha256': sha(Path('scripts/native_battle_declaration_standoff_v999.py').read_bytes()),
        'runner_sha256': sha(Path(__file__).read_bytes()),
        'context_successor_sha256':sha(Path('scripts/native_battle_declaration_lookout_v1017.py').read_bytes()),
        'source_and_disposable_donors_unchanged': True, 'source_donor_sha256': donor_digest}
    save(report_path, report)
    save(ROOT/f'{args.case}_terminal_source_preservation.json', {
        'source_and_disposable_donors_unchanged': True, 'source_donor_sha256': donor_digest,
        'final_navigation_sha256': sha(journal.read_bytes()), 'actual_scene_proofs_required_separately': True})
    print('V1018', args.case, 'terminal;source/disposable donors unchanged.', flush=True)


if __name__ == '__main__':
    main()
