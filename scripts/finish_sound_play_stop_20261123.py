"""Finish the verified Sound Setup transaction from its retained overflow snapshots."""

from gzip import open as open_gzip
from hashlib import file_digest
from inspect import getsource
from os import fsync
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_sound_play_stop_20261123 as release
from scripts.source_locked_derivation_v5118 import checked_text


OVERFLOW = Path("E:/Rota Nova translations/Generated/work/sound_stop_registration_recovery_20261123")
PLAN = release.VERIFY / "registration_mutation_plan.json"
STORAGE = release.VERIFY / "generated_snapshot_storage.json"
BUF_SIZE = 1 << 20
base = release.base


def apply_snapshot(source, destination):
    """Keep unchanged compressed blocks in place during install or rollback."""
    expected = base.digest(source)
    if expected == base.digest(destination):
        return
    with source.open("rb") as original, destination.open("r+b") as live:
        pos = 0
        while payload := original.read(BUF_SIZE):
            live.seek(pos)
            if live.read(len(payload)) != payload:
                live.seek(pos)
                assert live.write(payload) == len(payload)
            pos += len(payload)
        if destination.stat().st_size != pos:
            live.truncate(pos)
        live.flush()
        fsync(live.fileno())
    assert base.digest(destination) == expected


def main():
    assert not release.DOC.exists() and not PLAN.exists()
    saved = base.load(OVERFLOW / "prepared_transaction_recovery.json")
    registered = base.load(release.RELEASE)
    previous = base.load(release.parent.RELEASE)
    draft = base.load(release.REVIEW)
    startup = base.load(release.VERIFY / "own_startup_verification.json")
    snapshot = dict(registry_before=base.digest(base.REGISTRY), ledger_before=base.digest(base.LEDGER),
                    main_sha256=base.digest(base.PROMOTED))
    assert snapshot["registry_before"] == previous["registry_sha256"] == saved["registry_before"]
    assert snapshot["ledger_before"] == saved["ledger_before"]
    candidate = saved["candidate_sha256"]
    assert candidate == registered["candidate_sha256"] == draft["candidate_sha256"] == startup["candidate_sha256"]
    assert candidate == base.digest(release.ROM) and release.ROM.samefile(release.REBUILT) and release.ROM.samefile(release.stage.ROM)
    assert base.digest(release.PATCH) == registered["patch_sha256"] and registered["clean_input_patch_byte_exact"]
    assert base.digest(release.MANIFEST) == registered["manifest_sha256"]
    assert base.digest(registered["own_registered_startup"]) == registered["own_registered_startup_sha256"]
    registry_next, ledger_next = (Path(saved[k]) for k in ("exact_prepared_registry", "exact_prepared_ledger"))
    assert all(p.resolve().parent == OVERFLOW.resolve() for p in (registry_next, ledger_next))
    registry_sha = base.digest(registry_next)
    assert registry_sha == saved["registry_after"] == registered["registry_sha256"]
    assert base.digest(ledger_next) == saved["ledger_after"]
    archive = OVERFLOW / "editorial_ledger_before.json.gz"
    archive_pairs = ((archive, snapshot["ledger_before"]),
                     (release.PACKAGE / "build_manifest.json.gz", registered["manifest_sha256"]),
                     (release.PACKAGE / "build_release_stack.json.gz", registry_sha))
    for path, expected in archive_pairs:
        with open_gzip(path, "rb") as stream:
            assert file_digest(stream, "sha256").hexdigest() == expected

    namespace = release.scope.copy()
    mapped, value = (namespace[key] for key in ("mapped", "value"))
    with mapped(release.MANIFEST) as data:
        assert value(data, "candidate_sha256", 2) == candidate
        assert value(data, "release_stack_sha256", 2) == registry_sha
        assert len(value(data, "batches", 2)) == 1100
        node = value(data, "sound_play_stop_pipeline", 2)
        assert node["registration_driver_sha256"] == base.digest(Path(release.__file__))
        assert node["registered_review_sha256"] == base.digest(release.REVIEW)
    with mapped(registry_next) as data:
        profile = value(data, release.PROFILE, 4)
        assert profile["verified_pirate_affiliation_predecessor"] == registered["predecessor"]
    with mapped(ledger_next) as data:
        assert value(data, "current_integrated_candidate", 1)["sha256"] == candidate
        assert value(data, "records_editorially_completed", 1) == 27700
        assert not value(data, "full_goal_complete", 1)
    validate_natural_dialogue_batch(draft)
    assert all(base.digest(p) == h for p, h in (draft["visual_review"] | draft["evidence"]).items())

    base.save(STORAGE, dict(candidate_sha256=candidate, registry_snapshot=str(registry_next), registry_sha256=registry_sha,
        ledger_snapshot=str(ledger_next), ledger_sha256=saved["ledger_after"], predecessor_ledger_archive=str(archive),
        predecessor_ledger_archive_sha256=base.digest(archive), older_C_snapshots_preserved=True,
        staging_ROM_hardlinked_to_registered_ROM=True, recovery_driver_sha256=base.digest(Path(__file__))))
    commit = checked_text(release.commit, {
        'registry_next = WORK / "release_stack_with_sound_play_stop.json"': 'registry_next = overflow_registry',
        'ledger_backup, ledger_next = WORK / "ledger_before.json", WORK / "ledger_after.json"':
            'ledger_backup, ledger_next = WORK / "ledger_before.json", overflow_ledger',
        'update_ledger_in_place(ledger_backup.read_bytes(), ledger_next.read_bytes())':
            'copy_in_place(ledger_next, base.LEDGER)',
    })
    namespace.update(overflow_registry=registry_next, overflow_ledger=ledger_next, copy_in_place=apply_snapshot)
    exec(compile(commit, __file__ + "::commit-overflow", "exec"), namespace)
    start = release.build.index('    base.save(VERIFY / "registration_mutation_plan.json"')
    header = "def finish(snapshot, registry_sha, ledger_next, candidate):\n"
    exec(compile(header + release.build[start:], __file__ + "::finish-prepared", "exec"), namespace)
    namespace["finish"](snapshot, registry_sha, ledger_next, candidate)
    assert base.digest(base.REGISTRY) == registry_sha and base.digest(base.LEDGER) == saved["ledger_after"]


if __name__ == "__main__":
    main()
