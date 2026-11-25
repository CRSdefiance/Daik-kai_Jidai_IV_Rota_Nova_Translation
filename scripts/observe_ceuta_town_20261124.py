"""Record ordinary town conversations from the preserved Ceuta battery save."""

import json
import sys
from inspect import getsource
from pathlib import Path

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_claudio_opening_wrap_20261124 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest, read


ROOT = current.ROM.parent.with_name("editorial_20261124_ceuta_town")
CONTROLLER = ROOT / "controller.jsonl"
PRIOR = Path("translations/editorial_checkpoints/shared_display_20261123/ceuta_storm_and_hunger_20261124.json")
FIRST_PAUSE = 3400
ACTIONS = (dict(until=3700, duration=8, touch=[25, 27]),)


def main():
    earlier = read(PRIOR)["evidence"]
    capture = earlier["capture"]
    history = Path(capture["path"])
    assert digest(history) == capture["sha256"]
    donor = read(history)["battery_save_preloaded"]
    assert donor["source_sha256"] == earlier["donor"]["sha256"]
    ROOT.mkdir()
    with CONTROLLER.open("x", encoding="utf-8") as stream:
        stream.writelines(json.dumps(command) + "\n" for command in ACTIONS)
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER, PRIOR)',
    })
    scope = vars(replay) | globals() | dict(HISTORY=history)
    exec(compile(source, __file__ + "::ordinary-Ceuta-town", "exec"), scope)
    original, commands = sys.stdin, GrowingCommands(CONTROLLER)
    try:
        sys.stdin = commands
        scope["main"]()
    finally:
        sys.stdin = original
        commands.close()


if __name__ == "__main__":
    main()
