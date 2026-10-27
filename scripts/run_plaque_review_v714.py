"""Cold boot current plaques through ordinary saved-game controls."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.prepare_plaque_review_v714 import CAP, ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for key in ('donor', 'inputs'):
        assert sha(Path(pre[key]).read_bytes()) == pre[key + '_sha256']
    assert not CAP.exists()
    CAP.mkdir(parents=True)
    save(CAP / 'run_contract.json', {'preflight_sha256': sha((ROOT / 'preflight.json').read_bytes()),
        'runner_sha256': sha(Path(__file__).read_bytes()), 'ordinary_controls_no_live_fixtures': True})
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out', str(CAP),
        '--frames', str(pre['frames']), '--inputs-json', pre['inputs'], '--touchscreen',
        '--battery-save', pre['donor'], '--capture-every', '999999',
        '--capture-at', *map(str, pre['capture_frames'])]
    harness.main()
    print('V714 current plaque run terminal.', flush=True)


if __name__ == '__main__':
    main()
