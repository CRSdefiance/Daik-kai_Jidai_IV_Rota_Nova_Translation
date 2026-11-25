"""Recheck the final Inn build with the source-bound v2 test drivers."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import replay_inn_numerals_20261119 as first_game
from scripts import replay_inn_numerals_context_20261119 as earlier_game
from scripts import replay_inn_raid_numerals_20261119 as earlier_raid
from scripts import stage_inn_numerals_finish_20261119 as stage
from scripts import verify_inn_numerals_gameplay_20261119 as earlier_verify
from scripts import verify_inn_numerals_native_20261119 as earlier_native
from scripts.source_locked_derivation_v5118 import checked_text

CAPTURE = stage.ROOT/"istanbul"
STARTUP = stage.ROOT/"own_startup"
STARTUP_PROOF = stage.ROOT/"own_startup_verification.json"
PLAYBACK = stage.ROOT/"verified_istanbul_numerals.json"
inn = earlier_game.inn
base = stage.base


def derived(module,changes,extra=None):
    path = Path(module.__file__)
    source = checked_text(path.read_text(encoding="utf-8"),changes)
    scope = vars(module)|dict(__name__="inn_final_verification",__file__=__file__)|(extra or {})
    exec(compile(source,str(path)+"::final_inn", "exec"),scope)
    return scope


def raid_scope():
    return derived(earlier_raid,{
        "from scripts import stage_inn_numerals_context_20261119 as stage":
        "from scripts import stage_inn_numerals_finish_20261119 as stage",
    })


def native_check():
    scope = derived(earlier_native,{
        "from scripts import stage_inn_numerals_context_20261119 as stage":
        "from scripts import stage_inn_numerals_finish_20261119 as stage",
    })
    scope["main"]()


def gameplay():
    scope = derived(earlier_verify,{
        "from scripts import replay_inn_numerals_context_20261119 as game": "game = final_game",
        "from scripts import replay_inn_raid_numerals_20261119 as raid": "raid = final_raid",
        'and not case["findings"]\n': 'and not case["findings"]\n    assert case["lines"][-1].endswith("What a lousy thing to do!")\n',
    },dict(final_game=SimpleNamespace(stage=stage,inn=inn,CAPTURE=CAPTURE,PLAYBACK=PLAYBACK),
           final_raid=SimpleNamespace(**raid_scope())))
    scope["main"]()


if __name__=="__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("capture","startup","patch","raid","native","verify"))
    action = parser.parse_args().action
    if action=="raid":
        raid_scope()["capture"]()
    elif action=="native":
        native_check()
    elif action=="verify":
        gameplay()
    else:
        task = getattr(first_game,action)
        FunctionType(task.__code__,vars(first_game)|globals())()
