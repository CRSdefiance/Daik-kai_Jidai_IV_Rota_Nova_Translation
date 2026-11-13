"""Cold-boot the staged ROM and exercise the original Advice button in Items."""

import inspect
import sys
from types import FunctionType, SimpleNamespace

from scripts import native_inventory_fixture_v481 as inventory
from scripts import replay_utility_weapon_item_cards_v1 as items
from scripts import run_diplomatic_outcome_startup_v2 as startup
from scripts import stage_item_production_advice_v3 as candidate
from scripts.native_call_abi_v764 import call
from scripts.source_locked_derivation_v5118 import checked_text
from unicorn.arm_const import UC_ARM_REG_R0


base = candidate.previous.previous
stage = SimpleNamespace(**(vars(base) | vars(candidate) | {
    'PREP': candidate.PROOF,
    'RELEASE': base.review.RELEASE,
    'ARM': base.review.ARM,
}))
PRIOR = stage.ROOT.parent / 'promotional_item_cards_staged_20261111_v1' / 'own_startup'
STARTUP = stage.ROOT / 'own_startup'
ITEMS = stage.ROOT / 'items_advice'
ITEM = 4
FLAG_OWNER, FLAG_INDEX = 0x02276F90, 4
COMMANDS = (
    dict(until=8800, inventory_items=[ITEM], buttons=['X'], duration=8),
    dict(until=9200, touch=[143, 54], duration=8),
    dict(until=9600, buttons=['A'], duration=8),
    dict(until=9900, buttons=['X'], duration=8),
    dict(until=10200, buttons=['A'], duration=8),
    dict(until=10600, buttons=['B'], duration=8),
    dict(until=11000, buttons=['B'], duration=8),
    dict(stop=True),
)


def cold_boot():
    env = vars(startup) | dict(EVIDENCE=stage.PREP, ROM=stage.ROM, STARTUP=STARTUP, PRIOR=PRIOR)
    FunctionType(startup.main.__code__, env)()


def replay():
    prepared = stage.load(stage.PREP)
    registered = stage.load(stage.RELEASE)
    parent_arm = stage.NdsImage.open(registered['candidate']).read_file(stage.ARM)
    current_arm = stage.NdsImage.open(stage.ROM).read_file(stage.ARM)
    assert parent_arm[0x23C60:0x23CE4] == current_arm[0x23C60:0x23CE4]
    transfer_source = checked_text(inspect.getsource(inventory.transfer), {
        'category not in (2, 3, 4)': 'category != 0',
    })
    transfer_env = vars(inventory) | {'SUPPORTED_ARM_SHA': (prepared['research_ARM9_sha256'],)}
    exec(compile(transfer_source, __file__ + '::source_product_transfer', 'exec'), transfer_env)
    transfer = transfer_env['transfer']

    def enable_advice_and_supply_item(arm, raw, item_ids):
        assert arm == current_arm and item_ids == [ITEM]
        transferred, receipt = transfer(arm, raw, item_ids)
        assert receipt['items'][0]['name'] == 'Baby Shark'
        machine = inventory.machine(arm)
        machine.mem_write(inventory.BASE, transferred)
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
                                     original_flag_setter=0x02023C8C, advice_flag_change=flag)

    source = checked_text(inspect.getsource(items.items), {
        '''    use_original_transfer = FunctionType(fixture.transfer.__code__, vars(fixture) | {
        'SUPPORTED_ARM_SHA': (prepared['research_ARM9_sha256'],),
    })''': '    use_original_transfer = enable_advice_and_supply_item',
        "'--frames', '10401'": "'--frames', '11001'",
        "'--allow-inventory-fixtures', '--dump-ram'":
            "'--allow-inventory-fixtures', '--dump-ram', '--dump-pause-ram', "
            "'--capture-at', '9700', '9800', '9900', '--dump-capture-ram'",
    })
    env = vars(items) | globals() | {'enable_advice_and_supply_item': enable_advice_and_supply_item}
    exec(compile(source, __file__ + '::native-advice-replay', 'exec'), env)
    env['items']()


if __name__ == '__main__':
    assert sys.argv[1:] in (['items'], ['startup'])
    (replay if sys.argv[1] == 'items' else cold_boot)()
