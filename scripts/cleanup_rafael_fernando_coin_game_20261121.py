"""Clear redundant Fernando snapshots after the registered Drive update."""
from inspect import getsource
from pathlib import Path
import re

from scripts import cleanup_parallel_ship_lessons_20261121 as template
from scripts import register_rafael_fernando_coin_game_20261121 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
replay = release.live.replay


def preliminary_captures(retained):
    result = base.load(release.coin.PROOF)
    completed = base.load(replay.COIN_ROUND / "fixture.json")
    candidate = result["candidate_sha256"]
    assert candidate == base.digest(stage.ROM) == completed["candidate_sha256"] and result["round_completed"]
    retained[Path(completed["fixture"])] = completed["fixture_sha256"]
    for sheet in result["sheets"]:
        retained[Path(sheet["path"])] = sheet["sha256"]
    discard = {}
    for run, keep in ((replay.COIN, 5040), (replay.COIN_PLAY, 5355), (replay.COIN_TOUCH, 5180)):
        fixture = base.load(run / "fixture.json")
        capture_dir = run / "capture"
        report = base.load(capture_dir / "capture_report.json")
        assert fixture["candidate_sha256"] == candidate and report["ROM_sha256"] == fixture["fixture_sha256"]
        retained[Path(fixture["fixture"])] = fixture["fixture_sha256"]
        for item in report["frames_captured"]:
            path = Path(item["path"])
            assert path.resolve().parent == capture_dir.resolve()
            if re.fullmatch(r"frame_\d{6}_(?:cold_boot|final)\.png", path.name):
                selected = retained if item["frame"] == keep else discard
                selected[path] = item["PNG_sha256"]
    recovery = release.ROOT / "recovery_capture_cleanup.json"
    if recovery.is_file():
        prior = base.load(recovery)
        assert prior["candidate_sha256"] == candidate
        assert {Path(row["path"]): row["sha256"] for row in prior["removed"]} == discard
        assert all(not path.exists() for path in discard)
        return {}
    return discard


main_source = checked_text(getsource(template.main), {
    '"release_stack_with_parallel_ship_lessons.json"': '"release_stack_with_rafael_fernando_coin_game.json"',
    '    roots = tuple(folder.resolve() for folder in (release.ROOT, stage.ROOT))':
        '    discard.update(preliminary_captures(retained))\n'
        '    assert all(base.digest(path) == digest for path, digest in retained.items())\n'
        '    roots = tuple(folder.resolve() for folder in (release.ROOT, stage.ROOT))',
})
scope = vars(template) | globals()
exec(compile(main_source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
