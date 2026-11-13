"""Paired actual Refit navigation and ordinary startup, using isolated saves."""

import argparse
import sys
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/refit_editorial_v831')
CAP = Path('work/emulation_v193')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=('before', 'after', 'newgame_before', 'newgame_after'), required=True)
    args = parser.parse_args()
    version = 829 if args.case.endswith('before') else 831
    rom = Path(f'out/all_routes_combined_v{version}_candidate.nds')
    manifest = read(rom.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == sha(rom.read_bytes())
    folder = CAP / f'refit_editorial_v831_{args.case}'
    assert not folder.exists()
    newgame = args.case.startswith('newgame')
    if newgame:
        inputs = ROOT / 'ordinary_newgame_inputs.json'
        schedule = read('work/analysis/cliff_editorial_v829/ordinary_newgame_inputs.json')
        save(inputs, schedule)
        frames, captures, donor_args = 4000, [1, 60, 180, 1600, 2000, 3200, 4000], []
    else:
        pre = read('work/analysis/refit_help_v712/preflight.json')
        original = Path(pre['donor'])
        assert sha(original.read_bytes()) == pre['donor_sha256']
        donor = ROOT / 'disposable_refit_source.dsv'
        if not donor.exists():
            copy2(original, donor)
        assert sha(donor.read_bytes()) == pre['donor_sha256']
        inputs = ROOT / 'refit_inputs.json'
        schedule = read('work/analysis/refit_help_v713/inputs.json')
        save(inputs, schedule)
        frames = 20600
        captures = read('work/analysis/yard_selection_v705/capture_frames.json') + [20000, 20300, 20600]
        donor_args = ['--battery-save', str(donor)]
        save(ROOT / 'donor_copy.json', {'protected_source': str(original), 'protected_source_sha256': pre['donor_sha256'],
                                      'disposable_source': str(donor), 'disposable_source_sha256': sha(donor.read_bytes()),
                                      'original_donor_never_passed_to_emulator': True,
                                      'historical_save_fixture_scope': 'Existing isolated five-ship Copenhagen test save; not earned fleet or progression.'})
    save(ROOT / f'{args.case}_run_plan.json', {
        'candidate': str(rom), 'candidate_sha256': sha(rom.read_bytes()),
        'out': str(folder), 'frames': frames, 'captures': captures,
        'input_schedule': str(inputs), 'input_sha256': sha(inputs.read_bytes()),
        'new_game_without_save_or_fixture': newgame,
        'no_new_gameplay_RAM_or_code_fixtures': True})
    sys.argv = ['headless_desmume_v193.py', '--rom', str(rom), '--out', str(folder),
                '--frames', str(frames), '--inputs-json', str(inputs), '--touchscreen',
                '--capture-every', '999999', '--capture-at', *map(str, captures),
                '--dump-capture-ram', '--dump-ram', *donor_args]
    harness.main()
    if not newgame:
        assert sha(original.read_bytes()) == pre['donor_sha256']
        assert sha(donor.read_bytes()) == pre['donor_sha256']


if __name__ == '__main__':
    main()
