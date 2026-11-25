"""Replay the final fleet letter with its repaired escape line."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import replay_crew_accounts_20261118 as earlier
from scripts import stage_crew_accounts_letter_wrap_20261118 as stage

CASE, EXCERPTS = earlier.CASE, earlier.EXCERPTS
SCOPE = earlier.SCOPE | {"stage": stage}
for function in ("excerpt_commands", "folder", "inputs", "prepare", "capture", "verify"):
    SCOPE[function] = FunctionType(earlier.SCOPE[function].__code__, SCOPE)

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "verify"))
    SCOPE[parser.parse_args().action](CASE)
