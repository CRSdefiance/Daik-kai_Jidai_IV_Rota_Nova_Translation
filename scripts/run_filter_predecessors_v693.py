"""Capture predecessor paints with process-local configuration of frozen observers."""

import argparse
import copy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import observe_filter_clock_v693 as observer
from scripts import run_filter_clock_v693 as runner
from scripts.verify_village_wrap_v608 import read, save

ROOT = observer.ROOT / 'predecessors'


def prepare():
    ROOT.mkdir()
    original = read(observer.ROOT / 'preflight.json')
    pre = copy.deepcopy(original)
    pre['cases'] = {name + '_full': row for name, row in original['cases'].items()}
    pre['configuration'] = {'actual_paint_entry_frames': [9580, 9601, 10780, 10801],
        'complete_scanline_frames': [9600, 10800], 'launcher_sha256': sha(Path(__file__).read_bytes()),
        'no_producer_or_shared_helper_source_edited': True}
    pre['inherited_prefix_controls'] = str(observer.ROOT / 'prefix_controls/native_prefix_controls.json')
    pre['inherited_prefix_controls_sha256'] = sha(Path(pre['inherited_prefix_controls']).read_bytes())
    save(ROOT / 'preflight.json', pre)
    (ROOT / 'source_contract.json').write_bytes((observer.ROOT / 'source_contract.json').read_bytes())
    print('V693 predecessor range pinned; frozen original runner/observer unchanged.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('prepare', 'source_full', 'current_full'))
    args = parser.parse_args()
    if args.action == 'prepare':
        prepare()
    else:
        pre = read(ROOT / 'preflight.json')
        assert pre['configuration']['launcher_sha256'] == sha(Path(__file__).read_bytes())
        observer.WATCH = set(range(9580, 9602)) | set(range(10780, 10802))
        observer.ROOT = ROOT
        runner.WATCH = {9600, 10800}
        runner.ROOT = ROOT
        runner.run(args.action)
