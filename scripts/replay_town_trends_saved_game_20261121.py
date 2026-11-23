"""Open a registered town save for ordinary town trend gameplay verification."""

import argparse
from pathlib import Path
import sys

from scripts import replay_amsterdam_bread_20261121 as common


base, active, harness = common.base, common.active, common.harness
ROOT = Path("out/town_trends_gameplay_20261121")
HISTORY = {
    "lisbon": Path("work/emulation_v193/lisbon_reload_v470/capture_report.json"),
    "seoul": Path("E:/Rota Nova translations/Generated/work/emulation_v193/barmaid_v780_seoul_baseline/capture_report.json"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("city", choices=HISTORY)
    args = parser.parse_args()
    folder = ROOT / args.city
    assert not folder.exists()
    release = base.load(active.RELEASE)
    assert base.digest(active.ROM) == release["candidate_sha256"]
    original = HISTORY[args.city]
    old = base.load(original)
    donor = old["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    boot = [row for row in old["scripted_input_schedule"] if row["start"] <= 2801]
    assert [row["buttons"] for row in boot] == [["START"], ["A"], ["A"], ["A"]]
    folder.mkdir(parents=True)
    inputs = folder / "inputs.json"
    base.save(inputs, boot)
    base.save(folder / "source_save.json", dict(source_capture=str(original), source_capture_sha256=base.digest(original),
        donor=donor["source"], sha256=donor["source_sha256"], working_ROM_sha256=release["candidate_sha256"]))
    commands = folder / "navigation.jsonl"
    commands.touch(exist_ok=False)
    stream = common.GrowingCommands(commands)
    original_args, original_stdin = sys.argv, sys.stdin
    try:
        sys.stdin = stream
        sys.argv = [harness.__file__, "--rom", str(active.ROM), "--out", str(folder / "capture"),
            "--frames", "28500", "--inputs-json", str(inputs), "--battery-save", donor["source"],
            "--press-start", "-1", "--touchscreen", "--capture-every", "999999", "--pause-at", "3760",
            "--dump-ram"]
        harness.main()
    finally:
        sys.argv, sys.stdin = original_args, original_stdin
        stream.close()
    assert base.digest(donor["source"]) == donor["source_sha256"]


if __name__ == "__main__":
    main()

