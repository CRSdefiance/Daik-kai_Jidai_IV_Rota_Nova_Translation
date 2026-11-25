"""Observe ordinary Palace and Market choices on the registered Tunis build."""

import sys
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import observe_tunis_delicacy_shops_20261124 as town
from scripts.observe_fleet_company_inputs_20261124 import RELEASE
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import read


ROOT = town.ROOT.with_name("tunis_market_and_palace_20261124")
CONTROLLER = ROOT / "controller.jsonl"


def main():
    release = read(RELEASE)
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER)',
    })
    scope = vars(replay) | dict(ROOT=ROOT, HISTORY=town.HISTORY, FIRST_PAUSE=town.FIRST_PAUSE, CONTROLLER=CONTROLLER,
        current=SimpleNamespace(RELEASE=RELEASE, ROM=Path(release["candidate"])), __file__=__file__)
    exec(compile(source, __file__ + "::Tunis-town-choices", "exec"), scope)
    original = sys.stdin
    commands = GrowingCommands(CONTROLLER)
    try:
        sys.stdin = commands
        scope["main"]()
    finally:
        sys.stdin = original
        commands.close()


if __name__ == "__main__":
    main()
