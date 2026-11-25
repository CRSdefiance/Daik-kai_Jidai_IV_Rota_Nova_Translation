"""Exercise each revised credit through the original ending selector and movie playback."""

import io
import json
import sys
from argparse import ArgumentParser
from pathlib import Path

from scripts import headless_desmume_v193 as harness
from scripts import native_ending_fixture_v537 as fixture
from scripts import stage_ending_credit_spacing_20261123 as stage


base = stage.base
CASES = {
    "Rafael": ("ending_transitions_v642_rafael", 0, 10320, 11220, 11760),
    "Hodram": ("endings_current_v583_hodram", 1, 19632, 19932, 20280),
    "Lil": ("endings_current_v583_lil", 2, 25632, 25932, 26280),
    "Maria": ("endings_current_v583_maria", 3, 10612, 10912, 11280),
}


def run(captain):
    earlier, number, first, last, end = CASES[captain]
    history = Path("work/emulation_v193") / earlier / "capture_report.json"
    original = base.load(history)
    plan = base.load(stage.PROOF)
    assert plan["candidate_sha256"] == base.digest(stage.ROM)
    assert plan["exact_parent_inverse"]
    assert all(base.digest(path) == digest for path, digest in plan["evidence"].items())
    arm = base.NdsImage.open(stage.ROM).read_file(stage.parent.ARM)
    for row in plan["native_code_dependencies"]:
        lo, hi = row["offset"]
        assert fixture.sha(arm[lo:hi]) == row["sha256"]
    assert arm == base.NdsImage.open(stage.parent.ROM).read_file(stage.parent.ARM)
    assert original["cold_boot"] and not original["savestate_loaded"] and not original["callback_errors"]
    original_fixture, = original["synthetic_ending_fixtures"]
    pause = original_fixture["frame"]
    assert original_fixture["active_captain_id"] == number and pause < first
    assert original_fixture["changes"] == [{"address": 0x022796BC, "before": 1, "after": 4}]
    folder = stage.ROOT / captain.lower()
    folder.mkdir()
    schedule = folder / "inputs.json"
    base.save(schedule, original["scripted_input_schedule"])
    command = dict(ending_captain=number, until=end)
    stream = io.StringIO(json.dumps(command) + '\n{"stop": true}\n')
    original_shas, old_args, old_stdin = fixture.VERIFIED_ARM_SHAS, sys.argv, sys.stdin
    args = [harness.__file__, "--rom", str(stage.ROM), "--out", str(folder / "capture"),
        "--frames", str(end), "--inputs-json", str(schedule), "--press-start", "-1", "--touchscreen",
        "--capture-every", "999999", "--pause-at", str(pause), "--allow-ending-fixtures", "--dump-pause-ram",
        "--capture-at", *map(str, range(first, last + 1, 12))]
    donor = original.get("battery_save_preloaded")
    if donor:
        assert base.digest(donor["source"]) == donor["source_sha256"] and donor["copied_byte_exact_before_cold_boot"]
        args += ["--battery-save", donor["source"]]
    try:
        fixture.VERIFIED_ARM_SHAS = original_shas | {fixture.sha(arm)}
        sys.argv, sys.stdin = args, stream
        harness.main()
    finally:
        fixture.VERIFIED_ARM_SHAS, sys.argv, sys.stdin = original_shas, old_args, old_stdin
        stream.close()
    capture = folder / "capture/capture_report.json"
    report = base.load(capture)
    assert report["ROM_sha256"] == plan["candidate_sha256"] and report["frames"] == end
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not report["earned_completion_verified"] and not report["hardware_device_verification"]
    assert report["scripted_input_schedule"] == original["scripted_input_schedule"]
    new_fixture, = report["synthetic_ending_fixtures"]
    for key in ("frame", "active_captain_id", "changes", "movie", "native_dispatch_arguments"):
        assert new_fixture[key] == original_fixture[key]
    assert not any(value for key, value in report.items()
                   if key.startswith("synthetic_") and key != "synthetic_ending_fixtures")
    if donor:
        assert base.digest(donor["source"]) == report["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"]
    evidence = (capture, history, schedule, Path(__file__), folder / "capture/navigation_command_journal.json")
    base.save(folder / "terminal.json", dict(candidate_sha256=plan["candidate_sha256"], original_report=str(history),
        capture_report=str(capture), ending_state_fixture=new_fixture,
        evidence={str(path): base.digest(path) for path in evidence}))
    print(f"{captain} original ending playback captured through frame {end}.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("captain", choices=CASES)
    run(parser.parse_args().captain)
