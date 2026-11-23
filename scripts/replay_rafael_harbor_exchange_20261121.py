"""Replay the revised harbor exchange and prepare the registered startup and patch."""
from argparse import ArgumentParser
from pathlib import Path
import sys
from types import FunctionType, SimpleNamespace

from scripts import checkpoint_rafael_harbor_shared_artwork_20261121 as harbor
from scripts import prepare_numbered_fleet_spacing_release_20261121 as common
from scripts import replay_stockholm_december_20261121 as games
from scripts import stage_rafael_harbor_exchange_20261121 as stage


base=stage.base
ROOT=stage.ROOT/"actual_harbor"
REPORT=ROOT/"capture/capture_report.json"
PLAN=ROOT/"identical_inputs.json"
STARTUP_CAPTURE=stage.ROOT/"startup/capture/capture_report.json"
STARTUP_PLAN=stage.ROOT/"startup/identical_inputs.json"


def replay():
    staged,earlier,proof=map(base.load,(stage.PROOF,harbor.REPORT,harbor.OUTPUT))
    assert not ROOT.exists() and base.digest(stage.ROM)==staged["candidate_sha256"]
    assert base.digest(harbor.REPORT)==proof["evidence"][str(harbor.REPORT)]
    assert staged["predecessor_sha256"]==earlier["ROM_sha256"]==proof["candidate_sha256"]
    ROOT.mkdir()
    base.save(PLAN,earlier["scripted_input_schedule"])
    frames=sorted(set(stage.review.CAPTURE.values())|{3000,6711,6920,7021,8020,9300})
    syms=games.harness
    sys.argv=[syms.__file__,"--rom",str(stage.ROM),"--out",str(REPORT.parent),
        "--frames",str(earlier["frames"]),"--inputs-json",str(PLAN),"--press-start","-1",
        "--capture-every","999999","--dump-ram","--capture-at",*map(str,frames)]
    syms.main()


if __name__=="__main__":
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("case",choices=("harbor","startup","patch"))
    selected=parser.parse_args().case
    if selected=="harbor":
        replay()
    else:
        action=common.startup if selected=="startup" else common.reconstruct
        runtime=SimpleNamespace(active=stage.parent,PROOF=stage.PROOF,ROOT=stage.ROOT,ROM=stage.ROM,
                                native=stage.native,play=games)
        FunctionType(action.__code__,action.__globals__|
                     {"stage":runtime,"STARTUP_CAPTURE":STARTUP_CAPTURE,"PLAN":STARTUP_PLAN})()
