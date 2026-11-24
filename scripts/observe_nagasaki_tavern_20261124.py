"""Follow the Nagasaki Tavern from the current Nagasaki town hold."""

import json
import sys
from inspect import getsource
from pathlib import Path

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_nagasaki_contract_wrap_20261124 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import read, reference


ROOT = Path(".codex-release-work/shared_display_20261123/nagasaki_tavern_20261124")
HISTORY = current.build.REPLAY
FIRST_PAUSE = 3720
CONTROLLER = ROOT / "controller.jsonl"
OPENING = dict(until=4120, touch=[75, 27], duration=8)


def main():
    paired, previous, release = map(read, (current.build.PAIRED, HISTORY, current.RELEASE))
    assert paired["after"] == reference(HISTORY) and FIRST_PAUSE in paired["unchanged_frames"]
    assert paired["candidate_sha256"] == previous["ROM_sha256"] == release["candidate_sha256"]
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER, PAIRED)',
    })
    ROOT.mkdir(parents=True)
    CONTROLLER.write_text(json.dumps(OPENING) + "\n", encoding="utf-8")
    scope = vars(replay) | dict(ROOT=ROOT, HISTORY=HISTORY, FIRST_PAUSE=FIRST_PAUSE, current=current,
        CONTROLLER=CONTROLLER, PAIRED=current.build.PAIRED, __file__=__file__)
    exec(compile(source, __file__ + "::Nagasaki-Tavern", "exec"), scope)
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
