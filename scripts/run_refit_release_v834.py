"""Ordinary Rename/startup and isolated qualified-helper scene navigation."""

import argparse
import sys
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import run_refit_fixture_adapter_v834 as adapter
from scripts.prepare_refit_release_v834 import ROOT
from scripts.verify_village_wrap_v608 import read, save

CAP = Path('work/emulation_v193')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=('helper_before', 'helper_after', 'rename_after', 'newgame_after'), required=True)
    args = parser.parse_args()
    version = 831 if args.case.endswith('before') else 834
    rom = Path(f'out/all_routes_combined_v{version}_candidate.nds')
    assert read(rom.with_suffix('.manifest.json'))['candidate_sha256'] == sha(rom.read_bytes())
    folder = CAP / f'refit_dialogue_v834_{args.case}'
    assert not folder.exists()
    donor = None
    donor_args = []
    if args.case != 'newgame_after':
        old = read('work/analysis/refit_editorial_v831/donor_copy.json')
        source = Path(old['disposable_source'])
        assert sha(source.read_bytes()) == old['disposable_source_sha256']
        donor = ROOT / f'disposable_{args.case}_source.dsv'
        assert not donor.exists()
        copy2(source, donor)
        donor_args = ['--battery-save', str(donor)]
    if args.case.startswith('helper'):
        events = [r for r in read('work/analysis/yard_selection_v705/full_inputs.json') if r['start'] <= 13101]
        events += [{'start': 13401, 'duration': 8, 'buttons': ['X']}]
        frames = 40000
        captures = [1, 60, 180, 3200, 11900, 12200, 12500, 12800, 13100, 13400, 13800,
                    14200, 14700, 15100, 15500, 15900, 16300, 16700, 17100, 17500, 17900, 18300]
        more = ['--pause-at', '3200', '--dump-pause-ram', '--allow-refit-helper-fixtures']
    elif args.case == 'rename_after':
        events = read('work/analysis/refit_dialogue_v832/name_entry_inputs.json')
        frames = 14600
        captures = read('work/analysis/refit_dialogue_v832/name_entry_run_plan.json')['captures']
        more = []
    else:
        events = read('work/analysis/cliff_editorial_v829/ordinary_newgame_inputs.json')
        frames, captures, more = 4000, [1, 60, 180, 1600, 2000, 3200, 4000], []
    inputs = ROOT / f'{args.case}_inputs.json'
    save(inputs, events)
    save(ROOT / f'{args.case}_run_plan.json', {
        'candidate': str(rom), 'candidate_sha256': sha(rom.read_bytes()), 'folder': str(folder),
        'frames_budget': frames, 'capture_at': captures, 'inputs': str(inputs), 'input_sha256': sha(inputs.read_bytes()),
        'disposable_source': str(donor) if donor else None, 'source_sha256': sha(donor.read_bytes()) if donor else None,
        'source_donor_never_passed_to_emulator': True,
        'helper_prerequisite_fixture_only_if_explicitly_requested_at_pause': args.case.startswith('helper')})
    sys.argv = ['headless_desmume_v193.py', '--rom', str(rom), '--out', str(folder),
                '--frames', str(frames), '--inputs-json', str(inputs), '--touchscreen',
                '--capture-every', '999999', '--capture-at', *map(str, captures),
                '--dump-capture-ram', '--dump-ram', *donor_args, *more]
    (adapter.main if args.case.startswith('helper') else harness.main)()
    if donor:
        assert sha(donor.read_bytes()) == old['disposable_source_sha256']


if __name__ == '__main__':
    main()
