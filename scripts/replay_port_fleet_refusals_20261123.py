"""Replay the original Port Fleet selection and Gerhard's refusal from Syracuse."""

from argparse import ArgumentParser
from io import StringIO
import json
from pathlib import Path
import sys
from types import FunctionType

from scripts import headless_desmume_v193 as harness
from scripts import native_finance_fixture_v615 as fixture
from scripts import register_market_introduction_wrap_20261123 as current


base = current.base
ROOT = Path(".codex-release-work/port_fleet_wrap_20261123")
HISTORY = Path("E:/Rota Nova translations/Generated/work/emulation_v193/regional_fleet_v615_admiral/capture_report.json")
SAVED_GAME_SHA = "958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb"
FRAMES = (11400, 15000, 15400, 15800, 16200, 16600, 17000, 17400)


def replay(which):
    release = base.load(current.RELEASE)
    rom, sha = current.ROM, release["candidate_sha256"]
    if which == "revised":
        from scripts import stage_port_fleet_wrap_20261123 as stage

        stored = base.load(stage.PROOF)
        assert stored["predecessor_sha256"] == sha
        rom, sha = stage.ROM, stored["candidate_sha256"]
    assert base.digest(rom) == sha
    native_arm = current.native.digest(base.NdsImage.open(rom).read_file(current.ARM))
    assert native_arm == release["target_ARM9_sha256"]

    historical = base.load(HISTORY)
    donor = historical["battery_save_preloaded"]
    assert historical["cold_boot"] and not historical["savestate_loaded"] and not historical["callback_errors"]
    assert historical["frames"] == FRAMES[-1]
    assert base.digest(donor["source"]) == donor["source_sha256"] == SAVED_GAME_SHA
    root = ROOT / which
    root.mkdir(parents=True)
    inputs = root / "inputs.json"
    base.save(inputs, historical["scripted_input_schedule"])
    end = FRAMES[-1]
    argv = [__file__, "--rom", str(rom), "--out", str(root / "capture"), "--frames", str(end),
        "--inputs-json", str(inputs), "--battery-save", donor["source"], "--touchscreen",
        "--pause-at", "3400", "--allow-finance-fixtures", "--allow-crew-ability-fixtures",
        "--capture-every", "999999", "--capture-at", *map(str, FRAMES)]
    prerequisites = ({"company_funds": 1000000, "until": 11400},
                     {"regional_admiral_command": 150, "until": end}, {"stop": True})
    scope = vars(fixture) | {"ARM": native_arm}
    fund, enable = fixture.fund_company, fixture.enable_admiral
    fixture.fund_company = FunctionType(fund.__code__, scope)
    fixture.enable_admiral = FunctionType(enable.__code__, scope)
    fixture.enable_admiral.__kwdefaults__ = enable.__kwdefaults__
    original_argv, original_stdin = sys.argv, sys.stdin
    try:
        sys.argv = argv
        sys.stdin = StringIO("".join(json.dumps(obj) + "\n" for obj in prerequisites))
        harness.main()
    finally:
        sys.argv, sys.stdin = original_argv, original_stdin
        fixture.fund_company, fixture.enable_admiral = fund, enable
    path = root / "capture/capture_report.json"
    report = base.load(path)
    assert report["frames"] == end and report["ROM_sha256"] == sha
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert base.digest(donor["source"]) == report["battery_save_preloaded"]["source_sha256"] == SAVED_GAME_SHA
    cash, = report["synthetic_finance_fixtures"]
    skill, = report["synthetic_crew_ability_fixtures"]
    assert cash["only_one_company_funds_word_changed"] and cash["fixture_funds"] == 1000000 and cash["frame"] == 3400
    assert skill["only_one_Gerhard_attribute_byte_changed"] and skill["fixture_Command"] == 150 and skill["frame"] == 11400
    assert len(cash["changes"]) == 3 and len(skill["changes"]) == 1
    base.save(root / "terminal.json", dict(rom_sha256=sha, history_sha256=base.digest(HISTORY),
        donor_sha256=SAVED_GAME_SHA, report=str(path), report_sha256=base.digest(path),
        inputs_sha256=base.digest(inputs), focused_fixture=True, earned_regional_fleet=False))
    print(f"{which}: cold boot with the original Fleet selection and declared prerequisites.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("side", choices=("current", "revised"))
    replay(parser.parse_args().side)
