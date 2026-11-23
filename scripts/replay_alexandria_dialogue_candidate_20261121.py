"""Run the registered startup checks and repeat the successful voyage on the draft."""
from argparse import ArgumentParser
from types import FunctionType, SimpleNamespace
import sys

from scripts import replay_alexandria_square_20261121 as baseline
from scripts import replay_rafael_first_market_20261121 as template
from scripts import stage_alexandria_dialogue_20261121 as stage


base = stage.base
ROOT = stage.ROOT / "voyage"
REPORT = ROOT / "capture/capture_report.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
STARTUP_PLAN = stage.ROOT / "startup/identical_inputs.json"
BASELINE = baseline.ROOT / "capture/capture_report.json"
OBSERVED = baseline.ROOT / "scene_frames.json"


def town():
    before, stored, observed = map(base.load, (BASELINE, stage.PROOF, OBSERVED))
    assert base.digest(BASELINE) == observed["report_sha256"]
    assert base.digest(stage.ROM) == stored["candidate_sha256"]
    assert before["ROM_sha256"] == stored["predecessor_sha256"] == base.digest(stage.parent.ROM)
    assert before["cold_boot"] and not before["savestate_loaded"] and not before["callback_errors"]
    assert not any(value for key, value in before.items() if key.startswith("synthetic_"))
    donor = before["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"]) == donor["source_sha256"]
    ROOT.mkdir()
    inputs = ROOT / "identical_inputs.json"
    base.save(inputs, before["scripted_input_schedule"])
    frames = sorted(set(observed["panels"]) | set(observed["controls"].values()))
    harness = template.template.games.harness
    sys.argv = [harness.__file__, "--rom", str(stage.ROM), "--out", str(REPORT.parent), "--frames", str(before["frames"]),
                "--inputs-json", str(inputs), "--battery-save", donor["source"], "--press-start", "-1",
                "--touchscreen", "--dump-ram", "--capture-every", "999999", "--capture-at", *map(str, frames)]
    harness.main()
    assert base.digest(donor["source"]) == donor["source_sha256"]


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("town", "startup", "patch"))
    case = parser.parse_args().case
    if case == "town":
        town()
    else:
        common = template.template
        action = common.common.startup if case == "startup" else common.common.reconstruct
        runtime = SimpleNamespace(active=stage.parent, PROOF=stage.PROOF, ROOT=stage.ROOT, ROM=stage.ROM,
                                  native=stage.native, play=common.games)
        FunctionType(action.__code__, action.__globals__ |
                     {"stage": runtime, "STARTUP_CAPTURE": STARTUP_CAPTURE, "PLAN": STARTUP_PLAN})()
