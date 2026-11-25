"""Continue the original Seoul Tavern choice with ordinary controller input."""

import json
import sys
from inspect import getsource

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_lisbon_purser_refit_20261124 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import read, reference
from scripts.verify_seoul_tavern_decline_20261123 import HISTORY
from scripts.verify_seoul_tavern_decline_20261123 import OUT as DECLINE


ROOT = current.ROM.parent.with_name("editorial_20261125_seoul_tavern_accept")
CONTROLLER = ROOT / "controller.jsonl"
FIRST_PAUSE = 15130
OPENING = dict(until=15350, duration=8, buttons=["A"])


def main():
    prior = read(DECLINE)
    previous = read(prior["terminal"]["path"])
    history = read(HISTORY)
    assert reference(HISTORY)["sha256"] == previous["evidence"][str(HISTORY)]
    assert reference(history["battery_save_preloaded"]["source"]) == prior["donor"]
    assert history["frames"] == FIRST_PAUSE
    ROOT.mkdir()
    with CONTROLLER.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(OPENING) + "\n")
    source = checked_text(getsource(replay.main), {
        'Path(__file__))': 'Path(__file__), CONTROLLER, DECLINE)',
    })
    scope = vars(replay) | globals()
    exec(compile(source, __file__ + "::ordinary-Seoul-Tavern", "exec"), scope)
    commands, original = GrowingCommands(CONTROLLER), sys.stdin
    try:
        sys.stdin = commands
        scope["main"]()
    finally:
        sys.stdin = original
        commands.close()


if __name__ == "__main__":
    main()
