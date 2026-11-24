"""Follow the original no-share Market investment branch in Syracuse."""

import json
import sys
from inspect import getsource
from pathlib import Path

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_lisbon_roster_galley_20261124 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest, read
from scripts.verify_syracuse_local_purchase_20261124 import OUT as PREVIOUS


ROOT = current.build.ROOT.with_name("editorial_20261124_syracuse_investment")
CONTROLLER = ROOT / "controller.jsonl"
FIRST_PAUSE = 4900
OPENING = (dict(until=5300, duration=8, touch=[25, 28]),
           dict(until=5700, duration=8, buttons=["A"]),
           dict(until=6100, duration=8, buttons=["A"]))


def main():
    source = read(PREVIOUS)["evidence"]["capture"]
    history = Path(source["path"])
    assert digest(history) == source["sha256"]
    ROOT.mkdir()
    CONTROLLER.write_text("".join(json.dumps(command) + "\n" for command in OPENING), encoding="utf-8")
    code = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER, PREVIOUS)',
    })
    scope = vars(replay) | (globals() | dict(HISTORY=history, __file__=__file__))
    exec(compile(code, __file__ + "::ordinary-Syracuse-investment", "exec"), scope)
    stdin, commands = sys.stdin, GrowingCommands(CONTROLLER)
    try:
        sys.stdin = commands
        scope["main"]()
    finally:
        sys.stdin = stdin
        commands.close()


if __name__ == "__main__":
    main()
