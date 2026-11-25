"""Follow ordinary Riga trade controls on the registered Cargo Setup candidate."""

from types import FunctionType

from scripts import observe_riga_town_services_20261124 as earlier
from scripts import register_cargo_storage_warning_20261124 as current

ROOT = current.ROM.parent.with_name("editorial_20261124_riga_trade")
CONTROLLER = ROOT / "controller.jsonl"
OPENING = (dict(until=3600, duration=8, touch=[128, 27]),)


if __name__ == "__main__":
    scope = vars(earlier) | dict(ROOT=ROOT, CONTROLLER=CONTROLLER, current=current, OPENING=OPENING, __file__=__file__)
    FunctionType(earlier.main.__code__, scope)()
