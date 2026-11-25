"""Observe the active setup and sound settings on the registered testing ROM."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_options_legacy_common_20261114 as options
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_ship_room_names_20261122 as current
from scripts import replay_rafael_setup_labels_20261115 as setup
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path("work/analysis/early_setup_display_20261122")
FOCUS = {*range(100,108), *range(120,122), *range(330,334)}


def run(case):
    assert not (ROOT / case).exists()
    schedule = setup.schedule if case == "setup" else options.schedule
    source = getsource(playback.main)
    if case == "setup":
        source = checked_text(source, {
            "    installed = []":"    argv += ['--touchscreen']\n    installed = []",
        })
    scope = vars(playback) | dict(ROOT=ROOT, parent=current, observer=trace.scoped_observer,
        get_schedule=schedule, FOCUS=FOCUS, __file__=__file__)
    exec(compile(source,__file__+"::registered-DS-setup","exec"),scope)
    scope["main"](case)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case",choices=("setup","options"))
    run(parser.parse_args().case)

