"""Exercise the original Mikhail branch from a copied Maria save in Nagasaki."""

from inspect import getsource
from io import StringIO
import json
from pathlib import Path
from struct import unpack_from
import sys
from types import FunctionType, SimpleNamespace

from unicorn.arm_const import UC_ARM_REG_R0

from scripts import headless_desmume_v193 as harness
from scripts import native_inventory_fixture_v481 as inventory
from scripts import replay_item_production_advice_v1 as previous
from scripts import stage_crew_equipment_advice_v2 as candidate
from scripts.native_call_abi_v764 import call
from scripts.source_locked_derivation_v5118 import checked_text


base = candidate.first.base
stage = SimpleNamespace(**(vars(base) | vars(candidate) | {
    'PREP': candidate.PROOF,
    'RELEASE': candidate.first.parent.RELEASE,
    'ARM': candidate.first.editorial.previous.ARM,
    'review': candidate.first.editorial.previous,
}))
PRIOR = candidate.first.parent.TEST.parent / 'weapon_armor_advice_staged_20261111_v2' / 'own_startup'
STARTUP = stage.ROOT / 'own_startup'
ITEMS = stage.ROOT / 'items_advice'
REFERENCE = Path('work/emulation_v193/conditions_live_v520/capture_report.json')
DONOR_SHA = 'fbae21aa2c5a695bde0eddfc10a3bbeb80d01478bd6a9ed743d824595dc3096e'
FLAG_OWNER, FLAG_INDEX = previous.FLAG_OWNER, previous.FLAG_INDEX
ITEM_IDS = (107, 110)
ITEM_NAMES = ('Illustrated Bible', 'Gupta Spirit Beast')
COMMANDS = (
    dict(until=3800, inventory_items=list(ITEM_IDS), buttons=['X'], duration=8),
    dict(until=4200, touch=[143, 54], duration=8),
    dict(until=4600, buttons=['A'], duration=8),
    dict(until=4900, buttons=['RIGHT'], duration=8),
    dict(until=5200, buttons=['X'], duration=8),
    dict(until=5500, buttons=['A'], duration=8),
    dict(until=5800, buttons=['RIGHT'], duration=8),
    dict(until=6100, buttons=['X'], duration=8),
    dict(until=6400, buttons=['A'], duration=8),
    dict(until=6800, buttons=['B'], duration=8),
    dict(until=7200, buttons=['B'], duration=8),
    dict(stop=True),
)


def inventory_fixture(parent_arm, arm, arm_sha):
    assert parent_arm[0x23C60:0x23CE4] == arm[0x23C60:0x23CE4]
    transfer_code = checked_text(getsource(inventory.transfer), {
        'category not in (2, 3, 4)': 'category != 4',
    })
    env = vars(inventory) | {'SUPPORTED_ARM_SHA': (arm_sha,)}
    exec(compile(transfer_code, __file__ + '::two-crew-equipment-items', 'exec'), env)

    def apply(current_arm, raw, item_ids):
        assert current_arm == arm and item_ids == list(ITEM_IDS)
        transferred, receipt = env['transfer'](arm, raw, item_ids)
        assert tuple(row['name'] for row in receipt['items']) == ITEM_NAMES
        assert unpack_from('<I', raw, 0x2796B0)[0] == 3
        machine = inventory.machine(arm)
        machine.mem_write(inventory.BASE, transferred)
        call(machine, 0x7F244, ())
        assert machine.reg_read(UC_ARM_REG_R0) == 3
        call(machine, 0x23C60, (FLAG_OWNER, FLAG_INDEX))
        assert machine.reg_read(UC_ARM_REG_R0) == 0
        call(machine, 0x23C8C, (FLAG_OWNER, FLAG_INDEX, 1))
        call(machine, 0x23C60, (FLAG_OWNER, FLAG_INDEX))
        assert machine.reg_read(UC_ARM_REG_R0) == 1 << FLAG_INDEX
        after = bytes(machine.mem_read(inventory.BASE, len(raw)))
        offset = FLAG_OWNER + 4 - inventory.BASE
        assert after[:offset] == transferred[:offset] and after[offset + 1:] == transferred[offset + 1:]
        assert after[offset] == transferred[offset] | (1 << FLAG_INDEX)
        flag = dict(address=inventory.BASE + offset, before=transferred[offset], after=after[offset])
        receipt['changes'].append(flag)
        return after, receipt | dict(after_RAM_sha256=inventory.sha(after), synthetic_advice_unlock=True,
                                     original_flag_setter=0x02023C8C, advice_flag_change=flag, original_captain=3,
                                     original_route_state=3)

    return apply


def replay_items():
    prepared, reference = map(stage.load, (stage.PREP, REFERENCE))
    assert stage.digest(stage.ROM) == prepared['research_ROM_sha256']
    donor = reference['battery_save_preloaded']
    assert stage.digest(donor['source']) == donor['source_sha256'] == DONOR_SHA
    assert donor['copied_byte_exact_before_cold_boot'] and reference['cold_boot']
    assert not reference['savestate_loaded'] and not reference['callback_errors']
    release = stage.load(stage.RELEASE)
    assert stage.digest(release['candidate']) == release['candidate_sha256']
    before, arm = (stage.NdsImage.open(path).read_file(stage.ARM) for path in (release['candidate'], stage.ROM))
    assert inventory.sha(arm) == prepared['research_ARM9_sha256']
    for lo, hi in ((0x49DE8, 0x4A200), (0x4A448, 0x4A66C), (0xCB190, 0xCB19C)):
        assert before[lo:hi] == arm[lo:hi]
    transfer = inventory_fixture(before, arm, prepared['research_ARM9_sha256'])
    ITEMS.mkdir()
    inputs, commands = ITEMS / 'inputs.json', ITEMS / 'commands.json'
    prefix = [row for row in reference['scripted_input_schedule'] if row['start'] < 3400]
    assert [(row['start'], row['buttons']) for row in prefix] == [
        (1601, ['START']), (2001, ['A']), (2401, ['A']), (2801, ['A']),
    ]
    stage.save(inputs, prefix)
    stage.save(commands, list(COMMANDS))
    original_args, original_input, original_transfer = sys.argv, sys.stdin, inventory.transfer
    try:
        inventory.transfer = transfer
        sys.stdin = StringIO(''.join(json.dumps(row) + '\n' for row in COMMANDS))
        sys.argv = [sys.argv[0], '--rom', str(stage.ROM), '--out', str(ITEMS / 'capture'),
                    '--frames', '7201', '--inputs-json', str(inputs), '--battery-save', donor['source'],
                    '--touchscreen', '--capture-every', '999999', '--pause-at', '3400',
                    '--allow-inventory-fixtures', '--dump-ram', '--dump-pause-ram',
                    '--capture-at', '5200', '6100', '--dump-capture-ram']
        harness.main()
    finally:
        sys.argv, sys.stdin, inventory.transfer = original_args, original_input, original_transfer
    assert stage.digest(donor['source']) == DONOR_SHA
    report = ITEMS / 'capture/capture_report.json'
    stage.save(ITEMS / 'terminal.json', dict(report=str(report), report_sha256=stage.digest(report),
        candidate_sha256=prepared['research_ROM_sha256'], donor_sha256=DONOR_SHA,
        commands_sha256=stage.digest(commands), unchanged_original_save=True))


if __name__ == '__main__':
    assert sys.argv[1:] in (['items'], ['startup'])
    if sys.argv[1] == 'items':
        replay_items()
    else:
        FunctionType(previous.cold_boot.__code__, vars(previous) | globals())()
