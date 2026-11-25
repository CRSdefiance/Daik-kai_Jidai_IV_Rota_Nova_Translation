"""Follow the ordinary Yes branch of the Nagasaki recruitment question."""

import json
import sys
from inspect import getsource
from pathlib import Path

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_lisbon_purser_refit_20261124 as current
from scripts import stage_nagasaki_tavern_recruitment_20261124 as earlier
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import read, reference


ROOT = current.ROM.parent.with_name("editorial_20261124_nagasaki_second_recruitment")
CONTROLLER = ROOT / "controller.jsonl"
HISTORY = earlier.REPLAY
PAIR = (Path("releases/all_routes_editorial_20261124_nagasaki_tavern_recruitment_candidate")
        / "verification/paired_gameplay.json")
FIRST_PAUSE = earlier.HOLD
OPENING = dict(until=13320, duration=8, buttons=["A"])


def main():
    prior = read(PAIR)
    history = read(HISTORY)
    assert prior["after"] == reference(HISTORY)
    assert prior["candidate_sha256"] == history["ROM_sha256"]
    ROOT.mkdir()
    with CONTROLLER.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(OPENING) + "\n")
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER, PAIR)',
    })
    scope = vars(replay) | globals()
    exec(compile(source, __file__ + "::ordinary-Nagasaki-recruitment", "exec"), scope)
    stdin, controller = sys.stdin, GrowingCommands(CONTROLLER)
    try:
        sys.stdin = controller
        scope["main"]()
    finally:
        sys.stdin = stdin
        controller.close()


if __name__ == "__main__":
    main()
