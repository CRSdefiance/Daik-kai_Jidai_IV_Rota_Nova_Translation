"""Run representative original scripted excerpts behind Rafael's New Game prelude."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_mediterranean_dialogue_20261121 as prior
from scripts import stage_rafael_north_sea_africa_20261121 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
STARTUP_PLAN = stage.ROOT / "startup/identical_inputs.json"
CASES = {55: (7997, 14500), 58: (7997, 11100)}

replay_source = checked_text(getsource(prior.replay), {
    'f"work/analysis/Rafael_B{number}_scene_fixtures_v{prior_version}"':
        'f"work/analysis/Rafael_B47_scene_fixtures_v{prior_version}"',
})
scope = vars(prior) | globals()
exec(compile(replay_source, __file__ + "::original-Rafael-prelude", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=(*map(str, CASES), "startup", "patch"))
    case = parser.parse_args().case
    if case.isdecimal():
        scope["replay"](int(case))
    else:
        template = prior.release_checks.template
        action = template.common.startup if case == "startup" else template.common.reconstruct
        runtime = SimpleNamespace(active=stage.parent, PROOF=stage.PROOF, ROOT=stage.ROOT, ROM=stage.ROM,
                                  native=native, play=template.games)
        FunctionType(action.__code__, action.__globals__ |
                     {"stage": runtime, "STARTUP_CAPTURE": STARTUP_CAPTURE, "PLAN": STARTUP_PLAN})()
