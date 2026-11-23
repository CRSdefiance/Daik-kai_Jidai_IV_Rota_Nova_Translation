"""Replay the same original Lisbon event with the staged two-line revisions."""
from pathlib import Path
import sys

from scripts import stage_lisbon_fragrance_wraps_20261121 as stage
from scripts import verify_lisbon_seoul_trend_gameplay_20261121 as original

base = stage.base
ROOT = stage.ROOT / "actual_lisbon"
PLAN = ROOT / "identical_inputs.json"
REPORT = ROOT / "capture/capture_report.json"


def capture():
    assert not ROOT.exists()
    stored = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == stored["candidate_sha256"]
    receipt = base.load(original.OUTPUT)
    case, = [r for r in receipt["town_runs"] if r["city"] == "lisbon"]
    assert receipt["candidate_sha256"] == stored["predecessor_sha256"]
    source = original.runs.ROOT / "lisbon/capture/capture_report.json"
    assert base.digest(source) == case["evidence"][str(source)]
    prior = base.load(source)
    donor = prior["battery_save_preloaded"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    ROOT.mkdir()
    base.save(PLAN, prior["scripted_input_schedule"])
    frames = [case["opened_existing_save"]["frame"], case["after_rest"]["frame"],
              *[row["observed"]["frame"] for row in case["records"]]]
    harness = original.runs.harness
    sys.argv = [harness.__file__, "--rom", str(stage.ROM), "--out", str(REPORT.parent),
        "--frames", str(case["Square_after_notice"]["frame"]), "--inputs-json", str(PLAN),
        "--battery-save", donor["source"], "--press-start", "-1", "--touchscreen", "--dump-ram",
        "--capture-every", "999999", "--capture-at", *map(str, frames)]
    harness.main()
    assert base.digest(donor["source"]) == donor["source_sha256"]


if __name__ == "__main__":
    capture()

