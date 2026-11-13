"""Replay the approved Lisbon Items path with the reviewed Charles Martel armor."""

import sys
from types import FunctionType, SimpleNamespace

from scripts import replay_utility_weapon_item_cards_v1 as previous
from scripts import stage_armor_item_cards_v1 as armor
from scripts import stage_utility_weapon_item_cards_v2 as parent


stage = SimpleNamespace(**(vars(armor.previous) | vars(armor)))
ITEM = 72
ITEMS, STARTUP = stage.ROOT / 'items_menu', stage.ROOT / 'own_startup'
COMMANDS = (previous.COMMANDS[0] | {'inventory_items': [ITEM]}, *previous.COMMANDS[1:])
env = vars(previous) | globals()
cold_boot = FunctionType(previous.cold_boot.__code__, env)
items = FunctionType(previous.items.__code__, env)


if __name__ == '__main__':
    assert sys.argv[1:] in (['items'], ['startup'])
    (items if sys.argv[1] == 'items' else cold_boot)()
