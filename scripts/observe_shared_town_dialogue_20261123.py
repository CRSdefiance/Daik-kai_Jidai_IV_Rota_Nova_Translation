"""Observe common dialogue in ordinary gameplay on the registered Hodram build."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from scripts import observe_amsterdam_square_current_20261114 as amsterdam
from scripts import observe_online_gallery_common_v1 as playback
from scripts import register_hodram_midroute_followups_20261123 as release
from scripts.observe_regional_town_dialogue_20261115 import VISITS
from scripts.observe_setup_save_common_v1 import scoped_observer
from scripts.source_locked_derivation_v5118 import checked_text

base = release.base
ROOT = Path(".codex-release-work/shared_display_20261123/ordinary")
HISTORY = {
    "athens": "tavern_family_v508_athens",
    "nagasaki": "japan_facilities_v518_reload",
}
CASES = ("amsterdam", *HISTORY)


def schedule(case):
    if case == "amsterdam":
        return amsterdam.schedule("food")
    reference = Path("work/emulation_v193") / HISTORY[case] / "capture_report.json"
    previous = base.load(reference)
    assert previous["cold_boot"] and not previous["savestate_loaded"] and not previous["callback_errors"]
    assert not any(value for key, value in previous.items() if key.startswith("synthetic_"))
    donor = previous["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"]) == donor["source_sha256"]
    if case == "athens":
        end = 13000
        events = [event for event in previous["scripted_input_schedule"] if event["start"] + 199 < end]
        return events, [event["start"] + 149 for event in events if event["start"] >= 2801], end, reference, donor
    events = [event for event in previous["scripted_input_schedule"] if event["start"] <= 2801]
    visits = VISITS + ((11801, (125, 35)), (12201, "A"), (12601, "A"), (13001, "B"), (13401, "B"))
    for frame, action in visits:
        controls = dict(touch=list(action), buttons=[]) if isinstance(action, tuple) else dict(buttons=[action])
        events.append(dict(start=frame, duration=8, **controls))
    return events, [3720, *(frame + 149 for frame, _ in visits)], 13700, reference, donor


def main(case):
    evidence = base.load(release.RELEASE)
    assert base.digest(release.ROM) == evidence["candidate_sha256"]
    assert base.digest(base.REGISTRY) == evidence["registry_sha256"]
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / case).exists()
    source = checked_text(getsource(playback.main), {
        "    installed = []": "    if '--touchscreen' not in argv:\n        argv.append('--touchscreen')\n    installed = []",
    })
    scope = vars(playback) | dict(ROOT=ROOT, parent=release, observer=scoped_observer,
        get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(source, __file__ + "::registered-ordinary-visits", "exec"), scope)
    scope["main"](case)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("case", choices=CASES)
    main(cli.parse_args().case)
