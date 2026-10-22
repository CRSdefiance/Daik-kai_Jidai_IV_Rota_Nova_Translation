"""Ordinary five-slot Sailor Info cursor capture; no gameplay or code fixtures."""

import argparse
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/equipment_cursor_v663')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--control', action='store_true')
    args = parser.parse_args()
    ROOT.mkdir(exist_ok=True)
    if not (ROOT / 'preflight.json').exists():
        prior = read('work/analysis/sepia_consumers_v662/preflight.json')
        donor = read(CAP / 'plaque_review_v632_current/capture_report.json')['battery_save_preloaded']
        inputs = read('work/analysis/plaque_current_v574/complete_replay_inputs.json')
        inputs = [r for r in inputs if r['start'] <= 5901]
        inputs += [{'start': 6301 + i * 400, 'duration': 8, 'buttons': [], 'touch': [x, 47]}
                   for i, x in enumerate((30, 80, 128, 176, 224))]
        save(ROOT / 'inputs.json', inputs)
        frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
        save(ROOT / 'preflight.json', {'candidate': prior['candidate'],
            'candidate_sha256': prior['candidate_sha256'], 'release_hashes': prior['release_hashes'],
            'control': 'out/all_routes_combined_v636_candidate.nds',
            'control_sha256': sha(Path('out/all_routes_combined_v636_candidate.nds').read_bytes()),
            'donor': donor['source'], 'donor_sha256': donor['source_sha256'],
            'previous_goal_turn_classification': 'progress: V662 complete native sepia paints and audit updates',
            'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen}})
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    rom = pre['control'] if args.control else pre['candidate']
    assert sha(Path(rom).read_bytes()) == pre['control_sha256' if args.control else 'candidate_sha256']
    frames = [4300, 6300] + [f for start in (6400, 6800, 7200, 7600, 8000) for f in range(start, start + 64)]
    native = [f for start in (6400, 6800, 7200, 7600, 8000) for f in (start, start + 63)]
    folder = CAP / ('equipment_cursor_v663_control' if args.control else 'equipment_cursor_v663_current')
    sys.argv = ['headless_desmume_v193.py', '--rom', rom, '--out', str(folder), '--frames', '8063',
        '--inputs-json', str(ROOT / 'inputs.json'), '--battery-save', pre['donor'],
        '--touchscreen', '--capture-every', '999999', '--capture-at', *map(str, frames)]
    if not args.control:
        sys.argv += ['--dump-capture-ram', '--capture-native-state-at', *map(str, native)]
    harness.main()
    print('V663 terminal ordinary cursor capture', 'control' if args.control else 'current', flush=True)


if __name__ == '__main__':
    main()
