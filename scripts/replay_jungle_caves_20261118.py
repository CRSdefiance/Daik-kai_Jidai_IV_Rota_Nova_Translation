"""Exercise both original cave branches from the initialized Maria entry."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_forest_expeditions_20261118 as previous
from scripts import replay_london_guild_assignments_20261118 as startup_contract
from scripts import stage_jungle_caves_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
ROOT = stage.ROOT / "maria_cave_replay"
ROM = ROOT / "Maria_Caves_Initialized_RESEARCH_ONLY.nds"
FIXTURE = ROOT / "fixture.json"
FOREST, FIRST = 259, 496
ATTACK = [(n, "A") for n in range(4200, 11201, 350)]


scope = vars(previous) | globals()
prepare_source = checked_text(getsource(previous.prepare), {
    'cmd["source_offset"] == 320': 'cmd["source_offset"] == FIRST',
    'Maria forest encounter with initialized setup and the original choice branches.':
        'Maria cave encounter with initialized setup and the original attack and retreat branches.',
})
exec(compile(prepare_source, __file__ + "::same-initialized-scene-owner", "exec"), scope)
prepare = scope["prepare"]
capture = FunctionType(previous.capture.__code__, scope)
startup = FunctionType(startup_contract.startup.__code__, vars(startup_contract) | {"stage": stage})


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "attack", "run", "startup"))
    parser.add_argument("--down", type=int)
    args = parser.parse_args()
    if args.action == "attack":
        capture("attack", ATTACK, 11501)
    elif args.action == "run":
        assert args.down
        actions = sorted(ATTACK + [(args.down, "DOWN")])
        capture("run", actions, 10401)
    else:
        globals()[args.action]()
