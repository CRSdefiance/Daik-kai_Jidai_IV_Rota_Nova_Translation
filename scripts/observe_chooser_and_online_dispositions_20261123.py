"""Replay the original chooser, Online guide, and About Extras menus."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import observe_extras_tie_in_common_20261114 as extras
from scripts import observe_online_gallery_common_v1 as replay
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_ending_credit_spacing_20261123 as current
from scripts.run_all_captain_chooser_v691 import STATES


base = current.base
ROOT = Path(".codex-release-work/shared_display_20261123/chooser_and_online_dispositions")
CHOOSER = Path("out/captain_biographies_20261111_v2/candidate/capture/capture_report.json")


def schedule(case):
    if case == "online":
        return replay.get_schedule(case)
    if case == "tie_in_advance":
        return extras.schedule(case)
    assert case == "chooser"
    prior = base.load(CHOOSER)
    assert prior["cold_boot"] and not prior["savestate_loaded"] and not prior["callback_errors"]
    fixture, = prior["synthetic_gallery_fixtures"]
    manifest = Path(fixture["preloaded_save_manifest"])
    assert base.digest(manifest) == fixture["manifest_sha256"]
    donor = prior["battery_save_preloaded"]
    assert base.load(manifest)["fixture_save_sha256"] == donor["source_sha256"] == base.digest(donor["source"])
    assert donor["copied_byte_exact_before_cold_boot"]
    assert not any(value for key, value in prior.items()
                   if key.startswith("synthetic_") and key != "synthetic_gallery_fixtures")
    return prior["scripted_input_schedule"], [2200, *(f for f, _ in STATES), 5500], 5550, CHOOSER, donor


def observe(case):
    release = base.load(current.RELEASE)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(current.ROM) == release["candidate_sha256"]
    env = vars(replay) | dict(ROOT=ROOT, parent=current, FOCUS=set(range(3668)), get_schedule=schedule,
        observer=replay.observer if case == "online" else trace.scoped_observer, __file__=__file__)
    FunctionType(replay.main.__code__, env)(case)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("case", choices=("chooser", "online", "tie_in_advance"))
    observe(cli.parse_args().case)
