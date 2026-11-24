"""Extend the registered Athens cold boot with ordinary Market visits."""

import json
from pathlib import Path
import sys

from scripts import observe_athens_active_trend_20261124 as earlier
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.stage_cartridge_title_20261123 import REGISTRY, digest, read, write
from scripts.verify_athens_active_trend_20261124 import END, OUT

ROOT = earlier.ROOT.with_name("editorial_20261124_athens_trade")
CONTROLLER = ROOT / "controller.jsonl"
PRIOR = earlier.ROOT / "capture/capture_report.json"
MARKET_ACTIONS = (
    dict(until=25990, duration=8, touch=[125, 76]),
    dict(until=26390, duration=8, buttons=['A']),
    dict(until=26790, duration=8, touch=[129, 96]),
    dict(until=27190, duration=8, buttons=['A']),
    dict(until=27590, duration=8, buttons=['A']),
    dict(until=27990, duration=8, buttons=['B']),
    dict(until=28390, duration=8, buttons=['A']),
    dict(until=28790, duration=8, buttons=['A']),
    dict(until=29190, duration=8, buttons=['A']),
    dict(until=29590, duration=8, buttons=['DOWN']),
    dict(until=29990, duration=8, buttons=['A']),
    dict(until=30390, duration=8, buttons=['A']),
    dict(until=30790, duration=8, buttons=['A']),
    dict(until=31190, duration=8, buttons=['A']),
    dict(until=31590, duration=8, buttons=['A']),
    dict(until=31990, duration=8, buttons=['A']),
    dict(until=32390, duration=8, buttons=['B']),
    dict(stop=True),
)


def main():
    release = read(earlier.current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"]
    assert digest(earlier.current.ROM) == release["candidate_sha256"]
    receipt = read(OUT)
    verified, = (ref for ref in receipt["evidence"] if Path(ref["path"]) == PRIOR)
    assert digest(PRIOR) == verified["sha256"]
    history = read(PRIOR)
    assert history["frames"] == END and history["cold_boot"]
    assert not history["savestate_loaded"] and not history["callback_errors"]
    assert not any(value for key, value in history.items() if key.startswith("synthetic_"))
    assert history["ROM_sha256"] == release["candidate_sha256"]
    donor = history["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"] == receipt["donor"]["sha256"]

    ROOT.mkdir()
    inputs = ROOT / "inputs.json"
    write(inputs, history["scripted_input_schedule"])
    CONTROLLER.write_text("".join(json.dumps(action) + "\n" for action in MARKET_ACTIONS), encoding="utf-8")
    old_args, old_stdin = sys.argv, sys.stdin
    stream = GrowingCommands(CONTROLLER)
    try:
        sys.argv = [__file__, "--rom", str(earlier.current.ROM), "--out", str(ROOT / "capture"),
            "--frames", "40000", "--inputs-json", str(inputs), "--battery-save", donor["source"],
            "--touchscreen", "--press-start", "-1", "--capture-every", "999999",
            "--pause-at", str(END), "--dump-pause-ram"]
        sys.stdin = stream
        earlier.harness.main()
    finally:
        sys.argv, sys.stdin = old_args, old_stdin
        stream.close()
    assert digest(donor["source"]) == donor["source_sha256"]


if __name__ == "__main__":
    main()
