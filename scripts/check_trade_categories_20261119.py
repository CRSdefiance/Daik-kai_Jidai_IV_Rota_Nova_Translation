"""Replay Trade and verify the category candidate's startup and clean patch."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import check_trade_labels_20261119 as prior
from scripts import stage_trade_categories_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

replay,verification,inn = prior.replay,prior.verification,prior.inn
CAPTURE = stage.ROOT/"trade"
STARTUP = stage.ROOT/"own_startup"
STARTUP_PROOF = stage.ROOT/"own_startup_verification.json"
PLAYBACK = stage.ROOT/"verified_trade_categories.json"


def capture():
    code = checked_text(getsource(replay.capture),{
        "from scripts import stage_trade_labels_20261119 as stage":
            "from scripts import stage_trade_categories_20261119 as stage",
    })
    scope = vars(replay)|dict(ROOT=stage.ROOT)
    exec(compile(code,__file__+"::trade_categories","exec"),scope)
    scope["capture"]("trade")


if __name__=="__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("capture","startup","patch"))
    action = parser.parse_args().action
    if action=="capture":
        capture()
    else:
        task = getattr(verification,action)
        FunctionType(task.__code__,vars(verification)|globals())()
