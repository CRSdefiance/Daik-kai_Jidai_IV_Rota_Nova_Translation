"""Select the sixth proof/map item on the second inventory row."""

import sys
from types import FunctionType

from scripts import replay_relic_map_item_cards_v1 as previous

stage, parent = previous.stage, previous.parent
STARTUP = previous.STARTUP
ITEMS = stage.ROOT / 'items_menu_v2'
FIXTURE_ITEMS, HOLDS = previous.FIXTURE_ITEMS, previous.HOLDS
BACK_MENU, TOWN = previous.BACK_MENU, previous.TOWN
COMMANDS = tuple(command | {'buttons': ['DOWN']} if command.get('until') == HOLDS[-1] else command
                 for command in previous.COMMANDS)
env = previous.env | globals()
items = FunctionType(previous.items.__code__, env)


if __name__ == '__main__':
    assert sys.argv[1:] == ['items']
    items()
