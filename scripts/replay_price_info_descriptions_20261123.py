"""Replay Beef in ordinary Price Info and prepare patch and startup checks."""

import sys
from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType

from scripts import check_supply_ratio_release_inputs_20261123 as checks
from scripts import headless_desmume_v193 as harness
from scripts import replay_price_info_wraps_20261115 as earlier
from scripts import stage_price_info_descriptions_20261123 as stage
from scripts.stage_cartridge_title_20261123 import digest, read, reference, write


ROOT = stage.ROOT
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
FRAMES = (12600, 13000, 13400, 13800, 14600, 15000, 15400, 15800, 16200, 16600, 17000)


def inputs():
    controls = [row for row in read(earlier.OLD_INPUTS) if row["start"] <= 14201]
    controls.extend(dict(start=at, duration=8, buttons=[key]) for at, key in (
        (14601, "UP"), (15001, "RIGHT"), (15401, "RIGHT"), (15801, "A"), (16201, "A"), (16601, "B")))
    donor = read(earlier.DONOR_PLAN)["source_save"]
    assert digest(donor["source"]) == donor["source_sha256"]
    return controls, donor


def play(action, staged):
    previous = read(stage.parent.RELEASE)
    path, sha = (stage.ROM, staged["candidate_sha256"]) if action == "revised" else (
        Path(previous["candidate"]), previous["candidate_sha256"])
    assert digest(path) == sha
    controls, donor = inputs()
    folder = ROOT / action
    folder.mkdir()
    schedule = folder / "inputs.json"
    write(schedule, controls)
    argv = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(path), "--out", str(folder / "capture"),
                    "--frames", str(FRAMES[-1]), "--inputs-json", str(schedule), "--press-start", "-1",
                    "--touchscreen", "--battery-save", donor["source"], "--capture-every", "999999",
                    "--dump-capture-ram", "--capture-at", *map(str, FRAMES)]
        harness.main()
    finally:
        sys.argv = argv
    assert digest(donor["source"]) == donor["source_sha256"]


def main(action):
    staged = read(stage.STORED)
    if action in ("current", "revised"):
        play(action, staged)
        return
    previous = read(stage.parent.RELEASE)
    proof = staged | dict(candidate=str(stage.ROM), clean_input_sha256=previous["clean_input_sha256"],
                          predecessor_sha256=previous["candidate_sha256"])
    scope = vars(checks) | dict(RELEASE=stage.parent.RELEASE, PATCH=PATCH, REBUILT=REBUILT,
                                STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(getattr(checks, action).__code__, scope)(proof)
    if action == "patch":
        write(PATCH_PROOF, dict(clean_input_sha256=proof["clean_input_sha256"], candidate=reference(stage.ROM),
                               patch=reference(PATCH), rebuilt=reference(REBUILT), byte_exact=True))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("current", "revised", "patch", "startup"))
    main(cli.parse_args().action)
