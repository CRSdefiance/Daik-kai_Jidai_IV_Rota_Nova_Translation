"""Observe ordinary sailing encounters and Tavern orders on the latest candidate."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from scripts import observe_lisbon_voyage_and_osaka_20261115 as voyage
from scripts import observe_regional_town_dialogue_20261115 as town
from scripts import register_regional_rumor_wrap_followups_20261123 as current


base = current.base
ROOT = Path(".codex-release-work/shared_display_20261123/current_shared_encounters")
VOYAGES = ("voyage", "osaka")
TAVERNS = ("tunis", "syracuse")
ORDER_INPUTS = ((10901, "A"), (11301, "A"), (11701, "A"), (12101, "A"), (12501, "B"))


def schedule(case):
    if case in VOYAGES:
        return voyage.schedule(case)
    inputs, frames, _, history, donor = town.schedule(case)
    prefix = [row for row in inputs if row["start"] <= 10601]
    prefix.extend(dict(start=frame, duration=8, buttons=[button]) for frame, button in ORDER_INPUTS)
    return prefix, [10350, 10750, *(frame + 149 for frame, _ in ORDER_INPUTS)], 12800, history, donor


def run(case):
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert not (ROOT / case).exists()
    scope = vars(voyage.playback) | dict(ROOT=ROOT, parent=current, observer=voyage.scoped_observer,
        get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(getsource(voyage.playback.main), __file__ + "::ordinary-shared-encounters", "exec"), scope)
    scope["main"](case)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("case", choices=(*VOYAGES, *TAVERNS))
    run(cli.parse_args().case)
