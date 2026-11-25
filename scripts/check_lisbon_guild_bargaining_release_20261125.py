"""Run the registered startup and clean reconstruction checks for Guild bargaining."""

from argparse import ArgumentParser
from types import FunctionType, SimpleNamespace

from scripts import check_fleet_diversion_release_20261125 as earlier
from scripts import replay_lisbon_guild_bargaining_20261125 as replay


ROOT = replay.ROOT
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
PATCH_PROOF = ROOT / "clean_patch_proof.json"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
QA = ROOT / "qa_passed.xml"


def main(action):
    stage = SimpleNamespace(draft=replay.draft, PROOF=replay.STAGED, ROM=replay.ROM)
    scope = vars(earlier) | dict(stage=stage, PATCH=PATCH, REBUILT=REBUILT, PATCH_PROOF=PATCH_PROOF,
                                 STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(earlier.main.__code__, scope)(action)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("patch", "startup"))
    main(parser.parse_args().action)
