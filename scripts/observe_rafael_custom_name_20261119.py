"""Observe normal captain name entry and its use in Rafael's opening dialogue."""

import sys
from pathlib import Path

from scripts import headless_desmume_v193 as harness
from scripts import register_deck_view_guidance_20261119 as current
from scripts.run_activity_special_live_v988 import GrowingCommands

base = current.base
ROOT = Path('work/rafael_custom_name_20261119')
CAPTURE = ROOT / 'capture'
JOURNAL = ROOT / 'navigation.jsonl'
REFERENCE = Path('work/analysis/papal_trade_route_runs_v7625/route0/ordinary_NewGame_inputs.json')
START = 2050


def main():
    assert JOURNAL.is_file() and not CAPTURE.exists()
    proof = base.load(current.RELEASE)
    assert base.digest(current.ROM) == proof['candidate_sha256']
    inputs = ROOT / 'new_game_prefix.json'
    prefix = [row for row in base.load(REFERENCE) if row['start'] + row['duration'] <= START]
    assert [row['buttons'] for row in prefix] == [['START'], ['A'], ['A']]
    base.save(inputs, prefix)
    original, arguments = sys.stdin, sys.argv
    commands = GrowingCommands(JOURNAL)
    try:
        sys.stdin = commands
        sys.argv = [harness.__file__, '--rom', str(current.ROM), '--out', str(CAPTURE), '--frames', '18000',
            '--inputs-json', str(inputs), '--press-start', '-1', '--touchscreen', '--capture-every', '999999',
            '--pause-at', str(START), '--dump-pause-ram']
        harness.main()
    finally:
        sys.stdin, sys.argv = original, arguments
        commands.close()
    report = base.load(CAPTURE / 'capture_report.json')
    assert report['ROM_sha256'] == proof['candidate_sha256'] and report['cold_boot'] and not report['savestate_loaded']
    assert not report.get('battery_save_preloaded') and not report['callback_errors']


if __name__ == '__main__':
    main()
