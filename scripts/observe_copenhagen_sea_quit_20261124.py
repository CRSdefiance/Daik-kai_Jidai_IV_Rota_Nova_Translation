"""Open the ordinary System Quit prompt from the verified Copenhagen sea approach."""

import json
import sys
from inspect import getsource
from pathlib import Path

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_lisbon_purser_refit_20261124 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import read, reference


ROOT = current.ROM.parent.with_name("editorial_20261124_copenhagen_sea_quit")
CONTROLLER = ROOT / "controller.jsonl"
PRIOR = Path("translations/editorial_checkpoints/shared_display_20261123/copenhagen_dock_producer_20261124.json")
FIRST_PAUSE = 3200
OPENING = dict(until=3600, duration=8, buttons=["X"])


def main():
    proof = read(PRIOR)
    assert proof["ordinary_gameplay"]
    history = Path(proof["replay"]["path"])
    assert reference(history) == proof["replay"]
    ROOT.mkdir()
    with CONTROLLER.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(OPENING) + "\n")
    source = checked_text(getsource(replay.main), {
        'Path(__file__))': 'Path(__file__), CONTROLLER, PRIOR)',
    })
    scope = vars(replay) | globals() | dict(HISTORY=history)
    exec(compile(source, __file__ + "::ordinary-Copenhagen-sea-quit", "exec"), scope)
    original, stream = sys.stdin, GrowingCommands(CONTROLLER)
    try:
        sys.stdin = stream
        scope["main"]()
    finally:
        sys.stdin = original
        stream.close()


if __name__ == "__main__":
    main()
