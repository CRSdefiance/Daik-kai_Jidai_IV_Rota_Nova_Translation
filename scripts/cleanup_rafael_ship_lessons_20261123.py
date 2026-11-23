"""Archive the wrap queue and remove verified duplicates for the new testing build."""

from shutil import copyfile

from scripts import cleanup_rafael_basra_and_map_keys_20261123 as prior
from scripts import register_rafael_ship_lessons_20261123 as current
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = current.base, current.stage
QUEUE = stage.BATCH / "current_wrap_queue.json"
CHECKPOINT_DIR = stage.paired.OUTPUT.parent
DRIVE = current.ROOT / "drive_latest_build_receipt.json"
RECEIPT = current.ROOT / "checkpoint_cleanup.json"
CLEANUP_PLAN = current.ROOT / "checkpoint_cleanup_plan.json"
REVIEW_COUNT = 26
all_reviews = "(" + ", ".join("current" + ".parent" * depth + ".REVIEW"
                             for depth in range(REVIEW_COUNT - 1, -1, -1)) + ")"
contents = checked_text(prior.refresh, {prior.all_reviews: all_reviews})
queue_scope = prior.queue_scope | dict(current=current, OUTPUT=QUEUE)
exec(compile(contents, __file__ + "::current-wrap-queue", "exec"), queue_scope)


def cleanup():
    release, drive = map(base.load, (current.RELEASE, DRIVE))
    assert release["clean_input_patch_byte_exact"] and release["whole_parent_inverse_exact"]
    assert drive["readback_verified"] and drive["sole_nds_in_folder"]
    candidate, patch = release["candidate_sha256"], release["patch_sha256"]
    assert candidate == drive["sha256"]
    assert base.digest(current.ROM) == candidate and base.digest(current.PATCH) == patch
    assert base.digest(current.MANIFEST) == release["manifest_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    parent = base.load(current.parent.RELEASE)
    assert current.parent.ROM.is_file() and base.digest(current.parent.ROM) == parent["candidate_sha256"]
    pins = {row["path"] for row in base.load(base.REGISTRY.parent / "rom_retention_pins.json")}
    retired = ((stage.ROM, current.ROM, candidate), (stage.REBUILT, current.ROM, candidate),
               (stage.PATCH, current.PATCH, patch))
    allowed = {stage.ROOT.resolve()}
    first_attempt = stage.BATCH.parent / "first_registration"
    if first_attempt.is_dir():
        superseded_rom = first_attempt / current.ROOT.name / current.ROM.name
        superseded_patch = first_attempt / current.PACKAGE.name / current.PATCH.name
        retired += ((superseded_rom, current.ROM, candidate), (superseded_patch, current.PATCH, patch))
        for source in (superseded_rom, superseded_patch):
            assert source.parent.resolve().is_relative_to(first_attempt.resolve())
            allowed.add(source.parent.resolve())
    if not CLEANUP_PLAN.exists():
        entries = []
        for source, target, digest in retired:
            assert base.digest(source) == base.digest(target) == digest
            entries.append(dict(path=str(source), kept=str(target), sha256=digest, bytes=source.stat().st_size))
        base.save(CLEANUP_PLAN, dict(candidate_sha256=candidate, entries=entries))
    plan = base.load(CLEANUP_PLAN)
    assert plan["candidate_sha256"] == candidate
    removed = plan["entries"]
    for (source, target, digest), entry in zip(retired, removed, strict=True):
        assert source.resolve().parent in allowed and not source.is_symlink()
        assert str(source.resolve()) not in pins and source.resolve() != target.resolve()
        assert (str(source), str(target), digest) == (entry["path"], entry["kept"], entry["sha256"])
        assert base.digest(target) == digest and target.stat().st_size == entry["bytes"]
        if source.exists():
            assert base.digest(source) == digest
            source.unlink()
    assert base.digest(current.ROM) == candidate and base.digest(current.PATCH) == patch
    base.save(RECEIPT, dict(candidate_sha256=candidate, removed=removed,
                           reclaimed_bytes=sum(row["bytes"] for row in removed)))


def handoff():
    drive, queue, receipt = map(base.load, (DRIVE, QUEUE, RECEIPT))
    release = base.load(current.RELEASE)
    candidate = release["candidate_sha256"]
    assert candidate == drive["sha256"] == queue["candidate_sha256"] == receipt["candidate_sha256"]
    for proof in (DRIVE, QUEUE, RECEIPT):
        target = CHECKPOINT_DIR / proof.name
        if not target.exists():
            copyfile(proof, target)
        assert base.digest(target) == base.digest(proof)
    open_wraps = sum("reviewed" not in row for row in queue["records"])
    stub = f"# Current editorial checkpoint - 2026-11-23\n\n{current.CHECKPOINT} [Checkpoint]({current.DOC.name})\n\n"
    section = (stub + f"""The registered review covers 217 texts across five Rafael exchanges. Sixteen wording changes and four wrap-only revisions address eleven queued records and nearby breaks. The ledger records 189 dialogue and notice retentions, eight unchanged captions and eleven localized names or roles. All 20 revised pages and the extra-armor notice passed native checks. Focused emulation verified 15 fresh holds and carried forward 17 exact prior holds, including both sailing choices. Natural story activation and handheld testing remain open. [Exact review](../{current.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. The cumulative release passed its cold boot, 17 focused tests and an exact clean-input patch round trip. Cleanup removed {len(receipt['removed'])} verified duplicates and reclaimed {receipt['reclaimed_bytes']:,} bytes. [Latest testing build]({drive["url"]}) · [Clean-input patch](../{current.PATCH.as_posix()}) · [Cleanup receipt](../{(CHECKPOINT_DIR / RECEIPT.name).as_posix()})

The refreshed scan has {open_wraps} open wrap leads. Jam's B176 R0040 still divides “True story” across lines in the new layout. Carry that visual finding into the next wrap pass. Continue the full contextual review, ordinary town and random gameplay samples, and the 276 shared display leads. Preserve the 27,700 historical credits, separate artwork work and later older-record technical re-audit. [Current wrap queue](../{(CHECKPOINT_DIR / QUEUE.name).as_posix()})

""").encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = current.DOC.with_name(name)
        old = path.read_bytes()
        if not old.startswith(section):
            assert old.startswith(stub.encode())
            base.replace_checked(path, section + old.removeprefix(stub.encode()))
    print(f"Retained {open_wraps} open scan leads. Reclaimed {receipt['reclaimed_bytes']:,} duplicate bytes.")


if __name__ == "__main__":
    if not QUEUE.exists():
        queue_scope["main"]()
    if not RECEIPT.exists():
        cleanup()
    handoff()
