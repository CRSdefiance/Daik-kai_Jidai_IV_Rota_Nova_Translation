"""Sail to Ezo from the existing Nagasaki save using ordinary controls."""

import sys
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_ordinary_azores_voyage_20261123 as voyage
from scripts import register_nagasaki_dream_20261123 as active
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path(".codex-release-work/shared_display_20261123/ezo_voyage")
HISTORY = Path("work/emulation_v193/japan_facilities_v518_reload/capture_report.json")
CONTROLLER = ROOT / "controller.jsonl"
FIRST_PAUSE = 3200


def main():
    release = active.stage.read(active.RELEASE)
    provenance = active.stage.read(Path("work/analysis/japan_facilities_v517/saved_checkpoint.json"))
    donor = active.stage.read(HISTORY)["battery_save_preloaded"]
    assert Path(donor["source"]) == Path(provenance["save"])
    assert active.stage.digest(donor["source"]) == donor["source_sha256"] == provenance["sha256"]
    source = checked_text(getsource(voyage.main), {"Path(__file__))": "Path(__file__), CONTROLLER)"})
    ROOT.mkdir(parents=True)
    CONTROLLER.touch(exist_ok=False)
    current = SimpleNamespace(RELEASE=active.RELEASE, ROM=Path(release["candidate"]))
    scope = vars(voyage) | dict(ROOT=ROOT, HISTORY=HISTORY, CONTROLLER=CONTROLLER,
        FIRST_PAUSE=FIRST_PAUSE, current=current, __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-ezo-voyage", "exec"), scope)
    original = sys.stdin
    stream = GrowingCommands(CONTROLLER)
    try:
        sys.stdin = stream
        scope["main"]()
    finally:
        sys.stdin = original
        stream.close()


if __name__ == "__main__":
    main()
