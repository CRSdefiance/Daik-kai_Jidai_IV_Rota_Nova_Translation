"""Reach Amsterdam on the current ROM and observe ordinary town interactions."""

import argparse
import json
import sys
from pathlib import Path

from scripts import headless_desmume_v193 as harness
from scripts.run_activity_special_live_v988 import GrowingCommands
from scripts.verify_rafael_custom_name_20261119 import digest, read

PREFIX = Path('work/amsterdam_town_summary_20261119/square/capture/capture_report.json')
REGISTERED = Path('releases/all_routes_editorial_20261119_captain_name_latin_candidate_v2/verification/registered_release_verification.json')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--prefix', type=Path, default=PREFIX)
    args = parser.parse_args()
    folder = args.output
    journal = folder / 'navigation.jsonl'
    capture = folder / 'capture'
    assert journal.is_file() and not capture.exists()
    seen, registered = map(read, (args.prefix, REGISTERED))
    rom = Path(registered['candidate'])
    start = seen['frames']
    assert 16150 <= start < 40000 and seen['cold_boot'] and not seen.get('battery_save_preloaded')
    assert not seen['savestate_loaded'] and not seen['callback_errors']
    assert not any(v for k, v in seen.items() if k.startswith('synthetic_'))
    assert all(row['start'] + row.get('duration', 5) <= start + 1 for row in seen['scripted_input_schedule'])
    assert digest(rom.read_bytes()) == registered['candidate_sha256']
    inputs = folder / 'original_inputs.json'
    inputs.write_text(json.dumps(seen['scripted_input_schedule'], indent=2) + '\n', encoding='utf-8')
    stream = GrowingCommands(journal)
    saved_argv, saved_stdin = sys.argv, sys.stdin
    try:
        sys.stdin = stream
        sys.argv = [harness.__file__, '--rom', str(rom), '--out', str(capture), '--frames', '40000',
                    '--press-start', '-1', '--touchscreen', '--capture-every', '999999', '--pause-at', str(start),
                    '--dump-pause-ram', '--inputs-json', str(inputs)]
        harness.main()
    finally:
        sys.argv, sys.stdin = saved_argv, saved_stdin
        stream.close()
    finished = read(capture / 'capture_report.json')
    assert finished['ROM_sha256'] == registered['candidate_sha256']
    assert finished['cold_boot'] and not finished['savestate_loaded'] and not finished.get('battery_save_preloaded')
    assert not finished['callback_errors'] and not any(v for key, v in finished.items() if key.startswith('synthetic_'))


if __name__ == '__main__':
    main()
