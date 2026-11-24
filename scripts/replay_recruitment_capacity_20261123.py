"""Verify the revised tavern capacity prompts in ordinary Azores and Istanbul play."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import check_supply_ratio_release_inputs_20261123 as release_checks
from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts import replay_recruit_crew_20261120 as istanbul
from scripts import stage_recruitment_capacity_wraps_20261123 as stage
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest, read, reference, write


ROOT = stage.ROOT
PLAY = ROOT / "ordinary"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
PATCH_PROOF = ROOT / "clean_patch_proof.json"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
AZORES_FRAMES = (8550, 13600, 13880, 15050, 15900, 16400, 17240, 17520, 17800, 18080, 18360)


def schedule(case):
    path = stage.VISIT if case == "azores" else istanbul.HISTORY
    if case == "azores":
        assert digest(path) == stage.VISIT_SHA
    previous = read(path)
    assert previous["cold_boot"] and not previous["savestate_loaded"] and not previous["callback_errors"]
    assert not any(value for key, value in previous.items() if key.startswith("synthetic_"))
    frames = AZORES_FRAMES if case == "azores" else istanbul.FRAMES
    return previous["scripted_input_schedule"], frames, previous["frames"], path, previous["battery_save_preloaded"]


def replay(case):
    PLAY.mkdir(exist_ok=True)
    selected = SimpleNamespace(ROM=stage.ROM, RELEASE=stage.PROOF)
    scope = vars(playback) | dict(parent=selected, ROOT=PLAY, observer=trace.scoped_observer,
                                 get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    source = checked_text(getsource(playback.main), {
        "'--capture-at', *map(str, frames)]": "'--dump-capture-ram', '--capture-at', *map(str, frames)]",
    })
    exec(compile(source, __file__ + "::ordinary-recruitment", "exec"), scope)
    scope["main"](case)


def check(action):
    release, proof = map(read, (stage.parent.RELEASE, stage.PROOF))
    arguments = proof | dict(predecessor_sha256=release["candidate_sha256"])
    scope = vars(release_checks) | dict(RELEASE=stage.parent.RELEASE, PATCH=PATCH, REBUILT=REBUILT,
                                        STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(getattr(release_checks, action).__code__, scope)(arguments)
    if action == "patch":
        write(PATCH_PROOF, dict(clean_input_sha256=proof["clean_input_sha256"], candidate=reference(stage.ROM),
                               patch=reference(PATCH), rebuilt=reference(REBUILT), byte_exact=True))


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("azores", "istanbul", "patch", "startup"))
    action = parser.parse_args().action
    (replay if action in {"azores", "istanbul"} else check)(action)
