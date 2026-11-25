"""Prove byte-exact clean reconstruction and independent startup."""

from argparse import ArgumentParser
from types import FunctionType, SimpleNamespace

from scripts import check_fleet_diversion_release_20261125 as earlier
from scripts import stage_levelup_numerals_20261125 as stage


PATCH, REBUILT = stage.ROOT / "translation.xdelta", stage.ROOT / "clean_rebuilt.nds"
PATCH_PROOF = stage.ROOT / "clean_patch_proof.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
QA = stage.ROOT / "qa_passed.xml"


def main(action):
    inputs = SimpleNamespace(draft=SimpleNamespace(current=stage.current), PROOF=stage.PROOF, ROM=stage.ROM)
    scope = vars(earlier) | dict(stage=inputs, PATCH=PATCH, REBUILT=REBUILT, PATCH_PROOF=PATCH_PROOF,
                                 STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(earlier.main.__code__, scope)(action)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("patch", "startup"))
    main(parser.parse_args().action)
