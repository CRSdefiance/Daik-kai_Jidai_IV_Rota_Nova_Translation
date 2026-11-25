"""Follow ordinary Riga Tavern controls on the registered Price Info candidate."""

import json
import sys
from inspect import getsource
from pathlib import Path

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_price_info_digits_20261124 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest, read


ROOT = current.build.ROOT.with_name("editorial_20261124_riga_tavern")
CONTROLLER = ROOT / "controller.jsonl"
PRIOR = Path("translations/editorial_checkpoints/shared_display_20261123/riga_seoul_ordinary_20261123.json")
FIRST_PAUSE = 3200
OPENING = (dict(until=3600, duration=8, touch=[75, 27]),
           dict(until=4000, duration=8, buttons=["A"]))


def main():
    evidence = read(PRIOR)["visits"]["riga"]["capture"]
    history = Path(evidence["path"])
    assert digest(history) == evidence["sha256"]
    ROOT.mkdir()
    CONTROLLER.write_text("".join(json.dumps(command) + "\n" for command in OPENING), encoding="utf-8")
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER, PRIOR)',
    })
    scope = vars(replay) | (globals() | dict(HISTORY=history, __file__=__file__))
    exec(compile(source, __file__ + "::ordinary-Riga-Tavern", "exec"), scope)
    original, commands = sys.stdin, GrowingCommands(CONTROLLER)
    try:
        sys.stdin = commands
        scope["main"]()
    finally:
        sys.stdin = original
        commands.close()


if __name__ == "__main__":
    main()
