"""Observe Maria's compass and instinct options in the initialized navigation scene."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import replay_ruins_clues_and_guides_20261118 as previous
from scripts import stage_temple_supply_shipyard_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
ROOT = stage.ROOT / "maria_navigation_replay"
ROM = ROOT / "Maria_Navigation_Initialized_RESEARCH_ONLY.nds"
FIXTURE = ROOT / "fixture.json"
FOREST, FIRST = 274, 98
ADVANCE = [(frame, "A") for frame in range(4200, 10101, 350)]

scope = previous.scope | globals()
source = checked_text(previous.prepare_source, {
    "Maria's map guide with initialized setup and the original two paths beyond the dead end.":
        "Maria's initialized expedition with the original compass and instinct choices.",
})
exec(compile(source, __file__ + "::original-branch-commands", "exec"), scope)
prepare = scope["prepare"]
capture = FunctionType(previous.capture.__code__, scope)
startup = FunctionType(previous.startup.__code__, previous.startup.__globals__ | {"stage": stage})

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "compass", "instinct", "startup"))
    parser.add_argument("--down", type=int)
    args = parser.parse_args()
    if args.action in ("compass", "instinct"):
        inputs = ADVANCE
        if args.action == "instinct":
            assert args.down
            inputs = sorted(inputs + [(args.down, "DOWN")])
        capture("hunch" if args.action == "instinct" else args.action, inputs, 10301)
    else:
        globals()[args.action]()

