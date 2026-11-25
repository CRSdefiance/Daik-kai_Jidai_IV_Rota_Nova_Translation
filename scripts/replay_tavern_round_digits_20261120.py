"""Replay both Tavern responses using the recorded ordinary Amsterdam inputs."""

from argparse import ArgumentParser
from pathlib import Path
from subprocess import run
import sys
from types import FunctionType

from scripts import replay_damaged_save_digits_20261120 as boot
from scripts import stage_tavern_round_digits_20261120 as stage


base = stage.base
FRAMES = (24550, 25290, 25630, 25960, 26160, 26500, 26900, 27230, 27560, 27890, 28220)


def scene(side):
    staged = base.load(stage.PROOF)
    release = base.load(stage.parent.RELEASE)
    before = stage.parent.stage.ROOT / "clean_rebuilt.nds"
    assert base.digest(before) == base.digest(stage.parent.ROM) == release["candidate_sha256"]
    rom, digest = (before, staged["parent_sha256"]) if side == "before" else (stage.ROM, staged["candidate_sha256"])
    assert base.digest(rom) == digest
    reference = stage.tavern.ROOT / "capture/capture_report.json"
    history = base.load(reference)
    evidence = base.load(stage.tavern.OUTPUT)
    assert evidence["evidence"][str(reference)] == base.digest(reference)
    events = [row for row in history["scripted_input_schedule"] if row["start"] < FRAMES[-1]]
    folder = stage.ROOT / side
    folder.mkdir()
    plan = folder / "inputs.json"
    base.save(plan, events)
    run([sys.executable, "-B", "-m", "scripts.headless_desmume_v193", "--rom", str(rom),
         "--out", str(folder / "capture"), "--frames", str(FRAMES[-1]), "--inputs-json", str(plan),
         "--press-start", "-1", "--touchscreen", "--capture-every", "999999", "--dump-capture-ram",
         "--capture-at", *map(str, FRAMES)], check=True)


def startup():
    history = base.load(stage.parent.STARTUP_CAPTURE)
    donor = history["battery_save_preloaded"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    assert base.digest(stage.ROM) == base.load(stage.PROOF)["candidate_sha256"]
    replay = FunctionType(boot.replay.__code__, boot.replay.__globals__ | {"stage": stage})
    replay(stage.ROM, history, donor["source"], "startup")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("before", "after", "startup"))
    case = parser.parse_args().case
    startup() if case == "startup" else scene(case)
