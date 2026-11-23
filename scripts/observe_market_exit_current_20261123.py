"""Replay the original Lisbon Trade exit controls on the registered candidate."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import observe_market_restart_common_20261114 as earlier
from scripts import observe_title_variant_display_20261123 as live


ROOT = live.ROOT.with_name("market_exit_current")


def main(case):
    release = live.current.base.load(live.current.RELEASE)
    assert live.current.base.digest(live.current.base.REGISTRY) == release["registry_sha256"]
    scope = vars(earlier) | dict(ROOT=ROOT, current=live.current, FOCUS=set(range(3668)), __file__=__file__)
    FunctionType(earlier.main.__code__, scope)(case)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("case", choices=earlier.TRADE_ACTIONS)
    main(cli.parse_args().case)
