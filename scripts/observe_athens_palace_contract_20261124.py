"""Replay Athens's Palace substitution and continue to the contract in ordinary play."""

import json
import sys
from inspect import getsource
from pathlib import Path

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_ceuta_contract_refusal_20261124 as current
from scripts import verify_athens_trade_20261124 as prior
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest, read


ROOT = current.ROM.parent.with_name("editorial_20261124_athens_palace_contract")
CONTROLLER = ROOT / "controller.jsonl"
HISTORY = prior.play.ROOT / "capture/capture_report.json"
FIRST_PAUSE = prior.END
HOLDS = tuple(range(25590, 32390, 400))
OPENING = (dict(until=32790, duration=8, touch=[127, 25]), dict(until=33190, duration=8, buttons=["A"]))


def main():
    earlier = read(prior.OUT)
    saved = next(row for row in earlier["evidence"] if Path(row["path"]) == HISTORY)
    assert digest(HISTORY) == saved["sha256"]
    history = read(HISTORY)
    assert history["ROM_sha256"] == earlier["candidate_sha256"] and history["frames"] == FIRST_PAUSE
    assert history["battery_save_preloaded"]["source_sha256"] == earlier["donor"]["sha256"]
    ROOT.mkdir()
    with CONTROLLER.open("x", encoding="utf-8") as stream:
        stream.writelines(json.dumps(command) + "\n" for command in OPENING)
    source = checked_text(getsource(replay.main), {
        '"--pause-at", str(FIRST_PAUSE), "--dump-pause-ram"':
            '"--pause-at", str(FIRST_PAUSE), "--capture-at", *map(str, HOLDS)',
        'Path(__file__))': 'Path(__file__), CONTROLLER, prior.OUT)',
    })
    space = vars(replay) | globals()
    exec(compile(source, __file__ + "::ordinary-athens-contract", "exec"), space)
    previous, commands = sys.stdin, GrowingCommands(CONTROLLER)
    try:
        sys.stdin = commands
        space["main"]()
    finally:
        sys.stdin = previous
        commands.close()


if __name__ == "__main__":
    main()
