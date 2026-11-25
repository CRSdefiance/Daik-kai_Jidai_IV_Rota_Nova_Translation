"""Replay both stock slot lists on the exact predecessor and staged ROM."""

from argparse import ArgumentParser
from pathlib import Path
import subprocess
import sys
from types import FunctionType

from scripts import replay_save_dialogue_followup_20261119 as prior
from scripts import stage_save_location_labels_20261119 as stage

base = stage.base
STARTUP = stage.ROOT / "startup_fixture"
FRAMES = (5400,5800,6200,6600,7000,7400)
REFERENCE = prior.REFERENCE


def patch():
    FunctionType(prior.prior.patch.__code__, vars(prior.prior) | {"stage":stage})()


def startup():
    FunctionType(prior.startup_workflow.startup.__code__, vars(prior.startup_workflow) | {
        "stage":stage, "STARTUP":STARTUP})()


def gameplay(side):
    assert side in ("before","after")
    reference = base.load(REFERENCE)
    original = reference["battery_save_preloaded"]
    donor = Path(original["source"])
    assert base.digest(donor) == original["source_sha256"]
    events = [row for row in reference["scripted_input_schedule"] if row["start"] < FRAMES[-1]]
    assert reference["cold_boot"] and not reference["savestate_loaded"] and not reference["callback_errors"]
    assert not any(value for key,value in reference.items() if key.startswith("synthetic_"))
    assert events[-1] == dict(start=7001,duration=8,buttons=["A"])
    folder = stage.ROOT / side
    folder.mkdir()
    inputs = folder / "inputs.json"
    base.save(inputs,events)
    rom = stage.parent.ROM if side == "before" else stage.ROM
    args = [sys.executable,"-m","scripts.headless_desmume_v193","--rom",str(rom),"--out",str(folder/"capture"),
        "--frames",str(FRAMES[-1]),"--inputs-json",str(inputs),"--battery-save",str(donor),
        "--touchscreen","--capture-every","999999","--capture-at",*map(str,FRAMES),"--dump-ram"]
    subprocess.run(args,check=True)
    path = folder/"capture/capture_report.json"
    report = base.load(path)
    assert report["ROM_sha256"] == base.digest(rom) and report["frames"] == FRAMES[-1]
    assert report["scripted_input_schedule"] == events and not report["callback_errors"]
    assert base.digest(donor) == original["source_sha256"] and report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    assert not any(value for key,value in report.items() if key.startswith("synthetic_"))
    base.save(folder/"terminal.json",dict(report=str(path),report_sha256=base.digest(path),
        donor_sha256=base.digest(donor),input_sha256=base.digest(inputs),reference_sha256=base.digest(REFERENCE),
        ROM_sha256=report["ROM_sha256"]))


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("before","after","patch","startup"))
    name = parser.parse_args().action
    if name in ("before","after"):
        gameplay(name)
    else:
        globals()[name]()

