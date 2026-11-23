"""Capture normal Inn and initialized rumor paths for the cumulative candidate."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import replay_inn_numerals_20261119 as predecessor
from scripts import stage_inn_numerals_context_20261119 as stage

inn = predecessor.inn
CAPTURE = stage.ROOT/"istanbul"
STARTUP = stage.ROOT/"own_startup"
STARTUP_PROOF = stage.ROOT/"own_startup_verification.json"
PLAYBACK = stage.ROOT/"verified_istanbul_numerals.json"


if __name__=="__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("capture","startup","patch"))
    task = getattr(predecessor,parser.parse_args().action)
    FunctionType(task.__code__,vars(predecessor)|globals())()
