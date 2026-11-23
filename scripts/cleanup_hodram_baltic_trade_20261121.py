"""Clear verified registration and emulator duplicates while retaining all ROMs."""

from inspect import getsource
from pathlib import Path

from scripts import cleanup_parallel_ship_lessons_20261121 as template
from scripts import register_hodram_baltic_trade_20261121 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
replay = release.display.replay

main_source = checked_text(getsource(template.main), {
    '    fixture = base.load(release.live.replay.ROOT / "fixture.json")':
        '''    gameplay = base.load(release.live.PROOF)
    report = base.load(replay.REPORT)
    assert report["ROM_sha256"] == gameplay["candidate_sha256"] == candidate
    assert base.digest(replay.REPORT) == gameplay["evidence"][str(replay.REPORT)]
    assert base.digest(report["battery_save_preloaded"]["source"]) == report["battery_save_preloaded"]["source_sha256"]''',
    'Path(fixture["fixture"]): fixture["fixture_sha256"]}':
        '''replay.REPORT: base.digest(replay.REPORT),
                Path(gameplay["read_only_snapshot"]["path"]): gameplay["read_only_snapshot"]["sha256"]}''',
    '"release_stack_with_parallel_ship_lessons.json"': '"release_stack_with_hodram_baltic_trade.json"',
    '''    timing = release.live.replay.ROOT / "timing_scratch.png"
    if timing.is_file():
        discard[timing] = base.digest(timing)''':
        '''    planned_frames = set(base.load(replay.ROOT / "replay_scope.json")["frames"])
    for frame in report["frames_captured"]:
        path = Path(frame["path"])
        assert path.resolve().parent == replay.REPORT.parent.resolve() and path.suffix == ".png"
        if frame["frame"] in planned_frames and path.name.endswith("_cold_boot.png"):
            retained[path] = frame["PNG_sha256"]
        else:
            discard[path] = frame["PNG_sha256"]
    donor = report["battery_save_preloaded"]
    clone = Path(donor["destination"])
    assert clone.resolve().parent == replay.REPORT.parent.resolve() / "saves" and clone.suffix == ".dsv"
    if base.digest(clone) == donor["source_sha256"]:
        discard[clone] = donor["source_sha256"]''',
    '    removed = []': '''    assert all(base.digest(path) == digest for path, digest in retained.items())
    removed = []''',
})
scope = vars(template) | globals()
exec(compile(main_source, __file__, 'exec'), scope)


if __name__ == '__main__':
    scope['main']()
