"""Sail from Copenhagen on ordinary controls and trace the village approach."""

import sys
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_tripoli_hodram_warning_20261124 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = replay.ROOT.with_name("copenhagen_narvik_20261124")
HISTORY = Path("work/emulation_v193/shield_voyage_v467/capture_report.json")
FIRST_PAUSE = 3200
CONTROLLER = ROOT / "controller.jsonl"


if __name__ == "__main__":
    release = replay.base.load(current.RELEASE)
    driver = checked_text(getsource(replay.main), {
        "Path(__file__))": "Path(__file__), CONTROLLER)",
    })
    context = vars(replay) | dict(ROOT=ROOT, HISTORY=HISTORY, FIRST_PAUSE=FIRST_PAUSE,
        CONTROLLER=CONTROLLER, current=SimpleNamespace(RELEASE=current.RELEASE, ROM=Path(release["candidate"])),
        __file__=__file__)
    exec(compile(driver, __file__ + "::ordinary-northern-voyage", "exec"), context)
    original, commands = sys.stdin, GrowingCommands(CONTROLLER)
    try:
        sys.stdin = commands
        context["main"]()
    finally:
        sys.stdin = original
        commands.close()
