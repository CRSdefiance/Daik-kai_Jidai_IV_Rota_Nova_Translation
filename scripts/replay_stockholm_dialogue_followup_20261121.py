"""Replay the same December and Tavern inputs on the Stockholm staging ROM."""
from pathlib import Path
import sys

from scripts import stage_stockholm_dialogue_followup_20261121 as stage
from scripts import verify_stockholm_december_20261121 as original


base = stage.base
ROOT = stage.ROOT / "actual_stockholm"
PLAN = ROOT / "identical_inputs.json"
REPORT = ROOT / "capture/capture_report.json"
CONTROL_FRAMES = (8640,8950,9260,9570,9880,10190,10500,46860,47160,47460)


def main():
    stored, observed, previous = map(base.load,(stage.PROOF,original.OUTPUT,original.REPORT))
    assert base.digest(stage.ROM) == stored["candidate_sha256"]
    assert base.digest(original.REPORT) == observed["evidence"][str(original.REPORT)]
    assert previous["ROM_sha256"] == observed["candidate_sha256"]
    assert original.RETURN == previous["frames"]
    donor = previous["battery_save_preloaded"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    ROOT.mkdir()
    base.save(PLAN,previous["scripted_input_schedule"])
    frames = sorted(set(CONTROL_FRAMES) | {p["observed"]["frame"] for p in observed["complete_fur_exchange"]})
    harness = original.replay.harness
    sys.argv = [harness.__file__, "--rom", str(stage.ROM), "--out", str(REPORT.parent),
        "--frames", str(previous["frames"]), "--inputs-json", str(PLAN), "--battery-save", donor["source"],
        "--press-start", "-1", "--touchscreen", "--dump-ram", "--capture-every", "999999", "--capture-at", *map(str,frames)]
    harness.main()
    assert base.digest(Path(donor["source"])) == donor["source_sha256"]


if __name__ == "__main__":
    main()
