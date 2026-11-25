"""Trace Maria canceling and confirming Quit Game on the registered candidate."""

from pathlib import Path
from types import FunctionType

from scripts import observe_nagasaki_voyage_20261124 as voyage


ROOT = voyage.ROOT.with_name("maria_system_quit_20261124")
CONTROLLER = ROOT / "controller.jsonl"
RELEASE = Path("releases/all_routes_editorial_20261124_maria_captured_ship_candidate/verification/registered_release_verification.json")


if __name__ == "__main__":
    prior = voyage.prior
    bindings = vars(prior) | dict(ROOT=ROOT, CONTROLLER=CONTROLLER, RELEASE=RELEASE,
        HISTORY=voyage.HISTORY, FIRST_PAUSE=3200, __file__=__file__)
    FunctionType(prior.main.__code__, bindings)()
