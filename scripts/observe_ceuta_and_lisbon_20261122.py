"""Observe ordinary Square and Tavern visits from established Ceuta and Lisbon saves."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_tripoli_copenhagen_20261122 as prior
from scripts import stage_rafael_charlotte_and_maria_20261122 as stage


base = stage.base
ROOT = stage.ROOT / "ordinary_town"
PORTS = {
    "ceuta": ("environment_voyage_v512_ceuta_reload", 3401, 600),
    "lisbon": ("lisbon_reload_v470", 2801, 0),
}


def schedule(city):
    directory, stop, delay = PORTS[city]
    source = Path("work/emulation_v193") / directory / "capture_report.json"
    previous = base.load(source)
    assert previous["cold_boot"] and not previous["savestate_loaded"] and not previous["callback_errors"]
    assert not any(value for key, value in previous.items() if key.startswith("synthetic_"))
    donor = previous["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    events = [action for action in previous["scripted_input_schedule"] if action["start"] <= stop]
    if city == "ceuta":
        events.extend(dict(start=frame, duration=8, buttons=[key])
                      for frame, key in ((3721, "DOWN"), (4001, "A")))
    for frame, action in prior.precedent.VISITS:
        fields = dict(touch=list(action), buttons=[]) if isinstance(action, tuple) else dict(buttons=[action])
        events.append(dict(start=frame + delay, duration=8, **fields))
    return events, [3720 + delay, *(frame + delay + 149 for frame, _ in prior.precedent.VISITS)], 11700 + delay, source, donor


def observe(city):
    scope = vars(prior.playback) | dict(ROOT=ROOT, parent=SimpleNamespace(ROM=stage.ROM, RELEASE=stage.PROOF),
        observer=prior.precedent.scoped_observer, get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(getsource(prior.playback.main), __file__ + "::ordinary-port-visit", "exec"), scope)
    scope["main"](city)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("city", choices=PORTS)
    observe(cli.parse_args().city)
