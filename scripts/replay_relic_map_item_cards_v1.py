"""Cold-boot the staged ROM and display the four item kinds in the original Items menu."""

import sys
from types import FunctionType, SimpleNamespace

from scripts import replay_figurehead_navigation_gift_cards_v1 as previous
from scripts import stage_figurehead_navigation_gift_cards_v1 as parent
from scripts import stage_relic_map_item_cards_v1 as current
from scripts.source_locked_derivation_v5118 import checked_text

stage = SimpleNamespace(**(vars(current.previous) | vars(current)))
ITEMS, STARTUP = stage.ROOT / 'items_menu', stage.ROOT / 'own_startup'
FIXTURE_ITEMS = (151, 155, 162, 174)
HOLDS = tuple(range(9600, 11401, 300))
BACK_MENU, TOWN = 11800, 12200
COMMANDS = (
    dict(until=8800, inventory_items=list(FIXTURE_ITEMS), buttons=['X'], duration=8),
    dict(until=9200, touch=[143, 54], duration=8),
    dict(until=HOLDS[0], buttons=['A'], duration=8),
    *(dict(until=frame, buttons=['RIGHT'], duration=8) for frame in HOLDS[1:]),
    dict(until=BACK_MENU, buttons=['B'], duration=8),
    dict(until=TOWN, buttons=['B'], duration=8),
    dict(stop=True),
)
source = checked_text(previous.source, {
    "category not in (5, 7)": "category not in (6, 8, 9, 10)",
    "'--frames', '11601'": "'--frames', str(TOWN + 1)",
})
env = previous.env | globals()
exec(compile(source, __file__ + '::proof-and-map-inventory-display', 'exec'), env)
items = env['items']
cold_boot = FunctionType(previous.cold_boot.__code__, env)


if __name__ == '__main__':
    assert sys.argv[1:] in (['items'], ['startup'])
    (items if sys.argv[1] == 'items' else cold_boot)()
