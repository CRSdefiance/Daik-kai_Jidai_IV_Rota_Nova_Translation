"""Follow the existing regional assignment into Fleet Info on the current ROM."""

import sys
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_current_regional_orders_20261123 as regional
from scripts import observe_legacy_fleet_info_current_20261123 as trace
from scripts import observe_legacy_fleet_text_20261123 as legacy
from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts.observe_seoul_tavern_decline_20261123 import RELEASE
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import read


ROOT = Path("E:/Rota Nova translations/Generated/work/assigned_fleet_detail_20261123")


def main():
    release = read(RELEASE)
    history = read(regional.HISTORY)
    original_fixture, = history["synthetic_regional_financial_display_fixtures"]
    assert original_fixture["frame"] == 37800 > 10600
    ROOT.mkdir(parents=True, exist_ok=True)
    controller = ROOT / "controller.jsonl"
    controller.touch(exist_ok=True)
    assert not controller.stat().st_size and not (ROOT / "capture").exists()
    env = vars(legacy) | dict(ROOT=ROOT, TARGETS=trace.TARGETS, __file__=__file__)
    exec(compile(getsource(legacy.observer), __file__ + "::assigned_fleet_trace", "exec"), env)
    observer = SimpleNamespace(scoped_observer=env["observer"])
    current = SimpleNamespace(RELEASE=RELEASE, ROM=Path(release["candidate"]))
    source = checked_text(getsource(replay.main), {
        'assert not any(value for key, value in history.items() if key.startswith("synthetic_"))':
            'assert all(fixture["frame"] > FIRST_PAUSE for fixture in history["synthetic_regional_financial_display_fixtures"])',
        "common_requests=watch.requests,": "common_requests=watch.requests, fleet_trace=watch.rows,",
        "Path(__file__))": "Path(__file__), CONTROLLER)",
    })
    scope = vars(replay) | dict(ROOT=ROOT, HISTORY=regional.HISTORY, FIRST_PAUSE=10600, trace=observer,
                               CONTROLLER=controller, current=current, __file__=__file__)
    exec(compile(source, __file__ + "::assigned_fleet_controller", "exec"), scope)
    stream, old = GrowingCommands(controller), sys.stdin
    try:
        sys.stdin = stream
        scope["main"]()
    finally:
        sys.stdin = old
        stream.close()


if __name__ == "__main__":
    main()
