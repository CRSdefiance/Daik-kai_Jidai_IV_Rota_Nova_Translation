"""Reach the Lisbon Guild after assigning Julio in ordinary play."""

from inspect import getsource
import json
import sys
from pathlib import Path

from scripts import observe_lisbon_purchase_variants_20261124 as prior
from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_fleet_diversion_20261125 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest, read


ROOT = current.ROM.parent.with_name("editorial_20261125_lisbon_guild_bargaining")
CONTROLLER = ROOT / "controller.jsonl"
FIRST_PAUSE = prior.PAUSE
OPENING = (dict(until=37540, duration=8, buttons=["B"]),
           dict(until=37780, duration=8, touch=[20, 145]),
           dict(until=38020, duration=8, buttons=["A"]))


def main():
    evidence = read(prior.BOOK)["evidence"]["capture"]
    history = Path(evidence["path"])
    assert digest(history) == evidence["sha256"] and read(history)["frames"] == FIRST_PAUSE
    ROOT.mkdir()
    CONTROLLER.write_text("".join(json.dumps(row) + "\n" for row in OPENING), encoding="utf-8")
    source = checked_text(getsource(replay.main), {
        'Path(__file__))': 'Path(__file__), CONTROLLER, prior.BOOK)',
    })
    scope = vars(replay) | globals() | {"HISTORY": history}
    exec(compile(source, __file__ + "::Lisbon-Guild-bargaining", "exec"), scope)
    original, commands = sys.stdin, GrowingCommands(CONTROLLER)
    try:
        sys.stdin = commands
        scope["main"]()
    finally:
        sys.stdin = original
        commands.close()


if __name__ == "__main__":
    main()
