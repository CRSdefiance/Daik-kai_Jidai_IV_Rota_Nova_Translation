"""Continue ordinary Square voyages on the registered ROM from verified inputs."""

from argparse import ArgumentParser
from pathlib import Path
import sys

from scripts import headless_desmume_v193 as harness
from scripts import register_refit_sailing_parallel_routes_20261121 as active
from scripts.run_activity_special_live_v989 import GrowingCommands


ROOT = Path('work/analysis/seville_square_gameplay_20261121')
PRIOR = Path('work/rafael_lisbon_return_20261119/capture/capture_report.json')
DISCOVERY = 53655
base = active.base
VOYAGES = {
    'seville': (ROOT, PRIOR, DISCOVERY, (50165, 52945, 53415)),
    'hamburg': (
        Path('work/analysis/hamburg_square_gameplay_20261121'),
        Path('out/additional_square_trend_gameplay_20261121/hamburg/capture/capture_report.json'),
        10710,
        (3760, 8620, 9010),
    ),
}


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--town', choices=VOYAGES, default='seville')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    default_folder, history, pause, samples = VOYAGES[args.town]
    folder = args.out or default_folder
    release, prior = map(base.load, (active.RELEASE, history))
    candidate = base.digest(active.ROM)
    assert candidate == release['candidate_sha256'] and release['clean_input_patch_byte_exact']
    assert release['registry_sha256'] == base.digest(base.REGISTRY)
    assert prior['cold_boot'] and not prior['savestate_loaded'] and not prior['callback_errors']
    donor = prior['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    assert not any(value for key, value in prior.items() if key.startswith('synthetic_'))
    inputs = [row for row in prior['scripted_input_schedule'] if row['start'] <= pause]
    assert all(row['start'] + row['duration'] <= pause + 1 for row in inputs)
    folder.mkdir(parents=True)
    prefix = folder / 'discovery_inputs.json'
    journal = folder / 'navigation.jsonl'
    base.save(prefix, inputs)
    base.save(folder / 'discovery_source.json', dict(candidate_sha256=candidate,
        prior_report=str(history), prior_report_sha256=base.digest(history), donor=donor['source'],
        donor_sha256=donor['source_sha256'], input_schedule_sha256=base.digest(prefix), stop_frame=pause))
    journal.touch(exist_ok=False)
    stream = GrowingCommands(journal)
    original_argv, original_stdin = sys.argv, sys.stdin
    try:
        sys.stdin = stream
        sys.argv = [harness.__file__, '--rom', str(active.ROM), '--out', str(folder / 'capture'),
                    '--frames', '90000', '--inputs-json', str(prefix), '--press-start', '-1',
                    '--touchscreen', '--battery-save', donor['source'], '--capture-every', '999999',
                    '--capture-at', *map(str, samples), '--pause-at', str(pause),
                    '--dump-pause-ram', '--dump-ram']
        harness.main()
    finally:
        sys.argv, sys.stdin = original_argv, original_stdin
        stream.close()
    assert base.digest(donor['source']) == donor['source_sha256']


if __name__ == '__main__':
    main()
