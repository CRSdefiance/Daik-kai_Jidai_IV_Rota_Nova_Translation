"""Replay controls and both setting confirmations on the registered build."""

from inspect import getsource
from pathlib import Path

from scripts import observe_options_legacy_common_20261114 as prior
from scripts import register_square_and_market_reward_wraps_20261123 as current


ROOT = Path(".codex-release-work/shared_display_20261123/current_options")
KEYS = (
    *prior.KEYS[:13],
    (6801, "A"), (7201, "B"), (7601, "A"), (8001, "A"),
    (8401, "A"), (8801, "A"), (9201, "DOWN"), (9601, "A"),
    (10001, "B"), (10401, "A"), (10801, "A"), (11201, "A"),
    (11601, "A"), (12001, "B"),
)


def schedule(case):
    assert case == "options"
    events = [dict(start=frame, duration=8, buttons=[key]) for frame, key in KEYS]
    return events, [frame + 199 for frame, _ in KEYS[2:]], 12300, None, None


def main():
    assert not (ROOT / "options").exists()
    release = current.base.load(current.RELEASE)
    assert current.base.digest(current.base.REGISTRY) == release["registry_sha256"]
    scope = vars(prior.playback) | dict(ROOT=ROOT, parent=current, FOCUS=prior.FOCUS,
        observer=prior.trace.scoped_observer, get_schedule=schedule, __file__=__file__)
    exec(compile(getsource(prior.playback.main), __file__ + "::observe-registered-options", "exec"), scope)
    scope["main"]("options")


if __name__ == "__main__":
    main()
