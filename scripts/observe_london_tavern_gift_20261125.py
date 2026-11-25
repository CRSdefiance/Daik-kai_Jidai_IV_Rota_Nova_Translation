"""Check ordinary London Tavern gift and conversation options on the registered ROM."""

from pathlib import Path
from types import FunctionType

from scripts import observe_london_tavern_20261123 as prior
from scripts import register_levelup_numerals_20261125 as current


ROOT = Path(".codex-release-work/shared_display_20261123/london_tavern_gift_20261125")
CONTROLLER = ROOT / "controller.jsonl"


if __name__ == "__main__":
    scope = vars(prior) | dict(ROOT=ROOT, CONTROLLER=CONTROLLER, current=current, __file__=__file__)
    FunctionType(prior.main.__code__, scope)()
