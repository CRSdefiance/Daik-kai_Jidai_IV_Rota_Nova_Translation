"""Observe original Square and Tavern selection in two new port visits."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_regional_town_dialogue_20261115 as precedent
from scripts import stage_aziza_shamshir_20261122 as stage


base = stage.base
ROOT = stage.ROOT / "ordinary_town"
PORTS = {
    "tripoli": ("environment_voyage_v510_tripoli_reload", 3401),
    "copenhagen": ("copenhagen_saved_reload_v420", 2801),
}


def schedule(case):
    city = "tripoli" if case == "tripoli_docked" else case
    history, stop = PORTS[city]
    path = Path("work/emulation_v193") / history / "capture_report.json"
    previous = base.load(path)
    assert previous["cold_boot"] and not previous["savestate_loaded"] and not previous["callback_errors"]
    donor = previous["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"]) == donor["source_sha256"]
    events = [row for row in previous["scripted_input_schedule"] if row["start"] <= stop]
    prefix, delay = [3720], 0
    if case == "tripoli_docked":
        events.extend(dict(start=n, duration=8, buttons=[key]) for n, key in ((3721, "DOWN"), (4001, "A")))
        prefix, delay = [3720, 3870, 4150], 600
    for frame, action in precedent.VISITS:
        fields = dict(touch=list(action), buttons=[]) if isinstance(action, tuple) else dict(buttons=[action])
        events.append(dict(start=frame + delay, duration=8, **fields))
    return events, [*prefix, *(frame + delay + 149 for frame, _ in precedent.VISITS)], 11700 + delay, path, donor


def observe(city):
    scope = vars(playback) | dict(ROOT=ROOT, parent=SimpleNamespace(ROM=stage.ROM, RELEASE=stage.PROOF),
        observer=precedent.scoped_observer, get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + "::ordinary-port-visit", "exec"), scope)
    scope["main"](city)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("city", choices=(*PORTS, "tripoli_docked"))
    observe(cli.parse_args().city)
