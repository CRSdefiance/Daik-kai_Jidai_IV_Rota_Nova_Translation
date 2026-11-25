"""Show exact Lil dialogue excerpts after the original route initialization."""

from argparse import ArgumentParser
import sys
from types import FunctionType

from scripts import replay_late_trade_exchanges_20261118 as earlier
from scripts import stage_company_name_dialogue_20261121 as build
from scripts import verify_late_trade_exchanges_20261118 as contexts


base = build.base
ROOT = build.ROOT / "lil_excerpt"
ROM = ROOT / "Lil_Company_Excerpts_RESEARCH_ONLY.nds"
SETUP = ROOT / "fixture.json"
LIL_INPUTS = contexts.build.ROOT / "lil_snapshot_inputs.json"
SELECTION = ((54, (27, 31, 34)), (60, (11, 15, 20, 46)), (151, (100, 103, 107)))


def prepare():
    prepare_excerpts = FunctionType(earlier.prepare_excerpts.__code__, vars(earlier) | {"stage": build})
    setup = prepare_excerpts(2, 22, 56, SELECTION, ROM)
    inputs = base.load(LIL_INPUTS) + [dict(start=n, duration=5, buttons=["A"]) for n in range(3800, 7651, 275)]
    plan = ROOT / "inputs.json"
    base.save(plan, inputs)
    base.save(SETUP, setup | dict(inputs=str(plan), inputs_sha256=base.digest(plan)))


def capture():
    setup = base.load(SETUP)
    assert base.digest(ROM) == setup["fixture_sha256"] and root_identity()
    assert base.digest(setup["inputs"]) == setup["inputs_sha256"]
    sys.argv = [earlier.harness.__file__, "--rom", str(ROM), "--out", str(ROOT / "capture"),
                "--frames", "7851", "--inputs-json", setup["inputs"], "--capture-every", "99999",
                "--capture-at", *map(str, range(3650, 7851, 20))]
    earlier.harness.main()


def root_identity():
    return base.load(SETUP)["candidate_sha256"] == base.digest(build.ROM)


if __name__ == "__main__":
    options = ArgumentParser(description=__doc__)
    options.add_argument("action", choices=("prepare", "capture"))
    globals()[options.parse_args().action]()
