"""Observe the original Tripoli Tavern through an ordinary saved game."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_tripoli_copenhagen_20261122 as visits
from scripts import stage_palace_eirene_pereira_london_20261122 as stage


ROOT = stage.ROOT / "ordinary_town"
CASE = "tripoli_tavern"


def schedule(case):
    assert case == CASE
    events, _, _, history, donor = visits.schedule("tripoli")
    events = [row for row in events if row["start"] <= 3401]
    events.extend((
        dict(start=3721, duration=8, buttons=["B"]),
        dict(start=4401, duration=8, buttons=[], touch=[80, 29]),
        dict(start=4801, duration=8, buttons=["A"]),
        dict(start=5201, duration=8, buttons=["A"]),
        dict(start=5601, duration=8, buttons=["A"]),
        dict(start=6001, duration=8, buttons=["B"]),
        dict(start=6401, duration=8, buttons=["B"]),
    ))
    return events, [4000, 4550, 4950, 5350, 5750, 6150, 6550], 6800, history, donor


if __name__ == "__main__":
    scope = vars(visits.playback) | dict(ROOT=ROOT, parent=SimpleNamespace(ROM=stage.ROM, RELEASE=stage.PROOF),
        observer=visits.precedent.scoped_observer, get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(getsource(visits.playback.main), __file__ + "::ordinary-tavern", "exec"), scope)
    scope["main"](CASE)
