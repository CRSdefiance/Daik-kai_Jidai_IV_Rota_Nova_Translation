"""Visit the Tunis Tavern from the ordinary Tunis battery save."""

from inspect import getsource
import json
import sys

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import observe_tunis_delicacy_shops_20261124 as town
from scripts import register_fleet_diversion_20261125 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = current.ROM.parent.with_name("editorial_20261125_tunis_tavern")
CONTROLLER = ROOT / "controller.jsonl"
HISTORY = town.HISTORY
FIRST_PAUSE = town.FIRST_PAUSE
OPENING = dict(until=4600, duration=8, touch=[82, 28])


def main():
    ROOT.mkdir()
    CONTROLLER.write_text(json.dumps(OPENING) + "\n", encoding="utf-8")
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER)',
    })
    scope = vars(replay) | globals()
    exec(compile(source, __file__ + "::Tunis-Tavern", "exec"), scope)
    original, commands = sys.stdin, GrowingCommands(CONTROLLER)
    try:
        sys.stdin = commands
        scope["main"]()
    finally:
        sys.stdin = original
        commands.close()


if __name__ == "__main__":
    main()
