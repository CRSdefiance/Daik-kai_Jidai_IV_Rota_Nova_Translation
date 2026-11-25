"""Stage a low-funds Lisbon Trade branch through ordinary Market inputs."""

import json
import sys
from pathlib import Path

from scripts import headless_desmume_v193 as harness
from scripts import register_claudio_opening_wrap_20261124 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.stage_cartridge_title_20261123 import REGISTRY, digest, read, write


ROOT = current.ROM.parent.with_name("editorial_20261124_lisbon_market_low_funds")
BOOK = Path("translations/editorial_checkpoints/shared_display_20261123/market_exit_current_20261123.json")
HISTORY = Path(".codex-release-work/shared_display_20261123/market_exit_current/back/capture/capture_report.json")
CONTROLLER = ROOT / "controller.jsonl"
FIRST = 11881
ACTIONS = (
    dict(until=12281, duration=8, touch=[126, 95]),
    dict(until=12681, duration=8, buttons=['A']),
    dict(until=13081, duration=8, buttons=['A']),
    dict(until=13481, duration=8, buttons=['R']),
    dict(until=13881, duration=8, buttons=['A']),
    dict(until=14281, duration=8, buttons=['A']),
    dict(until=14681, duration=8, buttons=['A']),
    dict(until=15081, duration=8, touch=[95, 104]),
    dict(until=15481, duration=8, buttons=['A']),
    dict(until=15881, duration=8, buttons=['X']),
    dict(until=16281, duration=8, buttons=['A']),
    dict(until=16681, duration=8, buttons=['B']),
    dict(until=17081, duration=8, buttons=['A']),
    dict(stop=True),
)


def schedule():
    prior = read(BOOK)
    assert digest(HISTORY) == prior["evidence"][str(HISTORY)]
    history = read(HISTORY)
    assert history["ROM_sha256"] == prior["candidate_sha256"]
    assert history["cold_boot"] and not history["savestate_loaded"] and not history["callback_errors"]
    assert not any(v for k, v in history.items() if k.startswith("synthetic_"))
    donor = history["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    return [r for r in history["scripted_input_schedule"] if r["start"] <= FIRST], donor


def main():
    release = read(current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(current.ROM) == release["candidate_sha256"]
    events, donor = schedule()
    ROOT.mkdir()
    plan = ROOT / "inputs.json"
    write(plan, events)
    CONTROLLER.write_text("".join(json.dumps(action) + "\n" for action in ACTIONS), encoding="utf-8")
    stream = GrowingCommands(CONTROLLER)
    old_args, old_in = sys.argv, sys.stdin
    try:
        sys.argv = [__file__, "--rom", str(current.ROM), "--out", str(ROOT / "capture"),
            "--frames", "35000", "--inputs-json", str(plan), "--battery-save", donor["source"],
            "--touchscreen", "--press-start", "-1", "--capture-every", "999999", "--pause-at", str(FIRST)]
        sys.stdin = stream
        harness.main()
    finally:
        sys.argv, sys.stdin = old_args, old_in
        stream.close()
    assert digest(donor["source"]) == donor["source_sha256"]


if __name__ == "__main__":
    main()
