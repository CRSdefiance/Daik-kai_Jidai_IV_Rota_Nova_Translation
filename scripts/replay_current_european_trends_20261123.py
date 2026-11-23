"""Replay the already-earned Athens and London trend triggers on the current build."""

import argparse
import sys
from pathlib import Path

from scripts import headless_desmume_v193 as harness
from scripts.observe_seoul_tavern_decline_20261123 import RELEASE
from scripts.reconcile_town_trend_catalogue_20261123 import BOOK, verification
from scripts.stage_cartridge_title_20261123 import REGISTRY, digest, read, write


ROOT = Path("E:/Rota Nova translations/Generated/work/current_european_trends_20261123")
PAIRED = verification("20261121_athens_london_trends") / "verified_trends.json"
ORDINARY = BOOK / "european_trend_gameplay_20261121_v1.json"
CASES = ("london", "athens")


def details(city):
    sealed = read(PAIRED)
    historic, = [Path(p) for p in sealed["evidence"] if city in Path(p).parts and p.endswith("capture_report.json")]
    assert digest(historic) == sealed["evidence"][str(historic)]
    previous = read(historic)
    assert previous["cold_boot"] and not previous["savestate_loaded"] and not previous["callback_errors"]
    assert previous["ROM_sha256"] == sealed["candidate_sha256"]
    assert not any(v for k, v in previous.items() if k.startswith("synthetic_"))
    case, = [row for row in read(ORDINARY)["scene_runs"] if row["city"] == city]
    controls = {k: row["frame"] for k, row in case["calendar_controls"].items()}
    holds = {row["snapshot"]["frame"]: row["id"] for row in sealed["holds"] if row["city"] == city}
    donor = previous["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    return historic, previous, controls, holds, donor


def replay(city):
    release = read(RELEASE)
    assert digest(release["candidate"]) == release["candidate_sha256"]
    assert digest(REGISTRY) == release["registry_sha256"]
    historic, previous, controls, holds, donor = details(city)
    directory = ROOT / city
    directory.mkdir(parents=True)
    plan = directory / "identical_inputs.json"
    write(plan, previous["scripted_input_schedule"])
    frames = sorted(set(controls.values()) | holds.keys())
    previous_args = sys.argv
    try:
        sys.argv = [harness.__file__, "--rom", release["candidate"], "--out", str(directory / "capture"),
            "--frames", str(previous["frames"]), "--inputs-json", str(plan), "--press-start", "-1",
            "--capture-every", "999999", "--capture-at", *map(str, frames),
            "--battery-save", donor["source"], "--touchscreen", "--dump-ram"]
        harness.main()
    finally:
        sys.argv = previous_args
    assert digest(donor["source"]) == donor["source_sha256"]


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("city", choices=CASES)
    replay(cli.parse_args().city)
