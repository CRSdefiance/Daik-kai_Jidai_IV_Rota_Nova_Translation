"""Follow the Nagasaki departure on the registered candidate with ordinary inputs."""

from pathlib import Path
from types import FunctionType

from scripts import observe_syracuse_services_20261124 as prior


ROOT = prior.ROOT.with_name("nagasaki_voyage_20261124")
HISTORY = Path("work/emulation_v193/osaka_v519/capture_report.json")
CONTROLLER = ROOT / "controller.jsonl"
FIRST_PAUSE = 3200


if __name__ == "__main__":
    scope = vars(prior) | dict(ROOT=ROOT, HISTORY=HISTORY, CONTROLLER=CONTROLLER,
                              FIRST_PAUSE=FIRST_PAUSE, __file__=__file__)
    FunctionType(prior.main.__code__, scope)()
