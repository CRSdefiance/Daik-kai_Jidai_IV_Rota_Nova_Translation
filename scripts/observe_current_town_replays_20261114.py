"""Replay ordinary saved-game town visits on the current cumulative release."""

import argparse
from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_about_extras_20261114 as current

ROOT = Path("work/current_town_coverage_20261114_v3")
REPORTS = {
    "nagasaki": "japan_facilities_v518_reload",
    "istanbul": "tavern_direct_actual_v2190_V2171",
    "amsterdam": "plaque_audit_v300_person",
}
EXTRA = {
    "nagasaki": [(5801, "A"), (6201, "A"), (6601, "B"), (7001, "B")],
    "istanbul": [],
    "amsterdam": [(8751, "B"), (9151, (21, 26)), (9551, "A"), (9951, "A"),
                  (10351, "A"), (10751, "A"), (11151, "A"), (11551, "B")],
}


def schedule(case):
    history = Path("work/emulation_v193") / REPORTS[case] / "capture_report.json"
    history_data = current.base.load(history)
    events = history_data["scripted_input_schedule"]
    donor = history_data.get("battery_save_preloaded")
    assert history_data["cold_boot"] and not history_data["savestate_loaded"]
    assert not history_data["callback_errors"]
    assert not any(value for key, value in history_data.items() if key.startswith("synthetic_"))
    if donor:
        assert current.base.digest(donor["source"]) == donor["source_sha256"]
    else:
        assert case == "amsterdam"
        events = [row for row in events if row["start"] < 8751]
    for frame, action in EXTRA[case]:
        fields = {"buttons": [action]} if isinstance(action, str) else {"touch": list(action), "buttons": []}
        events.append(dict(start=frame, duration=8, **fields))
    frames = [row["start"] + 150 for row in events if row["start"] >= (8400 if case == "amsterdam" else 2600)]
    return events, frames, frames[-1] + 40, history, donor


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=tuple(REPORTS))
    case = parser.parse_args().case
    env = vars(playback) | dict(ROOT=ROOT, parent=current, FOCUS=set(range(3668)),
        observer=trace.scoped_observer, get_schedule=schedule, __file__=__file__)
    source = getsource(playback.main)
    source = source.replace("    installed = []", "    if '--touchscreen' not in argv: argv.append('--touchscreen')\n    installed = []")
    exec(compile(source, __file__ + "::town-access-observer", "exec"), env)
    env["main"](case)


if __name__ == "__main__":
    main()
