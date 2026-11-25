"""Reach low funds through ordinary investment, then visit the Lisbon Guild."""

from inspect import getsource
import json
import sys

from scripts import observe_lisbon_market_low_funds_20261124 as previous
from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_fleet_diversion_20261125 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import read


ROOT = current.ROM.parent.with_name("editorial_20261125_lisbon_guild_shortfall")
CONTROLLER = ROOT / "controller.jsonl"
HISTORY = previous.ROOT / "capture/capture_report.json"
FIRST_PAUSE = 14281
OPENING = dict(until=14521, duration=8, buttons=["B"])


def main():
    prefix, donor = previous.schedule()
    earlier = read(HISTORY)
    assert earlier["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"]
    assert earlier["scripted_input_schedule"][:len(prefix)] == prefix
    assert earlier["ROM_sha256"] == read(previous.current.RELEASE)["candidate_sha256"]
    ROOT.mkdir()
    CONTROLLER.write_text(json.dumps(OPENING) + "\n", encoding="utf-8")
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER)',
    })
    scope = vars(replay) | globals()
    exec(compile(source, __file__ + "::Lisbon-Guild-shortfall", "exec"), scope)
    original, commands = sys.stdin, GrowingCommands(CONTROLLER)
    try:
        sys.stdin = commands
        scope["main"]()
    finally:
        sys.stdin = original
        commands.close()


if __name__ == "__main__":
    main()
