"""Reach Rafael's alternate preparation choice through the ordinary New Game entry."""

import sys
from pathlib import Path

from scripts import headless_desmume_v193 as emulator
from scripts import register_kurushima_confrontation_wraps_20261123 as active
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.stage_cartridge_title_20261123 import REGISTRY, digest, read, write


ROOT = Path(".codex-release-work/shared_display_20261123/rafael_prepare_alone")
SOURCE = Path("out/rafael_preparation_gameplay_20261121/verified_preparation.json")
REPORT = ROOT / "capture/capture_report.json"
CONTROLLER = ROOT / "controller.jsonl"
FIRST_PAUSE = 32225
PREFIX_HOLDS = (31085, 31355, 31625, 31895, 32165)


def main():
    release = read(active.RELEASE)
    assert digest(active.ROM) == release["candidate_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    previous = read(SOURCE)
    report = Path(previous["report"])
    assert previous["ordinary_new_game"] and digest(report) == previous["report_sha256"]
    assert previous["preparation_menu"]["selected"] == "Ask him."
    old = read(report)
    assert old["cold_boot"] and not old["savestate_loaded"] and not old.get("battery_save_preloaded")
    prefix = [row for row in old["scripted_input_schedule"] if row["start"] <= FIRST_PAUSE]
    ROOT.mkdir(parents=True)
    inputs = ROOT / "inputs.json"
    write(inputs, prefix)
    CONTROLLER.touch(exist_ok=False)
    channel = GrowingCommands(CONTROLLER)
    saved = sys.argv, sys.stdin
    try:
        sys.stdin = channel
        sys.argv = [__file__, "--rom", str(active.ROM), "--out", str(REPORT.parent), "--frames", "48000",
            "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
            "--capture-at", *map(str, PREFIX_HOLDS), "--pause-at", str(FIRST_PAUSE)]
        emulator.main()
    finally:
        sys.argv, sys.stdin = saved
        channel.close()


if __name__ == "__main__":
    main()
