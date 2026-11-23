"""Reconstruct the staged fleet ROM from clean and replay its startup."""
from argparse import ArgumentParser
from pathlib import Path
import sys

from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import stage_numbered_fleet_spacing_20261121 as stage


base = stage.base
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
PLAN = stage.ROOT / "startup/identical_inputs.json"


def startup():
    release = base.load(stage.active.RELEASE)
    proof = base.load(release["own_registered_startup"])
    source = Path(proof["exact_matching_frames"][0]["path"]).parent / "capture_report.json"
    before = base.load(source)
    assert before["ROM_sha256"] == release["candidate_sha256"]
    assert base.digest(stage.ROM) == base.load(stage.PROOF)["candidate_sha256"]
    donor = before["battery_save_preloaded"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    PLAN.parent.mkdir()
    base.save(PLAN,before["scripted_input_schedule"])
    harness = stage.play.harness
    sys.argv = [harness.__file__, "--rom", str(stage.ROM), "--out", str(STARTUP_CAPTURE.parent),
        "--frames", str(before["frames"]), "--inputs-json", str(PLAN), "--battery-save", donor["source"],
        "--press-start", "-1", "--touchscreen", "--dump-ram", "--capture-every", "999999",
        "--capture-at", *map(str,before["exact_requested_capture_frames"])]
    harness.main()


def reconstruct():
    patch, rebuilt = (stage.ROOT / name for name in ("translation.xdelta","clean_rebuilt.nds"))
    assert not patch.exists() and not rebuilt.exists()
    make_xdelta(stage.native.CLEAN,stage.ROM,patch)
    apply_xdelta(stage.native.CLEAN,patch,rebuilt)
    assert rebuilt.read_bytes() == stage.ROM.read_bytes()
    print("The clean-input patch reconstructs the staged numbered-fleet ROM exactly.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("check",choices=("startup","patch"))
    (startup if parser.parse_args().check == "startup" else reconstruct)()
