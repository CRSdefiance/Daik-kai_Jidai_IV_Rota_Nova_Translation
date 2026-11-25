"""Follow the paid Price Info and confirmed investment branches from Nagasaki."""

import json
import sys
from inspect import getsource

from scripts import observe_nagasaki_contract_decline_20261124 as decline
from scripts import verify_nagasaki_contract_decline_20261124 as verified
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import read, reference


ROOT = decline.ROOT.with_name("nagasaki_market_commitments_20261124")
CONTROLLER = ROOT / "controller.jsonl"
HISTORY = decline.ROOT / "capture/capture_report.json"
FIRST_PAUSE = 12520
OPENING = dict(until=12920, buttons=["LEFT"], duration=8)


def main():
    earlier = read(verified.OUT)
    assert reference(HISTORY) in earlier["evidence"]
    assert earlier["observed_free_current_town_quote"]["capture"]["frame"] == FIRST_PAUSE
    assert earlier["candidate_sha256"] == read(decline.current.RELEASE)["candidate_sha256"]
    source = checked_text(getsource(decline.replay.main), {
        ', "--dump-pause-ram"]': ']',
        'Path(__file__))': 'Path(__file__), CONTROLLER, PRIOR)',
    })
    ROOT.mkdir(parents=True)
    CONTROLLER.write_text(json.dumps(OPENING) + "\n", encoding="utf-8")
    scope = vars(decline.replay) | dict(ROOT=ROOT, HISTORY=HISTORY, FIRST_PAUSE=FIRST_PAUSE,
        current=decline.current, CONTROLLER=CONTROLLER, PRIOR=verified.OUT, __file__=__file__)
    exec(compile(source, __file__ + "::market-confirmations", "exec"), scope)
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
