"""Observe ordinary facility visits from the preserved Athens and Valencia saves."""

import argparse
import sys
from inspect import getsource
from pathlib import Path

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_rafael_prepare_alone_20261123 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest


ROOT = Path(".codex-release-work/shared_display_20261123/athens_valencia_town")
HISTORIES = {"athens": "environment_voyage_v510_leg", "valencia": "valencia_reload_v471"}
SAVES = {"athens": "hodram-athens-rested-v508.dsv", "valencia": "hodram-valencia-resupplied-blue-oak-v468.dsv"}


def main(city):
    area = ROOT / city
    commands = area / "controller.jsonl"
    history = Path("work/emulation_v193") / HISTORIES[city] / "capture_report.json"
    save = Path("E:/Rota Nova translations/Saves") / SAVES[city]
    donor = dict(source=str(save), source_sha256=digest(save))
    source = checked_text(getsource(replay.main), {
        'donor = history["battery_save_preloaded"]': 'donor = DONOR',
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), COMMANDS)',
    })
    area.mkdir(parents=True)
    commands.touch(exist_ok=False)
    scope = vars(replay) | dict(ROOT=area, HISTORY=history, FIRST_PAUSE=3200, DONOR=donor,
        current=current, COMMANDS=commands, __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-facility-visit", "exec"), scope)
    original = sys.stdin
    stream = GrowingCommands(commands)
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
