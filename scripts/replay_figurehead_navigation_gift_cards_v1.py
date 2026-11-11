"""Replay Lisbon Items with the existing sextant and isolated figurehead and gift ownership."""

import inspect
from types import FunctionType, SimpleNamespace
import sys

from scripts import replay_utility_weapon_item_cards_v1 as previous
from scripts import stage_crew_equipment_item_cards_v1 as parent
from scripts import stage_figurehead_navigation_gift_cards_v1 as current
from scripts.source_locked_derivation_v5118 import checked_text

stage = SimpleNamespace(**(vars(current.previous) | vars(current)))
ITEMS, STARTUP = stage.ROOT / 'items_menu', stage.ROOT / 'own_startup'
FIXTURE_ITEMS = (114, 127)
HOLDS = (9600, 9900, 10200, 10500, 10800)
COMMANDS = (
    dict(until=8800, inventory_items=list(FIXTURE_ITEMS), buttons=['X'], duration=8),
    dict(until=9200, touch=[143, 54], duration=8),
    dict(until=HOLDS[0], buttons=['A'], duration=8),
    *(dict(until=frame, buttons=['RIGHT'], duration=8) for frame in HOLDS[1:]),
    dict(until=11200, buttons=['B'], duration=8),
    dict(until=11600, buttons=['B'], duration=8),
    dict(stop=True),
)
source = checked_text(inspect.getsource(previous.items), {
    """    use_original_transfer = FunctionType(fixture.transfer.__code__, vars(fixture) | {
        'SUPPORTED_ARM_SHA': (prepared['research_ARM9_sha256'],),
    })""": """    transfer_source = checked_text(inspect.getsource(fixture.transfer), {
        'category not in (2, 3, 4)': 'category not in (5, 7)',
    })
    transfer_env = vars(fixture) | {'SUPPORTED_ARM_SHA': (prepared['research_ARM9_sha256'],)}
    exec(compile(transfer_source, __file__ + '::selected-catalogue-kinds', 'exec'), transfer_env)
    use_original_transfer = transfer_env['transfer']""",
    "'--frames', '10401'": "'--frames', '11601'",
})
env = vars(previous) | globals()
exec(compile(source, __file__ + '::native-items-with-checked-ownership', 'exec'), env)
items = env['items']
cold_boot = FunctionType(previous.cold_boot.__code__, env)


if __name__ == '__main__':
    assert sys.argv[1:] in (['items'], ['startup'])
    (items if sys.argv[1] == 'items' else cold_boot)()
