"""Replay original character setup and Options on the registered testing ROM."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from scripts import observe_early_setup_current_20261122 as early
from scripts import observe_options_paths_20261123 as options
from scripts import register_online_card_copy_20261123 as current


base = current.base
ROOT = Path(".codex-release-work/shared_display_20261123/legacy_and_scene_paths")


def schedule(case):
    return (early.setup.schedule if case == "setup" else options.schedule)(case)


def run(case):
    release = base.load(current.RELEASE)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(current.ROM) == release["candidate_sha256"]
    source = getsource(early.playback.main)
    if case == "setup":
        source = early.checked_text(source, {
            "    installed = []": "    argv += ['--touchscreen']\n    installed = []",
        })
    env = vars(early.playback) | dict(ROOT=ROOT, parent=current, observer=early.trace.scoped_observer,
        get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(source, __file__ + "::installed-controller-replay", "exec"), env)
    env["main"](case)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("case", choices=("setup", "options"))
    run(cli.parse_args().case)
