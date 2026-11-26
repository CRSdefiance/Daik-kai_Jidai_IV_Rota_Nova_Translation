"""Replay the Tunis Tavern opening and visit Recruit Crew through ordinary input."""

from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import observe_tunis_tavern_20261125 as tavern
from scripts import register_amsterdam_guild_crystal_20261125 as current


ROOT = Path(".codex-release-work/shared_display_20261123/tunis_recruitment_20261125").resolve()
CONTROLLER = ROOT / "controller.jsonl"


if __name__ == "__main__":
    scope = vars(tavern) | dict(ROOT=ROOT, CONTROLLER=CONTROLLER,
        current=SimpleNamespace(RELEASE=current.RELEASE, ROM=current.ROM), __file__=__file__)
    FunctionType(tavern.main.__code__, scope)()
