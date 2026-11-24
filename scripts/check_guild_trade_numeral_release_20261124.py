"""Run the registered Guild patch and startup checks on the four-price candidate."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import check_london_guild_release_20261124 as previous
from scripts import stage_guild_trade_numerals_20261124 as stage


PATCH, REBUILT, PATCH_PROOF, STARTUP_CAPTURE = (stage.ROOT / path for path in (
    "translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json", "startup/capture/capture_report.json"))


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("patch", "startup"))
    FunctionType(previous.main.__code__, vars(previous) | globals())(parser.parse_args().action)
