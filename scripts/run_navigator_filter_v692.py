"""Cold-boot navigator filter choices with copied donors and unchanged controls."""

import argparse
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.run_village_visits_v664 import CAP
from scripts.trace_deck_gender_v692 import DONOR_HASHES, DONORS, ROOT
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v692_candidate.nds')


def prepare():
    old = read(ROOT / 'unassigned_inputs.json')
    inputs = [row for row in old if row['start'] < 8801]
    inputs += [{'start': f, 'duration': 8, 'buttons': [key]} for f, key in (
        (8801, 'DOWN'), (9201, 'A'), (9601, 'X'), (10001, 'DOWN'),
        (10401, 'A'), (10801, 'DOWN'), (11201, 'A'), (11601, 'RIGHT'),
        (12001, 'X'), (12401, 'DOWN'), (12801, 'A'), (13201, 'UP'),
        (13601, 'UP'), (14001, 'A'), (14401, 'B'), (14801, 'B'))]
    save(ROOT / 'filter_inputs.json', inputs)
    ordinary = read('work/analysis/story_percent_v685/ordinary_inputs.json')
    save(ROOT / 'ordinary_inputs.json', ordinary)
    cases = {}
    for name, source, donor in (('source', True, 'hodram'), ('hodram', False, 'hodram'),
                                ('maria', False, 'maria'), ('ordinary', False, None)):
        path = Path('out/all_routes_combined_v685_candidate.nds') if source else ROM
        cases[name] = {'ROM': str(path), 'ROM_sha256': sha(path.read_bytes()), 'donor': donor,
            'inputs': str(ROOT / ('ordinary_inputs.json' if donor is None else 'filter_inputs.json')),
            'frames': 24100 if donor is None else 15200}
        cases[name]['inputs_sha256'] = sha(Path(cases[name]['inputs']).read_bytes())
        if donor:
            assert sha(DONORS[donor].read_bytes()) == DONOR_HASHES[donor]
            cases[name]['donor_path'], cases[name]['donor_sha256'] = str(DONORS[donor]), DONOR_HASHES[donor]
    save(ROOT / 'run_cases.json', {'cases': cases, 'producer_sha256': sha(Path(__file__).read_bytes())})
    print('V692 source/current complete filter choices and ordinary New Game schedules pinned.', flush=True)


def run(case):
    plan = read(ROOT / 'run_cases.json')
    assert plan['producer_sha256'] == sha(Path(__file__).read_bytes())
    row = plan['cases'][case]
    assert sha(Path(row['ROM']).read_bytes()) == row['ROM_sha256']
    assert sha(Path(row['inputs']).read_bytes()) == row['inputs_sha256']
    folder = CAP / ('navigator_filter_v692_' + case)
    assert not folder.exists()
    folder.mkdir()
    if row['donor']:
        frames = sorted({1, 60, 180, 1600, *range(2000, row['frames'] + 1, 400), row['frames']})
    else:
        old = read(CAP / 'story_percent_v685_ordinary/capture_report.json')
        assert old['scripted_input_schedule'] == read(row['inputs'])
        frames = sorted({r['frame'] for r in old['frames_captured']})
    save(folder / 'run_contract.json', {'config': row, 'producer_sha256': plan['producer_sha256'],
        'no_observer_savestate_or_live_game_state_fixture': True,
        'normal_menu_duty_changes_not_saved_to_donor': bool(row['donor']),
        'Maria_donor_historical_selection_unlock_not_earned': row['donor'] == 'maria'})
    sys.argv = ['headless_desmume_v193.py', '--rom', row['ROM'], '--out', str(folder),
        '--frames', str(row['frames']), '--inputs-json', row['inputs'], '--touchscreen',
        '--capture-every', '999999', '--capture-at', *map(str, frames), '--dump-capture-ram', '--dump-ram']
    if row['donor']:
        assert sha(Path(row['donor_path']).read_bytes()) == row['donor_sha256']
        sys.argv += ['--battery-save', row['donor_path']]
    harness.main()
    print('V692 navigator filter run terminal:', case, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('case', choices=('prepare', 'source', 'hodram', 'maria', 'ordinary'))
    args = parser.parse_args()
    if args.case == 'prepare':
        prepare()
    else:
        run(args.case)
