"""Observe the complete title cycle on the current registered ROM."""

from pathlib import Path
from types import FunctionType

from scripts import observe_opening_label_dispositions_20261123 as prior
from scripts import register_online_card_copy_20261123 as current


ROOT = prior.ROOT.parent / "title_variant_display"
TRACE = prior.trace
FRAMES = [579, 707, 807, 825, 987, 1005, 1039, 5835, 5947, 5991, 6099, 6167,
          6179, 6191, 6231, 6435, 6667, 6779, 6939, 7107, 7199, 7211]


def schedule(case):
    assert case == "title"
    return [], FRAMES, 7400, prior.COMPOSITION, None


def main():
    release = current.base.load(current.RELEASE)
    assert current.base.digest(current.base.REGISTRY) == release["registry_sha256"]
    scope = vars(prior.driver) | dict(ROOT=ROOT, parent=current, FOCUS=set(range(3668)),
        get_schedule=schedule, observer=TRACE.scoped_observer, __file__=__file__)
    FunctionType(prior.driver.main.__code__, scope)("title")


if __name__ == "__main__":
    main()
