"""Continue the ordinary Azores visit into the village's Deal screen."""

import json
import sys
from inspect import getsource

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_seoul_reika_20261125 as current
from scripts.observe_azores_return_20261123 import VISIT as HISTORY, VISIT_SHA
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest


ROOT = current.ROM.parent.with_name("editorial_20261125_azores_trade_checked")
CONTROLLER = ROOT / "controller.jsonl"
FIRST_PAUSE = 15050
OPENING = (dict(until=15320, duration=8, buttons=["A"]),
           dict(until=15590, duration=8, buttons=["X"]),
           dict(until=15860, duration=8, buttons=["B"]))


def main():
    assert digest(HISTORY) == VISIT_SHA
    ROOT.mkdir()
    with CONTROLLER.open("x", encoding="utf-8") as stream:
        stream.writelines(json.dumps(action) + "\n" for action in OPENING)
    source = checked_text(getsource(replay.main), {
        'Path(__file__))': 'Path(__file__), CONTROLLER)',
    })
    scope = vars(replay) | globals()
    exec(compile(source, __file__ + "::ordinary-Azores-market", "exec"), scope)
    commands, original = GrowingCommands(CONTROLLER), sys.stdin
    try:
        sys.stdin = commands
        scope["main"]()
    finally:
        sys.stdin = original
        commands.close()


if __name__ == "__main__":
    main()
