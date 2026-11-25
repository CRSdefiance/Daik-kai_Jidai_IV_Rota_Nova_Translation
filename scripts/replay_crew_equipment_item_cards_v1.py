"""Exercise the original Lisbon Items menu with a naturally held copy of Marco Polo."""

import sys
from types import FunctionType

from scripts import headless_desmume_v193 as harness
from scripts import run_diplomatic_outcome_startup_v2 as startup
from scripts import stage_armor_item_cards_v1 as parent
from scripts import stage_crew_equipment_item_cards_v1 as current
from scripts.replay_setup_save_equipment_v2 import REFERENCE

stage = current.previous
ROOT, ROM, PREP = current.ROOT, current.ROM, current.PREP
ITEM = 88
ITEMS, STARTUP = ROOT / 'items_menu', ROOT / 'own_startup'
HOLDS = (8400, 9600, 10000, 10060, 10400, 10800)


def cold_boot():
    env = vars(startup) | dict(EVIDENCE=PREP, ROM=ROM, STARTUP=STARTUP,
                               PRIOR=parent.ROOT / 'own_startup')
    FunctionType(startup.main.__code__, env)()


def items():
    prepared, reference = map(stage.load, (PREP, REFERENCE))
    assert stage.digest(ROM) == prepared['research_ROM_sha256']
    donor = reference['battery_save_preloaded']
    assert stage.digest(donor['source']) == donor['source_sha256']
    assert donor['copied_byte_exact_before_cold_boot'] and reference['cold_boot']
    assert not reference['savestate_loaded'] and not reference['callback_errors']
    assert not any(value for key, value in reference.items() if key.startswith('synthetic_'))
    ITEMS.mkdir()
    inputs = ITEMS / 'inputs.json'
    events = [row for row in reference['scripted_input_schedule'] if row['start'] < 10000]
    assert events[-1]['buttons'] == ['RIGHT']
    events.extend(dict(start=frame, duration=8, buttons=['B']) for frame in (10061, 10401))
    stage.save(inputs, events)
    original = sys.argv
    try:
        sys.argv = [sys.argv[0], '--rom', str(ROM), '--out', str(ITEMS / 'capture'),
                    '--frames', '10801', '--inputs-json', str(inputs), '--battery-save', donor['source'],
                    '--touchscreen', '--capture-every', '999999', '--capture-at', *map(str, HOLDS)]
        harness.main()
    finally:
        sys.argv = original
    assert stage.digest(donor['source']) == donor['source_sha256']
    report = ITEMS / 'capture/capture_report.json'
    stage.save(ITEMS / 'terminal.json', dict(report=str(report), report_sha256=stage.digest(report),
        candidate_sha256=prepared['research_ROM_sha256'], donor_sha256=donor['source_sha256'],
        inputs_sha256=stage.digest(inputs), unchanged_original_save=True))


if __name__ == '__main__':
    assert sys.argv[1:] in (['items'], ['startup'])
    (items if sys.argv[1] == 'items' else cold_boot)()
