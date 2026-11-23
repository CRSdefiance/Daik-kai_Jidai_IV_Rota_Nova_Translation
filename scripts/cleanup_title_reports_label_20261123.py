"""Record the verified Drive copy and remove redundant build paths."""

from pathlib import Path
from shutil import copyfile

from scripts import register_title_reports_label_20261123 as current


base, stage = current.base, current.stage
DRIVE = current.ROOT / "drive_latest_build_receipt.json"
RECEIPT = current.ROOT / "checkpoint_cleanup.json"
CLEANUP_PLAN = current.ROOT / "checkpoint_cleanup_plan.json"
OUTPUT = Path("translations/editorial_checkpoints/title_reports_label_20261123")


def cleanup():
    release, drive = map(base.load, (current.RELEASE, DRIVE))
    candidate = release["candidate_sha256"]
    patch = release["patch_sha256"]
    assert drive["readback_verified"] and drive["sole_nds_in_folder"] and drive["sha256"] == candidate
    assert release["clean_input_patch_byte_exact"] and release["whole_parent_inverse_exact"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(current.MANIFEST) == release["manifest_sha256"]
    assert base.digest(current.parent.ROM) == release["predecessor"]["candidate_sha256"]
    pins = {row["path"] for row in base.load(base.REGISTRY.parent / "rom_retention_pins.json")}
    pairs = (
        (stage.ROM, current.ROM, candidate),
        (stage.REBUILT, current.ROM, candidate),
        (stage.PATCH, current.PATCH, patch),
    )
    expected = []
    for source, target, sha in pairs:
        assert source.resolve().parent == stage.ROOT.resolve() and not source.is_symlink()
        assert source.resolve() != target.resolve() and str(source.resolve()) not in pins
        assert base.digest(target) == sha
        expected.append(dict(path=str(source), kept=str(target), sha256=sha, bytes=target.stat().st_size))

    plan = dict(candidate_sha256=candidate, entries=expected)
    if not CLEANUP_PLAN.exists():
        assert all(base.digest(source) == sha for source, _, sha in pairs)
        base.save(CLEANUP_PLAN, plan)
    assert base.load(CLEANUP_PLAN) == plan
    for source, _, sha in pairs:
        if source.exists():
            assert base.digest(source) == sha
            source.unlink()
    assert all(base.digest(target) == sha for _, target, sha in pairs)
    base.save(RECEIPT, dict(candidate_sha256=candidate, removed=expected,
        removed_entry_bytes=sum(row["bytes"] for row in expected), accounting="Logical sizes include a hardlinked ROM."))


def handoff():
    release, drive, receipt = map(base.load, (current.RELEASE, DRIVE, RECEIPT))
    candidate = release["candidate_sha256"]
    assert candidate == drive["sha256"] == receipt["candidate_sha256"]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for record in (DRIVE, RECEIPT):
        target = OUTPUT / record.name
        if not target.exists():
            copyfile(record, target)
        assert base.digest(record) == base.digest(target)
    stub = f"# Current editorial checkpoint - 2026-11-23\n\n{current.CHECKPOINT} [Checkpoint]({current.DOC.name})\n\n"
    section = (stub + f"""The title Options menu now says Reports, matching the confirmation and in-game label. The complete label passed ten highlighted or plain holds. Six prompt holds verified both On/Off orders and the effect of cancellation. Twenty offline cases checked preference changes and preservation of unrelated bits. The replay also restored both volume meters and returned to the title. The review retains four labels or prompts with individual reasons. Audio output and handheld testing remain unverified. [Exact review and scope](../{current.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. Cold startup, all 17 focused tests and exact clean-input reconstruction passed. Cleanup removed {len(receipt['removed'])} checked redundant build paths. [Latest testing build]({drive['url']}) · [Clean-input patch](../{current.PATCH.as_posix()}) · [Cleanup receipt](../{(OUTPUT / RECEIPT.name).as_posix()})

All 3,668 COMMON entries retain their bytes and locations. The five legacy Options keys were absent from the traced title flow and remain open for separate display paths. Continue with the 276 stored shared entries and practical ordinary town and random coverage. [Shared inventory](../{current.REVIEW.as_posix()})

""").encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = current.DOC.with_name(name)
        old = path.read_bytes()
        if not old.startswith(section):
            assert old.startswith(stub.encode())
            base.replace_checked(path, section + old.removeprefix(stub.encode()))
    print(f"Sealed {candidate} and removed {len(receipt['removed'])} verified redundant build paths.")


if __name__ == "__main__":
    if not RECEIPT.exists():
        cleanup()
    handoff()
