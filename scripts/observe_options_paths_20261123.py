"""Replay controls and both setting confirmations on the registered build."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_options_legacy_common_20261114 as prior
from scripts import register_square_and_market_reward_wraps_20261123 as current
from scripts import stage_title_reports_label_20261123 as stage


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


def replay(revised):
    release = current.base.load(current.RELEASE)
    assert current.base.digest(current.base.REGISTRY) == release["registry_sha256"]
    root, target = ROOT, current
    if revised:
        root = stage.ROOT / "playing"
        proof = current.base.load(stage.PROOF)
        assert proof["predecessor_sha256"] == release["candidate_sha256"]
        target = SimpleNamespace(ROM=stage.ROM, RELEASE=stage.PROOF)
    assert not (root / "options").exists()
    scope = vars(prior.playback) | dict(ROOT=root, parent=target, FOCUS=prior.FOCUS,
        observer=prior.trace.scoped_observer, get_schedule=schedule, __file__=__file__)
    exec(compile(getsource(prior.playback.main), __file__ + "::observe-registered-options", "exec"), scope)
    scope["main"]("options")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("--revised", action="store_true")
    replay(cli.parse_args().revised)
