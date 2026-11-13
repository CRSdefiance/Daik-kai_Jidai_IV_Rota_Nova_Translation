"""Cold-boot the staged ROM and open the native Items display with one isolated weapon."""

from io import StringIO
import json
import sys
from types import FunctionType

from scripts import headless_desmume_v193 as harness
from scripts import native_inventory_fixture_v481 as fixture
from scripts import run_diplomatic_outcome_startup_v2 as startup
from scripts import stage_source_item_cards_and_coin_v2 as parent
from scripts import stage_utility_weapon_item_cards_v1 as stage
from scripts.replay_setup_save_equipment_v2 import REFERENCE


ITEM = 24
ITEMS = stage.ROOT / 'items_menu'
STARTUP = stage.ROOT / 'own_startup'
MENU_FRAMES = (9600, 9660)
COMMANDS = (
    dict(until=8800, inventory_items=[ITEM], buttons=['X'], duration=8),
    dict(until=9200, touch=[143, 54], duration=8),
    dict(until=9600, buttons=['A'], duration=8),
    dict(until=9660),
    dict(until=10000, buttons=['B'], duration=8),
    dict(until=10400, buttons=['B'], duration=8),
    dict(stop=True),
)


def cold_boot():
    env = vars(startup) | dict(EVIDENCE=stage.PREP, ROM=stage.ROM, STARTUP=STARTUP,
                               PRIOR=parent.ROOT / 'own_startup')
    FunctionType(startup.main.__code__, env)()


def items():
    prepared, reference = map(stage.load, (stage.PREP, REFERENCE))
    assert stage.digest(stage.ROM) == prepared['research_ROM_sha256']
    donor = reference['battery_save_preloaded']
    assert stage.digest(donor['source']) == donor['source_sha256']
    assert donor['copied_byte_exact_before_cold_boot'] and reference['cold_boot']
    assert not reference['savestate_loaded'] and not reference['callback_errors']
    assert not any(value for key, value in reference.items() if key.startswith('synthetic_'))
    original = stage.load(stage.RELEASE)
    assert stage.digest(original['candidate']) == original['candidate_sha256']
    before, arm = (stage.NdsImage.open(path).read_file(stage.ARM) for path in (original['candidate'], stage.ROM))
    assert fixture.sha(arm) == prepared['research_ARM9_sha256']
    assert all(before[lo:hi] == arm[lo:hi] for lo, hi in (
        (0x49DE8, 0x4A200), (0x4A448, 0x4A66C), (0xCB190, 0xCB19C),
    ))
    use_original_transfer = FunctionType(fixture.transfer.__code__, vars(fixture) | {
        'SUPPORTED_ARM_SHA': (prepared['research_ARM9_sha256'],),
    })
    ITEMS.mkdir()
    inputs = ITEMS / 'inputs.json'
    commands = ITEMS / 'commands.json'
    stage.save(inputs, [row for row in reference['scripted_input_schedule'] if row['start'] < 8400])
    stage.save(commands, list(COMMANDS))
    original_args, original_input, original_transfer = sys.argv, sys.stdin, fixture.transfer
    try:
        fixture.transfer = use_original_transfer
        sys.stdin = StringIO(''.join(json.dumps(row) + '\n' for row in COMMANDS))
        sys.argv = [sys.argv[0], '--rom', str(stage.ROM), '--out', str(ITEMS / 'capture'),
                    '--frames', '10401', '--inputs-json', str(inputs), '--battery-save', donor['source'],
                    '--touchscreen', '--capture-every', '999999', '--pause-at', '8400',
                    '--allow-inventory-fixtures', '--dump-ram']
        harness.main()
    finally:
        sys.argv, sys.stdin, fixture.transfer = original_args, original_input, original_transfer
    assert stage.digest(donor['source']) == donor['source_sha256']
    report = ITEMS / 'capture/capture_report.json'
    stage.save(ITEMS / 'terminal.json', dict(report=str(report), report_sha256=stage.digest(report),
        candidate_sha256=prepared['research_ROM_sha256'], donor_sha256=donor['source_sha256'],
        commands_sha256=stage.digest(commands), unchanged_original_save=True))


if __name__ == '__main__':
    assert sys.argv[1:] in (['items'], ['startup'])
    (items if sys.argv[1] == 'items' else cold_boot)()
