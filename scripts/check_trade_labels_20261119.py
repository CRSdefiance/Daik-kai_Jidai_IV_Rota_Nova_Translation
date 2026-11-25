"""Check the Trade labels, cold startup and clean-input reconstruction."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import replay_inn_numerals_20261119 as verification
from scripts import replay_trade_labels_20261119 as replay
from scripts import stage_trade_labels_20261119 as stage

inn = verification.inn
STARTUP = stage.ROOT/"own_startup"
STARTUP_PROOF = stage.ROOT/"own_startup_verification.json"
PLAYBACK = stage.ROOT/"verified_trade_labels.json"


if __name__=="__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("capture","startup","patch"))
    action = parser.parse_args().action
    if action=="capture":
        replay.capture("corrected")
    else:
        task = getattr(verification,action)
        FunctionType(task.__code__,vars(verification)|globals())()
