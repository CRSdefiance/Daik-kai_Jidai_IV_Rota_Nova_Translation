"""Observe the rotating images and complete guide cards on the registered ROM."""

from pathlib import Path
from types import FunctionType

from scripts import observe_chooser_and_online_dispositions_20261123 as prior


base, current, driver = prior.base, prior.current, prior.replay
ROOT = Path(".codex-release-work/shared_display_20261123/promotional_paths")
FIRST_HOLDS = (2290, 3290, 4290, 5290, 6790, 7790, 8790, 9790, 11290, 12290, 13790, 14790, 15790)
SLIDE_COUNTS = (2, 1, 2, 1, 1, 2, 2, 2, 2, 2, 1, 2, 3)


def schedule(case):
    assert case == "online"
    events, _, end, source, donor = prior.schedule(case)
    # Give the native 180-frame timer room for each additional image and its transition.
    frames = sorted({first + 185 * step for first, count in zip(FIRST_HOLDS, SLIDE_COUNTS, strict=True)
                     for step in range(count + int(count > 1))})
    assert donor is None and frames[-1] < 16601
    return events, frames, end, source, donor


def main():
    release = base.load(current.RELEASE)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(current.ROM) == release["candidate_sha256"]
    settings = vars(driver) | dict(ROOT=ROOT, parent=current, FOCUS=set(range(3668)), get_schedule=schedule,
        __file__=__file__)
    FunctionType(driver.main.__code__, settings)("online")


if __name__ == "__main__":
    main()
