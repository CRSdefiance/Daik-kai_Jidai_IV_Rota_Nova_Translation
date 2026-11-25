"""Verify the complete Speyer battle tutorial from Hodram's ordinary voyage."""

from argparse import ArgumentParser
from pathlib import Path

from scripts import verify_seville_square_gameplay_20261121 as square


FOLDER = square.runs.VOYAGES['hamburg'][0]
PACKAGE = Path('releases/all_routes_editorial_20261119_hodram_early_confrontations_candidate/verification')
REVIEW = PACKAGE / 'registered_review.json'
STORED = PACKAGE / 'stored_proof.json'
SPEAKERS = {1: 'Hodram Bergstrom', 16: 'Gerhard Adernkatz', 18: 'Charles Rochefort',
            23: 'Manuel Almeida', 29: 'Martin Speyer', 151: 'Sailor'}
TUTORIAL = square.Exchange(1, 5, 29, 32, REVIEW, SPEAKERS)
PROOF = FOLDER / 'verified_speyer_tutorial.json'


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, required=True)
    args = parser.parse_args()
    base, active, native = square.base, square.runs.active, square.native
    report_path = FOLDER / 'capture/capture_report.json'
    journal_path = FOLDER / 'capture/navigation_command_journal.json'
    launch_path = FOLDER / 'discovery_source.json'
    report, journal, launch, plan, release = map(base.load, (report_path,
        journal_path, launch_path, args.plan, active.RELEASE))
    assert not PROOF.exists() and not report['callback_errors'] and report['cold_boot'] and not report['savestate_loaded']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    assert all(row['validation_passed'] for row in journal['commands_received'])
    candidate = base.digest(active.ROM)
    assert candidate == release['candidate_sha256'] == journal['ROM_sha256'] == report['ROM_sha256'] == launch['candidate_sha256']
    battery = report['battery_save_preloaded']
    assert battery['copied_byte_exact_before_cold_boot'] and battery['source'] == launch['donor']
    assert battery['source_sha256'] == launch['donor_sha256'] == base.digest(battery['source'])
    assert base.digest(native.CLEAN) == release['clean_input_sha256']
    clean, current = map(base.NdsImage.open, (native.CLEAN, active.ROM))
    group, = [r for r in base.load(STORED)['groups'] if r['block'] == 29 and r['route'] == 1]
    binding = dict(prior_review=dict(clean_block_sha256=group['source'],
                                    current_block_sha256=group['after'], records=32))
    rows = square.source_rows(clean, current, binding, TUTORIAL)
    assert sum(row['source_selector'] == 254 for row in rows) == 7
    captures = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_navigation.png')}
    assert launch['stop_frame'] < min(plan['panels'])
    assert plan['panels'] == sorted(set(plan['panels'])) and max(plan['panels']) < plan['fleet_warning'] < plan['sea_view']
    controls = {row['frame']: row['command'] for row in journal['commands_received']}
    sequence = [*plan['panels'], plan['fleet_warning'], plan['sea_view']]
    for frame, next_frame in zip(sequence, sequence[1:]):
        assert controls[frame]['buttons'] == ['A'] and controls[frame]['until'] == next_frame
    panels, previews = square.observe(current, rows, captures, plan['panels'], SPEAKERS)
    transitions = {}
    for key, label in (('fleet_warning', 'Speyer fleet warning'), ('sea_view', 'Return to Sea View')):
        transitions[key], image = square.town.read_frame(captures, plan[key])
        previews.append((label, image))
    sheets = []
    for at in range(0, len(previews), 6):
        target = FOLDER / f'speyer_tutorial_{at // 6 + 1}.png'
        square.town.sheet(previews[at:at + 6], target)
        sheets.append(dict(path=str(target), sha256=base.digest(target)))
    base.save(PROOF, dict(candidate_sha256=candidate, route=1, file_path=TUTORIAL.scene, block=TUTORIAL.block,
        ordinary_voyage_trigger=True, encounter_outcome_claimed=False, hardware_verified=False,
        panels=panels, observations=transitions, screenshots=sheets, native_stored_block_hashes=binding['prior_review'],
        new_editorial_credit=0,
        evidence={str(p): base.digest(p) for p in (report_path, journal_path, launch_path, args.plan, REVIEW, STORED)}))
    print('Verified all 32 Speyer battle tutorial panels and seven instruction pages.')


if __name__ == '__main__':
    main()
