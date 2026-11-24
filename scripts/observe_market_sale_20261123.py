"""Follow the ordinary Trade sale and its confirmation on the current testing ROM."""

import sys
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_missionary_destination_20261123 as current
from scripts.reconcile_market_exit_current_20261123 import OUT as EXIT_REVIEW
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest, read


ROOT = Path(".codex-release-work/shared_display_20261123/market_sale")
CONTROLLER = ROOT / "controller.jsonl"
FIRST_PAUSE = 12681


def history_path():
    path, expected = next((p, h) for p, h in read(EXIT_REVIEW)["evidence"].items()
                          if Path(p).name == "capture_report.json" and Path(p).parents[1].name == "confirm")
    assert digest(path) == expected
    return Path(path)


def main():
    release = read(current.RELEASE)
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER)',
    })
    ROOT.mkdir(parents=True)
    CONTROLLER.touch(exist_ok=False)
    scope = vars(replay) | dict(ROOT=ROOT, HISTORY=history_path(), FIRST_PAUSE=FIRST_PAUSE, CONTROLLER=CONTROLLER,
        current=SimpleNamespace(RELEASE=current.RELEASE, ROM=Path(release["candidate"])), __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-market-sale", "exec"), scope)
    original = sys.stdin
    stream = GrowingCommands(CONTROLLER)
    try:
        sys.stdin = stream
        scope["main"]()
    finally:
        sys.stdin = original
        stream.close()


if __name__ == "__main__":
    main()
