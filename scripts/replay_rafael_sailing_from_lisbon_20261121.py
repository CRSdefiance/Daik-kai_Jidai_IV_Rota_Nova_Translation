"""Continue Rafael's original Lisbon voyage on the registered testing ROM."""

from argparse import ArgumentParser
from pathlib import Path
import sys

from scripts import headless_desmume_v193 as harness
from scripts import register_hodram_baltic_trade_20261121 as active
from scripts.run_activity_special_live_v989 import GrowingCommands


ROOT = Path('work/analysis/rafael_sailing_lisbon_gameplay_20261121')
PRIOR = Path('work/rafael_lisbon_return_20261119/capture/capture_report.json')
BINDING = Path('translations/editorial_checkpoints/SharedText_20261110_v1/rafael_sailing_lisbon_entry_20261121_v1.json')
PAUSE = 55540
base = active.base


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT)
    args = parser.parse_args()
    release, prior, binding = map(base.load, (active.RELEASE, PRIOR, BINDING))
    assert base.digest(active.ROM) == release['candidate_sha256'] == binding['candidate_sha256']
    assert base.digest(active.MANIFEST) == release['manifest_sha256']
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(PRIOR) == binding['historical_replay_sha256']
    assert prior['cold_boot'] and not prior['savestate_loaded'] and not prior['callback_errors']
    assert not any(value for key, value in prior.items() if key.startswith('synthetic_'))
    donor = prior['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    inputs = [row for row in prior['scripted_input_schedule'] if row['start'] <= PAUSE]
    assert inputs and all(row['start'] + row['duration'] <= PAUSE + 1 for row in inputs)
    args.out.mkdir(parents=True)
    prefix, journal = (args.out / name for name in ('arrival_inputs.json', 'navigation.jsonl'))
    base.save(prefix, inputs)
    base.save(args.out / 'arrival_source.json', dict(candidate_sha256=release['candidate_sha256'],
        prior_report=str(PRIOR), prior_report_sha256=base.digest(PRIOR), binding_sha256=base.digest(BINDING),
        donor=donor['source'], donor_sha256=donor['source_sha256'], input_schedule_sha256=base.digest(prefix),
        stop_frame=PAUSE))
    journal.touch(exist_ok=False)
    stream = GrowingCommands(journal)
    previous = sys.stdin, sys.argv
    try:
        sys.stdin = stream
        sys.argv = [harness.__file__, '--rom', str(active.ROM), '--out', str(args.out / 'capture'),
                    '--frames', '93000', '--inputs-json', str(prefix), '--press-start', '-1',
                    '--touchscreen', '--battery-save', donor['source'], '--capture-every', '999999',
                    '--capture-at', '50165', '52945', '--pause-at', str(PAUSE), '--dump-pause-ram', '--dump-ram']
        harness.main()
    finally:
        sys.stdin, sys.argv = previous
        stream.close()
    assert base.digest(donor['source']) == donor['source_sha256']


if __name__ == '__main__':
    main()
