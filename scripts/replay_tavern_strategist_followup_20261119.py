"""Replay the original Tavern scheme menus and a cumulative cold boot."""

from argparse import ArgumentParser
from io import StringIO
from json import dumps
from pathlib import Path
import sys
from types import FunctionType

from scripts import replay_ceuta_lesson_20261119 as inherited
from scripts import native_scheme_expert_fixture_v776_v2 as expert
from scripts import native_strategist_fixture_v776 as assignment
from scripts import run_scheme_expert_capture_v776_v2 as runner
from scripts import stage_tavern_strategist_followup_20261119 as build

base = build.base
HISTORICAL = Path("E:/Rota Nova translations/Generated/work/emulation_v193/schemes_v776_qualified_live/capture_report.json")
ROOT = build.ROOT / "london_schemes_v2"
CAPTURE = ROOT / "capture"
STARTUP = build.ROOT / "startup_fixture"
INPUTS = ROOT / "ordinary_inputs.json"
FRAMES = 31200
CAPTURES = (5200, 6000, 6400, 7200, 7600, 14400, 15200, 16400, 17200, 17600, 18000, 18400,
            19600, 20800, 22000, 23200, 23600, 24000, 24400, 25600, 27200, 28400, 28800, 29600,
            30000, 30400, 30800, 31200)


def scoped_expert(arm, raw, request):
    stage = base.load(build.PROOF)
    assert base.digest(build.ROM) == stage["candidate_sha256"]
    assert build.native.digest(arm) == stage["target_ARM9_sha256"]
    new_assign = FunctionType(assignment.assign.__code__, vars(assignment) | {"BASELINE": build.native.digest(arm)})
    return FunctionType(expert.assign_expert.__code__, vars(expert) | {"assign": new_assign})(arm, raw, request)


def capture():
    assert not ROOT.exists()
    stage = base.load(build.PROOF)
    prior = base.load(HISTORICAL)
    donor = prior["battery_save_preloaded"]
    assert stage["candidate_sha256"] == base.digest(build.ROM)
    assert base.digest(donor["source"]) == donor["source_sha256"] and donor["copied_byte_exact_before_cold_boot"]
    assert prior["frames"] == FRAMES
    ROOT.mkdir()
    inputs = prior["scripted_input_schedule"]
    base.save(INPUTS, inputs)
    native_harness = runner.HARNESS.read_text(encoding="utf-8")
    assert base.digest(runner.HARNESS) == prior["controlled_strategist_adapter"]["original_harness_sha256"]
    import_line = "from scripts.native_strategist_fixture_v624 import assign, assign_expert"
    assert native_harness.count(import_line) == 1
    harness = native_harness.replace(import_line, "assign, assign_expert = ACTIVE_EXPERT, ACTIVE_EXPERT")
    previous, previous_input = sys.argv, sys.stdin
    try:
        sys.argv = [str(runner.HARNESS), "--rom", str(build.ROM), "--out", str(CAPTURE),
                    "--battery-save", donor["source"], "--frames", str(FRAMES), "--inputs-json", str(INPUTS),
                    "--touchscreen", "--allow-strategist-fixtures", "--pause-at", "3200", "--dump-pause-ram",
                    "--capture-every", "999999", "--capture-at", *map(str, CAPTURES), "--dump-capture-ram"]
        sys.stdin = StringIO(dumps({"strategist_expert_fixture": True, "until": FRAMES, "buttons": []}) +
                             "\n" + dumps({"stop": True}) + "\n")
        exec(compile(harness, str(runner.HARNESS), "exec"),
            {"__name__": "__main__", "__file__": str(runner.HARNESS.resolve()), "ACTIVE_EXPERT": scoped_expert})
    finally:
        sys.argv = previous
        sys.stdin = previous_input
    capture_path = CAPTURE / "capture_report.json"
    current = base.load(capture_path)
    assert current["frames"] == FRAMES and current["ROM_sha256"] == stage["candidate_sha256"]
    assert current["scripted_input_schedule"] == inputs and current["cold_boot"] and not current["savestate_loaded"]
    assert not current["callback_errors"] and base.digest(donor["source"]) == donor["source_sha256"]
    base.save(ROOT / "terminal.json", dict(terminal=True, frames=FRAMES, report=str(capture_path),
        report_sha256=base.digest(capture_path), historical_inputs=str(HISTORICAL),
        historical_inputs_sha256=base.digest(HISTORICAL), controls_sha256=base.digest(INPUTS),
        candidate_sha256=stage["candidate_sha256"], native_harness_sha256=base.digest(runner.HARNESS),
        effective_harness_sha256=build.native.digest(harness.encode()), original_expert_sha256=base.digest(expert.__file__),
        natural_eligibility=False, hardware=False))
    print("London Schemes capture complete.")


def startup():
    FunctionType(inherited.startup.__code__, vars(inherited) | {"build": build, "STARTUP": STARTUP})()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("capture", "startup"))
    globals()[parser.parse_args().action]()
