"""Follow ordinary Nagasaki town choices from the registered Yard candidate."""

import sys
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_yard_numerals_20261124 as active
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import read, reference


ROOT = Path(".codex-release-work/shared_display_20261123/nagasaki_town_services_20261124")
CONTROLLER = ROOT / "controller.jsonl"
HISTORY = active.build.REPLAY
FIRST_PAUSE = 3720


def main():
    release, paired, history = map(read, (active.RELEASE, active.build.PAIRED, HISTORY))
    assert paired["after"] == reference(HISTORY) and FIRST_PAUSE in paired["unchanged_frames"]
    assert paired["ordinary_saved_game"] and not paired["research_fixtures"]
    assert paired["candidate_sha256"] == history["ROM_sha256"] == release["candidate_sha256"]
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER, PAIRED)',
    })
    scope = vars(replay) | dict(ROOT=ROOT, HISTORY=HISTORY, FIRST_PAUSE=FIRST_PAUSE,
        current=SimpleNamespace(RELEASE=active.RELEASE, ROM=active.ROM),
        CONTROLLER=CONTROLLER, PAIRED=active.build.PAIRED, __file__=__file__)
    exec(compile(source, __file__ + "::Nagasaki-town-services", "exec"), scope)
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
