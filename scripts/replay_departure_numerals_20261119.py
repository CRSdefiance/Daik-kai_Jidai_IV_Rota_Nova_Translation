"""Replay the exact recorded departure with the cumulative numeral fix."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import check_rafael_voyage_ceuta_20261119 as precedent
from scripts import headless_desmume_v193 as harness
from scripts import observe_rafael_lisbon_return_20261119 as ordinary
from scripts import stage_departure_numerals_20261119 as stage

base = stage.base
SOURCE = ordinary.CAPTURE / 'capture_report.json'
CAPTURE = stage.ROOT / 'ordinary_departure'
STARTUP_DIR = stage.ROOT / 'own_startup'
STARTUP = stage.ROOT / 'own_startup_verification.json'
INPUT = stage.ROOT / 'ordinary_inputs.json'
FRAMES = (50165, 50395, 50705, 51905, 52625, 52875, 53165, 53415)
END = FRAMES[-1] + 1


def capture():
    assert not CAPTURE.exists() and not INPUT.exists()
    previous = base.load(stage.parent.RELEASE)
    prior_hash = base.load(ordinary.active.RELEASE)['candidate_sha256']
    assert previous['predecessor']['candidate_sha256'] == prior_hash
    old, stored = map(base.load, (SOURCE, stage.PROOF))
    assert old['ROM_sha256'] == prior_hash and old['cold_boot'] and not old['savestate_loaded']
    assert base.digest(stage.ROM) == stored['candidate_sha256'] and not old['callback_errors']
    donor = old['battery_save_preloaded']
    assert base.digest(donor['source']) == donor['source_sha256'] and donor['copied_byte_exact_before_cold_boot']
    inputs = [r for r in old['scripted_input_schedule'] if r['start'] + r['duration'] <= END]
    assert inputs and all(any(f['frame'] == frame for f in old['frames_captured']) for frame in FRAMES)
    base.save(INPUT, inputs)
    import sys
    prior = sys.argv
    sys.argv = [harness.__file__, '--rom', str(stage.ROM), '--out', str(CAPTURE), '--frames', str(END),
        '--press-start', '-1', '--touchscreen', '--battery-save', donor['source'], '--inputs-json', str(INPUT),
        '--capture-every', '999999', '--capture-at', *map(str, FRAMES), '--dump-capture-ram']
    try:
        harness.main()
    finally:
        sys.argv = prior
    assert base.digest(donor['source']) == donor['source_sha256']


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('capture', 'capture-startup', 'startup', 'patch'))
    action = parser.parse_args().action
    scope = vars(precedent) | dict(stage=stage, STARTUP=STARTUP, STARTUP_DIR=STARTUP_DIR)
    if action == 'capture':
        capture()
    elif action == 'patch':
        FunctionType(precedent.patch.__code__, scope)()
    else:
        FunctionType(precedent.startup.__code__, scope)(action == 'capture-startup')
