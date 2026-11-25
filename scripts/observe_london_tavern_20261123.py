"""Follow ordinary London Tavern controls on the registered Genoa candidate."""

import sys
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_genoa_alternate_dialogue_20261123 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import read


ROOT = Path(".codex-release-work/shared_display_20261123/london_tavern")
HISTORY = Path("work/emulation_v193/barmaid_intro_actual_v2216_V2171/capture_report.json")
CONTROLLER = ROOT / "controller.jsonl"
FIRST_PAUSE = 3200


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
    exec(compile(source, __file__ + "::ordinary-london-tavern", "exec"), scope)
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
