"""Visit Tunis's three Delicacy Shops from the registered Guild release."""

import sys
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts.reconcile_fleet_headquarters_20261124 import RELEASE
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import read


ROOT = Path(".codex-release-work/shared_display_20261123/tunis_delicacy_shops_20261124")
HISTORY = Path("work/emulation_v193/environment_voyage_v511_tunis_reload/capture_report.json")
CONTROLLER = ROOT / "controller.jsonl"
FIRST_PAUSE = 4200


def main():
    release = read(RELEASE)
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER)',
    })
    scope = vars(replay) | dict(ROOT=ROOT, HISTORY=HISTORY, FIRST_PAUSE=FIRST_PAUSE, CONTROLLER=CONTROLLER,
        current=SimpleNamespace(RELEASE=RELEASE, ROM=Path(release["candidate"])), __file__=__file__)
    exec(compile(source, __file__ + "::Tunis-Square", "exec"), scope)
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
