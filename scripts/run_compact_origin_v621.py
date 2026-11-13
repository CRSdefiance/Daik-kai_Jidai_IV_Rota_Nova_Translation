"""Replay the real duel and ordinary no-fixture Market on the integrated fix."""

import argparse
import json
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness

ROOT = Path('work/analysis/compact_origin_v621')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v621_candidate.nds')
DONOR = Path('work/analysis/lubeck_voyage_v421/donor_test_copy.dsv')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('context', choices=('duel', 'market'))
    context = parser.parse_args().context
    manifest = json.loads(ROM.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    assert manifest['profile'] == 'all-routes-unified-v621'
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    if context == 'duel':
        assert sha(DONOR.read_bytes()) == '97997ce6fbeda9ff0272c08d7420e96676240b017e0037b721ed7c5eb52770d5'
        plan = Path('work/analysis/battle_contexts_v620/sea_encounter_prefix.json')
        frames, captures = 60000, [20000, 20400]
    else:
        previous = json.loads((CAP / 'regional_missions_v617_market/capture_report.json').read_text(encoding='utf-8'))
        plan = ROOT / 'ordinary_market_inputs.json'
        plan.write_text(json.dumps(previous['scripted_input_schedule'], indent=2) + '\n')
        frames, captures = previous['frames'], sorted({r['frame'] for r in previous['frames_captured']})
    argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(CAP / ('compact_origin_v621_' + context)),
            '--frames', str(frames), '--inputs-json', str(plan), '--capture-every', '999999',
            '--capture-at', *map(str, captures), '--touchscreen']
    if context == 'duel':
        argv += ['--battery-save', str(DONOR), '--pause-at', '20400', '--dump-capture-ram',
                 '--dump-pause-ram', '--dump-native-state', '--allow-battle-fixtures']
    sys.argv = argv
    harness.main()


if __name__ == '__main__':
    main()
