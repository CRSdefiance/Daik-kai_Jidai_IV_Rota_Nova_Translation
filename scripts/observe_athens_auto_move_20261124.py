"""Follow ordinary Auto Move controls from the preserved Athens cartridge save."""

import sys
from inspect import getsource
from pathlib import Path

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_athens_item_rumor_20261124 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest, read


ROOT = Path(".codex-release-work/shared_display_20261123/athens_auto_move_20261124")
HISTORY = current.build.REPLAY
CONTROLLER = ROOT / "controller.jsonl"
FIRST_PAUSE = 3570


def main():
    run, release = read(HISTORY), read(current.RELEASE)
    assert run["ROM_sha256"] == release["candidate_sha256"]
    assert digest(run["battery_save_preloaded"]["source"]) == run["battery_save_preloaded"]["source_sha256"]
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER)',
    })
    ROOT.mkdir(parents=True)
    CONTROLLER.touch(exist_ok=False)
    scope = vars(replay) | dict(ROOT=ROOT, HISTORY=HISTORY, FIRST_PAUSE=FIRST_PAUSE, current=current,
        CONTROLLER=CONTROLLER, __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-athens-auto-move", "exec"), scope)
    previous = sys.stdin
    stream = GrowingCommands(CONTROLLER)
    try:
        sys.stdin = stream
        scope["main"]()
    finally:
        sys.stdin = previous
        stream.close()


if __name__ == "__main__":
    main()
