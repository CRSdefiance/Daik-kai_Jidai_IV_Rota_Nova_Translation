"""Trace ordinary voyages and crew conditions on the registered Tavern candidate."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_tavern_nearby_town_wrap_20261123 as current


base = current.base
ROOT = Path(".codex-release-work/additional_voyages_20261123")
HISTORIES = {
    "tripoli_arrival": "environment_voyage_v510_leg",
    "ceuta_leg": "environment_voyage_v513",
    "crew_conditions": "conditions_sailors_v388",
}


def schedule(case):
    reference = Path("work/emulation_v193") / HISTORIES[case] / "capture_report.json"
    prior = base.load(reference)
    assert prior["cold_boot"] and not prior["savestate_loaded"] and not prior["callback_errors"]
    assert not any(value for field, value in prior.items() if field.startswith("synthetic_"))
    donor = prior["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"]) == donor["source_sha256"]
    end = prior["frames"]
    frames = {row["frame"] for row in prior["frames_captured"] if row["frame"] >= 3200}
    frames.update(range(3200, end, 120))
    return prior["scripted_input_schedule"], sorted(frames), end, reference, donor


def run(case):
    release = base.load(current.RELEASE)
    assert release["candidate_sha256"] == base.digest(current.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert not (ROOT / case).exists()
    scope = vars(playback) | dict(ROOT=ROOT, parent=current, observer=trace.scoped_observer,
        get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + "::ordinary-voyage", "exec"), scope)
    scope["main"](case)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=HISTORIES)
    run(parser.parse_args().case)
