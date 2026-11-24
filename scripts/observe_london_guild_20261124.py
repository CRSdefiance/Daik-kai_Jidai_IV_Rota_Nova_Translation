"""Visit the London Guild on the registered Yard build with ordinary inputs."""

import sys
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_london_tavern_20261123 as london
from scripts import register_yard_numerals_20261124 as active
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path(".codex-release-work/shared_display_20261123/london_guild_20261124")
CONTROLLER = ROOT / "controller.jsonl"


def main():
    source = checked_text(getsource(london.replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER)',
    })
    scope = vars(london.replay) | dict(ROOT=ROOT, HISTORY=london.HISTORY, FIRST_PAUSE=3200,
        current=SimpleNamespace(RELEASE=active.RELEASE, ROM=active.ROM), CONTROLLER=CONTROLLER, __file__=__file__)
    exec(compile(source, __file__ + "::London-Guild", "exec"), scope)
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
