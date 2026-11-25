"""Run a fresh candidate startup and an initialized Maria quicksand sample."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import replay_ruins_clues_and_guides_20261118 as previous
from scripts import stage_overland_passages_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
ROOT = stage.ROOT / "maria_quicksand_replay"
ROM = ROOT / "Maria_Quicksand_Initialized_RESEARCH_ONLY.nds"
FIXTURE = ROOT / "fixture.json"
FOREST, FIRST = 269, 376
ADVANCE = [(n, "A") for n in range(4200, 9101, 350)]

scope = previous.scope | globals()
source = checked_text(previous.prepare_source, {
    "Maria's map guide with initialized setup and the original two paths beyond the dead end.":
        "Maria's initialized desert expedition and original quicksand choices.",
})
exec(compile(source, __file__ + "::same-initialized-scene-owner", "exec"), scope)
prepare = scope["prepare"]
capture = FunctionType(previous.capture.__code__, scope)
startup = FunctionType(previous.startup.__code__, previous.startup.__globals__ | {"stage": stage})


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "pull", "call", "startup"))
    parser.add_argument("--down", type=int)
    args = parser.parse_args()
    if args.action in ("pull", "call"):
        inputs = ADVANCE
        if args.action == "call":
            assert args.down
            inputs = sorted(inputs + [(args.down, "DOWN")])
        capture(args.action, inputs, 9451)
    else:
        globals()[args.action]()
