"""Reclaim redundant refit and sailing artifacts after the verified release."""
from inspect import getsource
from pathlib import Path
import re

from scripts import cleanup_parallel_ship_lessons_20261121 as template
from scripts import register_rafael_refit_sailing_lessons_20261121 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage


def rehearsal_artifacts(retained):
    earlier = stage.ROOT.with_name("staged_v2")
    old_candidate = base.load(earlier / "stored_proof.json")["candidate_sha256"]
    old_rom = earlier / stage.ROM.name
    assert base.digest(old_rom) == old_candidate
    retained[old_rom] = old_candidate
    if (earlier / "clean_rebuilt.nds").exists():
        retained[earlier / "clean_rebuilt.nds"] = old_candidate
    captures = earlier / "focused_rafael/capture"
    report = base.load(captures / "capture_report.json")
    receipt = base.load(earlier / "focused_rafael/fixture.json")
    assert receipt["candidate_sha256"] == old_candidate and report["ROM_sha256"] == receipt["fixture_sha256"]
    retained[Path(receipt["fixture"])] = receipt["fixture_sha256"]
    discard = {}
    for info in report["frames_captured"]:
        path = Path(info["path"])
        assert path.resolve().parent == captures.resolve()
        if re.fullmatch(r"frame_\d{6}_(?:cold_boot|final)\.png", path.name):
            discard[path] = info["PNG_sha256"]
    sketch = earlier / "focused_rafael/timing_scratch.png"
    if sketch.is_file():
        discard[sketch] = base.digest(sketch)
    return discard


main_source = checked_text(getsource(template.main), {
    '"release_stack_with_parallel_ship_lessons.json"': '"release_stack_with_rafael_refit_sailing_lessons.json"',
    '    roots = tuple(folder.resolve() for folder in (release.ROOT, stage.ROOT))':
        '    discard.update(rehearsal_artifacts(retained))\n'
        '    assert all(base.digest(path) == digest for path, digest in retained.items())\n'
        '    roots = tuple(folder.resolve() for folder in (release.ROOT, stage.ROOT, stage.ROOT.with_name("staged_v2")))',
})
scope = vars(template) | globals()
exec(compile(main_source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
