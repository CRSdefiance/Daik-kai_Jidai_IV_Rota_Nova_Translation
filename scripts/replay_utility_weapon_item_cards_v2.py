"""Replay the final utility and weapon card ROM in the verified startup and Items paths."""

import sys
from types import FunctionType, SimpleNamespace

from scripts import replay_utility_weapon_item_cards_v1 as earlier
from scripts import stage_utility_weapon_item_cards_v2 as final


stage = SimpleNamespace(**(vars(final.initial) | vars(final)))
ITEMS, STARTUP = stage.ROOT / 'items_menu', stage.ROOT / 'own_startup'
env = vars(earlier) | globals()
cold_boot = FunctionType(earlier.cold_boot.__code__, env)
items = FunctionType(earlier.items.__code__, env)


if __name__ == '__main__':
    assert sys.argv[1:] in (['items'], ['startup'])
    (items if sys.argv[1] == 'items' else cold_boot)()
