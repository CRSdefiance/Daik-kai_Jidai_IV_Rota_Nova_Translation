"""Replay the Nagasaki Market with ordinary controller and touch input."""

import sys
from inspect import getsource
from pathlib import Path

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_tavern_buy_a_round_20261124 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest, read


ROOT = Path(".codex-release-work/shared_display_20261123/nagasaki_market_20261124")
HISTORY = ROOT.parent / "ordinary/nagasaki/capture/capture_report.json"
REVIEW = Path("translations/editorial_checkpoints/shared_display_20261123/ordinary_gameplay.json")
FIRST_PAUSE = 3720
CONTROLLER = ROOT / "controller.jsonl"


def main():
    earlier = read(REVIEW)["visits"]["Nagasaki"]
    assert digest(HISTORY) == earlier["report_sha256"]
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER, REVIEW)',
    })
    ROOT.mkdir(parents=True)
    CONTROLLER.touch(exist_ok=False)
    scope = vars(replay) | dict(ROOT=ROOT, HISTORY=HISTORY, FIRST_PAUSE=FIRST_PAUSE,
        current=current, CONTROLLER=CONTROLLER, REVIEW=REVIEW, __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-Nagasaki-Market", "exec"), scope)
    stream = GrowingCommands(CONTROLLER)
    original = sys.stdin
    try:
        sys.stdin = stream
        scope["main"]()
    finally:
        sys.stdin = original
        stream.close()


if __name__ == "__main__":
    main()
