"""Run the patched Inn confirmation, startup and clean reconstruction."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import replay_inn_conversations_20261119 as inn
from scripts import stage_inn_numerals_20261119 as stage

CAPTURE = stage.ROOT/"istanbul"
STARTUP = stage.ROOT/"own_startup"
STARTUP_PROOF = stage.ROOT/"own_startup_verification.json"
PLAYBACK = stage.ROOT/"verified_istanbul_numerals.json"


def capture():
    FunctionType(inn.capture.__code__,vars(inn)|globals())()


def startup():
    run = inn.boot.boot.boot_replay.previous.startup
    FunctionType(run.__code__,run.__globals__|{"stage":stage,"STARTUP":STARTUP})()
    scope = vars(inn.boot)|vars(inn)|globals()|{"boot":inn.boot.boot}
    FunctionType(inn.boot.verify_startup.__code__,scope)()


def patch():
    FunctionType(inn.patch.__code__,vars(inn)|globals())()


if __name__=="__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("capture","startup","patch"))
    globals()[parser.parse_args().action]()
