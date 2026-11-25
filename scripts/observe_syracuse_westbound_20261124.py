"""Follow the original Syracuse departure on the registered Tavern candidate."""

from pathlib import Path
from types import FunctionType

from scripts import observe_syracuse_services_20261124 as template
from scripts.register_tavern_sighting_rumor_20261124 import RELEASE


ROOT = template.ROOT.with_name("syracuse_westbound_20261124")
HISTORY = Path("work/emulation_v193/village_ui_v609_compact_probe/capture_report.json")


if __name__ == "__main__":
    scope = vars(template) | dict(ROOT=ROOT, HISTORY=HISTORY, FIRST_PAUSE=5200,
        CONTROLLER=ROOT / "controller.jsonl", RELEASE=RELEASE, __file__=__file__)
    FunctionType(template.main.__code__, scope)()
