"""Independent ordinary docking captures with one disclosed proximity fixture each."""

import argparse
import io
import json
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import native_location_fixture_v519 as location
from scripts.native_village_visits_v664 import relocate
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/village_visits_v664')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('village', type=int)
    parser.add_argument('--prepare-only', action='store_true')
    parser.add_argument('--chief', action='store_true')
    args = parser.parse_args()
    assert 0 <= args.village < 24
    ROOT.mkdir(exist_ok=True)
    if not (ROOT / 'preflight.json').exists():
        prev = read('work/analysis/equipment_cursor_v663/preflight.json')
        frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
        inputs = read('work/analysis/village_backgrounds_v643/complete_replay_inputs.json')
        save(ROOT / 'inputs.json', [r for r in inputs if r['start'] <= 6801])
        save(ROOT / 'preflight.json', {'candidate': prev['candidate'], 'candidate_sha256': prev['candidate_sha256'],
            'release_hashes': prev['release_hashes'], 'donor': prev['donor'], 'donor_sha256': prev['donor_sha256'],
            'previous_goal_turn_classification': 'progress: V663 full equipment scenes and source scanline transitions',
            'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen}})
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    if args.prepare_only:
        print('V664 shared preflight ready; no emulator started.')
        return
    suffix = f'chief_{args.village:02d}' if args.chief else f'{args.village:02d}'
    folder = CAP / ('village_visits_v664_' + suffix)
    commands = [{'until': 5400, 'location_town': args.village}, {'until': 5800}, {'until': 6200},
                {'until': 6600}, {'until': 7200}]
    final, input_path = 7200, ROOT / 'inputs.json'
    if args.chief:
        # Original 789AC..78A54 modulo filters determine the visible menu rows.
        count = 3 + int(args.village % 2 == 0) + int(args.village % 3 == 0) + int(args.village % 5 == 0)
        inputs = read(input_path)
        inputs += [{'start': 7201 + i * 100, 'duration': 8, 'buttons': ['DOWN']} for i in range(count - 1)]
        accept = 7201 + (count - 1) * 100
        inputs.append({'start': accept, 'duration': 8, 'buttons': ['A']})
        input_path = ROOT / ('inputs_' + suffix + '.json')
        save(input_path, inputs)
        final = accept + 399
        commands.append({'until': final})
    commands.append({'stop': True})
    command_path = ROOT / ('commands_' + suffix + '.jsonl')
    command_path.write_text(''.join(json.dumps(c) + '\n' for c in commands), encoding='utf-8')
    old, stdin = location.relocate, sys.stdin
    location.relocate, sys.stdin = relocate, io.StringIO(command_path.read_text(encoding='utf-8'))
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out', str(folder),
        '--frames', str(final + 1), '--inputs-json', str(input_path), '--battery-save', pre['donor'],
        '--pause-at', '5200', '--allow-location-fixtures', '--touchscreen', '--capture-every', '999999',
        '--dump-pause-ram', '--dump-ram', '--dump-native-state']
    try:
        harness.main()
    finally:
        location.relocate, sys.stdin = old, stdin
    print('V664 terminal village proximity/docking run:', args.village, flush=True)


if __name__ == '__main__':
    main()
