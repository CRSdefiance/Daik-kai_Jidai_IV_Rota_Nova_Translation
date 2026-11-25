"""Run the registered clean-input and cold-start checks for the Azores return candidate."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import check_supply_ratio_release_inputs_20261123 as checks
from scripts.stage_azores_return_20261123 import PROOF, RELEASE, ROM, ROOT, read, reference, write


PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
PATCH_PROOF = ROOT / "clean_patch_proof.json"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"


def main(action):
    registered, staged = read(RELEASE), read(PROOF)
    proof = dict(candidate=str(ROM), candidate_sha256=staged["candidate_sha256"],
                 clean_input_sha256=registered["clean_input_sha256"],
                 predecessor_sha256=staged["verified_predecessor_sha256"])
    scope = vars(checks) | dict(RELEASE=RELEASE, PATCH=PATCH, REBUILT=REBUILT, STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(getattr(checks, action).__code__, scope)(proof)
    if action == "patch":
        write(PATCH_PROOF, dict(clean_input_sha256=proof["clean_input_sha256"], candidate=reference(ROM),
                               patch=reference(PATCH), rebuilt=reference(REBUILT), byte_exact=True))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("patch", "startup"))
    main(cli.parse_args().action)
