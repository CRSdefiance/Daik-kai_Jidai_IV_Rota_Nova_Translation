"""Exercise a promotional relic and map fragment in the original Lisbon Items screen."""

import sys
from types import FunctionType, SimpleNamespace

from scripts import replay_figurehead_navigation_gift_cards_v1 as previous
from scripts import stage_relic_map_item_cards_v1 as parent
from scripts import stage_promotional_item_cards_v1 as current
from scripts.source_locked_derivation_v5118 import checked_text

stage = SimpleNamespace(**(vars(current.previous) | vars(current)))
ITEMS, STARTUP = stage.ROOT / 'items_menu', stage.ROOT / 'own_startup'
FIXTURE_ITEMS = (194, 198)
HOLDS = previous.HOLDS
BACK_MENU, TOWN = 11200, 11600
COMMANDS = (previous.COMMANDS[0] | {'inventory_items': list(FIXTURE_ITEMS)}, *previous.COMMANDS[1:])
source = checked_text(previous.source, {"category not in (5, 7)": "category not in (4, 12)"})
env = previous.env | globals()
exec(compile(source, __file__ + '::promotional-relic-and-fragment-ownership', 'exec'), env)
items = env['items']
cold_boot = FunctionType(previous.cold_boot.__code__, env)


if __name__ == '__main__':
    assert sys.argv[1:] in (['items'], ['startup'])
    (items if sys.argv[1] == 'items' else cold_boot)()
