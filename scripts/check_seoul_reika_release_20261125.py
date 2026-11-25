"""Prove exact clean-input reconstruction and independent startup for Seoul."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import check_supply_ratio_release_inputs_20261123 as checks
from scripts import replay_seoul_reika_20261125 as stage
from scripts.stage_cartridge_title_20261123 import read, reference, write


PATCH = stage.ROOT / "translation.xdelta"
REBUILT = stage.ROOT / "clean_rebuilt.nds"
PATCH_PROOF = stage.ROOT / "clean_patch_proof.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
QA = stage.ROOT / "qa_passed.xml"


def main(action):
    parent_path = stage.play.current.RELEASE
    stored, previous = map(read, (stage.STAGED, parent_path))
    candidate = reference(stage.ROM)
    assert stored["candidate_sha256"] == candidate["sha256"] and stored["exact_parent_inverse"]
    assert stored["parent_release"] == reference(parent_path)
    proof = dict(candidate=str(stage.ROM), candidate_sha256=candidate["sha256"],
                 predecessor_sha256=previous["candidate_sha256"], clean_input_sha256=previous["clean_input_sha256"])
    scope = vars(checks) | dict(RELEASE=parent_path, PATCH=PATCH, REBUILT=REBUILT, STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(getattr(checks, action).__code__, scope)(proof)
    if action == "patch":
        write(PATCH_PROOF, dict(clean_input_sha256=proof["clean_input_sha256"], candidate=candidate,
                               patch=reference(PATCH), rebuilt=reference(REBUILT), byte_exact=True))


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("patch", "startup"))
    main(parser.parse_args().action)
