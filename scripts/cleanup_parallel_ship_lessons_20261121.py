"""Remove only disposable non-ROM staging files after release and Drive verification."""
from gzip import open as open_gzip
from hashlib import file_digest
from pathlib import Path

from scripts import register_parallel_ship_lessons_20261121 as release


base, stage = release.base, release.stage
TEST_ARTIFACTS = {"change.xdelta", "clean.dat", "modified.dat", "rebuilt.dat", "release_manifest.json", "wrong.dat"}


def main():
    state = base.load(release.VERIFY / "registration_mutation_plan.json")
    published = base.load(release.ROOT / "drive_latest_build_receipt.json")
    manifest = base.load(release.RELEASE)
    candidate = manifest["candidate_sha256"]
    assert published["sole_nds_in_folder"] and published["readback_verified"] and published["sha256"] == candidate
    assert base.digest(base.LEDGER) == state["ledger_after"]
    assert base.digest(base.REGISTRY) == state["registry_after"]
    assert base.digest(base.PROMOTED) == state["main_sha256"]
    assert base.load(release.PACKAGE / "checksums.json") == release.workflow.package_checksums(release.PACKAGE)

    fixture = base.load(release.live.replay.ROOT / "fixture.json")
    retained = {stage.ROM: candidate, release.ROM: candidate, stage.ROOT / "clean_rebuilt.nds": candidate,
                release.PATCH: manifest["patch_sha256"], release.MANIFEST: manifest["manifest_sha256"],
                Path(fixture["fixture"]): fixture["fixture_sha256"]}
    for proof in (release.display.PROOF, release.live.PROOF):
        for sheet in base.load(proof)["sheets"]:
            retained[Path(sheet["path"])] = sheet["sha256"]
    assert all(base.digest(path) == digest for path, digest in retained.items())

    target = release.ROOT / "checkpoint_cleanup.json"
    assert not target.exists()
    with open_gzip(release.ROOT / "editorial_ledger_before.json.gz", "rb") as compressed:
        assert file_digest(compressed, "sha256").hexdigest() == state["ledger_before"]
    discard = {release.ROOT / name: digest for name, digest in (
        ("ledger_before.json", state["ledger_before"]), ("ledger_after.json", state["ledger_after"]),
        ("release_stack_with_parallel_ship_lessons.json", state["registry_after"]))}
    timing = release.live.replay.ROOT / "timing_scratch.png"
    if timing.is_file():
        discard[timing] = base.digest(timing)
    test_dir = stage.ROOT / "pytest_tmp"
    for path in test_dir.glob("test_*/*"):
        if path.name in TEST_ARTIFACTS and path.resolve().parent.parent == test_dir.resolve():
            discard[path] = base.digest(path)
    roots = tuple(folder.resolve() for folder in (release.ROOT, stage.ROOT))
    assert {p.resolve() for p in discard}.isdisjoint(p.resolve() for p in retained)
    removed = []
    for path, digest in discard.items():
        assert any(path.resolve().is_relative_to(root) for root in roots)
        assert path.suffix.lower() != ".nds" and path.is_file() and not path.is_symlink() and not path.is_junction()
        assert base.digest(path) == digest
        removed.append(dict(path=str(path), sha256=digest, bytes=path.stat().st_size))
    for path in discard:
        path.unlink()
    assert all(base.digest(path) == digest for path, digest in retained.items())
    reclaimed = sum(row["bytes"] for row in removed)
    base.save(target, dict(removed=removed, reclaimed_bytes=reclaimed, registered_candidate_sha256=candidate,
                           verified_retained_evidence=len(retained)))
    print(f"Removed {len(removed)} redundant files and reclaimed {reclaimed:,} bytes.")


if __name__ == "__main__":
    main()
