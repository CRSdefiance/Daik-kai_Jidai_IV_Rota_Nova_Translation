"""Seal the credits checkpoint after the verified Drive update."""

from os import link, replace
from pathlib import Path

from scripts import register_ending_credit_spacing_20261123 as current
from scripts import replay_ending_credit_spacing_20261123 as replay


base = current.base
OUTPUT = Path("translations/editorial_checkpoints/ending_credit_spacing_20261123")
DRIVE = "drive_latest_build_receipt.json"
CLEANUP = "checkpoint_cleanup.json"


def cleanup(release):
    folder = current.EVIDENCE.resolve(strict=True)
    kept = current.ROM.resolve(strict=True)
    candidate = release["candidate_sha256"]
    assert kept.is_relative_to(folder) and base.digest(kept) == candidate
    reclaimed, removed = 0, []
    staged = current.stage.ROM.resolve(strict=True)
    assert staged.parent == folder and base.digest(staged) == candidate
    earlier = folder / "early_duplicate_reclamation.json"
    if earlier.exists():
        proof = base.load(earlier)
        assert proof["candidate_sha256"] == candidate and staged.samefile(kept)
        assert proof["path"] == str(staged) and Path(proof["retained"]).samefile(kept)
        assert proof["bytes"] == staged.stat().st_size and proof["replaced_with_exact_hard_link"]
        reclaimed += proof["bytes"]
        removed.append(dict(path=str(staged), retained=str(kept), sha256=candidate,
            bytes=proof["bytes"], reason="Independent duplicate storage replaced by a hard link before registration."))
    if not staged.samefile(kept):
        duplicate_size = staged.stat().st_size
        replacement = staged.with_suffix(".hardlink")
        assert not replacement.exists()
        link(kept, replacement)
        assert replacement.samefile(kept)
        replace(replacement, staged)
        assert staged.samefile(kept) and base.digest(staged) == candidate
        removed.append(dict(path=str(staged), retained=str(kept), sha256=candidate,
            bytes=duplicate_size, reason="Independent duplicate storage replaced by a hard link."))
        reclaimed += duplicate_size
    for folder_name in (*[name.lower() for name in replay.CASES], "startup"):
        capture = current.EVIDENCE / folder_name / "capture/capture_report.json"
        report = base.load(capture)
        save = report.get("battery_save_preloaded")
        if not save or not Path(save["destination"]).exists():
            continue
        duplicate = Path(save["destination"]).resolve(strict=True)
        donor = Path(save["source"]).resolve(strict=True)
        assert duplicate.is_relative_to(folder) and duplicate.parent == capture.parent.resolve() / "saves"
        assert not duplicate.samefile(donor)
        sha = base.digest(duplicate)
        if sha != save["source_sha256"]:
            continue
        assert base.digest(donor) == sha
        size = duplicate.stat().st_size
        duplicate.unlink()
        removed.append(dict(path=str(duplicate), retained=str(donor), sha256=sha, bytes=size,
            reason="The temporary emulator save is byte-identical to the original donor."))
        reclaimed += size
    interrupted = {
        folder / "registration_failed_disk_01/registration/release_stack_with_ending_credit_spacing.json":
            current.WORK / "release_stack_with_ending_credit_spacing.json",
        folder / "interrupted_partial_manifest.json": current.MANIFEST,
        folder / "interrupted_partial_ledger.json": current.WORK / "ledger_after.json",
    }
    for partial, final in interrupted.items():
        if not partial.exists():
            continue
        assert partial.resolve(strict=True).is_relative_to(folder)
        size = partial.stat().st_size
        assert 0 < size < final.stat().st_size
        with partial.open("rb") as first, final.open("rb") as second:
            matches = all(second.read(len(chunk)) == chunk for chunk in iter(lambda: first.read(1 << 20), b""))
        if matches:
            removed.append(dict(path=str(partial), retained=str(final), sha256=base.digest(partial), bytes=size,
                reason="Interrupted output exactly matches a prefix of its completed counterpart."))
            partial.unlink()
            reclaimed += size
    return dict(candidate_sha256=candidate, removed_duplicate_storage=removed,
        logical_duplicate_bytes_reclaimed=reclaimed, retained_stage_path=True, unique_ROMs_preserved=True)


def main():
    release, drive = map(base.load, (current.RELEASE, current.ROOT / DRIVE))
    candidate = release["candidate_sha256"]
    assert candidate == drive["sha256"] and drive["readback_verified"] and drive["sole_nds_in_folder"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    base.save(OUTPUT / DRIVE, drive)
    if not (OUTPUT / CLEANUP).exists():
        base.save(OUTPUT / CLEANUP, cleanup(release))
    receipt = base.load(OUTPUT / CLEANUP)
    assert receipt["candidate_sha256"] == candidate
    stub = f"# Current editorial checkpoint - 2026-11-23\n\n{current.CHECKPOINT} [Checkpoint]({current.DOC.name})\n\n"
    section = (stub + f"""All four ending movies display **Special Thanks: BRIDGE Inc.** Four focused cold boots used the original ending selector and verified {current.observed_count()} whole credit frames across fade states, plus all four ending-save prompts. The original attribution and complete lettering passed visual and pixel checks. Earned completion and hardware remain unvisited in this batch. [Source and render evidence](../{current.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. Cold startup, all 17 focused tests and exact clean-input reconstruction passed. Cleanup recorded {len(receipt['removed_duplicate_storage'])} verified duplicate storage paths. [Latest testing build]({drive['url']}) · [Clean-input patch](../{current.PATCH.as_posix()}) · [Cleanup receipt](../{(OUTPUT / CLEANUP).as_posix()})

The 276 stored shared text entries still need their display paths resolved. The source and installed bytes of all four story archives, COMMON and ARM9 remain exact to the predecessor.

""").encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = current.DOC.with_name(name)
        old = path.read_bytes()
        if not old.startswith(section):
            assert old.startswith(stub.encode())
            base.replace_checked(path, section + old.removeprefix(stub.encode()))
    print(f"Sealed the verified Drive copy and reclaimed {receipt['logical_duplicate_bytes_reclaimed']:,} logical bytes.")


if __name__ == "__main__":
    main()
