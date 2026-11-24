"""Observe ordinary Auto Move from Riga and continue from the Stockholm arrival."""

import sys
from inspect import getsource
from pathlib import Path

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_athens_item_rumor_20261124 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest, read


ROOT = Path(".codex-release-work/shared_display_20261123/riga_auto_dock_20261124")
HISTORY = Path("out/stockholm_december_gameplay_20261121/riga/capture/capture_report.json")
REVIEW = Path("translations/editorial_checkpoints/SharedText_20261110_v1/stockholm_december_gameplay_20261121_v1.json")
CONTROLLER = ROOT / "controller.jsonl"
FIRST_PAUSE = 8000
HOLDS = (3200, 4400, 4800, 5200, 5600, 6000, 6400, 6800, 7200, 7600)


def main():
    earlier = read(REVIEW)
    assert any(Path(p) == HISTORY and digest(HISTORY) == value for p, value in earlier["evidence"].items())
    assert earlier["ordinary_gameplay"] and any(row["frame"] == FIRST_PAUSE for row in earlier["calendar_and_voyage_holds"])
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ', "--dump-pause-ram", "--capture-at", *map(str, HOLDS)]',
        'Path(__file__))': 'Path(__file__), CONTROLLER, REVIEW)',
    })
    ROOT.mkdir(parents=True)
    CONTROLLER.touch(exist_ok=False)
    scope = vars(replay) | dict(ROOT=ROOT, HISTORY=HISTORY, FIRST_PAUSE=FIRST_PAUSE, HOLDS=HOLDS, current=current,
        CONTROLLER=CONTROLLER, REVIEW=REVIEW, __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-riga-stockholm-docking", "exec"), scope)
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
