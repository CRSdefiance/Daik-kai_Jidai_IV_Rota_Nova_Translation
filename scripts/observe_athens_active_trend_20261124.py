"""Open the market report after an earned Athens trend in ordinary gameplay."""

import json
import sys

from scripts import headless_desmume_v193 as harness
from scripts import register_deck_skill_guidance_20261124 as current
from scripts.replay_current_european_trends_20261123 import ROOT as PREVIOUS
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.stage_cartridge_title_20261123 import REGISTRY, digest, read, write

ROOT = current.ROM.parent.with_name("editorial_20261124_athens_active_trend")
CONTROLLER = ROOT / "controller.jsonl"
PRIOR = PREVIOUS / "athens/capture/capture_report.json"
LEDGER = "translations/editorial_checkpoints/shared_display_20261123/european_trends_current_gameplay_20261123.json"
FIRST = 17590
OPENING = (
    dict(until=17990, duration=8, touch=[24, 27]),
    dict(until=18390, duration=8, buttons=["A"]),
    dict(until=18790, duration=8, buttons=["A"]),
)


def main():
    release = read(current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(current.ROM) == release["candidate_sha256"]
    previous = read(LEDGER)["city_runs"]["athens"]
    assert digest(PRIOR) == previous["capture"]["sha256"]
    history = read(PRIOR)
    assert history["frames"] == FIRST and history["cold_boot"] and not history["savestate_loaded"]
    assert not history["callback_errors"] and not any(v for k, v in history.items() if k.startswith("synthetic_"))
    donor = history["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"] == previous["donor"]["sha256"]
    ROOT.mkdir()
    inputs = ROOT / "inputs.json"
    write(inputs, history["scripted_input_schedule"])
    CONTROLLER.write_text("".join(json.dumps(action) + "\n" for action in OPENING), encoding="utf-8")
    args, original = sys.argv, sys.stdin
    commands = GrowingCommands(CONTROLLER)
    try:
        sys.argv = [__file__, "--rom", str(current.ROM), "--out", str(ROOT / "capture"),
            "--frames", "40000", "--inputs-json", str(inputs), "--battery-save", donor["source"], "--touchscreen",
            "--press-start", "-1", "--capture-every", "999999", "--pause-at", str(FIRST), "--dump-pause-ram"]
        sys.stdin = commands
        harness.main()
    finally:
        sys.argv, sys.stdin = args, original
        commands.close()
    assert digest(donor["source"]) == donor["source_sha256"]


if __name__ == "__main__":
    main()
