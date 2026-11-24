"""Follow the ordinary Nagasaki contract cancellation and uncontracted Market branches."""

import json
import sys
from inspect import getsource
from pathlib import Path

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_nagasaki_contract_wrap_20261124 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import read, reference


ROOT = Path(".codex-release-work/shared_display_20261123/nagasaki_decline_20261124")
CONTROLLER = ROOT / "controller.jsonl"
HISTORY = current.build.REPLAY
FIRST_PAUSE = 8520
CHOICE = dict(until=8920, buttons=["B"], duration=8)


def main():
    earlier = read(current.build.PAIRED)
    release, history = map(read, (current.RELEASE, HISTORY))
    assert earlier["after"] == reference(HISTORY)
    assert earlier["candidate_sha256"] == history["ROM_sha256"] == release["candidate_sha256"]
    assert FIRST_PAUSE in earlier["unchanged_frames"] and earlier["ordinary_saved_game"]
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER, EARLIER)',
    })
    ROOT.mkdir(parents=True)
    # Further commands are appended after inspecting the ordinary transitions.
    CONTROLLER.write_text(json.dumps(CHOICE) + "\n", encoding="utf-8")
    scope = vars(replay) | dict(ROOT=ROOT, HISTORY=HISTORY, FIRST_PAUSE=FIRST_PAUSE,
        current=current, CONTROLLER=CONTROLLER, EARLIER=current.build.PAIRED, __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-nagasaki-cancellation", "exec"), scope)
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
