"""Leave Tripoli's port menu before the ordinary Square and Tavern visit."""

from inspect import getsource
from types import SimpleNamespace

from scripts import observe_tripoli_copenhagen_20261122 as visits


def schedule(case):
    events, _, _, old, donor = visits.schedule("tripoli")
    startup = [row for row in events if row["start"] <= 3401]
    startup.append(dict(start=3721, duration=8, buttons=["B"]))
    steps = [row | {"start": row["start"] + 600} for row in events if row["start"] > 3401]
    return startup + steps, [3720, 4000, *(row["start"] + 149 for row in steps)], 12300, old, donor


if __name__ == "__main__":
    scope = vars(visits.playback) | dict(ROOT=visits.ROOT, parent=SimpleNamespace(ROM=visits.stage.ROM, RELEASE=visits.stage.PROOF),
        observer=visits.precedent.scoped_observer, get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(getsource(visits.playback.main), __file__ + "::ordinary-Tripoli-visit", "exec"), scope)
    scope["main"]("tripoli_square")
