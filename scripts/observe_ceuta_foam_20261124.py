"""Repeat the original Ceuta voyage on the current candidate using only game controls."""

import sys
from inspect import getsource
from pathlib import Path

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_athens_item_rumor_20261124 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest, read


ROOT = Path(".codex-release-work/shared_display_20261123/ceuta_foam_20261124")
HISTORY = Path("work/emulation_v193/sea_foam_family_v514_final_actual/capture_report.json")
PROOF = Path("work/analysis/sea_foam_family_v514/release_proof.json")
CONTROLLER = ROOT / "controller.jsonl"
FIRST_PAUSE = 9476
HOLDS = (4000, 6000, 8000, 8476, 8676, 8876, 9076, 9276)


def main():
    prior = read(PROOF)
    assert digest(HISTORY) == prior["actual_capture_report_sha256"]
    assert prior["no_saved_completion_flags_or_movement_injection_in_sea_replay"]
    assert set(HOLDS) <= {row["frame"] for row in read(HISTORY)["frames_captured"]}
    ROOT.mkdir(parents=True)
    CONTROLLER.touch(exist_ok=False)
    source = checked_text(getsource(replay.main), {
        ', "--dump-pause-ram"]': ', "--capture-at", *map(str, HOLDS)]',
        'Path(__file__))': 'Path(__file__), CONTROLLER, PROOF)',
    })
    scope = vars(replay) | dict(ROOT=ROOT, HISTORY=HISTORY, FIRST_PAUSE=FIRST_PAUSE, HOLDS=HOLDS,
        current=current, CONTROLLER=CONTROLLER, PROOF=PROOF, __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-ceuta-random-encounter", "exec"), scope)
    previous = sys.stdin
    stream = GrowingCommands(CONTROLLER)
    try:
        sys.stdin = stream
        scope["main"]()
    finally:
        sys.stdin = previous
        stream.close()


if __name__ == "__main__":
    main()
