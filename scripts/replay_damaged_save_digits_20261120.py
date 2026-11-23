"""Replay the checksum warning and the established cumulative startup controls."""

from argparse import ArgumentParser
from pathlib import Path
from subprocess import run
import sys

from scripts import stage_damaged_save_digits_20261120 as stage


base = stage.base
HISTORY = Path("work/damaged_save_20261115_v2")


def corrupt_slot(case):
    stored = base.load(stage.PROOF)
    rom, digest = (stage.parent.ROM, stored["parent_sha256"]) if case == "parent" else (stage.ROM, stored["candidate_sha256"])
    assert base.digest(rom) == digest
    history = base.load(HISTORY / "corrupt_slot/capture/capture_report.json")
    fixture = base.load(HISTORY / "checksum_fixture.json")
    donor = Path(fixture["donor"])
    corrupted = Path(fixture["disposable_copy"])
    assert base.digest(donor) == fixture["donor_sha256"] and base.digest(corrupted) == fixture["copy_sha256"]
    first, second = donor.read_bytes(), corrupted.read_bytes()
    assert first[:4] == second[:4] and first[4] ^ second[4] == 1 and first[5:] == second[5:]
    replay(rom, history, str(corrupted), case)
    assert base.digest(donor) == fixture["donor_sha256"] and base.digest(corrupted) == fixture["copy_sha256"]


def replay(rom, history, save, case):
    folder = stage.ROOT / case
    folder.mkdir()
    plan = folder / "inputs.json"
    base.save(plan, history["scripted_input_schedule"])
    frames = history["exact_requested_capture_frames"]
    args = ["--dump-ram"] if case == "startup" else ["--touchscreen"]
    run([sys.executable, "-B", "-m", "scripts.headless_desmume_v193", "--rom", str(rom),
         "--out", str(folder / "capture"), "--frames", str(history["frames"]), "--inputs-json", str(plan),
         "--battery-save", save, "--press-start", "-1", "--capture-every", "999999",
         "--capture-at", *map(str, frames), *args], check=True)


def startup():
    history = base.load(stage.parent.STARTUP_CAPTURE)
    donor = history["battery_save_preloaded"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    assert base.digest(stage.ROM) == base.load(stage.PROOF)["candidate_sha256"]
    replay(stage.ROM, history, donor["source"], "startup")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("parent", "revised", "startup"))
    case = parser.parse_args().case
    startup() if case == "startup" else corrupt_slot(case)
