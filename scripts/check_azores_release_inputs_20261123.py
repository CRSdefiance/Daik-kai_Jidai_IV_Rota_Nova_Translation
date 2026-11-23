"""Check the staged Azores ROM's clean-input reconstruction and startup."""

from argparse import ArgumentParser
from inspect import getsource

from scripts import check_supply_ratio_release_inputs_20261123 as previous
from scripts import stage_azores_wording_20261123 as stage


PATCH = stage.ROM.parent / "translation.xdelta"
REBUILT = stage.ROM.parent / "clean_rebuilt.nds"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("patch", "startup"))
    action = parser.parse_args().action
    scope = vars(previous) | dict(PATCH=PATCH, REBUILT=REBUILT, RELEASE=stage.RELEASE, STARTUP_CAPTURE=STARTUP_CAPTURE)
    # Reuse the existing byte comparison and exact six-frame startup schedule.
    source = getsource(getattr(previous, action))
    exec(compile(source, __file__ + "::" + action, "exec"), scope)
    stored = stage.read(stage.PROOF)
    source_keys = dict(candidate=str(stage.ROM), candidate_sha256=stored["candidate_sha256"],
                       clean_input_sha256=stored["clean_sha256"], predecessor_sha256=stored["predecessor"]["sha256"])
    scope[action](source_keys)


if __name__ == "__main__":
    main()
