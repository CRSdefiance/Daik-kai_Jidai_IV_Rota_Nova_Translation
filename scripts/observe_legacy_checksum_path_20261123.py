"""Trace the original checksum warning with the preserved disposable save."""

from types import FunctionType

from scripts import observe_damaged_save_20261115 as previous
from scripts import observe_legacy_setup_paths_20261123 as context
from scripts import replay_damaged_save_digits_20261120 as old


base, current = context.base, context.current
FIXTURE = old.HISTORY / "checksum_fixture.json"
INPUTS = old.HISTORY / "corrupt_slot/capture/capture_report.json"


def schedule(case):
    assert case == "corrupt_slot"
    fixture, original = map(base.load, (FIXTURE, INPUTS))
    good, bad = previous.Path(fixture["donor"]), previous.Path(fixture["disposable_copy"])
    assert (base.digest(good), base.digest(bad)) == (fixture["donor_sha256"], fixture["copy_sha256"])
    a, b = good.read_bytes(), bad.read_bytes()
    assert len(a) == len(b) and a[:4] == b[:4] and a[4] ^ b[4] == 1 and a[5:] == b[5:]
    assert original["cold_boot"] and not original["savestate_loaded"]
    return (original["scripted_input_schedule"], original["exact_requested_capture_frames"], original["frames"],
        INPUTS, dict(source=str(bad), source_sha256=fixture["copy_sha256"]))


def run():
    release = base.load(current.RELEASE)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(current.ROM) == release["candidate_sha256"]
    driver = previous.playback
    scope = vars(driver) | dict(ROOT=context.ROOT, parent=current, FOCUS=set(range(3668)),
        get_schedule=schedule, observer=previous.observer, __file__=__file__)
    FunctionType(driver.main.__code__, scope)("corrupt_slot")


if __name__ == "__main__":
    run()
