"""Observe Riga Shipyard interactions from the original town battery save."""

from types import FunctionType

from scripts import observe_riga_town_services_20261124 as earlier
from scripts import register_palace_investment_wording_20261124 as current

ROOT = current.ROM.parent.with_name("editorial_20261124_riga_shipyard")
CONTROLLER = ROOT / "controller.jsonl"
OPENING = (dict(until=3600, duration=8, touch=[180, 27]),
           dict(until=4000, duration=8, buttons=["A"]))


if __name__ == "__main__":
    scope = vars(earlier) | dict(ROOT=ROOT, CONTROLLER=CONTROLLER, current=current, OPENING=OPENING, __file__=__file__)
    FunctionType(earlier.main.__code__, scope)()