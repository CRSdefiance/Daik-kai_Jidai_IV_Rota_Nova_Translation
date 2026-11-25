"""Replay No and Yes on the same pending Lisbon trade."""

from argparse import ArgumentParser
from subprocess import run
import sys

from scripts import observe_market_restart_common_20261114 as market
from scripts import stage_market_bargaining_20261120 as stage


base = stage.base
FRAMES = (9600, 10400, 11600, 11881, 12281, 12681, 13081, 13481)


def schedule(_):
    events, _, _, plan, donor = market.schedule("finish")
    events = [event for event in events if event["start"] <= 12001]
    events.extend(dict(start=at, duration=8, buttons=[key])
                  for at, key in ((12401, "X"), (12801, "A"), (13201, "A")))
    return events, FRAMES, 13500, plan, donor


def replay(case):
    stored = base.load(stage.STORED)
    rom, sha = (stage.parent.ROM, stored["previous_sha256"]) if case == "parent" else (stage.ROM, stored["candidate_sha256"])
    assert base.digest(rom) == sha
    events, frames, end, _, donor = schedule(case)
    output = stage.ROOT / f"ordinary_{case}"
    output.mkdir()
    plan = output / "inputs.json"
    base.save(plan, events)
    run([sys.executable, "-B", "-m", "scripts.headless_desmume_v193", "--rom", str(rom),
         "--out", str(output / "capture"), "--frames", str(end), "--inputs-json", str(plan),
         "--battery-save", donor["source"], "--touchscreen", "--press-start", "-1",
         "--capture-every", "999999", "--capture-at", *map(str, frames)], check=True)


def startup():
    report = base.load(stage.parent.STARTUP_CAPTURE)
    donor = report["battery_save_preloaded"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    assert base.digest(stage.ROM) == base.load(stage.STORED)["candidate_sha256"]
    plan = stage.ROOT / "startup_inputs.json"
    base.save(plan, report["scripted_input_schedule"])
    run([sys.executable, "-B", "-m", "scripts.headless_desmume_v193", "--rom", str(stage.ROM),
         "--out", str(stage.ROOT / "startup/capture"), "--frames", str(report["frames"]),
         "--inputs-json", str(plan), "--battery-save", donor["source"], "--press-start", "-1",
         "--capture-every", "999999", "--capture-at", *map(str, report["exact_requested_capture_frames"]),
         "--dump-ram"], check=True)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("parent", "revised", "startup"))
    case = parser.parse_args().case
    startup() if case == "startup" else replay(case)
