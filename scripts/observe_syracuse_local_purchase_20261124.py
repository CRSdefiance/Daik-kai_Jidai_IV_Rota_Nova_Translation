"""Replay an ordinary Syracuse Local purchase on the registered Maria ROM."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType

from scripts import observe_maria_system_quit_20261124 as active
from scripts import observe_syracuse_services_20261124 as prior


ROOT = prior.ROOT.with_name("syracuse_local_purchase_20261124")


def main(root):
    bindings = vars(prior) | dict(
        ROOT=root, CONTROLLER=root / "controller.jsonl", RELEASE=active.RELEASE,
        __file__=__file__,
    )
    FunctionType(prior.main.__code__, bindings)()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT)
    main(parser.parse_args().out)
