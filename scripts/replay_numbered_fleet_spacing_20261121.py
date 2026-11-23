"""Replay the ordinary map selection that exposed the missing fleet-name space."""
from pathlib import Path
import sys

from scripts import stage_numbered_fleet_spacing_20261121 as build


base = build.base
ROOT = build.ROOT / "actual_map"
REPORT = ROOT / "capture/capture_report.json"


def main():
    assert not ROOT.exists()
    proof = base.load(build.PROOF)
    assert base.digest(build.ROM) == proof["candidate_sha256"]
    original = build.play.ROOT / "capture/capture_report.json"
    assert base.digest(original) == proof["evidence"][str(original)]
    before = base.load(original)
    donor = before["battery_save_preloaded"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    ROOT.mkdir()
    inputs = ROOT / "identical_inputs.json"
    base.save(inputs, before["scripted_input_schedule"])
    harness = build.play.harness
    sys.argv = [harness.__file__, "--rom", str(build.ROM), "--out", str(REPORT.parent),
        "--frames", "5960", "--inputs-json", str(inputs), "--battery-save", donor["source"],
        "--press-start", "-1", "--touchscreen", "--dump-ram", "--capture-every", "999999",
        "--capture-at", "3760", "5140", "5680", "5960"]
    harness.main()
    assert base.digest(Path(donor["source"])) == donor["source_sha256"]


if __name__ == "__main__":
    main()
