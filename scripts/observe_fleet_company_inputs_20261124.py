"""Observe the original actor affiliation byte during ordinary save restores."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import observe_fleet_battery_fields_20261124 as restore
from scripts import stage_tunis_shop_advice_20261124 as current
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import REGISTRY, digest, read


RELEASE = Path("releases/all_routes_editorial_20261124_tunis_shop_advice_candidate/verification/registered_release_verification.json")
ROOT = restore.ROOT.with_name("fleet_company_loads_20261124")
AFFILIATION_READ = 0x0207EBC4
CALLS = {AFFILIATION_READ + offset: ("affiliation", 8, 5, bool(offset)) for offset in (0, 4)}


def schedule(case):
    if case == "nagasaki":
        return restore.schedule(case)
    assert case == "tunis"
    previous = current.BEFORE
    history = read(previous)
    assert history["cold_boot"] and not history["savestate_loaded"] and not history["callback_errors"]
    assert not any(v for k, v in history.items() if k.startswith("synthetic_"))
    donor = history["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    hold = 4200
    return [row for row in history["scripted_input_schedule"] if row["start"] < hold], (hold,), hold + 1, previous, donor


def main(case):
    release = read(RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(current.ROM) == release["candidate_sha256"]
    assert not (ROOT / case).exists()
    source = checked_text(getsource(restore.playback.main), {
        "'--capture-at', *map(str, frames)]": "'--dump-capture-ram', '--capture-at', *map(str, frames)]",
        "prepared_gallery_save=bool(donor)": "ordinary_cartridge_save=bool(donor)",
    })
    observer = FunctionType(restore.observe.__code__, vars(restore) | {"CALLS": CALLS, "__file__": __file__})
    scope = vars(restore.playback) | dict(ROOT=ROOT, parent=SimpleNamespace(RELEASE=RELEASE, ROM=current.ROM),
        get_schedule=schedule, observer=observer, FOCUS=set(), __file__=__file__)
    exec(compile(source, __file__ + "::affiliation-save-load", "exec"), scope)
    scope["main"](case)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("tunis", "nagasaki"))
    main(parser.parse_args().case)
