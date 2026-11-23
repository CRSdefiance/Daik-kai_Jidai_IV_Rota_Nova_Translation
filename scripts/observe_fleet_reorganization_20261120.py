"""Observe the stock Fleet Setup path after selecting Reorganize."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import observe_amsterdam_tavern_followup_20261120 as navigation
from scripts import observe_fleet_debt_disband_20261115 as earlier
from scripts import register_tavern_round_digits_20261120 as current
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path("work/fleet_reorganization_20261120")
PREFIX = earlier.ROOT / "fleet/capture/capture_report.json"
START = 9640


def main():
    source = checked_text(getsource(navigation.main), {
        '    previous = base.load(REPLAY / "capture_report.json")': '    previous = base.load(PREFIX)',
        '    assert previous["cold_boot"] and not previous["savestate_loaded"] and not previous.get("battery_save_preloaded")':
            '    assert previous["cold_boot"] and not previous["savestate_loaded"]\n'
            '    donor = previous["battery_save_preloaded"]\n'
            '    assert base.digest(donor["source"]) == donor["source_sha256"]',
        '    events = previous["scripted_input_schedule"]':
            '    events = [row for row in previous["scripted_input_schedule"] if row["start"] < START]',
        '"--capture-every", "999999", "--pause-at", str(START)]':
            '"--capture-every", "999999", "--pause-at", str(START), "--dump-pause-ram", "--battery-save", donor["source"]]',
        '    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture.get("battery_save_preloaded")':
            '    assert capture["cold_boot"] and not capture["savestate_loaded"]\n'
            '    save = capture["battery_save_preloaded"]\n'
            '    assert save["copied_byte_exact_before_cold_boot"] and base.digest(save["source"]) == donor["source_sha256"]',
        "shared requests after the Tavern return.": "shared requests after opening the Fleet Setup picker.",
    })
    env = vars(navigation) | globals()
    env["verified_schedule"] = FunctionType(navigation.verified_schedule.__code__, env)
    exec(compile(source, __file__ + "::fleet-navigation", "exec"), env)
    env["main"](ROOT, True)


if __name__ == "__main__":
    main()
