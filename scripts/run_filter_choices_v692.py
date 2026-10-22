"""Exercise all original filter outcomes with the frozen V692 capture runner."""

import argparse
import copy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import run_navigator_filter_v692 as runner
from scripts.verify_village_wrap_v608 import read, save

ROOT = runner.ROOT / 'all_choices'


def prepare():
    ROOT.mkdir()
    original = read(runner.ROOT / 'run_cases.json')
    inputs = read(runner.ROOT / 'filter_inputs.json')
    # Popup selection starts at Unassigned on every opening. The first schedule
    # selected Captain three times; preserve it and test the remaining outcomes.
    inputs.append({'start': 11001, 'duration': 8, 'buttons': ['DOWN']})
    for row in inputs:
        if row['start'] == 13601:
            row['buttons'] = ['DOWN']
    inputs.sort(key=lambda row: row['start'])
    save(ROOT / 'inputs.json', inputs)
    cases = {}
    for name in ('source', 'hodram', 'maria'):
        row = copy.deepcopy(original['cases'][name])
        row['inputs'], row['inputs_sha256'] = str(ROOT / 'inputs.json'), sha((ROOT / 'inputs.json').read_bytes())
        cases[name + '_full'] = row
    save(ROOT / 'run_cases.json', {'cases': cases, 'producer_sha256': original['producer_sha256'],
        'process_local_ROOT_configuration_only': True, 'launcher_sha256': sha(Path(__file__).read_bytes())})
    print('V692 all-choice schedule: Captain,All,Unassigned; original runs retained.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('case', choices=('prepare', 'source_full', 'hodram_full', 'maria_full'))
    args = parser.parse_args()
    if args.case == 'prepare':
        prepare()
    else:
        assert read(ROOT / 'run_cases.json')['launcher_sha256'] == sha(Path(__file__).read_bytes())
        runner.ROOT = ROOT
        runner.run(args.case)
