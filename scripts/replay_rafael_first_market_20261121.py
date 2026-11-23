"""Replay the first Market lesson with identical ordinary New Game input."""
from argparse import ArgumentParser
from types import FunctionType, SimpleNamespace
import sys

from scripts import stage_rafael_first_market_20261121 as stage
from scripts import replay_rafael_harbor_exchange_20261121 as template


base = stage.base
ROOT = stage.ROOT / "actual_market"
REPORT = ROOT / "capture/capture_report.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
STARTUP_PLAN = stage.ROOT / "startup/identical_inputs.json"


def replay():
    assert not ROOT.exists()
    baseline, stored = map(base.load, (stage.review.replay.REPORT, stage.PROOF))
    assert baseline["ROM_sha256"] == stored["predecessor_sha256"] == base.digest(stage.parent.ROM)
    assert stored["candidate_sha256"] == base.digest(stage.ROM)
    assert not baseline["savestate_loaded"] and not baseline["callback_errors"]
    assert not any(value for key, value in baseline.items() if key.startswith("synthetic_"))
    plan = ROOT / "identical_inputs.json"
    ROOT.mkdir()
    base.save(plan, baseline["scripted_input_schedule"])
    frames = sorted(set(stage.review.FRAMES.values()) | {32225, 32765, 37085, 39435, 40735})
    harness = template.games.harness
    sys.argv = [harness.__file__, "--rom", str(stage.ROM), "--out", str(REPORT.parent),
                "--frames", str(baseline["frames"]), "--inputs-json", str(plan), "--press-start", "-1",
                "--capture-every", "999999", "--capture-at", *map(str, frames)]
    harness.main()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("market", "startup", "patch"))
    case = parser.parse_args().case
    if case == "market":
        replay()
    else:
        action = template.common.startup if case == "startup" else template.common.reconstruct
        runtime = SimpleNamespace(active=stage.parent, PROOF=stage.PROOF, ROOT=stage.ROOT, ROM=stage.ROM,
                                  native=stage.native, play=template.games)
        FunctionType(action.__code__, action.__globals__ |
                     {"stage": runtime, "STARTUP_CAPTURE": STARTUP_CAPTURE, "PLAN": STARTUP_PLAN})()
