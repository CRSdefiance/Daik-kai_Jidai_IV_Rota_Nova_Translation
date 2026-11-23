"""Prepare the exact clean-input patch and run the established Stockholm startup."""
from argparse import ArgumentParser
from types import FunctionType, SimpleNamespace

from scripts import prepare_numbered_fleet_spacing_release_20261121 as common
from scripts import replay_stockholm_dialogue_followup_20261121 as replay
from scripts import stage_stockholm_dialogue_followup_20261121 as stage


STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
PLAN = stage.ROOT / "startup/identical_inputs.json"


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("check",choices=("startup","patch"))
    action = common.startup if parser.parse_args().check == "startup" else common.reconstruct
    runtime = SimpleNamespace(active=stage.parent,PROOF=stage.PROOF,ROOT=stage.ROOT,ROM=stage.ROM,
                              native=stage.native,play=replay.original.replay)
    FunctionType(action.__code__,action.__globals__ | {"stage":runtime,"STARTUP_CAPTURE":STARTUP_CAPTURE,"PLAN":PLAN})()
