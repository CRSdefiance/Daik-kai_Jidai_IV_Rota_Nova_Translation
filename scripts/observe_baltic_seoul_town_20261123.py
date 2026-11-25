"""Trace ordinary Riga and Seoul visits from unmodified cartridge saves."""

import argparse
import json
import sys
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts.play_special_target_battle_20261123 import RELEASE
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest, read, write


ROOT = Path("E:/Rota Nova translations/Generated/work/baltic_seoul_town_20261123")
CASES = ("riga", "seoul")
HISTORY = Path("work/emulation_v193/auto_move_riga_v399/capture_report.json")
SEOUL_DONOR = Path("E:/Rota Nova translations/Saves/maria-seoul-rested-v514.dsv")
SEOUL_DIGEST = "942c74828a7b7396f7567ca2d405ddc4cdd329e4837f591777d35ee458794b0f"


def main(case, staged=False):
    release = read(RELEASE)
    folder = ROOT / ("seoul_staged" if staged else case)
    folder.mkdir(parents=True)
    controller = folder / "controller.jsonl"
    receipt = RELEASE
    if staged:
        assert case == "seoul"
        stage = read(ROOT / "stage/stored_proof.json")
        assert stage["predecessor"]["sha256"] == release["candidate_sha256"]
        assert stage["changed_ids"] == [726] and stage["exact_whole_parent_inverse"]
        assert digest(stage["candidate"]["path"]) == stage["candidate"]["sha256"]
        release.update(candidate=stage["candidate"]["path"], candidate_sha256=stage["candidate"]["sha256"])
        receipt = folder / "staged_inputs.json"
        write(receipt, release)
        original_commands = [json.loads(row) for row in (ROOT / case / "controller.jsonl").read_text("utf-8").splitlines()]
        prefix = [cmd for cmd in original_commands if cmd.get("until", 99999) <= 10650]
        assert prefix[-1]["until"] == 10650
        controller.write_text("".join(json.dumps(cmd) + "\n" for cmd in (*prefix, dict(stop=True))), encoding="utf-8")
    else:
        controller.touch(exist_ok=False)
    current = SimpleNamespace(RELEASE=receipt, ROM=Path(release["candidate"]))
    donor = read(HISTORY)["battery_save_preloaded"]
    if case == "seoul":
        assert digest(SEOUL_DONOR) == SEOUL_DIGEST
        donor = dict(source=str(SEOUL_DONOR), source_sha256=SEOUL_DIGEST)
    source = checked_text(getsource(replay.main), {
        'donor = history["battery_save_preloaded"]': 'donor = DONOR',
        'Path(__file__))': 'Path(__file__), CONTROLLER)',
    })
    scope = vars(replay) | dict(ROOT=folder, HISTORY=HISTORY, FIRST_PAUSE=3200, DONOR=donor,
                               CONTROLLER=controller, current=current, __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-town-controller", "exec"), scope)
    original = sys.stdin
    stream = GrowingCommands(controller)
    try:
        sys.stdin = stream
        scope["main"]()
    finally:
        sys.stdin = original
        stream.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=CASES)
    parser.add_argument("--staged", action="store_true")
    args = parser.parse_args()
    main(args.case, args.staged)
