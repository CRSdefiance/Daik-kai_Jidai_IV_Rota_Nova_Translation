"""Run the clean-input, independent startup, and focused package checks."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import check_supply_ratio_release_inputs_20261123 as checks
from scripts import stage_claudio_opening_wrap_20261124 as stage
from scripts.stage_cartridge_title_20261123 import read, reference, write

PATCH = stage.ROOT / "translation.xdelta"
REBUILT = stage.ROOT / "clean_rebuilt.nds"
PATCH_PROOF = stage.ROOT / "clean_patch_proof.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
QA = stage.ROOT / "qa_passed.xml"


def main(action):
    stored = read(stage.STORED)
    assert stored["candidate"] == reference(stage.ROM)
    proof = dict(candidate=str(stage.ROM), candidate_sha256=stored["candidate"]["sha256"],
        predecessor_sha256=stored["previous"]["sha256"], clean_input_sha256=stored["clean"]["sha256"])
    scope = vars(checks) | dict(RELEASE=stage.parent.RELEASE, PATCH=PATCH, REBUILT=REBUILT, STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(getattr(checks, action).__code__, scope)(proof)
    if action == "patch":
        assert reference(REBUILT)["sha256"] == proof["candidate_sha256"]
        write(PATCH_PROOF, dict(clean_input_sha256=proof["clean_input_sha256"], candidate=reference(stage.ROM),
            patch=reference(PATCH), rebuilt=reference(REBUILT), byte_exact=True))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("patch", "startup"))
    main(cli.parse_args().action)
