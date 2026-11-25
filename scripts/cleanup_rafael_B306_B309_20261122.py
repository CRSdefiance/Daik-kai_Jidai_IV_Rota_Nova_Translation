"""Clear disposable files after publishing the verified Istanbul remedy candidate."""

from pathlib import Path

from scripts import cleanup_rafael_B261_B280_20261122 as precedent
from scripts import register_rafael_B306_B309_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage


def redundant_test_files(candidate_sha, patch_sha):
    failed = stage.ROOT / "startup/capture_default_options"
    report = failed / "capture_report.json"
    capture = base.load(report)
    assert capture["ROM_sha256"] == candidate_sha and not capture.get("battery_save_preloaded")
    assert capture["core_options"]["desmume_pointer_type"] == "mouse"
    good = base.load(release.STARTUP_CAPTURE)
    assert good["ROM_sha256"] == candidate_sha and good["core_options"]["desmume_pointer_type"] == "touch"
    discarded = {report: base.digest(report)}
    for shot in capture["frames_captured"]:
        path = failed / Path(shot["path"]).name
        assert path.resolve().parent == failed.resolve() and path.suffix == ".png"
        discarded[path] = shot["PNG_sha256"]
    snapshot = capture["read_only_RAM_snapshot"]
    assert Path(snapshot["path"]).name == "final_arm9_ram.bin"
    discarded[failed / "final_arm9_ram.bin"] = snapshot["sha256"]
    if (save := failed / "saves" / (stage.ROM.stem + ".dsv")).exists():
        assert save.resolve().parent == (failed / "saves").resolve()
        discarded[save] = base.digest(save)
    discarded[stage.ROOT / "clean_rebuilt.nds"] = candidate_sha
    discarded[stage.ROOT / "translation.xdelta"] = patch_sha
    return discarded


source = checked_text(precedent.source, {
    '"release_stack_with_rafael_B261_B280.json"': '"release_stack_with_rafael_B306_B309.json"',
    '    removed = []':
        '    discard.update(redundant_test_files(sha, manifest["patch_sha256"]))\n    removed = []',
    '{".json", ".png", ".dsv"}': '{".json", ".png", ".dsv", ".bin", ".nds", ".xdelta"}',
})
scope = precedent.scope | globals()
exec(compile(source, __file__ + "::verified-checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
