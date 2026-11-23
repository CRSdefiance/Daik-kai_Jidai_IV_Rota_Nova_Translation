"""Prepare exact patch and startup evidence for registering the Supply Ratio answer."""

import sys
from argparse import ArgumentParser
from pathlib import Path

from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts.reconcile_editorial_acceptance_20261123 import digest, read
from scripts.stage_supply_ratio_hint_20261123 import RELEASE


ROOT = Path(".codex-release-work/supply_ratio_mix_probe_20261123")
PROOF, PATCH, REBUILT = ROOT / "stored_proof.json", ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"


def patch(proof):
    clean, rom = Path("work/clean.nds"), Path(proof["candidate"])
    assert digest(clean) == proof["clean_input_sha256"] and digest(rom) == proof["candidate_sha256"]
    assert not REBUILT.exists()
    if not PATCH.exists():
        make_xdelta(clean, rom, PATCH)
    apply_xdelta(clean, PATCH, REBUILT)
    assert digest(REBUILT) == proof["candidate_sha256"] and REBUILT.read_bytes() == rom.read_bytes()
    print(f"Exact clean-input patch {digest(PATCH)}")


def startup(proof):
    from scripts import headless_desmume_v193 as harness
    from scripts.check_captain_name_release_20261119 import START_FRAMES

    previous = read(RELEASE)
    previous_startup = Path(previous["own_registered_startup"])
    assert digest(previous_startup) == previous["own_registered_startup_sha256"]
    capture = Path(read(previous_startup)["exact_matching_frames"][0]["path"]).parent / "capture_report.json"
    prior = read(capture)
    donor = prior["battery_save_preloaded"]
    assert proof["predecessor_sha256"] == previous["candidate_sha256"] == prior["ROM_sha256"]
    assert prior["cold_boot"] and not prior["savestate_loaded"] and prior["frames"] == START_FRAMES[-1]
    assert prior["scripted_start_frame"] == -1 and digest(donor["source"]) == donor["source_sha256"]
    rom = Path(proof["candidate"])
    assert digest(rom) == proof["candidate_sha256"]
    directory = STARTUP_CAPTURE.parent.parent
    directory.mkdir()
    inputs = directory / "inputs.json"
    import json
    inputs.write_text(json.dumps(prior["scripted_input_schedule"]), encoding="utf-8")
    argv = sys.argv
    try:
        sys.argv = ["headless_desmume_v193.py", "--rom", str(rom), "--out", str(STARTUP_CAPTURE.parent),
                    "--frames", str(START_FRAMES[-1]), "--inputs-json", str(inputs), "--press-start", "-1",
                    "--touchscreen", "--battery-save", donor["source"], "--capture-every", "999999", "--dump-ram",
                    "--capture-at", *map(str, START_FRAMES)]
        harness.main()
    finally:
        sys.argv = argv
    assert read(STARTUP_CAPTURE)["ROM_sha256"] == proof["candidate_sha256"]
    assert digest(donor["source"]) == donor["source_sha256"]


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("patch", "startup"))
    globals()[parser.parse_args().action](read(PROOF))
