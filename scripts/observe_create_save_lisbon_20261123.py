"""Use the verified Lisbon donor to check cancelling and writing a new slot."""

from pathlib import Path
from types import FunctionType

from scripts import observe_create_save_current_20261123 as controls


ROOT = controls.ROOT.with_name("create_save_lisbon")
REFERENCE = Path("work/retail_exit_scope_20261119/quit/capture/capture_report.json")
FRAMES = (4800, 5200, 5600, 6000, 6400, 6800, *range(6804, 6853, 4), 6872, 6910, 7200, 7700)


def schedule(case):
    assert case == "create"
    history = controls.base.load(REFERENCE)
    donor = history["battery_save_preloaded"]
    assert history["cold_boot"] and not history["savestate_loaded"] and not history["callback_errors"]
    assert not any(value for key, value in history.items() if key.startswith("synthetic_"))
    assert controls.base.digest(donor["source"]) == donor["source_sha256"]
    backup = Path(donor["source"]).read_bytes()
    assert backup[:4] == b"DK4R" and backup[0xA000:0x14000] == bytes([255]) * 0xA000
    events = [row for row in history["scripted_input_schedule"] if row["start"] <= 4401]
    events.extend(dict(start=frame, duration=8, buttons=[key]) for frame, key in (
        (4801, "A"), (5201, "DOWN"), (5601, "A"), (6001, "B"), (6401, "A"), (6801, "A")))
    return events, list(FRAMES), 7800, REFERENCE, donor


def main():
    namespace = vars(controls) | dict(ROOT=ROOT, schedule=schedule, __file__=__file__)
    FunctionType(controls.main.__code__, namespace)()


if __name__ == "__main__":
    main()
