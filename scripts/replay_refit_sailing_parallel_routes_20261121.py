"""Replay the revised Hodram sailing and Lil refit lessons in initialized excerpts."""
from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import replay_fernando_parallel_routes_20261121 as template
from scripts import stage_refit_sailing_parallel_routes_20261121 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
STARTUP_PLAN = stage.ROOT / "startup/identical_inputs.json"
CASES = {
    1: template.CASES[1] | dict(block=171, end=11000,
        sample=(5, 12, 18, 68, 71, 75, 78, 81, 88, 92, 95, 98, 101, 105, 109, 112, 115, 138)),
    2: template.CASES[2] | dict(block=166, end=12300,
        sample=(5, 27, 52, 68, 75, 98, 102, 106, 109, 112, 116, 130, 134, 140, 149, 153, 157, 161, 165, 169, 175)),
}


replay_source = checked_text(getsource(template.replay), {
    'g["route"] == route': 'g["route"] == route and g["block"] == case["block"]',
    'row["route"] == route': 'row["route"] == route and row["block"] == case["block"]',
    "Fernando_SC{route}_RESEARCH_ONLY.nds": "Refit_Sailing_SC{route}_RESEARCH_ONLY.nds",
})
scope = vars(template) | globals()
exec(compile(replay_source, __file__, "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("hodram", "lil", "startup", "patch"))
    case = parser.parse_args().case
    if case in ("hodram", "lil"):
        scope["replay"](1 if case == "hodram" else 2)
    else:
        prior = template.earlier.earlier.checks.template
        action = prior.common.startup if case == "startup" else prior.common.reconstruct
        runtime = SimpleNamespace(active=stage.parent, PROOF=stage.PROOF, ROOT=stage.ROOT, ROM=stage.ROM,
                                  native=native, play=prior.games)
        FunctionType(action.__code__, action.__globals__ |
                     {"stage": runtime, "STARTUP_CAPTURE": STARTUP_CAPTURE, "PLAN": STARTUP_PLAN})()
