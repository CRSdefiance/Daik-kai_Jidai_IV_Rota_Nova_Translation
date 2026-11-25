"""Exercise Maria's two revised map choices through the original scene branches."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import replay_jungle_caves_20261118 as previous
from scripts import replay_london_guild_assignments_20261118 as startup_contract
from scripts import stage_ruins_clues_and_guides_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
ROOT = stage.ROOT / "maria_map_replay"
ROM = ROOT / "Maria_Map_Guide_Initialized_RESEARCH_ONLY.nds"
FIXTURE = ROOT / "fixture.json"
FOREST, FIRST = 264, 512
ADVANCE = [(n, "A") for n in range(4200, 8701, 350)]


scope = previous.scope | globals()
prepare_source = checked_text(previous.prepare_source, {
    "Maria cave encounter with initialized setup and the original attack and retreat branches.":
        "Maria's map guide with initialized setup and the original two paths beyond the dead end.",
})
exec(compile(prepare_source, __file__ + "::same-initialized-scene-owner", "exec"), scope)
prepare = scope["prepare"]
capture = FunctionType(previous.capture.__code__, scope)
startup = FunctionType(startup_contract.startup.__code__, vars(startup_contract) | {"stage": stage})


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "push", "look", "startup"))
    parser.add_argument("--down", type=int)
    args = parser.parse_args()
    if args.action == "push":
        capture("push", ADVANCE, 9001)
    elif args.action == "look":
        assert args.down
        actions = sorted(ADVANCE + [(args.down, "DOWN")])
        capture("look", actions, 8401)
    else:
        globals()[args.action]()
