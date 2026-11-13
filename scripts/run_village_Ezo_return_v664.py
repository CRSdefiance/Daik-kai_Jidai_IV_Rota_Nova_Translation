"""Repeat the missed Ezo approach after its actual discovery, using coordinates only."""

import argparse
import io
import json
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import native_location_fixture_v519 as location
from scripts.native_village_visits_v664 import relocate
from scripts.run_village_visits_v664 import CAP, ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--story', action='store_true')
    parser.add_argument('--chief', action='store_true')
    args = parser.parse_args()
    pre = read(ROOT / 'preflight.json')
    inputs = [r for r in read(ROOT / 'inputs.json') if r['start'] <= 6001]
    inputs += [{'start': 6601, 'duration': 8, 'buttons': ['RIGHT']},
               {'start': 7001, 'duration': 8, 'buttons': ['A']}]
    inputs += [{'start': 7401 + i * 100, 'duration': 8, 'buttons': ['DOWN']} for i in range(4)]
    inputs.append({'start': 7801, 'duration': 8, 'buttons': ['A']})
    tag = 'Ezo_chief' if args.chief else 'Ezo_story' if args.story else 'Ezo_return'
    final = 12200 if args.chief else 13000 if args.story else 8200
    if args.story or args.chief:
        last = 11002 if args.chief else 12602
        inputs += [{'start': f, 'duration': 8, 'buttons': ['A']} for f in range(8201, last, 400)]
    if args.chief:
        inputs += [{'start': 11401 + i * 100, 'duration': 8, 'buttons': ['DOWN']} for i in range(4)]
        inputs.append({'start': 11801, 'duration': 8, 'buttons': ['A']})
    input_path = ROOT / ('inputs_' + tag + '.json')
    save(input_path, inputs)
    commands = [{'until': 5400, 'location_town': 18}, {'until': 5800}, {'until': 6200},
                {'until': 6400, 'location_town': 18}, {'until': 6800}, {'until': 7400},
                {'until': 8200}]
    if args.story or args.chief:
        commands += [{'until': f} for f in range(8600, final + 1, 400)]
    commands.append({'stop': True})
    command_path = ROOT / ('commands_' + tag + '.jsonl')
    command_path.write_text(''.join(json.dumps(c) + '\n' for c in commands), encoding='utf-8')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    old, stdin = location.relocate, sys.stdin
    location.relocate, sys.stdin = relocate, io.StringIO(command_path.read_text(encoding='utf-8'))
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'],
        '--out', str(CAP / ('village_visits_v664_' + tag)), '--frames', str(final + 1),
        '--inputs-json', str(input_path), '--battery-save', pre['donor'], '--pause-at', '5200',
        '--allow-location-fixtures', '--touchscreen', '--capture-every', '999999',
        '--dump-pause-ram', '--dump-ram', '--dump-native-state']
    try:
        harness.main()
    finally:
        location.relocate, sys.stdin = old, stdin
    print('V664 Ezo return terminal.', flush=True)


if __name__ == '__main__':
    main()
