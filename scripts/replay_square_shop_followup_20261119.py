"""Check the Square referral in ordinary gameplay and replay registered startup."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import replay_ceuta_lesson_20261119 as boot
from scripts import replay_square_country_briefings_20261115 as previous
from scripts import stage_square_shop_followup_20261119 as stage

build = stage
STARTUP = stage.ROOT / "startup_fixture"


def main(case):
    if case == "startup":
        FunctionType(boot.startup.__code__, vars(boot) | globals())()
        return
    FunctionType(previous.main.__code__, vars(previous) | globals())(case)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("startup", "amsterdam"))
    main(parser.parse_args().case)
