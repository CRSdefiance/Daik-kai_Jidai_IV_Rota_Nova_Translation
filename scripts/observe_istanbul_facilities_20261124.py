"""Observe Istanbul service and rumor branches on the registered Maria ROM."""

from pathlib import Path
from types import FunctionType

from scripts import observe_maria_system_quit_20261124 as active
from scripts import observe_syracuse_services_20261124 as template


ROOT = template.ROOT.with_name("istanbul_facilities_20261124")
HISTORY = Path("work/emulation_v193/istanbul_square_v482/capture_report.json")


if __name__ == "__main__":
    scope = vars(template) | dict(
        ROOT=ROOT, HISTORY=HISTORY, FIRST_PAUSE=3200,
        CONTROLLER=ROOT / "controller.jsonl", RELEASE=active.RELEASE, __file__=__file__,
    )
    FunctionType(template.main.__code__, scope)()
