"""Follow the verified custom name into a real save and Continue replay."""

import argparse
import sys
from pathlib import Path

from scripts import headless_desmume_v193 as harness
from scripts import observe_rafael_custom_name_20261119 as original
from scripts.run_activity_special_live_v988 import GrowingCommands

ROOT = original.ROOT / "save_roundtrip"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("save", "continue"))
    parser.add_argument("--battery", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT)
    args = parser.parse_args()
    folder = args.output / args.action
    journal = folder / "navigation.jsonl"
    capture = folder / "capture"
    assert journal.is_file() and not capture.exists()
    assert bool(args.battery) == (args.action == "continue")
    rom = original.current.ROM
    base = original.base
    assert base.digest(rom) == base.load(original.current.RELEASE)["candidate_sha256"]
    argv = [harness.__file__, "--rom", str(rom), "--out", str(capture), "--frames", "55000",
            "--press-start", "-1", "--touchscreen", "--capture-every", "999999", "--dump-pause-ram"]
    donor = None
    if args.battery:
        donor = base.digest(args.battery)
        argv.extend(["--battery-save", str(args.battery), "--pause-at", "900"])
    else:
        argv.extend(["--inputs-json", str(original.ROOT / "new_game_prefix.json"), "--pause-at", str(original.START)])
    old_args, old_stdin = sys.argv, sys.stdin
    stream = GrowingCommands(journal)
    try:
        sys.argv, sys.stdin = argv, stream
        harness.main()
    finally:
        sys.argv, sys.stdin = old_args, old_stdin
        stream.close()
    report = base.load(capture / "capture_report.json")
    assert report["ROM_sha256"] == base.digest(rom) and report["cold_boot"] and not report["savestate_loaded"]
    assert not report["callback_errors"] and not any(v for k, v in report.items() if k.startswith("synthetic_"))
    if donor:
        assert report["battery_save_preloaded"]["source_sha256"] == donor == base.digest(args.battery)
    else:
        assert not report.get("battery_save_preloaded")


if __name__ == "__main__":
    main()
