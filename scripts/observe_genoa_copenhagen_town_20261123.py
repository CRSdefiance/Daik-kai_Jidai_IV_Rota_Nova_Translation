"""Follow ordinary controls in Genoa or Copenhagen on the Price Info ROM."""

import argparse
import sys
from inspect import getsource
from pathlib import Path

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_price_info_descriptions_20261123 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path(".codex-release-work/shared_display_20261123/genoa_copenhagen")
HISTORIES = {"genoa": "weapon_voyage_v476", "copenhagen": "shield_voyage_v467"}
FIRST_PAUSE = 3200


def main(city):
    root = ROOT / city
    commands = root / "controller.jsonl"
    history = Path("work/emulation_v193") / HISTORIES[city] / "capture_report.json"
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), COMMANDS)',
    })
    root.mkdir(parents=True, exist_ok=True)
    commands.touch(exist_ok=False)
    scope = vars(replay) | dict(ROOT=root, HISTORY=history, FIRST_PAUSE=FIRST_PAUSE, current=current,
                                COMMANDS=commands, __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-town-controller", "exec"), scope)
    stream = GrowingCommands(commands)
    original = sys.stdin
    try:
        sys.stdin = stream
        scope["main"]()
    finally:
        sys.stdin = original
        stream.close()


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("city", choices=HISTORIES)
    main(cli.parse_args().city)
