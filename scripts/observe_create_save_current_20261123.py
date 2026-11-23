"""Use original controls to cancel and then create a save in an unused slot."""

from pathlib import Path
from types import FunctionType

from scripts import observe_opening_label_dispositions_20261123 as prior
from scripts import register_online_card_copy_20261123 as current


ROOT = prior.ROOT.parent / "create_save_current"
REFERENCE = Path("work/emulation_v193/save_load_plaques_v612_current/capture_report.json")
base, TRACE = current.base, prior.trace


def schedule(case):
    assert case == "create"
    history = base.load(REFERENCE)
    donor = history["battery_save_preloaded"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    assert history["cold_boot"] and not history["savestate_loaded"] and not history["callback_errors"]
    assert not any(value for key, value in history.items() if key.startswith("synthetic_"))
    events = [row for row in history["scripted_input_schedule"] if row["start"] <= 5401]
    events.extend(dict(start=frame, duration=8, buttons=[key]) for frame, key in (
        (5801, "DOWN"), (6201, "A"), (6601, "B"), (7001, "A"), (7401, "A")))
    return events, [5800, 6200, 6600, 7000, 7400, 7410, 7480, 7560, 7800, 8200], 8250, REFERENCE, donor


def main():
    release = base.load(current.RELEASE)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    scope = vars(prior.driver) | dict(ROOT=ROOT, parent=current, FOCUS=set(range(3668)),
        get_schedule=schedule, observer=TRACE.scoped_observer, __file__=__file__)
    FunctionType(prior.driver.main.__code__, scope)("create")


if __name__ == "__main__":
    main()
