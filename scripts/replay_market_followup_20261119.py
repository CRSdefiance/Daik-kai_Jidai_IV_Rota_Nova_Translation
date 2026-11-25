"""Replay the original recommendation branch and current-ROM startup."""

from argparse import ArgumentParser
from types import FunctionType, SimpleNamespace

from scripts import replay_market_reward_dialogue_20261115 as previous
from scripts import replay_sea_hazard_dialogue_20261119 as startup_check
from scripts import stage_market_followup_20261119 as build


STARTUP = build.ROOT / "startup_fixture"


def gameplay():
    stage = SimpleNamespace(base=build.base, ROOT=build.ROOT, ROM=build.ROM, STORED=build.PROOF,
                            ARM=build.ARM, digest=build.native.digest)
    replay = FunctionType(previous.reward.__code__, vars(previous) | {"stage": stage, "__file__": __file__})
    replay("reviewed", build.ROM)


def startup():
    run = FunctionType(startup_check.startup.__code__, vars(startup_check) | {"build": build, "STARTUP": STARTUP})
    run()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("gameplay", "startup"))
    globals()[parser.parse_args().action]()
