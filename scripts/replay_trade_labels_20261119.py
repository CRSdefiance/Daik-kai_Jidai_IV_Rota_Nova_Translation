"""Replay the established Lisbon Local and Cargo selection with ordinary inputs."""

from argparse import ArgumentParser
from pathlib import Path
import sys

from scripts import headless_desmume_v193 as harness
from scripts import register_inn_numerals_20261119 as parent

base = parent.base
ROOT = Path("work/trade_labels_20261119")
PLAN = Path("work/market_goods_info_terminator_release_v1/market_run_v3/run_plan.json")
FRAMES = (9200,9600,10000,10400,10800,11200,11600)


def capture(case):
    if case=="baseline":
        rom = parent.ROM
        expected = base.load(parent.RELEASE)["candidate_sha256"]
    else:
        from scripts import stage_trade_labels_20261119 as stage
        rom,expected = stage.ROM,base.load(stage.PROOF)["candidate_sha256"]
    assert base.digest(rom)==expected
    folder = ROOT/case
    assert not folder.exists()
    plan = base.load(PLAN)
    inputs = Path(plan["unchanged_inputs"])
    donor = plan["source_save"]
    assert base.digest(inputs)==plan["unchanged_inputs_sha256"]
    assert base.digest(donor["source"])==donor["source_sha256"]
    argv = [harness.__file__,"--rom",str(rom),"--out",str(folder),"--frames","11600",
        "--inputs-json",str(inputs),"--press-start","-1","--capture-every","999999","--capture-at",*map(str,FRAMES),
        "--dump-capture-ram","--touchscreen","--battery-save",donor["source"]]
    prior = sys.argv
    try:
        sys.argv = argv
        harness.main()
    finally:
        sys.argv = prior
    assert base.digest(donor["source"])==donor["source_sha256"]


if __name__=="__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case",choices=("baseline","corrected"))
    capture(parser.parse_args().case)
