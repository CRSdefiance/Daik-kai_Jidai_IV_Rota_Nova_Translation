"""Follow ordinary controls into Valencia's Governor's Office."""

import json
import sys
from inspect import getsource
from pathlib import Path

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_ceuta_contract_refusal_20261124 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest, read


ROOT = current.ROM.parent.with_name("editorial_20261124_valencia_government")
CONTROLLER = ROOT / "controller.jsonl"
PRIOR = Path("translations/editorial_checkpoints/shared_display_20261123/athens_valencia_town_20261123.json")
FIRST_PAUSE = 3200
OPENING = (dict(until=3500, duration=8, touch=[126, 26]), dict(until=3800, duration=8, buttons=["A"]))


def main():
    evidence = read(PRIOR)["towns"]["valencia"]["evidence"]
    history = Path(evidence["capture"]["path"])
    assert digest(history) == evidence["capture"]["sha256"]
    assert read(history)["battery_save_preloaded"]["source_sha256"] == evidence["donor"]["sha256"]
    ROOT.mkdir()
    with CONTROLLER.open("x", encoding="utf-8") as stream:
        stream.writelines(json.dumps(action) + "\n" for action in OPENING)
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER, PRIOR)',
    })
    scope = vars(replay) | globals() | dict(HISTORY=history)
    exec(compile(source, __file__ + "::ordinary-Valencia-Governor", "exec"), scope)
    original, commands = sys.stdin, GrowingCommands(CONTROLLER)
    try:
        sys.stdin = commands
        scope["main"]()
    finally:
        sys.stdin = original
        commands.close()


if __name__ == "__main__":
    main()
