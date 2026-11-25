"""Prove the cartridge-title build reconstructs exactly and cold-boots normally."""

from argparse import ArgumentParser
from os import link, replace
from types import FunctionType

from scripts import check_supply_ratio_release_inputs_20261123 as inherited
from scripts import stage_cartridge_title_20261123 as stage


PATCH = stage.WORK / "translation.xdelta"
REBUILT = stage.WORK / "clean_rebuilt.nds"
STARTUP_CAPTURE = stage.EVIDENCE / "startup/capture/capture_report.json"
PATCH_PROOF = stage.EVIDENCE / "clean_patch_proof.json"


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("check", choices=("patch", "startup"))
    check = parser.parse_args().check
    use = getattr(inherited, check)
    scope = use.__globals__ | dict(PATCH=PATCH, REBUILT=REBUILT, RELEASE=stage.PARENT_RELEASE,
                                   STARTUP_CAPTURE=STARTUP_CAPTURE)
    evidence = stage.read(stage.PROOF)
    proof = dict(candidate=str(stage.ROM), candidate_sha256=evidence["candidate"]["sha256"],
                  clean_input_sha256=evidence["clean"]["sha256"], predecessor_sha256=evidence["parent"]["sha256"])
    FunctionType(use.__code__, scope)(proof)
    if check == "patch":
        assert stage.digest(REBUILT) == proof["candidate_sha256"]
        alias = stage.WORK / "verified_rebuild.link"
        link(stage.ROM, alias)
        replace(alias, REBUILT)
        assert stage.ROM.samefile(REBUILT)
        stage.write(PATCH_PROOF, dict(clean_sha256=proof["clean_input_sha256"], candidate_sha256=proof["candidate_sha256"],
            patch=stage.reference(PATCH), byte_exact=True, exact_rebuild_retained_as_hardlink=True))


if __name__ == "__main__":
    main()
