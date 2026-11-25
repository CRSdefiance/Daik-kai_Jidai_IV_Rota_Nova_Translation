"""Cold-boot the integrated help correction and ordinary New Game regression."""

import argparse
import sys
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.run_room_gender_v694 import CAP
from scripts.run_room_gender_v694 import ROM as OLD_ROM
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/refit_help_v712')
ROM = Path('out/all_routes_combined_v712_candidate.nds')


def prepare():
    pre = read(ROOT / 'preflight.json')
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['profile'] == 'all-routes-unified-v712'
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches']) == 470
    old = read('work/analysis/maria_intro_v684/preflight.json')
    intro = read('work/analysis/maria_intro_v684/run_config.json')
    cases = {}
    for case in ('yard', 'newgame', 'newgame_control'):
        selected = OLD_ROM if case.endswith('control') else ROM
        if case == 'yard':
            config = {'ROM': str(selected), 'ROM_sha256': sha(selected.read_bytes()),
                'frames': 19700, 'donor': pre['donor'], 'donor_sha256': pre['donor_sha256'],
                'inputs': 'work/analysis/yard_selection_v705/full_inputs.json',
                'capture_frames': read('work/analysis/yard_selection_v705/capture_frames.json')}
        else:
            unlock = deepcopy(read('work/analysis/maria_intro_v684/unlock_manifest.json'))
            unlock.update(production_ROM=str(selected), production_ROM_sha256=sha(selected.read_bytes()),
                current_test_scope='V712 integration regression: ordinary Maria New Game through Hangzhou using existing isolated system unlock; not earned unlock or route completion.')
            mp = ROOT / f'{case}_unlock_manifest.json'
            save(mp, unlock)
            config = {'ROM': str(selected), 'ROM_sha256': sha(selected.read_bytes()),
                'frames': intro['frames'], 'donor': old['donor'], 'donor_sha256': old['donor_sha256'],
                'inputs': intro['inputs'], 'capture_frames': intro['capture_frames'],
                'unlock_manifest': str(mp), 'unlock_manifest_sha256': sha(mp.read_bytes())}
        config['inputs_sha256'] = sha(Path(config['inputs']).read_bytes())
        assert sha(Path(config['donor']).read_bytes()) == config['donor_sha256']
        cases[case] = config
    save(ROOT / 'display_run_config.json', {'cases': cases,
        'runner_sha256': sha(Path(__file__).read_bytes()),
        'registry_sha256': sha(Path('translations/release_stack.json').read_bytes()),
        'current_manifest_sha256': sha(ROM.with_suffix('.manifest.json').read_bytes()),
        'current_candidate_sha256': sha(ROM.read_bytes()),
        'no_runtime_location_inventory_funds_health_story_outcome_or_picture_fixture': True})
    print('V712 integrated release/donors and three regression runs frozen.', flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--case', choices=('yard', 'newgame', 'newgame_control'))
    args = parser.parse_args()
    if args.prepare:
        prepare()
        return
    config = read(ROOT / 'display_run_config.json')
    assert config['runner_sha256'] == sha(Path(__file__).read_bytes())
    assert config['registry_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    case = config['cases'][args.case]
    for key in ('ROM', 'donor', 'inputs'):
        assert sha(Path(case[key]).read_bytes()) == case[key + '_sha256']
    folder = CAP / f'refit_help_v712_{args.case}'
    assert not folder.exists()
    sys.argv = ['headless_desmume_v193.py', '--rom', case['ROM'], '--out', str(folder),
        '--frames', str(case['frames']), '--inputs-json', case['inputs'], '--touchscreen',
        '--battery-save', case['donor'], '--capture-every', '999999',
        '--capture-at', *map(str, case['capture_frames']), '--dump-capture-ram', '--dump-ram']
    if 'unlock_manifest' in case:
        assert sha(Path(case['unlock_manifest']).read_bytes()) == case['unlock_manifest_sha256']
        sys.argv += ['--allow-gallery-fixtures', '--gallery-save-fixture-manifest', case['unlock_manifest']]
    harness.main()
    print('V712 terminal', args.case, case['frames'], flush=True)


if __name__ == '__main__':
    main()
