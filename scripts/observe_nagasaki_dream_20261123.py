"""Follow the original Nagasaki voyage and Inn dream with ordinary controls."""

import sys
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_missionary_destination_20261123 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import read


ROOT = Path(".codex-release-work/shared_display_20261123/nagasaki_dream")
HISTORY = Path("work/emulation_v193/shiraki_surname_v518_dream/capture_report.json")
CONTROLLER = ROOT / "controller.jsonl"
FIRST_PAUSE = 6440


def main():
    release = read(current.RELEASE)
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER)',
    })
    ROOT.mkdir(parents=True)
    CONTROLLER.touch(exist_ok=False)
    scope = vars(replay) | dict(ROOT=ROOT, HISTORY=HISTORY, FIRST_PAUSE=FIRST_PAUSE, CONTROLLER=CONTROLLER,
        current=SimpleNamespace(RELEASE=current.RELEASE, ROM=Path(release["candidate"])), __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-nagasaki-dream", "exec"), scope)
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
