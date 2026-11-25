"""Observe ordinary Riga town services on the registered recruitment candidate."""

import json
import sys
from inspect import getsource
from pathlib import Path

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import observe_riga_tavern_20261124 as prior
from scripts import register_riga_recruitment_20261124 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest, read

ROOT = current.ROM.parent.with_name("editorial_20261124_riga_town_services")
CONTROLLER = ROOT / "controller.jsonl"
FIRST_PAUSE = 3200
OPENING = (dict(until=3600, duration=8, touch=[25, 28]),)


def main():
    report = read(prior.PRIOR)["visits"]["riga"]["capture"]
    history = Path(report["path"])
    assert digest(history) == report["sha256"]
    ROOT.mkdir()
    with CONTROLLER.open("x", encoding="utf-8") as stream:
        stream.writelines(json.dumps(command) + "\n" for command in OPENING)
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER, prior.PRIOR)',
    })
    scope = vars(replay) | globals() | dict(HISTORY=history)
    exec(compile(source, __file__ + "::ordinary-riga-town", "exec"), scope)
    original, commands = sys.stdin, GrowingCommands(CONTROLLER)
    try:
        sys.stdin = commands
        scope["main"]()
    finally:
        sys.stdin = original
        commands.close()


if __name__ == "__main__":
    main()