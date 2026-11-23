"""Recover the original Sound Setup registration transaction after interrupted compression."""

from gzip import open as open_gzip
from hashlib import file_digest
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.register_sound_play_stop_20261123 import (
    ARM, COMMON, DOC, MANIFEST, PACKAGE, PATCH, PROFILE, REBUILT, RELEASE,
    RESEARCH_PATCH, REVIEW, ROM, ROOT, VERIFY, WORK, base, build, parent, scope, stage,
)


def resume_prepared():
    """Continue the qualified transaction after the package compression ran out of disk space."""
    previous, stored, draft, saved_release = map(base.load, (parent.RELEASE, stage.PROOF, REVIEW, RELEASE))
    candidate = stored["candidate_sha256"]
    assert saved_release["candidate_sha256"] == candidate == base.digest(ROM) == base.digest(stage.ROM)
    assert ROM.samefile(REBUILT) and ROM.samefile(stage.ROM)
    assert base.digest(PATCH) == saved_release["patch_sha256"] == base.digest(RESEARCH_PATCH)
    assert base.digest(MANIFEST) == saved_release["manifest_sha256"]
    snapshot = dict(registry_before=base.digest(base.REGISTRY), ledger_before=base.digest(base.LEDGER),
                    main_sha256=base.digest(base.PROMOTED))
    assert snapshot["registry_before"] == previous["registry_sha256"]
    registry_backup, registry_next = (WORK / f"release_stack_{form}_sound_play_stop.json" for form in ("before", "with"))
    ledger_backup, ledger_next = WORK / "ledger_before.json", WORK / "ledger_after.json"
    assert base.digest(registry_backup) == snapshot["registry_before"]
    assert base.digest(ledger_backup) == snapshot["ledger_before"]
    registry_sha = base.digest(registry_next)
    assert registry_sha == saved_release["registry_sha256"]
    with scope["mapped"](registry_next) as data:
        assert scope["value"](data, PROFILE, 4)["verified_pirate_affiliation_predecessor"] == saved_release["predecessor"]
    with scope["mapped"](MANIFEST) as data:
        assert scope["value"](data, "candidate_sha256", 2) == candidate
        assert scope["value"](data, "release_stack_sha256", 2) == registry_sha
        assert len(scope["value"](data, "batches", 2)) == 1100
    validate_natural_dialogue_batch(draft)
    assert all(base.digest(path) == h for path, h in (draft["visual_review"] | draft["evidence"]).items())
    for archive_path, original in ((PACKAGE / "build_manifest.json.gz", MANIFEST),
                                   (PACKAGE / "build_release_stack.json.gz", registry_next)):
        with open_gzip(archive_path, "rb") as stream:
            assert file_digest(stream, "sha256").hexdigest() == base.digest(original)
    assert not any(p.exists() for p in (ledger_next, VERIFY / "registration_mutation_plan.json", DOC))
    partial = ROOT / "editorial_ledger_before.json.gz"
    assert partial.resolve().parent == ROOT.resolve() and not partial.is_symlink()
    receipt = VERIFY / "interrupted_ledger_archive_recovery.json"
    if not receipt.exists():
        try:
            with open_gzip(partial, "rb") as stream:
                payload_sha256 = file_digest(stream, "sha256").hexdigest()
        except EOFError:
            payload_sha256 = None
        if payload_sha256 != snapshot["ledger_before"]:
            base.save(receipt, dict(incomplete_archive_bytes=partial.stat().st_size,
                incomplete_archive_sha256=base.digest(partial), failure="Insufficient disk space during compression.",
                preserved_raw_ledger_sha256=snapshot["ledger_before"],
                stage_and_registered_ROM_identical_hardlinks=True,
                recovery_script_sha256=base.digest(Path(__file__))))
            partial.unlink()
    if not partial.exists():
        scope["archive"](ledger_backup, partial)
    with open_gzip(partial, "rb") as stream:
        assert file_digest(stream, "sha256").hexdigest() == snapshot["ledger_before"]
    archives = {ARM: saved_release["target_ARM9_sha256"], COMMON: saved_release["target_COMMON_sha256"]}
    start = build.index("    with mapped(base.LEDGER) as data:")
    names = ("snapshot", "previous", "stored", "draft", "candidate", "archives", "registry_sha",
             "registry_backup", "registry_next", "ledger_backup", "ledger_next", "release")
    header = "def finish(" + ", ".join(names) + "):\n"
    environment, prepared = scope.copy(), locals() | {"release": saved_release}
    exec(compile(header + build[start:], __file__ + "::finish-prepared-package", "exec"), environment)
    environment["finish"](*(prepared[key] for key in names))


if __name__ == "__main__":
    resume_prepared()
