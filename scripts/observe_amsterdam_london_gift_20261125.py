"""Follow the ordinary London save toward Amsterdam and Marie's gift."""

from inspect import getsource
from pathlib import Path
import sys

from scripts import observe_london_tavern_20261123 as london
from scripts import register_london_square_rumor_20261125 as current
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path(".codex-release-work/shared_display_20261123/amsterdam_london_gift_20261125")
CONTROLLER = ROOT / "controller.jsonl"


def main():
    ROOT.mkdir(parents=True)
    CONTROLLER.touch(exist_ok=False)
    source = checked_text(getsource(london.replay.main), {
        'Path(__file__))': 'Path(__file__), CONTROLLER)',
    })
    scope = vars(london.replay) | dict(ROOT=ROOT, HISTORY=london.HISTORY, FIRST_PAUSE=london.FIRST_PAUSE,
        CONTROLLER=CONTROLLER, current=current, __file__=__file__)
    exec(compile(source, __file__ + "::Amsterdam-gift-route", "exec"), scope)
    original = sys.stdin
    commands = london.GrowingCommands(CONTROLLER)
    try:
        sys.stdin = commands
        scope["main"]()
    finally:
        sys.stdin = original
        commands.close()


if __name__ == "__main__":
    main()
