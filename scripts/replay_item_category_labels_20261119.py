"""Observe the revised category during focused Gallery and startup replays."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType
import sys

from scripts import headless_desmume_v193 as harness
from scripts import replay_tavern_strategist_followup_20261119 as prior
from scripts import stage_item_category_labels_20261119 as build
from scripts.verify_all_items_gallery_v535 import CAPTURE, OUT

base = build.base
GALLERY = build.ROOT / "gallery"
STARTUP = build.ROOT / "startup_fixture"


def gallery():
    assert not GALLERY.exists()
    old_capture = CAPTURE / "capture_report.json"
    old_manifest = OUT / "fixture/save_fixture_manifest.json"
    report, unlock, prepared = map(base.load, (old_capture, old_manifest, build.PROOF))
    fixture = Path(unlock["fixture_save"])
    assert report["ROM_sha256"] == unlock["production_ROM_sha256"]
    assert report["synthetic_gallery_fixtures"][0]["manifest_sha256"] == base.digest(old_manifest)
    assert base.digest(fixture) == unlock["fixture_save_sha256"] == report["battery_save_preloaded"]["source_sha256"]
    assert base.digest(unlock["original_donor"]) == unlock["original_donor_sha256"]
    assert unlock["synthetic_collection_history"] and not unlock["earned_unlock_verified"]
    assert prepared["candidate_sha256"] == base.digest(build.ROM)
    inputs = [r for r in report["scripted_input_schedule"] if r["start"] < 2900]
    inputs.append(dict(start=3101, duration=8, buttons=["B"]))
    GALLERY.mkdir()
    manifest, schedule = GALLERY / "save_fixture_manifest.json", GALLERY / "inputs.json"
    base.save(manifest, unlock | dict(production_ROM=str(build.ROM), production_ROM_sha256=base.digest(build.ROM),
              previous_manifest=str(old_manifest), previous_manifest_sha256=base.digest(old_manifest)))
    base.save(schedule, inputs)
    argv = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(build.ROM), "--out", str(GALLERY / "capture"),
                    "--battery-save", str(fixture), "--allow-gallery-fixtures", "--gallery-save-fixture-manifest",
                    str(manifest), "--touchscreen", "--inputs-json", str(schedule), "--frames", "3400",
                    "--capture-every", "999999", "--capture-at", "2600", "2800", "3000", "3350"]
        harness.main()
    finally:
        sys.argv = argv
    path = GALLERY / "capture/capture_report.json"
    current = base.load(path)
    assert current["ROM_sha256"] == prepared["candidate_sha256"] and current["frames"] == 3400
    assert current["cold_boot"] and not current["savestate_loaded"] and not current["callback_errors"]
    assert current["scripted_input_schedule"] == inputs and base.digest(fixture) == unlock["fixture_save_sha256"]
    base.save(GALLERY / "terminal.json", dict(report=str(path), report_sha256=base.digest(path),
              original_input_report_sha256=base.digest(old_capture), fixture_sha256=base.digest(fixture)))


def startup():
    FunctionType(prior.startup.__code__, vars(prior) | {"build": build, "STARTUP": STARTUP})()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("gallery", "startup"))
    globals()[parser.parse_args().action]()
