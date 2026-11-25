"""Replay the current Seoul tavern and sample the ordinary decline branch."""

import sys
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts.observe_baltic_seoul_town_20261123 import ROOT as PREVIOUS
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest, read


ROOT = PREVIOUS.with_name("seoul_tavern_decline_20261123")
RELEASE = Path("releases/all_routes_editorial_20261123_seoul_shop_rumor_candidate/verification/registered_release_verification.json")
HISTORY = PREVIOUS / "seoul/capture/capture_report.json"
FIRST_PAUSE = 15130


def main():
    release, history = map(read, (RELEASE, HISTORY))
    assert release["predecessor"]["candidate_sha256"] == history["ROM_sha256"]
    assert history["frames"] == FIRST_PAUSE
    parent_terminal = read(HISTORY.parent.parent / "terminal.json")
    assert parent_terminal["ordinary_controller_inputs"]
    assert parent_terminal["evidence"][str(HISTORY)] == digest(HISTORY)
    assert not ROOT.exists()
    ROOT.mkdir(parents=True)
    plan = ROOT / "controller.jsonl"
    plan.touch(exist_ok=False)
    current = SimpleNamespace(RELEASE=RELEASE, ROM=Path(release["candidate"]))
    source = checked_text(getsource(replay.main), {
        '"--pause-at", str(FIRST_PAUSE), "--dump-pause-ram"':
            '"--pause-at", str(FIRST_PAUSE), "--dump-pause-ram", "--capture-at", "9230", "9530", "14330"',
        'Path(__file__))': 'Path(__file__), CONTROLLER)',
    })
    scope = vars(replay) | dict(ROOT=ROOT, current=current, HISTORY=HISTORY, FIRST_PAUSE=FIRST_PAUSE,
                               CONTROLLER=plan, __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-Seoul-No", "exec"), scope)
    stream, original = GrowingCommands(plan), sys.stdin
    try:
        sys.stdin = stream
        scope["main"]()
    finally:
        sys.stdin = original
        stream.close()


if __name__ == "__main__":
    main()
