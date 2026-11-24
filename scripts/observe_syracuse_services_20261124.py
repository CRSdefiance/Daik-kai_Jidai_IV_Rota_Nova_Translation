"""Observe ordinary Syracuse services from the registered Palace candidate."""

import sys
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import observe_regional_town_dialogue_20261115 as town
from scripts.register_tunis_palace_refusal_20261124 import RELEASE
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path(".codex-release-work/shared_display_20261123/syracuse_services_20261124")
HISTORY = Path("work/emulation_v193") / town.HISTORY["syracuse"] / "capture_report.json"
CONTROLLER = ROOT / "controller.jsonl"
FIRST_PAUSE = 3720


def main():
    release = replay.base.load(RELEASE)
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER)',
    })
    scope = vars(replay) | dict(
        ROOT=ROOT, HISTORY=HISTORY, FIRST_PAUSE=FIRST_PAUSE, CONTROLLER=CONTROLLER,
        current=SimpleNamespace(RELEASE=RELEASE, ROM=Path(release["candidate"])), __file__=__file__,
    )
    exec(compile(source, __file__ + "::Syracuse-town-services", "exec"), scope)
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
