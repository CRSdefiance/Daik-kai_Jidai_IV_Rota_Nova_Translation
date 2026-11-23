"""Prepare the exact clean-input patch and independent startup for assigned Fleet Info."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import check_supply_ratio_release_inputs_20261123 as known
from scripts.observe_assigned_fleet_detail_20261123 import RELEASE, ROOT
from scripts.stage_cartridge_title_20261123 import read, reference, write

WORK = ROOT / "packed_report"
ROM = WORK / "Assigned_Fleet_Info_STAGED.nds"
PATCH, REBUILT = WORK / "translation.xdelta", WORK / "clean_rebuilt.nds"
PATCH_PROOF = WORK / "clean_patch_proof.json"
STARTUP_CAPTURE = ROOT.with_name("fleet_info_startup") / "capture/capture_report.json"


def check(action):
    stored = read(WORK / "stage.json")
    work = getattr(known, action)
    namespace = vars(known) | dict(RELEASE=RELEASE, PATCH=PATCH, REBUILT=REBUILT, STARTUP_CAPTURE=STARTUP_CAPTURE)
    proof = dict(candidate=str(ROM), candidate_sha256=stored["staged"]["sha256"],
                 clean_input_sha256=stored["clean"]["sha256"],
                 predecessor_sha256=stored["registered_predecessor"]["sha256"])
    FunctionType(work.__code__, namespace)(proof)
    if action == "patch":
        write(PATCH_PROOF, dict(clean_input_sha256=proof["clean_input_sha256"], candidate=reference(ROM),
                               patch=reference(PATCH), rebuilt=reference(REBUILT), byte_exact=True))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("patch", "startup"))
    check(cli.parse_args().action)
