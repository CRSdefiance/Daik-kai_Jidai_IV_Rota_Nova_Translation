"""Prove clean-input reconstruction and a fresh cold boot for the Guild candidate."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import check_supply_ratio_release_inputs_20261123 as checks
from scripts import stage_london_guild_display_20261124 as stage
from scripts.stage_cartridge_title_20261123 import read, reference, write


PATCH = stage.ROOT / "translation.xdelta"
REBUILT = stage.ROOT / "clean_rebuilt.nds"
PATCH_PROOF = stage.ROOT / "clean_patch_proof.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"


def main(action):
    source = read(stage.OUT)
    proof = dict(candidate=str(stage.ROM), candidate_sha256=source["candidate"]["sha256"],
                 predecessor_sha256=source["predecessor"]["sha256"], clean_input_sha256=source["clean_input"]["sha256"])
    scope = vars(checks) | dict(RELEASE=stage.play.active.RELEASE, PATCH=PATCH, REBUILT=REBUILT, STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(getattr(checks, action).__code__, scope)(proof)
    if action == "patch":
        write(PATCH_PROOF, dict(clean_input_sha256=proof["clean_input_sha256"], candidate=reference(stage.ROM),
                                patch=reference(PATCH), rebuilt=reference(REBUILT), byte_exact=True))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("patch", "startup"))
    main(cli.parse_args().action)
