"""Original regional mission controls and ordinary full-ROM regression."""

import argparse
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/regional_missions_v617')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v617_candidate.nds')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('context', choices=('actual', 'market'))
    args = parser.parse_args()
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['profile'] == 'all-routes-unified-v617' and sha(ROM.read_bytes()) == manifest['candidate_sha256']
    native = read(ROOT / 'native_guarded_assignment_proof.json')
    assert sha(NdsImage.open(ROM).read_file('/__arm9__.bin')) == native['target_ARM9_sha256']
    if args.context == 'actual':
        plan = ROOT / 'complete_V616_control_inputs.json'
        frames, captures = 60000, [7000, 7800, 9800, 10200, 10600, 11800]
    else:
        previous = read(CAP / 'regional_ui_v616_market/capture_report.json')
        plan = ROOT / 'ordinary_market_inputs.json'
        save(plan, previous['scripted_input_schedule'])
        frames, captures = previous['frames'], sorted({r['frame'] for r in previous['frames_captured']})
    argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(CAP / ('regional_missions_v617_' + args.context)),
            '--frames', str(frames), '--inputs-json', str(plan), '--touchscreen', '--capture-every', '999999',
            '--capture-at', *map(str, captures)]
    if args.context == 'actual':
        fixture = read('work/analysis/regional_fleet_v615/formed_fixture_manifest.json')
        assert sha(Path(fixture['fixture']).read_bytes()) == fixture['fixture_sha256']
        argv += ['--battery-save', fixture['fixture'], '--pause-at', '11800', '--dump-capture-ram',
                 '--dump-pause-ram', '--allow-regional-finance-fixtures']
    sys.argv = argv
    harness.main()


if __name__ == '__main__':
    main()
