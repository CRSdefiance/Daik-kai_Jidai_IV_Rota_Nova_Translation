"""Trace ordinary saved-game Village and Tavern visits on the registered ROM."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_cabin_square_wrap_20261123 as current


base = current.base
ROOT = Path(".codex-release-work/shared_display_20261123/village_tavern")
HISTORIES = {
    "village": "village_ui_v609_compact_probe",
    "tavern": "tavern_editorial_v767_decline_v767",
}


def schedule(case):
    source = Path("work/emulation_v193") / HISTORIES[case] / "capture_report.json"
    historical = base.load(source)
    assert historical["cold_boot"] and not historical["savestate_loaded"] and not historical["callback_errors"]
    assert not any(value for key, value in historical.items() if key.startswith("synthetic_"))
    donor = historical["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    end = historical["frames"]
    frames = {row["frame"] for row in historical["frames_captured"] if row["frame"] >= 3200}
    frames.update(range(3200, end, 100))
    return historical["scripted_input_schedule"], sorted(frames), end, source, donor


def replay(case):
    release = base.load(current.RELEASE)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / case).exists()
    scope = vars(playback) | dict(ROOT=ROOT, parent=current, observer=trace.scoped_observer,
        get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + "::ordinary_shared_visits", "exec"), scope)
    scope["main"](case)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=HISTORIES)
    replay(parser.parse_args().case)
