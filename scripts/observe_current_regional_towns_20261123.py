"""Trace Square and Tavern dialogue during ordinary visits on the current ROM."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from scripts import observe_regional_town_dialogue_20261115 as regional
from scripts import register_hodram_b261_b310_wrap_fixes_20261123 as current
from scripts.source_locked_derivation_v5118 import checked_text


base = current.base
ROOT = Path(".codex-release-work/shared_display_20261123/current_regional_towns")


def run(city):
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert not (ROOT / city).exists()
    source = checked_text(getsource(regional.playback.main), {
        "    installed = []": "    argv.append('--touchscreen')\n    installed = []",
    })
    scope = vars(regional.playback) | dict(ROOT=ROOT, parent=current, observer=regional.scoped_observer,
        get_schedule=regional.schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-town-visits", "exec"), scope)
    scope["main"](city)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("city", choices=regional.HISTORY)
    run(cli.parse_args().city)
