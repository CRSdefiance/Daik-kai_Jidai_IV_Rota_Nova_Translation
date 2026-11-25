"""Initialize Maria's desert event after its map gate, preserving all three choice branches."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_forest_expeditions_20261118 as inherited
from scripts import stage_desert_censer_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = stage.ROOT / "dune"
ROM = ROOT / "Maria_Desert_RESEARCH_ONLY.nds"
FIXTURE = ROOT / "fixture.json"
FOREST, FIRST = 285, 360

source = checked_text(getsource(inherited.prepare), {
    'cmd["source_offset"] == 320': 'cmd["source_offset"] == FIRST',
    "Maria forest encounter with initialized setup and the original choice branches.":
        "Maria desert encounter with initialized setup and the original three choice branches.",
})
scope = vars(inherited) | globals()
exec(compile(source, __file__ + "::source-owned-event", "exec"), scope)
capture = FunctionType(inherited.capture.__code__, scope)

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "fight"))
    args = parser.parse_args()
    if args.action == "prepare":
        scope["prepare"]()
    else:
        capture("fight", [(n, "A") for n in range(4200, 8901, 350)], 9101)
