"""Follow the ordinary post-lesson route to Lisbon's refit and Market menus."""

import sys
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_village_clue_punctuation_20261124 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path("E:/Rota Nova translations/Generated/work/editorial_20261124_lisbon_purser")
HISTORY = Path("work/rafael_deck_after_trade_20261119/corrected/capture/capture_report.json")
FIRST_PAUSE = 16801
CONTROLLER = Path(".codex-release-work/shared_display_20261123/lisbon_purser_20261124_controller.jsonl")


if __name__ == "__main__":
    release = replay.base.load(current.RELEASE)
    source = checked_text(getsource(replay.main), {
        '"--dump-pause-ram"]': '"--dump-ram"]',
        'Path(__file__))': 'Path(__file__), CONTROLLER)',
    })
    scope = vars(replay) | dict(ROOT=ROOT, HISTORY=HISTORY, FIRST_PAUSE=FIRST_PAUSE,
        current=SimpleNamespace(RELEASE=current.RELEASE, ROM=Path(release["candidate"])),
        CONTROLLER=CONTROLLER, __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-Lisbon-purser", "exec"), scope)
    CONTROLLER.parent.mkdir(parents=True, exist_ok=True)
    CONTROLLER.touch(exist_ok=True)
    startup = sys.stdin
    commands = GrowingCommands(CONTROLLER)
    try:
        sys.stdin = commands
        scope["main"]()
    finally:
        sys.stdin = startup
        commands.close()
