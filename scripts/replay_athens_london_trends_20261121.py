"""Replay the same original Athens or London event with the revised text."""
from argparse import ArgumentParser
import sys

from scripts import stage_athens_london_trends_20261121 as stage
from scripts import verify_european_trends_gameplay_20261121 as original


base = stage.base
ROOT = stage.ROOT / "actual_towns"


def replay_paths(city):
    folder = ROOT / city
    return folder / "identical_inputs.json", folder / "capture/capture_report.json"


def source_run(city, stored):
    receipt = base.load(original.OUTPUT)
    assert receipt["candidate_sha256"] == stored["predecessor_sha256"]
    case, = [r for r in receipt["scene_runs"] if r["city"] == city]
    source = original.runs.ROOT / city / "capture/capture_report.json"
    assert base.digest(source) == case["evidence"][str(source)]
    return case, base.load(source)


def capture(city):
    plan, report = replay_paths(city)
    assert not plan.parent.exists()
    stored = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == stored["candidate_sha256"]
    case, prior = source_run(city, stored)
    donor = prior["battery_save_preloaded"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    plan.parent.mkdir(parents=True)
    base.save(plan, prior["scripted_input_schedule"])
    frames = sorted({r["frame"] for r in case["calendar_controls"].values()}
                    | {r["observed"]["frame"] for r in case["panels"]})
    harness = original.runs.previous.harness
    sys.argv = [harness.__file__, "--rom", str(stage.ROM), "--out", str(report.parent),
        "--frames", str(case["calendar_controls"]["returned"]["frame"]), "--inputs-json", str(plan),
        "--battery-save", donor["source"], "--press-start", "-1", "--touchscreen", "--dump-ram",
        "--capture-every", "999999", "--capture-at", *map(str, frames)]
    harness.main()
    assert base.digest(donor["source"]) == donor["source_sha256"]


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("city", choices=original.CASES)
    capture(parser.parse_args().city)
